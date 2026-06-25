# Conference Submission Version

Use for finance conference submissions and annual-meeting calls.

## Required Checks

- current call for papers / submission page
- anonymous PDF requirements
- abstract, keywords, JEL codes
- author information separation
- page/word limits if stated
- working-paper version conflict with anonymity
- discussant or presentation materials only after acceptance

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 45
  source_type: field_convention_fallback until the current call for papers overrides it
  source_url: _shared/version-targets/conference-submission.md
  count_scope: conference submission PDF as defined by the current call
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
If the current CFP gives a page or word limit, replace this fallback with the
official CFP rule and record the URL/date checked.

## Risk

Conference submission is usually not final publication formatting. Do not replace journal manuscript
planning with conference formatting.
