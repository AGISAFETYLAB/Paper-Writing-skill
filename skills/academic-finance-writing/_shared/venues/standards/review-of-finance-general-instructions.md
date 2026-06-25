# Review of Finance General Instructions

Official source: https://academic.oup.com/rof/pages/General_Instructions

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use when the target is Review of Finance or a European Finance Association journal route.

## Page Window

```yaml
target_page_window:
  min_pages: 40
  max_pages: 60
  source_type: official_max_plus_fallback_minimum
  source_url: https://academic.oup.com/rof/pages/General_Instructions
  count_scope: manuscript PDF including appendices, bibliographies, figures, and tables; Internet Appendix excluded
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
The 60-page ceiling is official and is an extreme upper limit; the minimum is a
field convention for a complete finance journal draft.

## Required Shape

- current OUP/Review of Finance instructions checked
- manuscript, abstract, references, supplemental material, ethics/authorship, and data-code
  expectations handled under current instructions
- standard review route versus fast-track route identified when relevant

## Template Role

No package-local Review of Finance template is bundled. Use official instructions first, then a
neutral finance journal shell if no official template is required.

## Blocking Checks

- Do not infer Review of Finance constraints from RFS or JF.
- Record whether the route is normal review or fast-track if the user asks about submission process.
- Re-check OUP instructions before submission-ready wording.
