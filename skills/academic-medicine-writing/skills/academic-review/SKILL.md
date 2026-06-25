---
name: academic-review
description: Use when reviewing, auditing, or checking a medical, clinical, biomedical, public-health, diagnostic, treatment, systematic-review, prediction-model, case-report, or health-economics manuscript for submission readiness.
---

# Academic Review — Medicine

Owns the closing gates for a medical manuscript.

Intent class: `submission-review`. Use this route when the user asks to review an existing
manuscript package, run a submission-readiness check, audit checklist/statement/citation/display
gates, or identify reviewer risk. This is not a request to generate a new first draft. If review
findings require missing package components to be produced, route those follow-up production tasks
back to the hub as `package-completion`.

Route summary: review an existing manuscript package; this is not a request to generate a new first draft.

## Protocol

1. Read `manifest.yaml`.
2. Load `references/review.md`, `../../_shared/checks/research-veto.md`, and
   `references/checks/review-qc.md` before giving a submission-readiness verdict.
3. Load `../../_shared/checks/reliability.md` and `../../_shared/checks/claim-verification.md` whenever the
   review touches result validity, claim strength, citation drift, or central clinical conclusions.
4. Load `../../_shared/submission/data-availability.md`, `../../_shared/submission/submission-standards.md`, the
   selected checklist JSON, target journal standard card, and statement references when the package is a full
   draft or submission check.
5. Load `../../_shared/core/package-gates.md` and run or inspect
   `scripts/audit_submission_package.py` for package-level PASS/BLOCKED consistency.
6. Apply the Research veto before any PASS, clean, reviewable, or submission-ready wording.

## Submission-Readiness Review

Run this whenever a complete medical `paper/` manuscript package exists, when the user asks for a medical
submission check, or before calling a draft clean. Findings lead the response and are ordered by
severity.

## Required Gates

1. Research veto: no fabricated DOI/PMID/registry values, no invented sample sizes, p values,
   confidence intervals, adverse events, ethics approvals, trial registrations, or patient-specific
   medical advice.
2. Manuscript completeness: title page, structured abstract, Key Points when required, IMRaD body,
   limitations, statements, references, tables/figures, supplement/checklist notes.
3. Reporting checklist: selected item-level checklist JSON items mapped to manuscript locations or
   justified as not applicable.
4. Medical claim audit: population, intervention/exposure/index test/predictor, comparator,
   outcome, timeframe, uncertainty, and analysis population are explicit.
5. Claim verification audit: Claim Registry coverage, source tracing, no `MAJOR_DISTORTION`, no
   unresolved `UNVERIFIABLE` central claim, and no source-to-claim overextension according to
   `../../_shared/checks/claim-verification.md`.
6. Result reliability audit: design and bias, statistical and model risk, validation chain, and
   claim discipline are checked with `../../_shared/checks/reliability.md`.
7. Citation audit: run or inspect `../academic-citation/scripts/audit_medical_citations.py`; require no unsupported
   central claim, no orphaned references, no malformed DOI/PMID/PMCID fields, no lost biomedical
   acronym/proper-name capitalization in rendered references, AMA superscript citations for
   JAMA/JAMA-family word-first routes, and numbered references in first-citation order.
8. Statement audit: ethics, consent, trial registration, data sharing, funding, conflicts, author
   contributions, acknowledgments.
9. Data Availability And FAIR Audit: data/code availability, repository or controlled-access route,
   DataCite-ready metadata, third-party restrictions, and figure source data are checked with
   `../../_shared/submission/data-availability.md`.
10. Draft length audit: `paper/submission-package.md` records `Actual main-text word count`, the
   applicable main-text word budget, and `draft length gate: PASS` only when the count is inside the
   recorded budget or a confirmed exception is explicitly documented. An under-target draft cannot pass because it is polished, structurally complete, or compiled.
11. Display and figure asset audit: every planned main `Fig.` display has either a corresponding
   figure asset under `paper/figures/` and an `\includegraphics` call, or a documented framework
   decision downgrading it to a table.
12. Visual display gate: for observational cohort drafts with source-supported counts/effects, the
   main Results display set includes at least the cohort flow, outcome rate figure, and
   effect-estimate forest plot unless a precise blocker is documented.
13. Table aesthetics audit: rendered main tables use `booktabs` for LaTeX routes or visible Word
   cell borders for Word routes, compact typography, deliberate column widths and spacing, compact
   table notes, and no stacked-word or crowded effect-estimate rendering. For LaTeX routes, this
   includes compiled layout QA with `../academic-figure/scripts/inspect_compiled_layout.py`; record
   `paper/layout-qa/layout_qa_summary.md`, the contact sheet or page PNG paths, and the table-page
   inspection status. Block when table pages show clipped cells, unreadable effect estimates,
   sparse full-width pages, or right-side underfill, or when `main.log` contains unresolved
   `Float too large`, large `Overfull \vbox`, or margin-crossing `Overfull \hbox` signals.
14. Figure/table linkage audit: every table, figure, and supplement cited in text supports the stated
   claim and has matching numbering, denominator, timeframe, and caveat language.
   For JAMA/STROBE routes, a fixture-derived, deterministic, placeholder, or non-fitted adjusted
   estimate must not appear as a main claim, main Table 2 column, or main figure row; move it to a
   supplement/provenance table or report the JAMA component gate as `BLOCKED`.
15. Format-specific production gate:
   - Word route: `paper/manuscript.docx` exists, route is recorded as `word-first`, figures/tables are
     separate/editable where the journal expects them, any PDF is labeled `review-preview.pdf`, and
     the DOCX structure audit plus DOCX layout audit have passed, including double-space text,
     required new page section starts, and AMA superscript reference rendering.
   - LaTeX route: `paper/main.pdf` exists as the compiled PDF for `latex-first` full-draft outputs
     and compile status is recorded.
   - Generic-review route: the package is not called submission-ready.
16. Aggregate package gate: `scripts/audit_submission_package.py` confirms that
   `paper/submission-package.md`, route-specific production artifacts, and `paper/workflow-state.json`
   are internally consistent. A blocked-but-complete package may pass this aggregate contract only
   when `Submission-readiness verdict: BLOCKED` and the blocker set are explicit.

## Word-First DOCX Structure Audit

For every `word-first` package, run or inspect the result from
`scripts/audit_word_docx.py`. A Word-route `paper/manuscript.docx` is not enough by existence alone.
The DOCX structure audit must check `word/settings.xml`, `word/styles.xml`, `word/theme/`,
`word/numbering.xml`, paragraph style coverage, table style coverage, `word/media`, and `w:drawing`.
The DOCX layout audit must also check core title and heading style sizes, cell border coverage,
table grid coverage, `w:tcBorders`, `w:tblGrid`, double-space text coverage, required new page
breaks, and superscript reference runs.

Block or downgrade the production verdict when the DOCX is minimal OOXML, a package with
document.xml and styles.xml only, has no `word/media` or `w:drawing` evidence for embedded planned
figures, lacks styled editable tables, lacks cell borders/table grids, or inherits nonconforming
title/section style sizes. In those cases, do not mark `format-specific production gate: PASS (word-first)`,
do not mark `visual display gate: PASS`, and do not mark the table aesthetics gate PASS. Report the
exact DOCX audit defect as a production weakness.

For every package with `paper/references.bib`, run or inspect `../academic-citation/scripts/audit_medical_citations.py`.
Block or downgrade the citation verdict when bibliography keys are missing or uncited, modern medical
entries lack DOI/PMID/PMCID/URL/registry identifiers, DOI/PMID/PMCID fields are malformed, rendered
references hide identifiers, or biomedical acronyms/proper names such as STROBE, CONSORT, PRISMA,
COVID-19, SARS-CoV-2, ICD-10, NIHSS, AUC, or ROC are lowercased in rendered references.

For JAMA/JAMA-family routes, also run or inspect `../academic-citation/scripts/audit_ama_citations.py`. Block or downgrade
the citation verdict when the manuscript uses literal square-bracket citations, the reference list is
not in first-citation order, reference numbers are not consecutive, references are uncited, or a
reference with more than 6 authors is not shortened to the first 3 followed by et al.
Use `_shared/submission/word-first-production.md` as the detailed word-first DOCX and AMA production
contract.

If any gate fails, revise or return a blocking issue list. Do not call an incomplete manuscript
submission-ready.

## Required QC Outputs

Use the severity taxonomy from `references/checks/review-qc.md`. A full manuscript review must include:

- checklist severity table;
- claim-source audit table with evidence-level mapping;
- Claim Registry audit table with source tracing and `MAJOR_DISTORTION` / `UNVERIFIABLE` status;
- Result Reliability Audit table separating scientific weakness vs reporting weakness;
- Data Availability And FAIR Audit table for repository, restricted access, third-party data, and
  figure source data status;
- cross-component consistency table for title, abstract, methods, results, displays, statements, and
  submission package fields;
- citation integrity table that flags second-hand citation, overextension, quote drift, and
  unverified identifiers;
- explicit reviewer risk logic for every blocker or major compliance gap.

## Checklist Compliance Matrix

The final review must inspect the checklist compliance matrix from the Paper Framework or
`paper/submission-package.md` against the selected item-level checklist JSON. Each row must be
classified as `satisfied`, `partial`, `missing`, `not_applicable`, or `needs_user_evidence`. A
missing core checklist item is a blocking or major issue unless the manuscript type justifies not
applicable.

## Scientific Weakness Vs Reporting Weakness

Always label scientific weakness vs reporting weakness explicitly.

Separate these explicitly:

- Scientific weakness: evidence does not exist, design is underpowered, no external validation,
  missing sensitivity analysis, uncontrolled confounding, no reference standard, incomplete follow-up.
- Reporting weakness: evidence exists but the manuscript omits denominator, eligibility, missingness,
  endpoint timing, statistical model, flow diagram, statement text, or checklist location.

Writing can fix reporting weakness. Writing cannot fix missing science; it can only weaken the claim,
mark the gap, or ask the user.

## Official-Source Gate

Before saying submission-ready, verify `paper/submission-package.md` includes:

- target journal and article type,
- official-source URL and date checked,
- Submission Format Route and primary submission file,
- template status (official downloaded template, instruction-derived shell, generic shell, or
  user-provided template),
- selected reporting checklist,
- statement status,
- format-specific production gate status.

The gate fails if a generic/instruction-derived shell is called official, if current author
instructions were not checked or explicitly accepted as a dated snapshot, or if required statements
are invented/unknown. Do not require `paper/main.pdf` for word-first routes; require
`paper/manuscript.docx` instead.

## Before Returning

Return:

- blocking issues first,
- major reporting/compliance issues,
- citation/display/statement defects,
- research-veto defects,
- claim-source audit table,
- cross-component consistency table,
- severity taxonomy summary,
- figure asset audit defects,
- visual display gate defects,
- table aesthetics audit defects,
- format/template production risks,
- concise change summary only after findings.

Do not bury unresolved ethics, registration, data-sharing, checklist, citation, or production-artifact
defects in a generic "needs final author review" note.
