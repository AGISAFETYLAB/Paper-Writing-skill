# Management Science Submission Guidelines

Official source: https://pubsonline.informs.org/page/mnsc/submission-guidelines

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use for Management Science finance, fintech, operations-finance, platform, risk, or empirical
management submissions.

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 45
  source_type: field_convention_fallback
  source_url: https://pubsonline.informs.org/page/mnsc/submission-guidelines
  count_scope: initial anonymous manuscript PDF; electronic companions excluded
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
Initial submissions have no official hard page limit, but excessive length can
still be rejected. For invited revisions, replace this with the official limit: 40-47 pages
double-spaced or 28-32 pages at 1.5 spacing, excluding online appendix/electronic companions.

## Required Shape

- department fit, manuscript type, abstract, keywords, anonymous files, author metadata, and reviewer
  suggestions handled under the current ScholarOne submission process
- electronic companions and supplemental materials planned when proofs, robustness, data analysis,
  or disclosed data exceed the main text
- data disclosure plan recorded for empirical manuscripts

## Template Role

No package-local Management Science template is bundled. Use official INFORMS instructions and a
neutral finance/economics journal shell unless the user provides an official template.

## Blocking Checks

- Do not treat finance-conference acceptance as journal compliance.
- Check data/code disclosure and electronic companion requirements.
- Do not upload or expose confidential manuscript content to external tools during review checks.
