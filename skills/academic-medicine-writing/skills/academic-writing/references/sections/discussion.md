# Discussion

## Core Chain

Use this chain for medical discussions:

```text
principal finding -> interpretation -> comparison -> limitation -> impact -> mitigation -> cautious conclusion
```

The limitation sequence must be specific:

```text
limitation -> impact -> mitigation
```

Do not list limitations without explaining how they affect interpretation and what design or
analysis feature reduces or fails to reduce the risk.

## Paragraph Plan

| Paragraph | Role | Required content |
|---|---|---|
| 1 | principal findings | two or three findings, no new results |
| 2 | interpretation | why the findings matter within the study design boundary |
| 3 | comparison | prior work, guidelines, or biological/clinical context with verified citations |
| 4 | implications | clinical, public-health, diagnostic, methodological, or research implications, scoped to evidence strength |
| 5 | limitations | bias, confounding, missingness, sample, follow-up, measurement, external validity, multiplicity, model overfitting |
| 6 | conclusion | cautious take-home message aligned with title, abstract, and results |

Short formats can combine paragraphs, but principal finding, limitation, and conclusion must remain
separate in logic.

## Limitation Writing

Use this structure:

```text
<Limitation>. This could <specific impact on direction, precision, generalizability, or validity>.
We mitigated this by <design/analysis feature>, but <residual uncertainty> remains.
```

If no mitigation exists, state the residual uncertainty directly. Do not use generic language such
as "more research is needed" without naming the specific unresolved question.

## Claim Strength

- RCTs can discuss intervention effects if randomization, adherence, and analysis support the claim.
- Observational studies should discuss associations and residual confounding unless causal inference
  is explicitly designed and justified.
- Diagnostic studies should separate accuracy from clinical utility.
- Prediction-model studies should separate discrimination, calibration, validation, and deployment.
- Systematic reviews should separate evidence certainty from pooled effect size.

## Common Failures

- restating all Results instead of interpreting the principal findings,
- introducing new results or new endpoints,
- overstating clinical practice implications,
- citation-thin comparison with prior work,
- generic limitations not tied to bias, validity, precision, or generalizability.
