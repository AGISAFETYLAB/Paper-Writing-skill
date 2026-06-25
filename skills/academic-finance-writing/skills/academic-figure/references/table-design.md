# Finance Table Design Gate

Use this reference after the Display Choice Gate selects an editable table and before accepting a
LaTeX table shell, data-generated table, or final manuscript table. It owns table-specific content
hygiene, venue overrides, source-to-script provenance, skeleton selection, and page-budget pressure.
Use `figure-layout.md` for float width and compiled layout QA.

## Required Table Plan Fields

Record these fields for every planned table in the Display-Item Plan:

| Field | Required content |
|---|---|
| table_family | summary statistics, balance, main regression, robustness, portfolio sort, factor model, variable dictionary, merge diagnostic, calibration/moment fit, model performance, or appendix ledger |
| table_skeleton | nearest skeleton from Table Skeleton Selection, plus any deliberate deviation |
| table_payoff_sentence | One sentence stating what the table changes in the reader's assessment of the claim |
| venue_table_override | target-venue rule applied, or `none_checked` with date/source status |
| table_hygiene_status | pass/blocker list from the Table Content Hygiene Gate |
| source_table_to_script_map | script/model output/source file that produces the table values |
| table_output_path | expected editable `.tex`, `.csv`, `.xlsx`, or office-native table asset |
| page_budget_cost | estimated manuscript space: `inline`, `half_page`, `one_page`, `multi_page`, or `appendix_only` |
| appendix destination | body, internal appendix, Internet Appendix, supplement, or blocked |

If a table has no `source_table_to_script_map`, mark it as `needs_user_evidence`; do not present it
as reproducible. If `page_budget_cost` would push the paper over the target page window, move
nonessential detail to appendix before drafting prose around it.

## Venue-Specific Table Override

Official target-venue instructions override these defaults. Do not turn one venue's copyediting
rules into a universal finance rule.

For Journal of Finance style targets, check the current venue card and apply these table-specific
constraints unless a newer official source says otherwise:

- portrait orientation by default;
- up to 8 columns for main-paper tables;
- 12-point text unless the target card or template permits a different size;
- table title plus descriptive legend;
- self-contained legend that defines variable notation and explains what the table shows;
- if the legend exceeds 300 words, move variable construction detail to a definitions table or
  appendix and point the legend there;
- appendix table numbering follows the target venue card.

For Review of Finance, RFS, AEA, JFE, or other routes, re-check the target venue card and record the
actual table/page-count implication. Many finance/economics venues count figures and tables toward
the main manuscript page limit while excluding clearly labeled Internet Appendix or Supplemental
Appendix material. The body must still be self-contained.

## Table Content Hygiene Gate

A finance table is not submission-readable unless it passes these checks:

- use plain English row and variable names, not vendor mnemonics or code names;
- define sample window, unit of observation, transformations, winsorization, lagging, scaling, and
  data source/vendor where relevant;
- for regression tables, state dependent variable and units, main variable definition, controls,
  fixed effects, standard-error clustering or dependence treatment, observations, fit statistics,
  and economic magnitude or scaling;
- for headline contrasts, event-window CAR differences, high-minus-low rows, long-short spreads,
  alphas, or treatment effects, include uncertainty (SE, t-stat, p-value, confidence interval, or
  bootstrap interval) or explicitly mark the row descriptive-only and keep it out of headline
  inference;
- for summary/balance tables, report N, mean, SD, and relevant min/max or percentiles; define every
  variable in notes or a definitions table;
- for portfolio-sort and factor-model tables, state universe, breakpoints, weighting, rebalance and
  holding period, factor model, return frequency, costs/capacity status, and benchmark source;
- for variable dictionaries and data construction tables, keep the real meaning-bearing text column
  bounded and move long construction rules to appendix when they dominate the table;
- use consistent decimal places, usually 2-3 meaningful decimals unless the unit requires more;
- put units in column headings, not repeatedly inside body cells;
- precede decimal points with a digit, for example `0.10`, not `.10`;
- do not use ditto marks for repeated values; use row grouping, spanners, compact notes, or repeat
  the value when blank would be ambiguous;
- do not use vertical rules; do not use double rules; use booktabs-style horizontal rules.

## Table Provenance Ledger

Borrow the script-registry discipline from empirical-finance workflows. Every final table needs a
ledger entry:

| table_id | table_family | source_table_to_script_map | inputs | output_path | paper_target | in_text_anchor | status | blocker |
|---|---|---|---|---|---|---|---|---|

`Output/Tables/`-style terminal tables should be listed as final paper tables only when they feed
the manuscript directly and are not intermediate processed data. For generated tables, record the
model object or source CSV/Parquet and the script that writes the editable table. For hand-entered
LaTeX shells, record the user-provided value source and unresolved TODO markers.

Before submission-ready wording, verify that every table referenced by `\input{...}` or equivalent
exists, has a producing script or documented user-supplied source, and is listed in the source-data
audit or submission package. Orphan table files and tables with no text anchor are not ready.

## Table Payoff Gate

Every body table must earn its page space. Write one `table_payoff_sentence`:

```text
Table X changes the reader's assessment of <claim> by showing <estimate/comparison/check>.
```

If that sentence is vague, the table moves to appendix, becomes a compact companion, or is deleted.
Robustness sweeps, long variable definitions, and dense diagnostics are appendix material unless the
paper's contribution is data construction, measurement, or method validation.

## Table Skeleton Selection

Use skeletons as starting points, not templates to copy blindly. Choose the nearest family and then
adjust to the evidence and venue.

| Table family | Starting skeleton | Main design pressure |
|---|---|---|
| summary statistics | bounded label column; N, mean, SD, selected percentiles; compact units in headers | group comparisons and variable definitions without long prose cells |
| balance table | treatment/control means, difference, SE or p-value, standardized difference when relevant | separate balance from main effects; define randomization or exposure groups |
| main regression | rows for key variables, columns for parsimonious-to-rich specs, FE/control/stat rows at bottom | enough specs to show robustness without burying the main coefficient |
| robustness table | panels or columns by alternative sample/window/control/clustering/model | exact numbers for checks that matter; move broad sweeps to appendix |
| portfolio-sort table | quantile columns, long-short/spread, alpha/beta rows, SE/t-stat rows | quantile headers and factor-model rows must stay compact |
| factor-model table | alpha, factor loadings, SE/t-stat, N, adjusted R2, factor source | avoid mixing incompatible frequencies or benchmark models |
| variable dictionary | variable, definition, source, construction/timing/scaling | use a real bounded text column; long rules go to appendix |
| merge diagnostic | input counts, unique keys, matched/unmatched counts, match rates, duplicate notes | row-count reconciliation and join type clarity |
| calibration/moment fit | parameter or moment, data target, model value, source, targeted/untargeted status | distinguish fitted moments from validation moments |
| model performance | split, baseline, metric, model, seed/fold/leakage check | out-of-sample split and baseline must be visible |

## Static And Compiled QA

Run `scripts/lint_finance_tables.py` on LaTeX table sources before accepting table output. Treat
blocking findings such as vertical rules, `\hline`, double rules, malformed declared-width tables,
unjustified `\resizebox`, missing captions, leading decimals without zero, and
`central_contrast_missing_uncertainty` as defects to fix before compiled layout QA.

After the manuscript compiles, run `scripts/inspect_compiled_layout.py paper --pages tables --out-dir
paper/layout-qa`. Static lint catches source-level defects; compiled QA catches visual underfill,
overflow, clipping, tiny font, and float drift. Passing one does not replace the other.
The compiled layout gate is `partial`, not `pass`, until the contact sheet or page PNGs have been
opened and `layout_manual_inspection_status: pass` is recorded.
