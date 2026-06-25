# Finance Figure Backend And Export QA

Use this reference when creating, auditing, or polishing finance figures, tables, and display
assets.

For palette and cross-figure style consistency, load `references/finance-palette.md` before
accepting a rendered plotted figure. For generated Python figures, use
`scripts/finance_palette.py` as the canonical palette registry.
For figure/table width, span, float, and final-size placement, load `references/figure-layout.md`.
For editable finance tables, load `references/table-design.md`; when LaTeX table sources exist, run
`scripts/lint_finance_tables.py` before compiled table-page inspection.

## Figure Contract

Before drawing, record:

| field | required content |
|---|---|
| core conclusion | One finance claim the display supports. |
| source-data-to-panel map | Data file, model output, table, or script for every plotted element. |
| backend | Python, R, LaTeX table, office-native table, or author-supplied asset. |
| palette profile | Paper-level palette profile and semantic mapping from `references/finance-palette.md`. |
| small-N dark-color check | If a plotted figure uses 1-4 categorical colors, confirm the `deep` token is absent unless explicitly justified. |
| layout contract | `target_layout`, `placement_width`, `float_env`, `final_width_mm`, `panel_grid`, and `layout_risk` from `references/figure-layout.md`. |
| export format | Vector PDF/SVG when possible; PNG preview for visual inspection; LaTeX `booktabs` for tables. |
| manuscript integration | `\includegraphics`, `table`/`table*`, Internet Appendix placement, or source-data mapping. |
| review risk | What a referee cannot verify if the display is missing or unclear. |

## Backend Selection Gate

Backend selection is a blocking gate for plotted figures. If the user has not explicitly chosen
Python or R and has not provided a clearly language-specific workflow, ask one concise question:
`Python or R?` Then stop and wait before drawing, previewing, exporting, or doing visual QA. Do not
infer R merely because the manuscript is econometric, and do not infer Python merely because the
workspace contains CSV files.

The selected backend is exclusive. Once Python or R is selected, use that backend for plotting
scripts, preview files, SVG/PDF/PNG exports, and final visual QA. If R is selected and `Rscript`, R,
or required R packages are unavailable, report the blocker; do not use Python, matplotlib, seaborn,
or plotly to create a substitute preview or export. If Python is selected and Python or required
plotting packages are unavailable, report the blocker; do not use R, ggplot2, or fixest to create a
substitute preview or export.

The unselected language may be used only for non-visual utilities such as file listing, text search,
CSV inspection, or format conversion that does not open a graphics device, import plotting
libraries, create image/vector files, or decide visual layout.

## Palette Consistency Gate

Before drawing the first plotted figure in a paper, choose one palette profile from
`references/finance-palette.md` and record the semantic mapping in the Display-Item Plan. Reuse that
mapping across later figures so treatment, benchmark, risk, uncertainty, and control groups do not
change color meaning from figure to figure.

Do not use neon colors, default saturated red/green contrasts, pure primary RGB colors, or unrelated
palette families across figures. If a target journal, author template, or existing manuscript
requires a different palette, record it as the paper-level palette profile and keep it consistent.
If a chart has only a few categorical colors, do not consume a dark brown/plum block simply because
it exists in the profile. Use the registered small-N order first, and reserve dark tokens for text,
sparse high-contrast marks, network nodes, or a documented semantic role.

Color must not be the only encoding for a substantive distinction. Use marker shape, line style,
hatching, direct labels, table labels, or panel annotations when grayscale printing or color-vision
limits could change interpretation.

## Layout And Placement Gate

Before drawing or placing a display, use `references/figure-layout.md` to record final size,
placement width, float environment, panel grid, first text anchor, and layout risk.

Use the narrowest readable placement. Do not promote a sparse display to `figure*` or `table*` only
because the claim is important. In two-column templates, compact displays use `figure` or `table`
with `\columnwidth`; genuinely wide or multi-panel displays use `figure*` or `table*` with
`\textwidth` only with a span justification. In single-column manuscripts, do not use `figure*` or
`table*`; use regular floats with natural, fractional, or full `\textwidth` widths.

If a wide Results float may drift past the interpretive section, record the risk and use a deliberate
float strategy such as splitting the display, moving the text anchor, or using `\FloatBarrier` where
the template permits it.

## Export Rules

- Prefer vector PDF/SVG for event studies, coefficient plots, CAR plots, factor-model displays,
  portfolio-sort figures, portfolio backtest curves, risk-return scatters, backtest panels, and
  model schematics.
- Provide a PNG preview when visual inspection or journal upload needs raster evidence.
- Keep finance tables as editable LaTeX `booktabs` tables when possible; do not rasterize
  regression, robustness, portfolio-sort, or factor-model tables unless the user explicitly asks for
  figure-style output.
- Run `scripts/lint_finance_tables.py` on LaTeX table sources before accepting table output; fix or
  block vertical rules, `\hline`, unjustified `\resizebox`, missing captions, declared-width table
  defects, and leading decimals without zero.
- Run `scripts/audit_visual_assets.py` on rendered PNG/JPG previews before marking plotted figure
  export QA as pass. Fix blank previews, likely cropped titles/axis labels/legends, and extreme
  unused margins in the plotting script rather than hiding the issue with LaTeX scaling.
- Name files with stable display IDs, for example `fig2-event-study.svg` and
  `fig2-event-study.png`.
- Keep raw and processed source data separate from rendered assets and map them to panels.

## Preview Inspection

Before marking a visual display gate PASS, inspect the final-size preview or compiled output:

- not blank, cropped, or dominated by unused margins;
- final-size text is legible;
- event-time labels, confidence intervals, legends, table cells, and axis titles do not overlap;
- selected width/span/float environment follows the layout contract and does not overflow;
- sample, unit, model, benchmark, uncertainty definition, and scaling are visible or in the caption;
- colors follow the paper-level palette profile and remain interpretable when printed;
- the display message does not exceed source evidence;
- LaTeX route has `\includegraphics` or table paths that point to existing assets.
- LaTeX full-draft route has `paper/layout-qa/layout_qa_summary.md` from
  `scripts/inspect_compiled_layout.py`, plus page PNGs or a contact sheet for the relevant table
  pages; inspect it for margin crossing, clipping, unreadable fonts, sparse full-width pages, and
  right-side underfill.
- `compiled_layout_qa_status: pass` is recorded only after both clean machine layout and
  `layout_manual_inspection_status: pass`; otherwise record `partial` or `blocked`.

## Source Data Audit

Use this table in review reports or `paper/submission-package.md` when displays are central:

| display_id | backend | palette_profile | placement_width | final_width_mm | source_data | export_files | manuscript_linkage | preview_status | blocker |
|---|---|---|---|---|---|---|---|---|---|

For plotted figures with 1-4 categorical colors, add a note field or audit comment confirming the
small-N dark-color check.

If source data, backend runtime, package dependencies, or preview evidence are absent, report the
visual display gate as BLOCKED rather than assuming the planned figure exists.
