# Chart Code Patterns

Reusable Python/matplotlib patterns for generating publication-quality figures.
Load this file when the Figure Plan requires data-driven plots. Use the functions
below as implementation shortcuts; adapt colors, sizes, and labels to the active
Writing Policy.

## Contents

- Ownership boundary, mandatory setup, and palette mirrors
- Common helpers: luminance, save, grouped bars, trend lines, heatmap, radar
- Multi-panel helpers: shared legend radar, panel label, dedicated legend
- Expanded chart helpers: horizontal bars, paired scorecard, stacked bars, scatter, distribution,
  pie/donut, compact coverage donut

## Ownership Boundary

This file owns reusable Python/matplotlib helper functions only.
It does not own chart selection, palette policy, venue sizing, or figure planning.

## Mandatory Setup

Apply before any figure is created:

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})
```

## Color Palette

Choose the palette family from the **data structure** (see `plot-style.md` → Colors):
categorical/peer → `CS_PEER_PALETTE`; ordered magnitude → sequential ramp; signed →
diverging `RdBu_r`; one focus entity → hero-baseline. Never a rainbow/jet colormap, and
never hue as the only channel — pair categorical series with `CS_PEER_MARKERS` / `CS_HATCHES`.

Unless the user explicitly supplies a palette or asks to change colors, generated plotting code must
use these registered `CS_*` palettes by default. Import from `scripts/cs_palette.py` when possible;
if a paper-local script mirrors constants for portability, keep the names and hex values identical
and record the palette family in the execution report.

Palette constants below mirror palette-system.md and `scripts/cs_palette.py` for executable
snippets. The registry of approved palette names and hex values lives there; update those files
first and keep this code block in sync rather than inventing new palettes here.

```python
import numpy as np

# ── Categorical / peer palette — Okabe–Ito (colorblind-safe, luminance-balanced) ──
CS_PEER_PALETTE = [
    "#0072B2",   # blue
    "#D55E00",   # vermillion
    "#009E73",   # bluish green
    "#CC79A7",   # reddish purple
    "#E69F00",   # orange
    "#56B4E9",   # sky blue
]
CS_PEER_MARKERS = ['o', 's', '^', 'D', 'v', 'P']   # pair 1:1 with CS_PEER_PALETTE
CS_HATCHES      = ['/', '\\\\', '.', 'x', 'o', '+']  # bars/areas redundant channel

# ── Ordered magnitude — single-hue sequential ramp (low → high) ──
def sequential_ramp(n, cmap='Blues', lo=0.35, hi=0.95):
    return [plt.get_cmap(cmap)(t) for t in np.linspace(lo, hi, n)]

# ── Hero-Baseline (one proposed method vs muted baselines) ──
CS_HERO_COLOR = "#3775BA"
CS_BASELINE_PALETTE = [
    "#CFCECE", "#DDF3DE", "#FBDFE2", "#D9B9D4", "#DAA87C", "#B4C0E4",
]
CS_HERO_BASELINE_PALETTE = CS_BASELINE_PALETTE + [CS_HERO_COLOR]
CS_BODY_PASTEL_PALETTE = [
    "#C7D7EA", "#8FB3D1", "#5F8FB8", "#D07A68", "#D8C7DD", "#C9D8C5",
]
CS_COVERAGE_PALETTE = [  # style-reference ring/donut palette
    "#4B8BBE", "#6BA3CF", "#8FBCDB", "#E3A86D", "#E08F72", "#7DBD9C", "#B1A1C8",
]
CS_PAIRED_OPPOSING_PALETTE = {
    "lower_better": "#C97B6B",  # muted coral, for lower-is-better foreground metrics
    "higher_better": "#5E8FB8", # steel blue, for higher-is-better foreground metrics
}
CS_RADAR_PALETTE = [
    "#C97B6B", "#5E8FB8", "#5DA88A", "#D4A64E", "#8E7FB8", "#9B9B9B",
]
CS_RADAR_MARKERS = ['o', 's', '^', 'D', 'o', 's']
CS_RADAR_LINESTYLES = ['-', '-', (0, (6, 3)), (0, (6, 3)), (0, (2, 2)), (0, (2, 2))]
CS_RADAR_TICKS = [20, 40, 60, 80]
CS_RADAR_GRID_LINESTYLE = (0, (5, 5))
CS_RADAR_FILL_ALPHA = 0.04
CS_RADAR_LINEWIDTH = 1.8
CS_RADAR_MARKERSIZE = 5.0
CS_RADAR_MARKER_EDGEWIDTH = 1.5

# ── Delta markers (directional only, never entity identity) ──
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
CS_DELTA_UP = CS_SUPPORT_COLORS["delta_up"]
CS_DELTA_DOWN = CS_SUPPORT_COLORS["delta_down"]
```

---

## Helper: _luminance(hex_color)

```python
def _luminance(hex_color):
    """Return 0-255 perceptual luminance. White text on dark, black on light."""
    c = hex_color.lstrip('#')
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b
```

---

## Pattern: save_figure(fig, name, output_dir, formats=None)

```python
def save_figure(fig, name, output_dir, formats=None):
    """Save figure as SVG (primary), PDF, and PNG. Always close after saving."""
    if formats is None:
        formats = ['svg', 'pdf', 'png']
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    for fmt in formats:
        path = os.path.join(output_dir, f'{name}.{fmt}')
        if fmt == 'svg':
            fig.savefig(path, bbox_inches='tight')
        elif fmt == 'pdf':
            fig.savefig(path, bbox_inches='tight')
        elif fmt == 'png':
            fig.savefig(path, dpi=300, bbox_inches='tight')
        saved.append(path)
        print(f'Saved: {path}')
    plt.close(fig)
    return saved
```

---

## Pattern: grouped_bars(ax, categories, series, labels, colors, ...)

```python
def grouped_bars(ax, categories, series, labels, colors=None,
                 ylabel='', annotate=True, bar_width=0.8,
                 error_kw=None, fontsize=8, errors=None, dynamic_ylim=True,
                 hatches=None):
    """
    Grouped bar chart — publication style.

    Parameters
    ----------
    ax : matplotlib Axes
    categories : list[str]       — x-axis category names (length K)
    series : list[array]         — one array per group (each length K)
    labels : list[str]           — legend label per group
    colors : list[str] | None    — defaults to CS_PEER_PALETTE for equal-weight comparison; for
                                   journal grouped bars, prefer CS_BODY_PASTEL_PALETTE
    ylabel : str
    annotate : bool              — print value above each bar
    bar_width : float            — total width for all bars in one category
    error_kw : dict | None       — passed to ax.bar
    fontsize : int               — annotation font size
    errors : list | None         — per group, either array of symmetric errors
                                   (length K) or (lower, upper) arrays. Drives both
                                   the whiskers and the y-axis limits.
    dynamic_ylim : bool          — set an error-bar-aware y-axis (recommended)
    """
    if colors is None:
        colors = list(CS_PEER_PALETTE[:len(series)])
    if error_kw is None:
        error_kw = {'elinewidth': 1.5, 'capthick': 1.5, 'capsize': 4}

    n_groups = len(series)
    n_cats = len(categories)
    w = bar_width / n_groups
    x = np.arange(n_cats)

    tops, bots = [], []   # whisker extremes for ylim
    for i, (vals, label, color) in enumerate(zip(series, labels, colors)):
        vals = np.asarray(vals, dtype=float)
        offset = (i - (n_groups - 1) / 2) * w
        yerr = None
        lo_err = hi_err = np.zeros_like(vals)
        if errors is not None and errors[i] is not None:
            e = errors[i]
            if isinstance(e, (tuple, list)) and len(e) == 2 and np.ndim(e[0]) > 0:
                lo_err, hi_err = np.asarray(e[0]), np.asarray(e[1])
                yerr = [lo_err, hi_err]
            else:
                lo_err = hi_err = np.asarray(e)
                yerr = e
        hatch = hatches[i] if hatches is not None else None
        bars = ax.bar(x + offset, vals, width=w, label=label,
                      color=color, edgecolor=CS_SUPPORT_COLORS["edge"], linewidth=0.8,
                      yerr=yerr, error_kw=error_kw, hatch=hatch)
        tops.append((vals + hi_err).max())
        bots.append((vals - lo_err).min())
        if annotate:
            for bar, val, he in zip(bars, vals, np.broadcast_to(hi_err, vals.shape)):
                text_color = 'white' if _luminance(color) < 128 else 'black'
                ax.text(bar.get_x() + bar.get_width() / 2,
                        val + he + 0.5,
                        f'{val:.1f}', ha='center', va='bottom',
                        fontsize=fontsize, color=text_color)

    if dynamic_ylim:
        top, bot = max(tops), min(bots)
        span = max(top - bot, 1e-6)
        ax.set_ylim(max(0, bot - span * 0.15), top + span * 0.25)

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False)
```

---

## Pattern: trend_lines(ax, x, y_series, labels, colors=None, ...)

```python
def trend_lines(ax, x, y_series, labels, colors=None,
                ylabel='', xlabel='', lw=2.0, markersize=6,
                show_fill=False, fill_alpha=0.15, markers=None):
    """
    Multi-line trend plot — publication style.

    Parameters
    ----------
    ax : matplotlib Axes
    x : array-like               — shared x values
    y_series : list[array]       — one 1D array per line
    labels : list[str]
    colors : list[str] | None
    ylabel, xlabel : str
    lw : float                   — line width
    markersize : int             — marker size
    show_fill : bool             — if y is 2D (rows=runs), fill_between ± std
    fill_alpha : float
    """
    if colors is None:
        colors = list(CS_PEER_PALETTE[:len(y_series)])
    # Redundant channel: a distinct marker per series so identity survives
    # crossings, grayscale print, and color-vision deficiency.
    if markers is None:
        markers = list(CS_PEER_MARKERS[:len(y_series)])

    for y, label, color, mk in zip(y_series, labels, colors, markers):
        y = np.asarray(y)
        if y.ndim == 2:
            mean, std = y.mean(0), y.std(0)
        else:
            mean, std = y, None
        ax.plot(x, mean, color=color, lw=lw, marker=mk,
                markersize=markersize, label=label)
        if show_fill and std is not None:
            ax.fill_between(x, mean - std, mean + std,
                            color=color, alpha=fill_alpha)

    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.legend(frameon=False)
```

---

## Pattern: heatmap(ax, matrix, x_labels=None, y_labels=None,
            cmap='Blues', cbar_label=None, annotate=True,
            fmt='{:.0f}', fontsize=10, vmin=0, vmax=100):
    """
    Publication heatmap with clean white gridlines. Uses pcolormesh
    for professional cell separation.

    Parameters
    ----------
    ax : matplotlib Axes
    matrix : 2D array (n_rows × n_cols)
    x_labels, y_labels : list[str] | None
    cmap : str                    — 'Blues' (default), 'Reds' for danger/error metrics, 'RdBu_r' for diverging
    cbar_label : str | None       — colorbar label with unit
    annotate : bool
    fmt : str                     — format string for cell values
    fontsize : int                — 10 minimum for readability
    vmin, vmax : float            — color scale range
    """
    import matplotlib as mpl
    import numpy as np

    n_rows, n_cols = matrix.shape

    # pcolormesh with white gridlines — clean cell separation
    im = ax.pcolormesh(matrix, cmap=cmap, edgecolors='white',
                       linewidths=1, vmin=vmin, vmax=vmax)
    ax.invert_yaxis()

    if x_labels:
        ax.set_xticks(np.arange(n_cols) + 0.5)
        ax.set_xticklabels(x_labels, rotation=0, fontsize=fontsize)
    if y_labels:
        ax.set_yticks(np.arange(n_rows) + 0.5)
        ax.set_yticklabels(y_labels, rotation=0, fontsize=fontsize)

    if annotate:
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        cm_obj = plt.get_cmap(cmap)
        for i in range(n_rows):
            for j in range(n_cols):
                val = matrix[i, j]
                r, g, b, _ = cm_obj(norm(val))
                lum = 0.299*r + 0.587*g + 0.114*b
                color = 'white' if lum < 0.5 else 'black'
                ax.text(j + 0.5, i + 0.5, fmt.format(val),
                        ha='center', va='center',
                        fontsize=fontsize, color=color, fontweight='bold')

    if cbar_label:
        cbar = ax.figure.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
        cbar.set_label(cbar_label, fontsize=fontsize)
        cbar.ax.tick_params(labelsize=fontsize - 1)

    ax.figure.tight_layout(pad=1.5)
```

---

## Pattern: radar_chart(ax, categories, values_dict, colors=None, ...)

A radar is only legible with a few traces. The default radar grammar supports up to
six methods by using `CS_RADAR_PALETTE`, white-filled markers, mixed line styles,
light grey rings, and a below-figure legend. If there are more than six methods or
more than eight spokes, switch to grouped bars, a heatmap, or small multiples.
For supporting body-compact diagnostics, cap the visible methods at four.

For 0--100-style rates, keep `per_spoke_norm=False` and show the reference-style
20/40/60/80 radial ticks. Use per-spoke normalization only when spokes have
different units or incompatible ranges; state that normalization in the caption.

For the common paper case of two related radar panels, use
`draw_shared_legend_radar()` below. It uses the same visual grammar as `radar_chart()`
but removes per-panel legends and adds one shared legend below the full figure.

```python
def add_custom_theta_labels(ax, angles, labels, rmax, fontsize=9, pad=14,
                            color="#2C3E50", fontweight="bold"):
    """Place radar spoke labels outside the ring with visual-angle-aware alignment."""
    import numpy as np

    for angle, label in zip(angles, labels):
        visual_angle_rad = (np.pi / 2 - angle) % (2 * np.pi)
        deg = np.degrees(visual_angle_rad)
        if 85 < deg < 95:
            ha, va, dx, dy = "center", "bottom", 0, pad
        elif 5 < deg <= 85:
            ha, va, dx, dy = "left", "bottom", pad, pad
        elif 355 < deg <= 360 or 0 <= deg <= 5:
            ha, va, dx, dy = "left", "center", pad, 0
        elif 275 < deg <= 355:
            ha, va, dx, dy = "left", "top", pad, -pad
        elif 265 < deg <= 275:
            ha, va, dx, dy = "center", "top", 0, -pad
        elif 185 < deg <= 265:
            ha, va, dx, dy = "right", "top", -pad, -pad
        elif 175 < deg <= 185:
            ha, va, dx, dy = "right", "center", -pad, 0
        else:
            ha, va, dx, dy = "right", "bottom", -pad, pad
        ax.annotate(
            label,
            xy=(angle, rmax),
            xytext=(dx, dy),
            textcoords="offset points",
            ha=ha,
            va=va,
            fontsize=fontsize,
            fontweight=fontweight,
            color=color,
            zorder=30,
            annotation_clip=False,
        )


def radar_chart(ax, categories, values_dict, colors=None,
                fill_alpha=CS_RADAR_FILL_ALPHA, lw=CS_RADAR_LINEWIDTH,
                markersize=CS_RADAR_MARKERSIZE,
                per_spoke_norm=False, display_lo=0, display_hi=80,
                value_range=(0, 100), markers=None, linestyles=None,
                show_legend=True, radial_ticks=CS_RADAR_TICKS, title=None,
                label_fontsize=9, label_pad=14, tick_fontsize=8,
                title_fontsize=13, legend_ncol=None):
    """
    Multi-method radar / polar chart using the CS_RADAR_PALETTE reference grammar.

    Parameters
    ----------
    ax : matplotlib Axes (with projection='polar')
    categories : list[str]               — spoke labels
    values_dict : dict[str, list[float]] — method_name -> values (one per category)
    colors : list[str] | None
    fill_alpha : float                   — faint polygon fill, default 0.04
    lw : float                           — trace line width
    markersize : int                     — vertex marker size
    per_spoke_norm : bool                — normalize each spoke to [display_lo, display_hi]
                                           only when spoke units/ranges differ
    display_lo, display_hi : float       — radial display band
    value_range : (lo, hi)               — recorded expected raw range for captions/checks
    show_legend : bool                   — use False for shared-legend multi-panel radars
    radial_ticks : list[float] | None    — raw radial tick labels for shared-scale radars
    """
    names = list(values_dict.keys())
    if colors is None:
        colors = list(CS_RADAR_PALETTE[:len(names)])
    # Distinct marker per series: with many overlapping traces, shape (not just
    # color) tells methods apart at crossings, in grayscale, and for CVD readers.
    if markers is None:
        markers = list(CS_RADAR_MARKERS[:len(names)])
    if linestyles is None:
        linestyles = list(CS_RADAR_LINESTYLES[:len(names)])
    n_methods, n_spokes = len(names), len(categories)
    if n_methods > 6:
        raise ValueError(f"{n_methods} methods on one radar is unreadable; use grouped bars/heatmap.")
    if n_spokes > 8:
        raise ValueError(f"{n_spokes} spokes on one radar is unreadable; use grouped bars/heatmap.")

    angles = np.linspace(0, 2 * np.pi, n_spokes, endpoint=False)
    angles_closed = np.append(angles, angles[0])
    arr = np.array([values_dict[k] for k in names], dtype=float)  # (methods, spokes)

    # Per-spoke normalization spreads differences across the display band.
    if per_spoke_norm:
        lo, hi = arr.min(axis=0), arr.max(axis=0)
        span = np.where(hi > lo, hi - lo, 1.0)
        disp = display_lo + (display_hi - display_lo) * (arr - lo) / span
        visual_rmax = display_hi
    else:
        disp = arr
        visual_rmax = max(display_hi, float(np.nanmax(arr)))

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, visual_rmax)
    if title:
        ax.set_title(
            title,
            fontsize=title_fontsize,
            fontweight='bold',
            color=CS_SUPPORT_COLORS["radar_title"],
            y=1.18,
            pad=0,
        )

    # Hide default angular labels, then draw custom outside labels.
    ax.set_xticks(angles)
    ax.set_xticklabels([])
    ax.tick_params(axis="x", pad=0)

    if radial_ticks and not per_spoke_norm:
        ax.set_yticks(list(radial_ticks))
        ax.set_yticklabels([f"{tick:g}" for tick in radial_ticks],
                           fontsize=tick_fontsize,
                           color=CS_SUPPORT_COLORS["radar_tick"])
        ax.set_rlabel_position(22)
    else:
        ax.set_yticklabels([])

    ax.yaxis.grid(True, color=CS_SUPPORT_COLORS["radar_grid"], linewidth=0.8,
                  linestyle=CS_RADAR_GRID_LINESTYLE)
    ax.xaxis.grid(True, color=CS_SUPPORT_COLORS["radar_grid"], linewidth=0.8)
    ax.spines["polar"].set_linewidth(1.5)
    ax.spines["polar"].set_color(CS_SUPPORT_COLORS["radar_outer_ring"])

    for i in reversed(range(n_methods)):
        name, color, mk, ls = names[i], colors[i], markers[i], linestyles[i]
        ring = np.append(disp[i], disp[i][0])
        ax.plot(
            angles_closed,
            ring,
            color=color,
            linewidth=lw,
            linestyle=ls,
            marker=mk,
            markersize=markersize,
            markerfacecolor="white",
            markeredgecolor=color,
            markeredgewidth=CS_RADAR_MARKER_EDGEWIDTH,
            label=name,
            zorder=10 + (n_methods - i),
        )
        if fill_alpha:
            ax.fill(angles_closed, ring, color=color, alpha=fill_alpha)

    add_custom_theta_labels(
        ax,
        angles,
        categories,
        display_hi,
        fontsize=label_fontsize,
        pad=label_pad,
        color=CS_SUPPORT_COLORS["radar_label"],
    )
    ax.plot(0, 0, "o", color=CS_SUPPORT_COLORS["radar_center_dot"],
            markersize=2.2, zorder=20)

    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color=c, marker=m, linestyle=ls, lw=lw,
                      markerfacecolor='white', markersize=markersize,
                      markeredgecolor=c, markeredgewidth=CS_RADAR_MARKER_EDGEWIDTH, label=n)
               for n, c, m, ls in zip(names, colors, markers, linestyles)]
    if show_legend:
        if legend_ncol is None:
            legend_ncol = min(3, n_methods)
        ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.08),
                  ncol=legend_ncol, fontsize=8, frameon=False,
                  handlelength=2.4, columnspacing=1.15, handletextpad=0.45)
    return handles
```

When `per_spoke_norm=True`, raw value scales are no longer readable from the rings,
so state the per-spoke ranges in the caption or a small note (e.g. "each spoke
normalized to its own min–max across methods"). For a true shared 0–100 scale with
few methods, pass `per_spoke_norm=False`.

---

## Pattern: draw_shared_legend_radar(panel_specs, ...)

Use this for the **Preset: shared-legend radar**: two polar panels, faint fills,
consistent method encodings, light rings/spokes, and one shared legend below the figure.

```python
def draw_shared_legend_radar(panel_specs, colors=None, markers=None, linestyles=None,
                             figsize=None, shared_scale=True,
                             value_range=(0, 100), radial_ticks=(20, 40, 60, 80),
                             body_compact=False, max_body_traces=4):
    """
    Shared-legend multi-panel radar.

    panel_specs: list[dict] with keys:
      title      — panel title, e.g. '(a) Rate by category group'
      categories — spoke labels
      values     — dict[method_name, list[float]]

    Use shared_scale=True when all panels use the same unit, such as a percentage rate.
    Use body_compact=True for supporting main-body diagnostics; this caps the visible
    methods and uses a smaller export target intended for 0.78--0.86\textwidth inclusion.
    """
    if len(panel_specs) < 2:
        raise ValueError("shared-legend radar expects at least two panels")
    methods = list(panel_specs[0]["values"].keys())
    if any(list(spec["values"].keys()) != methods for spec in panel_specs):
        raise ValueError("all radar panels must use the same method order")
    if body_compact and len(methods) > max_body_traces:
        raise ValueError(
            f"body compact radar supports at most {max_body_traces} traces; "
            "move remaining methods to an appendix/table or use heatmap/grouped bars."
        )
    if figsize is None:
        figsize = (5.8, 2.65) if body_compact else (15.0, 7.8)
    if colors is None:
        colors = list(CS_RADAR_PALETTE[:len(methods)])
    if markers is None:
        markers = list(CS_RADAR_MARKERS[:len(methods)])
    if linestyles is None:
        linestyles = list(CS_RADAR_LINESTYLES[:len(methods)])

    fig, axes = plt.subplots(
        1, len(panel_specs), figsize=figsize,
        subplot_kw={"projection": "polar"}
    )
    if len(panel_specs) == 1:
        axes = [axes]

    shared_handles = None
    for ax, spec in zip(axes, panel_specs):
        shared_handles = radar_chart(
            ax,
            categories=spec["categories"],
            values_dict=spec["values"],
            colors=colors,
            markers=markers,
            linestyles=linestyles,
            fill_alpha=CS_RADAR_FILL_ALPHA,
            lw=CS_RADAR_LINEWIDTH,
            markersize=CS_RADAR_MARKERSIZE,
            per_spoke_norm=not shared_scale,
            display_lo=0 if shared_scale else 20,
            display_hi=80 if shared_scale else 95,
            value_range=value_range,
            radial_ticks=radial_ticks if shared_scale else None,
            show_legend=False,
            title=spec["title"],
            label_fontsize=16 if not body_compact else 9,
            label_pad=18 if not body_compact else 12,
            tick_fontsize=11 if not body_compact else 8,
            title_fontsize=20 if not body_compact else 13,
        )

    labels = [h.get_label() for h in shared_handles]
    legend_ncol = 2 if len(methods) <= 4 else 3
    legend_fontsize = 8 if body_compact else 15
    fig.legend(
        handles=shared_handles,
        labels=labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.035 if not body_compact else -0.02),
        ncol=legend_ncol,
        frameon=False,
        fontsize=legend_fontsize,
        handlelength=2.4,
        columnspacing=1.15,
        handletextpad=0.45,
    )
    if body_compact:
        fig.subplots_adjust(left=0.04, right=0.98, top=0.80, bottom=0.18, wspace=0.28)
    else:
        fig.subplots_adjust(left=0.055, right=0.985, top=0.76, bottom=0.18, wspace=0.28)
    return fig, axes
```

---

## Pattern: add_panel_label(ax, label, ...)

```python
def add_panel_label(ax, label, x=-0.06, y=1.02, fontsize=12,
                    fontweight='bold', color=CS_SUPPORT_COLORS["text"]):
    """Place a bold lowercase panel label near the top-left edge."""
    ax.text(x, y, label, transform=ax.transAxes, fontsize=fontsize,
            fontweight=fontweight, color=color, ha='left', va='bottom')
```

---

## Pattern: dedicated_legend_panel(fig, position, handles, labels, ...)

```python
def dedicated_legend_panel(fig, subplot_spec, handles, labels,
                           fontsize=10, ncol=1):
    """
    Turn a subplot into a legend-only panel. Use when the legend is too large
    to fit inside data axes without covering data.

    Parameters
    ----------
    fig : matplotlib Figure
    subplot_spec : GridSpec cell or (row, col) index
    handles, labels : from ax.get_legend_handles_labels()
    fontsize : int
    ncol : int
    """
    ax_leg = fig.add_subplot(subplot_spec)
    ax_leg.legend(handles, labels, fontsize=fontsize, loc='center',
                  frameon=False, ncol=ncol)
    ax_leg.set_axis_off()
```

---

## Pattern: horizontal_bars(ax, labels, values, ...)

Use horizontal bars for rankings, ablations, long labels, and delta contributions.

```python
def horizontal_bars(ax, labels, values, colors=None, errors=None,
                    xlabel='', annotate=True, zero_line=False):
    """Publication horizontal bars with optional uncertainty and value labels."""
    values = np.asarray(values, dtype=float)
    y = np.arange(len(labels))
    if colors is None:
        colors = [CS_HERO_COLOR] * len(labels)
    error_kw = {'elinewidth': 1.4, 'capthick': 1.4, 'capsize': 3}
    bars = ax.barh(y, values, color=colors, edgecolor=CS_SUPPORT_COLORS["edge"], linewidth=0.8,
                   xerr=errors, error_kw=error_kw)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.invert_yaxis()
    if zero_line:
        ax.axvline(0, color=CS_SUPPORT_COLORS["neutral_mid"], lw=1.0, ls='--', zorder=0)
    if annotate:
        span = max(values.max() - values.min(), 1e-6)
        pad = span * 0.03
        for bar, val in zip(bars, values):
            ha = 'left' if val >= 0 else 'right'
            x = val + pad if val >= 0 else val - pad
            ax.text(x, bar.get_y() + bar.get_height() / 2,
                    f'{val:.1f}', va='center', ha=ha, fontsize=8)
    ax.figure.tight_layout(pad=1.2)
```

---

## Pattern: paired_opposing_horizontal_scorecard(ax, labels, lower_values, higher_values, ...)

Use this for the **Preset: paired-opposing horizontal scorecard**.

```python
def paired_opposing_horizontal_scorecard(ax, labels, lower_values, higher_values,
                                         lower_label='Lower-is-better',
                                         higher_label='Higher-is-better',
                                         xlabel='Rate over comparable items (%)',
                                         xlim=None):
    """Paired horizontal bars for one lower-is-better and one higher-is-better metric."""
    lower_values = np.asarray(lower_values, dtype=float)
    higher_values = np.asarray(higher_values, dtype=float)
    y = np.arange(len(labels))
    height = 0.34
    lower_color = CS_PAIRED_OPPOSING_PALETTE["lower_better"]
    higher_color = CS_PAIRED_OPPOSING_PALETTE["higher_better"]

    ax.barh(y - height / 2, lower_values, height, color=lower_color,
            edgecolor="#A96A5D", linewidth=0.35, label=lower_label)
    ax.barh(y + height / 2, higher_values, height, color=higher_color,
            edgecolor="#4D789B", linewidth=0.35, label=higher_label)
    for yi, val in zip(y - height / 2, lower_values):
        ax.text(val + 1.0, yi, f"{val:.1f}", va="center", ha="left",
                fontsize=8, color="#333333")
    for yi, val in zip(y + height / 2, higher_values):
        ax.text(val + 1.0, yi, f"{val:.1f}", va="center", ha="left",
                fontsize=8, color="#333333")

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    if xlim is None:
        xlim = max(float(lower_values.max()), float(higher_values.max())) + 9
    ax.set_xlim(0, xlim)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", color="#E0E0E0", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", ncol=2)
    ax.figure.tight_layout(pad=0.6)
```

---

## Pattern: stacked_bars(ax, categories, components, component_labels, ...)

Use stacked bars for whole-part composition only. State totals/denominators in the caption.

```python
def stacked_bars(ax, categories, components, component_labels, colors=None,
                 ylabel='', normalize=False, annotate_totals=True):
    """
    Stacked bar chart.

    components: list[array] — one array per component, each length len(categories)
    normalize: if True, convert each category to shares summing to 100
    """
    vals = np.vstack([np.asarray(c, dtype=float) for c in components])
    totals = vals.sum(axis=0)
    plot_vals = np.divide(vals, totals, out=np.zeros_like(vals), where=totals != 0) * 100 if normalize else vals
    if colors is None:
        colors = list(CS_HERO_BASELINE_PALETTE[:len(component_labels)])
    x = np.arange(len(categories))
    bottom = np.zeros(len(categories))
    for comp, label, color in zip(plot_vals, component_labels, colors):
        ax.bar(x, comp, bottom=bottom, label=label, color=color,
               edgecolor=CS_SUPPORT_COLORS["edge"], linewidth=0.8)
        bottom += comp
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel or ('Share (%)' if normalize else 'Count'))
    ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.12),
              ncol=min(4, len(component_labels)))
    if annotate_totals:
        for xi, total, top in zip(x, totals, bottom):
            ax.text(xi, top * 1.01, f'n={total:.0f}', ha='center', va='bottom', fontsize=8)
    ax.figure.tight_layout(pad=1.2)
```

---

## Pattern: scatter_with_pareto(ax, x, y, labels=None, ...)

Use this for performance-cost or performance-latency tradeoffs. Always declare direction.

```python
def pareto_frontier(x, y, minimize_x=True, maximize_y=True):
    """Return indices of non-dominated points sorted by x."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    idx = np.argsort(x if minimize_x else -x)
    frontier = []
    best = -np.inf if maximize_y else np.inf
    for i in idx:
        yi = y[i]
        improves = yi > best if maximize_y else yi < best
        if improves:
            frontier.append(i)
            best = yi
    return np.asarray(frontier, dtype=int)

def scatter_with_pareto(ax, x, y, labels=None, sizes=None, colors=None,
                        xlabel='', ylabel='', minimize_x=True, maximize_y=True,
                        annotate_frontier=True):
    """Scatter plot with a connected Pareto frontier."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if sizes is None:
        sizes = np.full_like(x, 55.0)
    if colors is None:
        colors = list(CS_PEER_PALETTE[:len(x)])
    ax.scatter(x, y, s=sizes, c=colors, edgecolors='white', linewidths=0.8, alpha=0.9)
    front = pareto_frontier(x, y, minimize_x=minimize_x, maximize_y=maximize_y)
    front = front[np.argsort(x[front])]
    ax.plot(x[front], y[front], color=CS_SUPPORT_COLORS["axis"], lw=1.5, ls='--', zorder=2)
    if labels is not None and annotate_frontier:
        for i in front:
            ax.text(x[i], y[i], f' {labels[i]}', fontsize=8, va='center')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.figure.tight_layout(pad=1.2)
    return front
```

---

## Pattern: distribution_plot(ax, groups, labels, kind='box')

Use distribution plots only when the spread/shape is part of the evidence. Record `n`, center, and
spread definition in the caption or source-data note.

```python
def distribution_plot(ax, groups, labels, kind='box', colors=None,
                      ylabel='', bins=18, density=True):
    """
    kind: 'box', 'violin', 'hist', or 'density'.
    Density uses scipy gaussian_kde when available; fall back to a normalized histogram otherwise.
    """
    groups = [np.asarray(g, dtype=float) for g in groups]
    if colors is None:
        colors = list(CS_PEER_PALETTE[:len(groups)])
    if kind == 'box':
        bp = ax.boxplot(groups, tick_labels=labels, patch_artist=True, showfliers=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.35)
            patch.set_edgecolor('black')
    elif kind == 'violin':
        vp = ax.violinplot(groups, showmeans=False, showmedians=True, showextrema=False)
        for body, color in zip(vp['bodies'], colors):
            body.set_facecolor(color)
            body.set_alpha(0.30)
            body.set_edgecolor('black')
        ax.set_xticks(np.arange(1, len(labels) + 1))
        ax.set_xticklabels(labels)
    elif kind == 'hist':
        shared_bins = np.histogram_bin_edges(np.concatenate(groups), bins=bins)
        for g, label, color in zip(groups, labels, colors):
            ax.hist(g, bins=shared_bins, histtype='step', density=density,
                    lw=1.8, label=label, color=color)
        ax.legend(frameon=False)
    elif kind == 'density':
        xs = np.linspace(min(g.min() for g in groups), max(g.max() for g in groups), 300)
        try:
            from scipy.stats import gaussian_kde
            for g, label, color in zip(groups, labels, colors):
                ys = gaussian_kde(g)(xs)
                ax.plot(xs, ys, color=color, lw=1.8, label=label)
                ax.fill_between(xs, 0, ys, color=color, alpha=0.10)
        except Exception:
            shared_bins = np.histogram_bin_edges(np.concatenate(groups), bins=bins)
            for g, label, color in zip(groups, labels, colors):
                ax.hist(g, bins=shared_bins, histtype='step', density=True,
                        lw=1.8, label=label, color=color)
        ax.legend(frameon=False)
    else:
        raise ValueError("kind must be 'box', 'violin', 'hist', or 'density'")
    ax.set_ylabel(ylabel)
    ax.figure.tight_layout(pad=1.2)
```

---

## Pattern: pie_or_donut(ax, labels, values, ...)

Pie/donut charts are allowed only for one simple whole-part snapshot. Prefer stacked bars for
comparisons across groups.

```python
def pie_or_donut(ax, labels, values, colors=None, donut=True,
                 center_label=None, max_slices=5):
    """Restrained pie/donut chart with sorted slices and a required total."""
    values = np.asarray(values, dtype=float)
    order = np.argsort(values)[::-1]
    labels = [labels[i] for i in order]
    values = values[order]
    if len(values) > max_slices:
        other = values[max_slices-1:].sum()
        labels = labels[:max_slices-1] + ['Other']
        values = np.concatenate([values[:max_slices-1], [other]])
    if colors is None:
        colors = list(CS_HERO_BASELINE_PALETTE[:len(values)])
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.0f%%', startangle=90,
        counterclock=False, colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.0},
        textprops={'fontsize': 8}
    )
    if donut:
        ax.add_artist(plt.Circle((0, 0), 0.58, color='white'))
        if center_label is None:
            center_label = f'n={values.sum():.0f}'
        ax.text(0, 0, center_label, ha='center', va='center', fontsize=9, fontweight='bold')
    ax.set_aspect('equal')
```

For paper-ready taxonomy or category coverage, prefer the named preset below over
`pie_or_donut()`.

---

## Pattern: draw_compact_labeled_donut(ax, codes, values, ...)

Use this for the **Preset: compact labeled donut**: a thick ring, white wedge separators,
outside code-percentage labels, grey leader lines, and a bottom legend that maps short codes
to full category labels. Keep long labels out of wedges.

```python
from matplotlib.patches import Patch

def draw_compact_labeled_donut(ax, codes, values, full_labels=None, colors=None,
                               title=None, startangle=90, legend_ncol=3,
                               show_total_in_center=False, body_compact=False):
    """
    Compact labeled donut for 5-7 whole-part categories.

    codes: short labels shown around the ring, e.g. ['H1', 'H2', ...]
    values: counts or shares; percentages are computed from these values
    full_labels: optional long labels for the bottom legend
    body_compact: omit long legend text for supporting main-text figures
    """
    values = np.asarray(values, dtype=float)
    if len(codes) != len(values):
        raise ValueError("codes and values must have the same length")
    if len(values) > 7:
        raise ValueError("compact labeled donut supports at most 7 categories")
    total = values.sum()
    if total <= 0:
        raise ValueError("donut values must sum to a positive total")
    if colors is None:
        colors = CS_COVERAGE_PALETTE[:len(values)]

    wedges, _ = ax.pie(
        values,
        startangle=startangle,
        counterclock=False,
        colors=colors,
        radius=1.0,
        # white wedge separators are part of this preset, not decoration.
        wedgeprops={"width": 0.58 if body_compact else 0.62,
                    "edgecolor": "white",
                    "linewidth": 2.2 if body_compact else 3.0},
    )
    ax.set(aspect="equal")
    if title:
        ax.set_title(title, fontsize=9 if body_compact else 15,
                     fontweight="bold", color="#333333", pad=6 if body_compact else 20)

    for wedge, code, value in zip(wedges, codes, values):
        pct = 100 * value / total
        angle = np.deg2rad((wedge.theta1 + wedge.theta2) / 2.0)
        x, y = np.cos(angle), np.sin(angle)
        ha = "left" if x >= 0 else "right"
        # Pull bottom labels slightly inward so they do not collide with the legend.
        label_radius = 1.12 if body_compact else 1.26
        if y < -0.72:
            label_radius = 1.04 if body_compact else 1.16
        ax.annotate(
            f"{code} ({pct:.1f}%)",
            xy=(0.72 * x, 0.72 * y),
            xytext=(label_radius * x, label_radius * y),
            ha=ha,
            va="center",
            fontsize=6.8 if body_compact else 10,
            fontweight="bold",
            color="#3A3A3A",
            arrowprops={
                "arrowstyle": "-",
                "color": "#B8B8B8",
                "lw": 0.75 if body_compact else 0.9,
                "shrinkA": 0,
                "shrinkB": 0,
            },
        )

    if show_total_in_center:
        ax.text(0, 0, f"n={total:.0f}", ha="center", va="center",
                fontsize=10, fontweight="bold", color="#3A3A3A")

    # In body_compact mode, the legend should be omitted because long labels make a
    # supporting coverage figure visually dominate the page. Put definitions in the
    # caption, appendix, or an adjacent taxonomy table instead.
    if body_compact:
        return wedges

    if full_labels:
        handles = [
            Patch(facecolor=color, edgecolor="none", label=f"{code}: {label}")
            for code, label, color in zip(codes, full_labels, colors)
        ]
        ax.legend(
            handles=handles,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.22),
            ncol=legend_ncol,
            frameon=False,
            fontsize=9,
            handlelength=1.4,
            columnspacing=1.2,
        )
    return wedges
```

For a two-panel style-matched coverage figure, use the fixed seven-color
coverage donut palette for both panels instead of generic categorical colors:

```python
def draw_coverage_donut_pair(axes, left_items, right_items,
                             left_title="Coverage group A",
                             right_title="Coverage group B"):
    """
    Two quiet body coverage donuts using the reference palette.

    left_items / right_items: list[(code, count)] in semantic display order.
    """
    for ax, items, title, colors in (
        (axes[0], left_items, left_title,
         CS_COVERAGE_PALETTE[:len(left_items)]),
        (axes[1], right_items, right_title,
         CS_COVERAGE_PALETTE[:len(right_items)]),
    ):
        codes = [code for code, _ in items]
        values = [count for _, count in items]
        draw_compact_labeled_donut(
            ax,
            codes,
            values,
            colors=colors,
            title=title,
            startangle=90,
            show_total_in_center=True,
            body_compact=True,
        )
```

For a main-text two-panel coverage figure, start with `figsize=(5.6, 2.15)` and include the rendered
PDF at about `0.58--0.72\textwidth`. Use the full legend variant only when the composition figure is
the central evidence item or when no appendix/table defines the short codes. If a legend is kept,
reserve enough bottom margin (`fig.subplots_adjust(bottom=0.32)` or more for two-row legends) and
inspect the rendered PDF/PNG: label-legend overlap is a rendering defect, not a harmless compactness
tradeoff.

---

## Usage in Full Draft

When generating figures for a paper:

1. Import patterns from this file or inline the relevant function.
2. Map method names to semantic colors using the Writing Policy method list.
3. Call the pattern function with the correct data, labels, and colors.
4. Always call `save_figure()` with all three formats (SVG, PDF, PNG).
5. Do not hardcode results from memory — read from workspace result files.
