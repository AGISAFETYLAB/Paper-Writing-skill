# Generic Medical Article Profile

Use this profile when the target article type is unknown, mixed, early-stage, or not safely captured
by a more specific medical article-type profile. This is the fallback profile, not a claim that the
paper is an Original Investigation.

## Source Anchors

- ICMJE manuscript preparation: https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html
- EQUATOR reporting-guideline index: https://www.equator-network.org/reporting-guidelines/

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. If no target article type is known, use
the Generic Medical Length Fallbacks in `_shared/submission/templates.md` and mark the route as
`generic-review`.

## Checklist / Study-Type Pairing

Select the study checklist independently from `study_type`. If no checklist applies, record
`checklist: unresolved / not applicable` rather than inventing one.

## Priority Contract

- Primary core: the section that carries the central evidence or argument after article type is
  clarified.
- Evidence core: Methods and Results for empirical work; Synthesis/Argument for non-empirical work.
- Compress first: broad background, speculative implications, and unsupported secondary material.
- Core floor: paper identity, question, evidence source, method/approach, result or argument, and
  limitation must be explicit.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / abstract if required | outside main budget unless target counts it | State article identity, question, evidence source, and cautious takeaway. |
| 1 | Introduction / Background | 10-16% | Establish the problem, gap, and objective or thesis. |
| 2 | Methods / Approach | 28-38% | Describe design, data/materials, protocol, analytical approach, synthesis approach, or reasoning standard. |
| 3 | Results / Findings / Main Argument | 30-40% | Present the main evidence, findings, synthesis, or recommendations with uncertainty and boundaries. |
| 4 | Discussion / Implications | 16-24% | Interpret meaning, limitations, applicability, and next steps without overclaiming. |
| 5 | Conclusions | 1-3% | State only the supported conclusion. |
| Back | Declarations / references / supplement | outside main text unless target counts it | Carry statements, checklist, data/code, and extended material. |

## Flexible Adjustment Notes

- Prefer a specific profile as soon as article identity becomes clear.
- Do not let this profile hide a target-journal article-type requirement.
- Use generic only as a transparent fallback for unresolved, mixed, or locally reviewable drafts.
