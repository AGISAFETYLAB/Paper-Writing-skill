# Finance Display Selection

Use this reference at Paper Framework and display-planning time, before choosing Python or R.
It owns the Display Choice Gate: decide whether the manuscript claim needs a plotted figure,
editable LaTeX table, composite display, or appendix-only display before loading a backend chart
catalog.

## Display Choice Gate

This gate is backend-neutral before the Python/R Backend Language Gate. Do not ask for Python or R
only to decide whether a claim should be a figure or a table.

For every planned display, record:

| Field | Required content |
|---|---|
| `primary_evidence_role` | `main result`, `identification`, `mechanism`, `robustness`, `data construction`, `implementation friction`, `model fit`, or `appendix support`. |
| `display_choice_rationale` | Why this evidence should be a figure, table, composite, or appendix item. |
| `alternative_considered` | The nearest plausible alternative and why it was rejected, such as table instead of figure, figure instead of table, appendix instead of body. |
| `duplication_check` | Whether the same key result is already displayed elsewhere and, if so, why both displays are necessary. |

Allowed `duplication_check` values:

- `primary_display_only`: this is the only main display for the key result.
- `exact_values_companion`: a figure shows the pattern and an editable table gives exact estimates.
- `shape_companion`: a table gives exact estimates and a figure shows dynamics, distribution, or nonlinearity.
- `appendix_detail_only`: the body display carries the claim and appendix material gives extra diagnostics.
- `duplicate_blocked`: the display repeats an existing result without a distinct role and should be removed or redesigned.

One key result should have one primary display. A second display is allowed only when it has a
different evidence role, such as exact estimates versus visual dynamics. If both displays answer the
same question at the same level of detail, keep the stronger one and move the other to the appendix
or delete it.

## Figure Versus Table

Use plotted figures when the claim depends on shape, dynamics, timing, distribution, fit, geography,
networks, or high-dimensional patterns. Typical examples include:

- event-study or DiD dynamics, pre-trends, anticipation, and treatment timing;
- RD discontinuities, density/manipulation checks, bunching, and nonlinear response;
- synthetic-control paths, gaps, placebo distributions, and donor-weight diagnostics;
- cumulative returns, drawdowns, rolling exposures, intraday responses, and liquidity paths;
- maps, networks, flow diagrams, transition matrices, heatmaps, calibration/lift, embeddings, and
  topic trends.

Use editable LaTeX tables when the claim depends on exact estimates, standard errors, sample sizes,
fixed effects, model specifications, or summary statistics. Typical examples include:

- main regression estimates, robustness specifications, Fama-MacBeth results, and IV first stages;
- summary statistics, variable definitions, balance tests, merge/linkage ledgers, and sample
  construction counts;
- portfolio-sort returns, alphas, betas, turnover/cost/capacity values, and factor-model tables;
- calibration/moment-fit tables, model-performance tables, and appendix specification matrices.

Use a composite only when the panels support one shared conclusion and each panel answers a
different question. Do not build a composite to hide unrelated checks or to fill a full-width float.

## Body Versus Appendix

Keep the body display set narrow:

- The first Results display should usually be the main estimate, event-study, portfolio-sort, or
  model-fit display that most directly supports the paper's central claim.
- Move broad robustness sweeps, many specification columns, long variable dictionaries, and dense
  diagnostics to the Internet Appendix unless the paper's contribution is itself a data/method
  construction.
- A main-text display that exists only because it is available, visually attractive, or easy to
  render fails the Display Choice Gate.

## Method-Specific Defaults

| Method or evidence need | Prefer first | Companion only when |
|---|---|---|
| Main regression or factor-model estimate | editable LaTeX table | coefficient plot if many related estimates obscure the pattern. |
| Heterogeneity across many groups | coefficient or forest plot | table if exact subgroup estimates are central. |
| Event study / DiD | event-time figure with CI | table for key post-event coefficients or estimator comparisons. |
| RD | binned scatter with local fits | table for bandwidth and polynomial sensitivity. |
| Synthetic control | treated-vs-synthetic path plus gap/placebo as needed | weights/balance table supports credibility. |
| Portfolio sort / asset pricing | portfolio or factor-model table | cumulative return or risk-return figure if the path or tradeoff is the claim. |
| Backtest / implementation friction | curve plus drawdown/turnover/cost panel | table for cost/capacity assumptions. |
| Data construction | flow, coverage heatmap, or merge table based on the bottleneck | appendix ledger for full code-output map. |
| Structural or macro-finance | IRF, model-fit, or counterfactual figure | moment-fit/calibration table for exact targets. |
| ML/text finance | calibration, lift, topic trend, or feature-importance figure | performance table for split, baseline, and leakage checks. |

## Common Failure Modes

- Do not choose a heatmap, radar chart, or composite because it looks comprehensive; use it only
  when the claim depends on a high-dimensional pattern or multi-metric tradeoff.
- Do not use a full regression table when the reader only needs one coefficient path; use a
  coefficient plot and move exact estimates to the appendix.
- Do not use a figure for exact standard errors, fixed effects, clustering, or sample counts that a
  table must state.
- Do not duplicate the same key result as both a main figure and a main table without documenting
  the distinct evidence roles in `duplication_check`.
