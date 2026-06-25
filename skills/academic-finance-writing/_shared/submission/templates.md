# Finance LaTeX Templates

Finance is guideline-driven more often than template-driven. Do not assume that every target venue
has a required `.tex` class.

Templates are format shells, not writing sources. Use them for class, package, bibliography,
title-page, disclosure, appendix, and spacing conventions; remove sample prose before drafting.
Use `skills/academic-figure/references/figure-layout.md` for figure/table width, single-column versus double-column
placement, float environment, and appendix overflow decisions.
Use the selected `_shared/version-targets/*` card and target `_shared/venues/standards/*`
card for `target_page_window`, min_pages, max_pages, count scope, and compiled page-count gates.

## Template Selection Rule

1. **Official guideline first**: load the target venue card and current official author
   instructions.
2. **Official template package second**: use a bundled official template package only when the
   publisher or target journal requires or clearly supports it.
3. **package-local shell last**: use a generic package-local shell only when no official template is
   required, and label it as a drafting shell.

When the user specifies a target journal, conference, or platform, the selected project must follow
the official venue format rather than a generic finance convention. The chosen template must carry
the venue's required class/template status, font and spacing, margins, title-page/anonymity rules,
abstract/keyword/JEL constraints, appendix/supplement placement, figure/table constraints, and
reference/citation style. If the local template cannot implement a required rule, block the format
gate or request the missing official template; do not substitute `plainnat`, an author-year shell, or
another package-local default for a venue that requires a different style.

## Available Package-Local Templates

| Template | Source type | target_page_window | Use |
|---|---|---:|---|
| `assets/templates/generic_finance_working_paper.tex` | package-local shell | 40-60 pages, field_convention_fallback | working paper, seminar draft, or neutral compiled PDF when no target journal is fixed |
| `assets/templates/aea_journal_submission.tex` | package-local shell | 35-45 pages, official_recommendation_plus_fallback_minimum | finance/economics journal draft with abstract, JEL, data-code statement, and online appendix |
| Elsevier elsarticle: `assets/templates/elsevier-elsarticle/` | official template package | 40-55 pages, field_convention_fallback unless current Elsevier/JFE source says otherwise | JFE-style Elsevier accepted-paper or source-file production when appropriate |

Venue cards and provenance:

- `_shared/venues/standards/index.md`
- `assets/templates/index.md`
- `assets/templates/source-manifest.yaml`

Before real submission, verify the current target venue's author instructions and replace the shell
with an official template when one exists. Do not call a package-local shell an official JF, RFS,
QJE, AEA, or Management Science template.

Expected compiled project:

```text
main.tex
references.bib
main.pdf
```

Do not call a draft submission-ready until the PDF compiles and the data/code, appendix, disclosure,
JEL-code, reference/citation style, template, and target_page_window requirements have been checked against
`_shared/submission/submission-standards.md`, the selected version-target card, and the selected venue card.

The page window is a hard drafting contract: below min_pages and above max_pages both block a full
draft. Do not pad, duplicate material, or invent evidence to reach min_pages; record the shortfall
as `needs_user_evidence` when supported content is unavailable.
