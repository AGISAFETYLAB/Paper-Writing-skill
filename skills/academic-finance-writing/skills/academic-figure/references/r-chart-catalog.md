# R Chart Catalog For Finance Figures

Use this catalog only after R has been selected by the Backend Language Gate. Each row maps a
finance display need to the normal R route, required source data, and blocking QA checks.

Before drawing, apply `references/finance-palette.md`: select one paper-level palette profile and
reuse the same semantic color mapping across all figures.

## Catalog Parity Contract

This catalog must stay one-to-one with `references/python-chart-catalog.md`: use the same display
family names and the same row order. If adding, removing, or renaming a display family, update both
catalogs and run `scripts/validate_chart_catalog_parity.py`.

## Data Profiling And Sample Construction Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| summary statistics table | Data section or sample description needs distribution, missingness, and group comparisons. | `dplyr`/`data.table`, `modelsummary::datasummary`, `tinytable`, LaTeX `booktabs` | variables, sample filters, group labels, N, mean, SD, percentiles, missingness | Units, winsorization, sample window, and variable scaling must be stated. |
| variable definition table | Readers need construction, source, timing, or scaling for outcomes, treatments, signals, and controls. | `tibble`, `dplyr`, `tinytable`, LaTeX `booktabs` | variable name, definition, source, transformation, timing lag, unit | Do not leave vendor mnemonics unexplained; transformations must match Methods. |
| sample construction flow | Exclusions, filters, merges, or cohort formation determine the final sample. | `DiagrammeR`, `ggplot2` rectangles/arrows, `ggforce` | starting counts, exclusion reasons, merge drops, final analytic counts | Counts must reconcile and match the Data section and code-output map. |
| panel coverage heatmap | Entity-time coverage, entry/exit, or unbalanced panels affect interpretation. | `ggplot2::geom_tile`, `data.table`, `tidyr` | entity or group, time, observation indicator/count, sample filters | Axis ordering and aggregation must not hide sparse coverage or attrition. |
| missingness diagnostic | Missing values or structural missingness affect sample selection or variable availability. | `naniar`, `VIM`, `ggplot2::geom_col`/`geom_tile` | variable, missing indicator, time/group if relevant, missing-code rules | Distinguish true zero, not applicable, and missing; high-missing variables must be flagged. |
| merge/linkage diagnostic table | Data sources are linked by identifiers and match rates determine sample credibility. | `data.table`, `dplyr`, `tinytable`, LaTeX `booktabs` | left/right counts, match rates, duplicate keys, unmatched reason codes | Join type, key uniqueness, and row-count changes must be visible. |
| outlier/winsorization diagnostic | Extreme values, trimming, or winsorization could drive estimates. | `ggplot2` box/violin/hist/ECDF panels, `dplyr` summaries | raw and transformed values, cutoffs, sample, variable units | Show cutoff rules and whether results use raw, trimmed, or winsorized variables. |

## Econometric And Identification Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| regression table | Main or robustness estimates support a finance claim. | `fixest`, `modelsummary`, `tinytable`, LaTeX `booktabs` | estimate, SE/CI, sample, FE, controls, clustering, N | Notes must state sample, FE, controls, SE clustering, and economic scaling. |
| event-study figure | Dynamic effects, pre-trends, or market reaction timing is central. | `fixest::iplot`, `ggplot2::geom_pointrange` | event time, estimate, CI, omitted period, sample | Omitted period, CI, and anticipation/leakage boundary must be visible. |
| parallel-trends plot | DiD credibility depends on pre-treatment behavior before treatment. | `fixest::iplot`, `did`, `ggplot2::geom_pointrange` | relative time, cohort/group, estimate, CI, omitted period | Pre-period coefficients must not be visually compressed or selectively omitted. |
| treatment timing/adoption plot | Staggered adoption, policy exposure timing, or cohort composition affects design. | `ggplot2::geom_tile`, `geom_col`, `bacondecomp` outputs | unit/group, adoption date, cohort, exposure intensity, sample counts | Cohort definitions and never-treated/comparison groups must be identifiable. |
| coefficient plot | A set of model estimates or specifications must be compared visually. | `broom`, `ggplot2::geom_pointrange`, `modelsummary` | estimate, interval, model/spec label, reference line | Axis scale and reference line must match coefficient interpretation. |
| robustness grid | Many alternative specifications must be summarized compactly. | `modelsummary`, `ggplot2` tile/dot grid | specification labels, estimate/sign/status, sample notes | Do not hide failed, missing, or underpowered robustness checks. |
| robustness table | Alternative samples, controls, windows, clustering choices, or model variants must be reported as exact numbers. | `fixest`, `modelsummary`, `tinytable`, LaTeX `booktabs` | specification labels, estimate, SE/CI, N, FE, controls, clustering, sample/window notes | Main coefficient definition, sample changes, controls, FE, and standard-error rule must be visible; do not mix incompatible outcomes in one table. |
| mechanism or channel plot | Evidence supports a proposed mechanism rather than only the main effect. | `ggplot2` dot/bar/facet plot | channel variable, estimate or statistic, uncertainty, source model | Caption must distinguish mechanism evidence from causal proof. |
| covariate balance plot | Matching, weighting, experiment checks, or treated/control comparisons need balance evidence. | `cobalt::love.plot`, `ggplot2::geom_point` | covariate, standardized difference, before/after adjustment, threshold | Show before and after adjustment when applicable; threshold must be labeled. |
| placebo/permutation inference plot | Placebo dates, placebo units, randomization inference, or donor placebos support identification. | `ggplot2` histogram/rank/dot plot | placebo estimates, true estimate, p-value/rank, randomization scheme | True estimate and placebo construction must be explicit. |
| RD binned scatter plot | Regression discontinuity identification or local fit is central. | `rdrobust`, `ggplot2`, `binsreg` | running variable, outcome, cutoff, bins, bandwidth, polynomial/local fit | Cutoff, bandwidth, and side-specific fits must be visible. |
| RD density/manipulation plot | Sorting around a cutoff threatens RD validity. | `rddensity`, `ggplot2` density/bin plot | running variable, cutoff, bin width/bandwidth, density estimates | Manipulation test and binning choices must be reported. |
| IV first-stage diagnostic | Instrument relevance or weak-instrument concern must be reported. | `fixest`, `modelsummary`, `ggplot2` dot/bar plot | first-stage estimate, F-statistic, partial R2, sample, FE/controls | Weak-instrument threshold and excluded instrument definition must be stated. |
| synthetic-control path plot | Treated and synthetic outcomes are compared before and after intervention. | `Synth`, `tidysynth`, `gsynth`, `ggplot2` | treated outcome, synthetic outcome, intervention date, pre/post periods | Pre-period fit and intervention date must be clear. |
| synthetic-control weights/balance table | Donor composition or predictor balance supports synthetic-control credibility. | `tidysynth`, `Synth`, `modelsummary`, `tinytable` | donor weights, predictors, treated values, synthetic values | Nonzero donors and predictor balance must reconcile with path plot. |
| bunching/density plot | Bunching, thresholds, tax notches, or discontinuous incentives drive identification. | `ggplot2` histogram/density, `binsreg` | running variable, threshold/notch, bin counts, counterfactual fit | Bin width and counterfactual construction must be disclosed. |
| shift-share exposure diagnostic | Bartik/shift-share exposure or industry/geographic shares drive identification. | `ggplot2`, `sf` when geographic, `dplyr` | shares, shocks, exposure measure, geography/industry/time | Exposure construction and dominant-share sensitivity must be visible or tabled. |

## Asset Pricing, Market Microstructure, And Backtest Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| portfolio-sort table | Returns or characteristics are sorted by signal, quantile, or treatment. | `dplyr`, `modelsummary`, LaTeX `booktabs` | universe, signal, breakpoints, weights, returns/alphas, SE | Breakpoints, weighting, lag, rebalancing, and costs/capacity status must be stated. |
| factor-model performance table | Alphas, betas, spreads, or risk-adjusted returns are central. | `PerformanceAnalytics`, `sandwich`, `modelsummary` | returns, factor data, model, alpha/beta, SE/t-stat | Factor source, frequency, and benchmark model must be named. |
| cumulative abnormal return plot | Market reaction or event-window performance is shown. | `ggplot2::geom_line`, `geom_ribbon` | event date, abnormal return, window, benchmark, CI if claimed | Window and benchmark must match text claims. |
| long-short cumulative return curve | A long-short factor, spread portfolio, or strategy path is interpreted over time. | `xts`, `PerformanceAnalytics`, `ggplot2::geom_line` | long return, short return, spread return, date, benchmark | Do not imply tradability unless costs, turnover, and capacity are addressed. |
| portfolio backtest curve | A strategy, portfolio, or benchmark path is compared through historical cumulative value. | `xts`, `PerformanceAnalytics`, `ggplot2::geom_line` | portfolio returns, benchmark returns, date, rebalance rule, costs/capacity status | Label as historical or synthetic backtest unless implementation costs, turnover, and capacity are addressed. |
| factor exposure/beta heatmap | Betas or characteristic exposures vary by portfolio, time, or model. | `ggplot2::geom_tile`, `modelsummary`, `broom` | beta/exposure matrix, factor names, portfolio labels, model window | Heatmap midpoint and color scale must have economic meaning. |
| rolling beta/alpha plot | Time-varying exposures, alphas, or instability are central. | `zoo`, `slider`, `PerformanceAnalytics`, `ggplot2` | rolling window, date, alpha/beta, CI when available, factor model | Window length and re-estimation frequency must be stated. |
| backtest performance panel | Strategy or signal performance over time is discussed. | `PerformanceAnalytics`, `xts`, `ggplot2`, `patchwork` | returns, benchmark, date, costs, turnover when available | Do not imply investable strategy if costs/capacity are absent. |
| drawdown and turnover plot | Risk, capacity, or implementation frictions are discussed. | `PerformanceAnalytics`, `ggplot2` line/bar panels | returns, cumulative value, drawdown, turnover, dates | Drawdown and turnover definitions must be explicit. |
| risk-return scatter | Strategies, portfolios, managers, or factors must be compared by return against realized risk. | `PerformanceAnalytics::chart.RiskReturnScatter`, `ggplot2::geom_point`, `ggrepel` | annualized return, annualized volatility or risk metric, labels, benchmark, sample window | Frequency, annualization rule, risk definition, and benchmark/quadrant labels must be stated. |
| turnover/cost/capacity table | Implementation frictions need concise disclosure. | `dplyr`, `modelsummary`, `tinytable` | turnover, bid-ask spread, commission/slippage, ADV/capacity, portfolio size | Cost assumptions and capacity units must be stated. |
| liquidity/spread/volume diagnostic | Market microstructure, liquidity, or trading feasibility affects interpretation. | `ggplot2` line/dot/facet plots, `data.table` | spread, volume, depth, volatility, date/event time, security group | Frequency, market hours, and outlier handling must be documented. |
| intraday event-time plot | High-frequency market reaction or microstructure response is event-time aligned. | `data.table`, `ggplot2::geom_line`, `geom_ribbon` | timestamp/event time, return/spread/volume, benchmark, event window | Trading calendar, timezone, and event alignment must be explicit. |
| volatility/risk decomposition plot | Risk, variance, or factor contribution is decomposed across sources or time. | `PerformanceAnalytics`, `ggplot2` stacked bars/area | risk component, portfolio/model, date or horizon, contribution | Components must sum to the reported risk measure or explain residuals. |

## Corporate, Banking, Fintech, And Policy Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| institutional/event timeline | Institutional setting, regulation, treatment rollout, or event sequence must be readable. | `ggplot2::geom_segment`, `geom_point`, `ggrepel` | dates, events, categories, source references | Timeline cannot introduce dates or events absent from source evidence. |
| geographic exposure map | Policy, branch, loan, firm, investor, or county exposure varies geographically. | `sf`, `ggplot2`, `tmap` | geography ID, shapefile/source, exposure/rate, year/sample | Projection, denominator, and geographic crosswalk must be recorded. |
| network/exposure graph | Bank-firm, supply-chain, board, ownership, or transaction networks support the claim. | `igraph`, `ggraph`, `tidygraph` | node table, edge table, weights, time, sample filters | Network construction, thresholding, and isolated nodes must be disclosed. |
| rating or credit transition matrix | Credit states, risk grades, delinquency, or ratings evolve across states. | `dplyr`, `ggplot2::geom_tile`, `tinytable` | origin state, destination state, horizon, counts/rates | Rows/columns must reconcile to denominators and horizon. |
| funding or loan flow diagram | Balance-sheet flows, funding channels, borrower transitions, or platform flows need a map. | `ggalluvial`, `ggplot2`, `networkD3` when interactive output is acceptable | source, destination, amount/count, time, category | Flows must conserve totals unless leakage/default/exit is labeled. |

## Structural, Theory, Macro-Finance, ML, And Composite Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| distribution or binscatter plot | Sample distribution, nonlinearity, or binned relation supports design or results. | `ggplot2`, `binsreg` when available | variable, bins or raw data, sample, weights | Binning and winsorization must be stated. |
| model intuition diagram | A theory, institutional setting, or mechanism needs a compact schematic. | `DiagrammeR`, `ggplot2` annotations, LaTeX/TikZ when requested | model objects, timing, agents, equations or primitives | Diagram cannot introduce assumptions absent from the theory/model section. |
| calibration/moment-fit table | Structural, macro-finance, or equilibrium model credibility depends on targeted moments. | `dplyr`, `modelsummary`, `tinytable` | parameter, target moment, model moment, data moment, source | Targeted and untargeted moments must be distinguished. |
| impulse response function plot | Macro-finance, VAR, local projection, or policy shocks need dynamic responses. | `vars`, `lpirfs`, `ggplot2::geom_ribbon` | horizon, response, shock, CI, model/specification | Shock scaling, horizon units, and interval definition must be labeled. |
| model fit versus data moments plot | Model fit is judged visually against empirical moments or time paths. | `ggplot2` scatter/line/facet panels | model predictions, data moments, sample, parameterization | Do not hide moments the model misses; targeted moments must be marked. |
| counterfactual/welfare decomposition plot | Structural or policy results decompose welfare, surplus, or counterfactual channels. | `ggplot2` stacked/dot/waterfall style plots | counterfactual scenario, component, estimate, uncertainty if available | Baseline, scenario definition, and units must be explicit. |
| comparative statics plot | Theory or structural model predictions vary with primitives or parameters. | `ggplot2::geom_line`, facets, contour plots | parameter grid, outcome, model version, equilibrium status | Parameter range must be justified and infeasible regions labeled. |
| model performance table | Prediction, ML, text, or fintech model comparison needs out-of-sample metrics. | `yardstick`, `modelsummary`, `tinytable` | train/validation/test split, metric, baseline, seed/fold, model | Out-of-sample split and baseline must be stated; no leakage. |
| calibration/lift plot | Predicted risk, default, fraud, return, or adoption scores need calibration or ranking checks. | `yardstick`, `ggplot2` calibration/decile plot | predicted score, outcome, bins/deciles, sample split | Distinguish calibration from discrimination and state decile construction. |
| feature importance/SHAP plot | ML or text model interpretation supports a finance mechanism or prediction claim. | `vip`, `shapviz`, `ggplot2` | feature, importance/SHAP value, model, validation sample | Do not treat feature importance as causal evidence. |
| text topic/time-series plot | Disclosure, news, filings, or social-media topics vary over time or groups. | `quanteda`, `stm`, `tidytext`, `ggplot2` | document IDs, date/group, topic/term score, preprocessing choices | Preprocessing, dictionary/topic labels, and document coverage must be stated. |
| multi-panel evidence composite | A main figure needs aligned identification, effect size, mechanism, and robustness panels. | `patchwork`, `cowplot`, `ggplot2`, `tinytable` | panel-level source data, common sample definitions, display IDs | Every panel must support the same core conclusion and share palette semantics. |
| heatmap or bubble matrix | High-dimensional model, portfolio, country, sector, or robustness comparisons need compact display. | `ggplot2::geom_tile`, `geom_point`, `ComplexHeatmap` | row/column categories, value, uncertainty/status, ordering rule | Color scale, ordering, and missing cells must be explained. |
| radar/polar multi-metric chart | Many methods or portfolios are compared across standardized metrics and a table is unreadable. | `ggplot2`, `ggforce`, `fmsb` when available | metric matrix, normalization rule, method labels, benchmark radii | Normalization must be transparent; avoid when metrics lack common direction. |
| embedding/cluster plot | Text, firm, investor, patent, or transaction embeddings are used for exploratory grouping. | `uwot`, `Rtsne`, `ggplot2`, `ggrepel` | embedding coordinates, labels, preprocessing, seed, sample | Treat as exploratory unless validated; seed and preprocessing must be recorded. |
