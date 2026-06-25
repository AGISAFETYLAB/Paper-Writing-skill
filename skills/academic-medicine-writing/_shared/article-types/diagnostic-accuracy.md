# Diagnostic Accuracy Profile

Use this profile for studies that evaluate one or more index tests against a reference standard for
classification, diagnosis, staging, prognosis-related testing, or screening.

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Protect population, index test,
reference standard, thresholds, blinding, and accuracy-analysis detail.

## Checklist / Study-Type Pairing

Pair with STARD 2015 and STARD-AI when the diagnostic system uses AI or machine learning.

## Priority Contract

- Primary core: Methods.
- Evidence core: Results with 2x2/accuracy metrics and uncertainty.
- Compress first: long technology background, exploratory subgroup detail, and secondary metrics.
- Core floor: eligibility, test conduct, reference standard, threshold definition, blinding,
  indeterminate results, missingness, and accuracy-analysis methods cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / structured abstract | outside main budget unless target counts it | State index test, target condition, reference standard, population, and accuracy summary. |
| 1 | Introduction | 8-12% | Define diagnostic problem, current standard, and objective. |
| 2 | Methods | 34-42% | Describe design, setting, participants, index test, reference standard, timing, thresholds, blinding, sample size, indeterminate/missing results, and statistical analysis. |
| 3 | Results | 32-40% | Present participant/test flow, baseline characteristics, 2x2 data, sensitivity/specificity or AUC, calibration/decision curve if applicable, and subgroup/sensitivity analyses. |
| 4 | Discussion | 14-20% | Interpret diagnostic utility, applicability, bias risks, comparison with alternatives, and implementation limits. |
| 5 | Conclusions | 1-3% | State the test-performance conclusion within the studied setting. |
| Back | STARD checklist / supplement | outside main text unless target counts it | Carry extended metrics, threshold analyses, and source-data statements. |

## Flexible Adjustment Notes

- If the manuscript develops a risk score or model rather than evaluating a test at fixed threshold,
  consider `prediction-model.md`.
- Avoid clinical-decision claims unless the evidence includes consequences, calibration, or decision
  analysis.
