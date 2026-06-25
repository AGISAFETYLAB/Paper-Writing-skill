# Prediction Model Profile

Use this profile for studies that develop, validate, update, compare, or deploy diagnostic,
prognostic, screening, or monitoring prediction models, including regression, machine learning, and
AI systems.

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Protect model specification, validation
design, performance metrics, calibration, and clinical-utility evidence.

## Checklist / Study-Type Pairing

Pair with TRIPOD or TRIPOD+AI as applicable. Use STARD-AI only when the model is framed as a
diagnostic accuracy test against a reference standard.

## Priority Contract

- Primary core: Methods.
- Evidence core: Results with validation and performance.
- Compress first: model-family background, implementation detail that can move to supplement, and
  exploratory feature analyses.
- Core floor: source population, outcome horizon, predictors, sample size/events, missingness,
  modeling, internal/external validation, discrimination, calibration, and utility cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / structured abstract | outside main budget unless target counts it | State target population, outcome, prediction horizon, validation setting, and performance boundary. |
| 1 | Introduction | 8-12% | Motivate the decision problem, current gap, and intended model use. |
| 2 | Methods | 36-44% | Define data sources, participants, outcome, predictors, sample size/events, missingness, modeling pipeline, validation split, performance measures, calibration, and clinical-utility analysis. |
| 3 | Results | 30-38% | Present flow, characteristics, model specification, discrimination, calibration, decision curve or utility, subgroup/sensitivity results, and failure cases. |
| 4 | Discussion | 14-20% | Interpret performance, transportability, implementation risks, fairness/bias, limitations, and next validation needs. |
| 5 | Conclusions | 1-3% | State the validation-bounded conclusion and avoid deployment claims without evidence. |
| Back | TRIPOD checklist / model card or supplement | outside main text unless target counts it | Carry coefficients/features, hyperparameters, code/data statements, and extended validation. |

## Flexible Adjustment Notes

- Model performance without calibration is not enough for a strong clinical-use claim.
- If external validation is absent, label the model as internally validated or development-only.
- Keep patient-specific medical advice out of the manuscript.
