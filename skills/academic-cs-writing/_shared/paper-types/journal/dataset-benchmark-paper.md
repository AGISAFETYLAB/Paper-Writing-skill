# Journal Dataset / Benchmark Paper Type

Use this profile for journal papers whose main contribution is a dataset and an associated task /
benchmark: a new task definition, a curated and annotated dataset, defined splits and metrics, and a
baseline leaderboard. Representative shape: TPAMI dataset papers (e.g., a motion-expression video
segmentation dataset that defines a new task, documents annotation and statistics, sets splits and
metrics, and benchmarks many existing methods plus a baseline).

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Length: Defer To The Venue Card

This is a journal paper. Take absolute length from the venue card and plan sections as proportions
first. Move full datasheets, annotation guides, and per-method tables to supplemental material. Also
load `_shared/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Dataset Construction.
- Evidence core: Benchmark Experiments.
- Compress first: Conclusion, broad Related Work, full datasheets, annotation guides, and
  per-method tables.
- Core floor: protect construction, annotation, quality control, statistics, task/split/metric
  definition, and benchmark evidence; if the venue is short, move documentation to supplement before
  shrinking Dataset Construction below its proportional floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State the task, why existing datasets are insufficient, the dataset scale, and the benchmark finding. |
| 1 | Introduction | ~12-18% | Define the new task and why it matters, the limitation of prior datasets, the design goals, and contributions. |
| 2 | Related Work | ~8-12% | Compare prior datasets/benchmarks by task framing, coverage, annotation, and metrics. |
| 3 | Dataset Construction | ~25-33% | Data sources and collection, the annotation process and tooling, quality control, and dataset statistics/analysis. |
| 4 | Tasks, Splits, and Metrics | ~8-12% | Define the task settings, train/val/test splits (and any online evaluation), and the evaluation metrics. |
| 5 | Benchmark Experiments | ~20-28% | Benchmark existing methods and a proposed baseline; report the leaderboard and, crucially, failure cases that the dataset exposes. |
| 6 | Conclusion | ~3-5% | Restate the resource and task enabled and what the benchmark shows. |
| End | Limitations | venue-dependent | Coverage/annotation limits, bias and licensing, intended non-uses, ethical constraints. |
| Back | Appendix / Supplement | outside main budget | Datasheet, annotation guidelines, extra statistics, per-method tables, and examples. |

## Flexible Adjustment Notes

- Define a task, not just a file release: show why the target cannot be solved by prior framings
  (e.g., requires cross-frame/temporal reasoning, not single-frame static cues).
- Protect annotation, quality-control, and statistics space; reviewers probe data quality first.
- Use baseline failure cases and a leaderboard to argue the benchmark will drive follow-up work.
- Provide an evaluation entry point (splits, metrics, and ideally an online server) so results are
  comparable.
- If the contribution is measuring existing models rather than releasing data, use
  `evaluation-benchmark-paper.md` instead.
