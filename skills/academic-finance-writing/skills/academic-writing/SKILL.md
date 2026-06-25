---
name: academic-writing
description: Use when planning, drafting, revising, or reviewing a finance, financial economics, asset-pricing, corporate-finance, banking, fintech, event-study, theory-model, accounting, risk, portfolio, trading/backtest, or econometrics paper with version-target, paper-type, data-code, citation, figure/table, or submission-readiness constraints.
---

# Academic Finance Writing — Hub

This hub owns the finance writing pipeline:

`workspace -> Writing Policy -> Paper Framework -> LaTeX manuscript -> reviewed submission package`

Use Reader-first finance writing: concrete question, data/model, identification or benchmark,
headline result, economic magnitude, and evidence boundary first. Load `references/prose-style.md`
for drafting, revision, and anti-AI polishing; load `references/writing-craft.md` for the
Finance Writing Craft Gate, Contribution And Belief-Update Gate, Results Narrative Gate, and
Title-Abstract-Introduction Scorecard; load `../../_shared/checks/finance-domains.md` when
domain terminology, variables, literatures, display pressure, or reviewer risks shape the
manuscript; load `../../_shared/checks/identification-strategies.md` when causal design, event studies,
portfolio sorts, factor models, backtests, or structural estimation shape the prose.

It delegates specialized work to sibling skills:

- `../academic-figure/SKILL.md` for every table, figure, regression display, event-study plot, and appendix display.
- `../academic-citation/SKILL.md` for finance/economics citations, data/software citations, and bibliography audits.
- `../academic-review/SKILL.md` for econometrics, identification, data-code, appendix, and final submission-readiness gates.

## Workflow Intent Classifier

Classify the request before loading a workflow. Use exactly one primary intent class:

| Intent class | Trigger | Workflow |
|---|---|---|
| `full-draft-from-evidence` | source materials or workspace plus a request for a complete first finance manuscript | `full-draft` |
| `package-completion` | partial `paper/`, confirmed policy/framework, or incomplete LaTeX package should be continued or completed | `full-draft` re-entry |
| `draft-revision` | existing prose or LaTeX needs polish, rewrite, compression, local checking, or version preparation | `draft-revision` |
| `audit-only` | inspect/check/diagnose existing prose or package without changing files | `draft-revision` audit mode or `academic-review` for submission readiness |
| `figure-only` | only plotted figures, diagrams, visual displays, or display audits are requested | `academic-figure` |
| `table-only` | only regression, summary-statistics, portfolio/factor, robustness, appendix, or LaTeX table work is requested | `academic-figure` |
| `citation-only` | only source finding, BibTeX repair, data/software citation, or citation audit is requested | `academic-citation` |
| `submission-review` | existing package needs referee-risk, data-code, appendix, or final readiness review | `academic-review` |
| `revision-response` | referee/editor response, R&R package, response letter, or revision map is requested | `revision-response` |

If source evidence and an old manuscript/package coexist and the intended route is unclear, ask one
route-selection question and stop. Do not silently choose between clean-slate drafting, package
completion, draft revision, audit-only, figure-only, table-only, citation-only, or submission-review.

## Load Order

1. Read `manifest.yaml`.
2. Read every file under `always_load`.
3. Route `workflow`:
   - `full-draft`: workspace or source materials -> complete LaTeX manuscript.
   - `package-completion`: partial package -> earliest missing stage.
   - `draft-revision`: existing prose or existing LaTeX -> revision/polish/review.
   - `audit-only`: existing prose/package -> findings only unless the user asks for edits.
   - `revision-response`: referee/editor response package and revision map.
4. Detect `version_target` and `paper_type` before choosing section structure.
5. Load only the workflow, stage, section, and finance-method references needed for the request.

## Finance Boundary

Do not provide investment advice, trade recommendations, or forward-looking profit claims. Do not
run analyses unless explicitly asked outside the writing workflow. Do not invent data vendors,
sample windows, alphas, standard errors, identification assumptions, citations, repository records,
or robustness results.

Every substantive claim must bind data source/vendor, sample window, unit of observation, variable
construction, model or identification assumption, statistical uncertainty, economic magnitude, and
replication/data-code boundary.

For any full draft or major rewrite, maintain the Finance Evidence Ledger, Display-Item Plan,
Citation Evidence Ledger, and Research Workflow Ledger from `../../_shared/core/workflow-contract.md`.

## Output Contract

Full-draft output is not complete until `paper/main.tex`, `paper/references.bib`, display items,
data-code statement, online appendix plan when needed, and `paper/main.pdf` exist and pass the
sibling review gates. A Markdown-only output is allowed only when the user explicitly asks for
Markdown only.
