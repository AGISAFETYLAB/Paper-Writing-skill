# Medicine Scientific Integrity Veto

Run this before any final PASS, submission-ready wording, or clean-review verdict. Any triggered
item makes the verdict `BLOCKED` until corrected. This is a hard gate, not a scoring penalty.

## Scientific Integrity Veto

Block the output when any manuscript, response, citation file, figure, table, or submission package
contains:

- fabricated DOI, fabricated PMID, fabricated PMCID, fabricated registry identifier, or fabricated
  repository accession;
- invented sample sizes, event counts, adverse events, p values, confidence intervals, effect sizes,
  sensitivity analyses, subgroup results, or efficacy/safety data;
- patient-specific medical advice, diagnosis, treatment instruction, triage recommendation, or
  clinical decision support language;
- causal inflation: association, prediction, correlation, or exploratory biology written as causal
  evidence, mechanism established, clinical utility, deployment readiness, or treatment effect;
- ethics or registration claims that are absent from source material, including invented IRB names,
  approval numbers, consent status, trial registration IDs, protocol IDs, or SAP availability;
- a generic or instruction-derived journal shell represented as an official template;
- a checklist matrix represented as complete formal compliance when the underlying matrix is a short
  local core-screen or when official instructions have not been checked.

## Required Action

When a veto fires:

| Veto type | Required action |
|---|---|
| Fabricated identifier or citation | remove or mark `not verified`; invoke citation audit |
| Invented result or sample fact | remove the result or replace with a precise evidence-needed marker |
| Practice-boundary violation | rewrite as manuscript-scoped research text, not advice |
| Causal inflation | downgrade to descriptive, association, prediction, or hypothesis-generating wording |
| Ethics/registration invention | replace with `[AUTHOR: provide ...]` and mark submission blocked |
| Template/checklist overclaim | rename the artifact honestly and block submission-ready wording |

The review report must name the veto and the affected manuscript location. Do not hide a veto under
minor "author review needed" language.
