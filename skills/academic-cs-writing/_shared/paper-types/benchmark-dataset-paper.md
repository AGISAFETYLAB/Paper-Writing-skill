# Benchmark / Dataset Paper Type

Use this profile for papers whose main contribution is a benchmark, dataset, evaluation suite,
annotation protocol, data construction pipeline, or measurement framework.

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Section And Page-Budget Reference

When no venue-specific budget is known, use the workflow's soft 6-8 main-text-page drafting budget
and treat 8 pages as an upper bound, not a venue limit.

## Priority Contract

- Primary core: Benchmark / Dataset Construction.
- Evidence core: Experiments and Empirical Findings.
- Compress first: Conclusion, broad Related Work, extended examples, and full documentation that
  can move to appendix.
- Core floor: for an 8-page generic/conference draft, keep Construction at about 1.75-2.75 pages
  and never below 1.5 pages unless the user explicitly approves; protect enough evidence-core space
  for protocol, baselines, main findings, and failure cases.

| Order | Candidate section | Typical budget | Section role |
|---|---:|---:|---|
| Front | Abstract | 0.15-0.25 page | Move from the measurement/resource gap to the benchmark or dataset contribution, protocol advantage, and one bounded evidence sentence; do not list model-specific results or multiple percentages. |
| 1 | Introduction | 1.0-1.5 pages | Define the target task or capability, why existing benchmarks/resources miss it, the root evaluation gap, the benchmark proposal, contribution bullets, and one high-level evidence preview. |
| 2 | Related Work | 0.75-1.25 pages | Compare prior datasets, benchmarks, protocols, and metrics by coverage, construct, annotation, and evaluation assumptions. |
| 3 | Benchmark / Dataset Construction | 1.75-2.75 pages | Explain data sources, preprocessing, synthesis or transformation pipeline, annotation/scoring rules, quality control, and validation. |
| 4 | Experiments and Empirical Findings | 2.0-3.0 pages | Define evaluation protocol, metrics, baselines, prompting/training access, overall performance, fine-grained analysis, and case studies. |
| 5 | Conclusion | 0.25-0.5 page | Summarize enabled measurement or resource value and key findings. |
| End | Limitations | venue-dependent | State dataset coverage limits, annotation limits, metric limits, intended non-uses, and ethical or access constraints. |
| Back | Appendix | outside main budget when allowed | Put full data documentation, annotation guide, extra results, prompt details, examples, and release metadata here. |

## Section Naming And Adaptation Notes

The candidate section names above are defaults. Adapt to the actual paper:

| Default name | When to keep | When to adapt |
|---|---|---|
| Benchmark / Dataset Construction | The paper's core contribution is the construction pipeline | If the paper splits construction into design + protocol, consider "Benchmark Design" and "Evaluation Protocol" |
| Experiments and Empirical Findings | Standard for benchmark evaluation | If experiments are structured around research questions, "Results and Analysis" or "Empirical Evaluation" is fine |
| Conclusion | Standard | If limitations need more space, merge into "Conclusion and Limitations" |

If the contribution or experiments genuinely need a structure that doesn't map cleanly to the default sections, adapt and note the reason at the Paper Framework checkpoint. The goal is that section names reflect what the paper actually does, not that they match a template exactly.

## Flexible Adjustment Notes

- The content elements listed for each section (e.g., data sources, preprocessing, annotation rules,
  quality control, validation, coverage comparison) are **content blocks, not a mandatory numbered
  subsection list**. Keep Construction and Experiments to roughly 2–4 subsections each; do not turn
  every element into its own `3.1 … 3.6` / `4.1 … 4.6` heading. Group related elements into one
  subsection or flowing prose, and move fine-grained detail to the appendix.
- If construction quality is the main contribution, allocate more space to pipeline, annotation, and validation.
- If empirical findings are the main contribution, allocate more space to research-question-driven analysis and case studies.
- If the venue requires dataset documentation, datasheets, or checklists, include them in the Page Budget Summary or appendix plan.
