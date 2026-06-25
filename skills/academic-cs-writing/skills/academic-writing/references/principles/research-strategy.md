# Research Strategy Principles

Use this file before generating or updating a Writing Policy. It contains global paper-strategy
principles, not a required Writing Policy schema. Keep the Writing Policy compact and move section
structure to the Paper Framework.

## Goal-Driven Research

Start from goal-driven research:

1. What field-level or user-level goal matters?
2. What concrete task, setting, or evaluation target represents that goal?
3. What failure case makes the problem urgent?
4. What new knowledge should reviewers get from the paper?

The Writing Policy should capture the research goal and failure case only when they are central to
the paper's story. If the workspace does not support a specific failure case, state a weaker gap
instead of inventing one.

## Failure Case To Technical Challenge

The paper should convert a visible failure case into a root technical challenge. A failure is what
goes wrong; the technical challenge explains why it is hard to fix. The policy should state:

- failure case,
- technical challenge,
- why prior or naive solutions do not solve it,
- what insight or design addresses the challenge.

## Method Tree

Build a lightweight method tree internally before writing the story. For each contribution, module,
benchmark component, metric, dataset, or analysis axis, answer:

- why it is needed,
- why it should work,
- which claim it supports,
- which evidence will validate it.

The method tree informs Method, Experiments, figures, and contribution wording. Do not paste a full
method tree into the Writing Policy unless the user asks for it.

## Backward-Then-Forward Story

Use backward-then-forward construction:

1. Backward: identify the contribution, its benefit, the technical challenge it solves, and the
   prior-work discussion required to make the challenge natural.
2. Forward: write from task or setting to prior practice, unresolved challenge, proposed
   contribution, technical advantage, and evidence.

This prevents an Introduction that reads like a survey and only reveals the paper's point late.

## Avoid Naive-Baseline Patch Framing

Do not frame the work as a trivial patch over a deliberately weak baseline. Even when the change is
incremental, tell the story through the real challenge and the insight that makes the design
necessary.

## Evidence Package

For empirical method papers, the default evidence package is:

- comparison experiments,
- ablation studies,
- stress tests or failure analysis when robustness/safety/generalization is claimed.

Other paper-types can adapt the package, but every central claim still needs aligned evidence.

## Pre-Draft Risk Check

Before confirming a Writing Policy, run the Workspace Logic And Evidence Audit in
`references/checks/workspace-logic-audit.md` (trace-to-artifact, cross-file consistency,
result-to-conclusion logic, scope/integrity smells, evidence-type labeling, terminology stability,
plus the default-on independent recheck). That audit is the mechanism; this section names the
drafting dimensions it should cover. Inspect the policy internally for claim and evidence risks
across five drafting dimensions:

1. contribution,
2. writing clarity,
3. experimental strength,
4. evaluation completeness,
5. method design soundness.

Each serious weakness should become either a claim drafting action, a missing-evidence note, or an
Open Decision. The audit is writing-side only: a weakness can downgrade or scope the wording, mark
a claim, defer it, or trigger stop-and-ask — it never re-runs or redesigns the research. Do not
produce a formal review, scorecard, or long risk map during Writing Policy generation unless the
user explicitly asks for one.

## Key Terms

Stabilize key terms before drafting. Key terms include method names, dataset or benchmark names,
task names, metrics, system components, and concepts that appear in the title, abstract,
contribution list, or main figures.

Ask the user only when a term is decisive: conflicting names exist, the term will appear in the
title or abstract, or the definition changes the paper's claim. Otherwise, choose the clearest
workspace-supported wording and record the use policy.

## Source Notes

- Public sources checked for this adaptation:
  - `https://github.com/pengsida/learning_research`
  - `https://pengsida.net/files/how_to_do_research_v3.pdf`
  - `https://pengsida.net/files/learning_research_v4.pdf`
