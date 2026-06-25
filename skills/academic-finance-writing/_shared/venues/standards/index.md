# Finance Venue Standards Index

Use these cards after version target and target venue are known, or during a final
submission-readiness check. They are dated constraint cards, not prose sources and not substitutes
for checking the current official page before real submission.

## Selection Rule

1. Use a target-specific card when one exists.
2. If the exact venue is absent, use the closest venue-family card only for planning and mark the
   fit as approximate.
3. When the user names a target journal, conference, or platform, the venue's current official author
   instructions become the controlling format standard. Generic finance defaults are allowed only
   when no venue is named, or when the official source explicitly leaves a format choice open.
4. Record `target_page_window`, min_pages, max_pages, source type, and count scope from the selected
   version-target card and this venue card in the Paper Framework.
5. Record the official format source, template route, citation/reference style, anonymity/title-page
   handling, appendix/supplement handling, figure/table constraints, and data-code policy in the
   Paper Framework and `paper/submission-package.md`.
6. For conferences and working-paper platforms, use the platform card and the current year call or
   upload instructions.

## Supported Cards

The final row is the finance conferences and working-paper platforms card; use it for circulation
routes rather than journal submission formatting.

| Venue family | Card |
|---|---|
| Journal of Finance | `journal-of-finance-initial-submission.md` |
| Journal of Financial Economics | `journal-of-financial-economics-initial-submission.md` |
| Review of Financial Studies | `review-of-financial-studies-general-instructions.md` |
| Journal of Financial and Quantitative Analysis | `journal-of-financial-and-quantitative-analysis-author-instructions.md` |
| Review of Finance | `review-of-finance-general-instructions.md` |
| Management Science | `management-science-submission-guidelines.md` |
| AEA journals | `aea-journal-submission-and-data-code.md` |
| Quarterly Journal of Economics | `quarterly-journal-of-economics-general-instructions.md` |
| Econometrica | `econometrica-information-for-authors.md` |
| Review of Economic Studies | `review-of-economic-studies-submissions.md` |
| AFA, WFA, EFA, SFS Cavalcade, FMA, SSRN, NBER, CEPR | `finance-conferences-and-working-paper-platforms.md` |

## Global Blocking Rule

Do not call a manuscript submission-ready unless the exact target venue, version target, official
source URL, date checked, `target_page_window`, actual compiled PDF page count, and page-window
verdict are recorded in `paper/submission-package.md`.

If a target venue is specified, also do not call the manuscript target-compliant unless the compiled
project uses the venue-required format. This includes the required template or class when mandated,
font and spacing, margin rules, title page/anonymity handling, abstract/keyword/JEL constraints,
appendix/supplement placement, reference/citation style, figure/table constraints, and data/code
policy. If any item is unknown, unchecked, unsupported by the local template, or intentionally
provisional, record `format_compliance_status: blocked` or `partial`; do not silently fall back to a
generic working-paper shell.
