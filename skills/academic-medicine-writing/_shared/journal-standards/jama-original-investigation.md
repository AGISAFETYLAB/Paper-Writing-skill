# JAMA-Style Original Investigation Standard

Official source: https://jamanetwork.com/journals/jamanetworkopen/pages/instructions-for-authors

Source snapshot checked: 2026-06-25. Re-check before real submission.

## Applicability

Use for JAMA Network Open or JAMA-style reports of original clinical, public-health,
observational, trial, diagnostic, or health-economics data when the user wants a submitter-facing
medical manuscript.

## Required Shape

- structured abstract
- 3 Key Points: Question, Findings, Meaning
- IMRaD body with article-type-specific Methods detail
- Data Sharing Statement where required
- reporting guideline matched to design: STROBE, CONSORT, PRISMA, STARD, TRIPOD, CHEERS, or other
  target-required guideline
- statements for ethics/consent, trial registration, conflicts, funding, author contributions, and
  data/code availability
- `word-first` manuscript package with `manuscript.docx` as the primary submission file unless the
  current official instructions or user-provided template say otherwise

## JAMA Front-Matter Component Rules

- For reports other than clinical trials and meta-analyses, do not include study type or design in
  the title or subtitle. Use a design subtitle only when the current JAMA instructions require it
  for clinical trials or meta-analyses; otherwise keep design in the abstract Design heading.
- Key Points must use exactly `Question`, `Findings`, and `Meaning`.
- For research articles, the total Key Points text should stay within the JAMA-style 75-100 word
  window. If the target journal's current official page changes this budget, follow the official
  page and record the date checked.
- Findings should focus on the primary outcome and the study population. Do not overload Findings
  with p values, odds ratios, confidence intervals, detailed model caveats, or secondary outcomes;
  put those in the Abstract Results or main Results instead.
- For JAMA-style original data reports, draft the abstract with separate headings when source
  evidence supports them: `Importance`, `Objective`, `Design`, `Setting`, `Participants`,
  `Exposure` or `Interventions`, `Main Outcomes and Measures`, `Results`, and `Conclusions and
  Relevance`. Do not collapse Design, Setting, and Participants when the separate fields are known.
- Design must state the study type, study years or source dates, and follow-up window when
  source-supported. Setting must state the clinical/data environment. Participants must state the
  disease or eligibility frame, selection method, and follow-up completion. If any are absent, mark
  the JAMA component audit as `BLOCKED` for real submission rather than hiding the gap in a combined
  heading.
- A fixture-derived, deterministic, placeholder, or otherwise non-fitted adjusted estimate must not
  appear as a main claim, main Table 2 column, or main figure row. Move it to a supplement/provenance
  table or omit it from the manuscript. The JAMA component audit blocks a main display that contains
  a fixture-derived adjusted estimate even when the caveat is worded clearly.

## Length And Display Limits

These are dated local-snapshot constraints, not a substitute for a fresh pre-submission check.

- Structured budget:

```yaml
target_length_budget:
  source_type: official_current_snapshot
  source_url: https://jamanetwork.com/journals/jamanetworkopen/pages/instructions-for-authors
  length_unit: words
  main_text_words:
    min_words: 2500
    max_words: 3000
    min_source_type: field_convention_completion_floor
    max_source_type: official_maximum
  abstract_words:
    max_words: 350
    source_type: official_jama_network_abstract_guidance_when_applicable
  key_points: 3
  display_items:
    max_items: 5
    source_type: official_maximum
  references:
    min_references: 50
    max_references: 75
    source_type: official_range_or_jama_style_snapshot
  page_limit:
    status: not_specified
    rule: budget by words, display items, and references; do not invent a page limit
  count_scope: main text only; excludes abstract, tables, figures, acknowledgments, references, and online-only material
```

- Main text word budget: approximately 3000 words for Original Investigation-style research reports.
- Abstract and Key Points Budget: track the structured abstract and 3 Key Points separately from
  the main-text word budget. Do not count abstract, Key Points, article information, displays,
  references, or appendices toward the main-text total unless the confirmed target journal says so.
- Display-item budget: no more than 5 total tables/figures in the main article unless the current
  target-journal instructions say otherwise. This display-item cap is provisional until exact target-journal instructions are verified for the confirmed JAMA-family journal and article type.
- Reference budget: typically 50-75 references for Original Investigation-style research reports.
- No page-count limit is recorded in the local JAMA snapshot. For JAMA-style medical manuscripts,
  plan by word budget, display-item budget, and reference budget; do not invent a page limit.

## Submission Format

- Default route: `word-first`.
- Primary submission file: `manuscript.docx`.
- Do not require `main.pdf` for JAMA/JAMA-style word-first packages.
- `jama_original_investigation.tex` is an instruction-derived review shell only, not an official JAMA
  class or required submission template.
- The primary `manuscript.docx` should be submission-clean: title page, Key Points, abstract, text,
  references, Figure Legends, and Tables; figures should be submitted as separate files, 1 file per
  figure, and not embedded in the manuscript text. If a reader-friendly file is useful, create
  `paper/review-preview-inline.docx` and label it as a preview artifact, not the primary submission
  file.
- Start the title page, abstract/Key Points, main text, references, figure legends, and tables on new
  pages, with continuous page numbering beginning at the title page.

## Blocking Checks

- Confirm the exact JAMA-family journal and article type.
- Check the current word, reference, and display-item limits against the official page.
- Include the selected reporting checklist and a checklist compliance matrix.
- Do not claim JAMA compliance from the local shell alone; the shell is only a compile-ready
  drafting template.
