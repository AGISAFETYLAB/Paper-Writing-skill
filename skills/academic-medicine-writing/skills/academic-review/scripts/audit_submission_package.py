#!/usr/bin/env python3
"""Aggregate gate for medicine manuscript package readiness contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_STATE_FIELDS = (
    "schema_version",
    "workflow",
    "intent",
    "study_type",
    "article_type",
    "submission_format_route",
    "policy_confirmed",
    "framework_confirmed",
    "primary_submission_file",
    "selected_checklist",
    "required_displays",
    "required_audits",
    "blocking_gaps",
)

REQUIRED_SUBMISSION_TOKENS = (
    "Submission Format Route",
    "primary submission file",
    "selected reporting checklist",
    "Actual main-text word count",
    "draft length gate:",
    "visual display gate:",
    "table aesthetics gate:",
    "format-specific production gate:",
    "local_path_leak_status:",
    "Citation audit status:",
    "statement status:",
    "Submission-readiness verdict:",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_field(text: str, label: str) -> str:
    pattern = re.compile(rf"(?im)^\s*{re.escape(label)}\s*[:=]\s*(.+?)\s*$")
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def normalize_status(value: str) -> str:
    upper = value.upper()
    if "PASS" in upper:
        return "PASS"
    if "BLOCKED" in upper:
        return "BLOCKED"
    if "FAIL" in upper:
        return "FAIL"
    return "UNKNOWN"


def extract_int(value: str) -> int | None:
    match = re.search(r"\b(\d{1,5})\b", value)
    return int(match.group(1)) if match else None


def extract_main_text_budget(text: str) -> tuple[int, int] | None:
    """Return the first plausible main-text word budget range in the package text."""
    for match in re.finditer(
        r"(?<!\d)([1-9]\d{3,4})\s*[-–]\s*([1-9]\d{3,4})\s*(?:main[- ]text\s*)?words?\b",
        text,
        flags=re.IGNORECASE,
    ):
        lower = int(match.group(1))
        upper = int(match.group(2))
        if 1000 <= lower <= upper:
            return lower, upper
    return None


def validate_workflow_state(paper: Path, errors: list[str]) -> dict[str, Any] | None:
    state_path = paper / "workflow-state.json"
    if not state_path.exists():
        return None
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError as exc:
        errors.append(f"workflow-state.json is invalid JSON: {exc}")
        return None
    for field in REQUIRED_STATE_FIELDS:
        if field not in state:
            errors.append(f"workflow-state.json missing required field: {field}")
    if state.get("schema_version") != "medicine-workflow-state-v1":
        errors.append("workflow-state.json schema_version must be medicine-workflow-state-v1")
    if not isinstance(state.get("policy_confirmed"), bool):
        errors.append("workflow-state.json policy_confirmed must be boolean")
    if not isinstance(state.get("framework_confirmed"), bool):
        errors.append("workflow-state.json framework_confirmed must be boolean")
    for field in ("required_displays", "required_audits", "blocking_gaps"):
        if field in state and not isinstance(state[field], list):
            errors.append(f"workflow-state.json {field} must be a list")
    return state


def validate_submission_text(paper: Path, text: str, state: dict[str, Any] | None, errors: list[str]) -> str:
    for token in REQUIRED_SUBMISSION_TOKENS:
        if token not in text:
            errors.append(f"submission-package.md missing required field: {token}")

    route = extract_field(text, "Submission Format Route") or (state or {}).get("submission_format_route", "")
    primary_file = extract_field(text, "primary submission file") or (state or {}).get("primary_submission_file", "")
    production_status = normalize_status(extract_field(text, "format-specific production gate"))
    draft_length_status = normalize_status(extract_field(text, "draft length gate"))
    actual_word_count = extract_int(extract_field(text, "Actual main-text word count"))
    main_text_budget = extract_main_text_budget(text)
    local_path_status = extract_field(text, "local_path_leak_status").lower()
    verdict_status = normalize_status(extract_field(text, "Submission-readiness verdict"))

    route_lower = str(route).lower()
    primary_path = paper / str(primary_file).removeprefix("paper/")

    if "word-first" in route_lower:
        if not primary_file:
            errors.append("word-first route requires primary submission file")
        if primary_file and primary_path.name != "manuscript.docx":
            errors.append("word-first route primary submission file must be manuscript.docx")
        if production_status == "PASS" and not (paper / "manuscript.docx").exists():
            errors.append("word-first route requires manuscript.docx before format-specific production gate can PASS")
    elif "latex-first" in route_lower:
        if production_status == "PASS" and not (paper / "main.pdf").exists():
            errors.append("latex-first route requires main.pdf before format-specific production gate can PASS")
    elif "generic-review" in route_lower:
        if verdict_status == "PASS" or re.search(r"(?i)\bsubmission-ready\b", text):
            errors.append("generic-review route must not be called submission-ready")
    elif route:
        errors.append(f"unknown Submission Format Route: {route}")
    else:
        errors.append("missing Submission Format Route")

    if "pass" not in local_path_status:
        errors.append("local_path_leak_status must be pass before package return")

    if draft_length_status == "PASS" and actual_word_count is not None and main_text_budget is not None:
        lower, upper = main_text_budget
        if actual_word_count < lower or actual_word_count > upper:
            errors.append(
                "draft length gate cannot PASS when Actual main-text word count "
                f"{actual_word_count} is outside the recorded {lower}-{upper} word budget"
            )

    return "PASS" if verdict_status == "PASS" else "BLOCKED"


def audit_package(paper: Path) -> dict[str, Any]:
    errors: list[str] = []
    if not paper.exists() or not paper.is_dir():
        return {"overall_status": "FAIL", "errors": [f"paper directory not found: {paper}"]}

    submission_path = paper / "submission-package.md"
    if not submission_path.exists():
        return {"overall_status": "FAIL", "errors": ["missing submission-package.md"]}

    state = validate_workflow_state(paper, errors)
    text = read_text(submission_path)
    readiness_status = validate_submission_text(paper, text, state, errors)

    return {
        "overall_status": "FAIL" if errors else readiness_status,
        "submission_readiness_verdict": readiness_status,
        "workflow_state_present": state is not None,
        "errors": errors,
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"overall_status: {report['overall_status']}")
    print(f"submission_readiness_verdict: {report.get('submission_readiness_verdict', 'UNKNOWN')}")
    print(f"workflow_state_present: {str(report.get('workflow_state_present', False)).lower()}")
    for error in report.get("errors", []):
        print(f"ERROR: {error}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--require-submission-ready", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = audit_package(args.paper)
    if args.require_submission_ready and report["overall_status"] != "PASS":
        report.setdefault("errors", []).append("--require-submission-ready requested but verdict is not PASS")
        report["overall_status"] = "FAIL"
    if args.json_path:
        args.json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print_report(report)
    return 1 if report["overall_status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
