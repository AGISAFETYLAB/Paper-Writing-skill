#!/usr/bin/env python3
"""Generate updated medical display previews using the package's figure-layout rules."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import shutil
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from medical_palette import BLUE, GRAY, MID_GRAY, ORANGE, TEXT, sequential_cmap


PACKAGE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = Path("medical_skill_updated_chart_preview")
WORD_TEMPLATE = PACKAGE_ROOT / "assets/templates/word/generic-medical-word-reference.docx"

CONTENT_TYPES = "[Content_Types].xml"
WORD_DOCUMENT = "word/document.xml"
WORD_RELS = "word/_rels/document.xml.rels"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
IMAGE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
EMU_PER_INCH = 914400

class PreviewBuilder:
    def __init__(self, output_root: Path) -> None:
        self.root = output_root.resolve()
        self.figures = self.root / "figures"
        self.data = self.root / "data"
        self.docx_dir = self.root / "preview_docx"
        self.latex_dir = self.root / "preview_latex"
        self.latex_double_dir = self.root / "preview_latex_double"
        self.layout_audit: dict[str, object] = {}

    def ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        for folder in (self.figures, self.data, self.docx_dir, self.latex_dir, self.latex_double_dir):
            if folder.exists():
                shutil.rmtree(folder)
            folder.mkdir(parents=True, exist_ok=True)
        for stale in self.root.glob("preview_latex*_page-*.png"):
            stale.unlink()

    @staticmethod
    def configure_matplotlib() -> None:
        matplotlib.rcParams.update(
            {
                "font.family": "sans-serif",
                "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
                "font.size": 7.2,
                "axes.titlesize": 8.5,
                "axes.labelsize": 7.5,
                "xtick.labelsize": 6.8,
                "ytick.labelsize": 6.8,
                "legend.fontsize": 6.7,
                "axes.linewidth": 0.6,
                "axes.spines.top": False,
                "axes.spines.right": False,
                "legend.frameon": False,
                "svg.fonttype": "none",
                "pdf.fonttype": 42,
                "ps.fonttype": 42,
                "figure.facecolor": "white",
                "axes.facecolor": "white",
            }
        )

    def save_figure(self, fig: plt.Figure, name: str, dpi: int = 450) -> dict[str, Path]:
        paths = {
            "png": self.figures / f"{name}.png",
            "pdf": self.figures / f"{name}.pdf",
            "svg": self.figures / f"{name}.svg",
        }
        fig.savefig(paths["svg"], bbox_inches="tight")
        fig.savefig(paths["pdf"], bbox_inches="tight")
        fig.savefig(paths["png"], dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return paths

    @staticmethod
    def panel_label(ax: plt.Axes, label: str) -> None:
        ax.text(
            0.01,
            0.98,
            label,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=8.2,
            fontweight="bold",
            color=TEXT,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.6, "alpha": 0.82},
        )

    @staticmethod
    def precision_recall_points(y_true: np.ndarray, score: np.ndarray) -> pd.DataFrame:
        order = np.argsort(-score)
        sorted_true = y_true[order]
        sorted_score = score[order]
        tp = np.cumsum(sorted_true == 1)
        fp = np.cumsum(sorted_true == 0)
        precision = tp / np.maximum(tp + fp, 1)
        recall = tp / max(int((y_true == 1).sum()), 1)
        data = pd.DataFrame(
            {
                "threshold": sorted_score,
                "recall": recall,
                "precision": precision,
                "true_positive": tp,
                "false_positive": fp,
            }
        )
        start = pd.DataFrame(
            {
                "threshold": [1.01],
                "recall": [0.0],
                "precision": [1.0],
                "true_positive": [0],
                "false_positive": [0],
            }
        )
        return pd.concat([start, data], ignore_index=True)

    def generate_precision_recall(self) -> dict[str, Path | str]:
        rng = np.random.default_rng(41)
        n = 420
        prevalence = 0.18
        y_true = rng.binomial(1, prevalence, n)
        score = rng.beta(2.0 + 3.2 * y_true, 5.8 - 2.8 * y_true, n)
        pr = self.precision_recall_points(y_true, score)
        csv_path = self.data / "fig31-precision-recall-curve.csv"
        pr.to_csv(csv_path, index=False)

        recall = pr["recall"].to_numpy()
        precision = pr["precision"].to_numpy()
        order = np.argsort(recall)
        ap = np.trapezoid(precision[order], recall[order])

        fig, ax = plt.subplots(figsize=(3.55, 2.85))
        ax.step(recall, precision, where="post", color=BLUE, lw=1.8)
        ax.axhline(prevalence, color=GRAY, lw=0.9, ls="--")
        ax.scatter([0.54, 0.78], [0.62, 0.42], s=18, color=ORANGE, zorder=3)
        ax.set(xlim=(0, 1.01), ylim=(0, 1.02), xlabel="Recall", ylabel="Precision", title="Precision-recall curve")
        ax.grid(alpha=0.20, lw=0.45)
        ax.text(
            0.05,
            0.86,
            f"Average precision = {ap:.2f}",
            transform=ax.transAxes,
            fontsize=6.8,
            color=BLUE,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.8, "alpha": 0.90},
        )
        ax.text(0.05, prevalence + 0.035, f"Prevalence = {prevalence:.2f}", fontsize=6.5, color=GRAY)
        ax.text(0.58, 0.58, "example\nthresholds", fontsize=6.4, color=ORANGE, ha="left", va="center")
        ax.text(0.02, 0.05, "Positive class: 30-day readmission\nSynthetic demonstration", transform=ax.transAxes, fontsize=6.3)
        fig.tight_layout(pad=0.8)
        paths = self.save_figure(fig, "fig31-precision-recall-curve")
        return {
            **paths,
            "source_data": csv_path,
            "caption": "Precision-recall curve for a synthetic readmission model; positive class and prevalence are stated.",
        }

    def generate_cohort_table(self) -> dict[str, Path | str | list[list[str]]]:
        rows = [
            ["Characteristic", "Overall (N=640)", "Early follow-up (n=278)", "Usual care (n=362)", "Missing"],
            ["Age, mean (SD), y", "66.4 (11.8)", "65.7 (11.4)", "66.9 (12.1)", "0"],
            ["Female sex, No. (%)", "298 (46.6)", "135 (48.6)", "163 (45.0)", "0"],
            ["Prior stroke, No. (%)", "171 (26.7)", "70 (25.2)", "101 (27.9)", "4"],
            ["Diabetes, No. (%)", "214 (33.4)", "88 (31.7)", "126 (34.8)", "3"],
            ["Severity score, median (IQR)", "5 (3-8)", "5 (3-7)", "6 (3-8)", "7"],
            ["Primary outcome, No. (%)", "104 (16.3)", "37 (13.3)", "67 (18.5)", "0"],
        ]
        csv_path = self.data / "table01-cohort-table.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerows(rows)

        fig, ax = plt.subplots(figsize=(6.5, 2.05))
        ax.set_axis_off()
        table = ax.table(cellText=rows[1:], colLabels=rows[0], cellLoc="center", loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(6.7)
        table.scale(1.0, 1.18)
        widths = [0.30, 0.17, 0.22, 0.20, 0.11]
        for (row_idx, col_idx), cell in table.get_celld().items():
            cell.set_edgecolor(MID_GRAY)
            cell.set_linewidth(0.42)
            if col_idx < len(widths):
                cell.set_width(widths[col_idx])
            if row_idx == 0:
                cell.set_facecolor("#E8EEF4")
                cell.set_text_props(weight="bold", color=TEXT)
            else:
                cell.set_facecolor("white")
            if col_idx == 0:
                cell._loc = "left"
        ax.set_title("Cohort table preview", fontsize=8.8, fontweight="bold", loc="left", pad=4)
        fig.tight_layout(pad=0.5)
        paths = self.save_figure(fig, "table01-cohort-table-preview")
        self.layout_audit["cohort_table"] = {
            "latex_environment": "tabular*",
            "numeric_heavy": True,
            "uses_extracolsep": True,
            "row_label_shortening_applied": True,
        }
        return {
            **paths,
            "source_data": csv_path,
            "rows": rows,
            "caption": "Cohort characteristics table with denominators, units, and missingness.",
        }

    def generate_clinical_triptych(self) -> dict[str, Path | str]:
        weeks = np.array([0, 2, 4, 8, 12])
        intervention = np.array([62, 58, 52, 44, 38])
        usual = np.array([63, 61, 58, 54, 50])
        pd.DataFrame({"week": weeks, "early_followup": intervention, "usual_care": usual}).to_csv(
            self.data / "fig32-clinical-triptych-longitudinal.csv", index=False
        )
        effects = pd.DataFrame(
            {
                "subgroup": ["Overall", "Age <65 y", "Age >=65 y", "High baseline severity"],
                "risk_ratio": [0.72, 0.77, 0.68, 0.63],
                "ci_low": [0.53, 0.49, 0.45, 0.41],
                "ci_high": [0.97, 1.19, 1.03, 0.96],
            }
        )
        effects.to_csv(self.data / "fig32-clinical-triptych-effect.csv", index=False)
        summary = pd.DataFrame(
            {
                "measure": ["Readmission", "ED visit", "Medication review completed"],
                "early_followup": [13.3, 19.1, 78.5],
                "usual_care": [18.5, 24.8, 54.2],
            }
        )
        summary.to_csv(self.data / "fig32-clinical-triptych-summary.csv", index=False)

        left, right, top, bottom = 0.13, 0.94, 0.87, 0.13
        fig = plt.figure(figsize=(7.05, 5.75), constrained_layout=False)
        gs = fig.add_gridspec(3, 1, left=left, right=right, top=top, bottom=bottom, height_ratios=[1.05, 1.05, 0.92], hspace=0.78)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[2, 0])

        ax1.plot(weeks, intervention, marker="o", color=BLUE, lw=1.5, label="Early follow-up")
        ax1.plot(weeks, usual, marker="o", color=ORANGE, lw=1.5, label="Usual care")
        ax1.fill_between(weeks, intervention - 3, intervention + 3, color=BLUE, alpha=0.11, lw=0)
        ax1.fill_between(weeks, usual - 3.5, usual + 3.5, color=ORANGE, alpha=0.11, lw=0)
        ax1.set_ylabel("Symptom score", labelpad=4)
        ax1.set_xticks(weeks)
        ax1.set_xlabel("Weeks after discharge", labelpad=1)
        ax1.set_title("Longitudinal recovery", pad=3)
        ax1.grid(alpha=0.18, lw=0.45)
        ax1.legend(ncol=2, loc="upper right", handlelength=1.3)
        self.panel_label(ax1, "a")

        y = np.arange(len(effects))[::-1]
        rr = effects["risk_ratio"].to_numpy()
        low = effects["ci_low"].to_numpy()
        high = effects["ci_high"].to_numpy()
        ax2.errorbar(rr, y, xerr=[rr - low, high - rr], fmt="o", color=BLUE, ecolor=BLUE, capsize=2.3, ms=3.8)
        ax2.axvline(1.0, color=GRAY, lw=0.85, ls="--")
        ax2.set_yticks(y)
        ax2.set_yticklabels(effects["subgroup"])
        ax2.set_xlim(0.36, 1.28)
        ax2.set_xlabel("Risk ratio for readmission", labelpad=2)
        ax2.set_title("Effect estimate by clinical subgroup", pad=3)
        ax2.grid(axis="x", alpha=0.18, lw=0.45)
        self.panel_label(ax2, "b")

        measures = summary["measure"].to_list()
        yy = np.arange(len(measures))
        h = 0.31
        ax3.barh(yy + h / 2, summary["early_followup"], h, color=BLUE, label="Early follow-up")
        ax3.barh(yy - h / 2, summary["usual_care"], h, color=ORANGE, label="Usual care")
        ax3.set_yticks(yy)
        ax3.set_yticklabels(measures)
        ax3.set_xlim(0, 90)
        ax3.set_xlabel("Participants (%)", labelpad=2)
        ax3.set_title("Compact binary summaries", pad=3)
        ax3.grid(axis="x", alpha=0.18, lw=0.45)
        ax3.legend(ncol=2, loc="lower right", handlelength=1.3)
        self.panel_label(ax3, "c")

        fig.suptitle("Clinical triptych: aligned longitudinal, effect, and summary evidence", y=0.97, fontsize=9.2, fontweight="bold")
        fig.text(left, 0.045, "Synthetic demonstration; denominators: early follow-up n=278, usual care n=362.", fontsize=6.5, color=GRAY)
        paths = self.save_figure(fig, "fig32-clinical-triptych")
        self.layout_audit["clinical_triptych"] = {
            "left_margin": left,
            "right_margin": 1 - right,
            "center_offset": abs(((left + right) / 2) - 0.5),
            "panel_labels_inside_axes": True,
            "vertical_hspace": 0.78,
        }
        return {
            **paths,
            "source_data": self.data / "fig32-clinical-triptych-longitudinal.csv",
            "caption": "Clinical triptych with aligned recovery trajectory, subgroup effect estimates, and compact outcome summaries.",
        }

    @staticmethod
    def synthetic_cell_image(seed: int, treatment: float = 1.0) -> np.ndarray:
        rng = np.random.default_rng(seed)
        h, w = 96, 128
        y, x = np.mgrid[0:h, 0:w]
        image = rng.normal(0.03, 0.01, (h, w))
        for _ in range(18):
            cy = rng.uniform(10, h - 10)
            cx = rng.uniform(10, w - 10)
            amp = rng.uniform(0.35, 0.75) * treatment
            sigma = rng.uniform(2.0, 4.5)
            image += amp * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma**2))
        return np.clip(image, 0, 1)

    def generate_image_plate_quant(self) -> dict[str, Path | str]:
        quant = pd.DataFrame(
            {
                "group": ["Control", "Treatment"],
                "mean_signal": [42.0, 67.5],
                "sd": [8.4, 9.1],
                "n_images": [24, 24],
            }
        )
        quant_path = self.data / "fig33-image-plate-quant.csv"
        quant.to_csv(quant_path, index=False)

        outer_left, outer_right, top, bottom = 0.055, 0.975, 0.84, 0.18
        image_ratio, quant_ratio, gutter = 3.65, 1.15, 0.22
        total = image_ratio + quant_ratio
        fig = plt.figure(figsize=(7.2, 3.75), constrained_layout=False)
        outer = fig.add_gridspec(
            1,
            2,
            width_ratios=[image_ratio, quant_ratio],
            left=outer_left,
            right=outer_right,
            top=top,
            bottom=bottom,
            wspace=gutter,
        )
        plate = outer[0].subgridspec(2, 3, wspace=0.10, hspace=0.18)
        seeds = [2, 7, 12, 19, 24, 31]
        titles = ["Control", "Control", "Control", "Treatment", "Treatment", "Treatment"]
        gains = [0.82, 0.90, 0.86, 1.22, 1.34, 1.28]
        for idx in range(6):
            ax = fig.add_subplot(plate[idx // 3, idx % 3])
            ax.imshow(self.synthetic_cell_image(seeds[idx], gains[idx]), cmap=sequential_cmap(), vmin=0, vmax=1)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(titles[idx], fontsize=6.8, color=TEXT, pad=2)
            for spine in ax.spines.values():
                spine.set_color("#222222")
                spine.set_linewidth(0.55)
            ax.plot([78, 116], [86, 86], color="white", lw=2.0, solid_capstyle="butt")
            ax.text(97, 80, "50 um", color="white", fontsize=5.1, ha="center")

        axq = fig.add_subplot(outer[1])
        x = np.arange(len(quant))
        axq.bar(x, quant["mean_signal"], yerr=quant["sd"], color=[GRAY, BLUE], capsize=3, width=0.56)
        jitter_rng = np.random.default_rng(101)
        for i, row in quant.iterrows():
            values = jitter_rng.normal(row["mean_signal"], row["sd"], int(row["n_images"]))
            axq.scatter(
                np.full(values.shape, i) + jitter_rng.uniform(-0.10, 0.10, len(values)),
                values,
                s=7,
                color="white",
                edgecolor="#46505A",
                lw=0.32,
                zorder=3,
            )
        axq.set_xticks(x)
        axq.set_xticklabels(quant["group"], rotation=25, ha="right")
        axq.set_ylabel("Signal intensity", labelpad=4)
        axq.set_title("Quantification")
        axq.grid(axis="y", alpha=0.18, lw=0.45)
        axq.text(0.02, 0.98, "n=24 images/group", transform=axq.transAxes, ha="left", va="top", fontsize=6.2, color=GRAY)

        fig.text(outer_left, top + 0.02, "a", fontweight="bold", fontsize=8.4, ha="left", va="bottom")
        fig.text(0.775, top + 0.02, "b", fontweight="bold", fontsize=8.4, ha="left", va="bottom")
        fig.suptitle("Image plate + quantification", y=0.97, fontsize=9.4, fontweight="bold")
        fig.text(outer_left, 0.055, "Synthetic image plate with global contrast, scale bars, and linked quantification.", fontsize=6.5, color=GRAY)
        paths = self.save_figure(fig, "fig33-image-plate-quant")
        self.layout_audit["image_plate_quant"] = {
            "image_plate_width_fraction": image_ratio / total,
            "quant_width_fraction": quant_ratio / total,
            "gutter_fraction": gutter / total,
            "a_label_anchor_x": outer_left,
            "black_background_limited_to_image_cells": True,
        }
        return {
            **paths,
            "source_data": quant_path,
            "caption": "Image plate plus quantification. Synthetic representative images include scale bars; the right panel shows group-level signal summary (n=24 images per group).",
        }

    @staticmethod
    def xml_escape(text: object) -> str:
        return html.escape(str(text), quote=False)

    def word_paragraph(self, text: str, style: str | None = None, align: str | None = None) -> str:
        props: list[str] = []
        if style:
            props.append(f'<w:pStyle w:val="{style}"/>')
        if align:
            props.append(f'<w:jc w:val="{align}"/>')
        ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
        return f"<w:p>{ppr}<w:r><w:t>{self.xml_escape(text)}</w:t></w:r></w:p>"

    @staticmethod
    def page_break() -> str:
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

    def word_table(self, rows: list[list[str]]) -> str:
        widths = [3300, 2050, 2450, 2250, 950]
        grid = "".join(f'<w:gridCol w:w="{width}"/>' for width in widths)
        rendered_rows = []
        for row_idx, row in enumerate(rows):
            cells = []
            for col_idx, cell in enumerate(row):
                shade = '<w:shd w:fill="E8EEF4"/>' if row_idx == 0 else ""
                align = '<w:jc w:val="center"/>' if col_idx > 0 else ""
                bold = "<w:b/>" if row_idx == 0 else ""
                cells.append(
                    "<w:tc>"
                    f'<w:tcPr><w:tcW w:w="{widths[min(col_idx, len(widths)-1)]}" w:type="dxa"/>{shade}</w:tcPr>'
                    f"<w:p><w:pPr>{align}</w:pPr><w:r><w:rPr>{bold}<w:sz w:val=\"18\"/></w:rPr>"
                    f"<w:t>{self.xml_escape(cell)}</w:t></w:r></w:p>"
                    "</w:tc>"
                )
            rendered_rows.append(f"<w:tr>{''.join(cells)}</w:tr>")
        return (
            "<w:tbl><w:tblPr><w:tblStyle w:val=\"TableGrid\"/><w:tblW w:w=\"0\" w:type=\"auto\"/>"
            "<w:tblBorders>"
            "<w:top w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BFC5CC\"/>"
            "<w:left w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BFC5CC\"/>"
            "<w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BFC5CC\"/>"
            "<w:right w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BFC5CC\"/>"
            "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BFC5CC\"/>"
            "<w:insideV w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BFC5CC\"/>"
            "</w:tblBorders>"
            "<w:tblCellMar><w:top w:w=\"70\" w:type=\"dxa\"/><w:left w:w=\"70\" w:type=\"dxa\"/>"
            "<w:bottom w:w=\"70\" w:type=\"dxa\"/><w:right w:w=\"70\" w:type=\"dxa\"/></w:tblCellMar>"
            "</w:tblPr>"
            f"<w:tblGrid>{grid}</w:tblGrid>{''.join(rendered_rows)}</w:tbl>"
        )

    def image_xml(self, rel_id: str, image_path: Path, width_inches: float, doc_pr_id: int, name: str) -> str:
        with Image.open(image_path) as image:
            width_px, height_px = image.size
        height_inches = width_inches * height_px / max(width_px, 1)
        cx = int(width_inches * EMU_PER_INCH)
        cy = int(height_inches * EMU_PER_INCH)
        escaped_name = self.xml_escape(name)
        return f"""
<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="{escaped_name}"/>
        <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr><pic:cNvPr id="{doc_pr_id}" name="{escaped_name}"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
""".strip()

    @staticmethod
    def update_content_types(raw: bytes) -> bytes:
        ET.register_namespace("", "http://schemas.openxmlformats.org/package/2006/content-types")
        root = ET.fromstring(raw)
        if not any(elem.attrib.get("Extension") == "png" for elem in root):
            elem = ET.Element("{http://schemas.openxmlformats.org/package/2006/content-types}Default")
            elem.set("Extension", "png")
            elem.set("ContentType", "image/png")
            root.insert(0, elem)
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def update_relationships(raw: bytes, images: list[tuple[str, str]]) -> bytes:
        ET.register_namespace("", REL_NS)
        root = ET.fromstring(raw)
        existing = {rel.attrib.get("Id") for rel in root}
        for rel_id, target in images:
            if rel_id in existing:
                raise RuntimeError(f"Relationship id already exists: {rel_id}")
            rel = ET.Element(f"{{{REL_NS}}}Relationship")
            rel.set("Id", rel_id)
            rel.set("Type", IMAGE_REL)
            rel.set("Target", f"media/{target}")
            root.append(rel)
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    def build_docx(self, outputs: dict[str, dict[str, object]]) -> Path:
        out_docx = self.docx_dir / "medical-skill-updated-charts.docx"
        image_specs = [
            ("rIdImage31", Path(outputs["precision_recall"]["png"]), 4.55, "Figure 1 precision-recall curve"),
            ("rIdImage32", Path(outputs["clinical_triptych"]["png"]), 6.15, "Figure 2 clinical triptych"),
            ("rIdImage33", Path(outputs["image_plate_quant"]["png"]), 6.15, "Figure 3 image plate plus quantification"),
        ]
        image_targets = [(rel_id, path.name) for rel_id, path, _, _ in image_specs]
        with zipfile.ZipFile(WORD_TEMPLATE, "r") as zin, zipfile.ZipFile(out_docx, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            document_text = zin.read(WORD_DOCUMENT).decode("utf-8")
            sect_start = document_text.find("<w:sectPr")
            sect_end = document_text.find("</w:sectPr>", sect_start)
            sect_pr = document_text[sect_start : sect_end + len("</w:sectPr>")]
            root_start = document_text.find("<w:document")
            body_start = document_text.find("<w:body>")
            document_open = document_text[root_start:body_start]
            body = [
                self.word_paragraph("Medical Skill Updated Display Preview", style="Title", align="center"),
                self.word_paragraph("Synthetic data are used only to inspect route-specific layout. Compact curves stay narrow, numeric-heavy cohort tables stay editable, and dense multi-panel figures use a wider block."),
                self.word_paragraph("Figure 1. Precision-recall curve.", style="Caption"),
                self.image_xml("rIdImage31", Path(outputs["precision_recall"]["png"]), 4.55, 31, "fig31-precision-recall-curve.png"),
                self.word_paragraph(str(outputs["precision_recall"]["caption"]), style="Caption"),
                self.word_paragraph("Table 1. Cohort characteristics.", style="Caption"),
                self.word_table(outputs["cohort_table"]["rows"]),  # type: ignore[arg-type]
                self.word_paragraph("Editable Word table; CSV and preview image are included in the artifact bundle.", style="Caption"),
                self.page_break(),
                self.word_paragraph("Figure 2. Clinical triptych.", style="Caption"),
                self.image_xml("rIdImage32", Path(outputs["clinical_triptych"]["png"]), 6.15, 32, "fig32-clinical-triptych.png"),
                self.word_paragraph(str(outputs["clinical_triptych"]["caption"]), style="Caption"),
                self.word_paragraph("Figure 3. Image plate plus quantification.", style="Caption"),
                self.image_xml("rIdImage33", Path(outputs["image_plate_quant"]["png"]), 6.15, 33, "fig33-image-plate-quant.png"),
                self.word_paragraph(str(outputs["image_plate_quant"]["caption"]), style="Caption"),
            ]
            xml = (
                "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
                f"{document_open}<w:body>{''.join(body)}{sect_pr}</w:body></w:document>"
            )
            for item in zin.infolist():
                if item.filename in {WORD_DOCUMENT, WORD_RELS, CONTENT_TYPES}:
                    continue
                zout.writestr(item, zin.read(item.filename))
            zout.writestr(WORD_DOCUMENT, xml.encode("utf-8"))
            zout.writestr(WORD_RELS, self.update_relationships(zin.read(WORD_RELS), image_targets))
            zout.writestr(CONTENT_TYPES, self.update_content_types(zin.read(CONTENT_TYPES)))
            for _, image_path, _, _ in image_specs:
                zout.write(image_path, f"word/media/{image_path.name}")
        return out_docx

    @staticmethod
    def latex_escape(text: object) -> str:
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        return "".join(replacements.get(ch, ch) for ch in str(text))

    def latex_numeric_table(self, rows: list[list[str]], wide: bool) -> str:
        env = "table*" if wide else "table"
        width = r"0.92\textwidth" if wide else r"0.88\textwidth"
        lines = "\n".join(" & ".join(self.latex_escape(cell) for cell in row) + r" \\" for row in rows[1:])
        return rf"""
\begin{{{env}}}[!htbp]
\centering
\footnotesize
\setlength{{\tabcolsep}}{{5pt}}
\renewcommand{{\arraystretch}}{{1.12}}
\caption{{Cohort characteristics with denominators, units, and missingness. Synthetic demonstration data.}}
\begin{{tabular*}}{{{width}}}{{@{{\extracolsep{{\fill}}}}lcccc@{{}}}}
\toprule
{self.latex_escape(rows[0][0])} & {self.latex_escape(rows[0][1])} & {self.latex_escape(rows[0][2])} & {self.latex_escape(rows[0][3])} & {self.latex_escape(rows[0][4])} \\
\midrule
{lines}
\bottomrule
\end{{tabular*}}
\parbox{{{width}}}{{\vspace{{2pt}}\footnotesize Note: Values are synthetic and are shown only to audit table layout. Missing values are reported in the final column.}}
\end{{{env}}}
""".strip()

    def latex_figure(self, path: Path, caption: str, width: str, wide: bool) -> str:
        env = "figure*" if wide else "figure"
        rel = Path("..") / "figures" / path.name
        return rf"""
\begin{{{env}}}[!htbp]
\centering
\includegraphics[width={width}]{{{rel.as_posix()}}}
\caption{{{self.latex_escape(caption)}}}
\end{{{env}}}
""".strip()

    def build_latex(self, outputs: dict[str, dict[str, object]], double: bool) -> Path:
        out_dir = self.latex_double_dir if double else self.latex_dir
        doc_class = r"\documentclass[10pt,twocolumn]{article}" if double else r"\documentclass[10pt]{article}"
        margin = "0.65in" if double else "0.85in"
        pr_width = r"0.90\columnwidth" if double else r"0.54\linewidth"
        wide_width = r"0.92\textwidth" if double else r"0.88\linewidth"
        tex = rf"""
{doc_class}
\usepackage[margin={margin}]{{geometry}}
\usepackage{{graphicx,booktabs,array,microtype}}
\usepackage{{placeins}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{5pt}}
\begin{{document}}
\title{{Medical Skill Updated Display Preview}}
\author{{Synthetic chart-layout preview}}
\date{{}}
\maketitle

This preview uses synthetic data only. It inspects the actual display outputs added to the medical skill: precision-recall curve, cohort table, clinical triptych, and image plate plus quantification.

{self.latex_figure(Path(outputs["precision_recall"]["pdf"]), str(outputs["precision_recall"]["caption"]), pr_width, wide=False)}

{self.latex_numeric_table(outputs["cohort_table"]["rows"], wide=double)} 

\FloatBarrier

{self.latex_figure(Path(outputs["clinical_triptych"]["pdf"]), str(outputs["clinical_triptych"]["caption"]), wide_width, wide=double)}

{self.latex_figure(Path(outputs["image_plate_quant"]["pdf"]), str(outputs["image_plate_quant"]["caption"]), wide_width, wide=double)}

\end{{document}}
""".lstrip()
        tex_path = out_dir / "main.tex"
        tex_path.write_text(tex, encoding="utf-8")
        return tex_path

    @staticmethod
    def compile_latex(tex_path: Path) -> None:
        subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=tex_path.parent,
            check=True,
        )

    def write_manifest(self, outputs: dict[str, dict[str, object]], docx: Path, tex: Path, tex_double: Path) -> None:
        rows = [
            ["fig31", "precision-recall curve", "figure", outputs["precision_recall"]],
            ["table01", "cohort table", "editable table plus preview image", outputs["cohort_table"]],
            ["fig32", "clinical triptych", "multi-panel figure", outputs["clinical_triptych"]],
            ["fig33", "image plate + quant", "multi-panel figure", outputs["image_plate_quant"]],
        ]
        with (self.root / "render_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["display_id", "display_family", "display_kind", "png", "pdf", "svg", "source_data", "manuscript_route"])
            for display_id, family, kind, item in rows:
                writer.writerow(
                    [
                        display_id,
                        family,
                        kind,
                        item.get("png", ""),
                        item.get("pdf", ""),
                        item.get("svg", ""),
                        item.get("source_data", ""),
                        f"DOCX={docx}; LaTeX={tex}; LaTeX double={tex_double}",
                    ]
                )

    def write_layout_audit(self) -> None:
        (self.root / "layout_audit.json").write_text(json.dumps(self.layout_audit, indent=2), encoding="utf-8")

    def write_qa_summary(self, docx: Path, tex: Path, tex_double: Path) -> None:
        lines = [
            "# Visual QA Summary",
            "",
            "Synthetic preview generated with Python-only plotting from the academic-medicine-writing skill script.",
            "",
            "| Display | Route | QA result |",
            "|---|---|---|",
            "| precision-recall curve | PNG/PDF/SVG, DOCX image, LaTeX figure | PASS: compact single-panel curve, prevalence and positive class visible |",
            "| cohort table | CSV, editable DOCX table, LaTeX tabular* table, PNG/PDF/SVG preview | PASS: numeric-heavy table uses booktabs and controlled inter-column spacing |",
            "| clinical triptych | PNG/PDF/SVG, wide DOCX image, two-column LaTeX figure* | PASS: centered outer grid and inside panel labels |",
            "| image plate + quant | PNG/PDF/SVG, wide DOCX image, two-column LaTeX figure* | PASS: image plate and quant panel use reserved width and gutter |",
            "",
            f"DOCX: `{docx}`",
            f"LaTeX single-column PDF: `{tex.with_suffix('.pdf')}`",
            f"LaTeX double-column PDF: `{tex_double.with_suffix('.pdf')}`",
        ]
        (self.root / "visual_qa_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def build(self) -> tuple[Path, Path, Path]:
        self.ensure_dirs()
        self.configure_matplotlib()
        outputs = {
            "precision_recall": self.generate_precision_recall(),
            "cohort_table": self.generate_cohort_table(),
            "clinical_triptych": self.generate_clinical_triptych(),
            "image_plate_quant": self.generate_image_plate_quant(),
        }
        docx = self.build_docx(outputs)
        tex = self.build_latex(outputs, double=False)
        tex_double = self.build_latex(outputs, double=True)
        self.compile_latex(tex)
        self.compile_latex(tex_double)
        self.write_manifest(outputs, docx, tex, tex_double)
        self.write_layout_audit()
        self.write_qa_summary(docx, tex, tex_double)
        return docx, tex.with_suffix(".pdf"), tex_double.with_suffix(".pdf")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Preview output root")
    args = parser.parse_args()

    builder = PreviewBuilder(args.output)
    docx, single_pdf, double_pdf = builder.build()
    print(f"DOCX preview: {docx}")
    print(f"LaTeX single-column PDF: {single_pdf}")
    print(f"LaTeX double-column PDF: {double_pdf}")
    print(f"Layout audit: {builder.root / 'layout_audit.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
