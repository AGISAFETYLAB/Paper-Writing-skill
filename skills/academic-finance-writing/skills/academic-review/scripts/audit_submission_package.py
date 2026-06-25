#!/usr/bin/env python3
"""Audit finance submission-package status fields and attachment gates."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_STATUS_FIELDS = (
    "page_window_status",
    "format_compliance_status",
    "local_path_leak_status",
    "table_static_lint_status",
    "visual_asset_qa_status",
    "compiled_layout_qa_status",
    "layout_manual_inspection_status",
    "central_result_uncertainty_status",
    "submission_attachment_status",
    "replication_package_status",
    "submission_readiness_verdict",
)
PLACEHOLDER_RE = re.compile(
    r"\b(placeholder|would contain|would include|for a real|real submission must|"
    r"intentionally anonymous|no author conflict statement is supplied)\b",
    re.I,
)
BLOCKING_READINESS = {"blocked", "fail", "failed"}
NONPASS = {"partial", "blocked", "not_applicable", "not_performed", "waived", "missing", ""}


@dataclass(frozen=True)
class SubmissionPackageFinding:
    code: str
    message: str


def parse_status_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return fields


def file_contains_placeholder(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="ignore")
    return PLACEHOLDER_RE.search(text) is not None


def audit_submission_package(paper_dir: Path | str) -> list[SubmissionPackageFinding]:
    paper = Path(paper_dir)
    package_path = paper / "submission-package.md"
    findings: list[SubmissionPackageFinding] = []
    if not package_path.exists():
        return [SubmissionPackageFinding("missing_submission_package", "paper/submission-package.md is missing")]

    text = package_path.read_text(encoding="utf-8", errors="ignore")
    fields = parse_status_fields(text)

    for field in REQUIRED_STATUS_FIELDS:
        if field not in fields:
            findings.append(
                SubmissionPackageFinding(
                    "missing_status_field",
                    f"submission-package.md missing `{field}` status field",
                )
            )

    readiness = fields.get("submission_readiness_verdict", "").lower()

    if fields.get("compiled_layout_qa_status", "").lower() == "pass":
        manual_status = fields.get("layout_manual_inspection_status", "").lower()
        if manual_status != "pass":
            findings.append(
                SubmissionPackageFinding(
                    "layout_pass_without_manual_inspection",
                    "`compiled_layout_qa_status: pass` requires `layout_manual_inspection_status: pass`",
                )
            )

    if fields.get("visual_asset_qa_status", "").lower() == "pass":
        figures_dir = paper / "figures"
        if figures_dir.exists() and not any(figures_dir.glob("*")):
            findings.append(
                SubmissionPackageFinding(
                    "visual_asset_pass_without_assets",
                    "`visual_asset_qa_status: pass` is invalid when paper/figures is empty",
                )
            )

    if fields.get("central_result_uncertainty_status", "").lower() in {"missing", "blocked"}:
        if readiness not in BLOCKING_READINESS:
            findings.append(
                SubmissionPackageFinding(
                    "uncertainty_blocker_not_reflected",
                    "missing central-result uncertainty must block submission-readiness wording",
                )
            )

    title_placeholder = file_contains_placeholder(paper / "title-page.md")
    coi_placeholder = file_contains_placeholder(paper / "conflict-of-interest-disclosure.md")
    attachment_status = fields.get("submission_attachment_status", "").lower()
    if title_placeholder or coi_placeholder:
        if attachment_status == "pass":
            findings.append(
                SubmissionPackageFinding(
                    "placeholder_attachment_marked_pass",
                    "placeholder title page or COI disclosure cannot be marked as submission-ready",
                )
            )
        if readiness not in BLOCKING_READINESS:
            findings.append(
                SubmissionPackageFinding(
                    "placeholder_attachment_not_blocking",
                    "placeholder title page or COI disclosure must block submission-readiness wording",
                )
            )

    if "synthetic" in text.lower() and readiness not in BLOCKING_READINESS:
        findings.append(
            SubmissionPackageFinding(
                "synthetic_evidence_not_blocking",
                "synthetic evidence boundary must block real submission-readiness wording",
            )
        )

    for field in ("replication_package_status", "submission_attachment_status"):
        if fields.get(field, "").lower() in {"missing", "blocked"} and readiness not in BLOCKING_READINESS:
            findings.append(
                SubmissionPackageFinding(
                    "blocking_status_not_reflected",
                    f"`{field}` is blocking but submission_readiness_verdict is not blocked/fail",
                )
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit finance submission-package status integrity.")
    parser.add_argument("paper_dir", nargs="?", default="paper", type=Path)
    args = parser.parse_args()

    findings = audit_submission_package(args.paper_dir)
    if findings:
        for finding in findings:
            print(f"{finding.code}: {finding.message}")
        print(f"FAIL finance submission package audit: {len(findings)} finding(s)")
        return 1
    print("PASS finance submission package audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
