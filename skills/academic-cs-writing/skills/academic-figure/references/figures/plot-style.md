# Plot Style

Use this reference when the confirmed Figure Plan contains data-driven plots,
metric visualizations, ablations, scaling curves, heatmaps, or generated
tables.

**This file is venue-agnostic.** It contains rcParams, colors, per-chart-type
rules, legend rules, and multi-panel architecture — shared across conference and
journal papers. For column widths, `figsize` values, and font size hierarchy,
load the venue-specific sizing file:
- Conference: `references/figures/conference/figure-sizing.md`
- Journal: `references/figures/journal/figure-sizing.md`

For chart-family selection across bar, grouped bar, stacked bar, line, scatter, Pareto, radar,
heatmap, box, histogram, violin, density, pie, and donut plots, load
`references/figures/chart-taxonomy.md` before writing plotting code. This file keeps the core style
rules; the taxonomy decides which visual form, palette preset, label strategy, and statistics note
fit the claim.

## Contents

- Ownership boundary, backend gate, and output formats
- Python rcParams and global plot-style rules
- Palette consumption rules and annotation/legend conventions
- Chart contract and multi-panel routing

## Ownership Boundary

This file owns venue-agnostic rcParams, output formats, legibility floors, and global rendering style.
It does not own chart-family selection, palette definitions, multi-panel templates, or reusable helper code.

## Backend Gate

Python (matplotlib/seaborn) is the default plotting backend. If the user prefers
R (ggplot2/patchwork), they must explicitly request it before any plot is
generated. Once a backend is selected, use it exclusively for all plotting,
previewing, and exporting. Do not cross-render with the other language. If the
selected backend's runtime or packages are missing, stop and report the blocker
before rendering.

Do not hardcode results from memory. Every chart must read from a concrete
workspace result file or table recorded in the Figure Plan.

## Output Format

**SVG is the primary output.** SVG preserves editable text (when `svg.fonttype='none'`),
supports lossless scaling, and allows post-hoc text adjustment in vector editors
(Illustrator, Inkscape). PDF is the LaTeX inclusion format. PNG is the raster preview.

```text
paper/figures/
  <figure-id>.svg       # primary — editable vector, text as <text> nodes
  <figure-id>.pdf       # LaTeX inclusion
  <figure-id>.png       # raster preview, dpi=300
```

Save order:
```python
fig.savefig('figures/name.svg', bbox_inches='tight')
fig.savefig('figures/name.pdf', bbox_inches='tight')
fig.savefig('figures/name.png', dpi=300, bbox_inches='tight')
plt.close(fig)  # always close to free memory
```

DPI guide (PNG only): 300 standard, 600 for dense bar panels with many methods.

Do not create shared style modules, scripts directories, derived data folders, or
audit files by default. Create extra reproducibility packaging only when the user
requests it or when a complex result figure cannot be regenerated otherwise.

### Final-Inclusion Legibility

The venue sizing file decides column span and `figsize`, but the final included
artifact must still be readable at its LaTeX width. No text element may render
below 6 pt after insertion; labels below 7 pt are allowed only for secondary
tick labels or crowded legends. When in doubt, inspect the PNG/PDF at the final
paper scale, not at an enlarged viewer zoom.

## Python Style Contract

**Apply these rcParams before any figure drawing. This is mandatory, not optional.**
Failure to apply them produces figures with wrong fonts, low resolution, and
unreadable text.

```python
import matplotlib as mpl

mpl.rcParams.update({
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
    "pdf.fonttype": 42,
    "svg.fonttype": "none",       # keeps text as editable <text> nodes
})
```

### No Content Outside Figure Bounds

**All content — labels, legends, annotations, titles — must stay within the
figure canvas.** Check these before saving:

- Legend: prefer `loc='upper right'` or `loc='best'` inside axes, or
  `bbox_to_anchor=(0.5, -0.12), loc='upper center'` below the axes.
  **Never** anchor a legend outside the figure at coordinates like 1.35.
- Labels: all bar/point annotations must fit within `set_ylim` with headroom.
- `tight_layout(pad=...)` before every `savefig` is mandatory.

### Colors

Color is an **encoding**, not decoration. Three mistakes make generated figures look
amateur (all banned by journal figure practice — no rainbow/jet colormaps; hue must not be
the *only* encoding; grayscale print must stay readable):

For named colors and palette constants, use palette names from `palette-system.md`.
Do not define new named palettes in `plot-style.md`; this file explains selection,
redundant encodings, and verification.

Unless the user explicitly supplies a palette, provides a style reference, or asks to change colors,
load `palette-system.md` and use the registered `CS_*` palettes by default. Generated Python plot
code must import or mirror `scripts/cs_palette.py` before plotting the first data series. A raw
local hex palette, matplotlib/seaborn default color cycle, or unregistered colormap is a blocking
plot defect.

1. **Shipping the library default cycle.** matplotlib's `tab10` / seaborn's default
   saturated orange/blue cycle is the single most common
   "this looks like a generated/Excel chart" tell. **Never rely on the default color cycle —
   set an explicit palette before plotting every figure.** A two-series chart in raw
   `tab:orange`/`tab:blue` is a defect even though it is "only two colors."
2. a **rainbow of maximally-distinct, saturated hues** with no hierarchy (the "Excel"
   look) — caused by hand-mixing colors of unequal luminance, and
3. using **hue as the only channel**, which collapses in grayscale print and for
   colorblind readers.

Publication palettes are **deep and slightly muted, not neon**. When a color looks
vivid/saturated on screen, desaturate or deepen it — saturated primaries are what make a
figure read as amateur. **Reduce saturation before adding categories.**

Pick color in three steps: choose the palette family **from the data structure**, add a
**redundant channel**, then **verify**.

#### Step 0 — one palette for the whole paper (define once, reuse everywhere)

Every figure in the paper should read as **one visual system**, not a set of unrelated
charts. Before generating the first plot, fix a single palette and reuse it across the bar
chart, line plot, radar, and heatmap accents. **Family consistency beats maximal hue
separation:** keep baselines in one cool family and the proposed method in one hero family.

- **One entity → one (color, marker) pair across *every* figure.** If "Method A" is the
  deep-blue series in Figure 3, it is deep blue everywhere it appears — never remapped.
- Group related entities into **families** and color by family (e.g. all "Frontier LLM"
  baselines in cool blues, all "Specialist agent" baselines in warm neutrals), rather than
  giving N equal entities N unrelated hues.
- Reserve green/red for *direction* (gain/drop/threshold), never for entity identity.
- If two figures legitimately need different palettes (different entity sets), still keep
  the same saturation level and neutral family so they look related.

#### Step 1 — choose the palette family from the DATA (not the paper, not the chart)

| Data structure | Examples | Palette family |
|---|---|---|
| **Categorical / nominal** — distinct entities of equal status | methods, models, datasets, tasks, conditions | **Qualitative** (`CS_PEER_PALETTE`) |
| **Ordered / sequential** — one quantity that increases | ablation depth, model scale, dose, rank, magnitude | **Single-hue sequential ramp** |
| **Diverging** — signed values around a reference | z-score, gain/loss vs baseline, correlation | **Diverging colormap** (`RdBu_r`) |
| **Emphasis** — one focus entity vs the rest | "our method" vs baselines | **Hero-baseline** (1 saturated + muted family) |

Two hard mismatches to avoid:
- **Never use a sequential ramp for unordered categories** — adjacent shades become
  indistinguishable and it implies an order that does not exist. (A peer comparison of
  N equal methods is categorical, so it takes the qualitative palette, *not* a ramp.)
- **Never use a qualitative palette for an ordered magnitude** — it throws away the
  ordering the reader needs.

#### Categorical → Qualitative palette (default for equal peers)

Use the Okabe–Ito set: it is colorblind-safe by construction and **luminance-balanced**,
so no series jumps out — which is exactly what "equal peers" requires:

```python
CS_PEER_PALETTE = [
    "#0072B2",   # blue
    "#D55E00",   # vermillion
    "#009E73",   # bluish green
    "#CC79A7",   # reddish purple
    "#E69F00",   # orange
    "#56B4E9",   # sky blue
]
CS_PEER_MARKERS = ['o', 's', '^', 'D', 'v', 'P']  # pair 1:1 with colors
```

- Balanced luminance → equal visual weight (the point of a peer comparison).
- Cap at **6 categories**. Beyond that, group/aggregate or use small multiples; do not
  keep adding hues. **Reduce saturation before adding categories.**
- For a **2–3 series** comparison where every series matters (e.g. one lower-is-better and one
  higher-is-better rate across methods), pick from the local publication palette so the colors stay
  consistent across the paper. For opposite-valence headline rates, use the
  `paired-opposing-scorecard` palette: use `CS_PAIRED_OPPOSING_PALETTE` with muted coral for
  lower-is-better and steel blue for higher-is-better. Do **not** ship the matplotlib
  default orange/blue, the old harsh deep-red / deep-blue pairing, or
  hand-mixed brown/clay hues — those read muddy. Do not paint one series grey; keep the legend
  frameless (`frameon=False`).
- For a **journal grouped bar with 4 methods/series**, do not use a loud four-hue set unless the
  paper needs equal-status categorical separation. Prefer a restrained family palette such as
  `CS_BODY_PASTEL_PALETTE`: three related blues plus one warm focus color.
  Use thin black outlines and, only when grayscale is a real requirement, subtle hatches rather
  than heavy pattern fills.

#### Ordered → Single-hue sequential ramp

```python
import numpy as np
sequential = plt.cm.Blues(np.linspace(0.35, 0.95, n))  # low → high, darker = larger
```

Use for ablation depth, scaling, rank, or any single increasing quantity, and for
magnitude heatmaps (`Blues`; use `Reds` only when the metric is semantically
"worse/danger/error"). Never apply a ramp to unordered method identity.

#### Diverging → signed around a reference

```python
import matplotlib as mpl
cmap = plt.cm.RdBu_r
norm = mpl.colors.TwoSlopeNorm(vcenter=0)  # red = above, blue = below
```

Use for z-scores, gain/loss vs a baseline, or correlation — anything with a meaningful
zero/center.

#### Emphasis → Hero-baseline (one focus entity)

When the paper proposes a method, make the hero the **only saturated color**; baselines are
**pale and recede**. Use a row of soft, low-saturation baselines and one deeper hero, with
the **hero placed last** so the eye lands on it. Misapplying this to a peer comparison of
equal methods invents a hierarchy that is not there.

```python
CS_HERO_COLOR = "#3775BA"   # proposed method — the one advancing color
CS_BASELINE_PALETTE = [     # all baselines — low-saturation receding colors
    "#CFCECE",   # grey
    "#DDF3DE",   # pale green
    "#FBDFE2",   # pale pink
    "#D9B9D4",   # soft lavender
    "#DAA87C",   # warm tan
    "#B4C0E4",   # soft blue-purple
]
CS_HERO_BASELINE_PALETTE = CS_BASELINE_PALETTE + [CS_HERO_COLOR]
# usage: colors = CS_BASELINE_PALETTE[:n_baselines] + [CS_HERO_COLOR]  # hero last
```

This is the right fix whenever a "many methods, one metric" bar chart would otherwise become
a row of equally-saturated hues: keep the baselines pale and let one color carry the message.

#### Step 2 — add a redundant channel (mandatory when ≥4 overlapping series, or whenever grayscale/CVD matters)

Color alone fails where lines cross, in grayscale print, and for colorblind readers.
Pair each entity with a second, non-color channel so identity survives all three:

- **Lines / scatter / radar**: a fixed `marker` per entity (`CS_PEER_MARKERS`), and a
  `linestyle` cycle if still crowded. Build legend handles with both line + marker.
- **Bars / filled areas**: a `hatch` per entity when neighboring fills are close in
  luminance or may print in grayscale.

```python
HATCHES = ['/', '\\\\', '.', 'x', 'o', '+', '*', 'O']
```

#### Step 3 — verify (folds into the Display Review Gate "low contrast" check)

- **Grayscale**: render or imagine a desaturated copy; every series must still be
  distinguishable (this is why Step 2 exists).
- **Colorblind**: `CS_PEER_PALETTE` is CVD-safe by construction. For any
  hand-picked colors, sanity-check a deuteranopia simulation.

#### Support colors

```python
CS_SUPPORT_COLORS = {
    "delta_up": "#2E9E44",
    "delta_down": "#E53935",
    "axis": "#4D4D4D",
    "neutral_mid": "#767676",
    "neutral_light": "#D8D8D8",
}
```

#### Rules (all families)

- One entity = one **(color, marker)** pair across every figure in the paper. Never remap.
- **Grey is neutral/receding only** — never the color of a primary metric or a foreground
  series the reader must compare. Reserve grey for backgrounds, reference lines, "other"
  buckets, and de-emphasized baselines.
- Green/red (`CS_SUPPORT_COLORS["delta_up"]` / `CS_SUPPORT_COLORS["delta_down"]`) are reserved for direction (arrows, gain/drop), not
  entity identity.
- No rainbow/jet colormaps anywhere.
- Avoid in-figure titles; put the message in the caption.
- Axis labels must be readable labels, not raw variable names.
- One visual message per plot.
- If fewer than three data points, consider a table or text instead.

### Bar Chart Rules

These rules are mandatory for every bar chart (comparison, ablation, grouped).

**Edge and separation** — every bar must have a visible outline:
```python
ax.bar(..., edgecolor=CS_SUPPORT_COLORS["edge"], linewidth=0.8)
```

**Error bars** — make them visible at print scale:
```python
error_kw = {'elinewidth': 1.5, 'capthick': 1.5, 'capsize': 4}
```

**In-bar value annotation** — luminance-aware text color for readability:
```python
def _luminance(hex_color):
    c = hex_color.lstrip('#')
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return 0.299*r + 0.587*g + 0.114*b

for bar, color in zip(bars, bar_colors):
    val = bar.get_height()
    text_color = 'white' if _luminance(color) < 128 else 'black'
    ax.text(bar.get_x() + bar.get_width()/2, val + offset,
            f'{val:.1f}', ha='center', va='bottom',
            fontsize=8, color=text_color)
```

**Dynamic y-axis** — tighten to data range, but the limits must be computed from
the **error-bar extremes, not the bar heights**. Computing `ylim` from `vals` alone
clips the whisker tips and caps — the single most common bar-chart defect. Always
include the error reach on both ends, plus headroom for value labels:
```python
# vals: bar heights; lo_err/hi_err: lengths of the lower/upper error bars
top = (vals + hi_err)            # highest whisker tip
bot = (vals - lo_err)            # lowest whisker tip
span = top.max() - bot.min()
margin = span * 0.15
label_pad = span * 0.10          # extra room above for value labels
ax.set_ylim(max(0, bot.min() - margin),
            top.max() + margin + label_pad)
```
If there are no error bars, set `hi_err = lo_err = 0`. Never set the upper limit
from `vals.max()` when error bars or in-bar labels extend above it.

**Horizontal bars for ablation** — use alpha-graduated single color:
```python
base_rgb = (0.215, 0.459, 0.729)  # hero blue
alphas = np.linspace(0.2, 1.0, n_ablations)
colors = [(*base_rgb, a) for a in alphas]
ax.barh(..., color=colors)
```

**Print-safe hatching** for grayscale readability:
```python
hatches = ['/', '\\\\', '.', 'x', 'o']
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
```

- No grid lines on bar charts.
- No title inside the figure.
- X-ticks may be hidden when the legend names the methods: `ax.set_xticks([])`.

### Line / Trend Plot Rules

- Line width: 1.5–2.5 pt.
- Marker size: 5–8 pt. Use a **distinct marker per series** (`PEER_MARKERS`) as a redundant
  channel, not the same circle for every line.
- `fill_between` uncertainty bands: alpha 0.1–0.2.
- Reference baseline as dashed horizontal line:
  `ax.axhline(y=..., linestyle='--', color='#767676', alpha=0.5, linewidth=1)`.
- No grid; sparse y-ticks guide the eye.
- Place one shared legend above a multi-panel row rather than repeating per axis.
- Fading alpha for temporal progression: higher alpha for later time segments.

### Heatmap Rules

For publication heatmaps, prefer `ax.pcolormesh` with white gridlines. It gives clean cell
separation and high readability without relying on heavy borders.

**Mandatory rules:**
- White gridlines between every cell: `edgecolors='white', linewidths=1`.
- Default colormap: `Blues` for general percentage/score data (cleanest, most common
  in CS papers). Use `Reds` only when the metric is semantically "danger/error/worse."
  Use `RdBu_r` for diverging data (positive/negative z-scores).
- Horizontal labels: `rotation=0`. Never rotate heatmap x-tick labels.
- Figure size: at least 6–10 inches wide for 6+ columns, proportional to cell count.
- Base font.size: 10–12 for readability.
- Annotations: integers with `fmt='d'` or one decimal with `fmt='.1f'`.

```python
import matplotlib.pyplot as plt
import numpy as np

# ── publication heatmap with clean cell separation ──
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.pcolormesh(data, cmap='Reds', edgecolors='white',
                   linewidths=1, vmin=0, vmax=100)
ax.invert_yaxis()  # match imshow row order

# Cell annotations — luminance-aware (decide text color from the *rendered cell
# color*, not from a hardcoded value threshold). A fixed threshold like `val > 55`
# breaks whenever vmin/vmax or the colormap change; luminance always tracks the cell.
cmap = plt.cm.Reds
norm = mpl.colors.Normalize(vmin=0, vmax=100)
for i in range(n_rows):
    for j in range(n_cols):
        val = data[i, j]
        r, g, b, _ = cmap(norm(val))
        lum = 0.299*r + 0.587*g + 0.114*b
        ax.text(j + 0.5, i + 0.5, f'{val:.0f}',
                ha='center', va='center', fontsize=10,
                color='white' if lum < 0.5 else 'black',
                fontweight='bold')

# Clean ticks centered on cells
ax.set_xticks(np.arange(n_cols) + 0.5)
ax.set_xticklabels(col_labels, rotation=0, fontsize=10)
ax.set_yticks(np.arange(n_rows) + 0.5)
ax.set_yticklabels(row_labels, rotation=0, fontsize=10)

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
cbar.set_label('Value (%)', fontsize=10)

fig.tight_layout(pad=1.5)
```

**Do not:**
- Use `imshow` without white gridlines — cells blend together.
- Rotate x-tick labels.
- Use tiny font sizes (< 8pt) for cell annotations.
- Use `magma` or `YlOrRd` for simple percentage/count data — they add visual
  noise without adding information.

### Radar / Polar Chart Rules

Radar charts fail in two specific ways that make most of them ugly. Avoid both:

1. **Too many overlaid traces.** The reference radar grammar supports up to six methods only when
   each method has a registered `CS_RADAR_PALETTE` color, marker, and line style. In body-compact
   mode, cap the visible methods at four. Past six methods, a single radar is unreadable.
2. **Wrong scale choice.** For same-unit 0--100 rates, keep the raw shared radial scale and show
   20/40/60/80 ticks. Use per-spoke normalization only when spokes have different units or
   incompatible ranges, and state the per-spoke scaling in the caption because raw ring values no
   longer read directly.

Styling:

- Start from top: `ax.set_theta_offset(np.pi / 2)`; clockwise: `ax.set_theta_direction(-1)`.
- Use the `CS_RADAR_PALETTE` reference grammar: muted method colors, white-filled markers,
  mixed solid/dashed/dotted line styles, and a frameless legend below the figure.
- Fill alpha: use a faint `0.04` reference fill only; never use dense filled polygons for
  overlapping radar traces. Trace linewidth should be about 1.8.
- Give each method a **distinct marker** (`CS_RADAR_MARKERS`), not just a distinct color, so
  overlapping traces stay separable at crossings, in grayscale, and for colorblind readers.
  Show the marker in the legend handles.
- Use light grey dashed radial rings, light grey spokes, grey tick labels at 20/40/60/80 for
  0--100 rate plots, a restrained charcoal outer ring, and a small neutral center dot.
- Offset spoke labels just beyond the outer ring so they never overlap data, rings, or
  radial tick text. Do not leave the default `20%–100%` radial ticks sitting on top of a
  data spoke.
- Limit to 5–8 spokes; beyond 8, switch to grouped bars or a heatmap.
- Limit to six methods for the reference radar grammar. In body-compact mode, cap the visible
  traces at four and move the rest to an appendix/table or switch chart form.
- For a single six-method radar, prefer a compact two-row legend under the polar axes. For a wide
  two-panel radar, one shared legend row below both panels is acceptable if readable.

Use the `radar_chart()` helper in `chart-patterns.md`, which enforces the registered radar palette,
trace cap, light rings, outside label placement, and shared-scale default.

### Legend Rules

- **No frame**: `ax.legend(frameon=False)` — always.
- **Inside axes preferred**: `loc='upper right'` or `loc='best'` when data area
  has clear empty space.
- **Below axes**: `bbox_to_anchor=(0.5, -0.12), loc='upper center', ncol=N` when
  4+ entries exist.
- **Dedicated legend panel**: for multi-axis figures (3+ metrics side by side),
  make the last subplot legend-only with `ax.set_axis_off()`.
- **Direct labels**: when only 2–3 lines/bars with stable identities, label them
  directly with text annotations rather than a detached legend.
- Never anchor a legend outside the figure canvas at coordinates beyond ~1.2.

### Multi-Panel Template Routing

For figures with two or more panels, load `references/figures/multi-panel-patterns.md`. This file
keeps only global style requirements such as legibility, label readability, and shared visual
consistency; panel-role templates and anti-redundancy patterns live in the multi-panel reference.

## Chart Contract

Each chart generation pass must:

1. read input data from the source path recorded in the Figure Plan,
2. normalize labels and metric direction explicitly,
3. write output files under `paper/figures/`,
4. fail loudly if expected columns or metrics are missing,
5. avoid network calls and experiment execution unless the user explicitly asks,
6. insert the chart into the LaTeX section selected by the Paper Framework.
