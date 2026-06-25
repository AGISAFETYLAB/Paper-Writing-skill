#!/usr/bin/env python3
"""Audit Python plotting scripts for academic-figure palette compliance.

Generated CS plotting code should use registered CS_* palettes from cs_palette.py
instead of ad hoc color cycles or unregistered hex colors.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from pathlib import Path

import cs_palette


HEX_RE = re.compile(r"(?i)(?<![A-Za-z0-9_])#[0-9a-f]{6}\b")
PLOT_HINTS = (
    "plt.",
    "ax.",
    ".plot(",
    ".bar(",
    ".scatter(",
    ".fill(",
    ".fill_between(",
    ".imshow(",
    ".pcolormesh(",
    "seaborn",
    "sns.",
)
BANNED_COLOR_CYCLES = (
    "tab10",
    "tab20",
    "jet",
    "rainbow",
    "gist_rainbow",
    "nipy_spectral",
)
ALWAYS_ALLOWED_HEX = {
    "#000000",
    "#FFFFFF",
    "#F5F5F5",
}


def _flatten_colors(value: object) -> Iterable[str]:
    if isinstance(value, str):
        if HEX_RE.fullmatch(value):
            yield value.upper()
        return
    if isinstance(value, dict):
        for item in value.values():
            yield from _flatten_colors(item)
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _flatten_colors(item)


def registered_hex_colors() -> set[str]:
    colors: set[str] = set(ALWAYS_ALLOWED_HEX)
    for name in dir(cs_palette):
        if name.startswith("CS_"):
            colors.update(_flatten_colors(getattr(cs_palette, name)))
    return colors


def registered_palette_names() -> tuple[str, ...]:
    return tuple(name for name in dir(cs_palette) if name.startswith("CS_"))


def iter_python_files(paths: list[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*.py") if p.is_file())
        elif path.is_file() and path.suffix == ".py":
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def looks_like_plot_script(text: str) -> bool:
    return any(hint in text for hint in PLOT_HINTS) or bool(HEX_RE.search(text))


def audit_file(path: Path, approved_hex: set[str], palette_names: tuple[str, ...]) -> list[str]:
    if path.name in {"audit_plot_palettes.py", "cs_palette.py"}:
        return []

    text = read_text(path)
    if not looks_like_plot_script(text):
        return []

    errors: list[str] = []
    if "cs_palette" not in text and not any(name in text for name in palette_names):
        errors.append("missing registered CS_* palette reference or cs_palette import")

    for raw_hex in sorted(set(match.group(0).upper() for match in HEX_RE.finditer(text))):
        if raw_hex not in approved_hex:
            errors.append(f"unregistered hex color {raw_hex}")

    lowered = text.lower()
    for banned in BANNED_COLOR_CYCLES:
        if re.search(rf"['\"]{re.escape(banned.lower())}['\"]", lowered):
            errors.append(f"banned/default color cycle or colormap {banned!r}")

    if "sns.color_palette(" in text and "CS_" not in text:
        errors.append("seaborn color_palette used without registered CS_* colors")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Python plotting scripts or directories")
    args = parser.parse_args(argv)

    files = list(iter_python_files(args.paths))
    if not files:
        print("No Python files found.", file=sys.stderr)
        return 2

    approved_hex = registered_hex_colors()
    palette_names = registered_palette_names()
    failures: list[tuple[Path, list[str]]] = []
    checked = 0

    for path in files:
        text = read_text(path)
        if not looks_like_plot_script(text):
            continue
        checked += 1
        errors = audit_file(path, approved_hex, palette_names)
        if errors:
            failures.append((path, errors))

    if failures:
        for path, errors in failures:
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        return 1

    print(f"PASS palette audit: {checked} plotting script(s) checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
