#!/usr/bin/env python3
"""Audit JAMA/JAMA Network Open manuscript components in Markdown."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
BOLD_LABEL_RE = re.compile(r"\*\*([^*]+?)\*\*")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
FORBIDDEN_FINDINGS_STATS_RE = re.compile(
    r"\b(OR|odds ratio|aOR|RR|HR|CI|confidence interval|P\s*[<=>]|p\s*[<=>]|95%)\b",
    re.IGNORECASE,
)
YEAR_OR_DATE_RE = re.compile(r"\b(19|20)\d{2}\b|\b(date|dates|years|period|from|through|follow-up|follow up)\b", re.IGNORECASE)
REAL_EVIDENCE_GAP_RE = re.compile(
    r"\b(no real|not real|not a real|not supplied|unknown|none|workflow-validation fixture|generated fixture)\b",
    re.IGNORECASE,
)
NONTRIAL_TITLE_STUDY_DESIGN_RE = re.compile(
    r"\b(cohort|case-control|cross-sectional|observational|survey|quality improvement|diagnostic|prognostic)\s+study\b",
    re.IGNORECASE,
)
FIXTURE_ADJUSTED_MAIN_DISPLAY_RE = re.compile(
    r"\b(fixture-derived|deterministic transform|not a real fitted model)\b(?=[\s\S]{0,120}\badjusted\b)|"
    r"\badjusted\b(?=[\s\S]{0,120}\b(fixture-derived|deterministic transform|not a real fitted model)\b)",
    re.IGNORECASE,
)


def section_ranges(text: str) -> dict[str, tuple[int, int]]:
    matches = list(HEADING_RE.finditer(text))
    ranges: dict[str, tuple[int, int]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        ranges[match.group(1).strip()] = (start, end)
    return ranges


def section_text(text: str, heading: str) -> str:
    ranges = section_ranges(text)
    if heading not in ranges:
        return ""
    start, end = ranges[heading]
    return text[start:end].strip()


def clean_words(block: str) -> list[str]:
    block = re.sub(r"<sup>.*?</sup>", " ", block)
    block = re.sub(r"\*\*([^*]+?)\*\*", r"\1", block)
    return WORD_RE.findall(block)


def bold_label_blocks(block: str) -> dict[str, str]:
    matches = list(BOLD_LABEL_RE.finditer(block))
    labels: dict[str, str] = {}
    for index, match in enumerate(matches):
        label = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        labels[label] = block[start:end].strip()
    return labels


def markdown_table_after(block: str, marker: str) -> tuple[list[str], str]:
    marker_index = block.find(marker)
    if marker_index == -1:
        return [], ""
    tail = block[marker_index + len(marker) :]
    lines = tail.splitlines()
    table_lines: list[str] = []
    note_lines: list[str] = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        if in_table:
            if not stripped:
                continue
            if stripped.startswith("**Table "):
                break
            note_lines.append(stripped)
    return table_lines, "\n".join(note_lines)


def table_header_cells(table_lines: list[str]) -> list[str]:
    if not table_lines:
        return []
    return [cell.strip() for cell in table_lines[0].strip("|").split("|")]


def audit_jama_components(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    reasons: list[str] = []
    warnings: list[str] = []
    metrics: dict = {}

    title_match = TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else ""
    metrics["title"] = title
    if title and NONTRIAL_TITLE_STUDY_DESIGN_RE.search(title):
        reasons.append(
            "JAMA-style reports other than clinical trials and meta-analyses: do not include study type or design in the title"
        )

    key_points = section_text(text, "Key Points")
    kp_labels = bold_label_blocks(key_points)
    kp_words = clean_words(key_points)
    metrics["key_points_word_count"] = len(kp_words)
    metrics["key_points_labels"] = list(kp_labels)
    if list(kp_labels) != ["Question", "Findings", "Meaning"]:
        reasons.append("Key Points must contain exactly Question, Findings, and Meaning in order")
    if not (75 <= len(kp_words) <= 100):
        reasons.append("Key Points word count outside JAMA-style 75-100 word window")
    findings = kp_labels.get("Findings", "")
    forbidden_findings_statistics = bool(FORBIDDEN_FINDINGS_STATS_RE.search(findings))
    metrics["forbidden_findings_statistics"] = forbidden_findings_statistics
    if forbidden_findings_statistics:
        reasons.append("Findings contains statistical-detail overload; emphasize primary outcome without OR, CI, p value, or long caveats")

    abstract = section_text(text, "Abstract")
    abstract_labels = bold_label_blocks(abstract)
    metrics["abstract_labels"] = list(abstract_labels)
    required_labels = [
        "Importance",
        "Objective",
        "Design",
        "Setting",
        "Participants",
        "Main Outcomes and Measures",
        "Results",
        "Conclusions and Relevance",
    ]
    if "Design, Setting, and Participants" in abstract_labels:
        reasons.append("Original data abstract combines Design, Setting, and Participants; use separate headings")
    for label in required_labels:
        if label not in abstract_labels:
            reasons.append(f"Abstract missing JAMA original data heading: {label}")
    design_text = abstract_labels.get("Design", "")
    setting_text = abstract_labels.get("Setting", "")
    participants_text = abstract_labels.get("Participants", "")
    if design_text and not YEAR_OR_DATE_RE.search(design_text):
        reasons.append("Design heading lacks study years/source dates or follow-up window")
    if setting_text and REAL_EVIDENCE_GAP_RE.search(setting_text):
        reasons.append("Setting heading lacks real clinical/data environment evidence")
    if participants_text and REAL_EVIDENCE_GAP_RE.search(participants_text):
        reasons.append("Participants heading lacks real participant-source evidence")

    tables = section_text(text, "Tables")
    figure_legends = section_text(text, "Figure Legends")
    if FIXTURE_ADJUSTED_MAIN_DISPLAY_RE.search(tables + "\n" + figure_legends):
        reasons.append(
            "fixture-derived adjusted estimate appears in a main display; move it to the supplement or remove it from the main claim/display set"
        )
    table1, table1_notes = markdown_table_after(tables, "**Table 1")
    table2, table2_notes = markdown_table_after(tables, "**Table 2")
    table1_header = table_header_cells(table1)
    table2_header = table_header_cells(table2)
    metrics["table1_header"] = table1_header
    metrics["table2_header"] = table2_header

    table1_header_text = " | ".join(table1_header).lower()
    table1_notes_lower = table1_notes.lower()
    if "overall" not in table1_header_text:
        reasons.append("Table 1 missing overall column")
    if "missing" not in table1_header_text and "missing" not in table1_notes_lower:
        reasons.append("Table 1 missing values column or missingness footnote/eTable linkage")
    if "standardized difference" not in table1_notes_lower and "standardized differences" not in table1_notes_lower:
        reasons.append("Table 1 missing standardized difference definition")
    if not re.search(r"\b(range|score|scale|unit|units|years|y\b|no\./total|%|iqr|sd)\b", table1_notes_lower + " " + table1_header_text):
        warnings.append("Table 1 variable units/ranges are not clearly documented")

    table2_text = "\n".join(table2).lower()
    table2_header_text = " | ".join(table2_header).lower()
    table2_notes_lower = table2_notes.lower()
    if not re.search(r"\b(primary|secondary|role|prespecified)\b", table2_text + " " + table2_notes_lower):
        reasons.append("Table 2 missing prespecified primary/secondary outcome role labels")
    if "risk difference" not in table2_header_text or "95% ci" not in table2_header_text:
        if not re.search(r"risk difference 95% ci.*(needs source|not supplied|not available)", table2_notes_lower):
            reasons.append("Table 2 missing risk difference 95% CI or explicit needs source note")
    if "crude or" not in table2_header_text or "95% ci" not in table2_header_text:
        if not re.search(r"crude or.*95% ci.*(needs source|not supplied|not available)", table2_notes_lower):
            reasons.append("Table 2 missing crude OR with 95% CI or explicit needs source note")

    return {
        "path": str(path),
        "status": "PASS" if not reasons else "BLOCKED",
        "reasons": reasons,
        "warnings": warnings,
        "metrics": metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = audit_jama_components(args.markdown)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"JAMA component audit: {report['status']}")
        print(json.dumps(report["metrics"], indent=2, sort_keys=True))
        if report["reasons"]:
            print("Reasons:")
            for reason in report["reasons"]:
                print(f"- {reason}")
        if report["warnings"]:
            print("Warnings:")
            for warning in report["warnings"]:
                print(f"- {warning}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
