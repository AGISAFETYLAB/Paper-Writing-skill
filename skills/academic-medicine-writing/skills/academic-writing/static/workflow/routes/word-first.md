# Word-first Route

Use when the confirmed Submission Format Route is `word-first`.

Load `../../_shared/submission/word-first-production.md` for the detailed production contract.

## Required Production Artifact

The primary manuscript file is `paper/manuscript.docx`. Keep `paper/manuscript.md` or another
auditable source when useful. A PDF preview is optional and must be labeled `review-preview.pdf`;
it does not satisfy the word-first production gate.

## Assembly Requirements

- Use a preloaded official Word template, user-provided official template, official web-fetched
  template, or the package-local generic Word reference shell in that order.
- Do not call a generic Word reference shell an official journal template.
- Render editable text, editable tables, figure legends, figure callouts, and standard section
  starts.
- Keep figures as embedded or upload-ready assets under `paper/figures/` with manuscript callouts.
- Normalize JAMA/JAMA-family manuscripts to AMA superscript citations before rendering.

## PASS Gate

Record `format-specific production gate: PASS (word-first)` only when:

- `paper/manuscript.docx` exists;
- an auditable source exists;
- DOCX structure audit passes for settings, styles, theme, numbering, media/drawing evidence, table
  style coverage, cell borders, table grids, double spacing, new page starts, and superscript
  citation runs when required;
- AMA superscript citation audit passes for JAMA/JAMA-family routes;
- visual display gate and table aesthetics gate have route-specific evidence.

If any requirement fails, record `format-specific production gate: BLOCKED` with the exact missing
artifact or audit defect.
