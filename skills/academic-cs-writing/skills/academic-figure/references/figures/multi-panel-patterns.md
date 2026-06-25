# CS Multi-Panel Patterns

Read this before composing a figure with two or more panels. A multi-panel figure
is not a collage: every panel must support the same conclusion, carry unique
evidence, and share a consistent visual system.

## Use Rules

- Start with the one-sentence conclusion and assign one evidence role per panel.
- Prefer one primary panel plus supporting panels over a grid of equal-weight plots.
- Reuse the same method order, palette name, marker mapping, and legend order across panels.
- Use one shared legend unless panels intentionally compare different entities.
- Panel letters are small bold lowercase `(a)`, `(b)`, `(c)` near the top-left.
- If a panel does not change the reader's judgment, remove it or move it to appendix.

## Templates

### `pipeline-plus-results-row`

Use when the paper needs to connect a method/workflow to quantitative evidence.

| Panel | Role | Typical form |
|---|---|---|
| a | pipeline, architecture, framework, or benchmark construction | deterministic schematic |
| b | main outcome or headline comparison | grouped bar, horizontal bar, line, or scorecard |
| c | supporting breakdown | heatmap, ablation, radar, or compact table |

Design notes:

- Panel `a` often takes 45-60% of the width when the mechanism is the novelty.
- Panels `b` and `c` must use palette names from `palette-system.md`.
- Do not redraw the pipeline as a matplotlib chart; route it through schematic design.

### `main-result-ablation-robustness`

Use for an experiment section figure that must show the core result and why it holds.

| Panel | Role | Typical form |
|---|---|---|
| a | headline result | grouped bar, horizontal scorecard, line, or Pareto plot |
| b | ablation or component contribution | horizontal bars, delta plot, or compact table |
| c | robustness or sensitivity | line with confidence band, heatmap, distribution, or scatter |

Design notes:

- Panel `a` is the visual anchor. It should be larger than `b` and `c` when space is tight.
- Use one method ordering across panels.
- Avoid showing the same metric twice as both a bar and a heatmap unless the second panel
  shows a different statistic such as deviation, uncertainty, or subgroup behavior.

### `two-radar-shared-legend`

Use when two related taxonomies or metric groups compare the same methods.

| Panel | Role | Typical form |
|---|---|---|
| a | first capability or category group | radar chart |
| b | second capability or outcome group | radar chart |
| legend | shared method identities | one legend below both panels |

Design notes:

- Use the registered reference-style `CS_RADAR_PALETTE` grammar from `palette-system.md`.
- Keep radial scale comparable when units match. If normalization is per spoke, state it in
  the caption.
- Use only faint fills (`alpha <= 0.04`); white-filled markers and line style differences keep
  overlays readable.
- If there are more than six methods or more than eight spokes, switch to grouped bars or a heatmap.

### `heatmap-plus-summary-bar`

Use when a matrix is necessary but the reader also needs a simple takeaway.

| Panel | Role | Typical form |
|---|---|---|
| a | full matrix | heatmap |
| b | row/column aggregate, top-k summary, or selected contrast | horizontal bar, dot plot, or compact table |

Design notes:

- The heatmap carries detail; the summary panel carries the skim-readable conclusion.
- Use the same ordering in both panels.
- Summary values must be computed from the same source file recorded for the heatmap.

### `teaser-plus-evidence-row`

Use when Fig. 1 or an early overview combines a concept image with compact evidence.

| Panel | Role | Typical form |
|---|---|---|
| a | problem-setting, method idea, or qualitative scene | picture or schematic |
| b | small quantitative fact or benchmark coverage | donut, scorecard, compact bar, or mini heatmap |
| c | representative qualitative example | screenshot/case grid or small table |

Design notes:

- The teaser panel may be more visual, but it cannot invent claims, modules, datasets, or labels.
- Evidence panels must be sourced from concrete workspace data or confirmed paper facts.
- Keep the whole figure short enough for the target venue; do not ship a tall image with empty bands.

## Selection Checklist

Before rendering, record:

| Item | Required decision |
|---|---|
| Conclusion | one sentence for the whole figure |
| Pattern | one of the named templates above, or a justified custom layout |
| Evidence role | unique role for each panel |
| Layout | single-column fraction, double-column width, appendix, or supplement |
| Palette | named palette from `palette-system.md` |
| Legend | shared legend, direct labels, or dedicated legend panel |
| Export | SVG/PDF/PNG for plots and schematics; PNG plus wrapper PDF when using raster picture output |

Do not use a multi-panel figure to hide weak evidence. If the panels do not form a
single argument, split the figure or remove the weaker panels.
