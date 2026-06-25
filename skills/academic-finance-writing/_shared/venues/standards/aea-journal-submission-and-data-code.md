# AEA Journal Submission And Data-Code Policy

Official source: https://www.aeaweb.org/journals/policies

Additional official source: https://www.aeaweb.org/journals/data/data-code-policy

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use for AER, AER: Insights, AEJ journals, JEP/JEL where applicable, or economics-journal routes
whose data/code expectations follow AEA policy.

## Page Window

```yaml
target_page_window:
  min_pages: 35
  max_pages: 45
  source_type: official_recommendation_plus_fallback_minimum
  source_url: https://www.aeaweb.org/journals/aer/submissions
  count_scope: manuscript including figures, tables, references, and appendices
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
AEA/AER guidance strongly recommends a 40-page equivalent with 11-point,
1.5-spacing or 45-page equivalent with 12-point, 1.5-spacing; the minimum is a field convention.

## Required Shape

- data and code availability statement
- data legality and acquisition boundary
- disclosure statement even when there is nothing to disclose
- replication package plan for empirical, simulation, or experimental work before acceptance
- RCT registry treatment when field experiments are involved

## Template Role

No package-local AEA journal class is bundled. The local AEA-style shell is only a finance/economics
journal draft shell, not an official AEA template.

## Blocking Checks

- Do not claim AEA data-code compliance without a replication package map and access boundary.
- Do not invent repository URLs, data permissions, or disclosure facts.
- Check journal-specific AEA instructions in addition to the general policy.
