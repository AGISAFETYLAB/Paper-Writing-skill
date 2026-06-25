"""Shared restrained medical manuscript palettes for skill-generated figures.

The medicine skill uses one visual style per manuscript, not one literal color
list for every chart.  Named palette families keep figures coherent while still
letting bars, curves, heatmaps, risk maps, and imaging composites use colors
suited to their job.
"""

from __future__ import annotations

from dataclasses import dataclass

from matplotlib.colors import LinearSegmentedColormap, ListedColormap


TEXT = "#1F2933"
GRAY = "#716D66"
MID_GRAY = "#B8B1A5"
LIGHT_GRAY = "#E1DDD4"
PAPER = "#FAF8F2"
GRID = "#E6E1D7"

BAR_EDGE = "#62584F"
MAX_DARK_MARK_LUMINANCE = 0.05


@dataclass(frozen=True)
class PaletteFamily:
    """Complete color family for a manuscript or figure group."""

    name: str
    group: tuple[str, ...]
    contrast: tuple[str, ...]
    sequential: tuple[str, ...]
    diverging: tuple[str, ...]
    missingness: tuple[str, ...]
    risk_bias: tuple[str, ...]
    edge: str = BAR_EDGE


PALETTE_FAMILIES: dict[str, PaletteFamily] = {
    "teal_warm": PaletteFamily(
        name="teal_warm",
        group=("#4EAB90", "#8EB69C", "#EDDCC3", "#EEBF6D", "#D94F33", "#834026"),
        contrast=("#4EAB90", "#44757A", "#EEBF6D", "#D94F33", "#834026"),
        sequential=(PAPER, "#EDDCC3", "#B7C8B6", "#44757A"),
        diverging=("#D94F33", "#F3EAD8", "#44757A"),
        missingness=("#FFFFFF", "#746F68"),
        risk_bias=("#8EB69C", "#EEBF6D", "#D94F33"),
    ),
    "deep_teal_coral": PaletteFamily(
        name="deep_teal_coral",
        group=("#4F8589", "#8A6B7B", "#D44C3C", "#E5855B", "#B7B5A0", "#EDD5B7"),
        contrast=("#4F8589", "#8A6B7B", "#D44C3C", "#E5855B", "#EDD5B7"),
        sequential=("#FAF8F2", "#EDD5B7", "#B7B5A0", "#4F8589"),
        diverging=("#D44C3C", "#F4E6D2", "#4F8589"),
        missingness=("#FFFFFF", "#7B756C"),
        risk_bias=("#8EB69C", "#EEBF6D", "#C9644F"),
    ),
    "scientific_blue_red": PaletteFamily(
        name="scientific_blue_red",
        group=("#5E82A2", "#D15354", "#E8B86C", "#8887CB", "#5094D5", "#F9AD95"),
        contrast=("#5E82A2", "#5094D5", "#D15354", "#E8B86C", "#8887CB"),
        sequential=("#ECF6FD", "#BFC7E5", "#ABD8E5", "#5E82A2"),
        diverging=("#D15354", "#FEEEED", "#5094D5"),
        missingness=("#FFFFFF", "#6B7280"),
        risk_bias=("#8EB69C", "#E8B86C", "#D15354"),
    ),
}

DEFAULT_FAMILY = "teal_warm"

DISPLAY_PALETTE_DEFAULTS: dict[str, str] = {
    "bar": "teal_warm",
    "line": "scientific_blue_red",
    "distribution": "scientific_blue_red",
    "heatmap": "scientific_blue_red",
    "diagnostic": "scientific_blue_red",
    "survival": "scientific_blue_red",
    "effect_review": "scientific_blue_red",
    "flow": "teal_warm",
    "biomarker": "deep_teal_coral",
    "imaging": "teal_warm",
    "economic": "scientific_blue_red",
    "table": "teal_warm",
}


def get_palette_family(name: str = DEFAULT_FAMILY) -> PaletteFamily:
    try:
        return PALETTE_FAMILIES[name]
    except KeyError as exc:
        valid = ", ".join(sorted(PALETTE_FAMILIES))
        raise ValueError(f"unknown medical palette family {name!r}; expected one of: {valid}") from exc


def display_palette(display_family: str, manuscript_family: str | None = None) -> PaletteFamily:
    """Return the palette family for a chart family.

    `manuscript_family` lets a route force one family for a whole paper.  When it
    is absent, the skill picks a restrained family that fits the chart type.
    """

    family_name = manuscript_family or DISPLAY_PALETTE_DEFAULTS.get(display_family, DEFAULT_FAMILY)
    return get_palette_family(family_name)


def colors_for_display(display_family: str, manuscript_family: str | None = None) -> tuple[str, ...]:
    return display_palette(display_family, manuscript_family).group


def relative_luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    red, green, blue = (int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(value: float) -> float:
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def overly_dark_categorical_colors(family: str | None = None) -> tuple[str, ...]:
    palette = _family(family)
    return tuple(color for color in palette.group if relative_luminance(color) <= MAX_DARK_MARK_LUMINANCE)


def _family(name: str | None) -> PaletteFamily:
    return get_palette_family(name or DEFAULT_FAMILY)


DEFAULT_PALETTE = get_palette_family(DEFAULT_FAMILY)

BLUE = DEFAULT_PALETTE.group[0]
GREEN = DEFAULT_PALETTE.group[1]
CREAM = DEFAULT_PALETTE.group[2]
ORANGE = DEFAULT_PALETTE.group[3]
RED = DEFAULT_PALETTE.group[4]
PURPLE = DEFAULT_PALETTE.group[5]
TEAL = DEFAULT_PALETTE.contrast[1]
BROWN = DEFAULT_PALETTE.group[5]

GROUP_COLORS = DEFAULT_PALETTE.group
CONTRAST_GROUP_COLORS = DEFAULT_PALETTE.contrast
SEQUENTIAL_COLORS = DEFAULT_PALETTE.sequential
DIVERGING_COLORS = DEFAULT_PALETTE.diverging
MISSINGNESS_COLORS = DEFAULT_PALETTE.missingness
RISK_BIAS_COLORS = DEFAULT_PALETTE.risk_bias


def sequential_cmap(name: str = "medical_sequential", family: str | None = None) -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(name, _family(family).sequential)


def diverging_cmap(name: str = "medical_diverging", family: str | None = None) -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(name, _family(family).diverging)


def missingness_cmap(family: str | None = None) -> ListedColormap:
    return ListedColormap(_family(family).missingness)


def risk_bias_cmap(family: str | None = None) -> ListedColormap:
    return ListedColormap(_family(family).risk_bias)
