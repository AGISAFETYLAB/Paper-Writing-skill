# BMJ Case Reports Article-Type Standard

Official source: https://casereports.bmj.com/pages/authors

Official template sources:

- https://casereports.bmj.com/casereports/wp-content/uploads/sites/64/2023/06/Clinical-Case-Report-template-2023-word.docx
- https://casereports.bmj.com/casereports/wp-content/uploads/sites/64/2023/06/Global-Health-Case-Report-template-2023-word.docx
- https://casereports.bmj.com/casereports/wp-content/uploads/sites/64/2023/06/Images-in-template-2023-word.docx

Source snapshot checked: 2026-06-23. Re-check before real submission.

## Applicability

Use for BMJ Case Reports clinical case report, global health case report, and Images In routes when
the user names BMJ Case Reports or supplies one of the official BMJ Case Reports Word templates.

## Required Shape

- `word-first` route using the matching official BMJ Case Reports Word template.
- CARE-oriented case-report evidence boundary unless the confirmed route supplies a stricter BMJ
  checklist.
- Signed patient consent and author statements are required before submission-ready wording.
- Images and videos must be de-identified and uploaded/handled according to BMJ Case Reports
  instructions.

## Length And Display Limits

BMJ Case Reports uses article-type word limits and template instructions rather than a single page
limit. If the current official author page gives a stricter value, use it and record the URL/date.

```yaml
target_length_budget:
  clinical_case_report:
    source_type: official_author_page_or_template
    length_unit: words
    summary_words:
      max_words: 150
      source_type: official_template
    main_text_words:
      min_words: 1200
      max_words: 2000
      min_source_type: field_convention_completion_floor
      max_source_type: official_recommended_maximum
    display_items:
      max_items: not_specified
      source_type: official_author_page_or_template
      rule: no fixed figure count is recorded locally; choose only displays that teach the case
    page_limit:
      status: not_specified
      fallback_pages: 5-8
      fallback_source_type: field_convention_fallback
  global_health_case_report:
    source_type: official_author_page_or_template
    length_unit: words
    summary_words:
      max_words: 150
      source_type: official_template
    main_text_words:
      min_words: 1200
      max_words: 2000
      min_source_type: field_convention_completion_floor
      max_source_type: official_recommended_maximum
    display_items:
      max_items: not_specified
      source_type: official_author_page_or_template
    page_limit:
      status: not_specified
      fallback_pages: 5-8
      fallback_source_type: field_convention_fallback
  images_in:
    source_type: official_template
    length_unit: words
    description_words:
      min_words: 350
      max_words: 500
      min_source_type: field_convention_completion_floor
      max_source_type: official_template_maximum
    display_items:
      max_items: not_specified
      source_type: official_author_page_or_template
    page_limit:
      status: not_specified
      fallback_pages: 2-4
      fallback_source_type: field_convention_fallback
```

## Submission Format

- Default route: `word-first`.
- Primary submission file: `manuscript.docx` created from the matching official BMJ Case Reports
  Word template.
- Do not convert BMJ Case Reports to a generic LaTeX/PDF route unless the user only wants a review
  preview and the package labels it as non-submission-ready.

## Blocking Checks

- Confirm the BMJ Case Reports article type: clinical case report, global health case report, or
  Images In.
- Use the active `target_length_budget` for the chosen article type.
- Check patient consent, author statements, de-identification, image permissions, and CARE-style
  evidence completeness before submission-ready wording.
