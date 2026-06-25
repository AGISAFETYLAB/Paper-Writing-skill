# Journal Application / Large-Scale Deployment Paper Type

Use this profile for journal papers whose main contribution is applying and scaling technology to a
real-world coverage gap, with resource construction, model scaling, and practical-impact evaluation.
Representative shape: JMLR large-scale applied projects (e.g., extending speech technology to 1,000+
languages: motivate the coverage gap, build the data/resource, scale the models, then evaluate
real-world impact against strong baselines and release artifacts).

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Length: Defer To The Venue Card

This is a journal paper, usually long because it spans data + models + evaluation. Take absolute
length from the venue card and plan sections as proportions first. Move full per-language / per-domain
tables and pipeline details to supplemental material. Also load
`_shared/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Data / Resource Construction and Models / Scaling.
- Evidence core: Practical-Impact Evaluation.
- Compress first: Conclusion, broad Related Work, exhaustive per-language/per-domain tables, and
  secondary pipeline detail.
- Core floor: protect the construction-scaling-evaluation chain as the majority of main prose; if
  the venue is short, narrow the scale or move tables to supplement before shrinking those core
  sections below their proportional floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State the real-world coverage gap, the resource and models built, the scale, and the impact result. |
| 1 | Introduction | ~10-16% | Motivate the real-world need (who is unserved by current technology), the approach, and contributions/releases. |
| 2 | Related Work | ~6-10% | Position against prior systems by coverage, data source, and real-world reach. |
| 3 | Data / Resource Construction | ~20-28% | Document the data source, the construction/alignment/curation pipeline (step by step), coverage, and quality filtering. |
| 4 | Models / Scaling | ~18-26% | Describe the models built and how they scale across the target population (e.g., multiple tasks or domains), with training details. |
| 5 | Practical-Impact Evaluation | ~18-26% | Evaluate against strong baselines on real benchmarks, report coverage/reach, and analyze errors across the population (e.g., by region/domain/subgroup). |
| 6 | Responsible Use / Broader Impact | ~4-8% | Discuss access, fairness across the served population, risks, and intended deployment. |
| 7 | Conclusion + Resource Release | ~3-5% | Restate the reach achieved and specify released models, data, and tooling. |
| Back | Appendix / Supplement | outside main budget | Full coverage tables, pipeline details, per-subgroup results, and release metadata. |

## Flexible Adjustment Notes

- Lead from the real-world coverage gap, not from a model trick; the value is serving an underserved
  population or use case at scale.
- Close the loop: data source -> construction -> model scaling -> impact evaluation -> release.
  Reviewers distrust applied papers that only tune on a couple of clean datasets.
- Use strong baselines (not weak ones) and error analysis across the population; report where it
  underperforms.
- Make coverage/reach concrete (counts, populations, domains) and releases explicit.
- If the contribution is the data resource itself rather than its applied deployment, use
  `dataset-benchmark-paper.md`.
