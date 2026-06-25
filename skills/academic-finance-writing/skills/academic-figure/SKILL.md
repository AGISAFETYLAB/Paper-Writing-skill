---
name: academic-figure
description: Use when creating, revising, auditing, or polishing figures and tables for finance, financial economics, accounting, asset-pricing, corporate-finance, banking, fintech, event-study, theory-model, backtest, or econometrics manuscripts.
---

# Academic Figure — Finance

Owns every display item in the standalone finance package: summary statistics, regression tables,
portfolio sorts, event-study plots, coefficient plots, portfolio backtest curves, drawdown panels,
risk-return scatters, robustness tables, and online appendix displays. The backend catalogs cover
broad finance displays, including data profiling, identification diagnostics,
asset-pricing/backtest panels, corporate-finance and banking diagrams, structural/macro-finance
displays, ML/text diagnostics, and multi-panel composites.

Intent classes covered: `figure-only` and `table-only`.

## Display Intent Routing

- `display-plan-only`: plan tables/figures and source requirements; do not ask for Python or R.
- `latex-table-shell`: produce or audit booktabs/LaTeX table structure from user-provided values or
  placeholders; do not ask for Python or R.
- `table-from-data`: generate table values from data/model output; apply the Backend Language Gate
  unless an existing language-specific workflow is clear.
- `plotted-figure`: draw event-study, coefficient, backtest, risk-return, heatmap, network, map, or
  other plotted figures; apply the Backend Language Gate.
- `display-audit`: audit existing figures/tables; apply the Backend Language Gate only if the user
  asks to redraw or regenerate assets.

## Protocol

1. Read `manifest.yaml`.
2. Load `references/display-selection.md` and apply the Display Choice Gate before choosing a
   backend, display family, or layout.
3. Load `references/figures.md`.
4. Load `references/table-design.md` for every table, table shell, table-from-data output, or
   table audit. Apply the Finance Table Design Gate before accepting table content, provenance,
   venue-specific table overrides, page-budget cost, or skeleton selection.
5. Load `references/figure-export-qa.md` before producing or accepting final plotted assets,
   data-generated tables, or final display assets.
6. Load `references/finance-palette.md` before producing or accepting plotted figures; every
   paper must use one coherent palette profile and stable semantic color mapping across figures.
   For generated Python plotting code or palette-token audits, use `scripts/finance_palette.py`
   as the canonical executable registry.
7. Load `references/figure-layout.md` and apply the Layout And Placement Gate before placing
   or accepting final figures/tables; record target layout, single-column/double-column choice,
   float environment, final size, panel grid, text anchor, and layout risk.
8. Backend Language Gate applies only to `table-from-data` and `plotted-figure`. Do not trigger the
   Backend Language Gate for `latex-table-shell`, `display-plan-only`, or read-only `display-audit`.
   When the gate applies and the user has not chosen Python or R, stop and ask `Python or R?` Do not cross-render with the unselected language.
9. If the user selects R or provides R scripts/data workflow, load
   `references/r-figure-workflow.md` and `references/r-chart-catalog.md`; keep all
   drawing, previewing, exporting, and visual QA in R.
10. If the user selects Python or provides Python scripts/data workflow, load
   `references/python-figure-workflow.md` and `references/python-chart-catalog.md`;
   keep all drawing, previewing, exporting, and visual QA in Python.
11. Load `../../_shared/checks/econometrics.md` when the display reports estimates, uncertainty, or identification.
12. Load `../../_shared/checks/identification-strategies.md` for DiD, IV, RD, synthetic-control,
   event-study, portfolio-sort, factor-model, backtest, or structural displays.
13. Each figure/table must support one manuscript claim and include sample, unit, model, uncertainty,
   economic magnitude, and robustness status where relevant.
14. Tables must be submission-readable, source-mapped, linted when LaTeX is available, and appendix
   overflow must be explicit.
15. Plotted PNG/JPG preview assets must pass `scripts/audit_visual_assets.py` before
   `visual_asset_qa_status: pass`; likely cropped titles, clipped labels, blank previews, or
   extreme unused margins block the display gate.
16. Compiled layout QA is not pass from machine output alone. `compiled_layout_qa_status: pass`
   requires clean machine status and `layout_manual_inspection_status: pass` after inspecting the
   contact sheet or page PNGs.

Do not invent values, standard errors, p-values, alphas, or robustness results. If data are absent,
produce a display plan or a LaTeX table shell with TODO markers that the review gate treats as
unresolved.

Return or update a Display-Item Plan before drafting results text. The plan must record
`primary_evidence_role`, `display_choice_rationale`, `alternative_considered`, and
`duplication_check` from the Display Choice Gate. A display is not complete until it passes the
selection contract in `references/display-selection.md` and the relevant contract in
`references/figures.md`; tables must also pass the Finance Table Design Gate in
`references/table-design.md`; plotted figures and data-generated tables must pass the
selected backend catalog's blocking QA, the palette consistency gate in
`references/finance-palette.md`, and the layout placement gate in `references/figure-layout.md`.
