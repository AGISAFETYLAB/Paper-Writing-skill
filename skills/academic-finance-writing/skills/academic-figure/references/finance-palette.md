# Finance Figure Palette System

Use this reference for finance plots, figure composites, and figure-like tables. A paper must use
one coherent palette profile across all figures unless a target journal or existing author style
requires otherwise.

The supplied style references show restrained teal, steel-blue, muted red, warm gold, sand, and dark
brown/plum palettes. Treat style references as visual guidance only; do not copy their content,
labels, or data into a manuscript.

Executable palette source: `scripts/finance_palette.py`.

- This Markdown file defines the policy and naming logic.
- `scripts/finance_palette.py` is the canonical Python registry for generated plotting scripts.
- If a workflow cannot import that file directly, mirror the same tokens and record the profile
  name in the Display-Item Plan.
- Do not invent ad hoc hex lists inside paper-local plotting code unless a journal or author style
  requires a named override.

## Palette Profiles

Default profile: `finance-muted`.

`finance-muted` is the default teal-warm profile. It is closest to the teal/sage/sand/gold/red-brown
reference style and is safest for most finance figures.

| Token | Hex | Use |
|---|---:|---|
| primary | `#4EAB90` | main treatment, focal series, or first portfolio |
| secondary | `#8EB69C` | benchmark, comparison model, or second focal series |
| accent | `#D94F33` | negative effect, drawdown, risk, rejection, or important warning |
| warm | `#EEBF6D` | alternative group, moderate highlight, or capacity/cost component |
| support | `#EDDCC3` | control group, light comparison bars, or soft fills |
| deep | `#834026` | high-contrast line, text-safe dark series, network nodes |
| sand | `#EED5B7` | light fill, shaded event window, table band |
| mist | `#ECF6FD` | confidence band or panel background tint |
| blush | `#FEEEED` | negative-side background tint |
| neutral_text | `#2F3540` | text and dark axes |
| neutral_grid | `#D9DCE1` | light gridlines and table rules |
| neutral_muted | `#6B7280` | secondary labels |

Alternative profile: `finance-soft-contrast`.

Use this profile when the paper needs a cooler blue/red/gold diagnostic style, such as model
comparison panels, forecast diagnostics, or appendix robustness grids.

| Token | Hex | Use |
|---|---:|---|
| primary | `#5E82A2` | focal estimate, model, or portfolio |
| secondary | `#BFC7E5` | benchmark, comparison model, or soft grouped bar |
| accent | `#D15354` | negative effect, risk, rejection, or warning |
| warm | `#E8B86C` | alternative group, cost, capacity, or neutral highlight |
| support | `#ABD8E5` | supporting series or light comparison |
| deep | `#8887CB` | high-contrast but non-black categorical fallback |
| sand | `#F9AD95` | warm fill or event-region tint |
| mist | `#ECF6FD` | confidence band or panel background tint |
| blush | `#FEEEED` | negative-side background tint |
| neutral_text | `#2F3540` | text and dark axes |
| neutral_grid | `#D9DCE1` | light gridlines and table rules |
| neutral_muted | `#6B7280` | secondary labels |

Alternative profile: `finance-warm-deep`.

Use this profile for richer composites where the paper already uses earthy teal, sand, terracotta,
and plum tones. Keep the dark plum/brown token out of small categorical charts unless it is serving
a clear semantic role.

| Token | Hex | Use |
|---|---:|---|
| primary | `#44757A` | focal series |
| secondary | `#B7B5A0` | benchmark or control |
| accent | `#D44C3C` | loss, rejection, treatment event, or risk |
| warm | `#DD6C4C` | secondary highlight |
| support | `#E5855D` | tertiary highlight |
| deep | `#452A3D` | dark contrast |
| sand | `#EED5B7` | light fill |
| mist | `#F7F1E8` | confidence band or panel background tint |
| blush | `#FCEAE6` | negative-side background tint |
| neutral_text | `#2F3540` | text and dark axes |
| neutral_grid | `#D9DCE1` | light gridlines and table rules |
| neutral_muted | `#6B7280` | secondary labels |

## Consistency Rules

- Select one palette profile in the Display-Item Plan and reuse it across the paper.
- Keep semantic mappings stable: treatment/focal = primary, benchmark/control = secondary or
  support, risk/loss/rejection = accent, uncertainty/background = mist/sand/blush/neutral.
- Small-N dark-color rule: if a categorical chart needs only 1-4 plotted colors, choose from the
  profile's small-N order and avoid `deep` by default. Use `deep` only for text, a sparse
  high-contrast line, network nodes, or a documented semantic need.
- Generic categorical charts should use the small-N order before adding red or dark tones:
  `primary`, `secondary`, `warm`, `support`, then `accent`; `deep` appears only after those or when
  explicitly requested.
- Use at most two strong hues in a single figure unless the chart is explicitly categorical.
- Avoid neon colors, rainbow palettes, default saturated red/green contrasts, and pure primary RGB
  colors.
- When a figure needs more than six categories, prefer grouping, facets, ordered heatmaps, direct
  labels, line styles, markers, or hatches instead of adding many unrelated colors.
- For heatmaps, use muted sequential or diverging palettes. The midpoint must have an economic
  meaning such as zero abnormal return, no treatment effect, or benchmark parity.
- All palettes must remain readable in grayscale print: add marker shapes, line styles, hatching,
  direct labels, or table annotations when color alone carries meaning.
- Confidence intervals and event-window shading should use low-alpha fills from `mist`, `sand`, or
  `blush`; do not use saturated opaque blocks behind data.

## Display Defaults

Use the executable helper `colors_for_display(display_family, n, profile_name)` when generating
Python plots. For R or paper-local scripts, mirror these defaults:

| Display family | Default tokens |
|---|---|
| event-study figure | primary, secondary, sand |
| parallel-trends plot | primary, secondary, sand |
| coefficient plot | primary, secondary, accent |
| cumulative abnormal return plot | primary, secondary, mist |
| long-short cumulative return curve | primary, secondary, warm |
| portfolio backtest curve | primary, secondary, warm |
| backtest performance panel | primary, secondary, accent, warm |
| drawdown and turnover plot | accent, warm, secondary |
| risk-return scatter | primary, secondary, warm, support |
| factor exposure/beta heatmap | sequential palette |
| robustness grid | diverging palette |
| robustness table | primary, secondary, accent |
| heatmap or bubble matrix | sequential palette |
| geographic exposure map | sequential palette |

## Display-Item Plan Fields

Record these fields when planning or auditing figures:

| Field | Required content |
|---|---|
| palette_profile | `finance-muted`, `finance-soft-contrast`, `finance-warm-deep`, or a named author/journal palette |
| semantic_color_map | Mapping from treatment/control/risk/benchmark/groups to palette tokens |
| grayscale_fallback | Marker, hatch, line style, label, or table note that preserves interpretation |
| consistency_check | Whether colors match earlier paper figures and why any exception is justified |
| small_n_dark_color_check | If the figure has 1-4 categorical colors, confirm `deep` is absent unless explicitly justified |

If the palette profile or semantic mapping is absent, the visual display gate is incomplete.
