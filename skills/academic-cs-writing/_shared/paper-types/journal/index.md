# Journal Paper Type Index

Use this index when the confirmed `Venue Kind` is `journal` (see `_shared/venues/index.md`).
Journal paper types are kept separate from conference paper types because journal articles use
different section conventions, are usually longer and more complete, and are written to survive a
multi-round review. The conference paper-type files at the top level of `_shared/paper-types/`
are NOT used for journal submissions.

First decide the journal paper type, then load the matching profile before building the Paper
Framework. The user may select the type. If not selected, infer it from the main contribution,
evidence package, target journal, and requested output, then mark the inference in the Writing
Policy. Use `journal/generic-paper.md` only when the type is unknown, mixed, early-stage, or not
safely captured by a specific profile.

Journal paper-type profiles set section structure and a PROPORTIONAL budget. Absolute length comes
from the venue card (e.g., JMLR has no hard page limit; TPAMI uses double-column manuscript-type
limits). Also load `_shared/venues/journal-vs-conference.md` for the journal drafting posture.

## Framework Main Content Contract

During Paper Framework, the `Main Content` cell is a **one-sentence phrase** that carries the
section's **argument movement**. Use the selected profile's `Section role` cell as the source, then
compress it into a short planning cue, **not a component checklist**.

- **Abstract**: preserve `problem/challenge -> gap -> contribution/insight -> advantage -> evidence`.
  Name only the central object and strongest evidence; avoid inventories like "task count, protocol,
  result range". Evidence is a one-sentence budget: no model list, no model-specific deltas, and no
  multiple percentage values.
- **Introduction**: preserve `problem/gap -> contribution -> evidence preview`. State why the paper
  exists and what the evidence will support. Do not turn the preview into a model-list or result-recap
  paragraph.
- **Body sections**: name the section job plus the evidence or display anchor, e.g., "dataset
  construction and benchmark evidence", not paragraphs or subsection lists.

Keep Framework content brief. Detailed paragraph flow belongs to section drafting and the section
guides, not to the Paper Framework artifact.

## Journal Type Selection Map

| Journal Paper Type | Profile | Story center | Representative shape |
|---|---|---|---|
| Theory | `theory-paper.md` | A provable result: formalization, theorem/proof, convergence/generalization analysis. | JMLR theory article |
| Method / Scaling | `method-scaling-paper.md` | A method/recipe established by a large, systematic experimental matrix across variables and scales. | JMLR scaling study |
| Systems / Tools / Library | `systems-tools-paper.md` | A usable software system, library, or toolkit. | JMLR OSS/MLOSS paper |
| Evaluation / Benchmark | `evaluation-benchmark-paper.md` | An evaluation that measures a missed capability across a model suite, with failure analysis. | TPAMI evaluation benchmark |
| Dataset / Benchmark | `dataset-benchmark-paper.md` | A new task plus a curated, annotated dataset, splits, metrics, and a baseline leaderboard. | TPAMI dataset paper |
| Application / Deployment | `application-paper.md` | Applying and scaling technology to a real-world coverage gap, with resource construction and impact evaluation. | JMLR large-scale applied project |
| Survey | `survey-paper.md` | A taxonomy and synthesis of a field with trends and open questions (long journal survey). | TPAMI survey |
| Position / Governance | `position-governance-paper.md` | An argued position / perspective / trustworthy-AI framework with design or governance implications. | TPAMI human-centered perspective |
| Generic journal | `generic-paper.md` | Unknown, mixed, or early-stage journal contribution. | journal fallback |

## Common Mappings

| If the manuscript looks like... | Prefer this profile | Adjustment note |
|---|---|---|
| Theorems, proofs, convergence/generalization analysis, formal model | `theory-paper.md` | Statements + intuition in main text; full proofs in appendix; discuss practical utility (JMLR). |
| Recipe studied over task count / model size / data axes with a large result matrix | `method-scaling-paper.md` | Protect the experimental matrix and ablations; specify released resources. |
| Python/library/toolkit with APIs, modules, and reproducible examples | `systems-tools-paper.md` | OSS track is short; lead with pain point + design philosophy + coverage table. |
| Benchmark that scores many models on a missed capability | `evaluation-benchmark-paper.md` | Center on protocol + failure analysis, not the leaderboard. |
| New task + curated/annotated dataset + splits + leaderboard | `dataset-benchmark-paper.md` | Protect annotation/quality/statistics; use baseline failure cases. |
| Scaling a technology to an underserved real-world population/use case | `application-paper.md` | Close the loop data -> models -> impact -> release; strong baselines + error analysis. |
| Field-level taxonomy and synthesis with trends/open questions | `survey-paper.md` | Long; protect taxonomy and trends; compare families on shared dimensions. |
| Argued position, perspective, trustworthy-AI / ethics / governance framework | `position-governance-paper.md` | Integrate technical metrics, human evidence, and recommendations in one framework. |
| Position/theory note, mixed, or unclear journal contribution | `generic-paper.md` | Rename sections as needed; keep length governed by the venue card. |
