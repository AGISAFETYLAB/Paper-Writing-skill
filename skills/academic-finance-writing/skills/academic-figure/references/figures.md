# Finance Figures And Tables

Finance display items are evidence objects. They must be planned before drafting results and audited
before submission-ready wording.

Before drawing a plotted figure, apply `references/display-selection.md`: the Display Choice Gate
decides whether the claim needs a figure, editable LaTeX table, composite, or appendix display.
Only after that backend-neutral decision should `references/figure-export-qa.md` trigger the
Python/R Backend Language Gate for plotted figures or data-generated tables. Then load the selected
backend catalog (`references/r-chart-catalog.md` or `references/python-chart-catalog.md`) and the
paper-level palette system in `references/finance-palette.md`. For final size, single-column versus
double-column placement, float environment, and appendix overflow, load `references/figure-layout.md`.
For every table, also load `references/table-design.md` and apply the Finance Table Design Gate
before accepting content, source mapping, venue-specific table overrides, page-budget cost, or
appendix placement.

## Display Intent Routing

- `display-plan-only`: return a Display-Item Plan, source requirements, and QA risks only.
- `latex-table-shell`: produce or audit editable LaTeX/booktabs table structure from supplied values
  or TODO placeholders. Do not trigger the Backend Language Gate for `latex-table-shell`.
- `table-from-data`: generate table values from data or model output. Backend Language Gate applies
  only to `table-from-data` and `plotted-figure`.
- `plotted-figure`: draw or redraw visual figures from data/model outputs.
- `display-audit`: inspect existing figure/table assets and report blockers; ask for Python or R
  only when regeneration is requested.

## Display-Item Plan

Maintain this table in the Paper Framework:

| ID | Type | Location | Claim supported | Data/model source | Required notes | Palette profile | Placement width | Float env | Final size | Table fields / QA | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | summary statistics table | Data | sample composition | data profile | sample, winsorization | finance-muted | single-column or double-column after fit check | table/table* | final readable width | table_family, table_skeleton, table_payoff_sentence, source_table_to_script_map, page_budget_cost | planned |
| T2 | regression table | Results | main estimate | analysis script/model | FE, controls, SE clustering | finance-muted | double-column when many specs | table* or appendix table | final readable width | venue_table_override, table_hygiene_status, appendix destination, static lint status | planned |
| F1 | event-study figure | Identification | pre-trends/no anticipation | analysis script/model | event time, CI, omitted period | finance-muted | single-column unless labels/groups are cramped | figure | about 89 mm | not applicable | planned |

Allowed statuses: `planned`, `source_available`, `asset_rendered`, `audited`, `blocked`.

Also record `primary_evidence_role`, `display_choice_rationale`, `alternative_considered`, and
`duplication_check` from `references/display-selection.md`. One key result should have one primary
display; a companion table or figure is allowed only when it has a distinct evidence role, such as
exact values versus visual dynamics.

For tables, additionally record `table_family`, `table_skeleton`, `table_payoff_sentence`,
`venue_table_override`, `table_hygiene_status`, `source_table_to_script_map`, `table_output_path`,
`page_budget_cost`, and `appendix destination` from `references/table-design.md`.

## Regression Table Contract

A regression table is incomplete unless it states:

- dependent variable and units
- main variable definition
- sample window and unit of observation
- fixed effects and controls
- standard-error clustering or dependence treatment
- observations and relevant fit statistics
- economic magnitude or scaling
- whether the table is main text or Internet Appendix

Use booktabs-style LaTeX. Avoid unreadable wide tables; split into panels or move detail to the
Internet Appendix.

## Table Geometry Contract

Finance tables must look intentionally designed at their final manuscript size. A table that is
technically valid LaTeX but leaves a large empty band on the right, stacks labels one word per line,
or forces all numeric columns into equal-width prose cells is not submission-ready.

Apply this **Column width budget** before choosing `tabular`, `tabular*`, `tabularx`, or
`\resizebox`:

| Table family | Default geometry | Escalate when |
|---|---|---|
| summary statistics / balance | natural or single-column `tabular` with one bounded label column and compact numeric columns | many groups, long variable labels, or missingness notes force repeated wrapping |
| regression / robustness | `table*` or appendix-full-width only when many specifications must be compared; compact FE/control/stat rows | more than about 6-8 models, long specification labels, multiple outcomes, or many SE variants |
| portfolio-sort / factor-model | numeric-heavy `tabular*` with controlled inter-column fill and short quantile headers | many quantiles plus alphas/betas/factors need panel splitting or appendix placement |
| variable dictionary / code-output map | `tabularx` only with a real meaning-bearing `X`/bounded prose column | definitions, source notes, or construction rules dominate the table |

Never leave a declared full-width table underfilled. If a table declares `\linewidth`,
`\columnwidth`, or `\textwidth`, it must either use `tabular*` with
`@{\extracolsep{\fill}}` for mostly numeric tables, or `tabularx` with a real `X`/bounded prose
column that carries substantive text. A declaration such as `tabularx{\textwidth}{p{...}rrrr}`
without stretch/fill is an underfilled table: the rule spans the page while cells are packed left.
Use natural width, add a real fill mechanism, or redesign the columns.

Run repeated-label compression before widening a table: move repeated sample names, model families,
FE labels, benchmark names, clustering choices, and window definitions into column spanners, panel
headers, or compact notes. Row labels should name the economic object once; do not repeat the full
dataset/model phrase on every row.

Use `\resizebox` only after the semantic layout is correct and only for short-cell numeric tables.
Do not use it as the primary fix for prose-heavy variable dictionaries, label-heavy regression
tables, or crowded robustness tables.

For LaTeX full drafts, compiled layout QA is mandatory before accepting the table aesthetics gate:
run `scripts/lint_finance_tables.py` on table sources first, then
run `scripts/inspect_compiled_layout.py` on the compiled paper with `--pages tables`, keep
`paper/layout-qa/layout_qa_summary.md`, and inspect the contact sheet or rendered table pages for
margin crossing, clipping, unreadable font, sparse full-width pages, float drift, and right-side
underfill.

## Palette And Style Contract

For plotted figures and figure-like tables:

- choose one paper-level palette profile from `references/finance-palette.md`;
- keep semantic color mapping stable across the paper;
- use `scripts/finance_palette.py` for generated Python plotting code when available, or mirror
  its token names and profile values in R/paper-local scripts;
- if a plotted chart has only 1-4 categorical colors, avoid the `deep` token unless there is a
  documented semantic reason;
- avoid neon colors, unrelated palettes across figures, pure primary RGB colors, and default
  saturated red/green contrasts;
- use line styles, markers, hatches, direct labels, or table labels when color carries meaning;
- keep confidence bands and event-window shading low-alpha and visually subordinate to data.

## Layout And Placement Contract

Before rendering or inserting a display, apply `references/figure-layout.md`.

- Record `target_layout`, `placement_width`, `float_env`, `final_width_mm`, `aspect_ratio`,
  `panel_grid`, `text_anchor`, and `layout_risk`.
- In two-column templates, compact figures/tables use `figure`/`table` with `\columnwidth`; use
  `figure*`/`table*` with `\textwidth` only for genuinely wide, multi-panel, or label-heavy displays.
- In single-column manuscripts, do not use `figure*` or `table*`; use regular floats with natural,
  fractional, or full `\textwidth` widths.
- Wide finance tables must pass a fit check before promotion: abbreviate headers, right-size numeric
  columns, split panels, or move detail to appendix before using font shrinkage or `\resizebox`.
- Record float-order risk when wide Results floats could land after the interpretive text; use a
  deliberate split, text-anchor move, `\FloatBarrier`, or `\clearpage` only when appropriate.

## Event-Study Figure Contract

An event-study figure must show:

- event definition and event-date source
- pre-event periods sufficient for visual diagnosis
- omitted period
- confidence intervals
- sample and unit
- estimator note when staggered timing or heterogeneous effects matter
- leakage or anticipation boundary

Do not use an event-study figure as causal proof without the identification text in
`_shared/checks/identification-strategies.md`.

## Portfolio-Sort Table Contract

A portfolio-sort or factor-model table must state:

- universe and sample window
- signal construction and implementation lag
- breakpoints, weighting, rebalancing, and holding period
- excess return, spread, alpha, or risk adjustment definition
- benchmark or factor model
- transaction-cost and turnover status

If costs or capacity are absent, call it a paper return spread or synthetic backtest result, not a
profitable trading strategy.

## Backtest And Risk-Return Contract

A portfolio backtest curve, drawdown plot, or risk-return scatter is incomplete unless it states:

- sample window and return frequency
- portfolio construction and rebalancing rule
- benchmark, risk-free rate, or factor model when used
- transaction-cost, turnover, and capacity status
- annualization rule for risk-return scatter displays
- whether the display is a historical or synthetic backtest rather than a live trading result

Do not describe a curve as an investable strategy unless implementation costs, turnover, and
capacity limits are addressed. When those are absent, call it a historical or synthetic backtest.

## Robustness Table Contract

A robustness table is incomplete unless it states:

- main coefficient or statistic being stress-tested
- alternative samples, windows, controls, fixed effects, clustering, benchmarks, or model variants
- observations and sample changes for each column or panel
- whether the direction, magnitude, and uncertainty match the main claim
- unresolved missing, failed, or underpowered checks

Use robustness tables for exact numeric checks and robustness grids for compact visual summaries.

## Figure Types

Use backend catalog display families for:

- data profiling and sample construction: summary statistics, variable definitions, sample flow,
  panel coverage, missingness, merge diagnostics, and outlier/winsorization checks;
- econometric and identification evidence: regression tables, event studies, parallel trends,
  treatment timing, coefficient plots, robustness tables, robustness grids, mechanism plots, balance
  plots, placebo inference, RD, IV, synthetic control, bunching, and shift-share diagnostics;
- asset-pricing, market-microstructure, and backtest evidence: portfolio sorts, factor-model
  performance, CAR, long-short cumulative returns, portfolio backtest curves, factor exposure
  heatmaps, rolling betas/alphas, drawdown, risk-return scatter, turnover, costs, capacity,
  liquidity, intraday event-time, and risk decomposition;
- corporate-finance, banking, fintech, and policy displays: institutional timelines, geographic
  exposure maps, networks, credit transition matrices, and funding/loan flow diagrams;
- structural, theory, macro-finance, ML, text, and composite displays: calibration/moment fit, IRFs,
  model fit, counterfactual/welfare decomposition, comparative statics, ML performance, calibration
  or lift, feature importance, text topics, multi-panel composites, heatmaps/bubble matrices,
  radar/polar charts, and embedding/cluster plots.

Use editable LaTeX tables for numeric evidence that needs exact values. Use plotted figures when the
evidence depends on shape, dynamics, timing, distribution, fit, geography, networks, or
high-dimensional patterns. If a result could be either a table or figure, document the rejected
alternative in `alternative_considered` and record whether the selected item is the
`primary_display_only`, an `exact_values_companion`, a `shape_companion`, or
`appendix_detail_only`.

## QA Gate

A table is not done when LaTeX compiles. A figure is not done when the script runs.

Before accepting a display item, check:

- the display supports one named manuscript claim
- all notes define sample, model, benchmark, uncertainty, and scaling
- the palette profile and semantic color map match the paper-level style
- small categorical figures do not use dark blocks by accident
- placement width, final size, float environment, and text anchor match the layout contract
- every number discussed in prose appears in a table/figure or source ledger
- every table/figure is referenced from the main text or appendix
- every final table has a `source_table_to_script_map`, `page_budget_cost`, table payoff sentence,
  and appendix destination
- LaTeX tables pass `scripts/lint_finance_tables.py` or have a documented blocker
- visual layout is readable at submission size
- table pages have a compiled layout QA artifact and no visible right-side underfill, clipping, or
  sparse full-width float unless explicitly justified by the table's comparison structure
- appendix overflow is deliberate, not a hiding place for weak main evidence
