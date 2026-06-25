---
name: academic-figure
description: Use when creating, revising, auditing, or polishing figures and tables for medical, clinical, biomedical, public-health, diagnostic, treatment, systematic-review, prediction-model, or health-economics manuscripts.
---

# Academic Figure — Medicine

Owns every display item in the standalone medicine package: flow diagrams, baseline/cohort tables,
outcome tables, adverse-event tables, diagnostic plots, calibration displays, forest plots, clinical
composites, image plates with quantitative companion panels, and supplements.

## Scope

This skill creates, revises, plans, and audits display artifacts for a medical manuscript. It does
not run analyses or invent values. If source data are absent, produce a Display-Item Plan or a LaTeX
shell with explicit unresolved markers.

Intent class: `figure-table-only`. Use this route when the user only asks for a figure, table,
caption, display plan, or display audit. For display-only requests, do not start the full manuscript state machine, create a
Writing Policy/Paper Framework, or generate a manuscript package for a display-only request. If the
user asks for the whole display set for an incomplete manuscript package, return to the medicine hub
and use `package-completion` so display work stays integrated with manuscript, citation, and review
gates.

## Protocol

1. Read `manifest.yaml`.
2. Load `references/figures.md`.
3. Load `references/figure-export-qa.md` before producing or accepting final figure/table
   assets.
4. Apply the **Backend Language Gate** before producing plotted figures: if the user has not chosen
   Python or R and no unambiguous language-specific workflow is provided, stop and ask `Python or R?`
   Do not cross-render with the unselected language.
5. If the user selects R or provides R scripts/data workflow, load
   `references/r-figure-workflow.md` and `references/r-chart-catalog.md`; keep all
   drawing, previewing, exporting, and visual QA in R.
6. If the user selects Python or provides Python scripts/data workflow, load
   `references/python-figure-workflow.md` and `references/python-chart-catalog.md`; keep
   all drawing, previewing, exporting, and visual QA in Python.
7. Load the selected study-type checklist when the display item is checklist-bound.
8. Read the Paper Framework Display-Item Plan when available. If absent, create one before
   generating display text.

## Display-Item Plan

For every planned display, record:

| Field | Required content |
|---|---|
| Item ID | Table/Figure/Supplement number or provisional ID |
| Claim supported | One manuscript claim the display supports |
| Source data | Table, figure, analysis report, registry, or user-provided values |
| Population/denominator | Total N, group N, exclusions, missingness |
| Timeframe | Follow-up, visit, index date, search date, or assay timepoint |
| Analysis population | ITT, per-protocol, complete-case, validation cohort, etc. |
| Estimate and uncertainty | Effect estimate, CI, SD/SE/IQR, calibration/diagnostic metric |
| Checklist linkage | CONSORT/STROBE/PRISMA/STARD/TRIPOD/etc. item when applicable |
| Status | ready / needs source / not applicable / blocking |

## Display Types

- CONSORT/SPIRIT/STROBE participant flow. A cohort flow figure must produce a real figure asset
  under `paper/figures/` when source flow counts are available; do not satisfy a planned figure only
  by placing a table captioned as a figure in the manuscript.
- PRISMA flow diagram and study-characteristics/risk-of-bias table.
- Baseline/cohort table with denominators, missingness, clinically meaningful units, and group
  counts. Treat `cohort table` as the user-facing synonym for a baseline characteristics table in
  observational cohort manuscripts.
- Primary and secondary outcome tables and bar/line figures.
- Adverse-event and harms tables and companion plots.
- Subgroup/sensitivity forest plots and tables.
- Kaplan-Meier or time-to-event curves.
- Funnel plots for evidence synthesis.
- Diagnostic 2x2 tables, accuracy metrics tables, ROC curves, precision-recall curves, calibration
  plots, and decision curves.
- Prediction-model performance tables and validation/calibration displays.
- clinical triptych displays when a clinical claim needs three aligned evidence bands, usually
  longitudinal summaries, forest-plot-style effects, and compact binary or percentage summaries.
- Image plate + quant displays when microscopy, imaging, histology, spatial overlays,
  segmentation, or blot-like images lead the evidence and must be paired with quantified companion
  panels. Require representative-image traceability, scale bars, crop/overlay notes, and the source
  data behind the quantification.
- Omics/biomarker heatmaps only when source matrices and normalization status are provided.
- Case-report timelines and diagnostic workup tables.
- Global-health data-source inventories and trend/burden plots.
- Health-economics cost/effect tables, ICER planes, tornado sensitivity plots, and model schematics.
- ICMJE/checklist/statement tables for submission packages and appendices.

## Minimum Visual Display Set

For JAMA-style or general clinical observational cohort full drafts with usable source counts,
planned event rates, and effect estimates, the main display plan must default to a minimum visual
display set instead of a table-only Results section:

- Figure 1: cohort flow diagram generated as a real vector asset under `paper/figures/`.
- Figure 2: primary/secondary outcome rate figure, usually a grouped bar, dot, or slope-style rate
  comparison with denominators visible in the legend or caption.
- Figure 3: effect-estimate forest plot when crude, adjusted, subgroup, sensitivity, or comparable
  interval estimates are available. If only one estimate exists, combine crude and adjusted values in
  one compact estimate display when both are source-supported; otherwise document why the forest plot
  is blocked.
- Table 1: polished baseline characteristics table.
- Table 2: polished primary/secondary outcomes table.

Keep the main article display budget within the target journal cap. For a JAMA-style Original
Investigation posture, 3 figures plus 2 tables is the normal main-display ceiling; additional
subgroup, missingness, checklist, or statement tables should move to the supplement/appendix unless
the framework gives a stronger reason.

The minimum visual display set is not permission to invent analyses. If a required source value is
missing, downgrade that specific figure with a visible blocker and state the blocker in the
Display-Item Plan, `paper/submission-package.md`, and review report.

## Publication-Grade Table Styling

Clinical tables must be treated as display artifacts, not raw data dumps. A table that compiles but
renders with stacked words, crowded effect estimates, oversized captions, or uneven white space fails
the table aesthetics gate.

Required table styling for main manuscript tables:

- use `booktabs` rules and compact typography such as `\small` or a justified smaller size;
- set deliberate spacing, for example `\setlength{\tabcolsep}{...}` and
  `\renewcommand{\arraystretch}{...}`, instead of relying on template defaults;
- use fixed-width text columns only where meaning-bearing text needs wrapping; numeric columns should
  stay narrow and aligned;
- for numeric-heavy baseline/cohort tables with one label column and several numeric group columns,
  prefer `booktabs` + `tabular*` with controlled inter-column fill such as
  `@{\extracolsep{\fill}}lcccc@{}`; do not default to raw equal-width `tabularx` or wide `p{...}`
  numeric columns;
- reserve `tabularx` for text-heavy tables, with deliberate text-column widths and compact numeric
  columns;
- shorten clinical row labels before allowing repeated line breaks;
- reserve a wide effect/uncertainty column for outcome tables, or split the table and move secondary
  details to a figure/supplement;
- place abbreviations, synthetic-data warnings, missingness notes, and model caveats in a compact
  table note, not in bloated column cells;
- inspect the target output before closing the display gate: compiled PDF for LaTeX routes, or
  manuscript.docx/editable companion tables for Word routes.
- record the table layout class in a route-specific layout audit when a skill script generates the
  display.

Do not use raw equal-width `tabularx` as the default for dense clinical tables. `tabularx` is allowed
only with deliberate column widths and after verifying that row labels and effect estimates remain
readable at final PDF size.

## Figure Generation QA

When generating manuscript figures from available source evidence, prefer vector PDF/SVG plus a PNG
preview when tooling permits. Apply a restrained publication style: readable final-size text,
left/bottom spines for quantitative plots, frameless legends, consistent group colors across figures,
no rainbow palette, and no repeated redundant legends.

Use `references/figure-export-qa.md` as the backend and export contract. Record the
source-data-to-panel trace, backend used, vector export path, preview path, final-size inspection
status, and any route-specific Word/LaTeX placement issue before calling a display complete.

Before returning a full draft, run a route-specific visual display gate:

- every planned main `Fig.` item has a real asset under `paper/figures/`;
- in a LaTeX route, every main figure has an `\includegraphics` call in `paper/main.tex`;
- in a Word route, every main figure has a manuscript callout and a separate figure file suitable for
  upload or embedding;
- figure captions are self-contained, with denominator, group, timeframe, metric direction,
  uncertainty definition, and abbreviations when applicable;
- image plate + quant captions include what image channel/modality is shown, scale bars, crop or
  overlay meaning, quantification denominator, and whether adjustments were global and consistent;
- rendered or previewed figures are not tiny, blank, cropped incorrectly, or dominated by unused margins;
- text does not overlap at the final PDF size;
- the figure message does not exceed the source evidence.

## Layout Rules

Choose the display width from the claim and content, not from a single global default.

- In two-column manuscripts, compact displays use `figure` or `table` with `\columnwidth`.
- Flow diagrams, multi-panel outcome displays, long-label forest plots, calibration plus decision
  curves, wide outcomes tables, and wide harms tables use `figure*` or `table*`.
- clinical triptych displays usually use a cross-column `figure*`: keep columns semantically
  parallel across the top longitudinal row, middle forest/effect row, and bottom summary row.
- clinical triptych figures must use a centered outer grid, reserve vertical space between evidence
  bands, and anchor panel labels inside or flush with axes. Negative x-position panel labels are a
  layout defect because they expand the crop and make the figure appear shifted.
- Image plate + quant displays usually use a cross-column `figure*` when representative images and
  companion quantification must be read together; use black background only inside image cells, not
  behind ordinary charts or the whole page.
- image plate + quant layouts must reserve most width for the image plate, reserve readable width for
  the quantification panel, and keep a visible gutter between them. Panel `a` belongs near the left
  edge of the image plate, not after the image plate has drifted toward panel `b`.
- Short-label forest plots with few rows should remain single-column; do not promote them to
  cross-column merely because they contain confidence intervals.
- Flow diagrams must be cropped to their active node area before placement. Large blank margins
  inside the image file are a figure-generation defect, not a LaTeX sizing problem.
- Compact flow diagrams that need less than about two thirds of `\textwidth` should remain
  single-column; do not create a full-width float just to center a small diagram.
- Single-panel heatmaps are single-column unless the matrix, labels, clustering annotation, or panel
  count requires cross-column space.
- Small heatmaps with short labels should usually be capped near 0.70-0.80 `\columnwidth` instead of
  being stretched to fill the column.
- Simple schematics with few steps and short labels are single-column; reserve cross-column space
  for branched or label-heavy schematics.
- Table 2-style primary/secondary outcomes need a deliberately wide effect-estimate column.
- Table 3-style harms/adverse-event tables need wide definition/severity/denominator notes when
  present.
- Cohort tables follow baseline-table rules: use compact clinical labels first, then widen or split
  only when denominators, units, missingness, or long characteristic labels would wrap badly.
- Evidence-synthesis, statement, and checklist tables with long text fields should be cross-column
  with custom fixed-width columns, not narrow equal columns.
- Baseline tables should first use compact clinical labels and short group headers; if a table
  still wraps heavily, switch to a wider table instead of tolerating stacked one-word lines.
- Baseline or statement tables that contain long labels, units, missingness, or action notes should
  use cross-column/wide table rules before one-column wrapping becomes visually dominant.
- Do not stretch a short table across the full text width when it leaves large empty right-hand
  space. Use the narrowest readable width and give extra width only to meaning-bearing text columns.
- Flush or barrier Results floats before Discussion when wide floats would otherwise land after the
  interpretive section.
- Generated preview routes should run `scripts/audit_display_layout.py` or an equivalent
  route-specific layout audit before the visual display gate is marked complete.

## Legend Completeness

Treat legend completeness as a blocking display QA item for submission-facing figures.

Every legend must be self-contained. Include figure title, what each panel shows, denominator,
sample size, analysis population, timeframe, statistical test, error-bar/uncertainty definition,
abbreviation definitions, and representative/panel note when relevant.

## Hard Rules

- no fabricated values, sample sizes, p values, confidence intervals, subgroup counts, or adverse
  events;
- no hidden missingness in baseline or outcome tables;
- no display whose message is stronger than the source evidence;
- every display must support one manuscript claim;
- unresolved display data must remain visible to `academic-review`, never hidden in polished prose.
