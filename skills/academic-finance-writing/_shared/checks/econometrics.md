# Finance Econometrics And Identification Checks

Use this reference when claims depend on regressions, event studies, backtests, portfolio sorts, or
causal identification.

Load `_shared/checks/identification-strategies.md` for method-specific writing requirements.

## Empirical Checks

| Claim type | Required anchors |
|---|---|
| Return/alpha | factor model or benchmark, sample window, rebalancing, weighting |
| Portfolio sort | signal construction, breakpoints, holding period, risk adjustment |
| Event study | event date, estimation window, event window, expected-return model |
| DiD / policy | treated/control, timing, parallel trends, placebo/pre-trends |
| IV / RD | instrument/running variable, exclusion/local assumptions |
| Prediction/backtest | train/test split, out-of-sample period, transaction costs, turnover |
| Backtest curve / drawdown | cumulative-value definition, benchmark, costs/capacity status, sample window |
| Risk-return scatter | annualization rule, risk metric, return metric, benchmark/quadrant interpretation |
| Robustness table | alternative samples/specifications, FE/controls, clustering, N, main coefficient definition |

## Required Method Paragraphs

Each empirical method section must answer:

1. What variation or model feature identifies the estimate?
2. What would make the interpretation wrong?
3. Which table/figure tests or bounds that concern?
4. Which standard errors, clustering, bootstrap, or inference method is used?
5. What economic magnitude makes the result matter?

If any answer is missing, weaken claims and mark the item in the Finance Evidence Ledger.

## Wording Rules

- `associated with` for descriptive regressions.
- `consistent with` when mechanisms are suggestive.
- `causal effect` only when identification assumptions are explicit and supported.
- `profitable strategy` only if costs, slippage, capacity, and benchmark are handled; otherwise use
  `synthetic backtest result` or `paper return`.
