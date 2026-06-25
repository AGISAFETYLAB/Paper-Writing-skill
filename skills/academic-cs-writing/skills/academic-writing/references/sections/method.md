# Method Principles And Templates

## Goal

Write the Method section clearly by following this sequence:

1. Answer key method-design questions.
2. Draw a pipeline figure sketch.
3. Write the method section step by step.

## Pre-Writing Questions

Before writing Method, answer:

1. What modules, benchmark components, systems, algorithms, or analysis units exist?
2. What is the workflow of each module?
3. Why is each module needed?
4. Why does each module work?
5. Which claim and experiment does each module support?

## Method Writing Workflow

1. Draw a Pipeline Figure Sketch.
2. Use the sketch to decide Method subsections. Keep them minimal: group by real module/component,
   not by step. A Method section should usually have 0–4 subsections; prefer flowing prose or a
   `\paragraph{}` run-in over a numbered subsection for any block that is only one paragraph long.
   Do not emit one numbered subsection per pipeline step (no `3.1 … 3.6`).
3. For each subsection, plan four parts: motivation, module design, technical advantages, and
   evidence hook.
4. Write module design first to build the concrete backbone.
5. Add motivation, technical advantage, and evidence hook.

## Method Completeness Check

Every load-bearing module or design step must cover motivation, design, technical advantage, and
evidence hook. The evidence hook names which claim, experiment, metric, analysis, or figure will
later verify why the unit matters.

A method unit is underdeveloped if the reader cannot reconstruct the algorithm, architecture,
training/inference flow, protocol, or implementation-critical settings. Treat an underdeveloped unit
as a content defect and revise before returning. Length budgets and confirmed minimum lengths are set
in the Paper Framework and audited by review gates; this guide owns only method content completeness.

## Pipeline Figure Sketch

Before prose, sketch:

- input,
- major processing blocks,
- novel module or novel benchmark component,
- output,
- evidence or evaluation linkage.

The figure should help highlight novelty. If the full pipeline is not novel, highlight the novel
module or use focused subfigures.

## Module Triad

Every important subsection should contain the module triad:

1. **Motivation**: what problem or challenge requires this component?
2. **Design**: what is the concrete input-step-output process?
3. **Technical advantage**: why does this design help, and how can that advantage be verified?

Expert note:

1. The three elements are equally important. A module without clear motivation reads as an ad hoc
   patch. A module without technical advantage reads as unnecessary complexity.
2. Write the design first to establish a concrete backbone, then add motivation and advantage.
   This prevents the writing from becoming abstract hand-waving.

Matching example: `references/sections/examples/method/module-triad.md`.

## Overview Template

Use at the start of Method:

1. One or two sentences for task setting.
2. One or two sentences for core contribution.
3. Pipeline/framework figure pointer if useful.
4. A map of what each subsection covers.

Sentence skeleton:

1. `We aim to [task goal]. To this end, we propose [method name], which [core idea in one sentence].`
2. `An overview of [method name] is shown in Figure [x].`
3. `Section [x.1] describes ..., Section [x.2] presents ..., and Section [x.3] covers implementation details.`

Matching example: `references/sections/examples/method/overview-template.md`.

## Module Design Template

Describe representation/network/data-structure details and the forward process clearly.

Writing structure:

1. Define key structures first (representation, network, data structure).
2. Write forward process in strict execution order: given input → step 1 → step 2 → step 3 → output.
3. End with output interpretation or purpose.

Sentence skeleton:

1. `We represent [xxx] with [xxx].`
2. `Given [input], we first [step 1], then [step 2], and finally [step 3].`
3. `This produces [output], which is used for [purpose].`

Matching example: `references/sections/examples/method/module-design.md`.

## Module Motivation

Use problem-driven logic: because problem X exists, we design module Y.

Writing structure:

1. State a remaining problem or challenge.
2. Explain why previous/current practice has difficulty.
3. State why this module is needed.

Sentence skeleton:

1. `A remaining challenge is ...`
2. `Previous methods have difficulty in ... because ...`
3. `To address this, we introduce [module], which ...`

Expert note:

1. Motivation benefits from a concrete example or failure case. Abstract motivation ("to improve
   performance") is weak. Specific motivation ("to prevent the agent from hallucinating file paths
   when the app name is ambiguous") is strong.

Matching example: `references/sections/examples/method/module-motivation.md`.

## Technical Advantage Template

After design, explain what advantage the module creates and why it follows from the design.

Writing structure:

1. State what advantage the module creates.
2. Explain why the advantage follows from the design.
3. Tie to verifiable evidence: which metric, ablation, analysis, or qualitative result will verify it.

Sentence skeleton:

1. `This design provides two advantages. First, ... Second, ...`
2. `In contrast to [alternative], our module [advantage] because [reason rooted in design].`
3. `We verify this through [ablation/analysis] in Section [x].`

Matching example: `references/sections/examples/method/example-of-the-three-elements.md`.

## Example Bank

After selecting a section template, open only the matching example file if a concrete writing
pattern is needed. Reuse sentence logic and structure, not exact wording, task names, claims,
metrics, or citation framing.

1. `references/sections/examples/method-examples.md` (index)
2. `references/sections/examples/method/pre-writing-questions.md`
3. `references/sections/examples/method/module-triad.md`
4. `references/sections/examples/method/module-design.md`
5. `references/sections/examples/method/module-motivation.md`
6. `references/sections/examples/method/section-skeleton.md`
7. `references/sections/examples/method/overview-template.md`
8. `references/sections/examples/method/example-of-the-three-elements.md`
9. `references/sections/examples/method/method-writing-common-issues-note.md`

## Implementation Details

Put practical details near the end or in a dedicated implementation/protocol subsection:

- hyperparameters,
- model or system settings,
- feature dimensions,
- coordinate transforms or normalization,
- annotation protocol,
- task construction rules,
- evaluation scripts or environment constraints.

Use the implementation-detail checklist in this guide; the reference example bank does not include a
separate implementation-detail template.

## Method Clarity Check

Check at three levels:

1. **Logic**: summarize Method in a few bullets and test whether the flow is smooth.
2. **Paragraph**: each paragraph has one message and a clear opening sentence.
3. **Sentence**: each sentence has an explicit motivation; term names remain consistent. Check
   that the reader always knows **why this sentence content is needed**.

## Template Selection

Select the Method organization before writing:

1. Pipeline organization: input → modules → output.
2. Component organization: benchmark/data/protocol components or system components.
3. Module-on-prior-pipeline organization: prior pipeline overview → new module → integration.
4. Analysis/protocol organization: definitions → taxonomy/protocol → measurement pipeline.

Choose the organization internally based on the paper type and Writing Policy. Do not expose
template-selection notes unless the user asks for reasoning.

## Must Avoid

- Listing implementation details without motivation.
- Introducing modules that do not support any claim.
- Hiding reproducibility-critical details.
- Making the figure carry explanation that the prose should provide.
- **Enumerating a taxonomy/inventory in the body** (every component, condition, subgroup, category,
  or per-category count, one item per line). Mention it in one stroke — dimension, total, and only
  the salient/novel members — and put the full list in a table or appendix. See the Salience And
  Compression rules in `references/sections/paragraph-flow.md`.
- **Burying the point.** Each subsection must open with its key decision or claim, not with
  background, definitions, or counts. Allocate length by importance, not by what is available.

## Self-Check

- Can a reader reconstruct the workflow?
- Does each component map to the Method Tree?
- Does each module have motivation, design, and technical advantage?
- Does each subsection lead with its point rather than background or a list?
- Are taxonomies/inventories/per-category counts compressed to one stroke in the body, with the full
  list in a table or appendix?
- Are assumptions and limitations explicit enough for reviewer scrutiny?
