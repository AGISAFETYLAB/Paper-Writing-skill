# Medicine Submission Standards

Official-source snapshot checked: 2026-06-23.

Medicine is not a template-first writing domain. The blocking standard is the target journal's
current author instructions plus the correct reporting checklist and ethics/statements package.
The blocking production standard is route-specific: Word-first journals need a Word/editable
manuscript package, LaTeX-first journals need source plus compiled PDF, and unresolved targets remain
review-only. A PDF alone is never enough.

## Official Anchors

| Source | Use in this skill |
|---|---|
| ICMJE Recommendations, updated January 2026: https://www.icmje.org/recommendations/ | Baseline medical manuscript preparation, IMRaD logic, authorship, conflicts, ethics, trial registration, data sharing, and publishing responsibilities. |
| EQUATOR reporting guidelines: https://www.equator-network.org/reporting-guidelines/ | Route study type to CONSORT, SPIRIT, STROBE, PRISMA, STARD, TRIPOD/TRIPOD-AI, CARE, GATHER, CHEERS, or another required checklist. |
| JAMA Network Open Instructions for Authors: https://jamanetwork.com/journals/jamanetworkopen/pages/instructions-for-authors | JAMA-style Original Investigation constraints such as structured abstract, Key Points, word/display-item limits, Data Sharing Statement, required reporting guideline, and Word-first/editable manuscript handling when applicable. |
| Nature Medicine content types and initial formatting: https://www.nature.com/nm/content and https://www.nature.com/nm/submission-guidelines/initial-formatting | Content-type length budgets, display/reference limits, and initial submission PDF/source expectations. |
| BMJ Case Reports author page and official Word templates: https://casereports.bmj.com/pages/authors | BMJ Case Reports article-type templates, summary/description word limits, figure/video handling, consent, and author statements. |

## Submission Format Routes

Use the target journal's current author instructions to choose one route:

| Route | Use when | Required production artifact |
|---|---|---|
| `word-first` | The journal expects Word or editable manuscript files, including JAMA/JAMA-style Original Investigation unless an official source says otherwise. | `paper/manuscript.docx` plus editable/separate figures and tables where required, with passing DOCX structure audit and DOCX layout audit. |
| `latex-first` | The journal accepts or provides TeX/LaTeX source and the user or journal needs that route. | `paper/main.tex` and compiled `paper/main.pdf`. |
| `generic-review` | The target journal or accepted source format is unresolved. | `paper/manuscript.md`; not submission-ready. |

The submission package must record a `format-specific production gate` status. Do not require a compiled PDF for word-first routes. Do not call a generic-review package submission-ready. For word-first production details, use `_shared/submission/word-first-production.md`.

For word-first routes, the production gate must include a DOCX structure audit and DOCX layout
audit. Inspect `word/settings.xml`, `word/styles.xml`, `word/theme/`, `word/numbering.xml`,
paragraph style coverage, table style coverage, `word/media`, and `w:drawing`; also inspect core
title and heading style sizes, cell border coverage, table grid coverage, `w:tcBorders`, `w:tblGrid`,
double-space text coverage, required new page section starts, continuous page numbering, and AMA
superscript reference runs. A minimal OOXML package with document.xml and styles.xml only is not a valid
Word-first production artifact. A structurally valid DOCX with oversized inherited title styles or
borderless cells is also not a valid Word-first production artifact. A JAMA-style Word manuscript
with literal bracketed numeric citations, missing new page starts, or single-spaced main text is not
a valid Word-first production artifact. If the DOCX audit fails, do not
mark `format-specific production gate: PASS (word-first)` and do not mark `visual display gate: PASS`
from separate figure files alone.

For JAMA/JAMA-family word-first routes, distinguish the primary `submission-clean` manuscript from a
reader convenience preview. The primary `paper/manuscript.docx` should include the title page,
abstract, text, references, Figure Legends, and Tables, but figures should be submitted as separate
files and not embedded in the manuscript text. A separate `paper/review-preview-inline.docx` may
embed figures for internal review; record it as a preview artifact only. The DOCX audit must check
continuous page numbering from the title page and must report whether figures are embedded in the
primary manuscript or confined to the preview file.

Contract phrase: figures should be submitted as separate files.

Run `skills/academic-review/scripts/audit_jama_components.py` for JAMA/JAMA-family Original Investigation drafts. The audit
must check Key Points length and structure, Abstract heading structure, required Design/Setting/
Participants evidence, Table 1 content fields including Overall column, missing values, and
standardized difference definition, and Table 2 content fields including risk difference 95% CI,
crude OR with 95% CI, and prespecified outcome role labels.

For word-first routes with no valid official or user-provided Word template, use
`assets/templates/word/generic-medical-word-reference.docx` as the package-local generic Word
reference shell. This is not an official Word template. Record official-template lookup status in
`paper/submission-package.md`; use `download-blocked` when an official source exists but cannot be
downloaded in the current environment. JAMA/JAMA-style routes must not claim an official Word
template unless the target journal provides one or the user supplies a valid official file.

For JAMA/JAMA-family reference lists, run `skills/academic-citation/scripts/format_ama_manuscript.py` and
`skills/academic-citation/scripts/audit_ama_citations.py`. The manuscript must use AMA superscript numeric citations, number
references in first-citation order, keep reference-list numbering consecutive, and use AMA author
shortening when there are more than 6 authors. The manuscript component order should place
References before end-matter legends/tables and keep the Tables section as the final manuscript
component.

## Required Submission Package

A full medical output must include:

- the route-appropriate production artifact: `manuscript.docx` for `word-first`, `main.tex` and
  compiled `main.pdf` for `latex-first`, or `manuscript.md` for `generic-review`
- `paper/title-page.md` with author names, affiliations, corresponding author, ORCID fields when
  provided, word count, display count, and manuscript metadata
- `paper/cover-letter.md` for named target journals, or a visible blocker when author/journal facts
  are insufficient
- `paper/editorial-system-checklist.md` with ICMJE authorship approval, conflicts, funding,
  data/code availability, ethics/consent/registration, AI-use disclosure, permissions, suggested
  reviewers, and previous submission or reviewer comments when applicable
- target journal and article type
- active `target_length_budget`, source type, date checked, count scope, lower bound, upper bound,
  and whether the lower bound is official or a field-convention completion floor
- Submission Format Route and primary submission file
- selected reporting checklist and checklist compliance matrix
- ethics/IRB, consent, trial registration, funding, conflicts, author contributions, data/code availability, and AI-use statements as applicable
- flow diagram or protocol/SAP/supplement when required by study type
- citation audit for clinical claims, reporting guideline, registry, dataset, and software claims
- Data Availability And FAIR Audit covering repository choice, controlled-access route,
  third-party restrictions, DataCite-ready dataset metadata, code availability, and figure source
  data
- final submission-readiness verdict tied to the official source and date checked

## Blocking Checks

- Do not call the manuscript submission-ready until the target journal's current official
  instructions have been checked in this run or the user explicitly accepts a dated local snapshot.
- Do not use a generic LaTeX shell as an official journal template.
- Do not omit the checklist compliance matrix for CONSORT, STROBE, PRISMA, STARD, TRIPOD,
  SPIRIT, CARE, GATHER, CHEERS, or any target-required checklist.
- Do not invent ethics approvals, registration IDs, data-sharing records, adverse events, sample
  counts, or outcomes.
- Do not invent author names, ORCID identifiers, corresponding-author email, suggested reviewers,
  permissions, prior submission history, or ICMJE authorship approval.
- Do not call data availability or FAIR status complete when repository access, controlled-access
  procedure, third-party restrictions, DataCite metadata, or figure source data remain unknown.
- Do not stop at Markdown unless the route is `generic-review` or the user explicitly asks for
  prose-only output. A complete full-draft request must produce the route-appropriate primary file.
