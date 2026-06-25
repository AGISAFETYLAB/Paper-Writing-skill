# Conclusion Principles And Template

## Section Role

The Conclusion closes the argument. It should restate the contribution, evidence, and limitations
without expanding the claim beyond the paper.

## Template

1. Restate the problem and contribution in one sentence.
2. Summarize the strongest evidence.
3. State the scoped implication.
4. Acknowledge key limitations or future work when needed.

## Limitation Policy

A limitation should usually come from task goal or task setting, similar to future work. Do not
voluntarily frame the paper around a technical defect unless the defect is already central to the
honest evaluation.

Decision rule:

- If a weakness does not damage existing important metrics relative to current SOTA or the paper's
  promised evaluation target, it can often be written as task/setting scope or future work.
- If a weakness damages an important metric, breaks a key claim, or creates negative net value, it
  is a technical defect and must be addressed in Experiments, Reviewer Risk, or claim weakening.
- A limitation statement should be precise enough to avoid overclaiming but not so broad that it
  supplies an avoidable rejection argument.

## Limitations Section Length And Shape

A standalone `Limitations` section (ACL-style) must be **short and scannable, not exhaustive**.
A long, padded Limitations section reads as either anxiety or as handing reviewers a list of
attack surfaces — neither helps.

- **Cap at the 3–4 most material limitations.** Pick the ones a competent reviewer would
  actually raise; do not enumerate every conceivable caveat. Five or more numbered points is a
  signal to merge or cut.
- **1–2 sentences each.** State the limitation, then at most one clause of scope or mitigation.
  Do **not** append a "future work should…" sentence to every point — that doubles the length
  for no information.
- **No boilerplate frame.** Drop the throat-clearing opener ("We acknowledge several
  limitations of this work…") and the promotional closer ("Despite these limitations, we
  believe our work provides…"). Lead directly with the first limitation and stop after the last.
- **Lead with the limitation itself** (a short bold lead-in or topic phrase), not with a wind-up.
- **Target ≈ 120-180 words total** — well under half a column. If it is longer, it is a
  **blocking** writing defect for a first manuscript: compress before returning.

## Principles

- Close the story opened by the Introduction.
- Keep claims within demonstrated evidence.
- Mention limitations with precision, not apology.
- do not inflate the paper into solving a broader field problem.

## Must Avoid

- New claims, new citations, or new experimental interpretations.
- Unsupported future impact language.
- Repeating the Abstract mechanically.
- Presenting a serious technical defect as harmless future work.

## Template Selection

Select one conclusion mode:

1. Standard close: contribution -> evidence -> scoped implication.
2. Limitation-aware close: contribution -> evidence -> task/setting limitation -> future work.
3. Benchmark/resource close: artifact -> coverage/evidence -> intended use -> boundary.

Choose the conclusion mode internally based on the Writing Policy and evidence boundary. Do not
expose template-selection notes unless the user asks for reasoning.

## Self-Check

- Does the conclusion reinforce the Writing Policy's final takeaway?
- Are all claims already supported earlier?
- Does the limitation come from task goal or task setting rather than hidden method failure?
- Would a reviewer see honest scope control?
