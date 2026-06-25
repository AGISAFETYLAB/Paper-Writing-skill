# Finance Figure Layout And Placement

Use this reference after the display family is chosen and before rendering or placing a figure/table
in the manuscript. It owns final size, span, float environment, body-vs-appendix placement, and
layout QA. Use `figure-export-qa.md` for backend/export checks, `finance-palette.md` for color, and
the R/Python chart catalogs for display-family selection. For table-specific venue rules, content
hygiene, provenance, skeleton choice, and page-budget cost, apply `table-design.md` before this
layout step.

## Layout Contract

Record these fields in the Display-Item Plan or figure/table execution note:

```text
Final size:
```

| Field | Required content |
|---|---|
| target_layout | `single-column manuscript`, `two-column journal`, `working paper`, `appendix`, or target-venue override |
| placement_width | `inline`, `single-column`, `double-column`, `appendix-full-width`, or `supplement` |
| float_env | `figure`, `figure*`, `table`, `table*`, `sidewaystable`, or office-native placement |
| final_width_mm | Intended final rendered width, not only plotting-script `figsize` |
| aspect_ratio | `compact`, `wide`, `tall`, `square`, or explicit ratio |
| panel_grid | `1x1`, `1x2`, `2x2`, `asymmetric`, `hero-plus-support`, or table layout class |
| text_anchor | First section/paragraph where the display is cited |
| layout_risk | Main risk: unreadable text, cramped labels, float drift, sparse full-width use, or overflow |

Official target-venue instructions override these defaults. If the venue facts are unknown or stale,
record an open decision rather than guessing.

## Width Presets

Use millimeter targets as output-size presets. The plotting backend can use inches internally, but
the QA decision is based on final manuscript size.

| Placement width | Typical width | LaTeX target | Use when |
|---|---:|---|---|
| inline | 60-80 mm | fraction of `\linewidth` | Small schematic, compact timeline, simple diagnostic |
| single-column | about 89 mm | `\columnwidth` or `\linewidth` | One main axis, short labels, compact legend |
| mid-width | 120-140 mm | fraction of `\textwidth` in one-column drafts | Working-paper figures that need more room but not full page width |
| double-column | 170-183 mm | `\textwidth` via `figure*` or `table*` in two-column templates | Multi-panel or wide comparison that must be read across panels |
| appendix-full-width | 170-183 mm | appendix `\textwidth`; rotate/split if still too wide | Dense robustness, variable dictionary, wide portfolio/factor tables |

Keep dense journal body/tick/legend text readable at final size, usually 5-7 pt. Panel labels should
remain visible at final size, usually around 8 pt for journal-style figures.

## Single-Column Versus Double-Column

Default to the narrowest readable placement. Do not make a display double-column merely because it is
important. Promote only when the content needs horizontal space or cross-panel comparison.

### Usually single-column

- simple event-study figure with readable event-time labels
- compact coefficient plot with short labels and one uncertainty interval per row
- single CAR or cumulative return curve
- single portfolio backtest curve with one benchmark and short legend
- compact risk-return scatter with few labeled strategies or portfolios
- distribution, binscatter, or outlier/winsorization diagnostic
- short institutional timeline or simple mechanism schematic
- small missingness, panel coverage, or balance diagnostic
- short-label forest/coefficient plot with fewer than about eight rows

### Usually double-column

- multi-panel evidence composite, hero-plus-support figure, or asymmetric figure
- event-study or coefficient plot with many event periods, groups, or long labels
- factor exposure/beta heatmap, robustness heatmap, bubble matrix, or large panel coverage heatmap
- map, network/exposure graph, Sankey/alluvial funding flow, or label-heavy institutional diagram
- backtest panel combining cumulative return, drawdown, turnover, risk-return scatter, and benchmark panels
- synthetic-control path plus placebo or weight/balance companion panels
- structural/macro-finance grids: IRFs, model fit, counterfactuals, comparative statics
- ML/text displays with multiple metrics, models, topics, or validation panels

### Usually table* or appendix-full-width

- regression tables with many specifications, fixed-effect rows, or robustness columns
- robustness tables with many alternative samples, windows, controls, clustering rules, or benchmark models
- portfolio-sort and factor-model tables with many quantiles, alphas, and factor models
- variable dictionaries, sample construction ledgers, merge diagnostics, code-to-output maps
- dense robustness grids, placebo tables, and appendix matrices

## Template Rules

### Single-column manuscript or working paper

- Use regular `figure` and `table`, not `figure*` or `table*`.
- Small displays may use natural width or 0.65-0.85 `\linewidth`.
- Claim-critical but genuinely wide figures can use 0.9-1.0 `\textwidth`.
- Do not stretch sparse displays across the whole page; add supported comparison structure or keep
  them compact.

### Two-column journal layout

- Compact displays use `figure` or `table` with `\columnwidth` or less.
- Wide displays use `figure*` or `table*` with `\textwidth` only when there is a span
  justification.
- `figure*` and `table*` often float to a page top or later page. If a display must be read exactly
  at the first discussion point, split it into single-column displays or move the discussion to the
  float's landing page.
- Use `[t]` or `[tbp]` deliberately; do not rely on bare `[h]` for layout-critical floats.
- Use `\FloatBarrier` or a deliberate `\clearpage` before Discussion or Appendix when wide Results
  floats would otherwise drift after interpretive text. Do not overuse barriers if they create empty
  pages.

### Word-first or office-native route

- Do not use LaTeX labels such as `figure*` or `table*` in the user-facing plan.
- Record the upload/embedded asset, manuscript callout, target width, and whether the figure is
  inline, full-page, or supplement-bound.

## Table Overflow Ladder

A table wider than its declared container is a hard defect.

1. If it exceeds `\columnwidth` but fits `\textwidth`, use `table*` only when the table is
   body-worthy and full-width-justified; otherwise split, abbreviate, or move detail to appendix.
2. If it still exceeds `\textwidth`, rotate, split by column groups, transpose, or move to
   supplement.
3. Use `\small`, `\footnotesize`, or `\resizebox` only after the layout is logically correct. Do
   not resize prose-heavy or label-heavy tables as the primary fix.

Numeric columns should use `r`, `c`, or `siunitx S`; wrapping columns should be reserved for
meaning-bearing prose. Do not use equal-width text columns for dense numeric regression,
portfolio-sort, or factor-model tables.

Before compiled layout QA, run `scripts/lint_finance_tables.py` on the LaTeX table sources. Static
lint does not replace visual inspection, but it catches source-level defects such as vertical rules,
`\hline`, unjustified `\resizebox`, declared-width `tabularx` without a real `X` column, and leading
decimals without zero.

## Declared-Width Table Rule

A declared full-width table must visibly use the width it declares. Treat an underfilled
declared-width table as a layout defect, not a harmless aesthetic preference.

- `tabular*{\linewidth}` / `tabular*{\textwidth}` is appropriate for numeric-heavy tables only when
  the column spec includes `@{\extracolsep{\fill}}` or an equivalent deliberate fill mechanism.
- `tabularx{\linewidth}` / `tabularx{\textwidth}` is appropriate only when at least one real
  meaning-bearing text column is `X` or a custom bounded text column. Do not use `tabularx` merely to
  draw full-width rules around compact numeric cells.
- If a table has four or fewer short columns, keep it natural width or a narrow fraction of
  `\linewidth`; do not stretch it to `\textwidth` and leave right-hand space.
- If a dense finance table needs full width, spend width on the economic label, effect/uncertainty,
  benchmark/model, or sample-definition column; keep numeric estimates compact and aligned.

An underfilled declared-width table usually appears in the compiled PDF as full-width horizontal
rules with most cells packed against the left side and a large blank right-hand space. Fix it by
using natural width, adding `@{\extracolsep{\fill}}`, adding a real `X`/bounded prose column, or
splitting the table into logically comparable panels.

After compiling a LaTeX full draft, run
`scripts/inspect_compiled_layout.py paper --pages tables --out-dir paper/layout-qa`. The
`layout_qa_summary.md` and contact sheet are required evidence for table-page inspection; visible
right-hand underfill, margin crossing, clipping, unreadable font, or sparse full-width float pages
must be fixed before accepting the layout QA gate.

## Panel And Legend Rules

- Every panel must support the same figure-level conclusion while answering a distinct question.
- Do not force equal panel sizes when the evidence is not equally important.
- Use a hero panel only when one display carries the main evidence; keep robustness and diagnostic
  panels visually quieter.
- Prefer shared legends or direct labels. Repeated legends across small panels waste scarce width.
- Use fixed gutters and aligned baselines for multi-panel figures; do not let panel labels expand
  the crop by sitting far outside axes.
- Crop flow diagrams, maps, and schematics to their active content area before manuscript placement.
  Large blank margins inside image files are rendering defects, not LaTeX sizing issues.

## Layout QA Gate

Before accepting a display:

- final-size text is readable at the declared placement width;
- labels, CIs, legends, table cells, and notes do not overlap;
- the selected `placement_width` matches the claim and content density;
- `figure*`/`table*` use has a span justification and does not create sparse full-width pages;
- every display is cited from the text before or near where it appears;
- appendix displays pass the same width, overflow, caption, and source-data checks as body displays;
- table pages have an `inspect_compiled_layout.py` artifact (`layout_qa_summary.md` plus page PNGs or
  contact sheet) and no visible underfilled declared-width table;
- any float-order risk is recorded in `layout_risk`.
