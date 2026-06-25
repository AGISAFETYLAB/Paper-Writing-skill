#!/usr/bin/env python3
"""Static lint for finance manuscript prose."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, NamedTuple


TEXT_SUFFIXES = {".tex", ".md", ".txt"}
IGNORED_DIRS = {".git", "__pycache__", "build", "_minted", "layout-qa"}

BANNED_AI_RE = re.compile(
    r"\b("
    r"delve|landscape|multifaceted|pivotal|groundbreaking|shed light on|pave the way|"
    r"it is worth noting|it should be noted"
    r")\b",
    re.IGNORECASE,
)
EMPTY_CONTRIBUTION_RE = re.compile(
    r"\b(contributes? to the literature by|fills? (?:an? )?gap|adds? to the literature|"
    r"provides? new insights?)\b",
    re.IGNORECASE,
)
CAUSAL_RE = re.compile(
    r"\b(causes?|causal effect|effect of|impact of|impacts?|leads? to|drives?|"
    r"reduces?|increases?)\b",
    re.IGNORECASE,
)
IDENTIFICATION_CUE_RE = re.compile(
    r"\b(identification|instrument|random|experiment|difference-in-differences|diff-in-diff|"
    r"\bDiD\b|regression discontinuity|RD\b|event study|fixed effects|parallel trends|"
    r"placebo|synthetic control|matched|exogenous|shock)\b",
    re.IGNORECASE,
)
SIGNIFICANCE_RE = re.compile(r"\b(significant|statistically significant|robust)\b", re.IGNORECASE)
MAGNITUDE_CUE_RE = re.compile(
    r"(%|percentage point|percentage-point|basis point|bps|\$|dollar|standard deviation|"
    r"\bSD\b|elasticity|Sharpe|alpha|mean|median|relative to|compared with)",
    re.IGNORECASE,
)
TABLE_TOUR_RE = re.compile(
    r"^\s*(Table|Figure)\s+\d+[A-Za-z]?\s+(reports?|presents?|shows?|provides?)\b",
    re.IGNORECASE,
)


class ProseLintFinding(NamedTuple):
    path: Path
    line: int
    code: str
    message: str


def iter_text_files(root: Path) -> Iterable[Path]:
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


def strip_latex_commands(line: str) -> str:
    line = re.sub(r"%.*$", "", line)
    line = re.sub(r"\\(?:cite|citet|citep|ref|label|input|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}", " ", line)
    line = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", line)
    return line


def lint_line(path: Path, line_number: int, line: str) -> list[ProseLintFinding]:
    findings: list[ProseLintFinding] = []
    text = strip_latex_commands(line).strip()
    if not text:
        return findings

    if BANNED_AI_RE.search(text):
        findings.append(
            ProseLintFinding(
                path,
                line_number,
                "banned_ai_phrase",
                "replace generic AI-sounding prose with a concrete finance claim",
            )
        )
    if EMPTY_CONTRIBUTION_RE.search(text):
        findings.append(
            ProseLintFinding(
                path,
                line_number,
                "empty_contribution_phrase",
                "state the actual belief update instead of a generic contribution phrase",
            )
        )
    if CAUSAL_RE.search(text) and not IDENTIFICATION_CUE_RE.search(text):
        findings.append(
            ProseLintFinding(
                path,
                line_number,
                "causal_language_without_identification_cue",
                "causal language needs an identification, design, or benchmark cue",
            )
        )
    if SIGNIFICANCE_RE.search(text) and not MAGNITUDE_CUE_RE.search(text):
        findings.append(
            ProseLintFinding(
                path,
                line_number,
                "significance_without_magnitude_cue",
                "statistical significance should be paired with an economic magnitude cue",
            )
        )
    if TABLE_TOUR_RE.search(text):
        findings.append(
            ProseLintFinding(
                path,
                line_number,
                "table_tour_sentence",
                "start the paragraph with the economic result, then cite the table or figure",
            )
        )
    return findings


def lint_text(path: Path, text: str) -> list[ProseLintFinding]:
    findings: list[ProseLintFinding] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        findings.extend(lint_line(path, line_number, line))
    return findings


def find_finance_prose_findings(root: Path | str) -> list[ProseLintFinding]:
    root_path = Path(root)
    findings: list[ProseLintFinding] = []
    for path in iter_text_files(root_path):
        text = path.read_text(encoding="utf-8", errors="replace")
        findings.extend(lint_text(path, text))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint finance manuscript prose for static writing defects.")
    parser.add_argument("path", type=Path, help="Text file or paper directory")
    args = parser.parse_args()

    findings = find_finance_prose_findings(args.path)
    if findings:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.code}: {finding.message}")
        print(f"FAIL finance prose lint: {len(findings)} finding(s)")
        return 1
    print("PASS finance prose lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
