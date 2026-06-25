#!/usr/bin/env python3
"""Generate grouped PDF chart-type overviews for the medical figure skill."""

from __future__ import annotations

import argparse
import csv
import math
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap

from medical_palette import (
    BAR_EDGE,
    DEFAULT_FAMILY,
    GRAY,
    LIGHT_GRAY,
    PALETTE_FAMILIES,
    display_palette,
    diverging_cmap as base_diverging_cmap,
    missingness_cmap as base_missingness_cmap,
    risk_bias_cmap as base_risk_bias_cmap,
    sequential_cmap as base_sequential_cmap,
)


DrawFunc = Callable[[plt.Axes, np.random.Generator], None]

ACTIVE_PALETTE = display_palette("bar")
ACTIVE_FAMILY = ACTIVE_PALETTE.name
PALETTE = list(ACTIVE_PALETTE.group)
BLUE, GREEN, CREAM, ORANGE, RED, PURPLE = ACTIVE_PALETTE.group[:6]
TEAL = ACTIVE_PALETTE.contrast[1]
RISK_BIAS_COLORS = ACTIVE_PALETTE.risk_bias

COMPOSITE_BOTTOM = 0.36
COMPOSITE_BASELINE = 0.43
COMPOSITE_TOP = 0.80
COMPOSITE_LABEL_Y = 0.835
COMPOSITE_NOTE_Y = 0.315
COMPACT_QUANT_BAR_WIDTH = 0.045

CATEGORY_DISPLAY_FAMILY = {
    "01_bar_charts": "bar",
    "02_line_longitudinal": "line",
    "03_distribution_paired": "distribution",
    "04_heatmaps_matrices": "heatmap",
    "05_diagnostic_prediction": "diagnostic",
    "06_survival_time_to_event": "survival",
    "07_effect_review": "effect_review",
    "08_flow_timeline": "flow",
    "09_biomarker_omics": "biomarker",
    "10_clinical_imaging_composites": "imaging",
    "11_global_health_economics": "economic",
}


def set_active_palette(display_family: str, manuscript_family: str | None = None) -> None:
    global ACTIVE_PALETTE, ACTIVE_FAMILY, PALETTE, BLUE, GREEN, CREAM, ORANGE, RED, PURPLE, TEAL, RISK_BIAS_COLORS
    ACTIVE_PALETTE = display_palette(display_family, manuscript_family)
    ACTIVE_FAMILY = ACTIVE_PALETTE.name
    PALETTE = list(ACTIVE_PALETTE.group)
    BLUE, GREEN, CREAM, ORANGE, RED, PURPLE = ACTIVE_PALETTE.group[:6]
    TEAL = ACTIVE_PALETTE.contrast[1]
    RISK_BIAS_COLORS = ACTIVE_PALETTE.risk_bias


def palette_for_category(category: "ChartCategory", override: str = "auto") -> str:
    if override != "auto":
        return override
    display_family = CATEGORY_DISPLAY_FAMILY.get(category.slug, "bar")
    return display_palette(display_family).name


def sequential_cmap(name: str = "medical_sequential") -> LinearSegmentedColormap:
    return base_sequential_cmap(name, family=ACTIVE_FAMILY)


def diverging_cmap(name: str = "medical_diverging") -> LinearSegmentedColormap:
    return base_diverging_cmap(name, family=ACTIVE_FAMILY)


def missingness_cmap():
    return base_missingness_cmap(family=ACTIVE_FAMILY)


def risk_bias_cmap():
    return base_risk_bias_cmap(family=ACTIVE_FAMILY)


@dataclass(frozen=True)
class ChartItem:
    slug: str
    label: str
    draw: DrawFunc


@dataclass(frozen=True)
class ChartCategory:
    slug: str
    title: str
    plain_name: str
    items: tuple[ChartItem, ...]


def configure_matplotlib() -> None:
    matplotlib.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.4,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.65,
            "xtick.major.width": 0.55,
            "ytick.major.width": 0.55,
            "xtick.major.size": 2.4,
            "ytick.major.size": 2.4,
            "legend.frameon": False,
            "patch.edgecolor": BAR_EDGE,
            "patch.force_edgecolor": True,
            "patch.linewidth": 0.35,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def tidy(ax: plt.Axes) -> None:
    ax.tick_params(labelsize=6.2)
    ax.grid(alpha=0.18, linewidth=0.5)


def letter_title(ax: plt.Axes, letter: str, title: str) -> None:
    ax.set_title(f"{letter}. {title}", loc="left", fontsize=7.8, fontweight="bold", pad=3)


def normal_sample(rng: np.random.Generator, center: float, spread: float, n: int = 80) -> np.ndarray:
    return rng.normal(center, spread, n)


def unit_canvas(ax: plt.Axes) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("auto")


def draw_image_box(
    ax: plt.Axes,
    image: np.ndarray,
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    *,
    cmap: str | LinearSegmentedColormap = "gray",
    vmin: float = 0,
    vmax: float = 1,
) -> None:
    ax.imshow(image, cmap=cmap, extent=(x0, x1, y0, y1), vmin=vmin, vmax=vmax, aspect="auto")


def draw_compact_quant_bars(
    ax: plt.Axes,
    x0: float,
    x1: float,
    *,
    values: tuple[float, float],
    labels: tuple[str, str] = ("Case", "Control"),
    title: str = "Quantification",
    note: str = "cells/image",
) -> None:
    ax.add_patch(
        patches.Rectangle(
            (x0, COMPOSITE_BOTTOM),
            x1 - x0,
            COMPOSITE_TOP - COMPOSITE_BOTTOM,
            ec=LIGHT_GRAY,
            fc="#FFFFFF",
            lw=0.7,
        )
    )
    ax.text(x0 + 0.02, COMPOSITE_TOP - 0.045, title, fontsize=6.2, fontweight="bold")
    usable_height = (COMPOSITE_TOP - COMPOSITE_BASELINE) * 0.70
    max_value = max(max(values), 1e-6)
    centers = np.linspace(x0 + 0.10, x1 - 0.10, len(values))
    for center, value, color in zip(centers, values, [BLUE, ORANGE]):
        height = usable_height * value / max_value
        ax.add_patch(
            patches.Rectangle(
                (center - COMPACT_QUANT_BAR_WIDTH / 2, COMPOSITE_BASELINE),
                COMPACT_QUANT_BAR_WIDTH,
                height,
                fc=color,
                ec=BAR_EDGE,
                lw=0.25,
            )
        )
    ax.text((x0 + x1) / 2, COMPOSITE_NOTE_Y, note, fontsize=5.8, ha="center")


def draw_simple_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    values = rng.uniform(0.22, 0.58, 4)
    ax.bar(np.arange(4), values, color=PALETTE[:4])
    ax.set_xticks(range(4), ["A", "B", "C", "D"])
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 0.7)
    tidy(ax)


def draw_grouped_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(4)
    width = 0.34
    a = rng.uniform(15, 35, 4)
    b = a + rng.normal(-4, 3, 4)
    ax.bar(x - width / 2, a, width, color=BLUE, label="Control")
    ax.bar(x + width / 2, b, width, color=ORANGE, label="Intervention")
    ax.set_xticks(x, ["T0", "T1", "T2", "T3"])
    ax.set_ylabel("%")
    ax.legend(fontsize=6, loc="upper right")
    tidy(ax)


def draw_grouped_bar_dense(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(4)
    labels = ["Control", "Dose A", "Dose B"]
    width = 0.22
    baseline = rng.uniform(18, 34, len(x))
    values = np.vstack(
        [
            baseline,
            baseline + rng.normal(-3.0, 2.2, len(x)),
            baseline + rng.normal(-6.0, 2.4, len(x)),
        ]
    )
    offsets = np.linspace(-width, width, len(labels))
    for idx, (label, offset, color) in enumerate(zip(labels, offsets, [BLUE, GREEN, ORANGE])):
        ax.bar(x + offset, values[idx], width, color=color, label=label)
    ax.set_xticks(x, ["Site 1", "Site 2", "Site 3", "Site 4"], rotation=15, ha="right")
    ax.set_ylabel("Event rate (%)")
    ax.legend(fontsize=5.7, loc="upper right")
    tidy(ax)


def draw_stacked_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(5)
    parts = rng.dirichlet([2.8, 1.8, 1.2], len(x)).T
    bottom = np.zeros(len(x))
    for values, color, label in zip(parts, [BLUE, TEAL, RED], ["Mild", "Moderate", "Severe"]):
        ax.bar(x, values * 100, bottom=bottom * 100, color=color, label=label)
        bottom += values
    ax.set_xticks(x, [f"G{i}" for i in range(1, 6)])
    ax.set_ylim(0, 100)
    ax.set_ylabel("%")
    ax.legend(fontsize=5.8, loc="upper right")
    tidy(ax)


def draw_horizontal_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["AE 1", "AE 2", "AE 3", "AE 4", "AE 5"]
    values = np.sort(rng.uniform(4, 28, len(labels)))
    ax.barh(np.arange(len(labels)), values, color=BLUE)
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("Events (%)")
    tidy(ax)


def draw_diverging_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["Age", "Lab", "Score", "Risk", "Cost"]
    values = rng.normal(0, 0.45, len(labels))
    colors = [BLUE if v < 0 else RED for v in values]
    ax.axvline(0, color="#222222", lw=0.8)
    ax.barh(np.arange(len(labels)), values, color=colors)
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("Difference")
    tidy(ax)


def draw_error_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(4)
    values = rng.uniform(0.25, 0.55, 4)
    err = rng.uniform(0.04, 0.08, 4)
    ax.bar(x, values, yerr=err, capsize=3, color=TEAL, ecolor="#222222")
    ax.set_xticks(x, ["Q1", "Q2", "Q3", "Q4"])
    ax.set_ylabel("Mean")
    ax.set_ylim(0, 0.75)
    tidy(ax)


def draw_lollipop(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["A", "B", "C", "D", "E", "F"]
    values = np.sort(rng.uniform(0.12, 0.62, len(labels)))
    ax.hlines(np.arange(len(labels)), 0, values, color=LIGHT_GRAY, lw=2)
    ax.scatter(values, np.arange(len(labels)), color=BLUE, s=22)
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("Rate")
    ax.set_xlim(0, 0.7)
    tidy(ax)


def draw_percent_stacked(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(4)
    vals = rng.dirichlet([2.5, 2.0, 1.2, 0.8], len(x)).T
    bottom = np.zeros(len(x))
    for v, c in zip(vals, [BLUE, TEAL, ORANGE, RED]):
        ax.bar(x, v * 100, bottom=bottom * 100, color=c)
        bottom += v
    ax.set_xticks(x, ["Low", "Med", "High", "Very"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("%")
    tidy(ax)


def draw_waterfall(ax: plt.Axes, rng: np.random.Generator) -> None:
    change = np.sort(rng.normal(-8, 18, 22))
    colors = [BLUE if x < 0 else RED for x in change]
    ax.axhline(0, color="#222222", lw=0.7)
    ax.bar(np.arange(len(change)), change, color=colors, width=0.8)
    ax.set_xticks([])
    ax.set_ylabel("Change (%)")
    tidy(ax)


def draw_tornado_bar(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["Effect", "Cost", "Rate", "Utility", "Time"]
    low = -np.sort(rng.uniform(0.08, 0.35, len(labels)))[::-1]
    high = np.sort(rng.uniform(0.08, 0.35, len(labels)))[::-1]
    y = np.arange(len(labels))
    ax.barh(y, low, color=BLUE, alpha=0.8)
    ax.barh(y, high, color=ORANGE, alpha=0.8)
    ax.axvline(0, color="#222222", lw=0.8)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Impact")
    ax.invert_yaxis()
    tidy(ax)


def draw_single_line(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(8)
    y = 0.35 + np.cumsum(rng.normal(0.03, 0.035, len(x)))
    ax.plot(x, y, marker="o", color=BLUE)
    ax.set_xlabel("Visit")
    ax.set_ylabel("Mean")
    tidy(ax)


def draw_multi_line(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(8)
    for idx, color in enumerate([BLUE, ORANGE, TEAL]):
        y = 0.25 + idx * 0.08 + np.cumsum(rng.normal(0.02, 0.025, len(x)))
        ax.plot(x, y, marker="o", ms=2.5, color=color, label=f"G{idx + 1}")
    ax.legend(fontsize=6)
    ax.set_xlabel("Visit")
    tidy(ax)


def draw_ribbon_line(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(12)
    y = 0.35 + 0.03 * x + 0.05 * np.sin(x / 1.8)
    band = 0.05 + 0.01 * np.cos(x)
    ax.fill_between(x, y - band, y + band, color=BLUE, alpha=0.22)
    ax.plot(x, y, color=BLUE)
    ax.set_xlabel("Month")
    ax.set_ylabel("Estimate")
    tidy(ax)


def draw_spaghetti(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(7)
    traces = []
    for _ in range(28):
        y = 0.55 + np.cumsum(rng.normal(-0.015, 0.035, len(x)))
        traces.append(y)
        ax.plot(x, y, color="#CBD5E1", lw=0.6)
    mean = np.vstack(traces).mean(axis=0)
    ax.plot(x, mean, color=BLUE, lw=2.0, label="Mean")
    ax.set_xlabel("Visit")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_step_line(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(0, 13)
    y = np.cumsum(rng.poisson(3, len(x)))
    ax.step(x, y, where="post", color=ORANGE)
    ax.set_xlabel("Month")
    ax.set_ylabel("Events")
    tidy(ax)


def draw_cumulative_line(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(10)
    for idx, color in enumerate([BLUE, RED]):
        events = np.cumsum(rng.uniform(0.01, 0.045, len(x))) + idx * 0.015
        ax.plot(x, np.clip(events, 0, 0.5), color=color, label=f"Group {idx + 1}")
    ax.set_ylabel("Cumulative risk")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_slope_chart(ax: plt.Axes, rng: np.random.Generator) -> None:
    baseline = rng.uniform(35, 62, 7)
    follow = baseline + rng.normal(-6, 5, 7)
    for b, f in zip(baseline, follow):
        ax.plot([0, 1], [b, f], color="#CBD5E1", lw=1)
    ax.scatter(np.zeros_like(baseline), baseline, color=BLUE, s=16)
    ax.scatter(np.ones_like(follow), follow, color=ORANGE, s=16)
    ax.set_xticks([0, 1], ["Before", "After"])
    ax.set_ylabel("Score")
    tidy(ax)


def draw_event_annotation_line(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(14)
    y = 0.48 + 0.02 * x + 0.05 * np.sin(x / 1.7)
    ax.plot(x, y, color=BLUE)
    ax.axvline(6, color=RED, ls="--", lw=0.9)
    ax.text(6.2, max(y) - 0.02, "Index", fontsize=6.4, color=RED)
    ax.set_xlabel("Week")
    tidy(ax)


def draw_histogram(ax: plt.Axes, rng: np.random.Generator) -> None:
    values = normal_sample(rng, 52, 10, 160)
    ax.hist(values, bins=16, color=BLUE, alpha=0.78)
    ax.set_xlabel("Biomarker")
    ax.set_ylabel("Count")
    tidy(ax)


def draw_density(ax: plt.Axes, rng: np.random.Generator) -> None:
    grid = np.linspace(15, 85, 160)
    for center, color, label in [(44, BLUE, "A"), (56, ORANGE, "B")]:
        sample = normal_sample(rng, center, 9, 220)
        density = np.exp(-0.5 * ((grid[:, None] - sample[None, :]) / 4.5) ** 2).mean(axis=1)
        density /= density.max()
        ax.plot(grid, density, color=color, label=label)
        ax.fill_between(grid, 0, density, color=color, alpha=0.13)
    ax.set_yticks([])
    ax.legend(fontsize=6)
    tidy(ax)


def draw_boxplot(ax: plt.Axes, rng: np.random.Generator) -> None:
    data = [normal_sample(rng, m, 7, 80) for m in [48, 52, 57]]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55)
    for patch, color in zip(bp["boxes"], [BLUE, ORANGE, TEAL]):
        patch.set(facecolor=color, alpha=0.65)
    ax.set_xticks([1, 2, 3], ["A", "B", "C"])
    ax.set_ylabel("Value")
    tidy(ax)


def draw_violin(ax: plt.Axes, rng: np.random.Generator) -> None:
    data = [normal_sample(rng, m, s, 90) for m, s in [(45, 8), (55, 7), (60, 10)]]
    vp = ax.violinplot(data, showmeans=False, showmedians=True)
    for body, color in zip(vp["bodies"], [BLUE, ORANGE, TEAL]):
        body.set_facecolor(color)
        body.set_alpha(0.55)
        body.set_edgecolor("none")
    ax.set_xticks([1, 2, 3], ["A", "B", "C"])
    ax.set_ylabel("Value")
    tidy(ax)


def draw_strip(ax: plt.Axes, rng: np.random.Generator) -> None:
    for idx, color in enumerate([BLUE, ORANGE, TEAL]):
        y = normal_sample(rng, 48 + 5 * idx, 6, 42)
        x = rng.normal(idx + 1, 0.045, len(y))
        ax.scatter(x, y, s=10, color=color, alpha=0.75)
    ax.set_xticks([1, 2, 3], ["A", "B", "C"])
    ax.set_ylabel("Value")
    tidy(ax)


def draw_paired_distribution(ax: plt.Axes, rng: np.random.Generator) -> None:
    n = 34
    before = normal_sample(rng, 55, 7, n)
    after = before + rng.normal(-5, 5, n)
    for b, a in zip(before, after):
        ax.plot([0, 1], [b, a], color="#CBD5E1", lw=0.75)
    ax.scatter(np.zeros(n), before, color=BLUE, s=12)
    ax.scatter(np.ones(n), after, color=ORANGE, s=12)
    ax.set_xticks([0, 1], ["Base", "Follow"])
    tidy(ax)


def draw_ecdf(ax: plt.Axes, rng: np.random.Generator) -> None:
    for center, color, label in [(45, BLUE, "A"), (55, ORANGE, "B")]:
        x = np.sort(normal_sample(rng, center, 8, 90))
        y = np.arange(1, len(x) + 1) / len(x)
        ax.step(x, y, where="post", color=color, label=label)
    ax.set_ylabel("Cumulative")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_ridgeline(ax: plt.Axes, rng: np.random.Generator) -> None:
    grid = np.linspace(10, 90, 160)
    for idx, color in enumerate([BLUE, ORANGE, TEAL, RED]):
        sample = normal_sample(rng, 38 + idx * 8, 7, 150)
        density = np.exp(-0.5 * ((grid[:, None] - sample[None, :]) / 4.8) ** 2).mean(axis=1)
        density = density / density.max() * 0.75 + idx
        ax.fill_between(grid, idx, density, color=color, alpha=0.36)
        ax.plot(grid, density, color=color, lw=0.9)
    ax.set_yticks(range(4), ["G1", "G2", "G3", "G4"])
    tidy(ax)


def draw_heatmap(ax: plt.Axes, rng: np.random.Generator) -> None:
    mat = rng.normal(0, 1, (8, 8))
    ax.imshow(mat, cmap=diverging_cmap(), vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(8), [f"S{i}" for i in range(1, 9)], rotation=45, ha="right")
    ax.set_yticks(range(8), [f"F{i}" for i in range(1, 9)])
    ax.grid(False)


def draw_annotated_heatmap(ax: plt.Axes, rng: np.random.Generator) -> None:
    mat = rng.integers(0, 20, (5, 5))
    ax.imshow(mat, cmap=sequential_cmap(), aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, str(mat[i, j]), ha="center", va="center", fontsize=6)
    ax.set_xticks(range(5), [f"C{i}" for i in range(1, 6)])
    ax.set_yticks(range(5), [f"R{i}" for i in range(1, 6)])
    ax.grid(False)


def draw_missingness(ax: plt.Axes, rng: np.random.Generator) -> None:
    prob = np.array([0.03, 0.12, 0.18, 0.06, 0.24, 0.10])
    mat = rng.random((40, len(prob))) < prob
    ax.imshow(mat, cmap=missingness_cmap(), aspect="auto")
    ax.set_xticks(range(len(prob)), ["Age", "Lab", "Index", "FU", "Cost", "Rx"], rotation=35, ha="right")
    ax.set_yticks([])
    ax.grid(False)


def draw_confusion(ax: plt.Axes, rng: np.random.Generator) -> None:
    mat = np.array([[84, 10, 4], [12, 72, 16], [3, 17, 82]])
    ax.imshow(mat, cmap=sequential_cmap())
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(mat[i, j]), ha="center", va="center", fontsize=6)
    ax.set_xticks(range(3), ["Low", "Med", "High"], rotation=25, ha="right")
    ax.set_yticks(range(3), ["Low", "Med", "High"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.grid(False)


def draw_risk_bias(ax: plt.Axes, rng: np.random.Generator) -> None:
    vals = rng.choice([0, 1, 2], size=(7, 5), p=[0.58, 0.28, 0.14])
    cmap = risk_bias_cmap()
    ax.imshow(vals, cmap=cmap, vmin=-0.5, vmax=2.5, aspect="auto")
    ax.set_xticks(range(5), ["D1", "D2", "D3", "D4", "D5"])
    ax.set_yticks(range(7), [f"S{i}" for i in range(1, 8)])
    ax.grid(False)
    for x, lab, col in [(0.05, "Low", RISK_BIAS_COLORS[0]), (0.38, "Some", RISK_BIAS_COLORS[1]), (0.75, "High", RISK_BIAS_COLORS[2])]:
        ax.add_patch(patches.Rectangle((x, -0.18), 0.07, 0.055, transform=ax.transAxes, fc=col, ec="none", clip_on=False))
        ax.text(x + 0.085, -0.155, lab, transform=ax.transAxes, fontsize=5.8, va="center", clip_on=False)


def draw_correlation(ax: plt.Axes, rng: np.random.Generator) -> None:
    data = rng.normal(size=(120, 6))
    data[:, 2] = data[:, 0] * 0.55 + rng.normal(size=120) * 0.7
    corr = np.corrcoef(data, rowvar=False)
    ax.imshow(corr, cmap=diverging_cmap(), vmin=-1, vmax=1)
    ax.set_xticks(range(6), [f"V{i}" for i in range(1, 7)])
    ax.set_yticks(range(6), [f"V{i}" for i in range(1, 7)])
    ax.grid(False)


def draw_roc(ax: plt.Axes, rng: np.random.Generator) -> None:
    fpr = np.linspace(0, 1, 100)
    for power, color, label in [(2.2, BLUE, "Base"), (3.0, ORANGE, "Full")]:
        tpr = 1 - (1 - fpr) ** power
        ax.plot(fpr, tpr, color=color, label=label)
    ax.plot([0, 1], [0, 1], color=GRAY, ls="--", lw=0.8)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_pr(ax: plt.Axes, rng: np.random.Generator) -> None:
    recall = np.linspace(0, 1, 100)
    for base, color, label in [(0.83, BLUE, "Model A"), (0.73, ORANGE, "Model B")]:
        precision = np.clip(base - 0.42 * recall**1.7 + 0.03 * np.sin(recall * 8), 0.08, 1)
        ax.plot(recall, precision, color=color, label=label)
    ax.axhline(0.18, color=GRAY, ls="--", lw=0.8)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_calibration(ax: plt.Axes, rng: np.random.Generator) -> None:
    pred = np.linspace(0.05, 0.8, 9)
    obs = np.clip(pred + rng.normal(0, 0.035, len(pred)) - 0.015, 0, 1)
    ax.plot([0, 0.85], [0, 0.85], color=GRAY, ls="--", lw=0.8)
    ax.plot(pred, obs, marker="o", color=BLUE)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Observed")
    tidy(ax)


def draw_decision(ax: plt.Axes, rng: np.random.Generator) -> None:
    t = np.linspace(0.04, 0.7, 100)
    model = 0.11 * np.exp(-2.2 * (t - 0.25) ** 2) - 0.035 * t
    all_line = 0.055 - 0.085 * t
    ax.plot(t, model, color=BLUE, label="Model")
    ax.plot(t, all_line, color=ORANGE, label="Treat all")
    ax.axhline(0, color=GRAY, ls="--", lw=0.8, label="None")
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Net benefit")
    ax.legend(fontsize=5.8)
    tidy(ax)


def draw_risk_groups(ax: plt.Axes, rng: np.random.Generator) -> None:
    groups = ["Low", "Mod", "High", "V high"]
    pred = np.array([0.06, 0.14, 0.28, 0.45])
    obs = np.clip(pred + rng.normal(0, 0.025, len(pred)), 0, 1)
    ax.bar(np.arange(len(groups)), obs * 100, color=BLUE, alpha=0.8, label="Observed")
    ax.plot(np.arange(len(groups)), pred * 100, color=ORANGE, marker="o", label="Predicted")
    ax.set_xticks(range(len(groups)), groups, rotation=20, ha="right")
    ax.set_ylabel("Event rate (%)")
    ax.legend(fontsize=5.8)
    tidy(ax)


def draw_lift(ax: plt.Axes, rng: np.random.Generator) -> None:
    pct = np.linspace(0.05, 1, 20)
    lift = 1 + 2.4 * np.exp(-3.1 * pct)
    ax.plot(pct * 100, lift, color=BLUE)
    ax.axhline(1, color=GRAY, ls="--", lw=0.8)
    ax.set_xlabel("Population selected (%)")
    ax.set_ylabel("Lift")
    tidy(ax)


def draw_km(ax: plt.Axes, rng: np.random.Generator) -> None:
    time = np.arange(0, 25, 2)
    for hazard, color, label in [(0.035, ORANGE, "Control"), (0.025, BLUE, "Intervention")]:
        surv = np.clip(np.exp(-hazard * time) - np.linspace(0, 0.03, len(time)), 0.45, 1.0)
        ax.step(time, surv, where="post", color=color, label=label)
    ax.set_xlabel("Months")
    ax.set_ylabel("Event-free")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_cumulative_incidence_survival(ax: plt.Axes, rng: np.random.Generator) -> None:
    time = np.arange(0, 25, 2)
    for hazard, color, label in [(0.027, ORANGE, "Control"), (0.018, BLUE, "Intervention")]:
        inc = np.clip(1 - np.exp(-hazard * time), 0, 0.5)
        ax.step(time, inc * 100, where="post", color=color, label=label)
    ax.set_xlabel("Months")
    ax.set_ylabel("Incidence (%)")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_competing_risk(ax: plt.Axes, rng: np.random.Generator) -> None:
    time = np.arange(0, 20, 2)
    event = 1 - np.exp(-0.035 * time)
    competing = 0.4 * (1 - np.exp(-0.03 * time))
    ax.step(time, event * 100, where="post", color=BLUE, label="Target event")
    ax.step(time, competing * 100, where="post", color=RED, label="Competing")
    ax.set_xlabel("Months")
    ax.set_ylabel("Cumulative (%)")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_risk_table_style(ax: plt.Axes, rng: np.random.Generator) -> None:
    time = np.arange(0, 19, 3)
    surv = np.clip(np.exp(-0.035 * time), 0.5, 1.0)
    ax.step(time, surv, where="post", color=BLUE)
    for t, n in zip(time, np.linspace(220, 108, len(time)).astype(int)):
        ax.text(t, 0.43, str(n), ha="center", fontsize=5.8)
    ax.text(time[0] - 1.5, 0.43, "At risk", fontsize=5.8, ha="right")
    ax.set_ylim(0.38, 1.02)
    ax.set_xlabel("Months")
    ax.set_ylabel("Survival")
    tidy(ax)


def draw_hazard(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.linspace(0, 24, 90)
    h = 0.025 + 0.025 * np.exp(-((x - 7) / 5) ** 2) + 0.004 * np.sin(x / 2)
    ax.plot(x, h, color=RED)
    ax.fill_between(x, h - 0.006, h + 0.006, color=RED, alpha=0.18)
    ax.set_xlabel("Months")
    ax.set_ylabel("Hazard")
    tidy(ax)


def draw_forest(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["Overall", "Age<65", "Age>=65", "Female", "Male", "High risk"]
    est = np.array([0.78, 0.74, 0.86, 0.70, 0.83, 0.72])
    half = np.array([0.15, 0.22, 0.25, 0.20, 0.19, 0.21])
    y = np.arange(len(labels))[::-1]
    ax.axvline(1, color="#222222", ls="--", lw=0.8)
    ax.errorbar(est, y, xerr=[half, half], fmt="o", color=BLUE, capsize=2)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Risk ratio")
    ax.set_xlim(0.35, 1.35)
    tidy(ax)


def draw_meta_forest(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = [f"Study {i}" for i in range(1, 7)] + ["Pooled"]
    est = np.r_[rng.normal(-0.12, 0.12, 6), -0.10]
    se = np.r_[rng.uniform(0.08, 0.16, 6), 0.05]
    y = np.arange(len(labels))[::-1]
    ax.axvline(0, color="#222222", lw=0.8)
    ax.errorbar(est, y, xerr=1.96 * se, fmt="o", color=BLUE, capsize=2)
    ax.scatter(est[-1], y[-1], marker="D", color=RED, s=30)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Mean difference")
    tidy(ax)


def draw_coefficients(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["Age", "Sex", "Lab", "Comorb", "Score", "Site"]
    beta = rng.normal(0, 0.22, len(labels))
    se = rng.uniform(0.06, 0.11, len(labels))
    y = np.arange(len(labels))
    ax.axvline(0, color="#222222", lw=0.8)
    ax.errorbar(beta, y, xerr=1.96 * se, fmt="o", color=PURPLE, capsize=2)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Coefficient")
    tidy(ax)


def draw_funnel_plot(ax: plt.Axes, rng: np.random.Generator) -> None:
    se = rng.uniform(0.06, 0.32, 36)
    effect = rng.normal(0.03, se * 1.25)
    ax.scatter(effect, se, s=15, color=BLUE, alpha=0.75)
    grid = np.linspace(0.05, 0.35, 60)
    ax.plot(1.96 * grid, grid, color=GRAY, ls="--", lw=0.7)
    ax.plot(-1.96 * grid, grid, color=GRAY, ls="--", lw=0.7)
    ax.axvline(0, color="#222222", lw=0.8)
    ax.invert_yaxis()
    ax.set_xlabel("Effect")
    ax.set_ylabel("SE")
    tidy(ax)


def draw_balance(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = ["Age", "Sex", "Lab", "Prior", "Site", "Risk"]
    before = rng.uniform(0.12, 0.34, len(labels))
    after = before * rng.uniform(0.2, 0.5, len(labels))
    y = np.arange(len(labels))
    ax.scatter(before, y, color=ORANGE, label="Before")
    ax.scatter(after, y, color=BLUE, label="After")
    for b, a, yy in zip(before, after, y):
        ax.plot([b, a], [yy, yy], color=LIGHT_GRAY)
    ax.axvline(0.1, color="#222222", ls="--", lw=0.8)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("SMD")
    ax.legend(fontsize=5.8)
    tidy(ax)


def draw_evidence_summary(ax: plt.Axes, rng: np.random.Generator) -> None:
    outcomes = ["Death", "Readmit", "Function", "Harms", "QoL"]
    score = np.array([4, 3, 2, 3, 2])
    ax.barh(np.arange(len(outcomes)), score, color=["#8FB996" if s >= 3 else "#E9C46A" for s in score])
    ax.set_yticks(range(len(outcomes)), outcomes)
    ax.set_xlim(0, 4.4)
    ax.invert_yaxis()
    ax.set_xlabel("Certainty")
    tidy(ax)


def draw_flow_boxes(ax: plt.Axes, boxes: list[tuple[float, float, str, str]], arrows: list[tuple[tuple[float, float], tuple[float, float]]]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    for x, y, text, color in boxes:
        rect = patches.FancyBboxPatch((x - 1.35, y - 0.36), 2.7, 0.72, boxstyle="round,pad=0.04", fc=color, ec=GRAY, lw=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha="center", va="center", fontsize=6.2)
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "lw": 0.75, "color": GRAY})


def draw_consort_flow(ax: plt.Axes, rng: np.random.Generator) -> None:
    boxes = [
        (5, 8.8, "Assessed\nn=720", "#EFF6FF"),
        (5, 7.2, "Randomized\nn=600", "#F8FAFC"),
        (2.8, 5.5, "Control\nn=300", "#FFF7ED"),
        (7.2, 5.5, "Intervention\nn=300", "#F0FDF4"),
        (2.8, 3.7, "Analyzed\nn=286", "#F8FAFC"),
        (7.2, 3.7, "Analyzed\nn=292", "#F8FAFC"),
    ]
    arrows = [((5, 8.42), (5, 7.58)), ((5, 6.85), (2.8, 5.9)), ((5, 6.85), (7.2, 5.9)), ((2.8, 5.1), (2.8, 4.1)), ((7.2, 5.1), (7.2, 4.1))]
    draw_flow_boxes(ax, boxes, arrows)


def draw_prisma_flow(ax: plt.Axes, rng: np.random.Generator) -> None:
    boxes = [
        (5, 8.8, "Identified\nn=1284", "#EFF6FF"),
        (5, 7.2, "Screened\nn=912", "#F8FAFC"),
        (8.0, 7.2, "Excluded\nn=701", "#FFF7ED"),
        (5, 5.6, "Full text\nn=211", "#F8FAFC"),
        (5, 4.0, "Included\nn=47", "#F0FDF4"),
    ]
    arrows = [((5, 8.42), (5, 7.58)), ((5, 6.82), (5, 5.98)), ((5, 5.22), (5, 4.38)), ((6.35, 7.2), (6.65, 7.2))]
    draw_flow_boxes(ax, boxes, arrows)


def draw_cohort_flow(ax: plt.Axes, rng: np.random.Generator) -> None:
    boxes = [
        (5, 8.7, "EHR source\nn=42k", "#EFF6FF"),
        (5, 7.1, "Eligible\nn=9.4k", "#F8FAFC"),
        (5, 5.5, "Complete data\nn=7.8k", "#F8FAFC"),
        (2.9, 3.8, "Exposed\nn=2.2k", "#F0FDF4"),
        (7.1, 3.8, "Unexposed\nn=5.6k", "#FFF7ED"),
    ]
    arrows = [((5, 8.32), (5, 7.48)), ((5, 6.72), (5, 5.88)), ((5, 5.1), (2.9, 4.2)), ((5, 5.1), (7.1, 4.2))]
    draw_flow_boxes(ax, boxes, arrows)


def draw_patient_timeline(ax: plt.Axes, rng: np.random.Generator) -> None:
    days = [0, 2, 5, 9, 14, 28]
    labels = ["Admit", "Scan", "Test", "Rx", "Disch", "FU"]
    colors = [BLUE, ORANGE, TEAL, GREEN, PURPLE, RED]
    ax.hlines(0, 0, 28, color=LIGHT_GRAY, lw=2)
    for d, label, color in zip(days, labels, colors):
        ax.scatter(d, 0, s=42, color=color, zorder=3)
        ax.text(d, 0.12, label, ha="center", rotation=25, fontsize=6)
    ax.set_xlim(-1, 30)
    ax.set_ylim(-0.35, 0.65)
    ax.set_yticks([])
    ax.set_xlabel("Day")
    tidy(ax)


def draw_diagnostic_pathway(ax: plt.Axes, rng: np.random.Generator) -> None:
    boxes = [
        (1.8, 8.0, "Symptoms", "#EFF6FF"),
        (5.0, 8.0, "Index test", "#F8FAFC"),
        (8.2, 8.0, "Reference", "#F8FAFC"),
        (5.0, 5.7, "Risk group", "#F0FDF4"),
        (5.0, 3.4, "Treatment", "#FFF7ED"),
    ]
    arrows = [((3.15, 8), (3.65, 8)), ((6.35, 8), (6.85, 8)), ((8.2, 7.6), (5.4, 6.05)), ((5, 5.32), (5, 3.78))]
    draw_flow_boxes(ax, boxes, arrows)


def draw_model_workflow(ax: plt.Axes, rng: np.random.Generator) -> None:
    boxes = [
        (2, 8.2, "Data", "#EFF6FF"),
        (5, 8.2, "Features", "#F8FAFC"),
        (8, 8.2, "Model", "#F8FAFC"),
        (5, 5.8, "Validation", "#F0FDF4"),
        (5, 3.5, "Decision", "#FFF7ED"),
    ]
    arrows = [((3.35, 8.2), (3.65, 8.2)), ((6.35, 8.2), (6.65, 8.2)), ((8, 7.8), (5.4, 6.15)), ((5, 5.42), (5, 3.88))]
    draw_flow_boxes(ax, boxes, arrows)


def draw_volcano(ax: plt.Axes, rng: np.random.Generator) -> None:
    n = 260
    logfc = rng.normal(0, 1.1, n)
    p = np.clip(rng.beta(0.7, 8, n), 1e-5, 1)
    neglog = -np.log10(p)
    sig = (np.abs(logfc) > 1) & (p < 0.05)
    ax.scatter(logfc[~sig], neglog[~sig], s=8, color="#CBD5E1")
    ax.scatter(logfc[sig], neglog[sig], s=10, color=RED)
    ax.axvline(-1, color=GRAY, ls="--", lw=0.7)
    ax.axvline(1, color=GRAY, ls="--", lw=0.7)
    ax.axhline(-np.log10(0.05), color=GRAY, ls="--", lw=0.7)
    ax.set_xlabel("log fold change")
    ax.set_ylabel("-log10(p)")
    tidy(ax)


def draw_enrichment(ax: plt.Axes, rng: np.random.Generator) -> None:
    terms = ["Immune", "Cycle", "Hypoxia", "Lipid", "Repair", "Signal"]
    ratio = np.linspace(0.08, 0.32, len(terms)) + rng.normal(0, 0.012, len(terms))
    size = rng.integers(20, 70, len(terms))
    color = -np.log10(np.linspace(0.08, 0.002, len(terms)))
    sc = ax.scatter(ratio, np.arange(len(terms)), s=size * 2.4, c=color, cmap=sequential_cmap(), edgecolor="#334155", lw=0.3)
    ax.set_yticks(range(len(terms)), terms)
    ax.invert_yaxis()
    ax.set_xlabel("Ratio")
    ax.figure.colorbar(sc, ax=ax, fraction=0.04, pad=0.02)
    tidy(ax)


def draw_upset(ax: plt.Axes, rng: np.random.Generator) -> None:
    ax.set_axis_off()
    x = np.arange(7)
    sizes = np.array([42, 35, 25, 18, 14, 10, 8])
    ax_in = ax.inset_axes([0.12, 0.42, 0.82, 0.48])
    ax_dot = ax.inset_axes([0.12, 0.10, 0.82, 0.26], sharex=ax_in)
    ax_in.bar(x, sizes, color=BLUE)
    ax_in.set_ylabel("Size", fontsize=6)
    ax_in.tick_params(labelbottom=False, labelsize=5.8)
    membership = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])
    for yi in range(3):
        ax_dot.scatter(x[membership[:, yi] == 1], np.full((membership[:, yi] == 1).sum(), yi), color="#111827", s=12)
        ax_dot.scatter(x[membership[:, yi] == 0], np.full((membership[:, yi] == 0).sum(), yi), color="#D1D5DB", s=10)
    for idx, row in enumerate(membership):
        ys = np.where(row == 1)[0]
        if len(ys) > 1:
            ax_dot.plot([idx, idx], [ys.min(), ys.max()], color="#111827", lw=0.7)
    ax_dot.set_yticks(range(3), ["A", "B", "C"], fontsize=5.8)
    ax_dot.set_xticks(x, [])


def draw_ma_plot(ax: plt.Axes, rng: np.random.Generator) -> None:
    mean = rng.uniform(1, 12, 260)
    diff = rng.normal(0, 0.42, 260) + 0.05 * (mean - 6)
    sig = np.abs(diff) > 0.8
    ax.scatter(mean[~sig], diff[~sig], s=8, color="#CBD5E1")
    ax.scatter(mean[sig], diff[sig], s=10, color=RED)
    ax.axhline(0, color=GRAY, lw=0.7)
    ax.set_xlabel("Mean abundance")
    ax.set_ylabel("Log ratio")
    tidy(ax)


def draw_pca(ax: plt.Axes, rng: np.random.Generator) -> None:
    for idx, color in enumerate([BLUE, ORANGE, TEAL]):
        xy = rng.normal([idx * 1.0, idx * 0.55], [0.45, 0.35], (36, 2))
        ax.scatter(xy[:, 0], xy[:, 1], s=13, color=color, alpha=0.75, label=f"G{idx + 1}")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.legend(fontsize=5.8)
    tidy(ax)


def draw_feature_rank(ax: plt.Axes, rng: np.random.Generator) -> None:
    labels = [f"F{i}" for i in range(1, 8)]
    imp = np.sort(rng.uniform(0.03, 0.22, len(labels)))[::-1]
    ax.barh(np.arange(len(labels)), imp, color=BLUE)
    ax.set_yticks(range(len(labels)), labels)
    ax.invert_yaxis()
    ax.set_xlabel("Importance")
    tidy(ax)


def draw_clinical_triptych(ax: plt.Axes, rng: np.random.Generator) -> None:
    unit_canvas(ax)
    panel_w = 0.27
    starts = [0.03, 0.37, 0.70]
    titles = ["Trend", "Effect", "Summary"]
    for start, title in zip(starts, titles):
        ax.add_patch(patches.Rectangle((start, 0.08), panel_w, 0.78, ec=LIGHT_GRAY, fc="#FFFFFF", lw=0.7))
        ax.text(start + 0.02, 0.82, title, fontsize=6.3, fontweight="bold")
    x = np.linspace(starts[0] + 0.04, starts[0] + panel_w - 0.03, 8)
    y1 = 0.65 - 0.22 * np.linspace(0, 1, 8) + rng.normal(0, 0.015, 8)
    y2 = y1 + 0.08
    ax.plot(x, y1, color=BLUE, lw=1.1)
    ax.plot(x, y2, color=ORANGE, lw=1.1)
    ax.axvline(starts[1] + 0.12, ymin=0.2, ymax=0.75, color="#222222", lw=0.7)
    for yy, est in zip([0.68, 0.52, 0.36], [-0.06, -0.12, 0.04]):
        ax.plot([starts[1] + 0.08, starts[1] + 0.19], [yy, yy], color=BLUE, lw=1)
        ax.scatter(starts[1] + 0.13 + est, yy, color=BLUE, s=13)
    bar_base = 0.22
    for xpos, height, color in [(starts[2] + 0.08, 0.30, BLUE), (starts[2] + 0.18, 0.22, ORANGE)]:
        ax.add_patch(patches.Rectangle((xpos - 0.03, bar_base), 0.06, height, fc=color, ec="none"))
    ax.text(starts[2] + 0.035, 0.14, "n=220 / 218", fontsize=5.7)


def draw_image_plate_quant(ax: plt.Axes, rng: np.random.Generator) -> None:
    unit_canvas(ax)
    for x0, label in [(0.03, "Case"), (0.30, "Control")]:
        img = rng.normal(0.45, 0.18, (18, 18))
        draw_image_box(ax, img, x0, x0 + 0.22, COMPOSITE_BOTTOM, COMPOSITE_TOP)
        ax.plot(
            [x0 + 0.04, x0 + 0.13],
            [COMPOSITE_BOTTOM + 0.03, COMPOSITE_BOTTOM + 0.03],
            color="white",
            lw=1.5,
        )
        ax.text(x0, COMPOSITE_LABEL_Y, label, fontsize=6.2)
    draw_compact_quant_bars(ax, 0.61, 0.91, values=(0.82, 0.58))


def draw_segmentation_overlay(ax: plt.Axes, rng: np.random.Generator) -> None:
    unit_canvas(ax)
    img = rng.normal(0.45, 0.16, (28, 28))
    iax = ax.inset_axes([0.23, 0.14, 0.54, 0.70])
    iax.set_box_aspect(1)
    iax.imshow(img, cmap="gray", vmin=0, vmax=1, aspect="equal")
    iax.set_axis_off()
    for _ in range(8):
        cx, cy = rng.uniform(5, 23, 2)
        radius = rng.uniform(1.7, 3.0)
        iax.add_patch(patches.Circle((cx, cy), radius, fill=False, ec=TEAL, lw=1.0))
    iax.plot([3, 10], [24, 24], color="white", lw=2)


def draw_image_before_after(ax: plt.Axes, rng: np.random.Generator) -> None:
    unit_canvas(ax)
    for x0, title in [(0.04, "Before"), (0.33, "After")]:
        img = rng.normal(0.45 + 0.1 * (title == "After"), 0.15, (18, 18))
        draw_image_box(ax, img, x0, x0 + 0.23, COMPOSITE_BOTTOM, COMPOSITE_TOP, cmap=sequential_cmap())
        ax.text(x0, COMPOSITE_LABEL_Y, title, fontsize=6.2)
    before = rng.normal(0.58, 0.08, 16)
    after = before + rng.normal(-0.10, 0.06, 16)
    low, high = 0.34, 0.72
    before_y = COMPOSITE_BOTTOM + (np.clip(before, low, high) - low) / (high - low) * (COMPOSITE_TOP - COMPOSITE_BOTTOM)
    after_y = COMPOSITE_BOTTOM + (np.clip(after, low, high) - low) / (high - low) * (COMPOSITE_TOP - COMPOSITE_BOTTOM)
    ax.plot([0.66, 0.66], [COMPOSITE_BOTTOM, COMPOSITE_TOP], color=LIGHT_GRAY, lw=0.7)
    ax.plot([0.90, 0.90], [COMPOSITE_BOTTOM, COMPOSITE_TOP], color=LIGHT_GRAY, lw=0.7)
    for b, a in zip(before, after):
        yb = COMPOSITE_BOTTOM + (np.clip(b, low, high) - low) / (high - low) * (COMPOSITE_TOP - COMPOSITE_BOTTOM)
        ya = COMPOSITE_BOTTOM + (np.clip(a, low, high) - low) / (high - low) * (COMPOSITE_TOP - COMPOSITE_BOTTOM)
        ax.plot([0.66, 0.90], [yb, ya], color=LIGHT_GRAY, lw=0.7)
    ax.scatter(np.repeat(0.66, len(before_y)), before_y, s=8, color=BLUE)
    ax.scatter(np.repeat(0.90, len(after_y)), after_y, s=8, color=ORANGE)
    ax.text(0.66, COMPOSITE_NOTE_Y, "Before", fontsize=5.7, ha="center")
    ax.text(0.90, COMPOSITE_NOTE_Y, "After", fontsize=5.7, ha="center")


def draw_multi_endpoint(ax: plt.Axes, rng: np.random.Generator) -> None:
    x = np.arange(3)
    ax.bar(x - 0.18, [20, 32, 15], width=0.32, color=BLUE, label="Control")
    ax.bar(x + 0.18, [15, 25, 11], width=0.32, color=ORANGE, label="Treat")
    ax.set_xticks(x, ["Death", "Readm", "AE"], rotation=20, ha="right")
    ax.set_ylabel("%")
    ax.legend(fontsize=5.8)
    tidy(ax)


def draw_cohort_table(ax: plt.Axes, rng: np.random.Generator) -> None:
    ax.set_axis_off()
    rows = [["Age", "64.1", "63.7"], ["Female", "51%", "50%"], ["Diabetes", "22%", "25%"], ["Follow-up", "12 mo", "12 mo"]]
    table = ax.table(cellText=rows, colLabels=["Variable", "Group A", "Group B"], loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(6.2)
    table.scale(1, 1.25)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        if row == 0:
            cell.set_facecolor("#F8FAFC")
            cell.set_text_props(weight="bold")


def draw_image_quant_combo(ax: plt.Axes, rng: np.random.Generator) -> None:
    draw_image_plate_quant(ax, rng)


def draw_choropleth_tile(ax: plt.Axes, rng: np.random.Generator) -> None:
    vals = rng.uniform(20, 80, (3, 4))
    ax.imshow(vals, cmap=sequential_cmap(), aspect="equal")
    for i in range(3):
        for j in range(4):
            ax.text(j, i, f"R{i+1}{j+1}", ha="center", va="center", fontsize=5.8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)


def draw_uncertainty_ribbon(ax: plt.Axes, rng: np.random.Generator) -> None:
    year = np.arange(2015, 2027)
    estimate = 54 + 2.1 * (year - year.min()) + 4 * np.sin(np.linspace(0, 2.5, len(year)))
    interval = np.linspace(5, 8, len(year))
    ax.fill_between(year, estimate - interval, estimate + interval, color=BLUE, alpha=0.22)
    ax.plot(year, estimate, color=BLUE)
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate")
    tidy(ax)


def draw_icer(ax: plt.Axes, rng: np.random.Generator) -> None:
    effect = rng.normal(0.18, 0.08, 180)
    cost = rng.normal(7300, 4200, 180)
    ax.scatter(effect, cost, s=10, color=BLUE, alpha=0.55)
    xs = np.linspace(-0.05, 0.42, 80)
    ax.plot(xs, 50000 * xs, color=ORANGE, lw=1.1)
    ax.axhline(0, color=GRAY, lw=0.7)
    ax.axvline(0, color=GRAY, lw=0.7)
    ax.set_xlabel("Effect")
    ax.set_ylabel("Cost")
    tidy(ax)


def draw_ceac(ax: plt.Axes, rng: np.random.Generator) -> None:
    thresholds = np.arange(0, 105000, 5000)
    a = 1 / (1 + np.exp(-(thresholds - 42000) / 13500))
    b = 1 / (1 + np.exp(-(thresholds - 62000) / 16000))
    ax.plot(thresholds / 1000, a, color=BLUE, label="A")
    ax.plot(thresholds / 1000, b, color=ORANGE, label="B")
    ax.set_xlabel("Threshold (k)")
    ax.set_ylabel("Probability")
    ax.legend(fontsize=6)
    tidy(ax)


def draw_budget(ax: plt.Axes, rng: np.random.Generator) -> None:
    years = np.arange(2026, 2032)
    drug = np.linspace(2.2, 4.8, len(years))
    monitoring = np.linspace(0.8, 1.4, len(years))
    hospital = np.linspace(3.2, 2.5, len(years))
    ax.stackplot(years, drug, monitoring, hospital, labels=["Drug", "Monitor", "Hosp"], colors=[BLUE, ORANGE, GREEN], alpha=0.82)
    ax.set_xlabel("Year")
    ax.set_ylabel("Million")
    ax.legend(fontsize=5.6, loc="upper left")
    tidy(ax)


def categories() -> tuple[ChartCategory, ...]:
    return (
        ChartCategory(
            "01_bar_charts",
            "Chart Type Overview 01 | Bar charts",
            "Bar charts",
            (
                ChartItem("simple_bar", "Single-series bar", draw_simple_bar),
                ChartItem("grouped_bar", "Grouped bar", draw_grouped_bar),
                ChartItem("grouped_bar_dense", "Grouped bar with more groups", draw_grouped_bar_dense),
                ChartItem("stacked_bar", "Stacked bar", draw_stacked_bar),
                ChartItem("horizontal_bar", "Horizontal bar", draw_horizontal_bar),
                ChartItem("diverging_bar", "Diverging bar", draw_diverging_bar),
                ChartItem("error_bar", "Bar with uncertainty", draw_error_bar),
                ChartItem("lollipop", "Lollipop", draw_lollipop),
                ChartItem("percent_stacked", "Percent stacked", draw_percent_stacked),
                ChartItem("waterfall", "Waterfall", draw_waterfall),
                ChartItem("tornado_bar", "Tornado-style bar", draw_tornado_bar),
            ),
        ),
        ChartCategory(
            "02_line_longitudinal",
            "Chart Type Overview 02 | Line and longitudinal trends",
            "Line and longitudinal trends",
            (
                ChartItem("single_line", "Single trend", draw_single_line),
                ChartItem("multi_line", "Multi-group trend", draw_multi_line),
                ChartItem("ribbon_line", "Uncertainty ribbon", draw_ribbon_line),
                ChartItem("spaghetti", "Individual traces + mean", draw_spaghetti),
                ChartItem("step_line", "Step/event curve", draw_step_line),
                ChartItem("cumulative_line", "Cumulative trend", draw_cumulative_line),
                ChartItem("slope_chart", "Before-after slope", draw_slope_chart),
                ChartItem("event_annotation", "Annotated event trend", draw_event_annotation_line),
            ),
        ),
        ChartCategory(
            "03_distribution_paired",
            "Chart Type Overview 03 | Distribution and paired data",
            "Distribution and paired data",
            (
                ChartItem("histogram", "Histogram", draw_histogram),
                ChartItem("density", "Density curves", draw_density),
                ChartItem("boxplot", "Box plot", draw_boxplot),
                ChartItem("violin", "Violin plot", draw_violin),
                ChartItem("strip", "Strip plot", draw_strip),
                ChartItem("paired_change", "Paired change", draw_paired_distribution),
                ChartItem("ecdf", "Cumulative distribution", draw_ecdf),
                ChartItem("ridgeline", "Ridgeline", draw_ridgeline),
            ),
        ),
        ChartCategory(
            "04_heatmaps_matrices",
            "Chart Type Overview 04 | Heatmaps and matrices",
            "Heatmaps and matrices",
            (
                ChartItem("heatmap", "Continuous heatmap", draw_heatmap),
                ChartItem("annotated_heatmap", "Annotated heatmap", draw_annotated_heatmap),
                ChartItem("missingness", "Missingness map", draw_missingness),
                ChartItem("confusion", "Confusion matrix", draw_confusion),
                ChartItem("risk_bias", "Risk-of-bias matrix", draw_risk_bias),
                ChartItem("correlation", "Correlation matrix", draw_correlation),
            ),
        ),
        ChartCategory(
            "05_diagnostic_prediction",
            "Chart Type Overview 05 | Diagnostic and prediction curves",
            "Diagnostic and prediction curves",
            (
                ChartItem("roc", "ROC curve", draw_roc),
                ChartItem("pr", "Precision-recall curve", draw_pr),
                ChartItem("calibration", "Calibration plot", draw_calibration),
                ChartItem("decision", "Decision curve", draw_decision),
                ChartItem("risk_groups", "Risk-group plot", draw_risk_groups),
                ChartItem("lift", "Lift curve", draw_lift),
            ),
        ),
        ChartCategory(
            "06_survival_time_to_event",
            "Chart Type Overview 06 | Survival and time-to-event",
            "Survival and time-to-event",
            (
                ChartItem("kaplan_meier", "Kaplan-Meier curve", draw_km),
                ChartItem("cumulative_incidence", "Cumulative incidence", draw_cumulative_incidence_survival),
                ChartItem("competing_risk", "Competing-risk curves", draw_competing_risk),
                ChartItem("risk_table_style", "Curve with risk counts", draw_risk_table_style),
                ChartItem("hazard", "Smoothed hazard", draw_hazard),
            ),
        ),
        ChartCategory(
            "07_effect_review",
            "Chart Type Overview 07 | Effect estimates and review evidence",
            "Effect estimates and review evidence",
            (
                ChartItem("forest", "Subgroup forest", draw_forest),
                ChartItem("meta_forest", "Meta-analysis forest", draw_meta_forest),
                ChartItem("coefficients", "Coefficient intervals", draw_coefficients),
                ChartItem("funnel", "Funnel plot", draw_funnel_plot),
                ChartItem("balance", "Covariate balance", draw_balance),
                ChartItem("evidence_summary", "Evidence summary", draw_evidence_summary),
            ),
        ),
        ChartCategory(
            "08_flow_timeline",
            "Chart Type Overview 08 | Study flow and timelines",
            "Study flow and timelines",
            (
                ChartItem("consort_flow", "CONSORT-style flow", draw_consort_flow),
                ChartItem("prisma_flow", "PRISMA-style flow", draw_prisma_flow),
                ChartItem("cohort_flow", "Cohort selection flow", draw_cohort_flow),
                ChartItem("patient_timeline", "Patient timeline", draw_patient_timeline),
                ChartItem("diagnostic_pathway", "Diagnostic pathway", draw_diagnostic_pathway),
                ChartItem("model_workflow", "Model workflow", draw_model_workflow),
            ),
        ),
        ChartCategory(
            "09_biomarker_omics",
            "Chart Type Overview 09 | Biomarker and omics displays",
            "Biomarker and omics displays",
            (
                ChartItem("volcano", "Volcano plot", draw_volcano),
                ChartItem("enrichment", "Enrichment bubble", draw_enrichment),
                ChartItem("upset", "UpSet plot", draw_upset),
                ChartItem("ma_plot", "MA plot", draw_ma_plot),
                ChartItem("pca", "PCA scatter", draw_pca),
                ChartItem("feature_rank", "Feature rank", draw_feature_rank),
            ),
        ),
        ChartCategory(
            "10_clinical_imaging_composites",
            "Chart Type Overview 10 | Clinical, imaging, and table composites",
            "Clinical, imaging, and table composites",
            (
                ChartItem("clinical_triptych", "Clinical triptych", draw_clinical_triptych),
                ChartItem("image_plate_quant", "Image plate + quant", draw_image_plate_quant),
                ChartItem("segmentation_overlay", "Segmentation overlay", draw_segmentation_overlay),
                ChartItem("before_after_image", "Before-after image + dots", draw_image_before_after),
                ChartItem("multi_endpoint", "Multi-endpoint panel", draw_multi_endpoint),
                ChartItem("cohort_table", "Cohort table preview", draw_cohort_table),
                ChartItem("image_quant_combo", "Image + numeric companion", draw_image_quant_combo),
            ),
        ),
        ChartCategory(
            "11_global_health_economics",
            "Chart Type Overview 11 | Global-health and economic displays",
            "Global-health and economic displays",
            (
                ChartItem("choropleth_tile", "Choropleth-style tile map", draw_choropleth_tile),
                ChartItem("uncertainty_ribbon", "Uncertainty ribbon", draw_uncertainty_ribbon),
                ChartItem("icer", "ICER plane", draw_icer),
                ChartItem("ceac", "Acceptability curve", draw_ceac),
                ChartItem("tornado", "Tornado plot", draw_tornado_bar),
                ChartItem("budget", "Budget impact", draw_budget),
            ),
        ),
    )


def chunked(items: tuple[ChartItem, ...], size: int) -> list[tuple[ChartItem, ...]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def render_category(
    category: ChartCategory,
    pdf_dir: Path,
    preview_dir: Path,
    manifest_rows: list[dict[str, str]],
    seed: int,
    palette_override: str = "auto",
) -> None:
    display_family = CATEGORY_DISPLAY_FAMILY.get(category.slug, "bar")
    family_name = palette_for_category(category, palette_override)
    set_active_palette(display_family, family_name)
    pdf_path = pdf_dir / f"{category.slug}.pdf"
    per_page = 9
    page_chunks = chunked(category.items, per_page)
    rng = np.random.default_rng(seed)
    with PdfPages(pdf_path) as pdf:
        for page_index, page_items in enumerate(page_chunks, start=1):
            page_png = preview_dir / f"{category.slug}_page{page_index:02d}.png"
            fig, axes = plt.subplots(3, 3, figsize=(11.0, 8.35))
            axes_flat = list(axes.flat)
            fig.patch.set_facecolor("white")
            fig.suptitle(
                f"{category.title} | synthetic layout preview"
                if len(page_chunks) == 1
                else f"{category.title} | synthetic layout preview | page {page_index}/{len(page_chunks)}",
                fontsize=12.5,
                fontweight="bold",
                x=0.055,
                ha="left",
            )
            fig.text(
                0.055,
                0.918,
                f"Each panel uses random synthetic data for visual taxonomy and layout QA only. Palette family: {family_name}.",
                fontsize=7.2,
                color=GRAY,
                ha="left",
            )
            fig.subplots_adjust(left=0.065, right=0.985, top=0.865, bottom=0.07, wspace=0.42, hspace=0.62)
            for local_index, (ax, item) in enumerate(zip(axes_flat, page_items)):
                letter = chr(ord("a") + (page_index - 1) * per_page + local_index)
                item.draw(ax, rng)
                letter_title(ax, letter, item.label)
                manifest_rows.append(
                    {
                        "category_slug": category.slug,
                        "category": category.plain_name,
                        "subtype_slug": item.slug,
                        "subtype": item.label,
                        "pdf": str(pdf_path),
                        "preview_png": str(page_png),
                        "page": str(page_index),
                        "palette_family": family_name,
                    }
                )
            for ax in axes_flat[len(page_items) :]:
                ax.set_visible(False)
            pdf.savefig(fig, bbox_inches="tight")
            fig.savefig(page_png, dpi=220, bbox_inches="tight")
            plt.close(fig)


def render_index_pdf(categories_: tuple[ChartCategory, ...], output_dir: Path) -> None:
    index_pdf = output_dir / "00_chart_type_overview_index.pdf"
    with PdfPages(index_pdf) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.set_axis_off()
        fig.patch.set_facecolor("white")
        ax.text(0.05, 0.965, "Medical chart type overview index", fontsize=15, fontweight="bold", transform=ax.transAxes)
        ax.text(
            0.05,
            0.935,
            "Grouped PDFs generated from the academic-medicine-writing figure skill with synthetic data.",
            fontsize=8,
            color=GRAY,
            transform=ax.transAxes,
        )
        y = 0.885
        for idx, category in enumerate(categories_, start=1):
            ax.text(0.06, y, f"{idx:02d}", fontsize=8, fontweight="bold", transform=ax.transAxes)
            ax.text(0.13, y, category.plain_name, fontsize=8.4, fontweight="bold", transform=ax.transAxes)
            ax.text(0.13, y - 0.022, f"{len(category.items)} subtypes | pdfs/{category.slug}.pdf", fontsize=7.2, color=GRAY, transform=ax.transAxes)
            y -= 0.066
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)


def write_manifest(output_dir: Path, rows: list[dict[str, str]]) -> None:
    manifest_path = output_dir / "chart_type_overview_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "category_slug",
                "category",
                "subtype_slug",
                "subtype",
                "pdf",
                "preview_png",
                "page",
                "palette_family",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_qa(output_dir: Path, categories_: tuple[ChartCategory, ...], rows: list[dict[str, str]]) -> None:
    lines = [
        "# Medical Chart Type Overview QA",
        "",
        "- Backend: Python only (`matplotlib`, `numpy`).",
        "- Data: synthetic random data for display taxonomy and layout inspection only.",
        f"- Major categories: {len(categories_)}.",
        f"- Subtype panels: {len(rows)}.",
        "- Palette: named medical palette families are selected by chart category; heatmaps and risk maps use semantic scales.",
        "- Output: one grouped PDF per major chart type plus one PNG preview per PDF page.",
        "",
        "| # | Category | Subtypes | Palette family | PDF |",
        "|---:|---|---:|---|---|",
    ]
    for idx, category in enumerate(categories_, start=1):
        family = rows_by_category_palette(rows, category.slug)
        lines.append(f"| {idx} | {category.plain_name} | {len(category.items)} | `{family}` | `pdfs/{category.slug}.pdf` |")
    (output_dir / "visual_qa_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rows_by_category_palette(rows: list[dict[str, str]], category_slug: str) -> str:
    for row in rows:
        if row["category_slug"] == category_slug:
            return row.get("palette_family", DEFAULT_FAMILY)
    return DEFAULT_FAMILY


def clean_output(output_dir: Path) -> tuple[Path, Path]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    pdf_dir = output_dir / "pdfs"
    preview_dir = output_dir / "png_previews"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)
    return pdf_dir, preview_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / "medical_chart_type_overview",
        help="Output directory for grouped chart-type overview PDFs.",
    )
    parser.add_argument("--seed", type=int, default=20260622, help="Random seed for synthetic data.")
    parser.add_argument(
        "--palette-family",
        choices=("auto", *sorted(PALETTE_FAMILIES)),
        default="auto",
        help="Use auto chart-category palette selection or force one named palette family.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_matplotlib()
    output_dir = args.output.resolve()
    pdf_dir, preview_dir = clean_output(output_dir)
    cats = categories()
    manifest_rows: list[dict[str, str]] = []
    for idx, category in enumerate(cats):
        render_category(category, pdf_dir, preview_dir, manifest_rows, args.seed + idx * 1000, args.palette_family)
    render_index_pdf(cats, output_dir)
    write_manifest(output_dir, manifest_rows)
    write_qa(output_dir, cats, manifest_rows)
    print(f"Output root: {output_dir}")
    print(f"Grouped PDFs: {len(cats) + 1}")
    print(f"Subtype panels: {len(manifest_rows)}")
    print(f"Manifest: {output_dir / 'chart_type_overview_manifest.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
