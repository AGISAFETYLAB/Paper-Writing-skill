# Journal Position / Perspective / Governance Paper Type

Use this profile for journal papers whose main contribution is an argued position, perspective,
forward-looking agenda, or trustworthy-AI / ethics / governance synthesis built around a
human-centered or stakeholder framework. Representative shape: TPAMI human-centered perspectives
(e.g., a survey of user studies for model explanations that frames stakeholder needs, defines
evaluation dimensions such as trust/understanding/usability/collaboration, synthesizes evidence, and
derives design and governance implications).

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Length: Defer To The Venue Card

This is a journal paper. Take absolute length from the venue card and plan sections as proportions
first. The evidence-synthesis and implications sections carry the contribution. Also load
`_shared/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Framework / Evaluation Dimensions.
- Evidence core: Evidence Synthesis and Design / Governance Implications.
- Compress first: Conclusion, broad Background / Related Work, repeated motivation, and secondary examples.
- Core floor: protect the framework, evidence synthesis, and implications chain; if the venue is
  short, narrow the position or evidence scope before shrinking those sections below their
  proportional floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State the stakeholder need, the framework/dimensions, the evidence synthesized, and the implications. |
| 1 | Introduction | ~12-18% | Establish the stakeholder need and the gap between technical metrics and human/organizational outcomes; state the position and contributions. |
| 2 | Background / Related Work | ~8-14% | Position against prior perspectives and adjacent technical work; clarify the framing this paper advances. |
| 3 | Framework / Evaluation Dimensions | ~18-26% | Define the organizing framework: the dimensions, categories, or objectives (e.g., trust, understanding, usability, collaboration) used to structure the analysis. |
| 4 | Evidence Synthesis | ~22-30% | Synthesize the evidence along the framework (study designs, measures, findings); analyze what is and is not supported, including inconsistencies. |
| 5 | Design / Governance Implications | ~12-18% | Derive concrete, actionable implications: best practices, design guidelines, or governance/policy recommendations grounded in the evidence. |
| 6 | Future Directions | ~6-10% | Lay out the forward agenda and open problems. |
| 7 | Conclusion | ~3-5% | Restate the position, the framework, and the implications. |
| Back | Appendix | outside main budget | Full evidence tables, coding schemes, and extended analyses. |

## Flexible Adjustment Notes

- Anchor on stakeholder needs and outcomes, not on whether a technique looks impressive; the move is
  from "is the artifact good?" to "do the intended humans/organizations benefit?".
- Keep technical metrics, human evidence, and design/governance recommendations in one coherent
  framework; that integration is the contribution.
- Recommendations must be traceable to the synthesized evidence, not asserted.
- If the paper is primarily a neutral literature taxonomy rather than an argued position, use
  `journal/survey-paper.md`.
