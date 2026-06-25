# Medicine Templates

Available package-local templates and shells:

- `assets/templates/word/generic-medical-word-reference.docx`
- `assets/templates/word/bmj-case-reports/bmj-clinical-case-report-template.docx`
- `assets/templates/word/bmj-case-reports/bmj-global-health-case-report-template.docx`
- `assets/templates/word/bmj-case-reports/bmj-images-in-template.docx`
- `assets/templates/word/index.md`
- `assets/templates/generic_medical_article.tex`
- `assets/templates/jama_original_investigation.tex` (optional review shell only for JAMA-style work)
- `assets/templates/cover_letter_template.md`
- `assets/templates/springer-nature-latex/sn-article-template/sn-article.tex`
- `assets/templates/springer-nature-latex/sn-article-template/sn-jnl.cls`
- `assets/templates/springer-nature-latex/sn-article-template/sn-bibliography.bib`
- `assets/templates/springer-nature-latex/sn-article-template/user-manual.pdf`
- `assets/templates/index.md`
- `assets/templates/source-manifest.yaml`

Use the generic template only for early review drafts or unspecified venues that need a PDF preview.
For JAMA-style Original Investigation, the default route is `word-first`: produce
`paper/manuscript.docx` as the primary submission file. Use the JAMA-style LaTeX shell only as an
optional review artifact, not as the official submission template. Use the Springer Nature journal
article template for Nature Portfolio / Springer Nature LaTeX submissions when appropriate; this is
an official downloaded template package and must be copied with its class and bibliography companion
files.

Medical writing is not template-first. Choose the target journal/article type and reporting
checklist first, then select a template that fits the confirmed submission route. The template is a
format shell only; it must not contribute sample body prose, sample claims, sample file names, or
unverified reference text to the manuscript.

The generic and JAMA-style LaTeX files are compile-ready review artifacts, not official journal class
files. The generic Word DOCX is a package-local generic Word reference shell, not an official Word
template. Before real submission, verify the current target journal's author instructions and replace
a shell with an official template if the journal provides one.

The cover letter template is a package-local shell. Use it to draft `paper/cover-letter.md`, but do
not invent author approval, ORCID, conflicts, suggested reviewers, permissions, or previous
submission history.

## Length Budget Selection

Always resolve `target_length_budget` before drafting. Source priority is:

1. current official target-journal author instructions,
2. selected journal standard card under `_shared/journal-standards/`,
3. official template text, such as a bundled BMJ Case Reports DOCX,
4. Generic Medical Length Fallbacks below when no official length rule is available.

Official word/display/reference limits override fallback page or word windows. Fallback values are
completion contracts for the skill, not journal claims. Do not pad with unsupported background or
duplicated caveats to hit a lower bound; mark the draft length gate blocked if evidence is missing.

## Generic Medical Length Fallbacks

Use these only when no current official journal or article-type source gives a usable length rule.

```yaml
target_length_budget:
  generic_observational_cohort:
    length_unit: words
    min_words: 2500
    max_words: 3500
    fallback_pages: 8-12
    source_type: field_convention_fallback
    count_scope: main text; exclude abstract, tables, figures, references, statements, and supplement
  generic_rct_or_intervention:
    length_unit: words
    min_words: 2500
    max_words: 3500
    fallback_pages: 8-12
    source_type: field_convention_fallback
  generic_systematic_review:
    length_unit: words
    min_words: 3000
    max_words: 4500
    fallback_pages: 10-14
    source_type: field_convention_fallback
  generic_diagnostic_or_prediction:
    length_unit: words
    min_words: 2500
    max_words: 3500
    fallback_pages: 8-12
    source_type: field_convention_fallback
  generic_health_economics:
    length_unit: words
    min_words: 3000
    max_words: 4000
    fallback_pages: 10-14
    source_type: field_convention_fallback
  generic_case_report:
    length_unit: words
    min_words: 1200
    max_words: 2000
    fallback_pages: 5-8
    source_type: field_convention_fallback
  generic_research_letter:
    length_unit: words
    min_words: 600
    max_words: 800
    fallback_pages: 2-4
    source_type: field_convention_fallback
  generic_narrative_review_or_perspective:
    length_unit: words
    min_words: 3000
    max_words: 4500
    fallback_pages: 10-15
    source_type: field_convention_fallback
```

## Selection Rules

1. Named Nature Portfolio / Springer Nature target with TeX/LaTeX allowed -> use
   `springer-nature-latex/sn-article-template/sn-article.tex` and `sn-jnl.cls`; select `sn-nature`
   or the target-required bibliography style. Load the Nature Medicine journal standard card for
   `target_length_budget` when the target is Nature Medicine; otherwise use the target journal's
   current official content-type rules. Use the `iicol` class option only when the user or journal
   needs a two-column review/production-style preview. Initial-submission review PDFs may be
   single-column unless the official instructions or user request says otherwise.
2. JAMA-style Original Investigation -> use `word-first` with `paper/manuscript.docx` as the primary
   submission file. If `jama_original_investigation.tex` is used for an optional PDF preview, record
   "instruction-derived review shell, not official JAMA class" in `paper/submission-package.md`.
   JAMA/JAMA-style routes must not claim an official Word template; use the official JAMA-family
   author instructions plus the JAMA journal standard card's `target_length_budget` and
   `assets/templates/word/generic-medical-word-reference.docx` unless the user supplies a valid
   official/current Word template.
3. BMJ Case Reports -> use the matching preloaded official Word template under
   `assets/templates/word/bmj-case-reports/` when the confirmed article route is clinical case
   report, global health case report, or Images In. Load `_shared/journal-standards/bmj-case-reports.md`
   for the active article-type `target_length_budget`. Do not use a BMJ case-report template for
   JAMA, BMC, cohort Original Investigation, trial, or review manuscripts.
4. Word-first target with no local official Word template -> acquire in this order:
   preloaded official Word template -> user-provided official template -> official web fetch ->
   package-local generic Word reference shell. Use `skills/academic-writing/scripts/fetch_medical_word_templates.py` for
   allowlisted official web fetches. If the fetch fails, record `download-blocked`, `not-found`, or
   the exact failure in `paper/submission-package.md`; do not call the generic reference shell
   official.
5. Unspecified medical target -> use `generic-review`; choose the closest Generic Medical Length
   Fallback as the active `target_length_budget`; generate `generic_medical_article.tex` only if a
   preview PDF is requested.
6. Named target with no local official template -> use a user-provided template or fetch official
   author instructions/template source; report if only a shell is available.

Route-specific expected project:

```text
word-first:
  manuscript.docx
  manuscript.md
  references.bib
  title-page.md
  cover-letter.md
  editorial-system-checklist.md
  submission-package.md

latex-first:
  main.tex
  references.bib
  main.pdf
  title-page.md
  cover-letter.md
  editorial-system-checklist.md
  submission-package.md
```

Do not call a draft submission-ready until the route-specific production gate passes and the
checklist compliance matrix has been checked against `_shared/submission/submission-standards.md`.

## Display Layout Rules

- Do not force every figure to full text width. Match width to the evidence role.
- In a two-column layout, simple plots and compact tables use `figure`/`table` with
  `\columnwidth` or smaller.
- Complex flow diagrams, multi-panel outcome plots, forest plots with long labels, calibration plus
  decision-curve panels, and wide clinical tables use `figure*`/`table*` with `\textwidth`.
- Outcome and harms tables must reserve enough width for effect estimates, uncertainty intervals,
  definitions, and interpretation notes. Do not use equal-width `X` columns when the effect column
  becomes the narrowest column.
- Flush or barrier Results floats before Discussion when double-column floats would otherwise drift
  after interpretive text.
