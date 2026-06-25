# Working Paper Version

Use for early circulation, seminar feedback, SSRN-style drafts, NBER/CEPR-style discussion-paper
logic, or when no target journal is fixed.

## Expected Features

- complete argument and evidence chain
- fuller tables, mechanisms, robustness, and appendix
- clear title page with authors/affiliations if not anonymous
- abstract, keywords, JEL codes
- data/code statement if replication is discussed
- transparent limitations and version date

## Page Window

```yaml
target_page_window:
  min_pages: 40
  max_pages: 60
  source_type: field_convention_fallback
  source_url: _shared/version-targets/working-paper.md
  count_scope: main PDF including references, tables, figures, and internal appendix; online appendix recorded separately
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
Do not mark a working paper complete until the compiled PDF is inside this
window unless the user sets a different page window explicitly.

## Risk

Do not treat working-paper circulation as journal acceptance or external validation.
