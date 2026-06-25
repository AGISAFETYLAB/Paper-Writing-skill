# Stage: LaTeX Project — Finance

## Load Prerequisites

Load before creating files:

- Confirmed Writing Policy and Paper Framework.
- `../../_shared/submission/templates.md` for template selection order.
- `../../../../../assets/templates/index.md` for available local shells and official packages.
- `../../_shared/venues/standards/index.md` plus the target venue card when available.
- `../../_shared/submission/submission-standards.md` before calling the project
  submission-ready.

Templates are format shells. After copying an official or package-local template, strip
sample/instruction body text and keep only formatting setup, required hooks, and confirmed Paper
Framework content. This strip sample/instruction body text rule is mandatory before drafting.

Create `paper/` as a submission-style LaTeX project:

- copy or adapt the selected template from `../../../../../assets/templates/`,
- create `main.tex`, `references.bib`, and `figures/` when figures are present,
- when the user specified a target journal, conference, or platform, implement the target's official
  format rules exactly unless a rule is explicitly unavailable or unsupported; do not use generic
  finance defaults for template/class, font, spacing, margins, citation/reference style, anonymity,
  title-page handling, abstract constraints, appendix/supplement placement, or figure/table policy,
- include abstract, JEL codes, keywords, data-code statement, and appendix note,
- use finance-readable regression tables with economic magnitude and uncertainty,
- compile with `latexmk -pdf -interaction=nonstopmode -file-line-error main.tex`.
- count compiled pages with `pdfinfo paper/main.pdf` or an equivalent PDF page-count tool.
- run the page-window audit after every compile:
  `python3 <academic-finance-writing>/skills/academic-review/scripts/audit_page_window.py paper --min-pages <min_pages> --max-pages <max_pages>`.
  Record the resulting `target_page_window`, `actual_pdf_pages`, and `page_window_status` in
  `paper/submission-package.md`. below_min_pages blocks the full-draft return; continue supported
  drafting from the confirmed page-window expansion budget or return a blocker asking the user to
  confirm a smaller target.
- run the finance citation static audit before calling the draft citation-ready:
  `python3 <academic-finance-writing>/skills/academic-citation/scripts/audit_citations.py paper --require-ledger`.
  Add `--min-citations <floor>` when the Paper Framework or paper type sets a citation floor.
  This audit does not prove claim support; claim support still requires live lookup and Citation
  Evidence Ledger rows.
- run finance table static lint with
  `python3 <academic-finance-writing>/skills/academic-figure/scripts/lint_finance_tables.py paper`.
- run finance visual asset QA when plotted assets exist:
  `python3 <academic-finance-writing>/skills/academic-figure/scripts/audit_visual_assets.py paper/figures`.
- run compiled table layout QA with
  `python3 <academic-finance-writing>/skills/academic-figure/scripts/inspect_compiled_layout.py paper --pages tables --out-dir paper/layout-qa`.
  Machine status alone is not a pass. Open `paper/layout-qa/contact_sheet.png` or page PNGs and
  record `layout_manual_inspection_status`. Use `compiled_layout_qa_status: partial` when the
  contact sheet has not been inspected.
- run submission package status integrity audit before submission-ready wording:
  `python3 <academic-finance-writing>/skills/academic-review/scripts/audit_submission_package.py paper`.
- run the Local Path Leak Gate before returning any paper package:
  `python3 <academic-finance-writing>/skills/academic-review/scripts/audit_local_path_leaks.py paper`.
  The paper package is blocked if any artifact contains absolute local paths, local workspace roots,
  generator script paths, or package provenance. Rewrite the artifact with relative source labels or
  redacted source IDs, then rerun the audit.

For working papers, the compiled PDF is the public-facing draft. For journal submissions, record
which template/format is provisional and which journal-specific checks remain.

Write this status in `paper/submission-package.md`:

```yaml
actual_pdf_pages: <integer>
page_window_status: pass | below_min_pages | above_max_pages | blocked_uncounted
format_source_url: <official author-instruction URL or current-year conference call URL>
format_date_checked: <YYYY-MM-DD>
template_route: official_template | official_guideline_with_local_shell | package_local_fallback | blocked_missing_template
citation_reference_style: <venue-required style and implemented LaTeX/BibTeX setting>
format_compliance_status: pass | partial | blocked
local_path_leak_status: pass | blocked
table_static_lint_status: pass | blocked
visual_asset_qa_status: pass | blocked | not_applicable
compiled_layout_qa_status: pass | partial | blocked
layout_manual_inspection_status: pass | partial | blocked | not_performed
central_result_uncertainty_status: pass | partial | blocked | not_applicable
submission_attachment_status: pass | partial | blocked | not_applicable
replication_package_status: pass | partial | blocked | not_applicable
submission_readiness_verdict: pass | warn | fail | blocked
```

Block completion when the compiled page count is below min_pages, above max_pages, or unavailable.
Do not report LaTeX compile PASS as full-draft PASS when `page_window_status` is not `pass`.
Do not pad the manuscript to reach min_pages; add only supported, framework-approved content or mark
the missing evidence as `needs_user_evidence`.

Also block target-compliance when `format_compliance_status` is not `pass`. A package-local fallback
may produce a readable draft, but it cannot be described as strict target-venue formatting unless all
venue-required formatting fields above are implemented and verified.

Also block package return when `local_path_leak_status` is not `pass`. Local file-system details are
not manuscript provenance and must not appear in `paper/` artifacts.

The LaTeX project is also blocked when `main.log` contains unresolved `Float too large`,
large `Overfull \vbox`, or margin-crossing `Overfull \hbox` signals affecting table/figure pages.
The table static lint and layout QA runs must leave a pass/block status plus
`paper/layout-qa/layout_qa_summary.md` and rendered table pages or a contact sheet. Inspect those
artifacts for clipped cells, unreadable table fonts, sparse full-width floats, and right-side
underfill before recording the table aesthetics gate as pass.

The figure export QA is blocked when `audit_visual_assets.py` reports a blank preview, likely
cropped title/axis label/legend, or extreme unused margins. Redraw the figure with a larger canvas,
`constrained_layout=True`, or `bbox_inches="tight"` plus sufficient padding before accepting the
asset.

The central result uncertainty gate is blocked when a headline contrast row, such as high-minus-low
CAR, long-short spread, alpha, or treatment effect, lacks SE, t-stat, p-value, confidence interval,
or bootstrap interval. If no uncertainty is available, demote the row to descriptive-only prose and
record `central_result_uncertainty_status: partial` or `blocked`; do not use it as a headline
inferential result.

For journal submissions, placeholder `title-page.md` or `conflict-of-interest-disclosure.md` files
are allowed only for workflow-test fixtures. Record `submission_attachment_status: partial` or
`blocked`; do not mark the package submission-ready until real author/title-page and disclosure
content satisfy the venue card.
