# Finance Template Index

Use the selection order below. Source status is recorded in `source-manifest.yaml`.

1. **Official guideline first**: venue card plus current official author instructions.
2. **Official template package second**: publisher template when actually required or appropriate.
3. **package-local shell last**: generic or AEA-style shell only when no official template is required.

| Target | Template | target_page_window | Use |
|---|---|---:|---|
| generic finance working paper | `generic_finance_working_paper.tex` | 40-60 pages | Unspecified finance working paper or early draft PDF |
| AEA-style journal submission | `aea_journal_submission.tex` | 35-45 pages | Submission-style finance/economics article with abstract, JEL codes, data-code statement, references, and online appendix |
| Elsevier elsarticle | `elsevier-elsarticle/` | 40-55 pages unless the current target source says otherwise | Official Elsevier template package for JFE-style accepted-paper or source-file production when appropriate |

Before real submission, verify the current target-journal author instructions and replace the shell
with an official template if the journal provides one.

Every template selection must carry `target_page_window`, `min_pages`, `max_pages`, `source_type`,
and `count_scope` from the selected version-target card, selected venue card, or a current official
source.
