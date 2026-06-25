#!/usr/bin/env python3
"""Generate a synthetic medical display gallery from the package-local skill resources."""

from __future__ import annotations

import argparse
import math
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from medical_palette import BLUE, GRAY, GREEN, LIGHT_GRAY, ORANGE, RED


PACKAGE_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_DIR = PACKAGE_ROOT / "assets/templates/springer-nature-latex/sn-article-template"
ROOT = Path.cwd() / "academic_medicine_all_display_types_demo"
PAPER = ROOT / "paper"
FIGURES = PAPER / "figures"


LIGHT_BLUE = "#EAF2F7"
LIGHT_ORANGE = "#F5EADF"


def configure(output: Path) -> None:
    global ROOT, PAPER, FIGURES
    ROOT = output.resolve()
    PAPER = ROOT / "paper"
    FIGURES = PAPER / "figures"


def ensure_dirs() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    FIGURES.mkdir(parents=True, exist_ok=True)
    copy_template_support()


def copy_template_support() -> None:
    """Copy only class/style support files, never sample manuscript prose."""
    shutil.copy2(TEMPLATE_DIR / "sn-jnl.cls", PAPER / "sn-jnl.cls")
    for bst in (TEMPLATE_DIR / "bst").glob("*.bst"):
        shutil.copy2(bst, PAPER / bst.name)


def savefig(name: str) -> None:
    path = FIGURES / name
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def arrow(ax, start, end, color=GRAY):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", color=color, lw=1.4),
    )


def box(ax, xy, text, width=2.6, height=0.72, face=LIGHT_GRAY, edge=GRAY, fontsize=8):
    x, y = xy
    patch = plt.Rectangle((x - width / 2, y - height / 2), width, height, fc=face, ec=edge, lw=1.0)
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, wrap=True)


def fig_consort_flow() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 8.4))
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    box(ax, (5, 11), "Assessed for eligibility\nn = 720", width=3.6, face=LIGHT_BLUE)
    box(ax, (5, 9.7), "Randomized\nn = 600", width=2.8, face="#e0f2fe")
    box(ax, (2.5, 8.2), "Allocated to intervention\nn = 300", width=3.2, face="#ecfdf5")
    box(ax, (7.5, 8.2), "Allocated to comparator\nn = 300", width=3.2, face=LIGHT_ORANGE)
    box(ax, (2.5, 6.8), "Received allocated intervention\nn = 292", width=3.4)
    box(ax, (7.5, 6.8), "Received comparator\nn = 296", width=3.4)
    box(ax, (2.5, 5.35), "Lost to follow-up\nn = 18", width=3.2, face="#fee2e2")
    box(ax, (7.5, 5.35), "Lost to follow-up\nn = 22", width=3.2, face="#fee2e2")
    box(ax, (2.5, 3.9), "Analyzed ITT\nn = 300", width=3.2, face="#dcfce7")
    box(ax, (7.5, 3.9), "Analyzed ITT\nn = 300", width=3.2, face="#dcfce7")
    box(ax, (5, 2.2), "Primary endpoint assessed at 30 days\nSynthetic demonstration only", width=4.2, face="#fef9c3")
    for a, b in [((5, 10.65), (5, 10.05)), ((5, 9.35), (2.5, 8.6)), ((5, 9.35), (7.5, 8.6)),
                 ((2.5, 7.85), (2.5, 7.15)), ((7.5, 7.85), (7.5, 7.15)),
                 ((2.5, 6.45), (2.5, 5.7)), ((7.5, 6.45), (7.5, 5.7)),
                 ((2.5, 5.0), (2.5, 4.25)), ((7.5, 5.0), (7.5, 4.25)),
                 ((2.5, 3.55), (5, 2.55)), ((7.5, 3.55), (5, 2.55))]:
        arrow(ax, a, b)
    ax.text(0.1, 11.7, "CONSORT-style participant flow", fontsize=12, fontweight="bold", ha="left")
    savefig("fig01_consort_flow.pdf")


def fig_primary_secondary_outcomes() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
    groups = ["Intervention", "Comparator"]
    values = [18.4, 24.7]
    err = [2.4, 2.8]
    axes[0].bar(groups, values, yerr=err, color=[BLUE, ORANGE], capsize=5)
    axes[0].set_ylabel("30-day event rate (%)")
    axes[0].set_title("Primary outcome")
    axes[0].grid(axis="y", alpha=0.25)

    months = np.array([0, 1, 3, 6, 12])
    intervention = np.array([42, 36, 31, 27, 25])
    comparator = np.array([43, 39, 36, 33, 32])
    axes[1].plot(months, intervention, marker="o", color=BLUE, label="Intervention")
    axes[1].plot(months, comparator, marker="o", color=ORANGE, label="Comparator")
    axes[1].fill_between(months, intervention - 2, intervention + 2, color=BLUE, alpha=0.15)
    axes[1].fill_between(months, comparator - 2.5, comparator + 2.5, color=ORANGE, alpha=0.15)
    axes[1].set_xlabel("Follow-up month")
    axes[1].set_ylabel("Symptom score")
    axes[1].set_title("Secondary repeated measure")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.25)
    fig.suptitle("Outcome display styles with uncertainty", fontsize=13, fontweight="bold")
    savefig("fig02_primary_secondary_outcomes.pdf")


def fig_harms_bar() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    events = ["Any adverse event", "Serious adverse event", "Treatment discontinuation", "Hospitalization"]
    intervention = np.array([31, 8, 5, 12])
    comparator = np.array([29, 7, 4, 14])
    y = np.arange(len(events))
    ax.barh(y + 0.18, intervention, height=0.34, color=BLUE, label="Intervention")
    ax.barh(y - 0.18, comparator, height=0.34, color=ORANGE, label="Comparator")
    ax.set_yticks(y)
    ax.set_yticklabels(events)
    ax.set_xlabel("Participants with event (%)")
    ax.set_title("Adverse-event table companion plot")
    ax.legend(frameon=False)
    ax.grid(axis="x", alpha=0.25)
    savefig("fig03_harms_bar.pdf")


def fig_forest_plot() -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    labels = ["Overall", "Age <65", "Age >=65", "Female", "Male", "High baseline risk", "Low baseline risk"]
    rr = np.array([0.76, 0.80, 0.72, 0.78, 0.75, 0.68, 0.88])
    low = np.array([0.61, 0.58, 0.53, 0.56, 0.55, 0.49, 0.64])
    high = np.array([0.94, 1.09, 0.98, 1.07, 1.03, 0.94, 1.21])
    y = np.arange(len(labels))[::-1]
    ax.errorbar(rr, y, xerr=[rr - low, high - rr], fmt="o", color=BLUE, ecolor=BLUE, capsize=2.5, ms=4)
    ax.axvline(1.0, color=GRAY, lw=1, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    ax.set_xlabel("Risk ratio (95% CI), synthetic", fontsize=9)
    ax.set_title("Subgroup / sensitivity forest plot", fontsize=10)
    ax.set_xlim(0.35, 1.35)
    ax.grid(axis="x", alpha=0.25)
    savefig("fig04_forest_plot.pdf")


def fig_km_curve() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    t = np.arange(0, 181, 15)
    s1 = np.exp(-0.0028 * t) - np.linspace(0, 0.03, len(t))
    s2 = np.exp(-0.0040 * t) - np.linspace(0, 0.04, len(t))
    s1 = np.clip(s1, 0, 1)
    s2 = np.clip(s2, 0, 1)
    ax.step(t, s1, where="post", color=BLUE, label="Intervention")
    ax.step(t, s2, where="post", color=ORANGE, label="Comparator")
    ax.set_xlabel("Days since randomization")
    ax.set_ylabel("Event-free probability")
    ax.set_title("Kaplan-Meier-style time-to-event display")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    savefig("fig05_km_curve.pdf")


def fig_prisma_flow() -> None:
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(4.0, 10.95)
    box(ax, (5, 10), "Records identified\nn = 1,284", width=3.2, face=LIGHT_BLUE)
    box(ax, (5, 8.7), "Records screened\nn = 912", width=3.2)
    box(ax, (8.2, 8.7), "Excluded\nn = 701", width=2.6, face="#fee2e2")
    box(ax, (5, 7.3), "Full-text reports assessed\nn = 211", width=3.4)
    box(ax, (8.2, 7.3), "Excluded with reasons\nn = 164", width=2.8, face="#fee2e2")
    box(ax, (5, 5.9), "Studies included\nn = 47", width=3.0, face="#dcfce7")
    box(ax, (5, 4.5), "Meta-analysis subset\nn = 32", width=3.0, face="#fef9c3")
    for a, b in [((5, 9.65), (5, 9.05)), ((5, 8.35), (5, 7.65)), ((5, 6.95), (5, 6.25)), ((5, 5.55), (5, 4.85))]:
        arrow(ax, a, b)
    arrow(ax, (6.6, 8.7), (6.9, 8.7))
    arrow(ax, (6.7, 7.3), (6.85, 7.3))
    ax.text(0.2, 10.7, "PRISMA-style flow display", fontsize=12, fontweight="bold")
    savefig("fig06_prisma_flow.pdf")


def fig_funnel_plot() -> None:
    rng = np.random.default_rng(7)
    se = np.linspace(0.08, 0.35, 36)
    effect = rng.normal(0.0, se * 1.2)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.scatter(effect, se, color=BLUE, alpha=0.75)
    se_line = np.linspace(0.06, 0.38, 100)
    ax.plot(1.96 * se_line, se_line, color=GRAY, ls="--")
    ax.plot(-1.96 * se_line, se_line, color=GRAY, ls="--")
    ax.axvline(0, color=GRAY, lw=1)
    ax.invert_yaxis()
    ax.set_xlabel("Log effect estimate")
    ax.set_ylabel("Standard error")
    ax.set_title("Funnel plot style for evidence synthesis")
    ax.grid(alpha=0.2)
    savefig("fig07_funnel_plot.pdf")


def fig_roc_curve() -> None:
    fpr = np.linspace(0, 1, 101)
    tpr = 1 - (1 - fpr) ** 2.6
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, color=BLUE, lw=2, label="AUC = 0.82 (synthetic)")
    ax.plot([0, 1], [0, 1], color=GRAY, ls="--", label="Chance")
    ax.set_xlabel("1 - specificity")
    ax.set_ylabel("Sensitivity")
    ax.set_title("ROC curve")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    savefig("fig08_roc_curve.pdf")


def fig_calibration_decision() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    pred = np.linspace(0.05, 0.75, 9)
    obs = pred * 0.92 + 0.04 * np.sin(np.linspace(0, 2 * math.pi, 9))
    axes[0].plot([0, 0.8], [0, 0.8], color=GRAY, ls="--", label="Ideal")
    axes[0].plot(pred, obs, marker="o", color=BLUE, label="Model")
    axes[0].set_xlabel("Predicted risk")
    axes[0].set_ylabel("Observed risk")
    axes[0].set_title("Calibration plot")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.25)

    threshold = np.linspace(0.02, 0.6, 60)
    model = 0.12 * np.exp(-2 * threshold) - 0.015
    treat_all = 0.08 - 0.16 * threshold
    axes[1].plot(threshold, model, color=BLUE, label="Model")
    axes[1].plot(threshold, np.maximum(treat_all, -0.03), color=ORANGE, label="Treat all")
    axes[1].axhline(0, color=GRAY, ls="--", label="Treat none")
    axes[1].set_xlabel("Risk threshold")
    axes[1].set_ylabel("Net benefit")
    axes[1].set_title("Decision curve")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.25)
    savefig("fig09_calibration_decision.pdf")


def fig_heatmap() -> None:
    rng = np.random.default_rng(4)
    data = rng.normal(0, 1, (8, 10))
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    im = ax.imshow(data, cmap="RdBu_r", aspect="auto", vmin=-2.3, vmax=2.3)
    ax.set_xticks(range(10))
    ax.set_xticklabels([f"S{i+1}" for i in range(10)])
    ax.set_yticks(range(8))
    ax.set_yticklabels([f"Marker {i+1}" for i in range(8)])
    ax.set_title("Biomarker / omics heatmap style")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Standardized value")
    savefig("fig10_heatmap.pdf")


def fig_case_timeline() -> None:
    fig, ax = plt.subplots(figsize=(9, 3.8))
    days = [0, 2, 5, 12, 30, 90]
    labels = ["Presentation", "Index test", "Diagnosis", "Intervention", "Follow-up", "Outcome"]
    y = np.zeros(len(days))
    ax.hlines(0, min(days) - 5, max(days) + 5, color=GRAY, lw=1)
    ax.scatter(days, y, s=95, color=BLUE, zorder=3)
    for i, (d, lab) in enumerate(zip(days, labels)):
        offset = 0.34 if i % 2 == 0 else -0.42
        ax.text(d, offset, lab, ha="center", va="center", fontsize=8)
        ax.vlines(d, 0, offset * 0.72, color=GRAY, lw=0.8)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])
    ax.set_xlabel("Study day")
    ax.set_title("Case-report patient timeline style")
    ax.spines[["left", "top", "right"]].set_visible(False)
    savefig("fig11_case_timeline.pdf")


def fig_global_health_burden() -> None:
    years = np.arange(2018, 2026)
    regions = {
        "Region A": np.array([24, 23, 25, 26, 28, 27, 26, 25]),
        "Region B": np.array([18, 19, 20, 22, 21, 22, 23, 24]),
        "Region C": np.array([12, 14, 13, 15, 16, 18, 19, 20]),
    }
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for name, vals in regions.items():
        ax.plot(years, vals, marker="o", label=name)
        ax.fill_between(years, vals - 1.5, vals + 1.5, alpha=0.12)
    ax.set_ylabel("Rate per 100,000")
    ax.set_xlabel("Year")
    ax.set_title("Global-health stratified estimate with uncertainty")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    savefig("fig12_global_health_burden.pdf")


def fig_icer_plane() -> None:
    rng = np.random.default_rng(5)
    de = rng.normal(0.06, 0.025, 400)
    dc = rng.normal(1800, 1400, 400)
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    ax.scatter(de, dc, s=16, alpha=0.35, color=BLUE)
    ax.axhline(0, color=GRAY, lw=1)
    ax.axvline(0, color=GRAY, lw=1)
    ax.plot([0, 0.14], [0, 7000], color=ORANGE, ls="--", label="WTP threshold")
    ax.set_xlabel("Incremental effect")
    ax.set_ylabel("Incremental cost")
    ax.set_title("Health-economics ICER plane")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    savefig("fig13_icer_plane.pdf")


def fig_tornado_sensitivity() -> None:
    labels = ["Intervention cost", "Baseline event risk", "Utility gain", "Follow-up cost", "Discount rate"]
    low = np.array([-2100, -1600, -1200, -800, -450])
    high = np.array([1900, 1400, 1250, 900, 500])
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.barh(y, low, color=ORANGE, alpha=0.8)
    ax.barh(y, high, color=BLUE, alpha=0.8)
    ax.axvline(0, color=GRAY, lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Change in net monetary benefit")
    ax.set_title("One-way sensitivity tornado plot")
    ax.grid(axis="x", alpha=0.25)
    savefig("fig14_tornado_sensitivity.pdf")


def fig_model_schematic() -> None:
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    steps = [
        (1.1, "Eligibility\ncriteria"),
        (3.0, "Randomization\n1:1"),
        (4.9, "Intervention /\nComparator"),
        (6.8, "Outcome\nassessment"),
        (8.7, "Checklist +\nstatements"),
    ]
    for x, text in steps:
        box(ax, (x, 2.1), text, width=1.55, height=1.0, face=LIGHT_BLUE if x < 4 else LIGHT_ORANGE)
    for i in range(len(steps) - 1):
        arrow(ax, (steps[i][0] + 0.8, 2.1), (steps[i + 1][0] - 0.8, 2.1))
    ax.text(0.2, 3.5, "Trial reporting schematic", fontsize=12, fontweight="bold")
    ax.text(0.2, 0.55, "Use: methods overview, supplement, or graphical abstract style. Synthetic demonstration only.", fontsize=8)
    savefig("fig15_model_schematic.pdf")


def tex_table(headers, rows, align=None, width=True, spec=None):
    align = align or ["l"] * len(headers)
    if spec:
        table_spec = spec
    elif width:
        table_spec = ">{\\raggedright\\arraybackslash}p{0.24\\linewidth}" + "".join(
            [">{\\raggedright\\arraybackslash}p{0.18\\linewidth}" for _ in headers[1:]]
        )
    else:
        table_spec = "".join(align)
    out = [f"\\begin{{tabular}}{{@{{}}{table_spec}@{{}}}}", "\\toprule"]
    out.append(" & ".join(headers) + r" \\")
    out.append("\\midrule")
    for row in rows:
        out.append(" & ".join(row) + r" \\")
    out.append("\\bottomrule")
    out.append("\\end{tabular}")
    return "\n".join(out)


def table_env(
    label,
    caption,
    body,
    small=True,
    wide=False,
    inline_wide=False,
    direct=False,
    tabcolsep="3pt",
):
    size = "\\small\n" if small else ""
    body_block = f"{{\n{size}\\setlength{{\\tabcolsep}}{{{tabcolsep}}}\n{body}\n}}"
    if direct:
        return f"""\\begin{{center}}
\\refstepcounter{{table}}\\label{{{label}}}
\\noindent\\textbf{{Table~\\thetable}}\\hspace{{0.5em}}{caption}\\par\\vspace{{0.35em}}
{body_block}
\\end{{center}}
"""
    if inline_wide:
        return f"""\\begin{{table*}}[!t]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
{body_block}
\\end{{table*}}
"""
    env = "table*" if wide else "table"
    placement = "!t" if wide else "!htbp"
    return f"""\\begin{{{env}}}[{placement}]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
{body_block}
\\end{{{env}}}
"""


def merge_strip_tables(first: str, second: str) -> str:
    first_block = first.strip()
    second_block = second.strip()
    if not (
        first_block.startswith("\\begin{strip}")
        and first_block.endswith("\\end{strip}")
        and second_block.startswith("\\begin{strip}")
        and second_block.endswith("\\end{strip}")
    ):
        return first + "\n" + second
    first_body = first_block.removesuffix("\\end{strip}").rstrip()
    second_body = second_block.removeprefix("\\begin{strip}").lstrip()
    return first_body + "\n\n\\vspace{1.1em}\n" + second_body + "\n"


def merge_strip_table_group(*blocks: str) -> str:
    merged = blocks[0]
    for block in blocks[1:]:
        merged = merge_strip_tables(merged, block)
    return merged


def write_references() -> None:
    (PAPER / "references.bib").write_text(
        r"""@misc{icmje2026,
  author = {{International Committee of Medical Journal Editors}},
  title = {Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals},
  year = {2026},
  note = {Updated January 2026. Accessed 16 June 2026},
  howpublished = {\url{https://www.icmje.org/recommendations/}}
}

@misc{consort2025equator,
  author = {{EQUATOR Network}},
  title = {CONSORT 2025 Statement: updated guideline for reporting randomised trials},
  year = {2025},
  note = {Accessed 16 June 2026},
  howpublished = {\url{https://www.equator-network.org/reporting-guidelines/consort/}}
}

@misc{consortspirit,
  author = {{CONSORT-SPIRIT}},
  title = {CONSORT and SPIRIT reporting guidelines},
  year = {2026},
  note = {Accessed 16 June 2026},
  howpublished = {\url{https://www.consort-spirit.org/}}
}
""",
        encoding="utf-8",
    )


def write_submission_package() -> None:
    (PAPER / "submission-package.md").write_text(
        """# Submission Package Snapshot

Target journal: medical journal / target TBD
Article type: synthetic display gallery for randomized trial reporting
Selected reporting checklist: CONSORT 2025
Statement framework: ICMJE Recommendations, updated January 2026
Template status: package-local generic LaTeX review shell, not an official journal template
Official sources checked: 2026-06-16
Figure sizing: evidence-weighted widths rather than one uniform full-page width
Compiled PDF: paper/main.pdf
Reference rendering: deterministic in-manuscript reference list; references.bib retained as source snapshot

Readiness verdict: NOT submission-ready. This is a synthetic style gallery for inspecting figure and table layouts. It contains no real trial evidence, no real ethics approval, no registration ID, and no data-sharing record.
""",
        encoding="utf-8",
    )


def write_checklist_matrix() -> None:
    rows = [
        ("CONSORT-01", "trial_design", "Title/Abstract; Methods", "satisfied for demo", "Synthetic RCT display gallery"),
        ("CONSORT-02", "participants_setting", "Methods", "satisfied for demo", "Synthetic adults; no real sites"),
        ("CONSORT-03", "interventions", "Methods", "satisfied for demo", "Synthetic intervention/comparator labels"),
        ("CONSORT-randomization", "randomization", "Methods", "satisfied for demo", "Computer-generated 1:1 allocation"),
        ("CONSORT-05", "allocation_concealment_blinding", "Methods", "partial", "Display demo; no real trial operations"),
        ("CONSORT-06", "outcomes_sample_size", "Methods", "satisfied for demo", "Synthetic endpoints and sample counts"),
        ("CONSORT-07", "statistical_methods", "Methods", "satisfied for demo", "Synthetic descriptive estimates"),
        ("CONSORT-08", "participant_flow_baseline", "Results; Figures/Tables", "satisfied for demo", "Flow diagram and baseline table"),
        ("CONSORT-09", "outcomes_harms", "Results", "satisfied for demo", "Outcome and harms displays"),
        ("CONSORT-10", "registration_protocol_ethics", "Statements", "not_applicable for demo", "No real human participant study"),
    ]
    text = "# CONSORT 2025 Demonstration Checklist Matrix\n\n"
    text += "| item_id | item | target_section | status | source_evidence |\n"
    text += "|---|---|---|---|---|\n"
    for row in rows:
        text += "| " + " | ".join(row) + " |\n"
    (PAPER / "checklist_compliance_matrix.md").write_text(text, encoding="utf-8")


def write_main_tex() -> None:
    tables = []
    tables.append(table_env(
        "tab:display-plan",
        "Display-item plan covering the figure and table styles requested.",
        tex_table(
            ["Display type", "Example in PDF", "Checklist or standard link", "Synthetic source"],
            [
                ["CONSORT participant flow", "Figure 1", "CONSORT randomized trial reporting", "Generated counts"],
                ["Baseline characteristics", "Table 1", "CONSORT participant baseline data", "Generated participant profiles"],
                ["Primary/secondary outcomes", "Figure 2 and Table 2", "CONSORT outcome reporting", "Generated endpoint table"],
                ["Adverse events and safety", "Figure 3 and Table 3", "CONSORT harms reporting", "Generated event counts"],
                ["Subgroup/sensitivity forest plot", "Figure 4 and Table 4", "CONSORT subgroup caution", "Generated risk ratios"],
                ["Time-to-event display", "Figure 5", "Outcome analysis display", "Generated survival probabilities"],
                ["Systematic-review flow and funnel", "Figures 6-7; Table 5", "PRISMA-style supplementary example", "Generated study counts"],
                ["Diagnostic accuracy", "Figure 8; Tables 6-7", "STARD-style supplementary example", "Generated 2x2 counts"],
                ["Prediction model displays", "Figure 9; Table 8", "TRIPOD-style supplementary example", "Generated model metrics"],
                ["Biomarker heatmap", "Figure 10", "Omics display only when matrix source exists", "Generated normalized matrix"],
                ["Case timeline", "Figure 11; Table 9", "CARE-style supplementary example", "Generated case milestones"],
                ["Global health estimates", "Figure 12; Table 10", "GATHER-style supplementary example", "Generated rates"],
                ["Health economics", "Figures 13-14; Table 11", "CHEERS-style supplementary example", "Generated cost-effect pairs"],
                ["Trial schematic", "Figure 15", "Methods overview", "Generated workflow labels"],
                ["ICMJE statements", "Table 12", "ICMJE Recommendations", "Demonstration statement statuses"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.23\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.18\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.28\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.21\\linewidth}",
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:baseline",
        "Baseline characteristics table style with denominators and units.",
        tex_table(
            ["Characteristic", "Interv.", "Comp.", "Miss"],
            [
                ["Age, mean (SD), y", "62.1 (10.4)", "61.8 (10.7)", "0"],
                ["Female, n (\\%)", "146 (48.7)", "149 (49.7)", "0"],
                ["Risk score, mean", "7.8 (2.1)", "7.9 (2.2)", "3"],
                ["Duration, med., y", "4.2 (1.8-8.3)", "4.4 (1.9-8.1)", "5"],
                ["Prior hosp., n (\\%)", "82 (27.3)", "86 (28.7)", "0"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.35\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.23\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.23\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.09\\linewidth}",
        ),
    ))

    tables.append(table_env(
        "tab:outcomes",
        "Primary and secondary outcome table style.",
        tex_table(
            ["Endpoint", "Intervention", "Comparator", "Effect estimate"],
            [
                ["Primary 30-day event", "55/300 (18.3\\%)", "74/300 (24.7\\%)", "Risk ratio 0.74 (95\\% CI, 0.55-0.99)"],
                ["Symptom score at 12 months", "25.0 (SD 8.8)", "32.0 (SD 9.4)", "Mean difference -7.0"],
                ["Medication reconciliation", "238/300 (79.3\\%)", "211/300 (70.3\\%)", "Risk difference 9.0 percentage points"],
                ["Follow-up completion", "264/300 (88.0\\%)", "249/300 (83.0\\%)", "Risk difference 5.0 percentage points"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.22\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.16\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.16\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.34\\linewidth}",
        ),
        inline_wide=True,
    ))

    tables.append(table_env(
        "tab:harms",
        "Adverse-event and harms table style.",
        tex_table(
            ["Event", "Intervention (n=300)", "Comparator (n=300)", "Definition note"],
            [
                ["Any adverse event", "93 (31.0\\%)", "87 (29.0\\%)", "Any recorded event during follow-up"],
                ["Serious adverse event", "24 (8.0\\%)", "21 (7.0\\%)", "Required hospitalization or urgent care"],
                ["Treatment discontinuation", "15 (5.0\\%)", "12 (4.0\\%)", "Stopped assigned care pathway"],
                ["Hospitalization", "36 (12.0\\%)", "42 (14.0\\%)", "All-cause hospitalization"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.24\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.17\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.17\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.30\\linewidth}",
        ),
        inline_wide=True,
    ))

    tables.append(table_env(
        "tab:sensitivity",
        "Subgroup and sensitivity table style.",
        tex_table(
            ["Analysis", "RR", "95\\% CI", "Interpretation"],
            [
                ["Overall ITT", "0.76", "0.61-0.94", "Primary"],
                ["Complete case", "0.78", "0.60-1.01", "Missingness"],
                ["High risk", "0.68", "0.49-0.94", "Exploratory"],
                ["Age 65+", "0.72", "0.53-0.98", "Exploratory"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.29\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.10\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.20\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.27\\linewidth}",
        ),
    ))

    tables.append(table_env(
        "tab:review",
        "Risk-of-bias / study-characteristics table style for evidence synthesis.",
        tex_table(
            ["Study", "Design", "N", "Risk-of-bias signal"],
            [
                ["Study A", "RCT", "420", "Some concerns: allocation detail unclear"],
                ["Study B", "Cluster RCT", "1,180", "Low: prespecified endpoints"],
                ["Study C", "Quasi-experimental", "760", "High: confounding likely"],
                ["Study D", "RCT", "540", "Some concerns: incomplete follow-up"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.11\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.21\\linewidth}"
            ">{\\raggedleft\\arraybackslash}p{0.08\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.52\\linewidth}",
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:diagnostic2x2",
        "Diagnostic 2x2 table style.",
        tex_table(
            ["Index test", "Reference positive", "Reference negative", "Total"],
            [
                ["Positive", "142", "38", "180"],
                ["Negative", "28", "292", "320"],
                ["Total", "170", "330", "500"],
            ],
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:diagnostic-metrics",
        "Diagnostic accuracy metrics table style.",
        tex_table(
            ["Metric", "Estimate", "95\\% CI", "Required reporting note"],
            [
                ["Sensitivity", "83.5\\%", "77.1-88.7\\%", "Define reference standard"],
                ["Specificity", "88.5\\%", "84.5-91.7\\%", "Report threshold"],
                ["Positive predictive value", "78.9\\%", "72.2-84.4\\%", "State prevalence context"],
                ["Negative predictive value", "91.3\\%", "87.7-94.1\\%", "Report indeterminate results"],
            ],
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:prediction",
        "Prediction-model performance table style.",
        tex_table(
            ["Cohort", "AUC", "Calibration slope", "Clinical-utility note"],
            [
                ["Development", "0.84", "0.98", "Optimism-corrected internal result"],
                ["Internal validation", "0.81", "0.94", "Bootstrap validation"],
                ["External validation", "0.77", "0.88", "Deployment claim pending"],
                ["High-risk subgroup", "0.75", "0.83", "Fairness review required"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.22\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.10\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.18\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.40\\linewidth}",
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:case",
        "Case-report diagnostic workup and follow-up table style.",
        tex_table(
            ["Time", "Assessment", "Finding", "Reporting note"],
            [
                ["Day 0", "Presentation", "Initial synthetic cluster", "Remove identifiers"],
                ["Day 2", "Index test", "Positive synthetic result", "State threshold"],
                ["Day 5", "Reference assessment", "Confirmed synthetic condition", "Avoid overgeneralization"],
                ["Day 90", "Follow-up", "Stable synthetic status", "Consent needed for real cases"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.12\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.18\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.32\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.28\\linewidth}",
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:gather",
        "Global-health data-source inventory table style.",
        tex_table(
            ["Source", "Population", "Years", "Uncertainty handling"],
            [
                ["Registry extract", "Region A adults", "2018-2025", "Sampling interval"],
                ["Survey series", "Region B households", "2019-2025", "Design weights"],
                ["Administrative file", "Region C visits", "2018-2024", "Missingness model"],
                ["Literature estimate", "Mixed regions", "2020-2025", "Prediction interval"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.22\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.22\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.14\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.32\\linewidth}",
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:cheers",
        "Health-economic cost and effect table style.",
        tex_table(
            ["Strategy", "Cost", "Effect", "Economic result"],
            [
                ["Comparator", "\\$12,400", "6.20 QALYs", "Reference"],
                ["Intervention", "\\$14,100", "6.28 QALYs", "ICER \\$21.3k/QALY"],
                ["Low-cost scenario", "\\$13,200", "6.27 QALYs", "Dominance possible"],
                ["High-cost scenario", "\\$16,700", "6.28 QALYs", "Threshold-sensitive"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.22\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.14\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.18\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.36\\linewidth}",
        ),
        direct=True,
    ))

    tables.append(table_env(
        "tab:statements",
        "ICMJE-oriented statement status table for this synthetic demonstration.",
        tex_table(
            ["Statement", "Status", "Source evidence", "Action before real submission"],
            [
                ["Ethics/IRB", "Not applicable", "No real participants", "Provide approval or exemption"],
                ["Consent", "Not applicable", "Synthetic data only", "Provide consent or waiver"],
                ["Trial registration", "Not applicable", "No real trial", "Provide registry ID"],
                ["Data availability", "Demo only", "Synthetic values", "Replace with repository/access terms"],
                ["Funding", "Unknown", "Not supplied", "Author must provide"],
                ["Conflicts", "Unknown", "Not supplied", "Author must provide"],
                ["AI disclosure", "Provided", "AI-assisted drafting", "Adapt to target journal wording"],
            ],
            spec=">{\\raggedright\\arraybackslash}p{0.17\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.18\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.22\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.35\\linewidth}",
        ),
        direct=True,
    ))

    figure_blocks = [
        ("fig01_consort_flow.pdf", "0.72\\textwidth", True, "CONSORT participant flow diagram. The flow diagram gives denominators at eligibility, randomization, allocation, follow-up, and analysis stages."),
        ("fig02_primary_secondary_outcomes.pdf", "0.84\\textwidth", True, "Primary and secondary outcome visualization styles. Error bars and shaded bands are synthetic uncertainty displays."),
        ("fig03_harms_bar.pdf", "0.92\\columnwidth", False, "Adverse-event visualization. Event definitions and denominators must be stated when real source data are used."),
        ("fig04_forest_plot.pdf", "0.95\\columnwidth", False, "Subgroup and sensitivity forest plot. Subgroup displays should not imply confirmatory effects unless prespecified."),
        ("fig05_km_curve.pdf", "0.95\\columnwidth", False, "Kaplan-Meier-style time-to-event display with synthetic event-free probabilities."),
        ("fig06_prisma_flow.pdf", "0.96\\columnwidth", False, "PRISMA-style flow display included as a cross-check of systematic-review display style."),
        ("fig07_funnel_plot.pdf", "0.90\\columnwidth", False, "Funnel plot style for evidence synthesis. Real use requires effect estimates and standard errors from eligible studies."),
        ("fig08_roc_curve.pdf", "0.90\\columnwidth", False, "ROC curve for diagnostic accuracy or model discrimination display."),
        ("fig09_calibration_decision.pdf", "0.84\\textwidth", True, "Calibration and decision-curve display for prediction-model reporting."),
        ("fig10_heatmap.pdf", "0.76\\columnwidth", False, "Biomarker heatmap style. Real use requires a normalized source matrix and preprocessing details."),
        ("fig11_case_timeline.pdf", "0.95\\columnwidth", False, "Case-report timeline style. Real case reports require de-identification and consent review."),
        ("fig12_global_health_burden.pdf", "0.95\\columnwidth", False, "Global-health estimate display with stratified rates and uncertainty bands."),
        ("fig13_icer_plane.pdf", "0.88\\columnwidth", False, "Health-economic incremental cost-effectiveness plane."),
        ("fig14_tornado_sensitivity.pdf", "0.92\\columnwidth", False, "One-way sensitivity tornado plot for economic evaluation uncertainty."),
        ("fig15_model_schematic.pdf", "0.95\\columnwidth", False, "Trial-reporting schematic for methods overview or supplement."),
    ]

    fig_tex = []
    for i, (filename, width, wide, caption) in enumerate(figure_blocks, start=1):
        env = "figure*" if wide else "figure"
        placement = "!t" if wide else "!htbp"
        fig_tex.append(
            f"""\\begin{{{env}}}[{placement}]
\\centering
\\includegraphics[width={width}]{{figures/{filename}}}
\\caption{{{caption} Synthetic data are used only to demonstrate layout and style.}}
\\label{{fig:gallery-{i:02d}}}
\\end{{{env}}}
"""
        )

    outcome_and_harms_tables = merge_strip_tables(tables[2], tables[3])
    supplementary_tables = "\n\\vspace{1.2em}\n".join(tables[5:12])
    statement_and_display_tables = "\n\\vspace{1.2em}\n".join([tables[12], tables[0]])

    main_tex = r"""\documentclass[pdflatex,iicol,sn-vancouver-num]{sn-jnl}

\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{url}

\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\raggedbottom

\title[CONSORT and ICMJE Display Gallery]{CONSORT and ICMJE Display Gallery for Medical Manuscript Figures and Tables}
\author*[1]{\fnm{Synthetic Medical Display} \sur{Group}}
\affil*[1]{\orgdiv{Demonstration Manuscript Unit}, \orgname{Synthetic Data Only}}

\abstract{
\textbf{Background:} This PDF is a synthetic style gallery for medical manuscript display items. 
\textbf{Objective:} To show figure and table layouts covering major medical manuscript display types while framing the demonstration with CONSORT 2025 and ICMJE Recommendations.
\textbf{Methods:} Synthetic counts, rates, model metrics, costs, and evidence-synthesis values were generated deterministically. No patient-level or real trial data were used.
\textbf{Results:} The gallery includes CONSORT participant flow, baseline, outcome, harms, subgroup, time-to-event, PRISMA-style, diagnostic, prediction-model, biomarker, case-report, global-health, and health-economics displays.
\textbf{Conclusions:} The artifact is suitable for layout review only and must not be interpreted as clinical evidence or as a submission-ready manuscript.
}

\keywords{CONSORT, ICMJE, medical figures, tables, synthetic data, reporting checklist}

\begin{document}
\maketitle

\section{Scope and Source Anchors}

This demonstration uses CONSORT 2025 as the reporting-checklist frame for randomized trial displays and ICMJE Recommendations as the manuscript statement and publication-ethics frame. CONSORT is a reporting guideline for randomized trials and includes a checklist and participant-flow diagram; ICMJE provides recommendations for medical journal reporting, authorship, conflicts, trial registration, data sharing, and related publication responsibilities \cite{consort2025equator,consortspirit,icmje2026}. This document is not submission-ready.

\textbf{Synthetic data notice.} All numbers, estimates, event rates, study counts, test metrics, model performance values, costs, and statement statuses are generated for display inspection. They do not describe a real trial, patient group, intervention, diagnostic test, model, or health-economic analysis.

\section{CONSORT-Framed Randomized Trial Displays}
""" + "\n".join(fig_tex[:5]) + "\n" + tables[1] + "\n" + r"""
\clearpage
""" + outcome_and_harms_tables + r"""
\clearpage
""" + tables[4] + r"""

\section{Supplementary Cross-Study Display Styles}
This section collects supplementary display styles for evidence synthesis, diagnostic accuracy,
prediction models, case reports, global-health estimates, and health economics.
""" + "\n".join(fig_tex[5:]) + r"""
\clearpage
\onecolumn
""" + supplementary_tables + r"""

\clearpage
\section{ICMJE-Oriented Statement Package}
""" + statement_and_display_tables + r"""

\section{Checklist Notes}

The demonstration checklist notes map CONSORT evidence slots to this synthetic artifact. Because this is a demonstration, real trial registration, ethics approval, protocol access, data sharing, funding, and competing-interest facts are not asserted.

\section{Review Verdict}

\textbf{Compiled artifact status:} PDF generated for layout review. 
\textbf{Submission readiness:} Fail by design. The document uses synthetic data, no target journal, no real participant evidence, no ethics approval, no trial registration, and no real data-sharing record.

\begin{thebibliography}{3}

\bibitem{consort2025equator}
EQUATOR Network. CONSORT 2025 Statement: updated guideline for reporting randomised trials. Accessed 16 June 2026. \url{https://www.equator-network.org/reporting-guidelines/consort/}.

\bibitem{consortspirit}
CONSORT-SPIRIT. CONSORT and SPIRIT reporting guidelines. Accessed 16 June 2026. \url{https://www.consort-spirit.org/}.

\bibitem{icmje2026}
International Committee of Medical Journal Editors. Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals. Updated January 2026. Accessed 16 June 2026. \url{https://www.icmje.org/recommendations/}.

\end{thebibliography}

\end{document}
"""
    (PAPER / "main.tex").write_text(main_tex, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a synthetic all-display-types medical manuscript demo."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / "academic_medicine_all_display_types_demo",
        help="Output directory to recreate. Default: ./academic_medicine_all_display_types_demo",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure(args.output)
    ensure_dirs()
    fig_consort_flow()
    fig_primary_secondary_outcomes()
    fig_harms_bar()
    fig_forest_plot()
    fig_km_curve()
    fig_prisma_flow()
    fig_funnel_plot()
    fig_roc_curve()
    fig_calibration_decision()
    fig_heatmap()
    fig_case_timeline()
    fig_global_health_burden()
    fig_icer_plane()
    fig_tornado_sensitivity()
    fig_model_schematic()
    write_references()
    write_submission_package()
    write_checklist_matrix()
    write_main_tex()
    print(f"Wrote {PAPER}")


if __name__ == "__main__":
    main()
