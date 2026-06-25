# Abstract Principles And Templates

## Goal

Write a strong abstract by doing three things repeatedly:

1. Think through the abstract logic first.
2. Follow one template (Version 1/2/3 below).
3. Revise the abstract many times.

## Pre-Writing Questions (Important)

Answer these before writing:

1. What technical problem does the paper solve, and why is there no well-established solution?
2. What is the technical contribution?
3. Why does the contribution work in essence?
4. What technical advantage or new insight should reviewers remember?

## Opening Funnel

Before the contribution appears, the opening must establish two distinct roles:

1. **task/context**: the setting, task, capability, phenomenon, or reader need that makes the paper
   relevant;
2. **gap/challenge**: the unresolved limitation, missing measurement, resource gap, technical
   obstacle, uncertainty, or decision problem that makes the contribution necessary.

Do not enforce a fixed sentence count. The two roles may fit in one strong sentence, two short
sentences, or a broader funnel when the venue and abstract cap allow it. What matters is that a
reviewer can identify both roles before the contribution arrives. If the contribution sentence feels
abrupt, the opening funnel is underdeveloped even if the required chain is technically present.

The paper type determines the kind of gap: method papers usually state a modeling or algorithmic
challenge; benchmark/dataset papers state a measurement, coverage, annotation, or resource gap;
empirical analysis papers state an unresolved phenomenon or comparison; clinical and social-science
papers state the population, intervention/exposure, or decision uncertainty; theory papers state the
formal question or missing guarantee. Use the active paper type to choose the gap, not to impose a
paper-type-specific sentence template.

## Version 1: Challenge -> Contribution

Use when the paper has one clear contribution. Introduce the technical challenge, then use one to
two sentences to present the technical contribution for solving the challenge.

Structure:

1. Task.
2. Technical challenge for previous methods.
3. One to two sentences introducing the technical contribution for solving the challenge.
4. Benefits or technical advantage of the contribution.
5. Experiment summary.

Matching example: `references/sections/examples/abstract/challenge-contribution.md`.

Expert notes:

1. Discuss previous work around the technical challenge that we actually solve.
2. Present each contribution as solving or enabling something, not as a flat list of components.
3. For the contribution sentence(s), mention the technical term/name only; do not explain every
   detailed step. The technical term must be easy to understand; readers should not feel a jump.
4. This ability is very important for writing a good abstract.

## Version 2: Challenge -> Insight -> Contribution

Use when the main contribution is best explained through an insight. Introduce the technical
challenge, then use one sentence to present the insight for solving the challenge, and then one to
two sentences to present the technical contribution that implements this insight.

Structure:

1. Task.
2. Technical challenge for previous methods.
3. One sentence introducing the insight for solving the challenge.
4. One to two sentences introducing the technical contribution that implements the insight.
5. Benefits of technical novelty.
6. Experiment summary.

Matching example: `references/sections/examples/abstract/challenge-insight-contribution.md`.

Expert notes:

1. Discuss previous work around the technical challenge that we actually solve.
2. Introduce the insight in one clear sentence.
3. Present each contribution as solving or enabling something, not as a flat list of components.
4. For the implementation sentence(s), mention the technical term/name only; do not explain every
   detailed step. The technical term must be easy to understand; do not create a reading jump.
5. This ability is very important for writing a good abstract.

## Version 3: Multiple Contributions

Use when the paper has several contributions that each need a compact contribution-plus-advantage
statement.

Structure:

1. Task.
2. If needed, one contrast sentence about prior methods.
3. Contribution 1 + technical advantage.
4. Contribution 2 + technical advantage.
5. Contribution 3 + technical advantage (optional).
6. Experiment summary.

Matching example: `references/sections/examples/abstract/multiple-contributions.md`.

Expert notes:

1. When there are multiple technical contributions, describe each together with its technical
   advantage. The ability to express "contribution + advantage" in one sentence is very important.
2. Present each contribution as solving or enabling something, not as a flat list of components.

## Template Selection

Before writing, select exactly one of Version 1, Version 2, or Version 3 internally. If the paper
has one central insight, prefer Version 2. If the paper has several independent contributions, use
Version 3. Do not expose template-selection notes unless the user asks for reasoning.

## Evidence Budget

The evidence sentence proves that the contribution is grounded; it is not a miniature Results
section.

- Use at most one high-level evidence sentence in the abstract.
- Prefer a qualitative or bounded comparative summary unless a single headline number is essential.
- Do not include model-specific deltas, intervention before/after chains, or multiple percentage values.
- Do not list evaluated models, full metric ranges, ablations, or table-level details.
- If several numbers feel necessary, move them to Experiments and keep the abstract at the
  problem -> challenge/gap -> insight/contribution -> advantage -> evidence level.

## Example Bank

After selecting a section template, open only the matching example file if a concrete writing
pattern is needed. Reuse sentence logic and structure, not exact wording, task names, claims,
metrics, or citation framing.

1. `references/sections/examples/abstract-examples.md` (index)

## Quality Checklist

1. Can a reader identify task, challenge, insight/contribution, and results in one pass?
2. Are all major claims supported by experiments?
3. Are technical names self-contained and readable?
4. Does each contribution sentence explain what it solves or enables?
5. Is there any sentence that mixes too many messages?
6. Does every claim map to the Writing Policy?
7. Would a skeptical reviewer know what is new, why it matters, and what evidence supports it?
8. Is the evidence sentence within the Evidence Budget, with no model-specific deltas or multiple
   percentage values?
