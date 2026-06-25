# Quarterly Journal of Economics General Instructions

Official source: https://academic.oup.com/qje/pages/Instructions_To_Authors

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use for QJE-targeted finance/economics papers or QJE-style economics-journal submissions.

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 50
  source_type: field_convention_fallback
  source_url: https://academic.oup.com/qje/pages/Instructions_To_Authors
  count_scope: complete manuscript PDF; supplementary material recorded separately
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
QJE asks authors to report total word count and gives abstract and file-shape
rules; no local hard page cap is recorded here.

## Required Shape

- title page, contributor names, correspondence address, total word count, and abstract checked
  against current QJE instructions
- abstract budget checked against current official limit
- author names and acknowledgments handled according to the current QJE route

## Template Role

No package-local QJE template is bundled. Use current QJE instructions as the authority and a neutral
economics/finance shell only when no official template is required.

## Blocking Checks

- Do not infer QJE requirements from AEA or finance-journal defaults.
- Verify whether the route expects named or anonymized manuscript materials.
- Keep word-count and abstract constraints explicit in the submission package.
