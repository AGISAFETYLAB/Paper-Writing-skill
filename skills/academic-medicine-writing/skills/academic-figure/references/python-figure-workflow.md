# Python Figure Workflow

Use this file when the user chooses Python, provides Python scripts, notebooks, or a Python-centered
data workflow for medical manuscript figures. Keep the normal medical figure contract: claim first,
source data second, drawing code third.

For chart-family selection after Python is chosen, load `references/python-chart-catalog.md`.

## Python-only Execution Rule

Contract phrase: Python-only execution rule.

When Python is selected, all figure drawing, previewing, exporting, and visual QA must be done in
Python. Do not call R, ggplot2, ComplexHeatmap, or another non-Python plotting backend to create a
temporary preview, fallback export, or layout approximation. If Python or required packages are
missing, stop before rendering and report the blocker. You may still write the Python script and
provide installation commands, but do not cross-render with another language.

Allowed non-Python utilities are limited to non-visual work such as shell file inspection, CSV line
counts, archive extraction, or text search. They must not create image/vector outputs or alter visual
layout.

## Common Python Packages

| Task | Preferred packages |
|---|---|
| Core plotting | `matplotlib`, `seaborn`, `pandas`, `numpy` |
| Statistical estimates and intervals | `scipy`, `statsmodels` |
| Survival displays | `lifelines`, `matplotlib` |
| Diagnostic and prediction displays | `scikit-learn`, `statsmodels`, `matplotlib` |
| Missingness and balance diagnostics | `missingno`, `pandas`, `statsmodels`, `matplotlib` |
| Network/flow/schematic displays | `networkx`, `graphviz`, `matplotlib` |
| Global-health maps | `geopandas`, `shapely`, `matplotlib` |
| Export | `matplotlib.savefig`, SVG/PDF/PNG/TIFF with editable text where possible |

## Minimal Python Export Scaffold

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "Arial",
    "font.size": 7,
    "axes.linewidth": 0.5,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

def save_medical_figure_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight")
```

## Python Palette Family Contract

Use a restrained visual system, not one literal color list for every chart. The package helper
`scripts/medical_palette.py` exposes `PALETTE_FAMILIES`, `DISPLAY_PALETTE_DEFAULTS`,
`display_palette(...)`, `colors_for_display(...)`, and semantic colormap helpers. Prefer importing
that helper in package scripts instead of retyping hex values.

```python
palette_families = {
    "teal_warm": {
        "group": ["#4EAB90", "#8EB69C", "#EDDCC3", "#EEBF6D", "#D94F33", "#834026"],
        "use": "bar charts, flow diagrams, tables, clinical triptychs, image plate + quant",
    },
    "deep_teal_coral": {
        "group": ["#4F8589", "#8A6B7B", "#D44C3C", "#E5855B", "#B7B5A0", "#EDD5B7"],
        "use": "bar, stacked-bar, lollipop, waterfall, categorical comparisons",
    },
    "scientific_blue_red": {
        "group": ["#5E82A2", "#D15354", "#E8B86C", "#8887CB", "#5094D5", "#F9AD95"],
        "use": "line, longitudinal, diagnostic, prediction, survival, forest, economic curves",
    },
}

display_palette_defaults = {
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
```

Use group colors for treatment/cohort/model groups within the selected family. Use sequential scales
for one-direction intensity such as counts, confusion matrices, annotated heatmaps, maps, and
enrichment intensity. Use diverging scales only for signed or midpoint-centered values such as
z-scores, correlations, and change-from-baseline matrices. Use missingness colors only for
observed/missing status. Use risk-bias colors only for ordered quality judgments. Do not mix ad hoc
Matplotlib colormaps such as `coolwarm`, `YlGnBu`, `Blues`, `magma`, `viridis`, or `rainbow` inside
one manuscript.

Do not use near-black colors as categorical fills in bars, area charts, or group markers. Reserve
very dark colors for text, axes, and sparse reference lines.

For image/composite panels, draw on a fixed normalized `0..1` canvas or explicit inset axes. Pass
`aspect="auto"` when using `imshow(..., extent=...)` on the parent axes, or use fixed inset boxes,
so image thumbnails, segmentation overlays, dot plots, and quantification bars share the same top,
bottom, and baseline instead of being shifted by Matplotlib's default equal-aspect image behavior.
Quantification bars beside images should use compact fixed-width marks rather than full-width bar
charts.

## Layout-Safe Python Patterns

For numeric-heavy clinical tables, generate LaTeX as `booktabs` + `tabular*` with controlled
inter-column fill, not raw equal-width `tabularx` numeric columns. Use `tabularx` only when the table
is text-heavy and the meaning-bearing text column needs wrapping.

For clinical triptych figures, build a centered outer `GridSpec` with explicit left/right margins and
enough vertical spacing / `hspace` between the longitudinal, effect-estimate, and summary bands. Anchor panel labels
inside or flush with axes; avoid negative x-position labels that expand the saved crop and make all
subplots appear shifted.

For image plate + quantification figures, use a two-part outer grid: the image plate receives most
of the width, the quantification panel receives a readable fixed share, and a visible gutter separates
them. Keep black backgrounds only inside image cells and place the `a` panel label near the left edge
of the image plate.

When a Python skill script generates a preview package, write a small layout audit record and run
`scripts/audit_display_layout.py` or an equivalent check before calling the route complete.

## Medical Figure QA

Before marking the figure complete, record:

| field | required content |
|---|---|
| source-data-to-panel | Source file/table for every plotted element. |
| Python script | Path to the script or notebook used for drawing. |
| export files | SVG/PDF plus PNG preview when possible. |
| visual QA | not blank, not cropped, final-size text legible, no overlapping labels. |
| medical linkage | denominator, timeframe, group labels, uncertainty, and missingness visible in the plot or legend. |
| blocker | Missing source data, missing Python runtime/package, or failed preview inspection. |

If source data, Python runtime, package dependencies, or visual QA evidence are missing, report the
visual display gate as BLOCKED rather than substituting an R render or claiming the Python figure is
done.
