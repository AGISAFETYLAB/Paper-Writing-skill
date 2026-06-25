# Medicine Review QC Rules

Use this file with `academic-review` for submission-readiness checks, full-draft closing review,
and revision-stage manuscript audits.

## Severity taxonomy

Classify every finding by the highest applicable severity:

| Severity | Meaning | Typical action |
|---|---|---|
| `blocker` | Cannot call the package submission-ready or review-clean | stop, fix, or mark `BLOCKED` |
| `major compliance gap` | Likely to create desk-rejection, major-revision, or credibility risk | revise before submission |
| `moderate reporting weakness` | Reviewers may request clarification but paper identity remains intact | revise when source evidence exists |
| `minor polish issue` | Formatting, wording, or local consistency cleanup | fix if low cost |
| `unclear_due_to_missing_material` | Input is insufficient for a reliable judgment | ask for source or mark unknown |
| `not_applicable` | Study type or target journal does not require the item | justify briefly |

Do not flatten reporting problems into a single checklist. A missing participant flow, endpoint
definition, validation detail, trial registration, or ethics statement is not equivalent to a minor
style issue.

## Required Audit Tables

### Checklist severity table

| checklist_item | status | severity | manuscript_location | missing_or_weak_evidence | action |
|---|---|---|---|---|---|

### claim-source audit table

| manuscript_claim | evidence_level_mapping | cited_or_internal_source | source_alignment | severity | required_action |
|---|---|---|---|---|---|

evidence-level mapping values: descriptive observation, association, predictive performance,
mechanistic support, causal suggestion, causal evidence, translational relevance, implementation
readiness. Do not let wording use a higher evidence tier than the study design supports.

### cross-component consistency table

| component_pair | checked_value | consistency_status | version_drift_pattern | severity | required_action |
|---|---|---|---|---|---|

Use this as the cross-manuscript consistency audit. Compare title, abstract, methods, results, figures, tables, supplements, statements, and
submission-package fields. Name version drift patterns explicitly: sample-size drift, endpoint
wording drift, outcome-label drift, analysis-description drift, terminology drift, figure/table
numbering drift, or conclusion-result mismatch.

### Citation integrity table

| claim_or_sentence | citation | alignment | issue_type | severity | required_action |
|---|---|---|---|---|---|

Issue types include topical-only support, population mismatch, outcome mismatch, evidence-level
overextension, quote drift, second-hand citation, unverified DOI/PMID, and orphaned reference.
Second-hand citation risk must be flagged when a review article or consensus document is used as if
it directly established primary data.

## Reviewer Risk Logic

For every blocker or major compliance gap, explain the reviewer risk in one concrete sentence. The
explanation should identify what a reviewer or editor cannot verify: eligibility, denominator,
endpoint, model validity, diagnostic reference standard, search reproducibility, ethics approval,
data access, citation support, figure/table linkage, or submission artifact completeness.

## Claim Registry And Reliability Cross-Checks

Use the Claim Registry from `_shared/checks/claim-verification.md` as an input to the claim-source audit
table. Any central claim marked `MAJOR_DISTORTION` or `UNVERIFIABLE` is at least a major compliance
gap and may be a blocker when it supports the title, abstract conclusion, primary outcome, diagnostic
accuracy, prediction-model performance, or policy recommendation.

Run the Result Reliability Audit from `_shared/checks/reliability.md` before closing the review. Record
whether each defect is a scientific weakness vs reporting weakness so the response does not imply
that better prose can repair missing validation, uncontrolled confounding, unavailable sensitivity
analysis, or absent reference-standard evidence.
