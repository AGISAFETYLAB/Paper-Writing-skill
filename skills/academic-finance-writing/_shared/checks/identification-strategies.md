# Finance Identification And Method Writing

Use this reference when drafting or auditing methods, identification, results, robustness, or
reviewer-risk text. It is a writing guide, not permission to invent analyses.

## Source Anchors

- American Economic Association JEL C guide: Mathematical and Quantitative Methods are classified
  separately from application fields, and applied papers should also be classified under the
  appropriate application category:
  https://www.aeaweb.org/jel/guide/jel.php?class=C
- American Economic Association JEL G: Financial Economics supplies the application field for
  finance manuscripts, separate from method labels:
  https://www.aeaweb.org/econlit/jelCodes.php?view=jel
- Elsevier financial-economics scopes cover theoretical, empirical, policy-oriented,
  structural-estimation, experimental, AI/machine-learning, and innovative-data-source finance
  contributions:
  https://shop.elsevier.com/journals/subjects/social-sciences-and-humanities/economics-and-finance/financial-economics/financial-economics-general

## Method Family Boundary

Use method family after paper_type. The selected structural `paper_type` controls section order.
The method family controls evidence standards, assumptions, diagnostics, robustness, and display
requirements. A method family is not a finance domain and does not replace the selected paper-type
profile.

Record one primary method family and any secondary method family in the Paper Framework. If a method
requires a structural deviation, mark it as an approved deviation from the paper-type profile rather
than silently changing the section plan.

## Method Family Index

| Method family | Methods covered | Writing use | Required pressure |
|---|---|---|---|
| causal identification | Difference-in-Differences, Instrumental Variables, Regression Discontinuity, Synthetic Control, policy/event treatment designs | state source of identifying variation, treated/control units, timing, identifying assumption, and causal-language boundary | pre-trends, exclusion/locality/manipulation tests, placebo or permutation inference, clustering/dependence |
| event-time market response | event studies, cumulative abnormal returns, dynamic treatment effects around corporate, market, regulatory, or policy events | define event source, window, expected-return model, abnormal return metric, leakage/anticipation checks | event-date credibility, multiple-event dependence, pre-event behavior, window sensitivity |
| asset-pricing and backtest evaluation | portfolio sorts, factor models, anomaly tests, fund-performance tests, trading/backtest designs | define universe, signal timing, breakpoints, weights, rebalancing, factor benchmark, alpha/spread, economic magnitude | costs, turnover, capacity, liquidity, look-ahead bias, data snooping, benchmark choice |
| structural or theory-linked estimation | structural estimation, calibration, simulated method of moments, model counterfactuals | state primitives, moments, estimation method, fit, counterfactual, and welfare/objective function | parameter identification, targeted/untargeted moments, sensitivity, computational boundary |
| prediction, machine learning, and text measurement | prediction models, causal ML, risk scoring, text/NLP measures, alternative data measurement | define target timing, split, leakage prevention, feature construction, metric, benchmark, and interpretability | out-of-sample performance, sample splitting/cross-fitting, construct validation, causal boundary |
| experimental, survey, and field-design evidence | lab/field experiments, surveys, preference/belief elicitation, questionnaire-based evidence | define sampling frame, treatment/task, response measure, balance, design, and construct | external validity, attrition, multiple testing, survey measurement, behavioral mechanism |
| theoretical model and proof support | analytical models, comparative statics, equilibrium characterization, proofs, numerical examples | state environment, assumptions, propositions, intuition, comparative statics, and empirical or institutional interpretation | assumption transparency, equilibrium selection, robustness of propositions, mapping to finance setting |

## Difference-in-Differences

Lead with the policy, shock, rule change, or institutional event that creates treatment variation.
State treated and control groups, treatment timing, and the identifying assumption in finance terms.

Required writing anchors:

- treatment timing and exposure definition
- unit and panel frequency
- parallel-trends argument and pre-trend evidence
- anticipation risk and event timing
- estimator choice for staggered adoption when relevant
- clustering or serial-correlation treatment

Use causal language only when the design and assumptions are stated. If pre-trends or controls are
missing, write "consistent with" or "associated with" and mark the gap.

## Instrumental Variables

Name the instrument early and explain what variation it isolates. Do not let a first-stage statistic
stand in for the exclusion restriction.

Required writing anchors:

- relevance channel
- exclusion restriction in economic terms
- first-stage strength or weak-instrument handling
- complier or local-effect interpretation when relevant
- why the instrument does not directly affect the outcome

If the instrument is a shift-share or Bartik design, describe both shares and shocks, and state
whether identification relies on share exogeneity, shock exogeneity, or both.

## Regression Discontinuity

Lead with the running variable and cutoff. Emphasize locality: the estimate applies near the cutoff.

Required writing anchors:

- running variable, cutoff, treatment assignment rule
- bandwidth choice and sensitivity
- manipulation or density test
- covariate continuity
- local interpretation and external-validity boundary

For fuzzy RD, report reduced form and first stage separately before the ratio estimate.

## Synthetic Control

Use for settings with a treated market, firm, country, policy, or event and a donor pool.

Required writing anchors:

- treated unit and event date
- donor-pool eligibility and exclusions
- pre-period fit and predictor balance
- donor weights or aggregate contribution
- placebo or permutation inference
- interpretation of the counterfactual path

Poor pre-period fit is a blocker for strong claims.

## Event Studies

Use for market reactions, policy events, corporate events, regulatory shocks, or dynamic treatment
effects.

Required writing anchors:

- event definition and event-date source
- estimation window and event window
- expected-return model or fixed-effect specification
- abnormal return, CAR, or dynamic coefficient definition
- leakage and anticipation checks
- multiple-event or clustered-event dependence treatment

An event-study figure should show pre-event behavior when the claim depends on no anticipation or
parallel dynamics.

## Portfolio Sorts And Factor Models

Use for asset-pricing, anomaly, fund, factor, or trading-strategy manuscripts.

Required writing anchors:

- universe, sample window, return frequency, and filters
- signal construction and timing lag
- breakpoints, weighting, rebalancing, and holding period
- benchmark or factor model
- transaction costs, turnover, shorting, capacity, and liquidity when performance is interpreted
- alpha, spread, t-statistic, and economic magnitude

Do not write "profitable strategy" unless costs, slippage, capacity, implementation timing, and
benchmark choice are handled. Use "paper return spread" or "synthetic backtest result" otherwise.

## Structural Estimation

Use when a finance model is estimated to recover primitives or run counterfactuals.

Required writing anchors:

- model environment and primitives
- data moments or variation identifying each key parameter
- estimation method and computational boundary
- model fit against targeted and untargeted moments
- counterfactual design and welfare/objective function
- sensitivity to key assumptions

State the model's identifying assumptions in words before equations.

## Machine Learning And Prediction

Use when ML supports prediction, heterogeneity, text measurement, risk scoring, or causal estimation.

Required writing anchors:

- prediction target and timing
- train/validation/test split and leakage prevention
- feature construction and missing-data treatment
- out-of-sample metric and benchmark model
- interpretability and economic mechanism boundary
- for causal ML, sample splitting/cross-fitting and valid uncertainty

Do not treat predictive accuracy as causal evidence.

## Multiple Strategy Papers

When a paper uses multiple designs, name one primary design and explain how the others change the
interpretation:

- robustness to a threat
- complementary population or margin
- mechanism test
- external-validity check

Do not present a menu of designs without saying which result the paper stands behind.
