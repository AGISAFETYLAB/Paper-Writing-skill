# Finance Conferences And Working-Paper Platforms

Official source: https://afajof.org/annual-meeting/

Additional official sources:

- https://westernfinance.org/submit-a-paper/
- https://efa2026.efa-finance.org/submission/
- https://sfs.org/sfs-cavalcade-north-america-2026/
- https://www.fma.org/tampa
- https://www.elsevier.support/ssrn/answer/get-started
- https://www.nber.org/nber-help-working-papers-general-information
- https://cepr.org/publications/discussion-papers

Source snapshot checked: 2026-06-22. Re-check current calls before real submission.

## Applicability

Use for AFA, WFA, EFA, SFS Cavalcade, FMA, SSRN, NBER, CEPR, or similar finance working-paper
circulation and conference-submission routes.

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 45
  source_type: field_convention_fallback until the current call or platform page overrides it
  source_url: _shared/venues/standards/finance-conferences-and-working-paper-platforms.md
  count_scope: submission PDF or working-paper PDF as defined by the current call/platform
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
For conference submissions, the current-year call overrides this fallback. For
SSRN/NBER/CEPR circulation, use the working-paper window when no call-specific page cap exists.

## Required Shape

- conference year/call, deadline, membership or fee constraints, PDF format, anonymity, and author
  limits checked against the current call
- SSRN treated as preprint/working-paper posting, not journal submission
- NBER and CEPR treated as selective working-paper series, not generic open-upload templates

## Template Role

No conference-specific LaTeX template is bundled. Conference submissions usually use a working-paper
PDF and current-year call requirements.

## Blocking Checks

- Do not treat conference acceptance as journal acceptance or publication formatting.
- Do not assume anonymity: AFA/WFA/EFA/SFS/FMA rules differ by year and venue.
- Do not present NBER or CEPR as ordinary open submission routes without verifying eligibility.
