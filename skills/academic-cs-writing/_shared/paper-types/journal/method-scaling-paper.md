# Journal Method / Scaling Paper Type

Use this profile for journal papers whose main contribution is a method, training paradigm, or
recipe whose value is established by decomposing it into controllable variables and proving its
behavior with a large, systematic experimental matrix across scales and benchmarks. Representative
shape: JMLR scaling studies (e.g., instruction finetuning analyzed over task count, model size, and
chain-of-thought data, with multi-benchmark generalization and an open model release).

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Length: Defer To The Venue Card

This is a journal paper. Do NOT use a conference soft page budget. Take absolute length from the
venue card and plan sections as proportions first. The defining feature of this type is a LARGE
experimental matrix; protect enough room for it and push secondary tables to supplement/appendix.
Also load `_shared/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Method / Variable Decomposition.
- Evidence core: Scaling Experiments and Ablations / Analysis.
- Compress first: Conclusion, broad Related Work, secondary matrices, and extended release details.
- Core floor: protect method decomposition plus the systematic experimental matrix; if the venue is
  short, move secondary tables to supplement before shrinking Method below its proportional floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State the method, the variables studied, the headline scaling finding, and the released resource. |
| 1 | Introduction | ~12-16% | Motivate the question ("does X help, and along which axes?"), summarize the scaling findings, list contributions and releases. |
| 2 | Method / Variable Decomposition | ~15-22% | Define the method and decompose it into the controllable variables (e.g., data/task count, model size, data format, an added ingredient), plus the training and evaluation protocol. |
| 3 | Scaling Experiments | ~25-35% | The experimental matrix: vary each axis, report held-out performance, and isolate each variable's effect. This is the core evidence. |
| 4 | Component Ablations | ~10-15% | Ablate the key ingredient(s) to show necessity and interaction effects, not just aggregate gains. |
| 5 | Cross-Benchmark Generalization | ~10-15% | Show the finding transfers across benchmarks, model families, and prompting setups; report where it does not. |
| 6 | Discussion / Takeaways | ~6-10% | Summarize the scaling rules learned, practical guidance, and limits. |
| 7 | Resource Release | ~2-4% | Specify released checkpoints, data, and code, and how to use them. |
| Back | Appendix / Supplement | outside main budget | Full result tables, per-task breakdowns, hyperparameters, and additional axes. |

## Flexible Adjustment Notes

- Frame the contribution as controlled variables with a designed matrix, not a single training
  trick; reviewers reward the regularity, not the anecdote.
- Every performance claim names dataset, metric, model scale, and setup; bare aggregate numbers do
  not survive review.
- Keep main-text tables to the load-bearing comparisons; move exhaustive grids to the supplement.
- If the contribution is a single algorithm with a mechanism rather than a scaling study, consider a
  method paper structure (theory or conference method-paper) instead.
- State the released resources concretely; reusable artifacts are part of this type's value.
