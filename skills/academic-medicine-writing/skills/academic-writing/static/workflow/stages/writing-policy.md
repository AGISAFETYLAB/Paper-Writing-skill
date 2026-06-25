# Stage: Writing Policy — Medicine

Load this fragment at the Writing Policy stage. It ends at a blocking confirmation gate: do not
proceed to Paper Framework until the user confirms.

Load `../../_shared/submission/submission-standards.md`, `../../_shared/submission/statements.md`,
`../../_shared/article-types/index.md`, the selected checklist card when known, and
`../academic-citation/references/citation.md` only for guideline/source anchors. Load
`../../_shared/core/package-gates.md` for the `workflow-state.json` schema. Do not load templates,
journal standard cards, section examples, figure design rules, or review rules by default.

## Medical Evidence And Reporting Audit

Run this writing-side audit before filling the policy tables. It does not run analyses or design the
study; it decides what the manuscript may safely say.

1. Trace every planned central claim to source material: protocol/SAP, registry, ethics record,
   analysis report, result table, figure, existing draft, or verified citation.
   If source evidence and an existing manuscript or paper package coexist, treat this as a
   Workspace Discovery Questions issue rather than silently choosing a route.
2. Classify the study design and Reporting Checklist Selection. Use CONSORT, SPIRIT, STROBE,
   PRISMA, STARD, TRIPOD, CARE, GATHER, CHEERS, or mixed checklist only when the source material
   justifies it. Record the matching structured checklist item file from
   `../../_shared/checklists/items/index.md`; do not expand the full item matrix until Paper
   Framework.
3. Classify the target article type profile from `../../_shared/article-types/index.md`. Record
   the manifest value and profile path. This is the medicine paper type layer: it determines default
   section structure and proportional budget, while the reporting checklist determines item-level
   evidence. Mark the profile as inferred when the target journal has not named an article type.
4. Build the PICO / PECO / PIT / prediction frame:
   - PICO for interventions/trials,
   - PECO for exposure or observational association,
   - PIT for diagnostic/prognostic tests (population, index test, target condition/reference
     standard),
   - prediction frame for model papers (target population, predictors, outcome, horizon,
     development/validation split).
5. Check endpoint and analysis-population consistency between Methods, Results, figures/tables, and
   abstract claims.
6. Separate scientific weakness vs reporting weakness. A missing sensitivity analysis is scientific
   or evidentiary; a present sensitivity analysis not described in Methods is reporting weakness.
7. Identify Statement Unknowns: ethics/IRB, consent, trial registration, protocol/SAP, data/code
   availability, funding, conflicts, author contributions, acknowledgments, AI-use disclosure.
8. List unsupported or unsafe claims to weaken, remove, or ask about.

## Required File

Save the policy to `writing-policies/<slug>-writing-policy.md`.

Also initialize or update `writing-policies/workflow-state.json` using schema version
`medicine-workflow-state-v1`. Set `policy_confirmed` to `false`, `framework_confirmed` to `false`,
record the detected `workflow`, `intent`, `study_type`, `article_type`, selected checklist, and
current `blocking_gaps`, and leave `submission_format_route` unresolved unless it is already safely
known. Do not mark this state confirmed before the user confirms the Writing Policy.

Required sections:

1. **Source Snapshot**: source label, files inspected, evidence date, and relative or redacted source trace.
   Do not store absolute local paths, raw workspace roots, generator script paths, or package
   provenance in the saved policy or terminal checkpoint.
2. **Paper Identity**: working title, target article type, selected article type profile path,
   target journal status, study type, selected reporting checklist, structured checklist item file,
   and template status if already known.
3. **Medical Question Frame**: PICO / PECO / PIT / prediction frame or a justified alternative.
4. **Core Story**: clinical/biomedical problem, evidence gap, study purpose, main finding boundary,
   and cautious takeaway.
5. **Medical Evidence And Reporting Audit**: compact table with item, verdict
   (`pass/risk/blocking/unknown`), source trace, and writing action.
6. **Claims And Evidence**: claim, evidence, allowed wording strength, drafting action, risk.
7. **Terminology And Endpoints**: term/endpoint, definition, source, use policy, status.
8. **Statement Unknowns**: ethics/consent/registration/data-sharing/funding/conflicts/contributions
   table; mark each as provided, absent, unknown, not applicable, or user-needed.
9. **Display And Citation Inventory**: expected flow diagram, baseline table, outcome/adverse-event
   tables, diagnostic/prediction/forest plots, checklist needs, and citation needs.
10. **Open Decisions**: only decisions that change paper identity, checklist, claim boundary,
    endpoint, target journal/template, or statements.
11. **Workspace Discovery Questions**: user-choice questions caused by workspace ambiguity, such as
    an existing manuscript or paper package, source-evidence conflict, multiple output roots, or
    uncertainty between clean-slate from evidence, revise existing package, and audit existing
    package.

Do not encode detailed section page budgets or final figure placement here; those belong to Paper
Framework. At this stage, record target journal status and whether official-source verification is
needed, but do not expand final author-instruction details. Keep this exact boundary:
`exact journal instructions, word limits, table/figure limits, and reference limits belong to Paper Framework`.

## Checkpoint Summary

Terminal-facing Writing Policy checkpoint: mirror the user's interaction language. The saved Writing
Policy artifact may keep the English section schema above, but the terminal checkpoint must use the
user's language for headings, status labels, warnings, and the confirmation request.

Return a concise checkpoint summary in the user's interaction language in this order:

1. **Policy snapshot**:
   - paper identity and checklist: working title, target article type, selected article type profile
     path, target journal status, study type, selected checklist, and structured checklist item file,
   - medical question frame,
   - central claim boundary and strongest supported claim,
   - evidence snapshot: source-evidence types and what they support, plus major unsupported claims,
     - statement unknowns,
     - Workspace Discovery Questions when discovery found an existing manuscript or paper package,
       source-evidence conflict, or route ambiguity,
     - top 2-3 risks,
      - required confirmation or corrections.
2. **Confirmation Matrix**:
   - show what is already confirmed, what was inferred from source materials, what must be confirmed
     before Paper Framework, what blocks submission/readiness later, and what is optional;
   - every row must include the item, current judgment, status, and user action needed;
   - allowed status values are `confirmed / inferred / required / blocking / optional`; for Chinese
     terminal output use `已确认 / 推断 / 必须确认 / 阻塞 / 可选`;
   - if the user says only `JAMA`, list `exact JAMA-family journal` as `required` / `必须确认`
     instead of treating the target as fully confirmed.
   - if the workspace contains `paper/`, `manuscript_*`, prior `writing-policies/`, `main.tex`,
     `manuscript.docx`, `submission-package.md`, or `review-report.md` beside source evidence, add a
     required row asking the user to choose `clean-slate from evidence`, `revise existing package`,
     or `audit existing package`; do not silently choose one route.
3. **Workflow Progress**:
   - current stage: Writing Policy generated,
   - waiting for: user confirmation or correction,
   - next stage after confirmation: Paper Framework,
   - not started: `paper/`, references, figures/tables, submission package.
4. **Stage ledger**:
   - completed: Writing Policy,
   - not started: Paper Framework and `paper/`,
   - artifact path.
5. **Example user replies**:
   - provide concrete replies the user can copy, including proceed, target-journal correction,
     estimate-use correction, statement/evidence supplement, and pause.
6. **Required user action**: ask whether to confirm or revise the Writing Policy.

The first substantive checkpoint block must be the policy content block. A checkpoint that opens with completion status, file path, line count, validation status, or source-check prose fails this stage, even if the saved policy file itself is correct. Put route/status only in a compact line before the content block or in the stage ledger after the content block.

Do not substitute a workflow/provenance report for the policy snapshot. Do not lead with stage
completion, file path, line count, validation status, or source URLs. Keep source verification notes
to at most one short line after the content summary when needed.

For Chinese terminal output, use these labels:

| English saved-artifact label | Chinese terminal label |
|---|---|
| `Detected route` | `路由判断` |
| `Policy snapshot` | `写作策略摘要` |
| `paper identity and checklist` | `论文身份与报告清单` |
| `medical question frame` | `医学问题框架` |
| `central claim boundary` | `核心主张边界` |
| `evidence snapshot` | `证据快照` |
| `statement unknowns` | `声明未知项` |
| `Workspace Discovery Questions` | `工作目录疑问` |
| `top risks` / `Blocking gaps` | `主要风险/阻塞缺口` |
| `Confirmation Matrix` | `确认状态` |
| `Workflow Progress` | `流程进度` |
| `Stage ledger` | `阶段记录` |
| `Example user replies` | `可直接回复` |
| `Required user action` | `请确认或修改` |

For English terminal output, render the Confirmation Matrix with this header:

```markdown
| Item | Current judgment | Status | User action needed |
|---|---|---|---|
```

For Chinese terminal output, render `确认状态` as a Markdown table with this localized header:

```markdown
| 项目 | 当前判断 | 状态 | 需要你确认/补充 |
|---|---|---|---|
```

For Chinese terminal output, include a `可直接回复` block with copyable examples such as:

```text
- 确认，继续生成 Paper Framework。
- 选择：clean-slate from evidence，忽略旧 manuscript_jama_network_open/。
- 选择：revise existing package，基于现有 manuscript_jama_network_open/ 修改。
- 选择：audit existing package，先审计现有稿件包。
- 修改：目标期刊是 JAMA Network Open。
- 修改：不要把 covariate_adjusted_logistic 写成真实拟合模型结果。
- 补充：ethics/IRB 为 <...>；funding/conflicts 为 <...>。
- 暂停，不继续。
```

Every Writing Policy checkpoint must include a visible Confirmation Matrix, Workflow Progress, and Example user replies. In Chinese conversations, the terminal checkpoint must not contain the English headings `Detected route`, `Policy snapshot`, `Blocking gaps`, `Stage ledger`, `Required user action`, or `STOP HERE and wait for user response`. Do not emit English terminal labels such as `Detected route`, `Policy snapshot`, `Blocking gaps`, `Stage ledger`, `Required user action`, or `STOP HERE and wait for user response` in Chinese conversations. Render the stop line in Chinese, for example: `在此停止并等待你的确认。请确认这份 Writing Policy 是否可以继续，或告诉我需要修改的内容。`

## Compliance Self-Check

Before showing the checkpoint, answer internally:

1. Is the article type profile selected or explicitly unknown?
2. Is the study type and checklist selected or explicitly unknown?
3. Does every central claim map to a source or a weaker drafting action?
4. Is the PICO / PECO / PIT / prediction frame complete enough for the study type?
5. Are endpoint, timeframe, and analysis population explicit for major results?
6. Are Statement Unknowns listed without invention?
7. Are scientific weakness and reporting weakness separated?
8. Did I avoid downstream template/section/figure/review references that this stage should not load?
9. Did I select or explicitly defer the structured checklist item file without inventing item
   evidence?
10. If discovery found an existing manuscript or paper package, source-evidence conflict, or multiple
   plausible output roots, did I show Workspace Discovery Questions and ask the user to choose rather
   than silently choose clean-slate from evidence, revise existing package, or audit existing package?

Any "no" means the Writing Policy is not ready. Fix it or ask before proceeding.

Stop after this stage unless the user has already confirmed an existing policy.
