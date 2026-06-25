# Related Work Principles And Template

## Section Role

Related Work should position the technical challenge and the paper's difference. It is not a
citation list.

## Template

List directly competing and recent baseline papers first, before broader topic grouping. These
papers anchor the section and prevent the strongest baselines from being hidden in background.

Use 2-4 focused topics by default. Merge thin topics, and move broad background that does not help
position the technical challenge out of the main Related Work section.

For each related-work group:

1. Name the research line.
2. State what this line contributes to the problem space.
3. Explain the remaining limitation or mismatch.
4. Clarify how the current paper differs.
5. Avoid overstating the gap.

## Citation Use

Use this compact paragraph shape:

`research line -> representative methods -> limitation or scope boundary -> paper distinction`

- Cite primary sources when they support a specific claim about a method, result, dataset, or
  limitation.
- Review papers may support background framing, not primary evidence claims.
- Do not use a citation group unless the sentence states what the group has in common.

## Citation Scope And Density

Set citation density by paper type, venue/page pressure, and section role; do not use a fixed
global reference count.

- Short conference papers: cite closest baselines, representative method families, standard
  benchmarks/datasets, and metric definitions needed for the argument.
- Journal or extended papers: allow broader coverage, but keep each paragraph organized by claim
  role instead of citation volume.
- Benchmark/dataset papers: cover prior benchmarks, datasets, task protocols, annotation or
  evaluation conventions, and metric definitions before general background.
- Survey papers: require a declared search scope or corpus logic before applying ordinary
  related-work density rules.

## Template Selection

Choose one organization:

1. Closest-baseline first: use when reviewers expect direct comparison to specific recent papers.
2. Technical-topic grouping: use when several method families explain the target challenge.
3. Task-then-technique grouping: use when the paper introduces a new setting but uses known
   techniques.

Choose the organization internally based on how the paper needs to position its technical
challenge. Do not expose template-selection notes unless the user asks for reasoning.

## Principles

- Organize by contrastive roles, not by chronology.
- Use citations to support positioning, not to decorate paragraphs.
- Separate "not addressed" from "addressed differently".
- Position the technical challenge in relation to prior work.
- If a claim depends on source content, mark citation status until verified.

## Must Avoid

- "A did X; B did Y; C did Z" paragraphs with no argument.
- Dismissing prior work without evidence.
- Claiming novelty before checking citation support.
- Do not hide strongest baselines.
- Do not make Related Work a citation dump.
- Do emphasize the exact gap your method fills.

## Self-Check

- Does each paragraph explain a difference that matters for the story?
- Are citations verified or marked not verified?
- Does this section make the contribution look necessary rather than isolated?
- Are all strongest/recent competitors covered?
- Is each topic connected to your problem setting?
- Is your difference explained in technical terms, not marketing terms?
- Is citation coverage complete for all core claims?
