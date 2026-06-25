#!/usr/bin/env python3
"""Audit medical BibTeX, citation evidence, and rendered-reference integrity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CITE_RE = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I)
FIELD_RE = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[{'\"]")
BBL_ITEM_RE = re.compile(r"\\bibitem(?:\s*\[[^\]]*\])?\s*\{([^}]*)\}", re.S)
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
VISIBLE_DOI_RE = re.compile(r"\b10\.\d{4,9}/\S+", re.I)
PMID_RE = re.compile(r"^\d{1,9}$")
PMCID_RE = re.compile(r"^PMC\d+$", re.I)
URL_RE = re.compile(r"https?://|www\.", re.I)
REGISTRY_RE = re.compile(r"\b(?:NCT\d{8}|ISRCTN\d+|ChiCTR[A-Za-z0-9]+)\b", re.I)
PLACEHOLDER_AUTHOR_RE = re.compile(r"\band\s+others\b|\bet\s+al\.?\b", re.I)
RENDERED_PLACEHOLDER_AUTHOR_RE = re.compile(r"\band\s+\d+\s+others\b|\b\d+\s+others\b", re.I)
TITLE_TERM_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*")
KEY_YEAR_RE = re.compile(r"(?:19|20)\d{2}")

MEDICAL_TITLE_TERMS = {
    "AUC",
    "CARE",
    "CHEERS",
    "CONSORT",
    "COVID-19",
    "CT",
    "DNA",
    "EHR",
    "GATHER",
    "HbA1c",
    "ICD-9",
    "ICD-10",
    "ICD-11",
    "ICMJE",
    "ICU",
    "IRB",
    "MRI",
    "NIHSS",
    "PMCID",
    "PMID",
    "PRISMA",
    "RCT",
    "RNA",
    "ROC",
    "SAP",
    "SARS-CoV-2",
    "SPIRIT",
    "STARD",
    "STROBE",
    "TRIPOD",
    "mRNA",
}

EVIDENCE_REQUIRED_HEADERS = (
    "claim id",
    "claim text",
    "citation key",
    "source anchor",
    "population match",
    "outcome match",
    "metric/timeframe match",
    "conclusion strength",
    "verdict",
    "required action",
)


def public_artifact_path(path: Path) -> str:
    parts = path.parts
    if "paper" in parts:
        return "/".join(parts[parts.index("paper") :])
    if path.is_dir() or not path.suffix:
        return "paper"
    return f"paper/{path.name}"


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        cut = len(line)
        for index, char in enumerate(line):
            if char == "\\":
                escaped = not escaped
                continue
            if char == "%" and not escaped:
                cut = index
                break
            escaped = False
        lines.append(line[:cut])
    return "\n".join(lines)


def find_matching_brace(text: str, open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
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
        field_matches = list(FIELD_RE.finditer(body))
        for field_index, field_match in enumerate(field_matches):
            name = field_match.group(1).lower()
            value_start = field_match.end()
            opener = body[value_start - 1]
            if opener == "{":
                value_end = find_matching_brace(body, value_start - 1)
                if value_end < 0:
                    fields[name] = body[value_start:].strip()
                else:
                    fields[name] = " ".join(body[value_start:value_end].split())
            else:
                next_match = field_matches[field_index + 1] if field_index + 1 < len(field_matches) else None
                next_comma = body.rfind(",", value_start, next_match.start() if next_match else len(body))
                if next_comma < 0:
                    next_comma = len(body)
                fields[name] = body[value_start:next_comma].strip().strip("'\"")
        entries[key] = fields
    return entries


def extract_tex_cites(tex_files: list[Path]) -> list[str]:
    keys: list[str] = []
    for path in tex_files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        for match in CITE_RE.finditer(text):
            for key in match.group(1).split(","):
                key = key.strip()
                if key:
                    keys.append(key)
    return keys


def year_value(fields: dict[str, str]) -> int | None:
    match = re.search(r"\d{4}", fields.get("year", ""))
    return int(match.group(0)) if match else None


def valid_doi(value: str) -> bool:
    return bool(DOI_RE.match(value.strip().rstrip(".,")))


def valid_pmid(value: str) -> bool:
    return bool(PMID_RE.match(value.strip()))


def valid_pmcid(value: str) -> bool:
    return bool(PMCID_RE.match(value.strip()))


def has_valid_registry(fields: dict[str, str]) -> bool:
    joined = " ".join(
        fields.get(name, "")
        for name in ("registry", "trialregistration", "clinicaltrials", "note", "url")
    )
    return bool(REGISTRY_RE.search(joined))


def has_stable_medical_identifier(fields: dict[str, str]) -> bool:
    if valid_doi(fields.get("doi", "")):
        return True
    if valid_pmid(fields.get("pmid", "")):
        return True
    if valid_pmcid(fields.get("pmcid", "")):
        return True
    if URL_RE.search(fields.get("url", "")):
        return True
    return has_valid_registry(fields)


def needs_title_preservation(token: str) -> bool:
    if token in MEDICAL_TITLE_TERMS:
        return True
    letters = [char for char in token if char.isalpha()]
    if len(letters) < 2:
        return False
    if all(char.isupper() for char in letters):
        return True
    return any(char.isupper() for char in token[1:])


def title_preservation_terms(title: str) -> list[str]:
    terms: set[str] = set()
    unbraced = title.replace("{", "").replace("}", "")
    for match in TITLE_TERM_RE.finditer(unbraced):
        token = match.group(0).strip("-")
        if token and needs_title_preservation(token):
            terms.add(token)
    for term in MEDICAL_TITLE_TERMS:
        if term in unbraced:
            terms.add(term)
    return sorted(terms, key=lambda value: (-len(value), value.lower()))


def parse_bbl_items(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(BBL_ITEM_RE.finditer(text))
    items: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        items.append((match.group(1).strip(), text[match.start() : end]))
    return items


def has_visible_identifier(text: str) -> bool:
    return bool(
        VISIBLE_DOI_RE.search(text)
        or URL_RE.search(text)
        or re.search(r"\bPMID[:\s]*\d+\b", text, re.I)
        or re.search(r"\bPMC\d+\b", text, re.I)
        or REGISTRY_RE.search(text)
    )


def audit_rendered_references(paper_dir: Path, entries: dict[str, dict[str, str]], errors: list[str]) -> None:
    for bbl_path in sorted(paper_dir.glob("*.bbl")):
        for key, block in parse_bbl_items(bbl_path):
            if RENDERED_PLACEHOLDER_AUTHOR_RE.search(block):
                errors.append(
                    f"rendered reference placeholder author: {public_artifact_path(bbl_path)}: {key}: "
                    "BibTeX output contains `and N others`; fix the author field and rerun BibTeX"
                )
            year = year_value(entries.get(key, {}))
            if year and year >= 2000 and not has_visible_identifier(block):
                errors.append(
                    "rendered reference lacks visible DOI/PMID/PMCID/URL/registry: "
                    f"{public_artifact_path(bbl_path)}: {key}"
                )
            title = entries.get(key, {}).get("title", "")
            lost_terms = [
                term
                for term in title_preservation_terms(title)
                if term not in block and term.lower() in block.lower()
            ]
            if lost_terms:
                shown = ", ".join(f"`{term}`" for term in lost_terms)
                errors.append(
                    "rendered reference lost biomedical title capitalization: "
                    f"{public_artifact_path(bbl_path)}: {key}: "
                    f"{shown} from the BibTeX title was lowercased; protect biomedical acronyms "
                    "and proper names with braces and rerun BibTeX"
                )


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip().strip("`").lower() for cell in line.strip().strip("|").split("|")]


def audit_evidence_table(paper_dir: Path, errors: list[str]) -> None:
    for filename in ("citation-evidence.md", "claim-registry.md"):
        path = paper_dir / filename
        if not path.exists():
            continue
        header: list[str] | None = None
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?", stripped):
                continue
            header = split_markdown_row(stripped)
            break
        if header is None:
            errors.append(
                f"medical citation evidence schema: {public_artifact_path(path)} has no markdown table header"
            )
            continue
        missing = [name for name in EVIDENCE_REQUIRED_HEADERS if name not in header]
        if missing:
            errors.append(
                f"medical citation evidence schema: {public_artifact_path(path)} is missing required column(s): "
                f"{', '.join(missing)}"
            )


def audit_entry(key: str, fields: dict[str, str], errors: list[str], warnings: list[str]) -> None:
    if fields.get("_parse_error"):
        errors.append(f"malformed BibTeX entry: {key}: {fields['_parse_error']}")
        return
    for required in ("title", "year"):
        if not fields.get(required):
            errors.append(f"missing required BibTeX field: {key}: {required}")
    if fields.get("entry_type") == "article" and not fields.get("journal"):
        errors.append(f"missing required BibTeX field: {key}: journal")
    author = fields.get("author", "")
    if not author:
        errors.append(f"missing required BibTeX field: {key}: author")
    elif PLACEHOLDER_AUTHOR_RE.search(author):
        errors.append(f"placeholder author in BibTeX: {key}: use a verified author list")

    doi = fields.get("doi", "")
    if doi and not valid_doi(doi):
        errors.append(f"malformed DOI: {key}: {doi}")
    pmid = fields.get("pmid", "")
    if pmid and not valid_pmid(pmid):
        errors.append(f"malformed PMID: {key}: {pmid}")
    pmcid = fields.get("pmcid", "")
    if pmcid and not valid_pmcid(pmcid):
        errors.append(f"malformed PMCID: {key}: {pmcid}")

    year = year_value(fields)
    if year and year >= 2000 and not has_stable_medical_identifier(fields):
        errors.append(f"modern medical entry lacks DOI/PMID/PMCID/URL/registry: {key}")
    elif not has_stable_medical_identifier(fields):
        warnings.append(f"entry lacks DOI/PMID/PMCID/URL/registry: {key}")


def audit(paper_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    bib_path = paper_dir / "references.bib"
    if not bib_path.exists():
        errors.append(f"missing bibliography file: {public_artifact_path(bib_path)}")
        return errors, warnings

    entries = parse_bib_entries(bib_path)
    tex_files = sorted(paper_dir.rglob("*.tex"))
    used_keys = extract_tex_cites(tex_files) if tex_files else []
    used = set(used_keys)
    bib_keys = set(entries)

    if tex_files:
        for key in sorted(used - bib_keys):
            errors.append(f"citation key missing from references.bib: {key}")
        for key in sorted(bib_keys - used):
            errors.append(f"uncited bibliography entry: {key}")

    keys_to_check = sorted((used & bib_keys) if tex_files else bib_keys)
    for key in keys_to_check:
        audit_entry(key, entries[key], errors, warnings)

    audit_rendered_references(paper_dir, entries, errors)
    audit_evidence_table(paper_dir, errors)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_dir", nargs="?", default="paper", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    errors, warnings = audit(paper_dir)
    report = {
        "path": public_artifact_path(paper_dir),
        "status": "PASS" if not errors else "BLOCKED",
        "errors": errors,
        "warnings": warnings,
        "metrics": {"error_count": len(errors), "warning_count": len(warnings)},
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Medical citation audit: {public_artifact_path(paper_dir)}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- WARN: {warning}")
        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"- ERROR: {error}")
            print(f"\nFAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
            return 1
        print(f"PASS: 0 error(s), {len(warnings)} warning(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
