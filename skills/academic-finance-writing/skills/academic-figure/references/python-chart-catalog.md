# Python Chart Catalog For Finance Figures

Use this catalog only after Python has been selected by the Backend Language Gate. Each row maps a
finance display need to the normal Python route, required source data, and blocking QA checks.

Before drawing, apply `references/finance-palette.md`: select one paper-level palette profile and
reuse the same semantic color mapping across all figures.

## Catalog Parity Contract

This catalog must stay one-to-one with `references/r-chart-catalog.md`: use the same display family
names and the same row order. If adding, removing, or renaming a display family, update both
catalogs and run `scripts/validate_chart_catalog_parity.py`.

## Data Profiling And Sample Construction Displays

| Display family | Use when | Python route | Required source data | Blocking QA |
|---|---|---|---|---|
| summary statistics table | Data section or sample description needs distribution, missingness, and group comparisons. | `pandas`, `numpy`, `statsmodels.iolib`, custom LaTeX `booktabs` writer | variables, sample filters, group labels, N, mean, SD, percentiles, missingness | Units, winsorization, sample window, and variable scaling must be stated. |
| variable definition table | Readers need construction, source, timing, or scaling for outcomes, treatments, signals, and controls. | `pandas`, custom LaTeX `booktabs` writer | variable name, definition, source, transformation, timing lag, unit | Do not leave vendor mnemonics unexplained; transformations must match Methods. |
| sample construction flow | Exclusions, filters, merges, or cohort formation determine the final sample. | `graphviz`, `networkx`, `matplotlib.patches` | starting counts, exclusion reasons, merge drops, final analytic counts | Counts must reconcile and match the Data section and code-output map. |
| panel coverage heatmap | Entity-time coverage, entry/exit, or unbalanced panels affect interpretation. | `pandas`, `seaborn.heatmap`, `matplotlib` | entity or group, time, observation indicator/count, sample filters | Axis ordering and aggregation must not hide sparse coverage or attrition. |
| missingness diagnostic | Missing values or structural missingness affect sample selection or variable availability. | `pandas.isna`, `missingno`, `seaborn.heatmap`, `matplotlib.bar` | variable, missing indicator, time/group if relevant, missing-code rules | Distinguish true zero, not applicable, and missing; high-missing variables must be flagged. |
| merge/linkage diagnostic table | Data sources are linked by identifiers and match rates determine sample credibility. | `pandas`, custom LaTeX `booktabs` writer | left/right counts, match rates, duplicate keys, unmatched reason codes | Join type, key uniqueness, and row-count changes must be visible. |
| outlier/winsorization diagnostic | Extreme values, trimming, or winsorization could drive estimates. | `pandas`, `seaborn.boxplot`/`histplot`, `matplotlib.ecdf` when available | raw and transformed values, cutoffs, sample, variable units | Show cutoff rules and whether results use raw, trimmed, or winsorized variables. |

## Econometric And Identification Displays

| Display family | Use when | Python route | Required source data | Blocking QA |
|---|---|---|---|---|
| regression table | Main or robustness estimates support a finance claim. | `statsmodels`, `linearmodels`, custom LaTeX `booktabs` writer | estimate, SE/CI, sample, FE, controls, clustering, N | Notes must state sample, FE, controls, SE clustering, and economic scaling. |
| event-study figure | Dynamic effects, pre-trends, or market reaction timing is central. | `pandas`, `matplotlib.errorbar`, `statsmodels`, `linearmodels` | event time, estimate, CI, omitted period, sample | Omitted period, CI, and anticipation/leakage boundary must be visible. |
| parallel-trends plot | DiD credibility depends on pre-treatment behavior before treatment. | `pandas`, `matplotlib.errorbar`, `linearmodels`, `statsmodels` | relative time, cohort/group, estimate, CI, omitted period | Pre-period coefficients must not be visually compressed or selectively omitted. |
| treatment timing/adoption plot | Staggered adoption, policy exposure timing, or cohort composition affects design. | `pandas`, `seaborn.heatmap`, `matplotlib.bar` | unit/group, adoption date, cohort, exposure intensity, sample counts | Cohort definitions and never-treated/comparison groups must be identifiable. |
| coefficient plot | A set of model estimates or specifications must be compared visually. | `pandas`, `matplotlib.errorbar`, `seaborn` | estimate, interval, model/spec label, reference line | Axis scale and reference line must match coefficient interpretation. |
| robustness grid | Many alternative specifications must be summarized compactly. | `pandas`, `seaborn.heatmap`, `matplotlib` dot grid | specification labels, estimate/sign/status, sample notes | Do not hide failed, missing, or underpowered robustness checks. |
| robustness table | Alternative samples, controls, windows, clustering choices, or model variants must be reported as exact numbers. | `pandas`, `statsmodels`, `linearmodels`, custom LaTeX `booktabs` writer | specification labels, estimate, SE/CI, N, FE, controls, clustering, sample/window notes | Main coefficient definition, sample changes, controls, FE, and standard-error rule must be visible; do not mix incompatible outcomes in one table. |
| mechanism or channel plot | Evidence supports a proposed mechanism rather than only the main effect. | `pandas`, `seaborn`, `matplotlib` | channel variable, estimate or statistic, uncertainty, source model | Caption must distinguish mechanism evidence from causal proof. |
| covariate balance plot | Matching, weighting, experiment checks, or treated/control comparisons need balance evidence. | `pandas`, `matplotlib` dot plot, `seaborn` | covariate, standardized difference, before/after adjustment, threshold | Show before and after adjustment when applicable; threshold must be labeled. |
| placebo/permutation inference plot | Placebo dates, placebo units, randomization inference, or donor placebos support identification. | `pandas`, `matplotlib.hist`, `seaborn.ecdfplot` | placebo estimates, true estimate, p-value/rank, randomization scheme | True estimate and placebo construction must be explicit. |
| RD binned scatter plot | Regression discontinuity identification or local fit is central. | `pandas`, `matplotlib`, `rdrobust` when available, custom bins | running variable, outcome, cutoff, bins, bandwidth, polynomial/local fit | Cutoff, bandwidth, and side-specific fits must be visible. |
| RD density/manipulation plot | Sorting around a cutoff threatens RD validity. | `pandas`, `seaborn.histplot`/`kdeplot`, `rdrobust` when available | running variable, cutoff, bin width/bandwidth, density estimates | Manipulation test and binning choices must be reported. |
| IV first-stage diagnostic | Instrument relevance or weak-instrument concern must be reported. | `linearmodels`, `statsmodels`, `pandas`, `matplotlib` | first-stage estimate, F-statistic, partial R2, sample, FE/controls | Weak-instrument threshold and excluded instrument definition must be stated. |
| synthetic-control path plot | Treated and synthetic outcomes are compared before and after intervention. | `pandas`, `numpy`, `matplotlib`, synthetic-control package when available | treated outcome, synthetic outcome, intervention date, pre/post periods | Pre-period fit and intervention date must be clear. |
| synthetic-control weights/balance table | Donor composition or predictor balance supports synthetic-control credibility. | `pandas`, custom LaTeX `booktabs` writer | donor weights, predictors, treated values, synthetic values | Nonzero donors and predictor balance must reconcile with path plot. |
| bunching/density plot | Bunching, thresholds, tax notches, or discontinuous incentives drive identification. | `pandas`, `seaborn.histplot`, `matplotlib` fitted line | running variable, threshold/notch, bin counts, counterfactual fit | Bin width and counterfactual construction must be disclosed. |
| shift-share exposure diagnostic | Bartik/shift-share exposure or industry/geographic shares drive identification. | `pandas`, `geopandas` when geographic, `seaborn`, `matplotlib` | shares, shocks, exposure measure, geography/industry/time | Exposure construction and dominant-share sensitivity must be visible or tabled. |

## Asset Pricing, Market Microstructure, And Backtest Displays

| Display family | Use when | Python route | Required source data | Blocking QA |
|---|---|---|---|---|
| portfolio-sort table | Returns or characteristics are sorted by signal, quantile, or treatment. | `pandas`, `numpy`, custom LaTeX `booktabs` writer | universe, signal, breakpoints, weights, returns/alphas, SE | Breakpoints, weighting, lag, rebalancing, and costs/capacity status must be stated. |
| factor-model performance table | Alphas, betas, spreads, or risk-adjusted returns are central. | `statsmodels`, `linearmodels`, `pandas` | returns, factor data, model, alpha/beta, SE/t-stat | Factor source, frequency, and benchmark model must be named. |
| cumulative abnormal return plot | Market reaction or event-window performance is shown. | `pandas`, `matplotlib.plot`, `fill_between` | event date, abnormal return, window, benchmark, CI if claimed | Window and benchmark must match text claims. |
| long-short cumulative return curve | A long-short factor, spread portfolio, or strategy path is interpreted over time. | `pandas`, `numpy`, `matplotlib.plot` | long return, short return, spread return, date, benchmark | Do not imply tradability unless costs, turnover, and capacity are addressed. |
| portfolio backtest curve | A strategy, portfolio, or benchmark path is compared through historical cumulative value. | `pandas`, `numpy`, `matplotlib.plot`, `empyrical` when available | portfolio returns, benchmark returns, date, rebalance rule, costs/capacity status | Label as historical or synthetic backtest unless implementation costs, turnover, and capacity are addressed. |
| factor exposure/beta heatmap | Betas or characteristic exposures vary by portfolio, time, or model. | `pandas`, `seaborn.heatmap`, `statsmodels` | beta/exposure matrix, factor names, portfolio labels, model window | Heatmap midpoint and color scale must have economic meaning. |
| rolling beta/alpha plot | Time-varying exposures, alphas, or instability are central. | `pandas.rolling`, `statsmodels`, `matplotlib` | rolling window, date, alpha/beta, CI when available, factor model | Window length and re-estimation frequency must be stated. |
| backtest performance panel | Strategy or signal performance over time is discussed. | `pandas`, `numpy`, `matplotlib`, `empyrical` when available | returns, benchmark, date, costs, turnover when available | Do not imply investable strategy if costs/capacity are absent. |
| drawdown and turnover plot | Risk, capacity, or implementation frictions are discussed. | `pandas`, `numpy`, `matplotlib` line/bar panels | returns, cumulative value, drawdown, turnover, dates | Drawdown and turnover definitions must be explicit. |
| risk-return scatter | Strategies, portfolios, managers, or factors must be compared by return against realized risk. | `pandas`, `numpy`, `matplotlib.scatter`, `adjustText` when available | annualized return, annualized volatility or risk metric, labels, benchmark, sample window | Frequency, annualization rule, risk definition, and benchmark/quadrant labels must be stated. |
| turnover/cost/capacity table | Implementation frictions need concise disclosure. | `pandas`, custom LaTeX `booktabs` writer | turnover, bid-ask spread, commission/slippage, ADV/capacity, portfolio size | Cost assumptions and capacity units must be stated. |
| liquidity/spread/volume diagnostic | Market microstructure, liquidity, or trading feasibility affects interpretation. | `pandas`, `seaborn`, `matplotlib` line/dot/facet plots | spread, volume, depth, volatility, date/event time, security group | Frequency, market hours, and outlier handling must be documented. |
| intraday event-time plot | High-frequency market reaction or microstructure response is event-time aligned. | `pandas`, `matplotlib`, `seaborn`, timezone-aware indexes | timestamp/event time, return/spread/volume, benchmark, event window | Trading calendar, timezone, and event alignment must be explicit. |
| volatility/risk decomposition plot | Risk, variance, or factor contribution is decomposed across sources or time. | `pandas`, `numpy`, `matplotlib.stackplot`/bars | risk component, portfolio/model, date or horizon, contribution | Components must sum to the reported risk measure or explain residuals. |

## Corporate, Banking, Fintech, And Policy Displays

| Display family | Use when | Python route | Required source data | Blocking QA |
|---|---|---|---|---|
| institutional/event timeline | Institutional setting, regulation, treatment rollout, or event sequence must be readable. | `pandas`, `matplotlib.hlines`, annotations | dates, events, categories, source references | Timeline cannot introduce dates or events absent from source evidence. |
| geographic exposure map | Policy, branch, loan, firm, investor, or county exposure varies geographically. | `geopandas`, `shapely`, `matplotlib` | geography ID, shapefile/source, exposure/rate, year/sample | Projection, denominator, and geographic crosswalk must be recorded. |
| network/exposure graph | Bank-firm, supply-chain, board, ownership, or transaction networks support the claim. | `networkx`, `pandas`, `matplotlib` | node table, edge table, weights, time, sample filters | Network construction, thresholding, and isolated nodes must be disclosed. |
| rating or credit transition matrix | Credit states, risk grades, delinquency, or ratings evolve across states. | `pandas.crosstab`, `seaborn.heatmap`, custom LaTeX table | origin state, destination state, horizon, counts/rates | Rows/columns must reconcile to denominators and horizon. |
| funding or loan flow diagram | Balance-sheet flows, funding channels, borrower transitions, or platform flows need a map. | `matplotlib.sankey`, `plotly` only if acceptable, `networkx`/patches | source, destination, amount/count, time, category | Flows must conserve totals unless leakage/default/exit is labeled. |

## Structural, Theory, Macro-Finance, ML, And Composite Displays

| Display family | Use when | Python route | Required source data | Blocking QA |
|---|---|---|---|---|
| distribution or binscatter plot | Sample distribution, nonlinearity, or binned relation supports design or results. | `pandas`, `seaborn.histplot`, `matplotlib`, `binsreg` when available | variable, bins or raw data, sample, weights | Binning and winsorization must be stated. |
| model intuition diagram | A theory, institutional setting, or mechanism needs a compact schematic. | `networkx`, `graphviz`, `matplotlib` annotations, LaTeX/TikZ when requested | model objects, timing, agents, equations or primitives | Diagram cannot introduce assumptions absent from the theory/model section. |
| calibration/moment-fit table | Structural, macro-finance, or equilibrium model credibility depends on targeted moments. | `pandas`, custom LaTeX `booktabs` writer | parameter, target moment, model moment, data moment, source | Targeted and untargeted moments must be distinguished. |
| impulse response function plot | Macro-finance, VAR, local projection, or policy shocks need dynamic responses. | `statsmodels`, `localprojections` when available, `matplotlib.fill_between` | horizon, response, shock, CI, model/specification | Shock scaling, horizon units, and interval definition must be labeled. |
| model fit versus data moments plot | Model fit is judged visually against empirical moments or time paths. | `pandas`, `matplotlib`, `seaborn` facets | model predictions, data moments, sample, parameterization | Do not hide moments the model misses; targeted moments must be marked. |
| counterfactual/welfare decomposition plot | Structural or policy results decompose welfare, surplus, or counterfactual channels. | `pandas`, `matplotlib` stacked/dot/waterfall style plots | counterfactual scenario, component, estimate, uncertainty if available | Baseline, scenario definition, and units must be explicit. |
| comparative statics plot | Theory or structural model predictions vary with primitives or parameters. | `pandas`, `numpy`, `matplotlib` line/facet/contour plots | parameter grid, outcome, model version, equilibrium status | Parameter range must be justified and infeasible regions labeled. |
| model performance table | Prediction, ML, text, or fintech model comparison needs out-of-sample metrics. | `scikit-learn`, `pandas`, custom LaTeX `booktabs` writer | train/validation/test split, metric, baseline, seed/fold, model | Out-of-sample split and baseline must be stated; no leakage. |
| calibration/lift plot | Predicted risk, default, fraud, return, or adoption scores need calibration or ranking checks. | `sklearn.calibration`, `pandas.qcut`, `matplotlib` | predicted score, outcome, bins/deciles, sample split | Distinguish calibration from discrimination and state decile construction. |
| feature importance/SHAP plot | ML or text model interpretation supports a finance mechanism or prediction claim. | `shap`, `sklearn.inspection`, `matplotlib.barh` | feature, importance/SHAP value, model, validation sample | Do not treat feature importance as causal evidence. |
| text topic/time-series plot | Disclosure, news, filings, or social-media topics vary over time or groups. | `scikit-learn`, `gensim`, `pandas`, `matplotlib` | document IDs, date/group, topic/term score, preprocessing choices | Preprocessing, dictionary/topic labels, and document coverage must be stated. |
| multi-panel evidence composite | A main figure needs aligned identification, effect size, mechanism, and robustness panels. | `matplotlib.gridspec`, `subplot_mosaic`, `pandas`, `seaborn` | panel-level source data, common sample definitions, display IDs | Every panel must support the same core conclusion and share palette semantics. |
| heatmap or bubble matrix | High-dimensional model, portfolio, country, sector, or robustness comparisons need compact display. | `pandas`, `seaborn.heatmap`, `matplotlib.scatter` | row/column categories, value, uncertainty/status, ordering rule | Color scale, ordering, and missing cells must be explained. |
| radar/polar multi-metric chart | Many methods or portfolios are compared across standardized metrics and a table is unreadable. | `matplotlib` polar axes, `numpy`, `pandas` | metric matrix, normalization rule, method labels, benchmark radii | Normalization must be transparent; avoid when metrics lack common direction. |
| embedding/cluster plot | Text, firm, investor, patent, or transaction embeddings are used for exploratory grouping. | `umap-learn`, `scikit-learn`, `matplotlib`, `adjustText` when available | embedding coordinates, labels, preprocessing, seed, sample | Treat as exploratory unless validated; seed and preprocessing must be recorded. |
