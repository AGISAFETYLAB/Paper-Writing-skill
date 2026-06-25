# Study Protocol Profile

Use this profile for manuscripts that report a planned study protocol rather than completed results:
clinical trial protocols, observational protocols, systematic review protocols, qualitative
protocols, or mixed-methods protocols.

## Source Anchors

- SPIRIT 2025 / CONSORT-SPIRIT: https://www.consort-spirit.org/
- SPIRIT 2025 on EQUATOR: https://www.equator-network.org/reporting-guidelines/spirit-2013-statement-defining-standard-protocol-items-for-clinical-trials/
- PRISMA-P on EQUATOR: https://www.equator-network.org/reporting-guidelines/prisma-protocols/

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Protocol journals often set word limits
by article type; do not use result-paper budgets.

## Checklist / Study-Type Pairing

Use SPIRIT for randomized trial protocols, PRISMA-P for systematic review/meta-analysis protocols,
and the closest design checklist for observational, qualitative, mixed-methods, diagnostic, or
prediction protocols.

## Priority Contract

- Primary core: Methods / Protocol.
- Evidence core: feasibility, planned outcomes, analysis plan, and ethics/governance.
- Compress first: broad background, expected results, and speculative impact.
- Core floor: objectives, design, eligibility, interventions/exposures/tests, outcomes, sample size
  or information power, data collection, analysis plan, monitoring, ethics, registration, and
  dissemination cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / structured abstract / registration | outside main budget unless target counts it | Identify the planned study, design, population, setting, and registry/protocol status. |
| 1 | Introduction / Rationale | 10-14% | Explain why the study is needed and define objectives/hypotheses. |
| 2 | Methods: Design and Setting | 16-22% | Define design, timeline, setting, governance, eligibility, recruitment, and allocation if relevant. |
| 3 | Methods: Intervention / Exposure / Data Collection | 18-26% | Specify intervention/comparator, exposure/test/model, measures, instruments, procedures, and participant flow. |
| 4 | Outcomes and Analysis Plan | 22-30% | Define outcomes, sample size/information power, statistical or qualitative analysis plan, missing data, and sensitivity plans. |
| 5 | Ethics, Monitoring, Data Sharing, Dissemination | 10-16% | Cover consent, safety/monitoring, data/code availability, amendments, and dissemination. |
| 6 | Discussion / Strengths and Limitations | 8-12% | Explain feasibility, expected contribution, limitations, and implementation risks without reporting results. |
| Back | Protocol checklist / schedule / appendices | outside main text unless target counts it | Carry SPIRIT schedule, PRISMA-P details, instruments, SAP, and supplementary materials. |

## Flexible Adjustment Notes

- Do not fabricate results, recruitment numbers, effect estimates, or conclusions for a protocol.
- If completed results are available and the user wants a results paper, switch to the appropriate
  article-type profile.
