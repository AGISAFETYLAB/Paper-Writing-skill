#!/usr/bin/env python3
"""Static citation audit for academic-writing drafts.

This does not prove that a source supports a claim. It catches local bibliography
integrity failures before a draft is described as citation-clean.

If paper/citation-evidence.md exists, it must use the claim-support ledger schema
from static/citation-workflow.md so citation verification does not collapse into a
source list.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CITE_RE = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I)
FIELD_RE = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[{'\"]")
MARKER_RE = re.compile(r"%\s*(CITATION_NEEDED|EVIDENCE_NEEDED)\b")
PLACEHOLDER_AUTHOR_RE = re.compile(r"\band\s+others\b|\bet\s+al\.?\b", re.I)
RENDERED_PLACEHOLDER_AUTHOR_RE = re.compile(r"\band\s+\d+\s+others\b|\b\d+\s+others\b", re.I)
ARXIV_RE = re.compile(r"\b\d{4}\.\d{4,5}(?:v\d+)?\b|[a-z-]+/\d{7}(?:v\d+)?", re.I)
DOI_RE = re.compile(r"10\.\d{4,9}/\S+")
URL_RE = re.compile(r"https?://|www\.", re.I)
KEY_YEAR_RE = re.compile(r"(?:19|20)\d{2}")
BBL_ITEM_RE = re.compile(r"\\bibitem(?:\s*\[[^\]]*\])?\s*\{([^}]*)\}", re.S)
TITLE_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z][A-Za-z0-9]*)*")
LEDGER_REQUIRED_HEADERS = (
    "claim id",
    "claim text / clause",
    "citation key",
    "source",
    "metadata source",
    "support grade",
    "evidence basis",
    "action",
)


def strip_comments(text: str) -> str:
    lines = []
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
        field_matches = list(FIELD_RE.finditer(body))
        for i, field_match in enumerate(field_matches):
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
            for key in match.group(1).split(","):
                key = key.strip()
                if key:
                    keys.append(key)
    return keys, markers


def has_stable_identifier(fields: dict[str, str]) -> bool:
    # A non-empty identifier field is not enough; it must look like a real DOI,
    # URL, or arXiv id. This rejects malformed placeholders such as
    # ``eprint = {2025}`` or ``arXiv preprint arXiv:2025`` (year used as the id).
    doi = fields.get("doi", "")
    if doi and (DOI_RE.search(doi) or "doi.org/" in doi.lower()):
        return True
    url = fields.get("url", "")
    if url and URL_RE.search(url):
        return True
    eprint = fields.get("eprint", "")
    if eprint and ARXIV_RE.search(eprint):
        return True
    # a real URL is a valid stable identifier for web / blog / report sources, and it is
    # commonly stored in howpublished or note rather than the url field.
    for name in ("howpublished", "note"):
        if URL_RE.search(fields.get(name, "")):
            return True
    joined = " ".join(fields.values())
    return bool(ARXIV_RE.search(joined) or "doi.org/" in joined.lower() or URL_RE.search(joined))


def has_visible_identifier(text: str) -> bool:
    return bool(DOI_RE.search(text) or ARXIV_RE.search(text) or URL_RE.search(text) or "\\href" in text)


def needs_title_case_preservation(token: str) -> bool:
    letters = [char for char in token if char.isalpha()]
    if len(letters) < 2:
        return False
    if all(char.isupper() for char in letters):
        return True
    # Detect CamelCase / mixed acronym terms such as AgentDojo, OSWorld,
    # WebArena, ToolLLM, APIs, and ReAct. Plain Title Case words do not match.
    return any(char.isupper() for char in token[1:])


def title_preservation_terms(title: str) -> list[str]:
    terms: set[str] = set()
    unbraced = title.replace("{", "").replace("}", "")
    for match in TITLE_TOKEN_RE.finditer(unbraced):
        token = match.group(0).strip("-")
        if not token:
            continue
        parts = [part for part in token.split("-") if part]
        preserved_parts = [part for part in parts if needs_title_case_preservation(part)]
        if "-" in token:
            terms.update(preserved_parts)
            continue
        if needs_title_case_preservation(token):
            terms.add(token)
    return sorted(terms, key=lambda item: (-len(item), item.lower()))


def year_value(fields: dict[str, str]) -> int | None:
    match = re.search(r"\d{4}", fields.get("year", ""))
    return int(match.group(0)) if match else None


def key_years(key: str) -> set[int]:
    # Year-like tokens embedded in the citation key, restricted to a plausible
    # publication range so identifiers such as ``imagenet1000`` or ``iso27001``
    # are not misread as years.
    return {int(m.group(0)) for m in KEY_YEAR_RE.finditer(key) if 1900 <= int(m.group(0)) <= 2099}


def parse_bbl_items(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(BBL_ITEM_RE.finditer(text))
    items: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        items.append((match.group(1).strip(), text[match.start():end]))
    return items


def audit_rendered_bibliography(
    paper_dir: Path, entries: dict[str, dict[str, str]], errors: list[str]
) -> None:
    for bbl_path in sorted(paper_dir.glob("*.bbl")):
        for key, block in parse_bbl_items(bbl_path):
            if RENDERED_PLACEHOLDER_AUTHOR_RE.search(block):
                errors.append(
                    f"rendered bibliography placeholder author: {bbl_path}: {key}: "
                    "BibTeX output contains `and N others`; fix the author field and rerun BibTeX"
                )

            years = [int(m.group(0)) for m in KEY_YEAR_RE.finditer(block)]
            year = min((y for y in years if 1900 <= y <= 2099), default=None)
            if year and year >= 2000 and not has_visible_identifier(block):
                errors.append(
                    f"rendered bibliography lacks visible DOI/URL/arXiv: {bbl_path}: {key}: "
                    "modern bibliography item renders without a traceable source link"
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
                    f"rendered bibliography lost title capitalization: {bbl_path}: {key}: "
                    f"{shown} from the BibTeX title was lowercased in the rendered bibliography; "
                    "protect CS proper names and acronyms with extra braces in the title field and rerun BibTeX"
                )


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip().strip("`").lower() for cell in line.strip().strip("|").split("|")]


def audit_citation_evidence_ledger(paper_dir: Path, errors: list[str]) -> None:
    ledger = paper_dir / "citation-evidence.md"
    if not ledger.exists():
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
        errors.append(
            f"citation evidence ledger schema: {ledger} has no markdown table header; "
            "use the Claim ID / Claim text / Citation key / support-grade ledger"
        )
        return
    missing = [name for name in LEDGER_REQUIRED_HEADERS if name not in header]
    if missing:
        errors.append(
            f"citation evidence ledger schema: {ledger} is missing required column(s): "
            f"{', '.join(missing)}; use the claim-support ledger from static/citation-workflow.md"
        )


def audit(paper_dir: Path, min_citations: int = 0) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    bib_path = paper_dir / "references.bib"
    if not bib_path.exists():
        errors.append(f"missing bibliography file: {bib_path}")
        return errors, warnings

    tex_files = sorted(paper_dir.rglob("*.tex"))
    if not tex_files:
        errors.append(f"no .tex files found under {paper_dir}")
        return errors, warnings

    used_keys, markers = extract_cites(tex_files)
    entries = parse_bib_entries(bib_path)
    used = set(used_keys)
    bib_keys = set(entries)

    # Citation coverage floor. When the caller supplies a paper-type floor, treat it as an
    # explicit gate rather than a style smell: benchmark/survey/method papers with too few cited
    # works are usually missing prior benchmarks, datasets, models, or security baselines.
    if min_citations and len(used) < min_citations:
        errors.append(
            f"low citation coverage: {len(used)} distinct cited works (< {min_citations} expected "
            f"for this paper type); check that Related Work and Introduction cite prior work and "
            f"that every named model/dataset/baseline/framework is cited"
        )

    for path, lineno, line in markers:
        errors.append(f"unresolved citation marker: {path}:{lineno}: {line}")

    for key in sorted(used - bib_keys):
        errors.append(f"citation key missing from references.bib: {key}")

    for key in sorted(bib_keys - used):
        errors.append(f"uncited bibliography entry: {key}")

    for key in sorted(used & bib_keys):
        fields = entries[key]
        if fields.get("_parse_error"):
            errors.append(f"malformed BibTeX entry: {key}: {fields['_parse_error']}")
            continue
        for required in ("title", "author", "year"):
            if not fields.get(required):
                errors.append(f"missing required BibTeX field: {key}: {required}")

        author = fields.get("author", "")
        if PLACEHOLDER_AUTHOR_RE.search(author):
            errors.append(f"placeholder author in BibTeX: {key}: use full verified author list, no `and others`")

        year = year_value(fields)
        key_year_set = key_years(key)
        if year is not None and key_year_set and year not in key_year_set:
            shown = "/".join(str(y) for y in sorted(key_year_set))
            errors.append(
                f"year-key mismatch: {key}: key year {shown} != year field {year} "
                f"(fix or replace; mismatched keys indicate a fabricated or botched entry)"
            )

        if year and year >= 2000 and not has_stable_identifier(fields):
            errors.append(f"modern entry lacks DOI/URL/arXiv: {key}")
        elif not has_stable_identifier(fields):
            warnings.append(f"entry lacks DOI/URL/arXiv: {key}")

        venue = " ".join(
            fields.get(name, "") for name in ("journal", "booktitle", "institution", "publisher")
        ).lower()
        if ("technical report" in venue or "arxiv preprint" in venue) and not has_stable_identifier(fields):
            errors.append(f"vague source label without stable identifier: {key}")

    audit_rendered_bibliography(paper_dir, entries, errors)
    audit_citation_evidence_ledger(paper_dir, errors)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit citation and BibTeX integrity for a LaTeX paper.")
    parser.add_argument("paper_dir", nargs="?", default="paper", help="Paper directory containing references.bib")
    parser.add_argument(
        "--min-citations",
        type=int,
        default=0,
        help="Fail if the draft cites fewer than this many distinct works (0 disables; set per "
        "paper type, e.g. benchmark/survey/method papers expect a fuller bibliography).",
    )
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    errors, warnings = audit(paper_dir, min_citations=args.min_citations)

    print(f"Citation audit: {paper_dir}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- WARN: {item}")
    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- ERROR: {item}")
        print(f"\nFAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
