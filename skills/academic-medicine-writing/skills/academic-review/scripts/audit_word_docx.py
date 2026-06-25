#!/usr/bin/env python3
"""Audit a Word-first medical manuscript DOCX for production-quality structure."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CORE_STYLE_SIZE_RANGES = {
    "Normal": (20, 24),
    "Title": (20, 24),
    "Heading1": (20, 24),
    "Heading2": (20, 24),
    "Caption": (18, 24),
}
TABLE_BORDER_TAGS = ("top", "left", "bottom", "right", "insideH", "insideV")
CELL_BORDER_TAGS = ("top", "left", "bottom", "right")


def public_artifact_path(path: Path) -> str:
    parts = path.parts
    if "paper" in parts:
        return "/".join(parts[parts.index("paper") :])
    if path.suffix.lower() == ".docx":
        return f"paper/{path.name}"
    return path.name


def parse_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    if name not in zf.namelist():
        return None
    return ET.fromstring(zf.read(name))


def find_style(styles: ET.Element, style_id: str) -> ET.Element | None:
    for style in styles.findall(".//w:style", NS):
        if style.attrib.get(W + "styleId") == style_id:
            return style
    return None


def style_size_half_points(styles: ET.Element, style_id: str) -> int | None:
    style = find_style(styles, style_id)
    if style is None:
        return None
    size = style.find("w:rPr/w:sz", NS)
    if size is None:
        return None
    value = size.attrib.get(W + "val")
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def style_size_conforms(styles: ET.Element, style_id: str, lo: int, hi: int) -> bool:
    value = style_size_half_points(styles, style_id)
    return value is not None and lo <= value <= hi


def has_border_set(parent: ET.Element | None, border_name: str, tags: tuple[str, ...]) -> bool:
    if parent is None:
        return False
    borders = parent.find(f"w:{border_name}", NS)
    if borders is None:
        return False
    for tag in tags:
        elem = borders.find(f"w:{tag}", NS)
        if elem is None:
            return False
        if elem.attrib.get(W + "val") in {None, "nil", "none"}:
            return False
    return True


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def is_double_spaced(paragraph: ET.Element) -> bool:
    spacing = paragraph.find("w:pPr/w:spacing", NS)
    if spacing is None:
        return False
    return spacing.attrib.get(W + "lineRule") == "auto" and int(spacing.attrib.get(W + "line", "0")) >= 460


def has_page_break_before(paragraph: ET.Element) -> bool:
    return paragraph.find('.//w:br[@w:type="page"]', NS) is not None


def audit_docx(
    path: Path,
    expected_figures: int = 0,
    allow_separate_figures: bool = False,
    forbid_embedded_figures: bool = False,
) -> dict:
    result: dict = {
        "path": public_artifact_path(path),
        "status": "BLOCKED",
        "reasons": [],
        "metrics": {},
    }
    if not path.exists():
        result["reasons"].append("missing DOCX file")
        return result

    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            name_set = set(names)
            doc = parse_xml(zf, "word/document.xml")
            styles = parse_xml(zf, "word/styles.xml")
            if doc is None:
                result["reasons"].append("missing word/document.xml")
                return result
            if styles is None:
                result["reasons"].append("missing word/styles.xml")
                return result

            media_count = sum(1 for name in names if name.startswith("word/media/"))
            footer_parts = [name for name in names if name.startswith("word/footer") and name.endswith(".xml")]
            footer_text = ""
            for footer_name in footer_parts:
                footer_text += zf.read(footer_name).decode("utf-8", errors="replace")
            document_xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
            page_number_field_present = bool(
                re.search(r"<w:instrText[^>]*>\s*PAGE\s*</w:instrText>", footer_text)
                or re.search(r"<w:fldSimple[^>]+w:instr=\"PAGE", footer_text)
                or re.search(r"\bPAGE\b", footer_text)
            )
            footer_reference_present = "w:footerReference" in document_xml
            has_page_numbers = bool(footer_parts and page_number_field_present and footer_reference_present)
            has_theme = any(name.startswith("word/theme/") for name in names)
            has_numbering = "word/numbering.xml" in name_set
            has_settings = "word/settings.xml" in name_set
            paragraphs = doc.findall(".//w:p", NS)
            tables = doc.findall(".//w:tbl", NS)
            table_paragraph_ids = {id(paragraph) for table in tables for paragraph in table.findall(".//w:p", NS)}
            text_paragraphs = [
                paragraph
                for paragraph in paragraphs
                if id(paragraph) not in table_paragraph_ids and paragraph_text(paragraph).strip()
            ]
            drawings = doc.findall(".//w:drawing", NS)
            page_breaks = doc.findall('.//w:br[@w:type="page"]', NS)
            superscript_runs = doc.findall('.//w:rPr/w:vertAlign[@w:val="superscript"]', NS)
            bracket_numeric_citations = [
                text
                for text in (paragraph_text(paragraph) for paragraph in text_paragraphs)
                if re.search(r"\[\d+(?:\s*(?:,|-)\s*\d+)*\]", text)
            ]
            double_spaced_count = sum(1 for paragraph in text_paragraphs if is_double_spaced(paragraph))
            double_spacing_coverage = double_spaced_count / max(len(text_paragraphs), 1)
            pstyles = [
                style.attrib.get(W + "val")
                for style in doc.findall(".//w:pPr/w:pStyle", NS)
                if style.attrib.get(W + "val")
            ]
            table_styles = [
                style.attrib.get(W + "val")
                for style in doc.findall(".//w:tblPr/w:tblStyle", NS)
                if style.attrib.get(W + "val")
            ]
            table_border_count = sum(
                1
                for table in tables
                if has_border_set(table.find("w:tblPr", NS), "tblBorders", TABLE_BORDER_TAGS)
            )
            cells = doc.findall(".//w:tc", NS)
            cell_border_count = sum(
                1
                for cell in cells
                if has_border_set(cell.find("w:tcPr", NS), "tcBorders", CELL_BORDER_TAGS)
            )
            table_grid_count = sum(1 for table in tables if table.findall("w:tblGrid/w:gridCol", NS))
            style_nodes = styles.findall(".//w:style", NS)
            paragraph_style_coverage = len(pstyles) / max(len(paragraphs), 1)
            table_style_coverage = len(table_styles) / max(len(tables), 1) if tables else 1.0
            table_border_coverage = table_border_count / max(len(tables), 1) if tables else 1.0
            cell_border_coverage = cell_border_count / max(len(cells), 1) if cells else 1.0
            table_grid_coverage = table_grid_count / max(len(tables), 1) if tables else 1.0
            core_style_half_points = {
                style_id: style_size_half_points(styles, style_id)
                for style_id in CORE_STYLE_SIZE_RANGES
            }
            core_style_size_conformance = {
                style_id: style_size_conforms(styles, style_id, lo, hi)
                for style_id, (lo, hi) in CORE_STYLE_SIZE_RANGES.items()
            }
            minimal_ooxml = (
                len(names) <= 5
                and "word/document.xml" in name_set
                and "word/styles.xml" in name_set
                and not has_settings
                and not has_theme
                and not has_numbering
            )

            result["metrics"] = {
                "zip_entries": len(names),
                "paragraphs": len(paragraphs),
                "tables": len(tables),
                "drawings": len(drawings),
                "media_count": media_count,
                "style_count": len(style_nodes),
                "paragraph_style_coverage": round(paragraph_style_coverage, 3),
                "double_spacing_coverage": round(double_spacing_coverage, 3),
                "page_break_count": len(page_breaks),
                "footer_parts": footer_parts,
                "page_number_field_present": page_number_field_present,
                "footer_reference_present": footer_reference_present,
                "has_page_numbers": has_page_numbers,
                "superscript_reference_runs": len(superscript_runs),
                "bracket_numeric_citations": len(bracket_numeric_citations),
                "table_style_coverage": round(table_style_coverage, 3),
                "table_border_coverage": round(table_border_coverage, 3),
                "cell_border_coverage": round(cell_border_coverage, 3),
                "table_grid_coverage": round(table_grid_coverage, 3),
                "core_style_half_points": core_style_half_points,
                "core_style_size_conformance": core_style_size_conformance,
                "paragraph_style_counts": Counter(pstyles).most_common(20),
                "has_word_settings_xml": has_settings,
                "has_word_styles_xml": "word/styles.xml" in name_set,
                "has_word_theme": has_theme,
                "has_word_numbering_xml": has_numbering,
                "minimal_ooxml": minimal_ooxml,
                "has_word_media": media_count > 0,
                "has_w_drawing": len(drawings) > 0,
            }

            if minimal_ooxml:
                result["reasons"].append("minimal_ooxml: package contains document.xml and styles.xml only")
            if not has_settings:
                result["reasons"].append("missing word/settings.xml")
            if not has_theme:
                result["reasons"].append("missing word/theme/")
            if not has_numbering:
                result["reasons"].append("missing word/numbering.xml")
            if len(style_nodes) < 20:
                result["reasons"].append("word/styles.xml has fewer than 20 styles")
            if double_spacing_coverage < 0.8:
                result["reasons"].append("double_spacing_coverage below 0.8 for non-table manuscript text")
            if len(page_breaks) < 5:
                result["reasons"].append("page_break_count below JAMA section-start expectation")
            if not has_page_numbers:
                result["reasons"].append("continuous page numbering missing from title page/footer")
            if bracket_numeric_citations:
                result["reasons"].append("numeric citations remain in square brackets instead of AMA superscript")
            if len(superscript_runs) == 0:
                result["reasons"].append("no superscript reference runs found")
            if len(tables) and table_style_coverage < 0.5:
                result["reasons"].append("table_style_coverage below 0.5")
            if len(tables) and table_border_coverage < 1.0:
                result["reasons"].append("table_border_coverage below 1.0")
            if len(tables) and cell_border_coverage < 1.0:
                result["reasons"].append("cell_border_coverage below 1.0")
            if len(tables) and table_grid_coverage < 1.0:
                result["reasons"].append("table_grid_coverage below 1.0")
            for style_id, conforms in core_style_size_conformance.items():
                if not conforms:
                    lo, hi = CORE_STYLE_SIZE_RANGES[style_id]
                    result["reasons"].append(
                        f"{style_id} style size outside expected range {lo}-{hi} half-points"
                    )
            if expected_figures and not allow_separate_figures:
                if media_count < expected_figures or len(drawings) < expected_figures:
                    result["reasons"].append("word/media or w:drawing count below expected figures")
            elif expected_figures and allow_separate_figures:
                result["metrics"]["separate_upload_exception"] = True
            if forbid_embedded_figures and (media_count > 0 or len(drawings) > 0):
                result["reasons"].append("submission-clean manuscript contains embedded figures; use separate figure upload assets")

            if not result["reasons"]:
                result["status"] = "PASS"
            return result
    except zipfile.BadZipFile:
        result["reasons"].append("not a valid DOCX ZIP package")
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--expected-figures", type=int, default=0)
    parser.add_argument("--allow-separate-figures", action="store_true")
    parser.add_argument("--forbid-embedded-figures", action="store_true")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    report = audit_docx(
        args.docx,
        args.expected_figures,
        args.allow_separate_figures,
        args.forbid_embedded_figures,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"DOCX structure audit: {report['status']}")
        print(json.dumps(report["metrics"], indent=2, sort_keys=True))
        if report["reasons"]:
            print("Reasons:")
            for reason in report["reasons"]:
                print(f"- {reason}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
