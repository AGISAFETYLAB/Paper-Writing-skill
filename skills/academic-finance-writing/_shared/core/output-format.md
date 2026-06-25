# Finance Output Format

Unless the user asks for another format, return or write these artifacts for a full manuscript task:

```text
paper/main.tex
paper/references.bib
paper/main.pdf
paper/submission-package.md
paper/figures/* when figures are produced
```

Online Appendix, Internet Appendix, proof, and data-code notes belong in `paper/main.tex`,
`paper/submission-package.md`, or a clearly named supplemental file only when the confirmed Paper
Framework calls for one.

For non-checkpoint interactive replies, lead with:

```text
Detected route: workflow=<...>; version_target=<...>; paper_type=<...>; sections=<...>.
Blocking gaps: <none or concise list>.
Output artifacts: <paths or planned files>.
```

## Route Output Templates

For every routed request, keep the terminal reply short and use this route output template before
adding route-specific details:

```text
A. Input Match Check
   workflow=<...>; intent=<...>; version_target=<...>; paper_type=<...>; input_sufficiency=<enough|partial|insufficient>.
B. Route Output
   <the artifact, revision, display, table, citation audit, review verdict, or checkpoint requested by this route>
C. Blocking Gaps
   <none, or P0/P1/P2 items with severity and correction priority>
D. Next Action
   <user confirmation, missing input, or generated artifact path>
```

Route-specific output scope:

- `full-draft-from-evidence` and `package-completion`: checkpoint or package artifacts, plus the
  submission-readiness verdict when a complete package exists.
- `draft-revision`: revised prose or localized edit report inside the requested edit boundary.
- `audit-only`: findings only; do not rewrite or create files unless the user then asks.
- `figure-only`: display artifact, visual plan, caption, or display audit only.
- `table-only`: LaTeX/booktabs table, table shell, table plan, or table audit only.
- `citation-only`: citation search result, bibliography repair, or citation audit only.
- `submission-review`: findings first, ordered by severity, then residual risk and next action.
- `revision-response`: response letter/backlog/revision map items tied to evidence.

Writing Policy and Paper Framework checkpoints are exceptions. Do not use `Detected route` as the
first line of a checkpoint. For those gates, follow
`skills/academic-writing/static/workflow/full-draft.md` and the relevant stage file: show the
policy snapshot or framework overview first, then put route, file path, and validation details in
Workflow Progress.

At confirmation gates, content structure overrides route logging. A Writing Policy checkpoint must
open with Policy Snapshot / `写作策略摘要`; a Paper Framework checkpoint must open with Framework
Overview / `论文框架概览`. Do not lead with workflow completion, saved file path, line count,
validation status, or source URLs. File paths, line counts, validation status, and source URLs
belong only in Workflow Progress or Stage ledger after the content summary.
For Chinese Paper Framework checkpoints, use `流程进度`, `阶段记录`, `可直接回复`, and
`请确认或修改` for the closing interaction blocks.

For citation or review workflows, lead with blocking issues and evidence gaps before revised prose.

If a full-draft workflow writes files, create and compile the LaTeX project unless the user
explicitly asks for Markdown only.

For full-draft checkpoints, include concise ledger status:

- Finance Evidence Ledger: supported / partial / needs user evidence
- Display-Item Plan: planned / rendered / audited / blocked
- Citation Evidence Ledger: verified / partial / unsupported
- Research Workflow Ledger: dataset, code-output, replication, and appendix status
- Finance Writing Craft Gate: one-sentence contribution contract, `belief_update_status`,
  `results_narrative_status`, `writing_craft_status`, and `finance_prose_lint_status`
- Page Window Gate: `target_page_window`, `actual_pdf_pages`, and pass/block status
- Table Design Gate: `table_static_lint_status`, table provenance, table payoff, page-budget cost,
  and appendix destination status
- Visual/Layout QA Gate: `visual_asset_qa_status`, `compiled_layout_qa_status`, and
  `layout_manual_inspection_status`
- Submission Attachment Gate: `submission_attachment_status` for title-page, anonymity,
  conflict-of-interest, funding, and acknowledgement handling
- Central Result Uncertainty Gate: `central_result_uncertainty_status` for headline differences,
  spreads, alphas, event-window contrasts, and treatment effects

Record page status in `paper/submission-package.md`:

```yaml
target_page_window:
  min_pages: <integer>
  max_pages: <integer>
  source_type: official | official_recommendation | official_max_plus_fallback_minimum | field_convention_fallback
  count_scope: <what pages count>
actual_pdf_pages: <integer>
page_window_status: pass | below_min_pages | above_max_pages | blocked_uncounted
table_static_lint_status: pass | blocked | not_applicable
visual_asset_qa_status: pass | blocked | not_applicable
compiled_layout_qa_status: pass | partial | blocked
layout_manual_inspection_status: pass | partial | blocked | not_performed
central_result_uncertainty_status: pass | partial | blocked | not_applicable
submission_attachment_status: pass | partial | blocked | not_applicable
replication_package_status: pass | partial | blocked | not_applicable
finance_prose_lint_status: pass | blocked | waived | not_applicable
belief_update_status: pass | partial | blocked
results_narrative_status: pass | partial | blocked
writing_craft_status: pass | partial | blocked
submission_readiness_verdict: pass | warn | fail | blocked
```

If `actual_pdf_pages` is below min_pages or above max_pages, the full draft is blocked. Do not
mark a draft complete or submission-ready when the compiled PDF is below min_pages, above
max_pages, or uncounted.

Do not report LaTeX compile PASS as full-draft PASS. Compile success only means the PDF exists.
The full-draft package remains blocked until `skills/academic-review/scripts/audit_page_window.py paper --min-pages
<min_pages> --max-pages <max_pages>` passes and the submission package records:

```yaml
target_page_window:
  min_pages: <integer>
  max_pages: <integer>
actual_pdf_pages: <integer>
page_window_status: pass
```

## Local Path Leak Gate

Public paper artifacts must not contain absolute local paths, local workspace roots, generator
script paths, or package provenance. This includes `paper/main.tex`, `paper/references.bib`,
`paper/main.pdf`, `paper/submission-package.md`, DOCX/Markdown exports, captions, appendices, and
review-facing reports. Use relative source labels or redacted source IDs instead.

Run `skills/academic-review/scripts/audit_local_path_leaks.py paper` before returning a full draft or submission-review
package. A hit for absolute local paths blocks the return until the artifact is rewritten or the
source trace is moved to a private engineering note outside `paper/`.

Record the result in `paper/submission-package.md`:

```yaml
local_path_leak_status: pass | blocked
```

## Table Static Lint Gate

For LaTeX full-draft or submission-review packages with editable tables, run
`skills/academic-figure/scripts/lint_finance_tables.py paper` before returning the package. Blocking findings include
vertical rules, `\hline`, unjustified `\resizebox`, declared-width `tabularx` without a real `X`
column, missing captions, and leading decimals without zero.

Record the result in `paper/submission-package.md`:

```yaml
table_static_lint_status: pass | blocked | not_applicable
```

## Visual Asset And Compiled Layout QA Gate

For plotted figure assets, run `skills/academic-figure/scripts/audit_visual_assets.py paper/figures`
or the relevant figure directory before marking figure export QA as pass. The audit catches blank
previews, likely cropped titles/axis labels/legends, and extreme unused margins. Record:

```yaml
visual_asset_qa_status: pass | blocked | not_applicable
```

For compiled LaTeX packages, run
`skills/academic-figure/scripts/inspect_compiled_layout.py paper --pages tables --out-dir paper/layout-qa`.
The script's machine check is not enough for a final pass. After opening the contact sheet or page
PNGs, record:

```yaml
compiled_layout_qa_status: pass | partial | blocked
layout_manual_inspection_status: pass | partial | blocked | not_performed
layout_qa_summary_path: paper/layout-qa/layout_qa_summary.md
layout_qa_contact_sheet_path: paper/layout-qa/contact_sheet.png
```

`compiled_layout_qa_status: pass` is valid only when the script reports clean machine layout and
`layout_manual_inspection_status: pass` is recorded after human/visual inspection. If the contact
sheet has not been inspected, the status is `partial`, not `pass`.

## Central Result Uncertainty Gate

Every headline estimate, event-window contrast, long-short spread, high-minus-low difference,
treatment effect, alpha, or central regression coefficient must carry uncertainty: SE, t-stat,
p-value, confidence interval, bootstrap interval, or an explicit descriptive-only downgrade. Run
`skills/academic-figure/scripts/lint_finance_tables.py paper`; it blocks central contrast rows with
missing uncertainty cells. Record:

```yaml
central_result_uncertainty_status: pass | partial | blocked | not_applicable
```

Do not use a central difference without uncertainty as an inferential headline. It can remain only
as a descriptive table row with weakened prose.

## Submission Attachment Gate

For journal submissions, title-page, anonymity, disclosure, funding, acknowledgement, and conflict
files must match the target venue card. Placeholder files are allowed only for workflow-test
fixtures and must be recorded as partial or blocked. Record:

```yaml
submission_attachment_status: pass | partial | blocked | not_applicable
```

Run `skills/academic-review/scripts/audit_submission_package.py paper` before reporting
submission-readiness. Placeholder title pages, placeholder conflict-of-interest disclosures,
synthetic evidence boundaries, missing status fields, or partial/blocked layout and replication
states must keep `submission_readiness_verdict` at `blocked` or `fail`.

## Finance Prose Lint Gate

For full-draft, draft-revision, and submission-review packages with editable text, run
`skills/academic-writing/scripts/lint_finance_prose.py paper` before reporting a clean full draft or submission-readiness
verdict. Blocking findings include banned AI phrase, empty contribution phrase, causal language
without identification cue, significance without magnitude cue, and table tour sentence. Pair this
static check with `skills/academic-writing/references/writing-craft.md`; the script is a warning system, not a replacement
for the Contribution And Belief-Update Gate or Results Narrative Gate.

Record the result in `paper/submission-package.md`:

```yaml
finance_prose_lint_status: pass | blocked | waived | not_applicable
belief_update_status: pass | partial | blocked
results_narrative_status: pass | partial | blocked
writing_craft_status: pass | partial | blocked
```
