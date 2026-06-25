#!/usr/bin/env python3
"""Audit finance figure image assets for obvious export defects."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
IGNORED_DIRS = {".git", "__pycache__", "layout-qa", "build", "_minted"}


@dataclass(frozen=True)
class VisualAssetFinding:
    path: Path
    code: str
    message: str


def iter_image_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in IMAGE_SUFFIXES:
            yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in IMAGE_SUFFIXES:
            yield path


def public_path(path: Path) -> str:
    parts = path.parts
    if "paper" in parts:
        return "/".join(parts[parts.index("paper") :])
    return str(path)


def audit_image(path: Path, edge_margin: int = 6, ink_threshold: int = 245) -> list[VisualAssetFinding]:
    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover - environment dependent
        return [
            VisualAssetFinding(
                path,
                "pillow_unavailable",
                f"Pillow import failed; cannot inspect raster preview assets: {exc}",
            )
        ]

    findings: list[VisualAssetFinding] = []
    try:
        image = Image.open(path).convert("RGBA")
    except Exception as exc:
        return [VisualAssetFinding(path, "image_open_failed", f"could not open image asset: {exc}")]

    width, height = image.size
    pixels = image.load()
    min_x, min_y = width, height
    max_x, max_y = -1, -1
    ink_count = 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if min(r, g, b) < ink_threshold:
                ink_count += 1
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if ink_count == 0:
        findings.append(VisualAssetFinding(path, "blank_preview", "image contains no visible non-white content"))
        return findings

    edge_hits: list[str] = []
    if min_x <= edge_margin:
        edge_hits.append("left")
    if min_y <= edge_margin:
        edge_hits.append("top")
    if width - 1 - max_x <= edge_margin:
        edge_hits.append("right")
    if height - 1 - max_y <= edge_margin:
        edge_hits.append("bottom")
    if edge_hits:
        findings.append(
            VisualAssetFinding(
                path,
                "content_near_edge",
                "visible content touches or nearly touches image edge(s): "
                + ", ".join(edge_hits)
                + "; likely cropped title, axis label, legend, or panel annotation",
            )
        )

    content_width = max_x - min_x + 1
    content_height = max_y - min_y + 1
    if content_width < width * 0.25 or content_height < height * 0.25:
        findings.append(
            VisualAssetFinding(
                path,
                "dominant_unused_margin",
                "visible content occupies less than one quarter of image width or height",
            )
        )

    return findings


def find_visual_asset_findings(root: Path | str) -> list[VisualAssetFinding]:
    root_path = Path(root)
    findings: list[VisualAssetFinding] = []
    for path in iter_image_files(root_path):
        findings.extend(audit_image(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit finance figure image assets for export QA defects.")
    parser.add_argument("path", type=Path, help="Paper directory, figures directory, or image file")
    args = parser.parse_args()

    findings = find_visual_asset_findings(args.path)
    if findings:
        for finding in findings:
            print(f"{public_path(finding.path)}: {finding.code}: {finding.message}")
        print(f"FAIL finance visual asset QA: {len(findings)} finding(s)")
        return 1
    print("PASS finance visual asset QA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
