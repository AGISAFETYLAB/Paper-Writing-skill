# Medicine Figures And Tables

Every display is evidence. It must support one manuscript claim, have an identified source, and
state denominator, analysis population, timeframe, metric direction, uncertainty, and missingness
when applicable.

Common display items:

- RCT: CONSORT flow diagram, baseline table, primary/secondary outcome tables, harms table
- observational study: cohort flow, cohort table/baseline table, adjusted association table,
  sensitivity table
- systematic review: PRISMA flow diagram, risk-of-bias table, forest plot, funnel plot when relevant
- diagnostic study: participant flow, 2x2 table, sensitivity/specificity table, ROC curve,
  precision-recall curve when positive-class performance or class imbalance matters
- prediction model: calibration plot, discrimination table, external validation table, decision curve
- imaging, pathology, or biomarker study: image plate + quant figure when representative images lead
  the claim and quantified companion panels are available
- case report: patient timeline, diagnostic workup table, follow-up summary
- global health: data-source inventory, stratified burden estimates, uncertainty intervals
- health economics: model schematic, cost/effect table, ICER plane, sensitivity analysis

## Minimum Visual Display Set For Observational Cohort Drafts

When source evidence supports it, a clinical observational cohort full draft should not collapse the
Results section into text plus tables only. Plan the main display set as 3 figures plus 2 tables,
while staying within the target journal's main display cap:

| Item | Required role | Source basis | Main/supplement default |
|---|---|---|---|
| Figure 1 | cohort flow diagram | screened, excluded, analytic, and group denominators | main |
| Figure 2 | outcome rate comparison | event counts and group denominators for primary/secondary outcomes | main |
| Figure 3 | effect-estimate forest plot | crude/adjusted/subgroup/sensitivity estimates with CIs | main when supported, otherwise blocker |
| Table 1 | baseline characteristics / cohort table | group denominators, units, missingness or explicit absence | main |
| Table 2 | primary/secondary outcomes | event counts, rates, risk differences, effect estimates, caveats | main |

Move subgroup detail tables, missingness summaries, checklist matrices, and statement inventories to
the supplement/appendix unless the framework explains why they need main-text display space. For a
JAMA-style Original Investigation posture, the normal main-display ceiling is no more than 5 total
tables/figures, so the preferred set is exactly 3 figures and 2 tables when all source values exist.

Missing values do not license invention. If an effect-estimate forest plot, rate plot, or flow figure
cannot be generated from provided evidence, the Display-Item Plan must mark it blocked and explain the
specific missing source.

## Supported Display Catalog

Figure types:

- CONSORT participant flow diagram
- PRISMA flow diagram
- primary and secondary outcome bar/line plots
- adverse-event or harms bar plot
- subgroup or sensitivity forest plot
- Kaplan-Meier or time-to-event curve
- funnel plot for evidence synthesis
- ROC curve
- precision-recall curve
- calibration plot plus decision curve
- clinical triptych
- image plate + quant
- biomarker/omics heatmap
- case-report patient timeline
- global-health trend or burden estimate plot
- ICER plane
- tornado sensitivity plot
- trial, model, diagnostic, or health-economic schematic

Table types:

- display-item plan table
- baseline characteristics table / cohort table
- primary and secondary outcomes table
- adverse-event/harms table
- subgroup or sensitivity table
- risk-of-bias or study-characteristics table
- diagnostic 2x2 table
- diagnostic accuracy metrics table
- prediction-model performance table
- case timeline/workup table
- global-health data-source inventory table
- health-economics costs/effects table
- ICMJE-oriented statement table

## Display Plan Fields

| Field | Required content |
|---|---|
| Claim supported | One manuscript claim, not a broad theme |
| Source data | Result file/table/figure/user-provided values |
| Denominator | Total N and group N; exclusions/missingness if applicable |
| Timeframe | Follow-up, visit, assay timepoint, search date, or horizon |
| Analysis population | ITT, per-protocol, complete-case, derivation/validation cohort |
| Uncertainty | CI, SD, SE, IQR, prediction interval, heterogeneity, calibration |
| Checklist link | CONSORT/STROBE/PRISMA/STARD/TRIPOD/etc. item if applicable |
| Layout class | single-column, cross-column, or supplement/appendix |

## Table Standards

- Baseline tables and cohort tables include denominators, missingness, and clinically meaningful
  units. Use `cohort table` as the observational-study synonym for a baseline characteristics table
  unless the target journal defines a different table shell.
- For JAMA/STROBE cohort manuscripts, Table 1 must normally include an Overall column when source
  evidence supports it, exposure/comparator group columns, standardized differences, and either a
  missing values column or a precise missingness footnote/eTable linkage. If an Overall column,
  missing values, variable units/ranges, or the standardized difference definition cannot be derived
  from source evidence, mark the table field as `needs source` rather than silently omitting it.
- For JAMA/STROBE outcome tables, Table 2 must distinguish prespecified primary and secondary
  outcomes, provide event counts and denominators, risk differences with 95% CI when
  source-supported, crude OR with 95% CI when source-supported, and table notes defining CI,
  outcome windows, and any model/provenance caveat. Missing risk difference 95% CI or crude OR with
  95% CI is a content-completeness gap, not merely a styling issue.
- JAMA-style Word tables should be editable and should use restrained AMA table styling. Prefer
  sparse horizontal rules or minimal visible borders over dense full grids when the output route
  supports it; the audit should still verify readability, cell boundaries, table-grid structure, and
  editable text. Do not rasterize tables.
- Main manuscript tables must pass a table aesthetics gate: they use `booktabs`, compact typography,
  deliberate `\tabcolsep` and `\arraystretch`, and custom column widths that prevent stacked words.
- Numeric-heavy baseline/cohort tables with one characteristic column and several numeric group
  columns should default to a `booktabs` + `tabular*` layout with controlled inter-column fill, for
  example `@{\extracolsep{\fill}}lcccc@{}`. Do not use raw equal-width `tabularx` or wide `p{...}`
  numeric columns for this table shape.
- Use `tabularx` only when the table is genuinely text-heavy. In that case, assign width to the
  meaning-bearing text column and keep numeric columns compact.
- Baseline tables should use compact clinical labels and short group headers before escalating to
  cross-column layout. Avoid row labels that force one word per line in a single-column table.
- Baseline tables with long characteristic labels, units, and missingness columns should move to a
  cross-column table before they become stacked or one-word-per-line in a side column.
- Outcome tables separate primary, secondary, safety, subgroup, and sensitivity results.
- Primary/secondary outcome tables must not compress the effect-estimate column. Use a wider
  effect/uncertainty column, a `table*`, landscape/supplement placement, or a split table if needed.
- Adverse-event tables include denominator, event definition, severity/seriousness when available,
  and analysis population.
- Harms tables must reserve enough width for severity, seriousness, definition, and denominator
  notes; avoid narrow equal-width columns for these fields.
- Diagnostic tables define index test, reference standard, threshold, indeterminate results, and
  confidence intervals.
- Prediction-model displays distinguish development, internal validation, and external validation.
- Precision-recall curves must report the positive class, prevalence, threshold direction, and
  whether average precision or another summary is claimed.
- Table notes should carry abbreviations, missingness, synthetic-data caveats, and model-status
  caveats; do not pack long caveats into data cells.
- Inspect the target output before closing the display gate. For LaTeX routes, render the compiled PDF
  and inspect table pages. For Word routes, inspect `manuscript.docx` or the editable table companion
  files. A source table that renders with stacked labels, overlapping notes, or unreadable effect
  estimates is not publication-grade.
- When a table is generated by a skill script, record the table layout class in a route-specific
  layout audit so later checks can distinguish a numeric-heavy clinical table from a text-heavy table.

## Actual Manuscript Layout QA

Preview-package audits and source-level table checks are not enough for a finished manuscript. The
final route-specific artifact must be inspected because table floats, captions, notes, and page
breaks can fail only after compilation or Word rendering.

For LaTeX-first routes, run compiled layout QA after `paper/main.pdf` exists:

```bash
python3 <academic-medicine-writing>/skills/academic-figure/scripts/inspect_compiled_layout.py paper --pages tables --out-dir paper/layout-qa
```

Keep `paper/layout-qa/layout_qa_summary.md` plus the page PNGs or contact sheet as the evidence
artifact. Inspect every rendered table page for stacked-word labels, crowded effect/CI fields,
right-hand space or right-side underfill, clipped notes, unreadable font, sparse full-width table
pages, and float order drift. A table aesthetics gate cannot pass if this artifact is missing for a
LaTeX-first route.

For generated preview routes, `scripts/audit_display_layout.py` still checks the preview package
geometry. It does not replace actual manuscript compiled layout QA. For Word-first routes, use the
DOCX structure/layout audit and editable table companion files instead of requiring `main.pdf`.

## Figure And Float Layout

- Match figure width to the claim. Compact ROC, precision-recall, funnel, ICER, tornado, harms, and
  time-to-event plots can be single-column when labels remain readable.
- Use cross-column layouts for CONSORT/PRISMA flows, multi-panel outcomes, long-label forest plots,
  calibration plus decision-curve panels, clinical triptych figures, image plate + quant figures,
  and any plot whose labels or uncertainty intervals become cramped in one column.
- Clinical triptych figures should keep the three evidence bands visually parallel: longitudinal or
  repeated-measure summaries on top, forest/effect displays in the middle, and compact binary or
  percentage summaries at the bottom.
- Clinical triptych figures must use a centered outer grid with reserved left/right margins, enough
  vertical space between evidence bands, and panel labels anchored inside or flush with axes. Do not
  place panel labels at negative x positions that expand the crop and make the figure appear shifted.
- Image plate + quant figures must pair representative images with quantification rather than using
  images as decoration. Keep black backgrounds only inside image cells, include scale bars and crop
  or overlay notes, and make the denominator behind the quantitative panel visible.
- Image plate + quant figures must use an outer grid that reserves most width for the image plate,
  a readable fixed companion width for the quantification panel, and a visible gutter between the two.
  Panel `a` should be anchored near the left edge of the image plate, not after the plate has drifted
  toward the quantification panel.
- Do not enlarge a forest plot only because it has uncertainty intervals. A short-label forest plot
  with fewer than about eight rows should usually remain single-column; use cross-column only when
  row labels, strata count, or interval annotations become unreadable.
- Flow diagrams should be cropped to the active node area before manuscript placement. Do not leave
  large top/bottom margins inside the image file and then compensate by shrinking the display.
- Do not use `figure*` for a compact flow diagram that is visually narrower than about two thirds of
  `\textwidth`; place it as a single-column figure to avoid a full-width float with large blank space.
- Do not make a single-panel heatmap cross-column by default. A compact heatmap with short row/column
  labels belongs in one column; use cross-column only for large clustered matrices, long labels, or
  multiple heatmap panels.
- Small heatmaps with fewer than about 100 cells should usually stay at roughly 0.70-0.80
  `\columnwidth` unless label legibility requires more.
- Do not use one uniform full-width rule for all figures.
- When drafting in a double-column shell, flush Results floats before Discussion if their delayed
  placement would make the narrative incoherent.
- For main outcome figures, prefer vector exports and a restrained clinical palette with consistent
  exposure-group colors across all displays. Figure captions must define denominators, outcome
  direction, uncertainty, and synthetic/demo status when applicable.
- Palette Family Contract: one manuscript should have a unified visual style, not one literal color
  list applied to every chart. Assign colors by meaning, keep a group's color stable within a
  manuscript, and choose from named restrained palette families in `scripts/medical_palette.py`
  (`PALETTE_FAMILIES`). The built-in families are `teal_warm` (`#4EAB90`, `#8EB69C`, `#EDDCC3`,
  `#EEBF6D`, `#D94F33`, `#834026`), `deep_teal_coral` (`#4F8589`, `#8A6B7B`, `#D44C3C`,
  `#E5855B`, `#B7B5A0`, `#EDD5B7`), and `scientific_blue_red` (`#5E82A2`, `#D15354`,
  `#E8B86C`, `#8887CB`, `#5094D5`, `#F9AD95`). Pale fills need a subtle neutral edge so marks
  remain visible on white backgrounds. Also avoid near-black categorical fills; reserve very dark
  colors for text, axes, and sparse reference lines rather than bars, area fills, or group markers.
- Chart-family palette defaults: bar, stacked-bar, lollipop, and waterfall displays use
  the reference-image-1-style `teal_warm`; line, longitudinal, diagnostic, prediction, survival, forest, effect-estimate,
  and health-economic curves use `scientific_blue_red`; flow diagrams, tables, clinical triptychs,
  and image plate + quant displays use `teal_warm`. A user or journal style guide may override this
  with one named palette family for the whole manuscript.
- Heatmap and matrix displays must use restrained semantic color scales from the selected palette
  family, not the categorical group colors. Use sequential scales for one-direction intensity,
  counts, confusion matrices, annotated heatmaps, choropleth-style tiles, and enrichment intensity.
  Use diverging scales only when data are centered around a meaningful midpoint such as zero,
  correlation, or signed change. Use missingness colors only for observed/missing status. Use muted
  green/yellow/red only for ordered quality or risk-of-bias judgments. Do not mix `coolwarm`,
  `YlGnBu`, `Blues`, `magma`, `viridis`, or other ad hoc colormaps inside the same manuscript unless
  the user or journal supplies a style guide.
- Composite image panels must use a fixed normalized panel canvas or fixed inset boxes for their
  internal sub-images, dot plots, and quantification bars. Align companion image and quant/dot
  elements to shared top, bottom, and baseline coordinates; do not let `imshow` default equal-aspect
  behavior shrink a panel box or move image subpanels off the shared row. Quantification companion
  bars should be compact subordinate marks with fixed narrow widths, not full-width bar charts that
  visually compete with representative images.
- Flow diagrams should not be tiny in the final PDF. If a flow asset becomes unreadable after
  placement, regenerate or crop the asset instead of shrinking it further.

## Width Decision Rules

Choose the narrowest layout that preserves legibility.

| Display condition | Preferred layout |
|---|---|
| Single panel; short labels; no dense legend | single-column figure or table |
| Two or more panels that must be compared side by side | cross-column figure |
| Flow diagram with multiple stages or branches | cross-column figure |
| Forest plot with long subgroup labels or many rows | cross-column figure |
| Forest plot with short labels and few rows | single-column figure |
| Clinical triptych with aligned longitudinal, effect, and summary bands | cross-column figure |
| Image plate + quant with microscopy, histology, imaging, spatial overlays, segmentation, or blot-like images | cross-column figure or supplement |
| Compact heatmap with short labels | single-column figure |
| Large clustered heatmap, long labels, or multiple heatmap panels | cross-column or supplement |
| Simple schematic with few steps and short labels | single-column figure |
| Complex architecture/model schematic with branches or long labels | cross-column figure |
| Table with four or fewer short columns | single-column table |
| Table with long text in any column, effect/CI fields, definitions, or action notes | cross-column table with fixed custom widths |
| Baseline, cohort, or statement table that wraps repeatedly in one column | cross-column table with compact labels and fixed custom widths |
| Table with more than six columns or dense checklist matrix | appendix/supplement, landscape, or split table |

Never let a high-information table use equal-width columns by default. Allocate extra width to the
meaning-bearing column: effect estimate, uncertainty, risk-of-bias signal, definition note,
statement action, or interpretation boundary.

Do not stretch a short four-column table across the full text width when it creates large empty
right-hand space. Keep it single-column or use a narrower direct block. For wide tables, make column
widths add up to the available line width and assign spare width to the column that carries the
message, not to numeric columns.

If a cross-column `table*` would float away from its section heading or appear after later sections,
use a non-floating cross-column block instead and keep the table near the relevant text.

For preview or generated-manuscript routes, run a display layout audit before treating the layout as
accepted. The audit should cover the table environment, cross-column placement, figure image
non-blankness, triptych centering/vertical spacing, and image-plate/quantification gutter and width
allocation. For actual LaTeX-first manuscript routes, also run compiled layout QA and inspect
`layout_qa_summary.md` plus the table-page contact sheet.

## Word Single-Column Display Sizing

In a Word-first single-column manuscript, the text block is a maximum available width, not the
default width for every figure. Do not embed every plot at the same width merely because the page is
single-column. Size the display from density, reading task, and caption budget.

Use these Word sizing classes for generated previews and word-first manuscripts:

| Word size class | Typical inserted width | Use for |
|---|---:|---|
| compact | 3.5-4.2 in | sparse single-panel ROC/PR/KM/funnel/ICER/tornado/simple bar plots |
| standard | 4.4-5.2 in | ordinary grouped bars, line plots, distributions, short forest plots |
| wide | 5.4-6.2 in | dense heatmaps, flow diagrams, multi-panel comparisons, image plate + quant, clinical triptychs |
| square/medium | 4.2-4.8 in | correlation matrices, compact heatmaps, confusion matrices, PCA/scatter-style panels |

Keep the single-column text block around 6.0-6.5 in with 1-inch margins. Cap ordinary figure height
near 4.5 in in Word previews so a heading, a short paragraph, the figure, and its caption can share a
page. Long-caption displays should be shorter than short-caption displays. If a figure becomes
unreadable at its assigned class, redraw or split it before simply stretching it to full width.

Word preview packages must include manuscript-like surrounding text: title/abstract-style material,
section headings, and short Results/Methods paragraphs before groups of displays. A gallery of
caption-image-caption blocks is not a valid Word layout stress test because it cannot reveal how
figures interact with real manuscript prose and page breaks.

For generated Word preview routes, record a `word_display_catalog` object in `layout_audit.json`
with figure count, table count, text width, maximum figure height, prose paragraph count, inserted
width/height per figure, and size-class counts. The audit must fail if all figures use the same
inserted width or if fewer than three size classes are exercised.

## Legend Standards

Legends are self-contained. Define abbreviations, sample size, groups, axes/panels, statistical test,
error bars, effect measure, and representative/panel note when relevant. If any value is missing,
use an explicit author marker rather than inventing it.

Do not draw a clinical figure from unverified invented numbers unless the output is explicitly a
synthetic demonstration and is labeled as such.
