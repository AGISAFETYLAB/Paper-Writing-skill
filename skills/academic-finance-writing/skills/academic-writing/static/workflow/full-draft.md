# Full Draft Workflow — Finance

Use when the user provides source materials or a workspace and wants a complete finance manuscript,
or when an existing finance manuscript package is incomplete and the user asks to continue it.

Intent classes covered: `full-draft-from-evidence` and `package-completion`.

## State Machine

```text
workspace
  -> Writing Policy
  -> user confirmation unless already confirmed
  -> Paper Framework
  -> user confirmation unless already confirmed
  -> paper/ LaTeX project
  -> figure/table + citation search/verify/audit workflow + review gates
  -> compiled main.pdf
  -> submission package + official-source gate

partial `paper/` or incomplete finance manuscript package
  -> Package Completion Intake
  -> earliest missing stage
  -> missing package components
  -> figure/table + citation search/verify/audit workflow + review gates
  -> compiled main.pdf
  -> submission package + official-source gate
```

## Required Outputs

| Stage | Output |
|---|---|
| Writing Policy | `writing-policies/<slug>-writing-policy.md` with contribution, version target, paper type, data/code boundary, identification/econometric claims, Finance Evidence Ledger, unsupported claims |
| Paper Framework | `writing-policies/<slug>-paper-framework.md` with Section Plan table, Display-Item Plan table, identification and robustness map, Citation Evidence Ledger, Data-Code And Replication Plan, template choice |
| Package Completion Intake | concise inventory of existing `paper/`, `writing-policies/`, source evidence, missing route artifacts, unresolved blockers, confirmed policy and framework status, and the earliest missing stage |
| Full Draft | `paper/main.tex`, `paper/references.bib`, any `paper/figures/*`, data-code and online-appendix notes, compiled `paper/main.pdf`, `paper/submission-package.md` |

## Stage Loading

This is the route-level loading map. Each stage file repeats the exact files it must load before
producing that stage's artifact.

1. Load `../../manifest.yaml`, `../../_shared/core/workflow-contract.md`,
   `references/prose-style.md`, `../../_shared/paper-types/index.md`,
   `../../_shared/paper-types/profile-boundary.md`, and the selected version-target and
   paper-type cards.
2. For finance domain terminology, field-specific variables, display pressure, or reviewer risks,
   load `../../_shared/checks/finance-domains.md` after selecting the structural paper type.
3. For empirical methods, method family, or identification claims, load
   `../../_shared/checks/identification-strategies.md` and
   `../../_shared/checks/econometrics.md`.
4. For data/code and replication, load `../../_shared/checks/data-code.md` and
   `../../_shared/checks/research-workflow.md`.
5. For target-venue planning, load `../../_shared/venues/standards/index.md`, then the
   target-specific venue card when available.
6. For template choice, load `../../_shared/submission/templates.md` and
   `../../../../assets/templates/index.md`.
7. For page limits and compiled page-count gates, use the selected version-target card and the
   target venue card.
8. For section planning, load `references/sections/index.md`; for section drafting,
   also load `references/sections/paragraph-flow.md` and the selected section guide.
9. For contribution, belief update, results narrative, and final prose quality, load
   `references/writing-craft.md`.

## Confirmation Gates

After Writing Policy, STOP HERE unless the user has already confirmed a compatible policy.
After Paper Framework, STOP HERE unless the user has already confirmed a compatible framework.

For `package-completion`, first run Package Completion Intake. If `paper/` exists but is partial,
inventory manuscript source, references, figures/tables, citation ledger, data-code statement,
layout QA, compiled PDF, and `paper/submission-package.md`. Resume from the earliest missing stage.
Use confirmed policy and framework when they are present and consistent. The goal is to complete
existing package components from the earliest missing stage; package completion does not re-run
confirmed gates unless they conflict with current evidence, manuscript identity, version target,
paper type, data source, sample window, method family, or target venue.

Mandatory terminal checkpoint behavior:

- Do not compress, batch, or silently satisfy the Writing Policy or Paper Framework confirmation
  gates.
- Mirror the user's interaction language at both confirmation gates. `STOP HERE and wait for user
  response` is an internal gate marker, not terminal-facing text. In Chinese conversations, render
  the stop line as Chinese, for example: `在此停止并等待你的确认。`
- Do not lead with workflow completion, Detected route, file path, line count, validation status, or source URLs.
- After Writing Policy, return only a concise finance policy checkpoint: policy snapshot first,
  then Core Claim Check, Ledger Status, Confirmation Matrix, Workflow Progress, Stage ledger,
  Example user replies, and Required user action. The checkpoint must show the policy content before
  process status. Do not lead with workflow completion, Detected route, file path, line count,
  validation status, source URLs, or "已按 ... 进入 full-draft workflow". The route, saved file path,
  line count, validation status, and source URLs may appear only inside Workflow Progress or Stage
  ledger after the policy content. In Chinese terminal output, use `写作策略摘要`, `核心主张核对`,
  `账本状态`, `确认状态`, `流程进度`, `阶段记录`, `可直接回复`, and `请确认或修改`. Core Claim Check,
  Ledger Status, and Confirmation Matrix must be Markdown tables. The Confirmation Matrix must use
  confirmed / inferred / required / blocking / optional, or `已确认 / 推断 / 必须确认 / 阻塞 / 可选`
  in Chinese. STOP HERE and wait for user response. Do not generate Paper Framework until
  confirmed.
- After Paper Framework, return only a concise finance framework checkpoint: framework overview
  first, then page-window/template/data-code summary, the Section Plan table and Display-Item Plan
  table, Decisions to confirm table, Unresolved blockers, Workflow Progress, Stage ledger, Example
  user replies, and Required user action. The checkpoint must show the planned manuscript content
  before process status. Do not lead with workflow completion, Detected route, file path, line
  count, validation status, source URLs, or "Paper Framework 已完成". The route, saved framework path,
  line count, validation status, and source URLs may appear only inside Workflow Progress or Stage
  ledger after the framework content. In Chinese terminal output, use `论文框架概览`, `写作质量计划`,
  `页数窗口与模板摘要`, `章节计划`, `图表计划`, `待确认决策`, `未解决阻塞项`, `流程进度`, `阶段记录`,
  `可直接回复`, and `请确认或修改`. Section Plan, Display-Item Plan, and Decisions to confirm must be
  Markdown tables. Decisions to confirm must use confirmed / inferred / required / blocking /
  optional, or `已确认 / 推断 / 必须确认 / 阻塞 / 可选` in Chinese. STOP HERE and wait for user
  response. Do not create `paper/` until confirmed. Do not draft sections, generate new
  figures/tables, or write BibTeX until the user confirms.
- If the user asks for autonomous or one-shot full-draft generation, still stop at both gates. The
  request authorizes the workflow; it does not authorize skipping confirmation.

## Completion Gate

A full draft is incomplete until the sibling skills have handled:

- figures/tables: `academic-figure`
- citations/bibliography/data citations: `academic-citation`
- econometrics, data-code, appendix, and submission readiness: `academic-review`

Never return a full finance draft with unresolved producible markers such as `CITATION_NEEDED`,
`TABLE_NEEDED`, `FIGURE_NEEDED`, missing data-code statement text, or an uncompiled PDF.

The draft must also include:

- Finance Evidence Ledger status for central claims
- Finance Writing Craft Gate status: one-sentence contribution contract, `belief_update_status`,
  `results_narrative_status`, and `writing_craft_status`
- Display-Item Plan status for tables and figures
- Citation Evidence Ledger status for papers, data, software, methods, and institutional facts
- Research Workflow Ledger status for dataset profile, code-output map, Script Registry / Code
  Sweep, replication package, and Internet Appendix
- Data-Code And Replication Plan with unresolved blockers explicitly marked
- Visual/Layout QA Gate status for `visual_asset_qa_status`, `compiled_layout_qa_status`, and
  `layout_manual_inspection_status`
- Submission Attachment Gate status for title page, anonymity, conflict-of-interest disclosure,
  funding, acknowledgements, and venue-specific attachment handling
- Central Result Uncertainty Gate status for headline estimates, spreads, alphas, event-window
  contrasts, long-short spreads, and treatment effects

Before calling citation work complete, run
`../academic-citation/scripts/audit_citations.py paper --require-ledger` and add the applicable
`--min-citations` floor when set by paper type or framework. The audit is a structural BibTeX and
local-marker gate; it does not prove claim support. Claim support requires the `academic-citation`
search/verify path, live lookup or user-provided verified sources, and Citation Evidence Ledger
rows.

If the user specified a target journal, conference, or platform, citation work is not complete until
the manuscript uses that target's required in-text citation and reference-list style. Record the
official source, required style, implemented LaTeX/BibTeX settings, and `format_compliance_status` in
the Paper Framework and `paper/submission-package.md`. Do not leave an author-year finance default
in place when the selected target requires numeric, footnote, Vancouver, IEEE, ACM, APA, Chicago, or
another explicit style.

## Page-Window Gate

Every full draft must carry a `target_page_window` from the selected version-target card, selected
venue card, or a current official source. Record `min_pages`, `max_pages`, `source_type`,
`source_url`, `date_checked`, and `count_scope` in the Paper Framework and
`paper/submission-package.md`.

Synthetic/demo workspaces are not exempt from the page-window gate. A synthetic fixture still tests
whether the writing workflow can produce a realistic full-length package. During Paper Framework,
build a page-window expansion budget that maps every planned page to supported material: method
detail, data provenance, variable construction, display interpretation, robustness limits,
replication/code-output mapping, Internet Appendix material, and citation context. Section budgets
must sum to at least `min_pages` for the confirmed `target_page_window`. If the evidence package
cannot support that target without padding, duplication, invented results, or weakened evidence
boundaries, ask the user to confirm a smaller target before drafting; do not proceed to a below-min
full draft under the original target.

After compiling `paper/main.pdf`, record `actual_pdf_pages`. The gate fails if the PDF is missing,
uncounted, under target window, or over target window:

- below `min_pages` -> `page_window_status: below_min_pages`
- above `max_pages` -> `page_window_status: above_max_pages`
- no reliable PDF count -> `page_window_status: blocked_uncounted`

Do not pad, duplicate content, invent results, invent citations, or weaken evidence boundaries to
hit min_pages. If legitimate material is missing, add only supported content from the confirmed
Paper Framework; otherwise mark the gap `needs_user_evidence`.

Run `../academic-review/scripts/audit_page_window.py paper --min-pages <min_pages> --max-pages <max_pages>` after every
compile. A `below_min_pages`, `above_max_pages`, or `blocked_uncounted` result blocks the full-draft
return. Do not report a full draft as complete unless the audit prints `PASS finance page-window
audit` and `paper/submission-package.md` records `page_window_status: pass`.

## Visual/Layout QA Gate

Run `../academic-figure/scripts/audit_visual_assets.py paper/figures` when plotted figure assets
exist. The gate fails for blank previews, likely cropped titles/axis labels/legends, or dominant
unused margins that make the figure unreadable at manuscript size. Record `visual_asset_qa_status`
in `paper/submission-package.md`.

Run `../academic-figure/scripts/inspect_compiled_layout.py paper --pages tables --out-dir
paper/layout-qa` after every compile. The script records machine layout status and writes a contact
sheet. Machine status alone is not a pass: open the contact sheet or page PNGs and record
`layout_manual_inspection_status`. `compiled_layout_qa_status: pass` requires both clean machine
layout and `layout_manual_inspection_status: pass`; otherwise record `partial` or `blocked`.

## Central Result Uncertainty Gate

For every central result table or figure, ensure the manuscript gives uncertainty for headline
differences, event-window contrasts, high-minus-low rows, long-short spreads, alphas, treatment
effects, and main regression coefficients. Acceptable anchors are SE, t-stat, p-value, confidence
interval, bootstrap interval, or an explicit descriptive-only downgrade. Run
`../academic-figure/scripts/lint_finance_tables.py paper`; a
`central_contrast_missing_uncertainty` finding blocks inferential headline wording and sets
`central_result_uncertainty_status: blocked` until fixed or demoted.

## Submission-Standard Gate

Before saying the draft is submission-ready, load `../../_shared/submission/submission-standards.md`,
`../../_shared/venues/standards/index.md`, and the target venue card when available. Record the
official source URL and date checked in `paper/submission-package.md`. The
gate fails if the PDF is missing, the version target is unknown, the page-window status is not
`pass`, the target venue rules are unchecked, title page/anonymity/disclosure handling is
unresolved, the official template or format route is not implemented, the citation/reference style
does not match the target, or data/code, JEL, Internet Appendix, and replication boundaries are
missing. Run `scripts/lint_finance_prose.py paper` when editable text exists and record
`finance_prose_lint_status`; unresolved prose lint, blocked `belief_update_status`, blocked
`results_narrative_status`, or blocked `writing_craft_status` also blocks submission-ready wording.

Run `../academic-review/scripts/audit_submission_package.py paper` before any submission-ready
claim. The audit blocks missing machine-readable status fields, placeholder title-page or
conflict-of-interest files marked as pass, `compiled_layout_qa_status: pass` without
`layout_manual_inspection_status: pass`, synthetic evidence not reflected in a blocked/fail verdict,
and missing central-result uncertainty not reflected in the readiness verdict.
