# Econometrica Information For Authors

Official source: https://www.econometricsociety.org/publications/econometrica/information-authors

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use for Econometrica-targeted theory, econometrics, financial economics, or high-identification
empirical submissions.

## Page Window

```yaml
target_page_window:
  min_pages: 20
  max_pages: 30
  source_type: official_recommendation
  source_url: https://www.econometricsociety.org/publications/statement-editors-econometrica-quantitative-economics-and-theoretical-economics
  count_scope: main paper, with online appendices minimized and recorded separately
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
The Econometric Society editors state they are not imposing an overall page
limit, but they encourage authors to aim for a 20-30 page paper instead of 30-40 pages.

## Required Shape

- Econometric Society submission instructions checked
- membership/submission route handled when relevant
- supplemental material, data editor, replication policy, and LaTeX support checked where relevant
- theory papers must plan proof placement and supplemental material carefully

## Template Role

No package-local Econometric Society template is bundled. If the current official page requires or
offers LaTeX support, use the official source rather than a package-local shell.

## Blocking Checks

- Do not claim Econometrica fit from method complexity alone.
- Check data editor and replication policy for empirical or computational papers.
- Do not infer final publication formatting from initial submission guidance.
