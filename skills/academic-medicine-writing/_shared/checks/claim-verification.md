# Claim Verification Protocol

Use this protocol when a paper, abstract, figure legend, reviewer response, or citation audit needs
to prove that quantitative and factual claims match their sources.

## Scope

Extract and verify:

- all numerical claims: counts, percentages, effect sizes, confidence intervals, p values, dates;
- categorical assertions: first, largest, validated, established, guideline-recommended;
- trend claims: increasing, declining, stable, improved, worse;
- causal or practice-facing claims;
- claims that cite reviews when primary evidence is needed.

## Claim Registry

Create a Claim Registry before judging support:

| claim_id | manuscript_claim | section_or_location | cited_or_internal_source | implied_support_level | verification_mode |
|---|---|---|---|---|---|

For citation audits or final-check mode, expand the registry into the medical citation evidence
schema used by `skills/academic-citation/scripts/audit_medical_citations.py`:

| claim id | claim text | citation key | source anchor | population match | outcome match | metric/timeframe match | conclusion strength | verdict | required action |
|---|---|---|---|---|---|---|---|---|---|

`verification_mode` values:

- `pre-review-sample`: check at least 30% of factual claims, minimum 10 when available.
- `final-check`: check 100% of central and high-risk claims before PASS/submission-ready wording.
- `targeted`: check a user-specified claim or reviewer concern.

## Source Tracing

Use source tracing for every central claim before PASS wording.

For each claim, identify the exact source anchor:

| claim_id | source_anchor | population_match | outcome_match | timeframe_match | method_match | support_verdict | action |
|---|---|---|---|---|---|---|---|

Source anchors may be a table, figure, registry field, protocol/SAP section, repository record, or
verified literature passage. If the source cannot be inspected, use `UNVERIFIABLE_ACCESS` rather
than inventing support.

## Verdict Taxonomy

| Verdict | Meaning | PASS effect |
|---|---|---|
| `VERIFIED` | Claim matches source exactly or within justified rounding. | Can remain. |
| `MINOR_DISTORTION` | Paraphrase is slightly loose but meaning is preserved. | Revise when low cost. |
| `MAJOR_DISTORTION` | Claim exaggerates, changes population/outcome/timeframe, or overstates certainty. | Blocks PASS. |
| `UNVERIFIABLE` | Source does not contain the claim or source identity is missing. | Blocks PASS. |
| `UNVERIFIABLE_ACCESS` | Source exists but cannot be inspected in the current run. | Note risk; do not use for central PASS claims without author acceptance. |
| `SECOND_HAND_CITATION_RISK` | Review or guideline is used as if it were primary evidence. | Replace or weaken. |

PASS requires zero `MAJOR_DISTORTION` and zero `UNVERIFIABLE` for central claims. Final-check mode
requires every central clinical claim to have either verified source support or an internal
manuscript evidence anchor.

## Rewrite Rule

When support is weak, provide the strongest supportable wording. Do not simply add hedging words.
Change the claim type when needed: causation -> association, clinical utility -> predictive
performance, mechanism established -> mechanistic support, deployment readiness -> future
validation needed.
