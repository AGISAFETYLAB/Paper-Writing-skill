# Reviewer Risk Check

Use this register to predict reviewer attacks and convert them into writing or experiment actions.
For Nature-family or other broad-audience high-impact journal targets, also load
`high-impact-journal-review.md` and assess originality, scientific importance,
interdisciplinary readership, technical soundness, and readability for nonspecialists.

## Risk Register Format

| Risk | Why reviewers may care | Preventive writing action | Needs experiment? |
|---|---|---|---|

## Common Risks

- Weak novelty: clarify insight, difference, and non-claims.
- Unclear problem: rewrite Introduction from problem-first framing.
- Insufficient evidence: weaken claims or add required experiments.
- Unfair baselines: add stronger baselines or explain scope.
- Weak ablation: map ablations to claimed mechanisms.
- Weak metric design: revise metric/evidence mapping.
- Overclaiming: downgrade claim strength.
- Missing limitations: add scoped limitations and failure cases.
- Unrealistic setting: explain assumptions and practical relevance.
- Low reproducibility: add details needed to reproduce method and evaluation.

## Risk Action Mapping

Map each material risk to one action type before returning a review or readiness report:

| Action type | Use when | Allowed handling |
|---|---|---|
| `PROSE_REVISION` | The evidence exists but the text is unclear, disordered, or under-explained | Revise wording, structure, transitions, captions, or section placement |
| `CLAIM_WEAKENING` | The claim is too broad, causal, novel, universal, or strong for the evidence | Narrow scope, change verbs, add boundaries, or delete the unsupported claim |
| `CITATION_VERIFICATION` | A prior-work, dataset, model, baseline, or standard claim lacks a verified citation | Route through `academic-citation`; do not invent metadata |
| `ADDITIONAL_ANALYSIS` | Existing data may answer the concern but the paper lacks analysis, aggregation, or error breakdown | Ask for or add real analysis output; otherwise mark the item open |
| `NEW_EXPERIMENT` | The claim depends on a comparison, ablation, control, or setting not present in the evidence | Flag as outside writing-only scope unless the user supplies results |
| `OPEN_DECISION` | A venue rule, evidence source, compile/PDF state, or missing material could resolve the risk but is unavailable | Do not declare readiness; ask for the missing fact or artifact |
| `BLOCKED` | The supplied draft already contains a false/unsupported central claim, broken format gate, or missing required artifact | Stop readiness; fix, weaken, or surface the blocker |

Prefer the cheapest truthful action. Do not label a missing experiment as prose polish, and do not
label an unsupported central claim as `OPEN_DECISION` when the current manuscript already makes it.
