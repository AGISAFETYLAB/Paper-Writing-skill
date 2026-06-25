# Journal of Finance Initial Submission Standard

Official source: https://afajof.org/submissions/

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use when the target is the Journal of Finance or when the user asks for a JF-style finance journal
submission package.

## Page Window

```yaml
target_page_window:
  min_pages: 45
  max_pages: 60
  source_type: official_max_plus_fallback_minimum
  source_url: https://afajof.org/submissions/
  count_scope: manuscript PDF including internal appendices, reference lists, figures, and tables; Internet Appendix excluded from the 60-page cap
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
The 60-page ceiling is official; the minimum is a finance field convention for
a complete journal-style draft.

## Required Shape

- title page at the beginning of the manuscript
- author-named conflict-of-interest disclosure statement immediately after the title page
- abstract not over the current official limit
- page-limit, spacing, font, and margin checks against official instructions
- Internet Appendix placed at the end of the same PDF when used and clearly labeled
- code-sharing plan for accepted-paper stage
- compiled PDF and source TeX
- AI-use disclosure and prompt/model documentation when applicable under current JF policy

## Blocking Checks

- Confirm whether the paper is initial submission, resubmission, or final accepted version.
- Include disclosure even when there is nothing to disclose.
- Keep the main paper self-contained; the Internet Appendix cannot carry essential logic.
- Do not mark as JF-ready without page-count, abstract, spacing, disclosure, AI-use, and
  appendix-placement checks.
