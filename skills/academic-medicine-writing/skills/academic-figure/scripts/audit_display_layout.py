#!/usr/bin/env python3
"""Audit rendered medical display previews for generic table and panel-layout defects."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageStat


EMU_PER_INCH = 914400


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def load_layout_audit(root: Path) -> dict:
    path = root / "layout_audit.json"
    if not path.exists():
        fail("missing layout_audit.json; generated previews must record table and panel geometry")
    return json.loads(read(path))


def audit_docx(root: Path, layout: dict) -> None:
    docx_files = sorted((root / "preview_docx").glob("*.docx"))
    if not docx_files:
        fail("missing DOCX preview under preview_docx/")
    docx = docx_files[0]
    try:
        with zipfile.ZipFile(docx) as archive:
            names = archive.namelist()
            document = archive.read("word/document.xml").decode("utf-8", errors="replace")
    except zipfile.BadZipFile:
        fail(f"not a valid DOCX zip: {docx}")

    media_count = len([name for name in names if name.startswith("word/media/")])
    drawing_count = document.count("<w:drawing>")
    table_count = document.count("<w:tbl>")
    if media_count < 3 or drawing_count < 3:
        fail("DOCX preview must embed at least three figure drawings")
    if table_count < 1:
        fail("DOCX preview must contain an editable Word table")

    catalog = layout.get("word_display_catalog")
    if catalog:
        extents = [
            (int(cx) / EMU_PER_INCH, int(cy) / EMU_PER_INCH)
            for cx, cy in re.findall(r"<wp:extent cx=\"(\d+)\" cy=\"(\d+)\"", document)
        ]
        if len(extents) < int(catalog.get("figure_count", 0)):
            fail("Word display catalog audit found fewer drawing extents than planned figures")
        unique_widths = {round(width, 2) for width, _ in extents}
        min_unique = int(catalog.get("min_unique_widths", 3))
        if len(unique_widths) < min_unique:
            fail("Word display catalog uses too few figure widths; do not scale every figure identically")
        text_width = float(catalog.get("text_width_in", 6.5))
        max_height = float(catalog.get("max_figure_height_in", 4.8))
        if any(width > text_width + 0.03 for width, _ in extents):
            fail("Word display catalog contains a figure wider than the text block")
        if any(height > max_height + 0.03 for _, height in extents):
            fail("Word display catalog contains a figure taller than the single-page budget")
        if int(catalog.get("prose_paragraphs", 0)) < 12:
            fail("Word display catalog must include manuscript-like prose paragraphs around displays")
        size_classes = catalog.get("size_class_counts", {})
        if len([name for name, count in size_classes.items() if int(count) > 0]) < 3:
            fail("Word display catalog must exercise at least three figure size classes")


def audit_latex(root: Path, layout: dict) -> None:
    single = read(root / "preview_latex/main.tex")
    double = read(root / "preview_latex_double/main.tex")

    for name, tex in (("single-column", single), ("double-column", double)):
        if tex.count("\\includegraphics") < 3:
            fail(f"{name} LaTeX preview must include the plotted figure assets")
        if "\\begin{tabular*}" not in tex:
            fail(f"{name} LaTeX cohort table must use a deliberate tabular* numeric-table layout")
        if "@{\\extracolsep{\\fill}}" not in tex:
            fail(f"{name} LaTeX table must use controlled inter-column fill, not raw equal columns")
        if "p{0.28\\textwidth}" in tex or "p{0.28\\linewidth}" in tex:
            fail(f"{name} LaTeX table still uses raw p-column widths for a numeric-heavy cohort table")

    if "\\begin{figure*}" not in double or "\\begin{table*}" not in double:
        fail("double-column LaTeX preview must use cross-column floats for wide tables/figures")

    table = layout.get("cohort_table", {})
    if table.get("latex_environment") != "tabular*":
        fail("cohort table layout audit must report tabular*")
    if not table.get("numeric_heavy"):
        fail("cohort table layout audit must classify numeric-heavy tables explicitly")


def audit_panel_geometry(layout: dict) -> None:
    triptych = layout.get("clinical_triptych", {})
    if abs(float(triptych.get("center_offset", 1))) > 0.04:
        fail("clinical triptych panels are not horizontally centered in the figure canvas")
    if float(triptych.get("left_margin", 0)) < 0.10 or float(triptych.get("right_margin", 0)) < 0.02:
        fail("clinical triptych must reserve balanced margins for labels and captions")
    if not triptych.get("panel_labels_inside_axes"):
        fail("clinical triptych panel labels must be anchored inside or flush with axes, not negative outside")
    if float(triptych.get("vertical_hspace", 0)) < 0.65:
        fail("clinical triptych must reserve enough vertical spacing between evidence bands")

    image_plate = layout.get("image_plate_quant", {})
    if float(image_plate.get("image_plate_width_fraction", 0)) < 0.64:
        fail("image plate + quant layout must reserve most width for representative images")
    if float(image_plate.get("quant_width_fraction", 0)) < 0.18:
        fail("image plate + quant layout must reserve readable width for the quantification panel")
    if float(image_plate.get("gutter_fraction", 0)) < 0.04:
        fail("image plate + quant layout must keep a visible gutter between image and quant panels")
    if float(image_plate.get("a_label_anchor_x", 1)) > 0.08:
        fail("image plate panel a label is too far right; image plate is likely visually shifted")


def audit_nonblank_pngs(root: Path) -> None:
    pngs = sorted((root / "figures").glob("*.png"))
    if not pngs:
        fail("missing PNG previews under figures/")
    for png in pngs:
        image = Image.open(png).convert("L")
        stat = ImageStat.Stat(image)
        if stat.stddev[0] <= 5:
            fail(f"blank or near-blank figure preview: {png.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-root", type=Path, required=True, help="Generated preview root")
    args = parser.parse_args()

    root = args.preview_root.resolve()
    if not root.exists():
        fail(f"preview root does not exist: {root}")
    layout = load_layout_audit(root)
    audit_docx(root, layout)
    if layout.get("word_display_catalog"):
        if not layout.get("word_display_catalog", {}).get("word_route_only", False):
            audit_latex(root, layout)
            audit_panel_geometry(layout)
    else:
        audit_latex(root, layout)
        audit_panel_geometry(layout)
    audit_nonblank_pngs(root)
    print("PASS display layout audit")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(1)
