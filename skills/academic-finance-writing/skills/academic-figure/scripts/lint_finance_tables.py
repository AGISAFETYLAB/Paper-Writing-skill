#!/usr/bin/env python3
"""Static lint for finance manuscript LaTeX tables."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, NamedTuple


TEXT_SUFFIXES = {".tex", ".ltx"}
IGNORED_DIRS = {".git", "__pycache__", "layout-qa", "build", "_minted"}
CENTRAL_CONTRAST_RE = re.compile(
    r"\b(high\s+minus\s+low|low\s+minus\s+high|long[-\s]+short|long\s+minus\s+short|"
    r"treated\s+minus\s+control|treatment\s+minus\s+control|difference|diff\.)\b",
    re.I,
)


class TableLintFinding(NamedTuple):
    path: Path
    line: int
    code: str
    message: str


def iter_latex_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in TEXT_SUFFIXES:
            yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def contains_vertical_rule(column_spec: str) -> bool:
    return "|" in column_spec


def tabularx_without_x(column_spec: str) -> bool:
    return "X" not in column_spec


def clean_cell(cell: str) -> str:
    cell = re.sub(r"\\(?:textbf|emph|textit)\{([^{}]*)\}", r"\1", cell)
    cell = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", "", cell)
    cell = cell.replace("\\", "").strip()
    return cell


def row_has_missing_central_uncertainty(row: str) -> bool:
    if "&" not in row or not row.rstrip().endswith(r"\\"):
        return False
    cells = [clean_cell(part) for part in row.rstrip().rstrip("\\").split("&")]
    if len(cells) < 4:
        return False
    label = cells[0]
    if not CENTRAL_CONTRAST_RE.search(label):
        return False
    numeric_cells = cells[1:]
    blank_count = sum(1 for cell in numeric_cells if not cell)
    nonblank_count = sum(1 for cell in numeric_cells if cell)
    return nonblank_count >= 1 and blank_count >= 2


def lint_text(path: Path, text: str) -> list[TableLintFinding]:
    findings: list[TableLintFinding] = []

    for match in re.finditer(r"\\begin\{tabular\*?\}(?:\{[^{}]*\})?\{(?P<spec>[^{}]*)\}", text):
        spec = match.group("spec")
        if contains_vertical_rule(spec):
            findings.append(
                TableLintFinding(
                    path,
                    line_number(text, match.start()),
                    "vertical_rules",
                    "booktabs-style finance tables should not use vertical column rules",
                )
            )

    for match in re.finditer(r"\\begin\{tabularx\}\{[^{}]*(?:\\textwidth|\\linewidth)[^{}]*\}\{(?P<spec>[^{}]*)\}", text):
        spec = match.group("spec")
        if contains_vertical_rule(spec):
            findings.append(
                TableLintFinding(
                    path,
                    line_number(text, match.start()),
                    "vertical_rules",
                    "booktabs-style finance tables should not use vertical column rules",
                )
            )
        if tabularx_without_x(spec):
            findings.append(
                TableLintFinding(
                    path,
                    line_number(text, match.start()),
                    "tabularx_without_x_column",
                    "declared-width tabularx tables need a real X or bounded prose column",
                )
            )

    for match in re.finditer(r"\\hline\b", text):
        findings.append(
            TableLintFinding(
                path,
                line_number(text, match.start()),
                "hline_used",
                "use booktabs rules such as \\toprule, \\midrule, and \\bottomrule instead of \\hline",
            )
        )

    for match in re.finditer(r"\\resizebox\{(?:\\textwidth|\\linewidth|[^{}]+)\}", text):
        findings.append(
            TableLintFinding(
                path,
                line_number(text, match.start()),
                "resizebox_used",
                "\\resizebox is allowed only after semantic table layout is correct; review manually",
            )
        )

    for match in re.finditer(r"(?<![\w.])-?\.\d+", text):
        findings.append(
            TableLintFinding(
                path,
                line_number(text, match.start()),
                "leading_decimal_without_zero",
                "numbers below one should include a leading zero, for example 0.10",
            )
        )

    for table_match in re.finditer(r"\\begin\{table\*?\}.*?\\end\{table\*?\}", text, flags=re.DOTALL):
        table_text = table_match.group(0)
        if "\\caption" not in table_text:
            findings.append(
                TableLintFinding(
                    path,
                    line_number(text, table_match.start()),
                    "missing_caption",
                    "finance tables need a title/caption plus descriptive legend or notes",
                )
            )
        if "\\toprule" in table_text and "\\bottomrule" not in table_text:
            findings.append(
                TableLintFinding(
                    path,
                    line_number(text, table_match.start()),
                    "incomplete_booktabs_rules",
                    "booktabs tables with \\toprule should also close with \\bottomrule",
                )
            )

    for match in re.finditer(r"^.*&.*\\\\\s*$", text, flags=re.MULTILINE):
        row = match.group(0)
        if row_has_missing_central_uncertainty(row):
            findings.append(
                TableLintFinding(
                    path,
                    line_number(text, match.start()),
                    "central_contrast_missing_uncertainty",
                    "central contrast rows need uncertainty (SE, CI, p-value, or t-stat) or must be demoted from headline inference",
                )
            )

    return findings


def find_table_lint_findings(root: Path | str) -> list[TableLintFinding]:
    root_path = Path(root)
    findings: list[TableLintFinding] = []
    for path in iter_latex_files(root_path):
        text = path.read_text(encoding="utf-8", errors="replace")
        findings.extend(lint_text(path, text))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint finance LaTeX tables for source-level defects.")
    parser.add_argument("path", type=Path, help="LaTeX file or paper directory")
    args = parser.parse_args()

    findings = find_table_lint_findings(args.path)
    if findings:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.code}: {finding.message}")
        print(f"FAIL finance table static lint: {len(findings)} finding(s)")
        return 1
    print("PASS finance table static lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
