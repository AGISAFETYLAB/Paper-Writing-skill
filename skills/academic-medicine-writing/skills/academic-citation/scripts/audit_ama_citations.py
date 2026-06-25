#!/usr/bin/env python3
"""Audit AMA/JAMA numeric citation order and reference-list formatting."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


BRACKET_CITE_RE = re.compile(r"\[(\d+(?:\s*(?:,|-)\s*\d+)*)\]")
SUP_CITE_RE = re.compile(r"<sup>(\d+(?:\s*(?:,|-)\s*\d+)*)</sup>")
REFERENCE_RE = re.compile(r"^(\d+)\.\s+(.*)$")
ORDERED_TAIL_SECTIONS = ("References", "Figure Legends", "Tables")


def public_artifact_path(path: Path) -> str:
    parts = path.parts
    if "paper" in parts:
        return "/".join(parts[parts.index("paper") :])
    return f"paper/{path.name}"


def split_reference_section(markdown: str) -> tuple[str, str]:
    marker = "\n## References"
    index = markdown.find(marker)
    if index == -1:
        return markdown, ""
    return markdown[:index], markdown[index:]


def expand_numbers(cite: str) -> list[int]:
    numbers: list[int] = []
    for part in re.split(r"\s*,\s*", cite.strip()):
        if "-" in part:
            start, end = [int(value) for value in re.split(r"\s*-\s*", part, maxsplit=1)]
            step = 1 if end >= start else -1
            numbers.extend(range(start, end + step, step))
        elif part:
            numbers.append(int(part))
    return numbers


def parse_references(reference_section: str) -> dict[int, str]:
    refs: dict[int, str] = {}
    for line in reference_section.splitlines():
        match = REFERENCE_RE.match(line.strip())
        if match:
            refs[int(match.group(1))] = match.group(2).strip()
    return refs


def section_order(markdown: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE)]


def component_order_issues(markdown: str) -> list[str]:
    order = section_order(markdown)
    positions = {heading: index for index, heading in enumerate(order)}
    issues: list[str] = []
    if "References" in positions:
        for section in ("Figure Legends", "Tables"):
            if section in positions and positions["References"] > positions[section]:
                issues.append(f"References section appears after {section}; JAMA-style manuscript components should place References before end-matter legends/tables")
    if "Tables" in positions and positions["Tables"] != max(positions.values()):
        issues.append("Tables section is not the final manuscript component")
    return issues


def author_count_issue(reference_text: str) -> str | None:
    first_period = reference_text.find(". ")
    if first_period == -1:
        return "reference missing period after author/source field"
    authors = reference_text[:first_period]
    if "Committee" in authors or "Network" in authors or "Guidelines" in authors:
        return None
    if ", et al" in authors:
        listed = [part.strip() for part in authors.split(", et al", 1)[0].split(",") if part.strip()]
        if len(listed) > 3:
            return "AMA style requires first 3 authors followed by et al when there are more than 6 authors"
        return None
    listed = [part.strip() for part in authors.split(",") if part.strip()]
    if len(listed) > 6:
        return "AMA style lists all authors up to 6; if more than 6, list first 3 followed by et al"
    return None


def audit_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    body, references = split_reference_section(text)
    refs = parse_references(references)
    bracket_cites = BRACKET_CITE_RE.findall(body)
    sup_cites = SUP_CITE_RE.findall(body)
    cited_numbers: list[int] = []
    first_seen: list[int] = []
    seen = set()
    for cite in sup_cites:
        for number in expand_numbers(cite):
            cited_numbers.append(number)
            if number not in seen:
                seen.add(number)
                first_seen.append(number)

    reasons: list[str] = []
    if bracket_cites:
        reasons.append("numeric citations use square brackets instead of AMA superscript")
    if not sup_cites:
        reasons.append("no AMA superscript numeric citations found before References")
    expected_order = list(range(1, len(first_seen) + 1))
    if first_seen and first_seen != expected_order:
        reasons.append("reference numbers do not appear in first-citation order")
    if refs:
        expected_refs = list(range(1, len(refs) + 1))
        if sorted(refs) != expected_refs:
            reasons.append("reference list numbers are not consecutive from 1")
    if cited_numbers and refs:
        missing = sorted(set(cited_numbers) - set(refs))
        orphaned = sorted(set(refs) - set(cited_numbers))
        if missing:
            reasons.append(f"cited reference numbers missing from list: {missing}")
        if orphaned:
            reasons.append(f"reference list contains uncited numbers: {orphaned}")
    for number, reference_text in refs.items():
        issue = author_count_issue(reference_text)
        if issue:
            reasons.append(f"reference {number}: {issue}")
    reasons.extend(component_order_issues(text))

    return {
        "path": public_artifact_path(path),
        "status": "PASS" if not reasons else "BLOCKED",
        "reasons": reasons,
        "metrics": {
            "bracket_numeric_citations": len(bracket_cites),
            "superscript_numeric_citations": len(sup_cites),
            "first_seen_reference_numbers": first_seen,
            "reference_count": len(refs),
            "cited_reference_count": len(set(cited_numbers)),
            "section_order": section_order(text),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = audit_markdown(args.markdown)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"AMA citation audit: {report['status']}")
        print(json.dumps(report["metrics"], indent=2, sort_keys=True))
        if report["reasons"]:
            print("Reasons:")
            for reason in report["reasons"]:
                print(f"- {reason}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
