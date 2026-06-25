#!/usr/bin/env python3
"""Convert RIS or PubMed NBIB citation exports into simple BibTeX."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def _append_field(record: dict[str, list[str]], key: str, value: str) -> None:
    value = value.strip()
    if value:
        record.setdefault(key, []).append(value)


def parse_ris(text: str) -> list[dict[str, list[str]]]:
    """Parse a small, dependency-free subset of RIS."""

    records: list[dict[str, list[str]]] = []
    current: dict[str, list[str]] = {}
    last_key: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        match = re.match(r"^([A-Z0-9]{2})\s+-\s?(.*)$", raw_line)
        if match:
            key, value = match.groups()
            if key == "TY" and current:
                records.append(current)
                current = {}
            if key == "ER":
                if current:
                    records.append(current)
                    current = {}
                last_key = None
                continue
            _append_field(current, key, value)
            last_key = key
        elif last_key and current:
            current[last_key][-1] = f"{current[last_key][-1]} {raw_line.strip()}"
    if current:
        records.append(current)
    return [_normalize_ris(record) for record in records]


def parse_nbib(text: str) -> list[dict[str, list[str]]]:
    """Parse PubMed NBIB text exports."""

    records: list[dict[str, list[str]]] = []
    current: dict[str, list[str]] = {}
    last_key: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip():
            if current:
                records.append(_normalize_nbib(current))
                current = {}
                last_key = None
            continue
        match = re.match(r"^([A-Z0-9]{2,4})\s*-\s?(.*)$", raw_line)
        if match:
            key, value = match.groups()
            _append_field(current, key, value)
            last_key = key
        elif last_key and current:
            current[last_key][-1] = f"{current[last_key][-1]} {raw_line.strip()}"
    if current:
        records.append(_normalize_nbib(current))
    return records


def _first(record: dict[str, list[str]], *keys: str) -> str:
    for key in keys:
        values = record.get(key, [])
        if values:
            return values[0]
    return ""


def _normalize_ris(record: dict[str, list[str]]) -> dict[str, list[str]]:
    doi_values = record.get("DO", [])
    pmid_values = [value.removeprefix("PMID:").strip() for value in record.get("PMID", [])]
    for note in record.get("N1", []) + record.get("M1", []):
        pmid_match = re.search(r"PMID[:\s]+(\d+)", note, flags=re.IGNORECASE)
        if pmid_match:
            pmid_values.append(pmid_match.group(1))
    return {
        "ENTRYTYPE": ["article"],
        "author": record.get("AU", []) + record.get("A1", []),
        "title": [_first(record, "TI", "T1")],
        "journal": [_first(record, "JO", "T2", "JF", "J1")],
        "year": [_year(_first(record, "PY", "Y1", "DA"))],
        "volume": [_first(record, "VL")],
        "number": [_first(record, "IS")],
        "pages": [_pages(_first(record, "SP"), _first(record, "EP"))],
        "DOI": doi_values,
        "PMID": pmid_values,
        "url": record.get("UR", []),
    }


def _normalize_nbib(record: dict[str, list[str]]) -> dict[str, list[str]]:
    doi_values = []
    for value in record.get("LID", []) + record.get("AID", []):
        doi_match = re.search(r"([^ ]+)\s+\[doi\]", value, flags=re.IGNORECASE)
        if doi_match:
            doi_values.append(doi_match.group(1))
    return {
        "ENTRYTYPE": ["article"],
        "author": record.get("FAU", []) or record.get("AU", []),
        "title": [_first(record, "TI")],
        "journal": [_first(record, "JT", "TA")],
        "year": [_year(_first(record, "DP", "DEP", "PHST"))],
        "volume": [_first(record, "VI")],
        "number": [_first(record, "IP")],
        "pages": [_first(record, "PG")],
        "DOI": doi_values,
        "PMID": record.get("PMID", []),
        "url": record.get("AID", []),
    }


def _year(value: str) -> str:
    match = re.search(r"(19|20)\d{2}", value)
    return match.group(0) if match else value.strip()


def _pages(start: str, end: str) -> str:
    if start and end:
        return f"{start}--{end}"
    return start or end


def _clean_values(record: dict[str, list[str]]) -> dict[str, list[str]]:
    return {key: [value for value in values if value] for key, values in record.items()}


def _citation_key(record: dict[str, list[str]], index: int) -> str:
    author = _first(record, "author") or "unknown"
    title = _first(record, "title") or "untitled"
    year = _first(record, "year") or "nodate"
    last_name = re.split(r"[, ]+", author.strip())[0].lower()
    title_word = re.sub(r"[^A-Za-z0-9]+", "", title.split()[0].lower()) if title.split() else "paper"
    return re.sub(r"[^A-Za-z0-9:_-]+", "", f"{last_name}{year}{title_word}{index}")


def _bibtex_escape(value: str) -> str:
    return value.replace("\\", "\\textbackslash{}").replace("{", "\\{").replace("}", "\\}")


def to_bibtex(records: list[dict[str, list[str]]]) -> str:
    """Render normalized citation records as BibTeX."""

    entries: list[str] = []
    for index, raw_record in enumerate(records, start=1):
        record = _clean_values(raw_record)
        entry_type = _first(record, "ENTRYTYPE") or "article"
        key = _citation_key(record, index)
        lines = [f"@{entry_type}{{{key},"]
        field_order = ("author", "title", "journal", "year", "volume", "number", "pages", "DOI", "PMID", "url")
        for field in field_order:
            values = record.get(field, [])
            if not values:
                continue
            value = " and ".join(values) if field == "author" else values[0]
            bib_field = "doi" if field == "DOI" else "pmid" if field == "PMID" else field
            lines.append(f"  {bib_field} = {{{_bibtex_escape(value)}}},")
        if len(lines) == 1:
            lines.append("  note = {not verified},")
        lines.append("}")
        entries.append("\n".join(lines))
    return "\n\n".join(entries) + ("\n" if entries else "")


def _detect_format(path: Path, text: str, requested: str) -> str:
    if requested != "auto":
        return requested
    suffix = path.suffix.lower()
    if suffix == ".nbib":
        return "nbib"
    if suffix == ".ris":
        return "ris"
    if "PMID-" in text or "FAU -" in text:
        return "nbib"
    return "ris"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert RIS or NBIB citation exports to BibTeX.")
    parser.add_argument("input", type=Path, help="Input .ris, .nbib, or text export")
    parser.add_argument("-o", "--output", type=Path, help="Output .bib path; stdout when omitted")
    parser.add_argument("--format", choices=("auto", "ris", "nbib"), default="auto")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8", errors="replace")
    source_format = _detect_format(args.input, text, args.format)
    records = parse_nbib(text) if source_format == "nbib" else parse_ris(text)
    bibtex = to_bibtex(records)
    if args.output:
        args.output.write_text(bibtex, encoding="utf-8")
    else:
        print(bibtex, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
