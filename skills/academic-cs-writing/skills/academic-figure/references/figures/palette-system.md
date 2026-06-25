# Palette System

Use this file as the single palette registry for CS paper figures. The executable
companion is `scripts/cs_palette.py`; generated Python plotting scripts should import
or mirror those canonical names and record the palette family they use.

Default rule: unless the user explicitly supplies a palette, provides a style reference,
or asks to change colors, load this file and use one of the registered palettes below.
Unregistered local hex palettes and library default color cycles are blocking failures.

## Ownership

- `palette-system.md` is the single source of truth for named palettes.
- No other academic-figure reference owns palette definitions.
- `scripts/cs_palette.py` is the executable registry used by Python plotting helpers.
- `plot-style.md` explains selection and verification rules.
- `chart-taxonomy.md` maps chart families to palette names.
- `chart-patterns.md` may mirror palette constants only so code snippets remain runnable.
- Do not define new hex palettes in other files. Add the named palette here first, then
  update `scripts/cs_palette.py` and references that need to point to it.
- A user-provided style reference can influence visual grammar, but colors still resolve to a named
  `CS_*` palette unless the user explicitly requests a new or different palette.

## Naming Contract

Use canonical `CS_*` names only. Avoid older context-specific aliases because they hide the
actual design role of the palette.

| Canonical name | Role |
|---|---|
| `CS_PEER_PALETTE` | equal-status methods, models, systems, datasets, tasks, or conditions |
| `CS_BODY_PASTEL_PALETTE` | quieter grouped bars or compact body figures |
| `CS_HERO_BASELINE_PALETTE` | one focus or proposed method versus muted baselines |
| `CS_COVERAGE_PALETTE` | benchmark coverage, task taxonomy, dataset composition, or whole-part panels |
| `CS_PAIRED_OPPOSING_PALETTE` | paired foreground metrics with opposite direction |
| `CS_RADAR_PALETTE` | single-panel or shared-legend radar/profile comparisons |
| `CS_QUALITATIVE_PANEL_PALETTE` | screenshots, qualitative grids, and subtle callout frames |
| `CS_SUPPORT_COLORS` | text, grid, edge, leader-line, and directional annotation colors |

## Palette Presets

Choose the palette from the data relationship, not from visual preference.

| Palette name | Use when | Colors / rule |
|---|---|---|
| `CS_PEER_PALETTE` | equal-status CS entities need categorical separation | restrained Okabe-Ito-derived colors plus one marker per entity; cap at 6 entities before grouping or small multiples |
| `CS_BODY_PASTEL_PALETTE` | a figure needs a quieter, low-saturation family for grouped bars or compact body plots | related pale blues, warm focus coral, and soft neutrals |
| `CS_HERO_BASELINE_PALETTE` | one proposed method or focus entity should stand out against baselines | muted baseline colors plus one deeper hero color, with the hero placed last |
| `CS_COVERAGE_PALETTE` | benchmark, dataset, task, or taxonomy coverage is shown as a donut, pie, stacked bar, or coverage panel | muted categorical fills with white separators; labels carry short codes and the caption carries denominator/definitions |
| `CS_PAIRED_OPPOSING_PALETTE` | paired headline rates have opposite valence, such as one lower-is-better metric and one higher-is-better metric | muted coral for the lower-is-better foreground metric and steel blue for the higher-is-better foreground metric |
| `CS_RADAR_PALETTE` | one or more radar/profile panels compare the same method set | muted coral, steel blue, green, gold, purple, and neutral grey; use white-filled markers, mixed line styles, light grey rings, and at most faint polygon fills (`alpha <= 0.04`) |
| `CS_QUALITATIVE_PANEL_PALETTE` | screenshots, qualitative grids, or example panels need subtle status/region/category accents | use neutral frames first, then restrained accents; never let accent colors imply unverified performance or labels |

### `CS_PEER_PALETTE`

```python
CS_PEER_PALETTE = [
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
]
CS_PEER_MARKERS = ["o", "s", "^", "D", "v", "P"]
```

Use this for equal peers when no method is visually privileged. Pair each color with
a marker or hatch; do not rely on hue alone. Do not use true black as a normal
categorical plotting color. If more than six entities need equal status, group them,
use small multiples, or move detailed comparison to a table.

### `CS_BODY_PASTEL_PALETTE`

```python
CS_BODY_PASTEL_PALETTE = [
    "#C7D7EA",
    "#8FB3D1",
    "#5F8FB8",
    "#D07A68",
    "#D8C7DD",
    "#C9D8C5",
]
```

Use the pastel family for restrained body figures and grouped bars when a louder
equal-peer palette would dominate the page.

### `CS_HERO_BASELINE_PALETTE`

```python
CS_HERO_COLOR = "#3775BA"
CS_BASELINE_PALETTE = [
    "#CFCECE",
    "#DDF3DE",
    "#FBDFE2",
    "#D9B9D4",
    "#DAA87C",
    "#B4C0E4",
]
CS_HERO_BASELINE_PALETTE = CS_BASELINE_PALETTE + [CS_HERO_COLOR]
```

Use this when the paper has one proposed method or focus entity. Baselines stay pale;
the hero color appears last so the reader lands on it.

### `CS_COVERAGE_PALETTE`

```python
CS_COVERAGE_PALETTE = [
    "#4B8BBE",
    "#6BA3CF",
    "#8FBCDB",
    "#E3A86D",
    "#E08F72",
    "#7DBD9C",
    "#B1A1C8",
]
```

Use for a single whole-part snapshot such as benchmark coverage, task taxonomy,
dataset composition, or category distribution. Keep white separators between
segments and move long definitions into the caption or legend.

### `CS_PAIRED_OPPOSING_PALETTE`

```python
CS_PAIRED_OPPOSING_PALETTE = {
    "lower_better": "#C97B6B",
    "higher_better": "#5E8FB8",
}
```

Use this only for paired foreground metrics with opposite direction. The two series
are both primary; do not make either one grey.

### `CS_RADAR_PALETTE`

```python
CS_RADAR_PALETTE = [
    "#C97B6B",
    "#5E8FB8",
    "#5DA88A",
    "#D4A64E",
    "#8E7FB8",
    "#9B9B9B",
]
CS_RADAR_MARKERS = ["o", "s", "^", "D", "o", "s"]
CS_RADAR_LINESTYLES = [
    "-",
    "-",
    (0, (6, 3)),
    (0, (6, 3)),
    (0, (2, 2)),
    (0, (2, 2)),
]
CS_RADAR_TICKS = [20, 40, 60, 80]
CS_RADAR_GRID_LINESTYLE = (0, (5, 5))
CS_RADAR_FILL_ALPHA = 0.04
```

Use for single-panel radar figures and paired radar panels that share methods. This is the
default registered reference-style radar grammar:

- 0 degrees at the top, clockwise spokes.
- Muted six-color method palette in the exact order above.
- White-filled markers with colored edges, 1.8 pt lines, and line styles from
  `CS_RADAR_LINESTYLES`.
- Light grey dashed radial rings, light grey spokes, a restrained charcoal outer ring, and a small
  neutral center dot.
- Bold deep-blue spoke labels placed outside the outer ring with visual-angle-aware alignment.
- Radial ticks shown at 20/40/60/80 for 0--100-style rate plots; allow the actual axis limit to
  expand when a value exceeds the top labeled tick.
- Use a frameless legend below the figure. For a single six-method radar, use a compact two-row
  legend; for a wide two-panel shared radar, a one-row shared legend is acceptable when it remains
  readable.
- Use at most a very faint polygon fill (`alpha <= 0.04`). Never use dense filled polygons for
  overlapping method profiles.

### `CS_QUALITATIVE_PANEL_PALETTE`

```python
CS_QUALITATIVE_PANEL_PALETTE = {
    "frame": "#D8D8D8",
    "text": "#4D4D4D",
    "focus": "#5E8FB8",
    "warning": "#C97B6B",
    "success": "#5DA88A",
    "neutral_fill": "#F5F5F5",
}
```

Use for qualitative grids, screenshots, image examples, and callout frames. These
colors are visual annotations only; they must not invent class labels, result
statuses, or claims not present in the paper evidence.

### `CS_SUPPORT_COLORS`

```python
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
```

Use support colors for structure, labels, gridlines, leader lines, and directional
annotations. They are not entity colors. Green/red support colors are directional only.

## Global Rules

- One entity keeps the same `(color, marker)` pair across every figure in the paper.
- Same metric semantics keep the same direction, colormap, and label convention.
- Green/red are directional annotation colors only; do not use them as entity identity.
- Do not use rainbow or jet colormaps.
- Do not use true black as a normal categorical plotting color.
- Paper-local plotting scripts may mirror hex constants from this file, but they must record the
  registered palette name they use. An unnamed raw-hex `PALETTE` in a generated plotting script is a
  blocking audit failure because it bypasses the shared visual system.
- Add markers, hatches, line styles, direct labels, or panel grouping when color alone
  would carry identity.
- Any palette selected from a bundled asset or external example must be recorded as
  `style-only extraction` and then normalized to one of the named palettes above unless
  the user explicitly asks for a new named palette.
