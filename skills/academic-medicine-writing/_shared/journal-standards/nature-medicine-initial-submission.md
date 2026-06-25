# Nature Medicine Initial Submission Standard

Official source: https://www.nature.com/nm/submission-guidelines/initial-formatting
Content-type source: https://www.nature.com/nm/content

Source snapshot checked: 2026-06-23. Re-check before real submission.

## Applicability

Use when the target is Nature Medicine or a Nature-family medical journal and the user needs an
initial submission manuscript rather than accepted-paper production formatting.

## Required Shape

- complete manuscript suitable for editorial assessment and peer review
- compiled PDF when the source is TeX/LaTeX
- readable methods, figures, Extended Data or Supplementary Information plan where applicable
- cover-letter and policy-material checklist when requested by the target journal
- clinical/statistical reporting checklist when required by study design
- no assumption that the initial submission must use a two-column production layout unless the
  current instructions or user explicitly require it

## Length And Content-Type Limits

Nature Medicine specifies length primarily by article content type, usually in words, display items,
and reference guidance rather than a universal page limit. Choose the confirmed content type first.

```yaml
target_length_budget:
  Nature Medicine Article:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 4000
    target_min_words: 3200
    target_min_source_type: field_convention_completion_floor
    abstract_words: 150
    display_items: 6
    references: 60
    page_limit: not_specified
  Nature Medicine Resource:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 4000
    target_min_words: 3200
    abstract_words: 150
    display_items: 6
    references: 60
    page_limit: not_specified
  Nature Medicine Analysis:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 4000
    target_min_words: 3200
    abstract_words: 150
    display_items: 6
    references: 60
    page_limit: not_specified
  Nature Medicine Brief Communication:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 2000
    target_min_words: 1600
    abstract_words: 150
    display_items: 2
    references: 20
    page_limit: official_page_limit_referenced_but_numeric_page_count_not_recorded_locally
  Nature Medicine Correspondence:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 1000
    target_min_words: 700
    display_items: 2
    references: 10
    page_limit: not_specified
  Nature Medicine Review:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 4000
    target_min_words: 3200
    references: 100
    page_limit: not_specified
  Nature Medicine Perspective:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 4000
    target_min_words: 3200
    references: 100
    page_limit: not_specified
  Nature Medicine Comment:
    source_type: official_current_snapshot
    length_unit: words
    main_text_words: 1500-2000
    target_min_words: 1500
    references: 15
    page_limit: not_specified
```

For official maximum-only word limits, the `target_min_words` value is a completion floor used by
the skill so full drafts are not underdeveloped; it is not an official journal minimum.

## Blocking Checks

- Confirm that Nature Medicine is the target journal and that the content type is accepted.
- Confirm the active `target_length_budget` before drafting; if the content type is unresolved, use
  Nature Medicine Article/Resource/Analysis only as a provisional planning route and list the
  unresolved content type as a blocker.
- Do not overfit to final production formatting during initial submission unless the journal asks.
- If LaTeX is used, provide the compiled PDF alongside source files.
- Keep checklist, ethics, registration, data, conflicts, and funding statements explicit.
