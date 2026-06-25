# Stage: Paper Framework — Finance

## Load Prerequisites

Load after the Writing Policy is confirmed:

- `../../_shared/core/workflow-contract.md` for ledger schemas.
- `../../_shared/paper-types/index.md` and
  `../../_shared/paper-types/profile-boundary.md`.
- The selected version-target and paper-type cards from
  `../../_shared/version-targets/` and `../../_shared/paper-types/`.
- `../../_shared/venues/standards/index.md` plus the target venue card when available.
- `../../_shared/submission/templates.md` and `../../../../../assets/templates/index.md`.
- `references/sections/index.md` for section-guide routing and section-role planning.
- `references/writing-craft.md` for the Finance Writing Craft Gate, Results
  Narrative Gate, and Title-Abstract-Introduction Scorecard.
- `../../_shared/checks/data-code.md` and `../../_shared/checks/research-workflow.md`
  for replication, appendix, and code-output planning.
- `../../_shared/checks/finance-domains.md` when the finance domain, JEL G field, or selected
  finance domain adapter changes terminology, variables, displays, literature, or reviewer risks.
- `../../_shared/checks/identification-strategies.md` and
  `../../_shared/checks/econometrics.md` when the method requires them.
- `../academic-figure/references/finance-palette.md` when the Display-Item Plan includes plotted
  figures or figure-like tables.
- `../academic-figure/references/table-design.md` when the Display-Item Plan includes any table,
  regression table, summary-statistics table, portfolio/factor table, appendix table, or table
  audit.
- `../academic-figure/references/figure-layout.md` when planning figure/table width, float placement,
  single-column/double-column use, or appendix overflow.

This stage is the content boundary: it says what each section must cover, which displays support
which claims, and what remains blocked. Section-level rhetoric stays in `references/sections/`.

Build the manuscript framework from the confirmed Writing Policy:

- Paper Type Profile Hard Default: use the selected profile's section table as the default
  structure; do not silently split, merge, rename, add, or reorder sections.
- Structure vs paper-type profile: include a short comparison that records each profile section,
  the planned section name, and any approved deviation.
- Domain vs paper-type profile: record the selected finance domain adapter separately from
  structure; domain changes terminology, variables, mechanisms, literature, display pressure, and
  reviewer risks, not section order.
- Method family vs paper-type profile: record the primary method family separately from structure;
  method family changes evidence standards, diagnostics, robustness, assumptions, and display
  requirements, not section order unless the user approves a structural deviation.
- Section Plan table with section order, paragraph-level message plan, word/page budget, evidence,
  and writing risks,
- section-guide routing table that maps each planned section to the selected section guide and any
  required domain or method guide,
- Writing Craft Plan with the one-sentence contribution contract, `belief_update_status`,
  `results_narrative_status`, `writing_craft_status`, and the Title-Abstract-Introduction
  Scorecard,
- model/identification/evidence map,
- Display-Item Plan table: descriptive statistics, main estimates, robustness, event-study,
  portfolio, diagnostic, structural, ML/text, or composite displays, with a paper-level palette
  profile and layout placement for plotted figures and wide tables; for tables include table
  skeleton, table payoff, venue override, table hygiene status, source_table_to_script_map,
  page_budget_cost, and appendix destination,
- citation plan: theory, empirical benchmark, econometric method, data/software sources,
- venue card choice from `../../_shared/venues/standards/index.md`,
- template choice from `../../_shared/submission/templates.md` and
  `../../../../../assets/templates/index.md`,
- page-window choice from the selected version-target card, target venue card, or current official
  source:
  `target_page_window`, `min_pages`, `max_pages`, `source_type`, `source_url`, `date_checked`,
  and `count_scope`,
- Data-Code And Replication Plan: dataset profile, code-output map, Script Registry / Code Sweep
  status, online appendix, and replication package blockers.

Required tables:

| # | section | role | main content | budget | evidence/source | writing risk |
|---|---|---|---|---|---|---|

| gate | planned evidence | status | blocker |
|---|---|---|---|
| one-sentence contribution contract | belief update and closest benchmark | partial | yes/no |
| Title-Abstract-Introduction Scorecard | title, abstract, intro first-three-paragraph result | partial | yes/no |
| Results Narrative Gate | result-first sequence, magnitude, benchmark, robustness threat | partial | yes/no |
| Paragraph Evidence Contract | claim, data/model/design, uncertainty, magnitude, limit | partial | yes/no |

| ID | type | location | claim supported | data/model source | notes | table skeleton / payoff | source_table_to_script_map | page_budget_cost / appendix destination | palette profile | placement width | float env | final size | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Required page-window block:

```yaml
target_page_window:
  min_pages: <integer>
  max_pages: <integer>
  source_type: official | official_recommendation | official_max_plus_fallback_minimum | field_convention_fallback
  source_url: <official URL, selected venue card URL, or selected version-target card fallback>
  date_checked: <YYYY-MM-DD>
  count_scope: <what pages count>
```

Page-budget planning is mandatory. Synthetic/demo workspaces are not exempt from the page-window
gate: they are test cases for whether the workflow can produce a realistic full-length manuscript.
Add a page-window expansion budget after the Section Plan. Section budgets must sum to at least `min_pages`; if they do not, revise the framework before confirmation by adding supported
discussion, method detail, data provenance, variable construction, display interpretation,
robustness-limit, replication/code-output, and Internet Appendix material. If the source package
cannot support the confirmed target without padding, duplication, invented results, or weakened
evidence boundaries, ask the user to confirm a smaller target before drafting.

## Terminal checkpoint schema

Terminal-facing Paper Framework checkpoint: when returning to the user after writing the framework
artifact, show a concise checkpoint in the interaction language. The saved Markdown artifact may
keep the English schema above, but the terminal checkpoint must be content-first and table-driven.
Do not return only a file path, route log, validation note, line count, source URL, or change list.

Required order:

1. **Framework Overview**: paper identity, confirmed structural profile, domain adapter, method
   family, target venue/version target, page-window source status, template route, data-code
   boundary, and major evidence boundary.
2. **Writing Craft Plan**: one-sentence contribution contract, `belief_update_status`,
   `results_narrative_status`, `writing_craft_status`, and the Title-Abstract-Introduction
   Scorecard.
3. **Page-Window And Template Summary**: target page window, source status, section-budget
   arithmetic, template route, official-source status, and whether the current source package can
   support the target without padding.
4. **Section Plan**: Markdown table with section order, role, main content, page/word budget,
   evidence/source, and writing risk. This table is mandatory terminal output.
5. **Display-Item Plan**: Markdown table with every planned table/figure/appendix display, source
   asset/code, claim supported, placement width, float environment, final size, and QA status. For
   tables, include table payoff, source_table_to_script_map, page_budget_cost, and appendix
   destination. This table is mandatory terminal output.
6. **Decisions to confirm**: Markdown table for venue/template choice, page-window handling,
   section deviations from the paper-type profile, display placement, citation blockers, and
   data-code/replication route.
7. **Unresolved blockers**: current source checks, citations, official venue rules, synthetic-data
   or proprietary-data limits, missing scripts, unsupported claims, and blocked writing craft gates.
8. **Workflow Progress**: current stage, waiting-for state, next stage after confirmation, and
   not-started artifacts such as `paper/`, section drafting, formal citations, figure/table
   generation, compiled PDF, and submission package.
9. **Stage ledger**: saved framework artifact path, route, whether `paper/` was created, and any
   compact static-check result. This is the first place where `Detected route`, file paths, line
   counts, validation status, and source URLs may appear.
10. **Example user replies**: include exact short replies such as `确认，继续生成 paper/。`,
    `修改：...`, `选择：...`, and `暂停，不继续。`.
11. **Required user action**: ask whether to confirm or revise the Paper Framework.

For English terminal output, render Section Plan with this header:

```markdown
| # | Section | Role | Main content | Page/word budget | Evidence/source | Writing risk |
|---:|---|---|---|---|---|---|
```

For Chinese terminal output, render `章节计划` with this localized header:

```markdown
| # | 章节 | 角色 | 主要内容 | 页数/字数预算 | 证据/来源 | 写作风险 |
|---:|---|---|---|---|---|---|
```

For English terminal output, render Display-Item Plan with this compact header:

```markdown
| ID | Type | Location | Claim supported | Data/model source | Layout/width | QA status |
|---|---|---|---|---|---|---|
```

For Chinese terminal output, render `图表计划` with this localized header:

```markdown
| ID | 类型 | 位置 | 支持的主张 | 数据/模型来源 | 版式/宽度 | QA状态 |
|---|---|---|---|---|---|---|
```

For English terminal output, render Decisions to confirm with this header:

```markdown
| Decision | Current judgment | Status | User action needed |
|---|---|---|---|
```

For Chinese terminal output, render `待确认决策` with this localized header:

```markdown
| 决策 | 当前判断 | 状态 | 需要你确认/补充 |
|---|---|---|---|
```

Allowed Decisions to confirm status values are `confirmed / inferred / required / blocking /
optional`; for Chinese terminal output use `已确认 / 推断 / 必须确认 / 阻塞 / 可选`.

For Chinese terminal output, use these labels:

| English saved-artifact label | Chinese terminal label |
|---|---|
| `Framework Overview` | `论文框架概览` |
| `Writing Craft Plan` | `写作质量计划` |
| `Page-Window And Template Summary` | `页数窗口与模板摘要` |
| `Section Plan` | `章节计划` |
| `Display-Item Plan` | `图表计划` |
| `Decisions to confirm` | `待确认决策` |
| `Unresolved blockers` | `未解决阻塞项` |
| `Workflow Progress` | `流程进度` |
| `Stage ledger` | `阶段记录` |
| `Example user replies` | `可直接回复` |
| `Required user action` | `请确认或修改` |

For Chinese terminal output, include a `可直接回复` block with copyable examples such as:

```text
- 确认，继续生成 paper/。
- 修改：章节计划中的 <section> 改为 <...>。
- 修改：图表计划中 <table/figure> 改为 <...>。
- 修改：页数窗口改为 <...>。
- 选择：保留当前目标期刊和模板路线。
- 暂停，不继续。
```

Do not lead with workflow completion, route, saved file path, line count, validation status, source
URLs, or "Paper Framework 已完成". The first substantive checkpoint block must be Framework Overview
/ `论文框架概览`; file paths, line counts, validation status, and source URLs belong only in Workflow Progress or Stage ledger. Do not emit English terminal labels such as `Detected route`, `Framework Overview`, `Writing Craft Plan`, `Section Plan`, `Display-Item Plan`, `Decisions to confirm`, `Unresolved blockers`, `Workflow Progress`, `Stage ledger`, `Example user replies`, or `Required user action` in Chinese conversations. Render the stop line in Chinese, for example: `在此停止并等待你的确认。请确认这份 Paper Framework 是否可以继续，或告诉我需要修改的内容。`

Stop after this stage unless the framework has already been confirmed.

Template choice must follow the finance order: official guideline first, official template package
second, package-local shell last. Do not select a package-local shell merely because a named venue
exists.
