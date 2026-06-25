# Claim-Evidence Check

Use this rulebook to decide what the paper is allowed to claim.

## Claim Strength Levels

| Level | Meaning | Required evidence | Writing action |
|---|---|---|---|
| strong | Direct, broad claim such as state-of-the-art or robust generalization | fair strong baselines, matching protocols, multiple settings, ablation or analysis | allow only when evidence is direct |
| moderate | Claim holds under the paper's evaluated settings | main results plus reasonable baselines | state scope explicitly |
| weak | Preliminary or narrow claim | limited result or qualitative evidence | use cautious wording |
| speculative | Plausible but not shown | no direct evidence | move to discussion or future work |
| forbidden | False, unsupported, or citation-mismatched claim | none or contradictory evidence | remove |

## Abstract And Introduction Rule

Claims in Abstract and Introduction receive the strictest checks because reviewers use them to
form the paper's first impression.

## Examples

- "Achieves state-of-the-art performance" requires fair comparison against strong current baselines.
- "Improves robustness" requires robustness-specific evaluation, not only average task success.
- "Generalizes to unseen tasks" requires cross-task, cross-domain, or held-out setting evidence.
- "Reduces cost" requires cost, token, latency, or compute measurements.
