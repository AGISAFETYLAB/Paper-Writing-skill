#!/usr/bin/env python3
"""Audit the finance page-window gate for a compiled manuscript package."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


VALID_STATUSES = {"pass", "below_min_pages", "above_max_pages", "blocked_uncounted"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def parse_int_field(text: str, field: str) -> int | None:
    match = re.search(rf"(?m)^\s*{re.escape(field)}\s*:\s*(\d+)\s*$", text)
    return int(match.group(1)) if match else None


def parse_status(text: str) -> str | None:
    match = re.search(r"(?m)^\s*page_window_status\s*:\s*([A-Za-z0-9_-]+)\s*$", text)
    return match.group(1).strip() if match else None


def pdfinfo_pages(pdf_path: Path) -> int | None:
    if not pdf_path.exists():
        return None
    try:
        proc = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", proc.stdout)
    return int(match.group(1)) if match else None


def aux_pages(aux_path: Path) -> int | None:
    match = re.search(r"\\gdef\s*\\@abspage@last\{(\d+)\}", read_text(aux_path))
    return int(match.group(1)) if match else None


def expected_status(actual_pages: int | None, min_pages: int, max_pages: int) -> str:
    if actual_pages is None:
        return "blocked_uncounted"
    if actual_pages < min_pages:
        return "below_min_pages"
    if actual_pages > max_pages:
        return "above_max_pages"
    return "pass"


def audit_package(paper_dir: Path, min_pages_arg: int | None, max_pages_arg: int | None) -> list[str]:
    errors: list[str] = []
    submission_path = paper_dir / "submission-package.md"
    submission = read_text(submission_path)
    if not submission:
        errors.append(f"missing submission package: {submission_path}")

    for token in (
        "target_page_window:",
        "min_pages:",
        "max_pages:",
        "source_type:",
        "source_url:",
        "date_checked:",
        "count_scope:",
        "actual_pdf_pages:",
        "page_window_status:",
    ):
        if token not in submission:
            errors.append(f"submission-package.md missing `{token}`")

    min_pages = min_pages_arg if min_pages_arg is not None else parse_int_field(submission, "min_pages")
    max_pages = max_pages_arg if max_pages_arg is not None else parse_int_field(submission, "max_pages")
    if min_pages is None:
        errors.append("missing min_pages; pass --min-pages or record it under target_page_window")
    if max_pages is None:
        errors.append("missing max_pages; pass --max-pages or record it under target_page_window")
    if min_pages is not None and max_pages is not None and min_pages > max_pages:
        errors.append(f"invalid page window: min_pages {min_pages} > max_pages {max_pages}")

    actual_pages = pdfinfo_pages(paper_dir / "main.pdf")
    if actual_pages is None:
        actual_pages = aux_pages(paper_dir / "main.aux")
    recorded_pages = parse_int_field(submission, "actual_pdf_pages")
    if recorded_pages is not None and actual_pages is not None and recorded_pages != actual_pages:
        errors.append(
            f"actual_pdf_pages mismatch: submission-package.md records {recorded_pages}, "
            f"compiled PDF/aux reports {actual_pages}"
        )
    if recorded_pages is None and actual_pages is not None:
        errors.append(f"submission-package.md missing actual_pdf_pages: {actual_pages}")
    if actual_pages is None:
        errors.append("blocked_uncounted: could not count pages from main.pdf or main.aux")

    status = parse_status(submission)
    if status is not None and status not in VALID_STATUSES:
        errors.append(f"invalid page_window_status: {status}")

    if min_pages is not None and max_pages is not None:
        expected = expected_status(actual_pages, min_pages, max_pages)
        if status != expected:
            errors.append(f"page_window_status mismatch: recorded {status!r}, expected {expected!r}")
        if expected != "pass":
            errors.append(
                f"{expected} blocks the full-draft return: actual_pdf_pages={actual_pages}, "
                f"target_page_window={min_pages}-{max_pages}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit finance page-window status")
    parser.add_argument("paper_dir", type=Path, help="Path to paper/ directory")
    parser.add_argument("--min-pages", type=int, default=None)
    parser.add_argument("--max-pages", type=int, default=None)
    args = parser.parse_args()

    errors = audit_package(args.paper_dir.resolve(), args.min_pages, args.max_pages)
    if errors:
        print("FAIL finance page-window audit")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS finance page-window audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
