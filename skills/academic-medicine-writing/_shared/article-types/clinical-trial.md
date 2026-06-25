# Clinical Trial Profile

Use this profile for randomized or nonrandomized clinical intervention result manuscripts. Use
SPIRIT/protocol structure only when the manuscript is a trial protocol rather than results.

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Preserve trial design, intervention,
outcome, and harms reporting before compressing interpretation.

## Checklist / Study-Type Pairing

Pair trial result manuscripts with CONSORT and trial protocols with SPIRIT. Use extensions when the
source evidence requires them.

## Priority Contract

- Primary core: Methods.
- Evidence core: Results, especially participant flow, primary outcome, and harms.
- Compress first: broad background, secondary subgroup detail, implementation detail not needed for
  reproducibility, and exploratory analyses.
- Core floor: randomization/allocation, blinding, intervention, outcomes, sample size/statistical
  methods, participant flow, and harms cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / structured abstract / trial registration | outside main budget unless target counts it | Identify the trial design, intervention, primary outcome, result, and registration. |
| 1 | Introduction | 8-12% | State clinical need, prior evidence, and trial objective. |
| 2 | Methods | 34-42% | Describe design, setting, participants, randomization, allocation concealment, blinding, intervention, outcomes, sample size, protocol deviations, missing data, and statistical analysis. |
| 3 | Results | 32-40% | Present participant flow, recruitment, baseline data, primary and secondary outcomes, uncertainty, adherence, protocol deviations, and harms. |
| 4 | Discussion | 14-20% | Interpret benefit/risk, compare with prior evidence, discuss limitations, generalizability, and clinical implications. |
| 5 | Conclusions | 1-3% | State the trial-supported conclusion only. |
| Back | Declarations / CONSORT checklist / protocol-SAP / supplement | outside main text unless target counts it | Carry registration, ethics, funding, conflicts, CONSORT flow, and protocol/SAP materials. |

## Flexible Adjustment Notes

- CONSORT flow is usually a main display unless the target journal has a strict display cap.
- If harms or adverse events are collected, plan a harms display even when the main effect is null.
- Do not write treatment-effect language unless randomization, estimand, and outcome windows support
  it.
