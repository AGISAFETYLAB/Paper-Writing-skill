# Experiments Principles And Templates

## Goal

Experiments provide evidence for the paper's claims. They should answer research questions, not
only report numbers.

## Three Questions

Before writing Experiments, answer:

1. Is the method better than strong baselines? — comparison experiments against strong and recent
   baselines, standard metrics on main benchmarks, fair protocol.
2. Which modules/design choices make the gain? — ablation studies for each key module/design
   choice, remove/replace/disable variants, report delta to full model.
3. How far can the method generalize? — harder settings, stress tests, failure modes, realistic
   boundaries.

## Experiment Planning

Plan experiments from two directions:

1. **Claim-driven**: each contribution in the Writing Policy → one validation experiment.
2. **Module-driven**: each component in the Method Tree → one ablation study.

This ensures every claim has evidence and every module has a reason to exist.

## Evidence Package

For empirical method-style papers, check whether the section includes:

1. comparison experiments against strong and relevant baselines,
2. ablation studies for key modules or design choices,
3. stress tests, failure analysis, or limitations when safety/generalization is claimed.

For benchmark or analysis papers, adapt the package to coverage, reliability, evaluation protocol,
taxonomy validity, and insight quality.

## Section Organization

Standard method evaluation: setup → main comparison → ablation → analysis → failure cases.
Benchmark evaluation: benchmark statistics → model evaluation → breakdown → controls → limits.
Analysis paper: research questions → findings → supporting experiments → caveats.
New-task setting: protocol → adapted baselines/variants → diagnostics → realistic-scenario checks.

These flows are **content blocks and paragraph roles, not mandatory numbered subsections**. Prefer
flowing prose; turn a block into a `\subsection` only when it spans multiple paragraphs or owns a
distinct table/figure. Keep Experiments to roughly 0–4 subsections — do not emit one numbered
subsection per analysis step (no `4.1 … 4.6`); a single-paragraph step should stay a paragraph,
optionally with a `\paragraph{}` run-in or bold lead-in.

## Subsection Title Quality

Use finding-led, reader-facing subsection titles. The title should name the comparison, protocol, or
interpretation the reader will get, not the artifact state, data-storage state, or appendix location.
Avoid weak scaffolding titles such as `Aggregate Result Snapshot`, `Result Snapshot`, `Appendix Matrix`, `Appendix Heatmap`, or `Full Matrix`. Better titles include `Overall Performance-Robustness Tradeoff`, `Outcome Distribution and Denominator Effects`, `Category and Subgroup Concentration`, or another title that states the analysis role. If the only content is "the appendix
contains a detailed matrix," do not make a subsection; write one prose cross-reference at the end of
the relevant analysis block.

**Statistics are tables, not prose.** "Benchmark statistics" and per-category breakdowns (per-app,
per-condition, per-subgroup, per-split counts) belong in **one table or figure**, not enumerated in
sentences. In prose, lead with the point and cite only the figures that carry an argument — the
total, the dominant or surprising share, the headline coverage — then point to the table. Do not
transcribe a table into running text. See the Salience And Compression rules in
`references/sections/paragraph-flow.md`.

## Comparison Version 1 (direct baselines exist)

Use when direct baseline methods exist.

Template:

1. State dataset/task/protocol.
2. Explain baseline selection and fairness.
3. Report standard metrics.
4. Explain the primary comparison result.
5. State caveats such as run failures, missing baselines, or protocol differences.

## Comparison Version 2 (no direct baselines)

Use when the task is new and direct baselines are unavailable.

Template:

1. Explain why direct baselines do not exist.
2. Construct meaningful variants, simple baselines, adapted methods, or diagnostic controls.
3. Report what each comparison is meant to test.
4. Avoid claiming broad superiority over a nonexistent baseline set.

## Ablation Package

A strong ablation package usually has two levels:

1. A main ablation table and matching visualization that compare how the paper's core contributions
   and major components affect method performance.
2. Several focused ablation tables and matching visualizations. Each small table should isolate the
   design choices within one pipeline module and show their effect on method performance, such as
   hyperparameter sensitivity, input-quality sensitivity, or the performance impact of removing a
   design choice.

Each ablation should state:

- which claim it tests,
- what is removed/replaced/changed,
- expected effect,
- observed effect,
- whether the claim remains supported.

## Display Evidence Role

The Experiments section only owns the evidence role of display items: decide which claims need a
table or figure, what comparison or ablation each display carries, and what each display item
proves. All display design and implementation details -- caption, span, booktabs, overflow, and QA
-- belong to `academic-figure`.

## Template Selection

Select an experiment organization before writing:

1. Standard method evaluation: setup → main comparison → ablation → analysis → failure cases.
2. Benchmark evaluation: benchmark statistics → model evaluation → breakdown → controls → limits.
3. Analysis paper: research questions → findings → supporting experiments → caveats.
4. New-task setting: protocol → adapted baselines/variants → diagnostics → realistic-scenario
   checks.

Choose the organization internally based on paper type, available evidence, and reviewer risk.
Do not expose template-selection notes unless the user asks for reasoning.

## Rigor Checklist

1. Are baselines recent and relevant?
2. Are metrics sufficient and standard for this task?
3. Is ablation tied to every key design claim?
4. Are claims in Abstract/Introduction supported by reported numbers?
5. Are limitations of evaluation scope explicitly stated?
6. Do main results support the Abstract and Introduction?
7. Are missing baselines, controls, or metrics recorded as evaluation risks or limitations?
8. Are per-category statistics confined to a table/figure, with prose citing only the numbers that
   carry an argument, rather than enumerated in sentences?
