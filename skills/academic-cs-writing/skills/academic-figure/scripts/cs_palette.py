"""Canonical CS manuscript palettes for academic-figure generated plots.

This module is the executable companion to references/figures/palette-system.md.
Generated plotting scripts should import or mirror these names instead of
creating unnamed raw-hex palettes.
"""

from __future__ import annotations

from dataclasses import dataclass


CS_PEER_PALETTE = (
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
)
CS_PEER_MARKERS = ("o", "s", "^", "D", "v", "P")

CS_BODY_PASTEL_PALETTE = (
    "#C7D7EA",
    "#8FB3D1",
    "#5F8FB8",
    "#D07A68",
    "#D8C7DD",
    "#C9D8C5",
)

CS_HERO_COLOR = "#3775BA"
CS_BASELINE_PALETTE = (
    "#CFCECE",
    "#DDF3DE",
    "#FBDFE2",
    "#D9B9D4",
    "#DAA87C",
    "#B4C0E4",
)
CS_HERO_BASELINE_PALETTE = CS_BASELINE_PALETTE + (CS_HERO_COLOR,)

CS_COVERAGE_PALETTE = (
    "#4B8BBE",
    "#6BA3CF",
    "#8FBCDB",
    "#E3A86D",
    "#E08F72",
    "#7DBD9C",
    "#B1A1C8",
)

CS_PAIRED_OPPOSING_PALETTE = {
    "lower_better": "#C97B6B",
    "higher_better": "#5E8FB8",
}

CS_RADAR_PALETTE = (
    "#C97B6B",
    "#5E8FB8",
    "#5DA88A",
    "#D4A64E",
    "#8E7FB8",
    "#9B9B9B",
)
CS_RADAR_MARKERS = ("o", "s", "^", "D", "o", "s")
CS_RADAR_LINESTYLES = (
    "-",
    "-",
    (0, (6, 3)),
    (0, (6, 3)),
    (0, (2, 2)),
    (0, (2, 2)),
)
CS_RADAR_TICKS = (20, 40, 60, 80)
CS_RADAR_GRID_LINESTYLE = (0, (5, 5))
CS_RADAR_FILL_ALPHA = 0.04
CS_RADAR_LINEWIDTH = 1.8
CS_RADAR_MARKERSIZE = 5.0
CS_RADAR_MARKER_EDGEWIDTH = 1.5
CS_RADAR_TITLE_COLOR = "#333333"
CS_RADAR_LABEL_COLOR = "#2C3E50"
CS_RADAR_GRID_COLOR = "#E0E0E0"
CS_RADAR_OUTER_RING_COLOR = "#666666"
CS_RADAR_TICK_COLOR = "#999999"
CS_RADAR_CENTER_DOT_COLOR = "#AAAAAA"

CS_QUALITATIVE_PANEL_PALETTE = {
    "frame": "#D8D8D8",
    "text": "#4D4D4D",
    "focus": "#5E8FB8",
    "warning": "#C97B6B",
    "success": "#5DA88A",
    "neutral_fill": "#F5F5F5",
}

CS_SUPPORT_COLORS = {
    "text": "#333333",
    "text_soft": "#3A3A3A",
    "text_muted": "#666666",
    "text_light": "#9A9A9A",
    "axis": "#4D4D4D",
    "edge": "#4D4D4D",
    "grid": "#E0E0E0",
    "neutral_mid": "#767676",
    "neutral_light": "#D8D8D8",
    "radar_label": "#2C3E50",
    "radar_title": "#333333",
    "radar_grid": "#E0E0E0",
    "radar_outer_ring": "#666666",
    "radar_tick": "#999999",
    "radar_center_dot": "#AAAAAA",
    "paired_lower_edge": "#A96A5D",
    "paired_higher_edge": "#4D789B",
    "donut_leader": "#B8B8B8",
    "delta_up": "#2E9E44",
    "delta_down": "#E53935",
}

CS_HATCHES = ("/", "\\", ".", "x", "o", "+")


@dataclass(frozen=True)
class PaletteFamily:
    name: str
    colors: tuple[str, ...]
    role: str
    markers: tuple[str, ...] = ()
    linestyles: tuple[object, ...] = ()


CS_PALETTE_FAMILIES: dict[str, PaletteFamily] = {
    "peer": PaletteFamily("CS_PEER_PALETTE", CS_PEER_PALETTE, "equal-status categories", CS_PEER_MARKERS),
    "body_pastel": PaletteFamily("CS_BODY_PASTEL_PALETTE", CS_BODY_PASTEL_PALETTE, "quiet grouped body figures"),
    "hero_baseline": PaletteFamily("CS_HERO_BASELINE_PALETTE", CS_HERO_BASELINE_PALETTE, "one focus entity versus baselines"),
    "coverage": PaletteFamily("CS_COVERAGE_PALETTE", CS_COVERAGE_PALETTE, "whole-part coverage or composition"),
    "paired_opposing": PaletteFamily(
        "CS_PAIRED_OPPOSING_PALETTE",
        tuple(CS_PAIRED_OPPOSING_PALETTE.values()),
        "paired foreground metrics with opposite direction",
    ),
    "radar": PaletteFamily("CS_RADAR_PALETTE", CS_RADAR_PALETTE, "single-panel or shared-legend radar comparisons", CS_RADAR_MARKERS, CS_RADAR_LINESTYLES),
    "qualitative_panel": PaletteFamily(
        "CS_QUALITATIVE_PANEL_PALETTE",
        tuple(CS_QUALITATIVE_PANEL_PALETTE.values()),
        "qualitative panels and annotation frames",
    ),
}

CS_DISPLAY_PALETTE_DEFAULTS: dict[str, str] = {
    "bar": "hero_baseline",
    "grouped_bar": "body_pastel",
    "stacked_bar": "coverage",
    "line": "peer",
    "scatter": "peer",
    "pareto": "peer",
    "radar": "radar",
    "composition": "coverage",
    "qualitative": "qualitative_panel",
    "paired_scorecard": "paired_opposing",
}

MIN_CATEGORICAL_LUMINANCE = 0.06
_CATEGORICAL_FAMILIES = ("peer", "body_pastel", "hero_baseline", "coverage", "paired_opposing", "radar")


def get_palette_family(name: str) -> PaletteFamily:
    try:
        return CS_PALETTE_FAMILIES[name]
    except KeyError as exc:
        valid = ", ".join(sorted(CS_PALETTE_FAMILIES))
        raise ValueError(f"unknown CS palette family {name!r}; expected one of: {valid}") from exc


def colors_for_display(display_family: str, palette_family: str | None = None) -> tuple[str, ...]:
    family_name = palette_family or CS_DISPLAY_PALETTE_DEFAULTS.get(display_family, "peer")
    return get_palette_family(family_name).colors


def relative_luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    red, green, blue = (int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(value: float) -> float:
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def overly_dark_categorical_colors(family: str | None = None) -> tuple[str, ...]:
    family_names = (family,) if family else _CATEGORICAL_FAMILIES
    colors: list[str] = []
    for family_name in family_names:
        colors.extend(get_palette_family(family_name).colors)
    return tuple(color for color in colors if relative_luminance(color) <= MIN_CATEGORICAL_LUMINANCE)
