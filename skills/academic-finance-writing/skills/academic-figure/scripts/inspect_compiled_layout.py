#!/usr/bin/env python3
"""Render compiled-paper pages and summarize layout risks.

This script turns the "inspect rendered pages" gate into a durable artifact:
page PNGs, a contact sheet, and a compact markdown summary. It deliberately
does not decide paper quality from source alone.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


FLOAT_TOO_LARGE_RE = re.compile(
    r"Float too large for page by\s+([\d.]+)pt(?:.*?line\s+([\d-]+))?",
    re.I,
)
OVERFULL_VBOX_RE = re.compile(
    r"Overfull \\vbox\s+\(([\d.]+)pt too high\)(?:.*?lines?\s+([\d-]+))?",
    re.I,
)
OVERFULL_HBOX_RE = re.compile(
    r"Overfull \\hbox\s+\(([\d.]+)pt too wide\)(?:.*?lines?\s+([\d-]+))?",
    re.I,
)
UNDERFULL_HBOX_RE = re.compile(
    r"Underfull \\hbox\s+\(badness\s+(\d+)\)\s+in paragraph at lines\s+([\d-]+)",
    re.I,
)
DISPLAY_TEXT_RE = re.compile(r"\b(?:Table|Tab\.|Figure|Fig\.)\s+\d+", re.I)
TABLE_TEXT_RE = re.compile(r"\b(?:Table|Tab\.)\s+\d+", re.I)
FIGURE_TEXT_RE = re.compile(r"\b(?:Figure|Fig\.)\s+\d+", re.I)


def parse_latex_log(log_path: Path) -> list[dict[str, Any]]:
    """Return layout-related log signals from a LaTeX log file."""
    if not log_path.exists():
        return []
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    signals: list[dict[str, Any]] = []
    for regex, kind, unit in (
        (FLOAT_TOO_LARGE_RE, "Float too large", "pt"),
        (OVERFULL_VBOX_RE, "Overfull \\vbox", "pt"),
        (OVERFULL_HBOX_RE, "Overfull \\hbox", "pt"),
    ):
        for match in regex.finditer(text):
            signals.append(
                {
                    "kind": kind,
                    "amount": float(match.group(1)),
                    "unit": unit,
                    "lines": match.group(2) or "",
                }
            )
    return signals


def parse_underfull_hbox_warnings(log_path: Path, max_examples: int = 12) -> dict[str, Any]:
    """Return a compact underfull-hbox warning summary.

    Underfull boxes are not automatically blocking: finance appendix tables can
    produce harmless warnings. A high count is still a manual readability cue.
    """
    if not log_path.exists():
        return {"count": 0, "examples": []}
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    matches = list(UNDERFULL_HBOX_RE.finditer(text))
    examples = [
        {"badness": int(match.group(1)), "lines": match.group(2)}
        for match in matches[:max_examples]
    ]
    return {"count": len(matches), "examples": examples}


def combined_layout_status(machine_status: str, manual_status: str) -> str:
    if machine_status == "blocked" or manual_status == "blocked":
        return "blocked"
    if machine_status == "pass" and manual_status == "pass":
        return "pass"
    return "partial"


def pdf_text_pages(pdf_path: Path) -> list[str]:
    """Extract per-page text with pdftotext when available."""
    if shutil.which("pdfinfo") is None or shutil.which("pdftotext") is None:
        return []
    info = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if info.returncode != 0:
        return []
    page_count = 0
    for line in info.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                page_count = int(line.split(":", 1)[1].strip())
            except ValueError:
                page_count = 0
            break
    pages: list[str] = []
    for page in range(1, page_count + 1):
        proc = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), str(pdf_path), "-"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        pages.append(proc.stdout.replace("\f", "") if proc.returncode == 0 else "")
    return pages


def detect_display_pages(pdf_path: Path) -> dict[str, list[int]]:
    """Detect likely table/figure pages from rendered PDF text."""
    pages = pdf_text_pages(pdf_path)
    table_pages: list[int] = []
    figure_pages: list[int] = []
    display_pages: list[int] = []
    for index, text in enumerate(pages, 1):
        if TABLE_TEXT_RE.search(text):
            table_pages.append(index)
        if FIGURE_TEXT_RE.search(text):
            figure_pages.append(index)
        if DISPLAY_TEXT_RE.search(text):
            display_pages.append(index)
    return {
        "table_pages": table_pages,
        "figure_pages": figure_pages,
        "display_pages": sorted(set(display_pages)),
    }


def parse_pages(value: str, total_pages: int, detected: dict[str, list[int]]) -> list[int]:
    if value == "all":
        return list(range(1, total_pages + 1))
    if value == "display":
        return detected.get("display_pages", []) or list(range(1, total_pages + 1))
    if value == "tables":
        return detected.get("table_pages", [])
    if value == "figures":
        return detected.get("figure_pages", [])
    pages: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            pages.update(range(int(lo), int(hi) + 1))
        else:
            pages.add(int(part))
    return [page for page in sorted(pages) if 1 <= page <= total_pages]


def render_pdf_pages(pdf_path: Path, out_dir: Path, pages: list[int] | None = None, dpi: int = 90) -> list[Path]:
    """Render selected PDF pages to PNG with PyMuPDF (fitz)."""
    try:
        import fitz  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError("PyMuPDF import failed; install pymupdf to render layout QA pages") from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    selected = pages or list(range(1, len(doc) + 1))
    rendered: list[Path] = []
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    for page_number in selected:
        if page_number < 1 or page_number > len(doc):
            continue
        page = doc.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        output = out_dir / f"page_{page_number:03d}.png"
        pix.save(str(output))
        rendered.append(output)
    doc.close()
    return rendered


def build_contact_sheet(image_paths: list[Path], output_path: Path, thumb_width: int = 320) -> Path | None:
    """Build a contact sheet from rendered page images."""
    if not image_paths:
        return None
    from PIL import Image, ImageDraw

    thumbs = []
    for path in image_paths:
        img = Image.open(path).convert("RGB")
        scale = thumb_width / img.width
        thumb = img.resize((thumb_width, max(1, int(img.height * scale))))
        thumbs.append((path, thumb))

    cols = max(1, min(4, math.ceil(math.sqrt(len(thumbs)))))
    label_h = 22
    pad = 12
    cell_w = thumb_width + pad * 2
    cell_h = max(thumb.height for _, thumb in thumbs) + label_h + pad * 2
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)

    for idx, (path, thumb) in enumerate(thumbs):
        row = idx // cols
        col = idx % cols
        x = col * cell_w + pad
        y = row * cell_h + pad
        sheet.paste(thumb, (x, y + label_h))
        draw.text((x, y), path.stem.replace("_", " "), fill=(40, 40, 40))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)
    return output_path


def public_artifact_path(path: Path) -> str:
    parts = path.parts
    if "paper" in parts:
        return "/".join(parts[parts.index("paper") :])
    if "layout-qa" in parts:
        return "paper/" + "/".join(parts[parts.index("layout-qa") :])
    if path.name in {"main.pdf", "main.log"}:
        return f"paper/{path.name}"
    return path.name


def write_summary(
    output_path: Path,
    pdf_path: Path,
    log_path: Path,
    rendered_pages: list[Path],
    contact_sheet: Path | None,
    detected: dict[str, list[int]],
    log_signals: list[dict[str, Any]],
    underfull_hbox_warnings: dict[str, Any] | None = None,
    render_error: str | None = None,
    manual_status: str = "not_performed",
    manual_notes: str = "",
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    machine_status = "blocked" if render_error or log_signals else "pass"
    qa_status = combined_layout_status(machine_status, manual_status)
    underfull_hbox_warnings = underfull_hbox_warnings or {"count": 0, "examples": []}
    lines = [
        "# Compiled Layout QA Summary",
        "",
        f"- PDF: `{public_artifact_path(pdf_path)}`",
        f"- Log: `{public_artifact_path(log_path)}`",
        f"- machine_layout_status: {machine_status}",
        f"- layout_manual_inspection_status: {manual_status}",
        f"- compiled_layout_qa_status: {qa_status}",
        f"- table_pages: {detected.get('table_pages', [])}",
        f"- figure_pages: {detected.get('figure_pages', [])}",
        f"- rendered_pages: {[public_artifact_path(path) for path in rendered_pages]}",
        f"- contact_sheet: `{public_artifact_path(contact_sheet)}`" if contact_sheet else "- contact_sheet: not generated",
    ]
    if render_error:
        lines.append(f"- render_error: {render_error}")
    if manual_notes:
        lines.append(f"- manual_notes: {manual_notes}")
    lines.extend(["", "## Log Signals"])
    if log_signals:
        for signal in log_signals:
            lines.append(
                f"- {signal['kind']}: {signal['amount']}{signal['unit']}"
                + (f" at lines {signal['lines']}" if signal.get("lines") else "")
            )
    else:
        lines.append("- No Float too large / Overfull \\vbox / Overfull \\hbox signals found.")
    lines.extend(["", "## Readability Warnings"])
    underfull_count = underfull_hbox_warnings.get("count", 0)
    lines.append(f"- Underfull \\hbox warning count: {underfull_count}")
    for example in underfull_hbox_warnings.get("examples", []):
        lines.append(f"- Underfull \\hbox badness {example['badness']} at lines {example['lines']}")
    lines.extend(
        [
            "",
            "## Required Human Inspection",
            "",
            "Open the contact sheet or page PNGs and check table pages for margin crossing, clipping, "
            "right-side underfill, unreadable font, sparse float pages, and float order problems.",
            "Do not record `compiled_layout_qa_status: pass` unless `layout_manual_inspection_status: pass` "
            "after inspecting the contact sheet or page PNGs.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def inspect_layout(
    paper_dir: Path,
    out_dir: Path,
    pages: str,
    dpi: int,
    manual_status: str = "not_performed",
    manual_notes: str = "",
) -> tuple[dict[str, Any], int]:
    pdf_path = paper_dir / "main.pdf"
    log_path = paper_dir / "main.log"
    out_dir.mkdir(parents=True, exist_ok=True)
    if not pdf_path.exists():
        summary = out_dir / "layout_qa_summary.md"
        write_summary(
            summary,
            pdf_path,
            log_path,
            [],
            None,
            {},
            parse_latex_log(log_path),
            parse_underfull_hbox_warnings(log_path),
            "main.pdf missing",
            manual_status=manual_status,
            manual_notes=manual_notes,
        )
        return {"ok": False, "error": "main.pdf missing", "summary": str(summary)}, 1

    detected = detect_display_pages(pdf_path)
    log_signals = parse_latex_log(log_path)
    underfull_hbox_warnings = parse_underfull_hbox_warnings(log_path)
    rendered: list[Path] = []
    contact_sheet: Path | None = None
    render_error: str | None = None

    try:
        import fitz  # type: ignore

        doc = fitz.open(str(pdf_path))
        total_pages = len(doc)
        doc.close()
        selected = parse_pages(pages, total_pages, detected)
        rendered = render_pdf_pages(pdf_path, out_dir / "pages", selected, dpi=dpi)
        contact_sheet = build_contact_sheet(rendered, out_dir / "contact_sheet.png")
    except Exception as exc:  # pragma: no cover - depends on external packages/files
        render_error = str(exc)

    summary = out_dir / "layout_qa_summary.md"
    machine_status = "blocked" if render_error or log_signals else "pass"
    qa_status = combined_layout_status(machine_status, manual_status)
    write_summary(
        summary,
        pdf_path,
        log_path,
        rendered,
        contact_sheet,
        detected,
        log_signals,
        underfull_hbox_warnings,
        render_error,
        manual_status=manual_status,
        manual_notes=manual_notes,
    )
    result = {
        "ok": render_error is None,
        "machine_layout_status": machine_status,
        "layout_manual_inspection_status": manual_status,
        "compiled_layout_qa_status": qa_status,
        "summary": public_artifact_path(summary),
        "contact_sheet": public_artifact_path(contact_sheet) if contact_sheet else None,
        "rendered_pages": [public_artifact_path(path) for path in rendered],
        "table_pages": detected.get("table_pages", []),
        "figure_pages": detected.get("figure_pages", []),
        "log_signals": log_signals,
        "underfull_hbox_warnings": underfull_hbox_warnings,
        "render_error": render_error,
        "manual_notes": manual_notes,
    }
    (out_dir / "layout_qa_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result, 0 if render_error is None else 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Render compiled-paper pages for layout/table QA.")
    parser.add_argument("paper_dir", nargs="?", default="paper", help="Paper directory containing main.pdf/main.log")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory for page PNGs, contact sheet, and layout_qa_summary.md.",
    )
    parser.add_argument(
        "--pages",
        default="all",
        help="Pages to render: all, display, tables, figures, or a list such as 1,3-5.",
    )
    parser.add_argument("--dpi", type=int, default=90, help="Rendering DPI for page PNGs.")
    parser.add_argument(
        "--manual-status",
        choices=("not_performed", "pass", "partial", "blocked"),
        default="not_performed",
        help="Manual contact-sheet/page inspection status. Default keeps compiled layout QA partial.",
    )
    parser.add_argument("--manual-notes", default="", help="Short sanitized manual inspection note.")
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    out_dir = args.out_dir.resolve() if args.out_dir else paper_dir / "layout-qa"
    result, exit_code = inspect_layout(
        paper_dir,
        out_dir,
        args.pages,
        args.dpi,
        manual_status=args.manual_status,
        manual_notes=args.manual_notes,
    )
    print(f"Compiled layout QA: {paper_dir}")
    print(f"summary: {result.get('summary')}")
    print(f"compiled layout QA status: {result.get('compiled_layout_qa_status')}")
    if result.get("contact_sheet"):
        print(f"contact sheet: {result['contact_sheet']}")
    if result.get("render_error"):
        print(f"render error: {result['render_error']}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
