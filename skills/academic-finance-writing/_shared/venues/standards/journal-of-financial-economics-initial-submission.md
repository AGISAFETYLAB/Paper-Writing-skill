# Journal of Financial Economics Initial Submission Standard

Official source: https://www.jfinec.com/submissions

Additional official source: https://www.sciencedirect.com/journal/journal-of-financial-economics/publish/guide-for-authors

Source snapshot checked: 2026-06-24. Re-check before real submission.

## Applicability

Use when the target is Journal of Financial Economics or a JFE-style Elsevier finance submission.

## Page Window

```yaml
target_page_window:
  min_pages: 40
  max_pages: 55
  source_type: field_convention_fallback
  source_url: https://www.jfinec.com/submissions
  count_scope: anonymous main manuscript PDF; clearly marked online appendix pages recorded separately
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
The official JFE page gives formatting and anonymity rules but no local hard
main-paper page cap, so this window is a finance field convention fallback.

## Required Shape

- anonymous manuscript PDF for initial submission
- title and short abstract
- double-spaced manuscript with 12-point or larger font and one-inch minimum margins
- online appendix attached to the end of the main manuscript PDF when included
- separate conflict-of-interest disclosure PDF
- separate title page with author identifying information
- no supplementary-material upload for ordinary submissions; attach extra material to the manuscript
  PDF when allowed
- final accepted manuscript path can switch to Elsevier elsarticle style

## Reference And Citation Style

Use the current JFE / Elsevier Guide for Authors when the target is Journal of Financial Economics.
The checked guide requires numbered in-text references in square brackets, references numbered in
the order they appear in the article, journal-name abbreviations according to LTWA, and DOI links
where available. Do not use a finance author-year default for a JFE-targeted submission unless the
current official instructions have changed or the user explicitly requests a non-compliant working
draft.

Record in `paper/submission-package.md`:

```yaml
citation_reference_style: numbered square-bracket citations; references ordered by first appearance
citation_reference_source_url: https://www.sciencedirect.com/journal/journal-of-financial-economics/publish/guide-for-authors
format_compliance_status: pass | partial | blocked
```

## Blocking Checks

- Strip author information and acknowledgments from the initial manuscript PDF.
- Keep the online appendix anonymous for initial submission.
- Do not submit the same manuscript elsewhere while JFE is considering it.
- Do not use final production formatting as a substitute for initial-submission anonymity rules.
- Do not leave `plainnat` author-year references in a strict JFE-targeted submission when the current
  Guide for Authors requires numbered references.
- For accepted-paper production, switch to the official Elsevier elsarticle template package when
  appropriate.
