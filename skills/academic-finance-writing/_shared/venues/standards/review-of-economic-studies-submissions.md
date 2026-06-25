# Review of Economic Studies Submissions

Official source: https://www.restud.com/submissions/

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use for Review of Economic Studies-targeted finance/economics papers, especially theory,
identification-heavy empirical work, or macro-finance work.

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 45
  source_type: official_max_plus_fallback_minimum
  source_url: https://www.restud.com/submissions/
  count_scope: manuscript PDF including title page, tables, figures, references, and appendices; online appendix capped separately
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
The 45-page ceiling and 30-page online appendix cap are official; the minimum is
a field convention for a complete economics/finance submission.

## Required Shape

- REStud submission guidelines and Editorial Express route checked
- current data availability policy checked for empirical or computational work
- revision policy and resubmission restrictions checked before R&R wording

## Template Role

No package-local REStud template is bundled. Use official REStud/OUP instructions and a neutral
finance/economics shell only when no official template is required.

## Blocking Checks

- Do not infer REStud limits from QJE, AEA, or finance-journal rules.
- Check data availability policy before any submission-ready claim.
- Do not describe a rejected manuscript as resubmittable unless explicitly invited by an editor.
