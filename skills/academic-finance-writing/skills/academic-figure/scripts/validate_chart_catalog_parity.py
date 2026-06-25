#!/usr/bin/env python3
"""Validate that finance R and Python chart catalogs expose the same families."""

from __future__ import annotations

import argparse
from pathlib import Path


MIN_DISPLAY_FAMILIES = 36


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def extract_display_families(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)

    families: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        first = cells[0]
        if first in {"Display family", "---"} or set(first) <= {"-", ":"}:
            continue
        families.append(first)
    return families


def compare_catalogs(root: Path) -> tuple[list[str], list[str]]:
    r_catalog = root / "references/r-chart-catalog.md"
    python_catalog = root / "references/python-chart-catalog.md"
    return extract_display_families(r_catalog), extract_display_families(python_catalog)


def format_diff(r_families: list[str], python_families: list[str]) -> str:
    r_set = set(r_families)
    python_set = set(python_families)
    missing_in_python = sorted(r_set - python_set)
    missing_in_r = sorted(python_set - r_set)

    lines: list[str] = []
    if missing_in_python:
        lines.append("Families present in R but missing in Python:")
        lines.extend(f"  - {name}" for name in missing_in_python)
    if missing_in_r:
        lines.append("Families present in Python but missing in R:")
        lines.extend(f"  - {name}" for name in missing_in_r)
    if not missing_in_python and not missing_in_r:
        lines.append("Catalogs contain the same names but in a different order.")
        for index, (r_name, py_name) in enumerate(zip(r_families, python_families), start=1):
            if r_name != py_name:
                lines.append(f"  row {index}: R={r_name!r}; Python={py_name!r}")
                break
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=package_root(),
        help="academic-figure skill root",
    )
    parser.add_argument(
        "--min-families",
        type=int,
        default=MIN_DISPLAY_FAMILIES,
        help="minimum shared display families expected after broad finance coverage expansion",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    r_families, python_families = compare_catalogs(root)

    if r_families != python_families:
        print("FAIL: R and Python chart catalogs are not aligned")
        print(format_diff(r_families, python_families))
        return 1

    if len(r_families) < args.min_families:
        print(
            "FAIL: finance chart catalog is too narrow: "
            f"{len(r_families)} shared display families; expected at least {args.min_families}"
        )
        return 1

    print(f"PASS chart catalog parity: {len(r_families)} shared display families")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
