# Result Reliability Audit

Use this reference when a manuscript claim depends on whether reported medical or biomedical
results are trustworthy enough for the wording being used. This audit complements checklist review:
checklists test reporting completeness, while reliability tests whether the design, data, statistics,
validation chain, and interpretation can support the claim.

## Audit Dimensions

Contract phrases for validation and review handoff: design and bias; statistical and model risk;
validation chain; claim discipline.

| Dimension | Check | Common downgrade |
|---|---|---|
| Design and bias | Study design fits the question, groups are comparable, confounding and selection are addressed, temporal order is credible. | Causal or treatment-effect wording becomes association or exploratory wording. |
| Statistical and model risk | Sample size, events per variable, missing data, multiple testing, threshold selection, calibration, and resampling are reported and plausible. | Robust/validated language becomes fragile, internally checked, or hypothesis-generating. |
| Validation chain | Separate no validation, internal split/resampling, external cohort validation, orthogonal validation, replication, and prospective/implementation support. | Clinical utility or deployment readiness is blocked without external/prospective evidence. |
| Claim discipline | Wording does not upgrade association to causation, prediction to clinical utility, mechanism support to mechanism proof, or limited validation to generalizability. | Title, abstract, conclusion, and Discussion claims are narrowed. |

## Required Reliability Map

When reliability affects a review, Discussion, conclusion, or abstract, create a compact table:

| result_claim | evidence_chain | design_bias_risk | statistical_model_risk | validation_status | allowed_claim_strength | action |
|---|---|---|---|---|---|---|

Allowed `validation_status` values:

- `none`
- `internal_only`
- `external_cohort`
- `orthogonal_validation`
- `replicated`
- `prospective_or_implementation`
- `unclear`

Allowed `allowed_claim_strength` values:

- `descriptive observation`
- `association`
- `predictive performance`
- `mechanistic support`
- `causal suggestion`
- `causal evidence`
- `translational relevance`
- `implementation readiness`

Do not let the manuscript use a stronger evidence tier than the study design and validation chain
support.

## Blocking Patterns

Block or downgrade submission-ready wording when:

- a retrospective association is written as clinical benefit, treatment effect, or causal proof;
- a prediction model reports discrimination but omits calibration, external validation, or intended
  use boundary while claiming utility;
- a biomarker or omics signature is selected and tested on the same data without independent
  validation;
- mechanism language is based only on correlation or pathway enrichment;
- subgroup or sensitivity results are emphasized without prespecification or source evidence;
- safety or adverse-event claims are made without a harms data source.

## Review Output

For every blocker or major concern, state whether it is a scientific weakness vs reporting weakness:

- Scientific weakness: the needed evidence or validation does not exist in the source material.
- Reporting weakness: the evidence appears to exist but is not reported clearly enough.

Writing can fix reporting weakness. Writing cannot fix missing science; it can only weaken the
claim, mark the gap, or ask the author for source evidence.
