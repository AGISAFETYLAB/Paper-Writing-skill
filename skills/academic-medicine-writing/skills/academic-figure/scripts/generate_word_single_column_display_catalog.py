#!/usr/bin/env python3
"""Generate single-column Word display-catalog previews for medical figures/tables."""

from __future__ import annotations

import argparse
import csv
import html
import json
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageStat

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
FIGURE_SCRIPT_DIR = Path(__file__).resolve().parent
REVIEW_SCRIPT_DIR = PACKAGE_ROOT / "skills/academic-review/scripts"
WRITING_SCRIPT_DIR = PACKAGE_ROOT / "skills/academic-writing/scripts"
WORD_TEMPLATE = PACKAGE_ROOT / "assets/templates/word/generic-medical-word-reference.docx"
DEFAULT_OUTPUT = Path("medical_word_single_column_display_catalog")
DEFAULT_RSCRIPT = Path("Rscript")

for script_dir in (FIGURE_SCRIPT_DIR, REVIEW_SCRIPT_DIR, WRITING_SCRIPT_DIR):
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
import generate_chart_type_overview as chart_overview  # noqa: E402
from render_medical_word_docx import (  # noqa: E402
    A_NS,
    PIC_NS,
    R_NS,
    WP_NS,
    add_content_type_defaults,
    document_rels_xml,
    paragraph_xml,
    patch_styles_xml,
    table_borders_xml,
    text_runs_xml,
)


EMU_PER_INCH = 914_400
TEXT_WIDTH_DXA = 9_360
TEXT_WIDTH_IN = 6.5
MAX_FIGURE_HEIGHT_IN = 4.6


@dataclass(frozen=True)
class SizeSpec:
    size_class: str
    insert_width_in: float
    max_height_in: float
    native_size: tuple[float, float]
    role: str


@dataclass(frozen=True)
class FigureRecord:
    number: int
    category_slug: str
    category: str
    subtype_slug: str
    subtype: str
    png: Path
    pdf: Path | None
    size: SizeSpec
    inserted_width_in: float
    inserted_height_in: float
    width_px: int
    height_px: int
    stddev: float


@dataclass(frozen=True)
class TableSpec:
    slug: str
    title: str
    layout_class: str
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]
    widths: tuple[int, ...]
    note: str


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def inspect_png(path: Path) -> tuple[int, int, float]:
    image = Image.open(path).convert("L")
    stat = ImageStat.Stat(image)
    return image.width, image.height, float(stat.stddev[0])


def placed_size(path: Path, width_in: float, max_height_in: float) -> tuple[float, float]:
    with Image.open(path) as image:
        width_px, height_px = image.size
    height_in = width_in * height_px / max(width_px, 1)
    if height_in > max_height_in:
        height_in = max_height_in
        width_in = min(width_in, max_height_in * width_px / max(height_px, 1))
    return round(width_in, 3), round(height_in, 3)


def size_for_display(category_slug: str, subtype_slug: str, subtype: str) -> SizeSpec:
    key = f"{category_slug}/{subtype_slug}/{subtype}".lower()
    if any(token in key for token in ("clinical_triptych", "image_plate", "segmentation", "before_after", "multi_endpoint", "image_quant")):
        return SizeSpec("wide", 6.15, 4.25, (6.6, 3.9), "multi-panel clinical evidence")
    if any(token in key for token in ("consort", "prisma", "cohort_flow", "workflow", "pathway")):
        return SizeSpec("wide", 5.9, 4.45, (6.3, 4.3), "flow or schematic")
    if any(token in key for token in ("grouped_bar_dense", "stacked", "percent_stacked", "waterfall", "ribbon", "spaghetti", "annotated_heatmap", "missingness", "risk_bias", "correlation", "meta_forest", "evidence_summary", "upset", "choropleth", "budget")):
        return SizeSpec("wide", 5.75, 4.15, (6.2, 3.9), "dense comparison")
    if any(token in key for token in ("heatmap", "confusion", "pca", "volcano", "enrichment", "ma_plot")):
        return SizeSpec("square-medium", 4.65, 4.2, (4.8, 4.0), "matrix or scatter display")
    if any(token in key for token in ("forest", "balance", "coefficients", "risk_groups", "lift", "paired", "ridgeline", "timeline")):
        return SizeSpec("standard", 5.1, 3.75, (5.3, 3.4), "moderate label burden")
    if any(token in key for token in ("roc", "pr", "calibration", "decision", "kaplan", "hazard", "funnel", "icer", "ceac", "tornado", "simple_bar", "single_line", "histogram", "density", "boxplot", "violin", "strip", "ecdf", "lollipop")):
        return SizeSpec("compact", 3.85, 2.9, (4.1, 2.8), "sparse single-panel plot")
    return SizeSpec("standard", 4.8, 3.55, (5.0, 3.2), "standard single-column display")


def configure_single_panel_matplotlib() -> None:
    chart_overview.configure_matplotlib()
    matplotlib.rcParams.update(
        {
            "font.size": 7.8,
            "axes.titlesize": 8.5,
            "axes.labelsize": 7.6,
            "xtick.labelsize": 6.9,
            "ytick.labelsize": 6.9,
            "legend.fontsize": 6.8,
        }
    )


def render_python_figures(output_dir: Path) -> list[FigureRecord]:
    figures_dir = output_dir / "figures"
    pdf_dir = output_dir / "pdf"
    figures_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    configure_single_panel_matplotlib()
    records: list[FigureRecord] = []
    number = 1
    for cat_idx, category in enumerate(chart_overview.categories(), start=1):
        family = chart_overview.palette_for_category(category, "auto")
        display_family = chart_overview.CATEGORY_DISPLAY_FAMILY.get(category.slug, "bar")
        chart_overview.set_active_palette(display_family, family)
        for item_idx, item in enumerate(category.items, start=1):
            size = size_for_display(category.slug, item.slug, item.label)
            stem = f"figure{number}_{category.slug}_{item.slug}"
            png = figures_dir / f"{stem}.png"
            pdf = pdf_dir / f"{stem}.pdf"
            rng = np.random.default_rng(20260624 + cat_idx * 1000 + item_idx)
            fig, ax = plt.subplots(figsize=size.native_size)
            fig.patch.set_facecolor("white")
            item.draw(ax, rng)
            fig.text(0.01, 0.985, item.label, ha="left", va="top", fontsize=8.0, fontweight="bold", color="#333333")
            fig.text(0.99, 0.985, size.size_class, ha="right", va="top", fontsize=6.5, color="#555555")
            fig.savefig(png, dpi=260, bbox_inches="tight", facecolor="white")
            fig.savefig(pdf, bbox_inches="tight", facecolor="white")
            plt.close(fig)
            width_px, height_px, stddev = inspect_png(png)
            placed_width, placed_height = placed_size(png, size.insert_width_in, size.max_height_in)
            records.append(
                FigureRecord(
                    number,
                    category.slug,
                    category.plain_name,
                    item.slug,
                    item.label,
                    png,
                    pdf,
                    size,
                    placed_width,
                    placed_height,
                    width_px,
                    height_px,
                    stddev,
                )
            )
            number += 1
    return records


def r_string_vector(values: Iterable[str]) -> str:
    return "c(" + ", ".join(json.dumps(value) for value in values) + ")"


def write_r_renderer(r_dir: Path, figure_templates: list[FigureRecord]) -> Path:
    script = r_dir / "generate_r_medical_display_catalog.R"
    numbers = [str(record.number) for record in figure_templates]
    category_slugs = [record.category_slug for record in figure_templates]
    subtype_slugs = [record.subtype_slug for record in figure_templates]
    categories = [record.category for record in figure_templates]
    subtypes = [record.subtype for record in figure_templates]
    code = f'''#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args) >= 1) args[[1]] else getwd()
fig_dir <- file.path(out, "figures")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)
palette <- c("#4EAB90", "#8EB69C", "#EDDCC3", "#EEBF6D", "#D94F33", "#5E82A2", "#D15354")
figures <- data.frame(
  number = c({", ".join(numbers)}),
  category_slug = {r_string_vector(category_slugs)},
  subtype_slug = {r_string_vector(subtype_slugs)},
  category = {r_string_vector(categories)},
  subtype = {r_string_vector(subtypes)},
  stringsAsFactors = FALSE
)

draw_flow <- function(subtype, category) {{
  plot.new(); plot.window(xlim = c(0, 10), ylim = c(0, 10)); title(main = subtype, cex.main = 0.9)
  y <- c(8.2, 6.2, 4.2, 2.2)
  for (j in seq_along(y)) {{
    rect(2, y[j] - 0.48, 8, y[j] + 0.48, col = palette[(j %% length(palette)) + 1], border = "#555555")
    text(5, y[j], paste("Step", j, "n =", 900 - 120 * j), cex = 0.75)
    if (j < length(y)) arrows(5, y[j] - 0.55, 5, y[j + 1] + 0.55, length = 0.08, col = "#555555")
  }}
  mtext(category, side = 3, adj = 1, line = 0.15, cex = 0.58, col = "#555555")
}}

draw_generic <- function(i) {{
  subtype <- figures$subtype_slug[i]
  label <- figures$subtype[i]
  category <- figures$category[i]
  filename <- file.path(fig_dir, sprintf("figure%d_%s_%s.png", figures$number[i], figures$category_slug[i], subtype))
  png(filename, width = 1600, height = 1050, res = 260)
  par(family = "sans", mar = c(4, 4, 3, 1), col.axis = "#333333", col.lab = "#333333", cex = 0.9)
  key <- paste(subtype, label, category)
  if (grepl("flow|timeline|pathway|workflow", key)) {{
    draw_flow(label, category)
  }} else if (grepl("heatmap|matrix|risk|confusion|missing|correlation", key)) {{
    z <- matrix(rnorm(49), 7, 7)
    image(z, col = colorRampPalette(c("#5E82A2", "#F7F7F7", "#D15354"))(80), axes = FALSE, main = label, cex.main = 0.9)
    axis(1, at = seq(0, 1, length.out = 7), labels = paste0("C", 1:7), las = 2, cex.axis = 0.65)
    axis(2, at = seq(0, 1, length.out = 7), labels = paste0("R", 1:7), las = 2, cex.axis = 0.65)
  }} else if (grepl("forest|funnel|icer|coefficient|balance", key)) {{
    y <- 1:6; est <- rnorm(6, 0, 0.28); lo <- est - runif(6, 0.15, 0.35); hi <- est + runif(6, 0.15, 0.35)
    plot(est, y, xlim = range(lo, hi), pch = 19, col = palette[6], yaxt = "n", xlab = "Estimate", ylab = "", main = label, cex.main = 0.9)
    segments(lo, y, hi, y, col = "#555555"); abline(v = 0, lty = 2, col = "#888888")
    axis(2, at = y, labels = paste("Stratum", y), las = 2, cex.axis = 0.62)
  }} else if (grepl("bar|harms|tornado|budget|waterfall", key)) {{
    vals <- abs(rnorm(5, 20, 6))
    barplot(vals, col = palette[seq_along(vals)], border = "#4A4A4A", ylab = "Synthetic value", main = label, cex.main = 0.9)
  }} else if (grepl("image|triptych|endpoint|segmentation", key)) {{
    layout(matrix(c(1, 2, 3), nrow = 1), widths = c(1.1, 1.1, 0.9))
    image(matrix(runif(100), 10, 10), col = colorRampPalette(c("#15202B", "#4EAB90", "#EDDCC3"))(60), axes = FALSE, main = "a")
    image(matrix(runif(100), 10, 10), col = colorRampPalette(c("#15202B", "#5E82A2", "#D15354"))(60), axes = FALSE, main = "b")
    barplot(c(42, 68), col = palette[c(1, 5)], border = "#555555", ylim = c(0, 80), main = "c", ylab = "Signal")
  }} else {{
    x <- seq(0, 1, length.out = 18)
    y1 <- pmin(1, pmax(0, 0.18 + cumsum(rnorm(length(x), 0.035, 0.025))))
    y2 <- pmin(1, pmax(0, 0.24 + cumsum(rnorm(length(x), 0.025, 0.025))))
    plot(x, y1, type = "l", lwd = 2, col = palette[6], ylim = c(0, 1), xlab = "Synthetic x", ylab = "Synthetic y", main = label, cex.main = 0.9)
    lines(x, y2, lwd = 2, col = palette[5])
    legend("bottomright", legend = c("Group A", "Group B"), col = palette[c(6, 5)], lwd = 2, bty = "n", cex = 0.72)
  }}
  dev.off()
}}

set.seed(20260624)
for (i in seq_len(nrow(figures))) draw_generic(i)
write.csv(figures, file.path(out, "r_figure_manifest.csv"), row.names = FALSE)
cat("R display catalog written to", out, "\\n")
'''
    script.write_text(code, encoding="utf-8")
    script.chmod(0o755)
    return script


def render_r_figures(r_dir: Path, templates: list[FigureRecord], rscript: Path) -> list[FigureRecord]:
    rscript_command = str(rscript)
    if not rscript.exists():
        resolved = shutil.which(str(rscript))
        if resolved is None:
            raise FileNotFoundError(f"Rscript not found on PATH: {rscript}")
        rscript_command = resolved
    renderer = write_r_renderer(r_dir, templates)
    subprocess.run([rscript_command, str(renderer), str(r_dir)], check=True)
    records: list[FigureRecord] = []
    for template in templates:
        png = r_dir / "figures" / f"figure{template.number}_{template.category_slug}_{template.subtype_slug}.png"
        width_px, height_px, stddev = inspect_png(png)
        placed_width, placed_height = placed_size(png, template.size.insert_width_in, template.size.max_height_in)
        records.append(
            FigureRecord(
                template.number,
                template.category_slug,
                template.category,
                template.subtype_slug,
                template.subtype,
                png,
                None,
                template.size,
                placed_width,
                placed_height,
                width_px,
                height_px,
                stddev,
            )
        )
    return records


def table_specs() -> list[TableSpec]:
    return [
        TableSpec("display_item_plan", "Display-item plan table", "text-heavy planning table", ("Item", "Claim supported", "Source / denominator", "Layout"), (("Figure 1", "Shows analytic cohort construction.", "Screening log; n=842 screened.", "Compact or wide by flow complexity"), ("Table 1", "Compares baseline covariates.", "Analysis cohort; group denominators.", "Editable Word table"), ("Figure 2", "Displays primary event-rate difference.", "Outcome file; 30-day follow-up.", "Standard single-column")), (1200, 2900, 3000, 2260), "Planning tables are text-heavy and need wide meaning-bearing columns."),
        TableSpec("baseline_characteristics", "Baseline characteristics / cohort table", "numeric-heavy baseline table", ("Characteristic", "Intervention n=291", "Comparator n=349", "SMD", "Missing"), (("Age, median (IQR), y", "68 (59-77)", "70 (61-78)", "0.11", "4 (0.6%)"), ("Female sex, No. (%)", "132 (45.4)", "164 (47.0)", "0.03", "0"), ("Prior stroke, No. (%)", "87 (29.9)", "112 (32.1)", "0.05", "2 (0.3%)"), ("NIHSS score, median (IQR)", "5 (3-8)", "6 (3-9)", "0.09", "8 (1.3%)")), (2450, 1700, 1700, 900, 1100), "Numeric columns stay compact; the characteristic column carries units and missingness context."),
        TableSpec("primary_secondary_outcomes", "Primary and secondary outcomes table", "outcome table with wide effect column", ("Outcome", "Intervention", "Comparator", "Effect estimate (95% CI)", "P value"), (("30-day readmission, No. (%)", "49/291 (16.8)", "90/349 (25.8)", "Risk difference -8.9 pp (-14.9 to -2.9)", ".004"), ("Any emergency visit, No. (%)", "71/291 (24.4)", "109/349 (31.2)", "Risk difference -6.8 pp (-13.5 to -0.1)", ".047"), ("Functional follow-up completed", "238/291 (81.8)", "259/349 (74.2)", "Risk ratio 1.10 (1.02 to 1.19)", ".02")), (2200, 1400, 1400, 3300, 700), "The effect-estimate column is deliberately wider than count columns."),
        TableSpec("adverse_event_harms", "Adverse-event / harms table", "harms table with notes column", ("Event", "Severity", "Intervention", "Comparator", "Definition / denominator"), (("Bleeding event", "Serious", "3/291", "5/349", "Hospital-treated event within 30 days."), ("Fall with injury", "Moderate", "6/291", "8/349", "Emergency or clinic documentation."), ("Medication reaction", "Non-serious", "11/291", "15/349", "Self-report confirmed in record.")), (1850, 1300, 1200, 1200, 3810), "Harms tables need room for severity and denominator definitions."),
        TableSpec("subgroup_sensitivity", "Subgroup or sensitivity table", "estimate table", ("Analysis", "Subgroup / scenario", "Estimate", "95% CI", "Interaction / note"), (("Primary", "Age <70 y", "0.72", "0.50 to 1.04", "Exploratory"), ("Primary", "Age >=70 y", "0.61", "0.43 to 0.88", "Exploratory"), ("Sensitivity", "Complete-case", "0.66", "0.49 to 0.90", "Consistent direction")), (1600, 2050, 1050, 1600, 3060), "Scenario labels and caveats stay readable without widening numeric columns."),
        TableSpec("risk_bias_study_characteristics", "Risk-of-bias / study-characteristics table", "review text-heavy table", ("Study", "Design / population", "Key limitation", "Risk judgment"), (("Study A", "Prospective cohort; 3 hospitals.", "Outcome assessors were not masked.", "Some concerns"), ("Study B", "Registry-based cohort; national data.", "Exposure timing partly missing.", "Moderate"), ("Study C", "Randomized trial; 2 arms.", "Early stopping for recruitment.", "Low")), (1450, 3100, 3350, 1460), "Evidence-synthesis tables allocate width to rationale fields."),
        TableSpec("diagnostic_2x2", "Diagnostic 2x2 table", "compact diagnostic table", ("Index test", "Reference positive", "Reference negative", "Total"), (("Positive", "84", "21", "105"), ("Negative", "16", "179", "195"), ("Total", "100", "200", "300")), (2100, 2420, 2420, 2420), "Threshold and reference-standard notes should sit in caption/table note."),
        TableSpec("diagnostic_accuracy", "Diagnostic accuracy metrics table", "diagnostic metrics table", ("Metric", "Estimate", "95% CI", "Definition"), (("Sensitivity", "0.84", "0.76 to 0.91", "Positive reference standard correctly classified."), ("Specificity", "0.90", "0.85 to 0.94", "Negative reference standard correctly classified."), ("Positive predictive value", "0.80", "0.71 to 0.87", "At 33% demonstration prevalence."), ("Negative predictive value", "0.92", "0.88 to 0.95", "At 33% demonstration prevalence.")), (2000, 1200, 1800, 4360), "The definition column absorbs text so metric names do not stack."),
        TableSpec("prediction_performance", "Prediction-model performance table", "prediction metrics table", ("Cohort", "AUC", "Calibration slope", "Brier score", "Events / N"), (("Development", "0.78", "0.94", "0.141", "156/900"), ("Internal validation", "0.75", "0.91", "0.148", "49/291"), ("External validation", "0.73", "0.88", "0.152", "82/620")), (2400, 1200, 1900, 1500, 2360), "Development and validation cohorts must remain distinct."),
        TableSpec("case_timeline_workup", "Case timeline / diagnostic workup table", "case-report table", ("Day", "Clinical event", "Test / treatment", "Interpretation"), (("0", "Emergency presentation", "CT angiography", "No hemorrhage; stenosis suspected."), ("2", "Neurologic worsening", "MRI diffusion sequence", "New ischemic lesion."), ("7", "Discharge follow-up", "Medication reconciliation", "Adherence barrier identified.")), (900, 2850, 2850, 2760), "Timeline tables need a narrow time column and wider event/action columns."),
        TableSpec("global_health_sources", "Global-health data-source inventory table", "data-source inventory table", ("Source", "Geography / years", "Measure", "Completeness note"), (("Civil registration", "Region A; 2018-2025", "Mortality rate", "Lagged by one reporting year."), ("Household survey", "Region B; 2021", "Coverage estimate", "Cluster weights required."), ("Facility registry", "Region C; monthly", "Service volume", "Private-sector capture incomplete.")), (2200, 2100, 1850, 3210), "Inventory tables should expose source limitations."),
        TableSpec("health_economic_costs", "Health-economics costs/effects table", "cost-effect table", ("Strategy", "Cost, USD", "QALYs", "Incremental cost", "Incremental QALYs"), (("Usual care", "12,400", "7.82", "Reference", "Reference"), ("Care pathway A", "13,250", "7.96", "850", "0.14"), ("Care pathway B", "14,100", "8.01", "1,700", "0.19")), (2000, 1500, 1200, 2300, 2360), "Currency year, perspective, and time horizon belong in the note/caption."),
        TableSpec("icmje_statement", "ICMJE-oriented statement table", "submission statement table", ("Statement domain", "Required item", "Current status", "Action before submission"), (("Ethics", "Approval and consent statement", "Pending author confirmation", "Insert IRB identifier or exemption basis."), ("Data sharing", "Data availability and restrictions", "Drafted", "Verify repository/access conditions."), ("Conflicts", "ICMJE disclosure forms", "Not collected", "Collect from every author.")), (1650, 2850, 1800, 3060), "Statement tables are text-heavy and should not use equal narrow columns."),
    ]


def write_table_csvs(tables_dir: Path, specs: Iterable[TableSpec]) -> None:
    tables_dir.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        with (tables_dir / f"{spec.slug}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(spec.columns)
            writer.writerows(spec.rows)


def table_cell_xml(text: str, header: bool = False) -> str:
    return (
        '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        f'{text_runs_xml(text, None, size="18", base_bold=header)}</w:p>'
    )


def custom_table_xml(spec: TableSpec) -> str:
    rows = [spec.columns, *spec.rows]
    widths = spec.widths
    if sum(widths) > TEXT_WIDTH_DXA:
        scale = TEXT_WIDTH_DXA / sum(widths)
        widths = tuple(max(700, int(width * scale)) for width in widths)
    grid_cols = "".join(f'<w:gridCol w:w="{width}"/>' for width in widths)
    parts = [
        '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9360" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        + table_borders_xml("tblBorders", ("top", "left", "bottom", "right", "insideH", "insideV"), sz="6")
        + '<w:tblCellMar><w:top w:w="70" w:type="dxa"/><w:left w:w="85" w:type="dxa"/>'
        '<w:bottom w:w="70" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
        "</w:tblPr>"
        f"<w:tblGrid>{grid_cols}</w:tblGrid>"
    ]
    for row_idx, row in enumerate(rows):
        parts.append("<w:tr>")
        if row_idx == 0:
            parts.append("<w:trPr><w:tblHeader/></w:trPr>")
        for col_idx, width in enumerate(widths):
            text = row[col_idx] if col_idx < len(row) else ""
            fill = "EAF2F7" if row_idx == 0 else ("F8FAFA" if row_idx % 2 == 0 else "FFFFFF")
            cell_pr = (
                f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
                + table_borders_xml("tcBorders", ("top", "left", "bottom", "right"), sz="4", color="A6A6A6")
                + f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>'
            )
            parts.append(f"<w:tc>{cell_pr}{table_cell_xml(text, header=row_idx == 0)}</w:tc>")
        parts.append("</w:tr>")
    parts.append("</w:tbl>")
    return "".join(parts)


def image_xml(record: FigureRecord, rid: str, docpr_id: int) -> str:
    width_emu = int(record.inserted_width_in * EMU_PER_INCH)
    height_emu = int(record.inserted_height_in * EMU_PER_INCH)
    name = html.escape(record.png.name)
    return f"""
<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0">
<wp:extent cx="{width_emu}" cy="{height_emu}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{docpr_id}" name="{name}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic><a:graphicData uri="{PIC_NS}">
<pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>
</a:graphicData></a:graphic>
</wp:inline>
</w:drawing></w:r></w:p>"""


def manuscript_prose(category: str, size_class: str) -> str:
    return (
        f"The {category.lower()} displays are placed here as they would appear inside a Results section. "
        f"This paragraph is synthetic manuscript text used to test how {size_class} figures interact "
        "with prose, captions, page breaks, and editable Word tables."
    )


def render_docx(output_docx: Path, backend: str, figures: list[FigureRecord], tables: list[TableSpec]) -> int:
    body: list[str] = []
    media: list[tuple[str, Path, str]] = []
    prose_count = 0
    body.append(paragraph_xml(f"Medical Display Catalog Preview: {backend} Backend", "Title", "center"))
    body.append(paragraph_xml("Synthetic cohort display package for single-column Word layout inspection."))
    prose_count += 1
    body.append(paragraph_xml("Abstract", "Heading1", page_break_before=True))
    for text in (
        "Importance: Medical manuscripts mix sparse diagnostic curves, dense flow diagrams, editable clinical tables, and multi-panel imaging displays.",
        "Objective: This preview tests whether Word output preserves display-specific sizing instead of scaling every figure to the same width.",
        "Design: All values are synthetic. The purpose is layout verification, not scientific inference.",
    ):
        body.append(paragraph_xml(text))
        prose_count += 1
    body.append(paragraph_xml("Introduction", "Heading1", page_break_before=True))
    for text in (
        "Clinical papers rely on displays to carry denominators, uncertainty, and analysis populations. A visually valid package must therefore test both figures and editable tables in the same Word flow.",
        "The generated manuscript uses a single text column with one-inch margins. Compact displays remain compact, while dense figures receive more width only when the reading task requires it [1].",
    ):
        body.append(paragraph_xml(text))
        prose_count += 1
    body.append(paragraph_xml("Methods", "Heading1"))
    for text in (
        f"The {backend} backend generated the plotted figures. Word assembly only embeds the produced assets and keeps tables editable.",
        "Figure dimensions are assigned from display family, label density, panel count, and likely caption burden. The layout audit records every inserted width and height.",
    ):
        body.append(paragraph_xml(text))
        prose_count += 1
    body.append(paragraph_xml("Results", "Heading1", page_break_before=True))
    current_category = None
    for record in figures:
        if record.category != current_category:
            current_category = record.category
            body.append(paragraph_xml(record.category, "Heading2"))
            body.append(paragraph_xml(manuscript_prose(record.category, record.size.size_class)))
            prose_count += 1
        if record.number % 4 == 1:
            body.append(paragraph_xml("The next display block is intentionally embedded between prose paragraphs to expose crowded captions, stranded headings, and sparse full-width figure pages."))
            prose_count += 1
        body.append(
            paragraph_xml(
                f"**Figure {record.number}. {record.subtype}.** "
                f"Size class: {record.size.size_class}; inserted size: {record.inserted_width_in:.2f} x {record.inserted_height_in:.2f} in. "
                "Synthetic data are shown for Word layout testing only.",
                "Caption",
            )
        )
        rid = f"rIdImage{record.number}"
        media.append((rid, record.png, f"figure{record.number}.png"))
        body.append(image_xml(record, rid, record.number))
        if record.number % 5 == 0:
            body.append(paragraph_xml("This short follow-up paragraph simulates interpretation text after a figure and checks that the next display does not appear as a detached gallery item."))
            prose_count += 1
    body.append(paragraph_xml("Discussion", "Heading1", page_break_before=True))
    for text in (
        "The preview deliberately varies display size to keep low-density plots from dominating the page while preserving readability for dense multi-panel displays.",
        "A passing structural audit does not imply scientific readiness; it only confirms that the Word package embeds figures, preserves editable tables, and records layout decisions.",
    ):
        body.append(paragraph_xml(text))
        prose_count += 1
    body.append(paragraph_xml("References", "Heading1", page_break_before=True))
    body.append(paragraph_xml("1. Synthetic layout reference used only to exercise superscript citation rendering in this Word preview."))
    prose_count += 1
    body.append(paragraph_xml("Editable Tables", "Heading1", page_break_before=True))
    for idx, spec in enumerate(tables, start=1):
        body.append(paragraph_xml(f"**Table {idx}. {spec.title}.** {spec.note}", "Caption"))
        body.append(custom_table_xml(spec))
        body.append(paragraph_xml(f"Layout class: {spec.layout_class}.", "Caption"))

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="{R_NS}" xmlns:wp="{WP_NS}" xmlns:a="{A_NS}" xmlns:pic="{PIC_NS}">
  <w:body>
    {''.join(body)}
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
  </w:body>
</w:document>'''.encode("utf-8")

    image_exts = {path.suffix.lower().lstrip(".") for _, path, _ in media}
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(WORD_TEMPLATE) as src, zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            if info.filename in {"word/document.xml", "word/_rels/document.xml.rels"}:
                continue
            if info.filename == "[Content_Types].xml":
                dst.writestr(info, add_content_type_defaults(src.read(info.filename), image_exts))
            elif info.filename == "word/styles.xml":
                dst.writestr(info, patch_styles_xml(src.read(info.filename)))
            else:
                dst.writestr(info, src.read(info.filename))
        dst.writestr("word/document.xml", document_xml)
        dst.writestr("word/_rels/document.xml.rels", document_rels_xml([(rid, f"media/{name}") for rid, _, name in media]))
        for _, image_path, name in media:
            dst.writestr(f"word/media/{name}", image_path.read_bytes())
    return prose_count


def write_manifest(path: Path, backend: str, figures: list[FigureRecord], tables: list[TableSpec]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["kind", "backend", "number", "category", "slug", "title", "size_class", "inserted_width_in", "inserted_height_in", "asset", "layout_class"])
        for record in figures:
            writer.writerow(["figure", backend, record.number, record.category, f"{record.category_slug}/{record.subtype_slug}", record.subtype, record.size.size_class, record.inserted_width_in, record.inserted_height_in, record.png, record.size.role])
        for idx, spec in enumerate(tables, start=1):
            writer.writerow(["table", "office-native", idx, "Editable Medical Tables", spec.slug, spec.title, "", "", "", f"tables/{spec.slug}.csv", spec.layout_class])


def write_layout_audit(root: Path, backend: str, docx: Path, figures: list[FigureRecord], tables: list[TableSpec], prose_count: int) -> dict:
    counts = Counter(record.size.size_class for record in figures)
    audit = {
        "word_display_catalog": {
            "backend": backend,
            "word_route_only": True,
            "docx": str(docx),
            "figure_count": len(figures),
            "table_count": len(tables),
            "text_width_in": TEXT_WIDTH_IN,
            "max_figure_height_in": MAX_FIGURE_HEIGHT_IN,
            "min_unique_widths": 3,
            "prose_paragraphs": prose_count,
            "size_class_counts": dict(counts),
            "unique_inserted_widths": sorted({record.inserted_width_in for record in figures}),
            "figures": [
                {
                    "number": record.number,
                    "slug": f"{record.category_slug}/{record.subtype_slug}",
                    "size_class": record.size.size_class,
                    "inserted_width_in": record.inserted_width_in,
                    "inserted_height_in": record.inserted_height_in,
                    "png": str(record.png),
                }
                for record in figures
            ],
            "tables": [
                {"slug": spec.slug, "layout_class": spec.layout_class, "width_dxa": sum(spec.widths)}
                for spec in tables
            ],
        }
    }
    (root / "layout_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    return audit


def run_audits(root: Path, docx: Path, expected_figures: int) -> tuple[dict, str]:
    word_cmd = [sys.executable, str(REVIEW_SCRIPT_DIR / "audit_word_docx.py"), str(docx), "--expected-figures", str(expected_figures), "--json"]
    word_proc = subprocess.run(word_cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    try:
        word_report = json.loads(word_proc.stdout)
    except json.JSONDecodeError:
        word_report = {"status": "BLOCKED", "stdout": word_proc.stdout, "stderr": word_proc.stderr}
    display_cmd = [sys.executable, str(FIGURE_SCRIPT_DIR / "audit_display_layout.py"), "--preview-root", str(root)]
    display_proc = subprocess.run(display_cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return word_report, display_proc.stdout.strip()


def write_backend_readme(root: Path, backend: str, figures: list[FigureRecord], tables: list[TableSpec], word_report: dict, display_audit: str) -> None:
    counts = Counter(record.size.size_class for record in figures)
    lines = [
        f"# {backend} Backend Single-Column Word Preview",
        "",
        "- Data: synthetic demonstration values for layout inspection only.",
        f"- Figure subtype panels: {len(figures)}.",
        f"- Editable Word table types: {len(tables)}.",
        f"- DOCX structure audit: {word_report.get('status', 'UNKNOWN')}.",
        f"- Display layout audit: `{display_audit}`.",
        "",
        "| Size class | Count |",
        "|---|---:|",
    ]
    for key in sorted(counts):
        lines.append(f"| {key} | {counts[key]} |")
    lines.append("")
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def build_backend(root: Path, backend: str, figures: list[FigureRecord], tables: list[TableSpec]) -> dict:
    write_table_csvs(root / "tables", tables)
    preview_dir = root / "preview_docx"
    preview_dir.mkdir(parents=True, exist_ok=True)
    docx = root / f"medical_word_single_column_{backend.lower()}.docx"
    prose_count = render_docx(docx, backend, figures, tables)
    shutil.copy2(docx, preview_dir / docx.name)
    write_manifest(root / "display_manifest.csv", backend, figures, tables)
    write_layout_audit(root, backend, docx, figures, tables, prose_count)
    word_report, display_audit = run_audits(root, docx, len(figures))
    (root / "docx_structure_audit.json").write_text(json.dumps(word_report, indent=2, sort_keys=True), encoding="utf-8")
    (root / "display_layout_audit.txt").write_text(display_audit + "\n", encoding="utf-8")
    write_backend_readme(root, backend, figures, tables, word_report, display_audit)
    return {"docx": str(docx), "word_audit": word_report.get("status"), "display_audit": display_audit}


def write_root_readme(root: Path, reports: dict[str, dict]) -> None:
    lines = [
        "# Medical Word Single-Column Display Preview",
        "",
        "Generated by `academic-medicine-writing/skills/academic-figure/scripts/generate_word_single_column_display_catalog.py`.",
        "",
        "| Backend | DOCX | Word audit | Display audit |",
        "|---|---|---|---|",
    ]
    for backend, report in reports.items():
        lines.append(f"| {backend} | `{Path(report['docx']).relative_to(root)}` | `{report.get('word_audit')}` | `{report.get('display_audit')}` |")
    lines.append("")
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--rscript", type=Path, default=DEFAULT_RSCRIPT)
    parser.add_argument("--skip-r", action="store_true")
    args = parser.parse_args()

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    python_root = output / "python_backend"
    r_root = output / "r_backend"
    reset_dir(python_root)
    reset_dir(r_root)

    tables = table_specs()
    python_figures = render_python_figures(python_root)
    reports: dict[str, dict] = {"Python": build_backend(python_root, "python", python_figures, tables)}

    if not args.skip_r:
        r_figures = render_r_figures(r_root, python_figures, args.rscript)
        reports["R"] = build_backend(r_root, "r", r_figures, tables)

    summary = {
        "output": str(output),
        "reports": reports,
        "figure_count": len(python_figures),
        "table_count": len(tables),
        "rscript": str(args.rscript),
    }
    (output / "generation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_root_readme(output, reports)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
