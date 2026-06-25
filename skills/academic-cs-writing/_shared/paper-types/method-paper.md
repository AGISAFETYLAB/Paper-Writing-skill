# Algorithmic / Methodological Innovation Paper Type

Use this profile for papers whose main contribution is a new algorithm, model architecture,
training paradigm, objective, inference procedure, or methodological design.

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Section And Page-Budget Reference

When no venue-specific budget is known, use the workflow's soft 6-8 main-text-page drafting budget
and treat 8 pages as an upper bound, not a venue limit.

## Priority Contract

- Primary core: Method.
- Evidence core: Results and Analysis.
- Compress first: Conclusion, broad Related Work, secondary analysis, and implementation detail
  that can move to appendix.
- Core floor: for an 8-page generic/conference draft, keep Method at 2.0-3.0 pages and never below
  1.5 pages or roughly 25% of the main prose budget unless the user explicitly approves; for a
  4-page short paper, Method may shrink to about 0.8-1.0 pages with the omitted detail named in the
  framework.

| Order | Candidate section | Typical budget | Section role |
|---|---:|---:|---|
| Front | Abstract | 0.15-0.25 page | Summarize background, gap, method idea, main result, and scoped conclusion. |
| 1 | Introduction | 1.0-1.5 pages | Establish the problem, prior limitation, research question, core method insight, and contributions. |
| 2 | Related Work | 0.75-1.25 pages | Group related algorithms or methods by technical line and clarify the gap this method targets. |
| 3 | Method | 2.0-3.0 pages | Explain algorithm structure, architecture, training/inference flow, equations, pseudocode, and module rationale. |
| 4 | Experimental Setup | 0.5-0.75 page | State datasets, baselines, metrics, implementation settings, and hyperparameters needed for reproducibility. |
| 5 | Results and Analysis | 1.5-2.5 pages | Present main results, ablations, robustness checks, efficiency, qualitative analysis, and failure cases. |
| 6 | Conclusion | 0.25-0.5 page | Summarize the method contribution, strongest evidence, and future direction. |
| End | Limitations | venue-dependent | Discuss failure cases, compute/resource cost, assumptions, and settings where the method may not transfer. |
| Back | Appendix | outside main budget when allowed | Put long proofs, extra derivations, extra tables, implementation details, and extended qualitative examples here. |

## Flexible Adjustment Notes

- If the method is mathematically heavy, reserve more Method or Appendix space for derivations and reduce Related Work.
- If the core claim depends on empirical gains, protect enough Results and Analysis space for ablation and failure analysis.
- If the venue has a required limitations or ethics section, account for it in the venue-aware Page Budget Summary.
