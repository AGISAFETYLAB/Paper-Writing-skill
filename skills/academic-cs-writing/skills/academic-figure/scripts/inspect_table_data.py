#!/usr/bin/env python3
"""Inspect tabular data before designing a paper table.

The script reports machine-checkable facts only: shape, numeric columns, precision, long headers,
missing metric-direction markers, and width risks. It does not decide paper claims or rewrite data.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


NUMERIC_RE = re.compile(r"^[+-]?(?:\d+(?:,\d{3})*|\d*)(?:\.\d+)?%?$")
DIRECTION_RE = re.compile(r"(↑|↓|\\uparrow|\\downarrow|higher|lower|better|worse)", re.I)
COUNT_HEADER_RE = re.compile(r"^(n|#|count|counts|total|train|dev|test|items|examples|samples|size|id)$", re.I)


def clean_cell(cell: str) -> str:
    return " ".join(cell.strip().replace("<br>", " ").split())


def is_numeric(value: str) -> bool:
    value = clean_cell(value).replace(",", "")
    if not value or value in {"-", "–", "—"}:
        return False
    return bool(NUMERIC_RE.match(value))


def decimal_places(value: str) -> int | None:
    value = clean_cell(value).replace(",", "").rstrip("%")
    if not is_numeric(value):
        return None
    if "." not in value:
        return 0
    return len(value.split(".", 1)[1])


def parse_markdown_table(text: str) -> tuple[list[str], list[list[str]]]:
    rows: list[list[str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "|" not in line[1:]:
            continue
        cells = [clean_cell(part) for part in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return [], []
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    return rows[0], rows[1:]


def parse_csv_table(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = [[clean_cell(c) for c in row] for row in reader if any(c.strip() for c in row)]
    if not rows:
        return [], []
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    return rows[0], rows[1:]


def load_table(path: Path) -> tuple[str, list[str], list[list[str]]]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        if suffix == ".tsv":
            text = path.read_text(encoding="utf-8")
            rows = list(csv.reader(text.splitlines(), delimiter="\t"))
            rows = [[clean_cell(c) for c in row] for row in rows if any(c.strip() for c in row)]
            if not rows:
                return "tsv", [], []
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            return "tsv", rows[0], rows[1:]
        headers, rows = parse_csv_table(path)
        return "csv", headers, rows
    text = path.read_text(encoding="utf-8")
    headers, rows = parse_markdown_table(text)
    return "markdown", headers, rows


def column_values(rows: list[list[str]], index: int) -> list[str]:
    return [row[index] for row in rows if index < len(row) and clean_cell(row[index])]


def detect_numeric_columns(headers: list[str], rows: list[list[str]]) -> list[str]:
    numeric: list[str] = []
    for idx, header in enumerate(headers):
        vals = column_values(rows, idx)
        if vals and sum(1 for v in vals if is_numeric(v)) >= max(1, int(0.8 * len(vals))):
            numeric.append(header)
    return numeric


def precision_by_column(headers: list[str], rows: list[list[str]], numeric_columns: list[str]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for idx, header in enumerate(headers):
        if header not in numeric_columns:
            continue
        places = sorted({p for v in column_values(rows, idx) if (p := decimal_places(v)) is not None})
        result[header] = places
    return result


def unknown_direction_columns(headers: list[str], numeric_columns: list[str]) -> list[str]:
    unknown: list[str] = []
    for header in numeric_columns:
        stripped = header.strip()
        if DIRECTION_RE.search(stripped) or COUNT_HEADER_RE.search(stripped):
            continue
        unknown.append(header)
    return unknown


def suggest_table_kinds(headers: list[str], rows: list[list[str]], numeric_columns: list[str]) -> list[str]:
    lowered = [h.lower() for h in headers]
    first = lowered[0] if lowered else ""
    early_semantic_columns = set(lowered[:2])
    suggestions: list[str] = []

    if {"phase", "setting", "value"}.issubset(set(lowered)):
        suggestions.append("training configuration table")
    if {"train", "dev", "test"}.issubset(set(lowered)) or {"train", "validation", "test"}.issubset(set(lowered)):
        suggestions.append("data split table")
    if first in {"variant", "ablation", "component", "components"}:
        suggestions.append("ablation table")
    if first in {"lambda", "λ", "threshold", "k", "temperature"}:
        suggestions.append("hyperparameter sensitivity table")
    if first in {"code", "task", "dataset"} and any(h in lowered for h in {"metric", "items", "description"}):
        suggestions.append("benchmark summary table")
    if early_semantic_columns & {"model", "method", "system"} and len(numeric_columns) >= 5:
        suggestions.append("main result table")
        suggestions.append("multi-metric comparison table")
    elif early_semantic_columns & {"model", "method", "system"} and len(numeric_columns) >= 2:
        suggestions.append("multi-dataset comparison table")

    if not suggestions:
        suggestions.append("table type needs author decision")
    return suggestions


def inspect_table(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    fmt, headers, rows = load_table(source)
    n_columns = len(headers)
    numeric_columns = detect_numeric_columns(headers, rows)
    long_header_columns = [h for h in headers if len(h) > 14]
    prose_cell_count = sum(1 for row in rows for cell in row if len(clean_cell(cell)) > 45)
    width_risks: list[str] = []
    if n_columns >= 7:
        width_risks.append("many_columns")
    if long_header_columns:
        width_risks.append("long_headers")
    if prose_cell_count:
        width_risks.append("prose_cells")
    unknown = unknown_direction_columns(headers, numeric_columns)
    if unknown:
        width_risks.append("metric_direction_unknown")

    return {
        "source": str(source),
        "format": fmt,
        "n_rows": len(rows),
        "n_columns": n_columns,
        "columns": headers,
        "numeric_columns": numeric_columns,
        "precision_by_column": precision_by_column(headers, rows, numeric_columns),
        "long_header_columns": long_header_columns,
        "metric_direction_unknown_columns": unknown,
        "wide_table_risk": bool(n_columns >= 7 or long_header_columns or prose_cell_count),
        "width_risks": width_risks,
        "suggested_table_kinds": suggest_table_kinds(headers, rows, numeric_columns),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a markdown/csv/tsv table and emit JSON.")
    parser.add_argument("source", help="Path to a markdown, csv, or tsv table")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()
    report = inspect_table(args.source)
    print(json.dumps(report, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
