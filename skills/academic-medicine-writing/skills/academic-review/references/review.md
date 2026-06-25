# Medicine Review Risks

Check for:

- population too narrow for the stated conclusion
- endpoint, comparator, or timeframe mismatch
- missing external validation
- missing ethics, consent, or registry information
- unreported adverse events for safety claims
- selective subgroup emphasis
- citation supports only a weaker claim

Map each issue to prose weakening, citation verification, open decision, or blocker.

## Submission-Readiness Review

Use this verdict scale:

| Verdict | Meaning |
|---|---|
| PASS | Checklist-critical items satisfied or explicitly not applicable |
| WARN | Minor wording, formatting, or non-critical checklist gaps remain |
| FAIL | A central claim, analysis description, checklist item, or statement is incomplete |
| BLOCKED | Missing ethics/consent/registration/data access or invented clinical facts |

Always include a checklist compliance matrix in full manuscript reviews. For checklist-bound
reviews, compare it against the selected item-level checklist JSON under
`_shared/checklists/items/`.

## Official-Source Gate

For any PASS verdict, cite the target journal's official instructions, the date checked, and the
reporting checklist used. Full-draft readiness requires the route-appropriate production artifact:
`manuscript.docx` for a word-first route, `main.pdf` for a latex-first route, or an explicit
not-submission-ready status for a generic-review route. If the manuscript route is LaTeX-based and
only Markdown exists, the verdict is FAIL even when the prose is strong.

## Review Dimensions

| Dimension | Failure examples | Writing action |
|---|---|---|
| Medical claim grammar | missing population, endpoint, timeframe, analysis population, uncertainty | revise sentence or mark missing evidence |
| Checklist compliance | missing flow diagram, eligibility, missing data, bias, validation, risk-of-bias item | add text/display if source exists; otherwise block |
| Statements | unknown ethics/consent/registration/data sharing/funding/conflicts | write from facts or mark blocking unknown |
| Citation integrity | unsupported clinical effect, wrong population/outcome source, unverified DOI/PMID | invoke citation skill, weaken, or remove |
| Display integrity | table hides denominator/missingness, figure legend incomplete, no source data | invoke figure skill or block |
| Format/template production | missing manuscript.docx on Word route, missing compiled PDF on LaTeX route, generic shell mislabeled official, target instructions unchecked, missing continuous page numbering, figures embedded in a JAMA submission-clean manuscript instead of separate upload assets | fix package or report blocker |

For JAMA/JAMA-family submissions, the review must separate `submission-clean` artifacts from
reader-preview artifacts. A primary `manuscript.docx` with embedded figure images is a production
risk unless the current official instructions or author preference explicitly allow it; a separate
`review-preview-inline.docx` may embed figures but must not satisfy the primary submission-file gate.

Run or inspect `scripts/audit_submission_package.py` before final PASS/BLOCKED wording. This
aggregate package gate checks `submission-package.md`, route-specific production artifacts, and
`workflow-state.json`; it is allowed to return an internally consistent `BLOCKED` package when the
blocker set is explicit.

Also audit JAMA component quality: Key Points should be Question/Findings/Meaning within the active
75-100 word budget; Findings should emphasize the primary outcome without statistical-detail
overload; Original Investigation abstracts should use separate Design, Setting, and Participants
headings when source-supported; Table 1 should include Overall column, missing values or a precise
missingness note, and standardized difference definition; Table 2 should include risk difference
95% CI, crude OR with 95% CI, and prespecified primary/secondary outcome labels when source-supported.
For JAMA original data reports other than clinical trials and meta-analyses, titles should not
include study type/design labels such as "cohort study". Fixture-derived or deterministic adjusted
estimates are blocker-level main-display defects when they appear in Table 2 or a main figure row;
they belong in a supplement/provenance table or should be omitted.

For each finding, say whether it is a scientific weakness or a reporting weakness. Do not let strong
prose hide missing science.
