"""Canonical finance manuscript palettes for generated figures.

This module is the executable companion to references/finance-palette.md.
Generated Python plotting scripts should import or mirror these names instead
of creating unnamed raw-hex palettes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FinancePaletteProfile:
    name: str
    tokens: dict[str, str]
    role: str
    reference_style: str
    categorical_order: tuple[str, ...]
    small_n_order: tuple[str, ...]
    sequential: tuple[str, ...]
    diverging: tuple[str, ...]


FINANCE_MUTED = FinancePaletteProfile(
    name="finance-muted",
    role="default restrained teal-warm finance manuscript palette",
    reference_style="teal, sage, sand, gold, and muted red/brown reference style",
    tokens={
        "primary": "#4EAB90",
        "secondary": "#8EB69C",
        "accent": "#D94F33",
        "warm": "#EEBF6D",
        "support": "#EDDCC3",
        "deep": "#834026",
        "sand": "#EED5B7",
        "mist": "#ECF6FD",
        "blush": "#FEEEED",
        "neutral_text": "#2F3540",
        "neutral_grid": "#D9DCE1",
        "neutral_muted": "#6B7280",
    },
    categorical_order=("primary", "secondary", "warm", "support", "accent", "deep"),
    small_n_order=("primary", "secondary", "warm", "support", "accent"),
    sequential=("#ECF6FD", "#ABD8E5", "#8EB69C", "#4EAB90"),
    diverging=("#D94F33", "#FEEEED", "#5094D5"),
)


FINANCE_SOFT_CONTRAST = FinancePaletteProfile(
    name="finance-soft-contrast",
    role="soft blue/red/gold profile for model comparisons and diagnostics",
    reference_style="muted red, steel blue, soft lavender, gold, and pale blue reference style",
    tokens={
        "primary": "#5E82A2",
        "secondary": "#BFC7E5",
        "accent": "#D15354",
        "warm": "#E8B86C",
        "support": "#ABD8E5",
        "deep": "#8887CB",
        "sand": "#F9AD95",
        "mist": "#ECF6FD",
        "blush": "#FEEEED",
        "neutral_text": "#2F3540",
        "neutral_grid": "#D9DCE1",
        "neutral_muted": "#6B7280",
    },
    categorical_order=("primary", "support", "warm", "secondary", "accent", "deep"),
    small_n_order=("primary", "support", "warm", "secondary", "accent"),
    sequential=("#ECF6FD", "#ABD8E5", "#BFC7E5", "#5E82A2"),
    diverging=("#D15354", "#FEEEED", "#5094D5"),
)


FINANCE_WARM_DEEP = FinancePaletteProfile(
    name="finance-warm-deep",
    role="teal, warm, and deep-plum finance palette for richer composites",
    reference_style="earthy teal, gray-sage, terracotta, peach, sand, and plum reference style",
    tokens={
        "primary": "#44757A",
        "secondary": "#B7B5A0",
        "accent": "#D44C3C",
        "warm": "#DD6C4C",
        "support": "#E5855D",
        "deep": "#452A3D",
        "sand": "#EED5B7",
        "mist": "#F7F1E8",
        "blush": "#FCEAE6",
        "neutral_text": "#2F3540",
        "neutral_grid": "#D9DCE1",
        "neutral_muted": "#6B7280",
    },
    categorical_order=("primary", "secondary", "sand", "support", "warm", "accent", "deep"),
    small_n_order=("primary", "secondary", "sand", "support", "warm", "accent"),
    sequential=("#F7F1E8", "#EED5B7", "#B7B5A0", "#44757A"),
    diverging=("#D44C3C", "#F7F1E8", "#44757A"),
)


FINANCE_PALETTE_PROFILES: dict[str, FinancePaletteProfile] = {
    FINANCE_MUTED.name: FINANCE_MUTED,
    FINANCE_SOFT_CONTRAST.name: FINANCE_SOFT_CONTRAST,
    FINANCE_WARM_DEEP.name: FINANCE_WARM_DEEP,
}

DEFAULT_PROFILE = "finance-muted"
MAX_DARK_CATEGORICAL_LUMINANCE = 0.12
FEW_COLOR_LIMIT = 4


SEMANTIC_ROLE_TOKENS: dict[str, str] = {
    "treatment": "primary",
    "focal": "primary",
    "portfolio_1": "primary",
    "benchmark": "secondary",
    "control": "support",
    "comparison": "secondary",
    "risk": "accent",
    "loss": "accent",
    "drawdown": "accent",
    "rejection": "accent",
    "cost": "warm",
    "capacity": "warm",
    "event_window": "sand",
    "confidence_band": "mist",
    "negative_background": "blush",
    "text": "neutral_text",
    "grid": "neutral_grid",
}


DISPLAY_ROLE_DEFAULTS: dict[str, tuple[str, ...]] = {
    "event-study figure": ("primary", "secondary", "sand"),
    "parallel-trends plot": ("primary", "secondary", "sand"),
    "coefficient plot": ("primary", "secondary", "accent"),
    "cumulative abnormal return plot": ("primary", "secondary", "mist"),
    "long-short cumulative return curve": ("primary", "secondary", "warm"),
    "portfolio backtest curve": ("primary", "secondary", "warm"),
    "backtest performance panel": ("primary", "secondary", "accent", "warm"),
    "drawdown and turnover plot": ("accent", "warm", "secondary"),
    "risk-return scatter": ("primary", "secondary", "warm", "support"),
    "factor exposure/beta heatmap": ("sequential",),
    "robustness grid": ("diverging",),
    "robustness table": ("primary", "secondary", "accent"),
    "heatmap or bubble matrix": ("sequential",),
    "geographic exposure map": ("sequential",),
    "risk": ("accent",),
}


def get_palette_profile(name: str = DEFAULT_PROFILE) -> FinancePaletteProfile:
    try:
        return FINANCE_PALETTE_PROFILES[name]
    except KeyError as exc:
        valid = ", ".join(sorted(FINANCE_PALETTE_PROFILES))
        raise ValueError(f"unknown finance palette profile {name!r}; expected one of: {valid}") from exc


def role_color(role: str, profile_name: str = DEFAULT_PROFILE) -> str:
    profile = get_palette_profile(profile_name)
    token = SEMANTIC_ROLE_TOKENS.get(role, role)
    try:
        return profile.tokens[token]
    except KeyError as exc:
        valid = ", ".join(sorted(profile.tokens))
        raise ValueError(f"unknown finance palette role/token {role!r}; expected one of: {valid}") from exc


def categorical_colors(
    n: int,
    profile_name: str = DEFAULT_PROFILE,
    *,
    include_deep: bool = False,
) -> tuple[str, ...]:
    """Return categorical colors with a small-N dark-color safeguard.

    For few-color charts (n <= 4), the deep token is skipped by default. Deep
    colors remain available for text, sparse high-contrast lines, network nodes,
    or charts with many categories where the manuscript explicitly needs them.
    """

    if n < 0:
        raise ValueError("n must be non-negative")
    profile = get_palette_profile(profile_name)
    order = profile.categorical_order if include_deep or n > FEW_COLOR_LIMIT else profile.small_n_order
    colors = [profile.tokens[token] for token in order]
    if not include_deep and n <= FEW_COLOR_LIMIT:
        colors = [color for color in colors if color != profile.tokens.get("deep")]
    if n <= len(colors):
        return tuple(colors[:n])
    repeated = []
    while len(repeated) < n:
        repeated.extend(colors)
    return tuple(repeated[:n])


def colors_for_display(
    display_family: str,
    n: int | None = None,
    profile_name: str = DEFAULT_PROFILE,
) -> tuple[str, ...]:
    roles = DISPLAY_ROLE_DEFAULTS.get(display_family)
    if roles is None:
        return categorical_colors(n or 6, profile_name)
    if roles == ("sequential",):
        return sequential_colors(profile_name)
    if roles == ("diverging",):
        return diverging_colors(profile_name)
    colors = tuple(role_color(role, profile_name) for role in roles)
    return colors[:n] if n is not None else colors


def sequential_colors(profile_name: str = DEFAULT_PROFILE) -> tuple[str, ...]:
    return get_palette_profile(profile_name).sequential


def diverging_colors(profile_name: str = DEFAULT_PROFILE) -> tuple[str, ...]:
    return get_palette_profile(profile_name).diverging


def relative_luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    red, green, blue = (int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(value: float) -> float:
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def overly_dark_categorical_tokens(profile_name: str = DEFAULT_PROFILE) -> tuple[str, ...]:
    profile = get_palette_profile(profile_name)
    return tuple(
        token
        for token in profile.categorical_order
        if relative_luminance(profile.tokens[token]) <= MAX_DARK_CATEGORICAL_LUMINANCE
    )


def palette_audit(profile_name: str = DEFAULT_PROFILE) -> dict[str, object]:
    profile = get_palette_profile(profile_name)
    return {
        "profile": profile.name,
        "reference_style": profile.reference_style,
        "dark_categorical_tokens": overly_dark_categorical_tokens(profile.name),
        "small_n_order": profile.small_n_order,
        "categorical_order": profile.categorical_order,
    }
