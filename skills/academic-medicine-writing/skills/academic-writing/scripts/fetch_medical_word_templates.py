#!/usr/bin/env python3
"""Fetch and validate official medical Word template candidates.

The script downloads only allowlisted official template URLs. A failed download is reported as
download-blocked or another explicit status; it never creates an official-template manifest entry
from an invalid or non-DOCX response.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path


REQUIRED_DOCX_PARTS = (
    "[Content_Types].xml",
    "word/document.xml",
    "word/styles.xml",
)
GENERIC_FALLBACK = "assets/templates/word/generic-medical-word-reference.docx"


@dataclass(frozen=True)
class TemplateCandidate:
    key: str
    label: str
    url: str
    filename: str
    official_source_url: str


ALLOWLIST = {
    "bmj-clinical-case-report": TemplateCandidate(
        key="bmj-clinical-case-report",
        label="BMJ Case Reports Clinical Case Report",
        url="https://casereports.bmj.com/casereports/wp-content/uploads/sites/64/2023/06/Clinical-Case-Report-template-2023-word.docx",
        filename="bmj-clinical-case-report-template.docx",
        official_source_url="https://casereports.bmj.com/pages/authors",
    ),
    "bmj-global-health-case-report": TemplateCandidate(
        key="bmj-global-health-case-report",
        label="BMJ Case Reports Global Health Case Report",
        url="https://casereports.bmj.com/casereports/wp-content/uploads/sites/64/2023/06/Global-Health-Case-Report-template-2023-word.docx",
        filename="bmj-global-health-case-report-template.docx",
        official_source_url="https://casereports.bmj.com/pages/authors",
    ),
    "bmj-images-in": TemplateCandidate(
        key="bmj-images-in",
        label="BMJ Case Reports Images In",
        url="https://casereports.bmj.com/casereports/wp-content/uploads/sites/64/2023/06/Images-in-template-2023-word.docx",
        filename="bmj-images-in-template.docx",
        official_source_url="https://casereports.bmj.com/pages/authors",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_docx(path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            missing = [part for part in REQUIRED_DOCX_PARTS if part not in names]
    except zipfile.BadZipFile:
        return ["not a valid DOCX zip package"]
    return [f"missing DOCX part: {part}" for part in missing]


def download(candidate: TemplateCandidate, output_dir: Path, timeout: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / candidate.filename
    request = urllib.request.Request(
        candidate.url,
        headers={
            "User-Agent": "Mozilla/5.0 medical-template-fetch/1.0",
            "Referer": candidate.official_source_url,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        status = "download-blocked" if exc.code in {401, 403, 429} else "download-failed"
        return {
            "key": candidate.key,
            "label": candidate.label,
            "status": status,
            "http_status": exc.code,
            "url": candidate.url,
            "official_source_url": candidate.official_source_url,
        }
    except urllib.error.URLError as exc:
        return {
            "key": candidate.key,
            "label": candidate.label,
            "status": "download-failed",
            "error": str(exc.reason),
            "url": candidate.url,
            "official_source_url": candidate.official_source_url,
        }

    output.write_bytes(body)
    issues = validate_docx(output)
    if issues:
        output.unlink(missing_ok=True)
        return {
            "key": candidate.key,
            "label": candidate.label,
            "status": "invalid-docx",
            "issues": issues,
            "url": candidate.url,
            "official_source_url": candidate.official_source_url,
        }

    return {
        "key": candidate.key,
        "label": candidate.label,
        "status": "downloaded",
        "path": str(output),
        "sha256": sha256(output),
        "url": candidate.url,
        "official_source_url": candidate.official_source_url,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--template", choices=sorted(ALLOWLIST), action="append")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--timeout", type=int, default=45)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    keys = sorted(ALLOWLIST) if args.all else (args.template or [])
    if not keys:
        raise SystemExit("select at least one --template or use --all")

    results = [download(ALLOWLIST[key], args.output_dir, args.timeout) for key in keys]
    print(json.dumps({"results": results}, indent=2, sort_keys=True))
    return 1 if any(result["status"] != "downloaded" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
