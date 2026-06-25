# Observational Study Profile

Use this profile for cohort, case-control, cross-sectional, registry, claims, EHR, survey, or other
noninterventional empirical studies centered on exposure, association, prognosis, utilization, or
outcome patterns.

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Protect design, exposure/outcome,
missingness, confounding, and sensitivity-analysis detail.

## Checklist / Study-Type Pairing

Pair with STROBE, RECORD, SAGER, or other extensions when the source data and target journal require
them.

## Priority Contract

- Primary core: Methods.
- Evidence core: Results.
- Compress first: broad epidemiologic background, speculative mechanisms, and secondary subgroup
  results that can move to supplement.
- Core floor: source population, eligibility, exposure, outcome, covariates, bias/confounding,
  missingness, denominator accounting, and statistical model must remain explicit.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / structured abstract / Key Points when required | outside main budget unless target counts it | State design, population, exposure/outcome, main association, and uncertainty. |
| 1 | Introduction | 10-14% | Establish the clinical/public-health problem, knowledge gap, and objective. |
| 2 | Methods | 32-40% | Define design, setting/data source, participants, variables, exposure, outcomes, covariates, bias/confounding strategy, missingness, and statistical analysis. |
| 3 | Results | 30-38% | Report flow/eligibility, baseline characteristics, primary association or descriptive finding, uncertainty, subgroup/sensitivity analyses, and missingness. |
| 4 | Discussion | 16-22% | Interpret association or descriptive evidence, compare with literature, state limitations and residual confounding, and avoid causal overreach. |
| 5 | Conclusions | 1-3% | State the evidence-bounded conclusion. |
| Back | Declarations / STROBE checklist / supplement | outside main text unless target counts it | Carry data source details, extended models, code/data statements, and checklist matrix. |

## Flexible Adjustment Notes

- If the manuscript develops or validates a prediction model, prefer `prediction-model.md`.
- If it evaluates a diagnostic test against a reference standard, prefer `diagnostic-accuracy.md`.
- Treat causal language as a special claim requiring design, temporality, and identification support.
