# Word-first Production Contract

Use this reference whenever the confirmed `Submission Format Route` is `word-first`, especially for
JAMA/JAMA-family routes and any target journal that expects editable Word manuscript files.

## Primary Artifact Rule

- The primary submission artifact is `paper/manuscript.docx`.
- Keep `paper/manuscript.md` or another auditable source when useful.
- `paper/main.pdf`, `paper/review-preview.pdf`, or `paper/review-preview-inline.docx` can be review
  artifacts only; they do not satisfy the word-first production gate.
- For JAMA/JAMA-family routes, use a `submission-clean` primary manuscript by default: manuscript
  text, editable tables, figure legends, and figure callouts in the DOCX; figure assets remain
  separately upload-ready under `paper/figures/`.

## Template And Reference-DOCX Rule

Select Word template/reference input in this order:

1. preloaded official Word template;
2. user-provided official Word template;
3. official web fetch recorded with URL/date/status;
4. package-local generic Word reference shell.

Do not call a generic Word reference shell an official journal template. JAMA/JAMA-style routes must
not claim an official Word template unless an official source or user-supplied file proves one.

## JAMA/JAMA-Family Rule

Before rendering a JAMA/JAMA-family word-first manuscript:

- normalize Markdown to AMA superscript citations and first-citation order;
- run or inspect `skills/academic-citation/scripts/format_ama_manuscript.py`,
  `skills/academic-citation/scripts/audit_ama_citations.py`,
  `skills/academic-citation/scripts/audit_medical_citations.py`, and
  `skills/academic-review/scripts/audit_jama_components.py`;
- place References before Figure Legends and Tables;
- keep the Tables section as the final manuscript component.

The audit blocker text must include the exact phrase `Tables section is not the final manuscript component` when component order is wrong.

## DOCX Quality Gate

Record `format-specific production gate: PASS (word-first)` only when:

- `paper/manuscript.docx` exists and is a normal Word package, not minimal OOXML;
- `word/settings.xml`, `word/styles.xml`, `word/theme/`, `word/numbering.xml`, paragraph style
  coverage, table style coverage, `word/media`, and `w:drawing` are present or explicitly justified
  by a separate-upload route;
- DOCX layout audit passes for title/heading sizes, cell border coverage, `w:tcBorders`, table grid
  coverage, `w:tblGrid`, continuous page numbering, double spacing, new page starts, and
  route-appropriate citation rendering;
- editable Word tables or companion table files exist for main tables;
- visual display gate and table aesthetics gate have route-specific evidence.

If any requirement fails, use `format-specific production gate: BLOCKED` with the exact missing
artifact or audit defect.

## Citation And Component Order

For JAMA/JAMA-family routes, the AMA audit must block:

- square-bracket numeric citations such as `[5]`;
- references that are not numbered in first-citation order;
- nonconsecutive numbering or uncited numbered references;
- author lists that violate AMA/JAMA shortening rules;
- References appearing after end-matter legends or tables;
- missing or hidden DOI, PMID, PMCID, or verified source identifiers when required by the citation
  audit.

Use `review-preview-inline.docx` only as a reader-friendly preview when embedded figures help review.
Do not mark it as the primary submission file.
