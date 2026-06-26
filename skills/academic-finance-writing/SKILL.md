---
name: academic-finance-writing
description: Use when planning, drafting, revising, citing, preparing figures/tables, or reviewing finance, financial economics, asset pricing, market microstructure, corporate finance, accounting, banking, risk, portfolio, trading/backtest, fintech, event-study, policy-evaluation, theory-model, or econometrics research papers. Also trigger on Chinese requests such as 金融论文写作、资产定价论文、公司金融论文、风险管理论文、回测论文、事件研究、金融计量、working paper、JEL、online appendix、投稿前自检. This standalone finance package writes and revises paper artifacts only; it does not provide investment advice, trade recommendations, run analyses, or invent results.
---

# Academic Finance Writing — Standalone Entry Router

This is the standalone finance package of `paper-writing-skill`. It can be installed by itself:
copy this `academic-finance-writing/` folder and no other discipline package is required.

It does no writing work itself. Its job is to route the request to exactly one internal sub-skill
under `skills/`, then **read and follow that sub-skill's `SKILL.md`**.

| Sub-skill | Path | Owns |
|---|---|---|
| **`academic-writing` (hub)** | `skills/academic-writing/SKILL.md` | Finance full-draft and draft-revision workflows, including Writing Policy, Paper Framework, LaTeX project assembly, section drafting, and delegation. |
| `academic-figure` | `skills/academic-figure/SKILL.md` | Finance tables/figures, regression tables, event-study plots, portfolio panels, appendix displays, QA. |
| `academic-citation` | `skills/academic-citation/SKILL.md` | Finance/economics citations, data/software citations, BibTeX/reference-list integrity. |
| `academic-review` | `skills/academic-review/SKILL.md` | Finance submission-readiness review, identification/econometrics risk, data-code and online-appendix gates. |

Package-local resources live under `_shared/`, `skills/*/references`, `skills/*/scripts`, and
`assets/templates/`. Internal sub-skills load them by relative path, so this folder remains
self-contained when downloaded alone.

The package covers complete first-draft generation, meaning-preserving polish, finance/economics
tables and figures, citation verification, submission-readiness review, and referee/editor response
packages. It uses package-local references for prose style, identification strategies, data-code
governance, submission standards, and venue/template provenance.

## Routing

Classify the user's request before loading a sub-skill.

### Workflow Intent Classifier

Use exactly one primary intent class:

| Intent class | Trigger | Route |
|---|---|---|
| `full-draft-from-evidence` | workspace/source materials plus request to write or generate a complete first finance manuscript | `skills/academic-writing/SKILL.md` |
| `package-completion` | partial `paper/`, confirmed policy/framework, or incomplete LaTeX package that should be continued or completed | `skills/academic-writing/SKILL.md` |
| `draft-revision` | existing prose or LaTeX needs polish, rewrite, compression, local checking, or version preparation | `skills/academic-writing/SKILL.md` |
| `audit-only` | user asks only to inspect/check/diagnose existing prose or package without changing files | `skills/academic-writing/SKILL.md` or `skills/academic-review/SKILL.md` by scope |
| `figure-only` | only plotted figures, diagrams, visual displays, or display audits are requested | `skills/academic-figure/SKILL.md` |
| `table-only` | only regression tables, summary-statistics tables, portfolio/factor tables, robustness tables, or LaTeX table shells are requested | `skills/academic-figure/SKILL.md` |
| `citation-only` | only source finding, data/software citation, BibTeX repair, or citation audit is requested | `skills/academic-citation/SKILL.md` |
| `submission-review` | existing manuscript/package needs referee-risk, data-code, appendix, or submission-readiness review | `skills/academic-review/SKILL.md` |
| `revision-response` | referee/editor response, R&R package, response letter, or revision map is requested | `skills/academic-writing/SKILL.md` |

When a request spans writing plus figures/citations/review, route to the hub; it delegates at the
right stage.

If source evidence and an old manuscript/package coexist and the user intent is unclear, ask one
route-selection question and stop. The concrete options should include clean-slate first draft,
complete existing package, revise existing draft, audit only, figure-only, table-only, citation-only,
or submission-review as applicable.

## Scope

This package writes and revises manuscript artifacts only. It does not provide investment advice,
trade recommendations, execute analyses, backtests, or simulations, or invent results, alphas,
standard errors, data permissions, citations, code repositories, or robustness checks.

Every substantive claim must identify data source/vendor, sample window, unit of observation,
variable construction, model or identification assumption, statistical uncertainty, economic
magnitude, and replication/data-code boundary.
