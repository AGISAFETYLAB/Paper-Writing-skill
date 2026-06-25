# Generic Research Paper Type

Use this profile when the paper type is unknown, mixed, early-stage, or not well captured by the
other profiles. It follows a common research-paper structure while remaining neutral about
contribution type.

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Section And Page-Budget Reference

When no venue-specific budget is known, use the workflow's soft 6-8 main-text-page drafting budget
and treat 8 pages as an upper bound, not a venue limit.

## Priority Contract

- Primary core: Method / Approach / Design, or the section that carries the central contribution.
- Evidence core: Experiments / Evaluation / Analysis.
- Compress first: Conclusion, broad Related Work, optional Discussion, and secondary details that can
  move to appendix.
- Core floor: for an 8-page generic draft, keep the primary core at about 1.5-2.5 pages and avoid
  dropping below 1.25 pages unless the user explicitly approves the tradeoff.

| Order | Candidate section | Typical budget | Section role |
|---|---:|---:|---|
| Front | Abstract | 0.15-0.25 page | State task/problem, gap, contribution, main evidence, and scoped takeaway. |
| 1 | Introduction | 1.0-1.5 pages | Move from problem and motivation to gap, core idea, contribution summary, and evidence preview. |
| 2 | Related Work | 0.75-1.25 pages | Group relevant work by topic and clarify how the paper differs from the closest lines. |
| 3 | Method / Approach / Design | 1.5-2.5 pages | Explain the proposed approach, modules, workflow, design choices, or analytical setup. |
| 4 | Experiments / Evaluation / Analysis | 2.0-3.0 pages | Present setup, main evidence, comparisons, ablations or controls, qualitative examples, and limitations of evidence. |
| 5 | Discussion | 0.5-1.0 page | Interpret findings, tradeoffs, implications, and boundary conditions when not already covered elsewhere. |
| 6 | Conclusion | 0.25-0.5 page | Summarize the contribution and supported takeaway without adding new evidence. |
| End | Limitations | venue-dependent | State scope limits, assumptions, evidence gaps, risks, or deployment constraints. |
| Back | Appendix | outside main budget when allowed | Put extra details, prompts, proofs, extended tables, implementation notes, and additional examples here. |

## Flexible Adjustment Notes

- If the contribution is clearly a method, system, benchmark/dataset, or survey, prefer the specific profile.
- If the paper is short, combine Discussion with Experiments or Conclusion.
- If the venue has strict page limits, prioritize Introduction, the core contribution section, and the evidence section.
