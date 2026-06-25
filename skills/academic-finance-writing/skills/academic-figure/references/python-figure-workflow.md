# Python Figure Workflow

Use this file when the user chooses Python, provides Python scripts, notebooks, or a Python-centered
data workflow for finance manuscript figures. Keep the finance figure contract: claim first, source
data second, drawing code third.

For chart-family selection after Python is chosen, load `references/python-chart-catalog.md`.
For paper-level color consistency, load `references/finance-palette.md` and use one palette profile
for all figures in the manuscript.
For final size and manuscript placement, load `references/figure-layout.md`.

## Python-only Execution Rule

Contract phrase: Python-only execution rule.

When Python is selected, all figure drawing, previewing, exporting, and visual QA must be done in
Python. Do not call R, ggplot2, fixest, or another non-Python plotting backend to create a temporary
preview, fallback export, or layout approximation. If Python or required packages are missing, stop
before rendering and report the blocker. You may still write the Python script and provide
installation commands, but do not cross-render with another language.

Allowed non-Python utilities are limited to non-visual work such as shell file inspection, CSV line
counts, archive extraction, or text search. They must not create image/vector outputs or alter visual
layout.

## Common Python Packages

| Task | Preferred packages |
|---|---|
| Core plotting and data shaping | `matplotlib`, `seaborn`, `pandas`, `numpy` |
| Regression and econometric output | `statsmodels`, `linearmodels`, `scipy` |
| Event studies and panel diagnostics | `pandas`, `statsmodels`, `linearmodels`, `matplotlib` |
| Portfolio, returns, and backtests | `pandas`, `numpy`, `empyrical`, `pyfolio` when available |
| Maps, networks, and composite layouts | `geopandas`, `networkx`, `matplotlib.gridspec`, `subplot_mosaic` |
| Tables | `pandas`, `statsmodels.iolib`, custom LaTeX `booktabs` writers |
| Export | `matplotlib.savefig` to SVG/PDF/PNG/TIFF with editable text where possible |

## Minimal Python Export Scaffold

```python
from cycler import cycler
import matplotlib as mpl
import matplotlib.pyplot as plt

# Preferred: import the canonical registry from academic-finance-writing/scripts.
# If a paper-local script cannot import it directly, mirror the same tokens and
# record PALETTE_PROFILE in the Display-Item Plan.
from finance_palette import (
    categorical_colors,
    colors_for_display,
    diverging_colors,
    get_palette_profile,
    role_color,
    sequential_colors,
)

PALETTE_PROFILE = "finance-muted"
FINANCE_PROFILE = get_palette_profile(PALETTE_PROFILE)
FINANCE_PALETTE = FINANCE_PROFILE.tokens

FINANCE_SIZE_PRESETS_MM = {
    "inline": (70, 45),
    "single_column": (89, 65),
    "mid_width": (130, 85),
    "double_column": (178, 105),
    "appendix_full_width": (178, 120),
}

mpl.rcParams.update({
    "font.family": "Arial",
    "font.size": 7,
    "axes.linewidth": 0.5,
    "axes.edgecolor": FINANCE_PALETTE["neutral_text"],
    "axes.labelcolor": FINANCE_PALETTE["neutral_text"],
    "axes.prop_cycle": cycler(color=categorical_colors(6, PALETTE_PROFILE, include_deep=True)),
    "xtick.color": FINANCE_PALETTE["neutral_text"],
    "ytick.color": FINANCE_PALETTE["neutral_text"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

def save_finance_figure_py(fig, filename, dpi=600):
    # Use constrained layout or tight layout before this call when axes titles,
    # legends, or long tick labels are present.
    fig.savefig(f"{filename}.svg", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(f"{filename}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight", pad_inches=0.04)
```

Palette usage rules for generated Python scripts:

- Use `categorical_colors(n, PALETTE_PROFILE)` for generic grouped bars, lines, and categories.
  For `n <= 4`, this avoids the dark `deep` token by default.
- Use `colors_for_display("event-study figure", profile_name=PALETTE_PROFILE)` for known finance
  displays instead of picking raw hex values.
- Use `sequential_colors(PALETTE_PROFILE)` for ordered intensity heatmaps and
  `diverging_colors(PALETTE_PROFILE)` only when the midpoint has a clear economic meaning.
- Use `role_color("risk", PALETTE_PROFILE)` or another semantic role when a color encodes meaning
  rather than category order.

## Finance Figure QA

Before marking the figure complete, record:

| field | required content |
|---|---|
| source-data-to-panel | Source file/table/model output for every plotted element. |
| palette profile | Paper-level palette profile and semantic color map from `references/finance-palette.md`. |
| small-N color check | For 1-4 categorical colors, confirm `categorical_colors(n)` did not use `deep` unless justified. |
| layout contract | Placement width, float environment, final size, panel grid, text anchor, and layout risk from `references/figure-layout.md`. |
| Python script | Path to the script or notebook used for drawing. |
| export files | SVG/PDF plus PNG preview when possible. |
| visual QA | not blank, not cropped, final-size text legible, no overlapping labels, colors consistent with the paper palette, width matches the layout contract. |
| finance linkage | sample, unit, model, benchmark, economic magnitude, and uncertainty visible in plot, table note, or caption. |
| blocker | Missing source data, missing Python runtime/package, or failed preview inspection. |

For plotted assets, run `scripts/audit_visual_assets.py` on the exported PNG/JPG preview. A likely
cropped title, clipped axis label, clipped legend, blank preview, or dominant unused margin blocks
`visual_asset_qa_status: pass`. Prefer `constrained_layout=True` at figure creation, or call
`fig.tight_layout()` before export when constrained layout is unavailable.

If source data, Python runtime, package dependencies, or visual QA evidence are missing, report the
visual display gate as BLOCKED rather than substituting an R render or claiming the Python figure is
done.
