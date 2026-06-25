# Medicine Template Index

Use package-local templates first. Source status is recorded in `source-manifest.yaml`. The package
contains instruction-derived shells, one official downloaded LaTeX template package, and a
package-local generic Word reference shell for Word-first routes.

| Target | Template | target_length_budget | Use |
|---|---|---|---|
| BMJ Case Reports Word templates | `word/bmj-case-reports/*.docx` | Official/template budget from `_shared/journal-standards/bmj-case-reports.md`: clinical/global health 1200-2000 main words plus 150-word summary; Images In 350-500 words | Official BMJ Case Reports Word templates for clinical case report, global health case report, and Images In routes |
| generic medical Word-first manuscript | `word/generic-medical-word-reference.docx` | Generic Medical Length Fallback from `_shared/submission/templates.md`, usually 2500-3500 main words for original research or 1200-2000 for case report | Fallback reference DOCX for editable Word manuscripts when no valid official Word template or user-provided template is available; package-local generic Word reference shell, not an official Word template |
| generic medical draft | `generic_medical_article.tex` | Generic Medical Length Fallback from `_shared/submission/templates.md`, usually 2500-3500 main words or 8-12 review pages for original research | Unspecified medical journal or early draft PDF; package-local shell, not official |
| JAMA-style Original Investigation | `jama_original_investigation.tex` | JAMA journal-standard budget: 2500-3000 main words, 5 displays, 50-75 references; no page limit recorded | Optional PDF review shell for structured abstract, Key Points, article information, statements, and checklist appendix; instruction-derived shell, not official, not the primary Word-first submission template |
| Springer Nature journal article template | `springer-nature-latex/sn-article-template/sn-article.tex` + `sn-jnl.cls` | Target Nature/Springer content-type budget; Nature Medicine Article/Resource/Analysis use 3200-4000 main words and 6 displays | Nature Portfolio / Springer Nature LaTeX source when a journal accepts TeX/LaTeX; official downloaded template package |
| medical cover letter | `cover_letter_template.md` | n/a | Generic editor-facing cover letter shell; all author, ORCID, approval, conflict, suggested reviewer, and previous submission facts must be author-provided |

Before real submission, verify the current target-journal author instructions. A package-local shell
must not be called an official journal template. The Springer Nature directory is the official
downloaded template; preserve its class and companion files when using it.

For JAMA/JAMA-style targets, the primary submission file is normally `manuscript.docx`; this directory
does not contain an official JAMA Word template. JAMA/JAMA-style routes must not claim an official
Word template; use official author instructions plus the package-local Word reference shell unless
the user supplies a valid official Word template.

For Word-first routes, acquire templates in this order:
preloaded official Word template -> user-provided official template -> official web fetch ->
package-local generic Word reference shell. If official web fetch is blocked, record
`download-blocked` and continue only with a clearly labeled generic reference shell.

Use `skills/academic-writing/scripts/fetch_medical_word_templates.py` to stage official Word template downloads and validate
DOCX package structure before adding them under `assets/templates/word/`.

Template files are shells. Remove sample body text, placeholder claims, and template bibliography
sample prose before drafting. Manuscript body text must not mention internal local file names,
generator scripts, source paths, or package provenance unless the user explicitly asks for an
engineering/test report.

Every manuscript-producing template selection must carry a `target_length_budget` from the selected
journal standard card, official template text, current official author instructions, or the Generic Medical
Length Fallbacks in `_shared/submission/templates.md`.

Required companion files for Springer Nature:

- `springer-nature-latex/sn-article-template/sn-article.tex`
- `springer-nature-latex/sn-article-template/sn-jnl.cls`
- `springer-nature-latex/sn-article-template/sn-bibliography.bib`
- `springer-nature-latex/sn-article-template/user-manual.pdf`

Springer Nature layout note: `sn-jnl.cls` supports single-column and `iicol` two-column layouts.
Use `iicol` for a two-column preview only when requested or journal-appropriate; do not assume every
medical initial submission must be two-column.
