# Stage: Writing Policy — Finance

## Load Prerequisites

Load before writing this stage:

- `../../_shared/core/workflow-contract.md` for ledger schemas and cross-stage invariants.
- The selected `../../_shared/version-targets/` card.
- `../../_shared/paper-types/index.md` for paper-type selection.
- The selected `../../_shared/paper-types/` card.
- `references/writing-craft.md` for the Finance Writing Craft Gate and
  Contribution And Belief-Update Gate.
- `../../_shared/checks/finance-domains.md` when the finance domain, JEL G field, or selected
  finance domain adapter is known or inferred.
- `../../_shared/checks/identification-strategies.md` when the method family or
  identification strategy is known or inferred.
- `../../_shared/checks/data-code.md` and
  `../../_shared/checks/research-workflow.md` when data, code, replication, or appendix
  status is known or central.

This stage fixes scope and evidence boundaries; it does not choose the final template or write
section prose.

Write a concise policy before drafting the manuscript. It must fix:

- paper identity, version target, paper type, and selected paper type profile path,
- finance domain, selected finance domain adapter, method family, and identification strategy as
  separate fields when known,
- core contribution and target audience,
- one-sentence contribution contract and `belief_update_status`,
- data source/vendor, sample window, unit of observation, filters, and variable construction,
- identification strategy or model assumptions,
- available results, unsupported claims, and robustness boundary,
- data-code/replication package boundary and online appendix needs,
- display-item inventory and citation needs.

The policy must include a Finance Evidence Ledger with one row per central claim:

| claim | data/model source | sample/window | benchmark/specification | economic magnitude | robustness | status |
|---|---|---|---|---|---|---|

Also include initial Citation Evidence Ledger, Display-Item Plan, and Research Workflow Ledger
status when evidence exists. Also include Writing Craft Status with the Finance Writing Craft Gate,
Contribution And Belief-Update Gate, one-sentence contribution contract, and preliminary
`belief_update_status`. If data profile, code-output mapping, contribution benchmark, or replication
status is unknown, mark it `needs_user_evidence`.

## Terminal checkpoint schema

Terminal-facing Writing Policy checkpoint: when returning to the user after writing the policy
artifact, show a concise checkpoint in the interaction language. The saved Markdown artifact may
keep the English schema above, but the terminal checkpoint must be content-first and table-driven.
Do not return only a file path, route log, validation note, line count, or source URL.

Required order:

1. **Policy Snapshot**: provisional title, target venue/version target, structural paper type,
   finance domain adapter, method family, identification boundary, data-code boundary,
   non-advisory boundary, synthetic/proprietary-data boundary, one-sentence contribution contract,
   and `belief_update_status`.
2. **Core Claim Check**: 3-5 central claims with source file/model, economic magnitude when
   available, status (`supported`, `partial`, `needs_user_evidence`, or `unsupported`), and writing
   action. Render this as a Markdown table, not prose bullets.
3. **Ledger Status**: Finance Evidence Ledger, Display-Item Plan, Citation Evidence Ledger,
   Research Workflow Ledger, and Writing Craft Status. Render this as a compact Markdown table.
4. **Confirmation Matrix**: separate confirmed, inferred, required, blocking, and optional items so
   the user can see what must change before the Paper Framework stage. Every row must include item,
   current judgment, status, and user action needed.
5. **Workflow Progress**: current stage, waiting-for state, next stage after confirmation, and
   not-started artifacts such as `paper/`, formal citations, figure/table generation, and submission
   package.
6. **Stage ledger**: saved policy artifact path, route, whether `paper/` was created, and any
   compact static-check result. This is the first place where `Detected route`, file paths, line
   counts, validation status, and source URLs may appear.
7. **Example user replies**: include exact short replies such as `确认，继续生成 Paper Framework。`,
   `修改：...`, `选择：...`, and `暂停，不继续。`.
8. **Required user action**: ask whether to confirm or revise the Writing Policy.

For English terminal output, render the Core Claim Check with this header:

```markdown
| Claim | Source/model | Economic magnitude | Status | Writing action |
|---|---|---|---|---|
```

For Chinese terminal output, render `核心主张核对` with this localized header:

```markdown
| 主张 | 来源/模型 | 经济量级 | 状态 | 写作动作 |
|---|---|---|---|---|
```

For English terminal output, render Ledger Status with this header:

```markdown
| Ledger | Current status | Next step |
|---|---|---|
```

For Chinese terminal output, render `账本状态` with this localized header:

```markdown
| 账本 | 当前状态 | 下一步 |
|---|---|---|
```

For English terminal output, render the Confirmation Matrix with this header:

```markdown
| Item | Current judgment | Status | User action needed |
|---|---|---|---|
```

For Chinese terminal output, render `确认状态` with this localized header:

```markdown
| 项目 | 当前判断 | 状态 | 需要你确认/补充 |
|---|---|---|---|
```

Allowed Confirmation Matrix status values are `confirmed / inferred / required / blocking /
optional`; for Chinese terminal output use `已确认 / 推断 / 必须确认 / 阻塞 / 可选`.

For Chinese terminal output, use these labels:

| English saved-artifact label | Chinese terminal label |
|---|---|
| `Policy Snapshot` | `写作策略摘要` |
| `Core Claim Check` | `核心主张核对` |
| `Ledger Status` | `账本状态` |
| `Confirmation Matrix` | `确认状态` |
| `Workflow Progress` | `流程进度` |
| `Stage ledger` | `阶段记录` |
| `Example user replies` | `可直接回复` |
| `Required user action` | `请确认或修改` |

For Chinese terminal output, include a `可直接回复` block with copyable examples such as:

```text
- 确认，继续生成 Paper Framework。
- 修改：目标期刊改为 <...>。
- 修改：不要把 synthetic fixture 写成真实市场证据。
- 选择：在当前实验目录内创建新的 paper/，不覆盖旧产物。
- 补充：数据来源/样本窗口/复制包状态为 <...>。
- 暂停，不继续。
```

Do not lead with workflow completion, route, saved file path, line count, validation status, source
URLs, or "已按 ... 进入 full-draft workflow". The first substantive checkpoint block must be Policy
Snapshot / `写作策略摘要`; file paths, line counts, validation status, and source URLs belong only in Workflow Progress or Stage ledger. Do not emit English terminal labels such as `Detected route`, `Policy Snapshot`, `Core Claim Check`, `Confirmation Matrix`, `Workflow Progress`, `Stage ledger`, `Example user replies`, or `Required user action` in Chinese conversations. Render the stop line in Chinese, for example: `在此停止并等待你的确认。请确认这份 Writing Policy 是否可以继续，或告诉我需要修改的内容。`

Stop after this stage unless the user has already confirmed an existing policy.
