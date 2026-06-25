#!/usr/bin/env python3
"""Static finance citation audit.

This script checks local citation and BibTeX integrity. It does not prove that a
source supports a claim; that requires live lookup and the Citation Evidence
Ledger required by the finance citation workflow.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CITE_RE = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I)
FIELD_RE = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[{'\"]")
MARKER_RE = re.compile(r"%\s*(CITATION_NEEDED|EVIDENCE_NEEDED)\b|unsupported_until_verified|not verified", re.I)
PLACEHOLDER_AUTHOR_RE = re.compile(r"\band\s+others\b|\bet\s+al\.?\b|\\textit\{?missing\}?|unknown author", re.I)
DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.I)
URL_RE = re.compile(r"https?://|www\.", re.I)
ARXIV_RE = re.compile(r"\b\d{4}\.\d{4,5}(?:v\d+)?\b|[a-z-]+/\d{7}(?:v\d+)?", re.I)
LEDGER_HEADERS = (
    "claim id",
    "claim text / clause",
    "citation key",
    "source identity",
    "metadata_source",
    "support_grade",
    "evidence basis",
    "version/data-software status",
    "action",
)


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        escaped = False
        cut = len(line)
        for i, char in enumerate(line):
            if char == "\\":
                escaped = not escaped
                continue
            if char == "%" and not escaped:
                cut = i
                break
            escaped = False
        lines.append(line[:cut])
    return "\n".join(lines)


def find_matching_brace(text: str, open_index: int) -> int:
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def parse_bib_entries(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    entries: dict[str, dict[str, str]] = {}
    for match in ENTRY_RE.finditer(text):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        open_index = text.find("{", match.start())
        close_index = find_matching_brace(text, open_index)
        if close_index < 0:
            entries[key] = {"entry_type": entry_type, "_parse_error": "unclosed entry"}
            continue
        body = text[match.end() : close_index]
        fields = {"entry_type": entry_type}
        for field_match in FIELD_RE.finditer(body):
            name = field_match.group(1).lower()
            value_start = field_match.end()
            opener = body[value_start - 1]
            if opener == "{":
                value_end = find_matching_brace(body, value_start - 1)
                fields[name] = " ".join(body[value_start:value_end].split()) if value_end >= 0 else body[value_start:].strip()
            else:
                next_comma = body.find(",", value_start)
                if next_comma < 0:
                    next_comma = len(body)
                fields[name] = body[value_start:next_comma].strip().strip("'\"")
        entries[key] = fields
    return entries


def extract_cites(tex_files: list[Path]) -> tuple[list[str], list[tuple[Path, int, str]]]:
    keys: list[str] = []
    markers: list[tuple[Path, int, str]] = []
    for path in tex_files:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(raw.splitlines(), 1):
            if MARKER_RE.search(line):
                markers.append((path, lineno, line.strip()))
        text = strip_comments(raw)
        for match in CITE_RE.finditer(text):
            keys.extend(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys, markers


def has_stable_locator(fields: dict[str, str]) -> bool:
    for name in ("doi", "url", "eprint", "howpublished", "note"):
        value = fields.get(name, "")
        if DOI_RE.search(value) or URL_RE.search(value) or ARXIV_RE.search(value):
            return True
        if any(token in value.lower() for token in ("ssrn", "nber", "cepr", "repec", "edgar", "fred", "crsp", "compustat")):
            return True
    return False


def year_value(fields: dict[str, str]) -> int | None:
    match = re.search(r"(?:19|20)\d{2}", fields.get("year", ""))
    return int(match.group(0)) if match else None


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip().strip("`").lower() for cell in line.strip().strip("|").split("|")]


def audit_ledger(paper_dir: Path, require_ledger: bool, errors: list[str]) -> None:
    ledger = paper_dir / "citation-evidence.md"
    if not ledger.exists():
        if require_ledger:
            errors.append("missing Citation Evidence Ledger: paper/citation-evidence.md")
        return

    header: list[str] | None = None
    for line in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        header = split_markdown_row(stripped)
        break
    if header is None:
        errors.append("Citation Evidence Ledger has no markdown table header")
        return
    missing = [name for name in LEDGER_HEADERS if name not in header]
    if missing:
        errors.append(f"Citation Evidence Ledger missing column(s): {', '.join(missing)}")


def audit(paper_dir: Path, min_citations: int, require_ledger: bool) -> list[str]:
    errors: list[str] = []
    tex_files = sorted(paper_dir.rglob("*.tex"))
    if not tex_files:
        errors.append(f"no .tex files found under {paper_dir}")
        return errors

    bib_path = paper_dir / "references.bib"
    if not bib_path.exists():
        errors.append(f"missing bibliography file: {bib_path}")
        return errors

    cite_keys, markers = extract_cites(tex_files)
    unique_cites = sorted(set(cite_keys))
    entries = parse_bib_entries(bib_path)

    if len(unique_cites) < min_citations:
        errors.append(f"citation count {len(unique_cites)} below required floor {min_citations}")

    for path, lineno, marker in markers:
        errors.append(f"unresolved citation marker: {path}:{lineno}: {marker}")

    missing_entries = sorted(set(unique_cites) - set(entries))
    for key in missing_entries:
        errors.append(f"cited key missing from references.bib: {key}")

    uncited_entries = sorted(set(entries) - set(unique_cites))
    for key in uncited_entries:
        errors.append(f"uncited BibTeX entry: {key}")

    for key in unique_cites:
        fields = entries.get(key)
        if not fields:
            continue
        if fields.get("_parse_error"):
            errors.append(f"{key}: malformed BibTeX entry: {fields['_parse_error']}")
        for required in ("author", "title", "year"):
            if not fields.get(required, "").strip():
                errors.append(f"{key}: missing required field `{required}`")
        if PLACEHOLDER_AUTHOR_RE.search(fields.get("author", "")):
            errors.append(f"{key}: placeholder author list is not allowed")
        year = year_value(fields)
        if year is not None and year >= 2000 and not has_stable_locator(fields):
            errors.append(f"{key}: modern cited source lacks DOI/URL/arXiv/working-paper/data locator")

    audit_ledger(paper_dir, require_ledger, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Static finance citation audit")
    parser.add_argument("paper_dir", type=Path)
    parser.add_argument("--min-citations", type=int, default=0)
    parser.add_argument("--require-ledger", action="store_true")
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    errors = audit(paper_dir, args.min_citations, args.require_ledger)
    if errors:
        print("FAIL finance citation audit")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS finance citation audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
