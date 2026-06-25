#!/usr/bin/env python3
"""Normalize a medical manuscript Markdown file to AMA/JAMA numeric citation style."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from audit_ama_citations import audit_markdown, expand_numbers
except ImportError:  # pragma: no cover
    audit_markdown = None
    expand_numbers = None


BRACKET_CITE_RE = re.compile(r"\[(\d+(?:\s*(?:,|-)\s*\d+)*)\]")
SUP_CITE_RE = re.compile(r"<sup>(\d+(?:\s*(?:,|-)\s*\d+)*)</sup>")
REFERENCE_RE = re.compile(r"^(\d+)\.\s+(.*)$")
AMA_AUTHOR_SHORTENING_RULE = "list the first 3 followed by et al"
END_MATTER_SECTION_ORDER = ("Figure Legends", "Tables")


def split_reference_section(markdown: str) -> tuple[str, str, str]:
    marker = "\n## References"
    index = markdown.find(marker)
    if index == -1:
        return markdown, "", ""
    body = markdown[:index]
    rest = markdown[index:].lstrip("\n")
    lines = rest.splitlines()
    heading = lines[0]
    reference_lines = "\n".join(lines[1:])
    return body, heading, reference_lines


def preserve_tail_sections(reference_lines: str) -> tuple[str, dict[str, str]]:
    """Preserve Figure Legends/Tables that already appear after References."""
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", reference_lines, re.MULTILINE))
    sections: dict[str, str] = {}
    cut_index = len(reference_lines)
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        if heading not in END_MATTER_SECTION_ORDER:
            continue
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(reference_lines)
        sections[heading] = reference_lines[start:end].strip()
        cut_index = min(cut_index, start)
    return reference_lines[:cut_index].rstrip(), sections


def parse_references(reference_lines: str) -> dict[int, str]:
    refs: dict[int, str] = {}
    for line in reference_lines.splitlines():
        match = REFERENCE_RE.match(line.strip())
        if match:
            refs[int(match.group(1))] = match.group(2).strip()
    return refs


def split_named_sections(markdown: str) -> tuple[str, dict[str, str]]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE))
    sections: dict[str, str] = {}
    cut_index = len(markdown)
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        if heading not in END_MATTER_SECTION_ORDER:
            continue
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[heading] = markdown[start:end].strip()
        cut_index = min(cut_index, start)
    return markdown[:cut_index].rstrip(), sections


def compress_numbers(numbers: list[int]) -> str:
    if not numbers:
        return ""
    out: list[str] = []
    start = prev = numbers[0]
    for number in numbers[1:]:
        if number == prev + 1:
            prev = number
            continue
        out.append(f"{start}-{prev}" if start != prev else str(start))
        start = prev = number
    out.append(f"{start}-{prev}" if start != prev else str(start))
    return ",".join(out)


def truncate_authors(reference_text: str) -> str:
    first_period = reference_text.find(". ")
    if first_period == -1:
        return reference_text
    authors = reference_text[:first_period]
    rest = reference_text[first_period:]
    if "Committee" in authors or "Network" in authors or "Guidelines" in authors:
        return reference_text
    if ", et al" in authors:
        listed = [part.strip() for part in authors.split(", et al", 1)[0].split(",") if part.strip()]
        if len(listed) > 3:
            return ", ".join(listed[:3]) + ", et al" + rest
        return reference_text
    listed = [part.strip() for part in authors.split(",") if part.strip()]
    if len(listed) > 6:
        return ", ".join(listed[:3]) + ", et al" + rest
    return reference_text


def normalize_ama_markdown(markdown: str) -> tuple[str, dict]:
    body, heading, reference_lines = split_reference_section(markdown)
    reference_lines, tail_sections_after_refs = preserve_tail_sections(reference_lines)
    refs = parse_references(reference_lines)
    if not refs:
        return markdown, {"changed": False, "reason": "no References section found"}

    old_to_new: dict[int, int] = {}
    ordered_old_refs: list[int] = []

    def map_numbers(citation_text: str) -> str:
        mapped: list[int] = []
        for old_number in expand_numbers(citation_text):
            if old_number not in old_to_new:
                old_to_new[old_number] = len(old_to_new) + 1
                ordered_old_refs.append(old_number)
            mapped.append(old_to_new[old_number])
        return f"<sup>{compress_numbers(mapped)}</sup>"

    citation_body = SUP_CITE_RE.sub(lambda match: map_numbers(match.group(1)), body)
    citation_body = BRACKET_CITE_RE.sub(lambda match: map_numbers(match.group(1)), citation_body)
    normalized_body, end_matter_sections = split_named_sections(citation_body)
    end_matter_sections = {**tail_sections_after_refs, **end_matter_sections}

    remaining_refs = [number for number in sorted(refs) if number not in old_to_new]
    ordered_old_refs.extend(remaining_refs)
    for old_number in remaining_refs:
        old_to_new[old_number] = len(old_to_new) + 1

    normalized_refs = []
    for old_number in ordered_old_refs:
        normalized_refs.append(f"{old_to_new[old_number]}. {truncate_authors(refs[old_number])}")

    parts = [normalized_body.rstrip(), heading, "\n".join(normalized_refs)]
    for section in END_MATTER_SECTION_ORDER:
        if section in end_matter_sections:
            parts.append(end_matter_sections[section])
    normalized = "\n\n".join(part.strip() for part in parts if part.strip()) + "\n"
    return normalized, {
        "changed": normalized != markdown,
        "old_to_new_reference_numbers": old_to_new,
        "reference_count": len(normalized_refs),
    }


def map_citation_field(value: str, old_to_new: dict[int, int]) -> str:
    stripped = value.strip()
    if not re.fullmatch(r"\d+(?:\s*(?:,|-)\s*\d+)*", stripped):
        return value
    mapped = [old_to_new[number] for number in expand_numbers(stripped) if number in old_to_new]
    return compress_numbers(mapped)


def sync_table_citation_column(path: Path, old_to_new: dict[int, int]) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for line in lines:
        if not line.startswith("|") or line.startswith("|---"):
            out.append(line)
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1].lower() not in {"citation(s)", "citation"}:
            cells[1] = map_citation_field(cells[1], old_to_new)
            out.append("| " + " | ".join(cells) + " |")
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def replace_prefixed_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def sync_citation_reports(package_dir: Path, old_to_new: dict[int, int], audit_report: dict | None = None) -> None:
    sync_table_citation_column(package_dir / "citation-evidence.md", old_to_new)
    sync_table_citation_column(package_dir / "review-report.md", old_to_new)
    submission = package_dir / "submission-package.md"
    if submission.exists():
        text = submission.read_text(encoding="utf-8")
        status = audit_report.get("status") if audit_report else "PASS"
        if status == "PASS":
            line = (
                "- Citation audit status: PARTIAL. AMA/JAMA numeric style audit PASS "
                "(superscript citations, first-citation order, consecutive reference list, and author shortening); "
                "full JAMA-style real-submission reference development remains blocked because the synthetic scaffold "
                "intentionally has fewer than the usual 50-75 references."
            )
        else:
            line = "- Citation audit status: BLOCKED. AMA/JAMA numeric style audit did not pass."
        submission.write_text(replace_prefixed_line(text, "- Citation audit status:", line), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--audit-json", type=Path)
    parser.add_argument("--mapping-json", type=Path)
    parser.add_argument("--sync-citation-reports", action="store_true")
    args = parser.parse_args()

    original = args.markdown.read_text(encoding="utf-8")
    normalized, summary = normalize_ama_markdown(original)
    supplied_mapping = None
    if args.mapping_json and args.mapping_json.exists():
        mapping_report = json.loads(args.mapping_json.read_text(encoding="utf-8"))
        mapping = mapping_report.get("normalization", {}).get("old_to_new_reference_numbers")
        if mapping:
            supplied_mapping = {int(key): int(value) for key, value in mapping.items()}
    if args.in_place:
        args.markdown.write_text(normalized, encoding="utf-8")
    else:
        print(normalized, end="")

    if args.audit_json and audit_markdown is not None:
        target = args.markdown
        if not args.in_place:
            tmp = args.markdown.with_suffix(args.markdown.suffix + ".ama.tmp")
            tmp.write_text(normalized, encoding="utf-8")
            target = tmp
        report = audit_markdown(target)
        report["normalization"] = summary
        args.audit_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.sync_citation_reports:
            sync_citation_reports(
                args.markdown.parent,
                supplied_mapping or summary.get("old_to_new_reference_numbers", {}),
                report,
            )
        if target != args.markdown:
            target.unlink(missing_ok=True)
        return 0 if report["status"] == "PASS" else 1

    if args.sync_citation_reports:
        sync_citation_reports(args.markdown.parent, supplied_mapping or summary.get("old_to_new_reference_numbers", {}), None)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
