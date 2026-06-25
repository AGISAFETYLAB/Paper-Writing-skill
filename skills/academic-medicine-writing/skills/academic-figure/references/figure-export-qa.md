# Figure Backend And Export QA

Use this reference when creating, auditing, or polishing medical figures and display assets.

## Figure Contract

Before drawing, record:

| field | required content |
|---|---|
| core conclusion | One claim the figure supports. |
| source-data-to-panel map | Data file/table/analysis output for every panel or plotted element. |
| backend | Python, R, Graphviz, Mermaid, office-native table, or author-supplied asset. |
| export format | Vector PDF/SVG when possible; PNG/TIFF preview when required; DOCX editable table for word-first tables. |
| route integration | `\includegraphics` for LaTeX, figure callout plus upload/embedded asset for Word, supplement/source-data mapping for appendices. |
| review risk | What a reviewer cannot verify if the display is missing or unclear. |

## Backend Selection Gate

Backend selection is a blocking gate for plotted figures. If the user has not explicitly chosen
Python or R and has not provided a clearly language-specific workflow, ask one concise question:
`Python or R?` Then stop and wait for the answer before drawing, previewing, exporting, or doing
visual QA. Do not infer R merely because the work is medical or biological, and do not infer Python
merely because the workspace contains CSV files.

The selected backend is exclusive. Once Python or R is selected, use that backend for plotting
scripts, preview files, SVG/PDF/TIFF/PNG exports, and final visual QA. If R is selected and
`Rscript`, R, or required R packages are unavailable, report the blocker; do not use Python,
matplotlib, seaborn, or plotly to create a substitute preview or export. If Python is selected and
Python or required plotting packages are unavailable, report the blocker; do not use R, ggplot2, or
ComplexHeatmap to create a substitute preview or export.

The unselected language may be used only for non-visual utilities such as file listing, text search,
CSV inspection, or format conversion that does not open a graphics device, import plotting
libraries, create image/vector files, or decide visual layout.

## Export Rules

- Prefer vector output for line art, flow diagrams, forest plots, calibration curves, ROC curves,
  decision curves, ICER planes, and schematic figures.
- Provide a PNG preview when visual inspection or journal upload needs raster evidence.
- Keep tables editable for word-first routes; do not rasterize manuscript tables unless the journal
  explicitly expects figure-style table images.
- Name files with stable display IDs, for example `fig1-cohort-flow.svg` and
  `fig1-cohort-flow.png`.
- Keep raw or processed source data separate from rendered assets and map them to figure panels.

## Preview Inspection

Before marking a visual display gate PASS, inspect the final-size preview or route-specific output:

- not blank, cropped, or dominated by unused margins;
- final-size text is legible;
- labels, CIs, arrows, legends, and table cells do not overlap;
- denominators, timeframe, uncertainty, and missingness are visible or in the legend/caption;
- color palette is restrained and interpretable when printed;
- the display message does not exceed source evidence;
- Word route has figure callouts and embedded or upload-ready figure files;
- Word route uses display-specific inserted sizes rather than one global figure width; inspect
  `wp:extent` values or a route-specific layout audit and block the display gate if every figure is
  the same size.
- Word preview packages include manuscript-like body text around displays so page breaks, captions,
  and editable tables are tested in a realistic prose context.
- LaTeX route has `\includegraphics` paths that point to existing assets.
- LaTeX full-draft route has `paper/layout-qa/layout_qa_summary.md` from
  `scripts/inspect_compiled_layout.py`, plus page PNGs or a contact sheet for the relevant table
  pages; inspect it for stacked labels, crowded effect estimates, sparse full-width pages, clipped
  notes, and right-side underfill.

## Source Data Audit

Use this table in review reports or `paper/submission-package.md` when figures are central:

| display_id | backend | source_data | export_files | manuscript_linkage | preview_status | blocker |
|---|---|---|---|---|---|---|

If source data or preview evidence is absent, report the visual display gate as BLOCKED rather than
assuming the planned figure exists.
If the artifact inventory says only "preview generated" or "manual final-size inspection still required", do not report the visual display gate as fully PASS. Use `PARTIAL` or `BLOCKED` wording
until the final-size preview, route-specific layout, and manuscript linkage have been inspected.
