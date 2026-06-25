# Journal Submission Version

Use when preparing for a named journal or submission-ready package.

## Required Checks

- target journal manuscript guidelines
- title page vs anonymous manuscript handling
- abstract, keywords, JEL codes
- main manuscript length, tables/figures, references
- Internet appendix or supplemental materials
- data/code availability and replication policy
- disclosures, conflicts, funding, acknowledgements
- submission attachment status for title page, anonymity, conflict-of-interest disclosure, funding,
  and acknowledgements
- visual asset QA, compiled layout QA, and manual contact-sheet inspection status
- central-result uncertainty status for headline estimates, alphas, spreads, and event-window
  contrasts
- cover letter if requested

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 50
  source_type: field_convention_fallback until a target venue card or current official source overrides it
  source_url: _shared/version-targets/journal-submission.md
  count_scope: main manuscript PDF including references, tables, figures, and internal appendix
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
A target venue card or current official instruction overrides this generic
fallback, but the manuscript must still have both min_pages and max_pages before drafting.

## Risk

Do not claim compliance with a specific journal unless the current author instructions have been
checked.
