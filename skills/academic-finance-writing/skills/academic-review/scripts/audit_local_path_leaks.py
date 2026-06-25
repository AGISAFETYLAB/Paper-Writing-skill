#!/usr/bin/env python3
"""Audit finance paper artifacts for leaked local workspace paths."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import NamedTuple


TEXT_SUFFIXES = {
    ".aux",
    ".bbl",
    ".bib",
    ".csv",
    ".json",
    ".md",
    ".tex",
    ".txt",
    ".yaml",
    ".yml",
}
DOCX_XML_PREFIXES = ("word/", "docProps/")
# Examples blocked: /mnt/, /home/, /Users/, C:\\Users\\
FORBIDDEN_LOCAL_PATH_RE = re.compile(
    r"(?P<forbidden_local_path>"
    r"(?:/mnt|/home|/Users)/[^\s\"'<>)}\]]+"
    r"|[A-Za-z]:\\\\Users\\\\[^\s\"'<>)}\]]+"
    r")"
)


class Leak(NamedTuple):
    path: Path
    line: int
    match: str
    kind: str


def public_artifact_path(path: Path) -> str:
    parts = path.parts
    if "paper" in parts:
        return "/".join(parts[parts.index("paper") :])
    return path.name


def redacted_match(value: str) -> str:
    if value.startswith(("/mnt/", "/home/", "/Users/")) or re.match(r"^[A-Za-z]:\\\\Users\\\\", value):
        return "[absolute local path redacted]"
    return value


def text_leaks(path: Path, text: str, kind: str) -> list[Leak]:
    leaks: list[Leak] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for match in FORBIDDEN_LOCAL_PATH_RE.finditer(line):
            leaks.append(Leak(path=path, line=line_number, match=match.group("forbidden_local_path"), kind=kind))
    return leaks


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def docx_text(path: Path) -> str:
    chunks: list[str] = []
    try:
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                if name.endswith(".xml") and name.startswith(DOCX_XML_PREFIXES):
                    chunks.append(zf.read(name).decode("utf-8", errors="ignore"))
    except zipfile.BadZipFile:
        return ""
    return "\n".join(chunks)


def pdf_text(path: Path) -> str:
    if shutil.which("pdftotext") is None:
        return ""
    proc = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc.stdout if proc.returncode == 0 else ""


def find_local_path_leaks(root: Path) -> list[Leak]:
    leaks: list[Leak] = []
    files = [root] if root.is_file() else [path for path in root.rglob("*") if path.is_file()]
    for path in files:
        suffix = path.suffix.lower()
        if suffix in TEXT_SUFFIXES:
            leaks.extend(text_leaks(path, read_text_file(path), "text"))
        elif suffix == ".docx":
            leaks.extend(text_leaks(path, docx_text(path), "docx_xml"))
        elif suffix == ".pdf":
            leaks.extend(text_leaks(path, pdf_text(path), "pdf_text"))
    return leaks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    leaks = find_local_path_leaks(args.paper_dir)
    payload = {
        "status": "BLOCKED" if leaks else "PASS",
        "leaks": [
            {
                "path": public_artifact_path(leak.path),
                "line": leak.line,
                "match": redacted_match(leak.match),
                "kind": leak.kind,
            }
            for leak in leaks
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if leaks:
            print("FAIL finance local path leak audit")
            for leak in leaks:
                print(
                    f"{public_artifact_path(leak.path)}:{leak.line}: "
                    f"forbidden_local_path: {redacted_match(leak.match)}"
                )
        else:
            print("PASS finance local path leak audit")
    return 1 if leaks else 0


if __name__ == "__main__":
    raise SystemExit(main())
