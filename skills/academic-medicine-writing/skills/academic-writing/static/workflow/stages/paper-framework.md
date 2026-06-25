# Stage: Paper Framework — Medicine

Load this fragment after the Writing Policy is confirmed. It ends at a blocking confirmation gate: do
not create `paper/` until the user confirms.

Load only:

- confirmed Writing Policy,
- `../../_shared/submission/templates.md`,
- `../../_shared/submission/word-first-production.md` when `word-first` or JAMA/JAMA-family Word
  production is plausible,
- `../../assets/templates/index.md`,
- `../../_shared/article-types/index.md`,
- selected article type profile under `../../_shared/article-types/`,
- `../../_shared/article-types/profile-boundary.md`,
- selected checklist card,
- selected item-level checklist JSON from `../../_shared/checklists/items/`,
- `references/sections/index.md`,
- `../../_shared/submission/statements.md`,
- `../../_shared/submission/submission-standards.md`,
- `../../_shared/submission/data-availability.md`,
- `../../_shared/checks/reliability.md`,
- `../../_shared/checks/claim-verification.md`,
- `../../_shared/core/package-gates.md`,
- target journal standard card under `../../_shared/journal-standards/` only when a target
  journal has been named.

## Framework Purpose

The Paper Framework is a section-level manuscript plan, not prose. It must decide how the confirmed
study becomes a complete submission artifact.

## Article Type Profile Hard Default

Use the manifest-selected `article_type` profile as the medicine paper type layer. The selected
profile owns the default section list, order, naming, count, proportional word budget, priority
contract, compression order, and core-section floor. The selected `study_type` and checklist own
item-level reporting evidence.

The active profile is a hard default, not inspiration:

- Reproduce the profile's section list, order, names, and section count in the Section Plan unless
  the target journal, selected reporting checklist, source evidence, statement requirement, or explicit
  user request requires a structural change.
- If a structural change is needed, show a `Structure vs article-type profile` comparison in the
  Paper Framework checkpoint: canonical profile list, adopted list, and one-line reason for every
  split, merge, rename, addition, or reorder.
- If the structure matches the profile, state `Structure vs article-type profile: matches profile`.
- Do not silently preserve the old embedded default skeletons; structure now comes from the selected
  profile file.

## Section And Article-Type Plan

Choose section order from the confirmed target journal, selected article type profile, and study
type. Do not reuse a computer-science section pattern for medical manuscripts.

If the user names only a journal family such as `JAMA`, ask neutrally for the exact JAMA-family journal or keep the exact journal as an unresolved decision; do not phrase the decision as `JAMA flagship rather than JAMA Network Open` because that wording biases the user toward one journal. Until the exact journal is confirmed, treat JAMA-family limits and route choices as local-snapshot planning constraints, not final submission instructions.

If the target journal standard card gives a different required section order, follow the journal
standard card and record the deviation. If the target is unknown, use the closest medical
article-type skeleton and mark target journal as unresolved.

## Length And Section Budget

Resolve the target journal's active length unit before drafting. Medical journals often specify
word limits, display-item limits, and reference limits rather than page limits.

- Resolve the active `target_length_budget` using this order: current official target-journal
  instructions first, selected journal standard card second, official template text third, and the
  Generic Medical Length Fallbacks in `../../_shared/submission/templates.md` fourth. In short: official
  first, field-convention fallback second.
- Length source rule: official first, field-convention fallback second.
- A valid Length Budget Summary must record the active `target_length_budget`, source type, date or
  snapshot status, count scope, lower bound, upper bound, and whether the lower bound is official or
  a field-convention completion floor.
- If the target source specifies a word limit, create a **Length Budget Summary** with active length
  unit, main-text word limit, abstract/key-points handling, display-item cap, reference cap, and
  exclusions or unresolved fields.
- Add an **Abstract and Key Points Budget** whenever the target article type requires a structured
  abstract or Key Points. Track this budget separate from the main-text word budget. The Section Plan
  may mark `Title / structured abstract / Key Points` as `n/a` for the main-text total, but the
  Length Budget Summary must still state the abstract limit/status, Key Points limit/status, and
  whether both are verified or provisional.
- Do not invent a page limit when the source specifies words rather than pages. If no page-count
  limit is recorded, state `page limit: not specified / not used; budget by words and display items`.
- Section Plan must include a section-level word budget for every main manuscript section that counts
  toward the active main-text limit. The planned section word budgets must sum to the active main-text
  word budget or explicitly explain a conservative under-target.
- For JAMA-style Original Investigation, use the journal standard card's local snapshot as a planning input:
  main text approximately 3000 words, no more than 5 main tables/figures, and typically 50-75
  references, while keeping a fresh official-source check as a blocker before submission-ready
  wording.
- For Nature Medicine, choose the exact official content type before drafting. If unresolved, use
  Nature Medicine Article/Resource/Analysis only as a provisional route and list content type as a
  blocker.
- For BMJ Case Reports, choose clinical case report, global health case report, or Images In before
  drafting and load the matching `target_length_budget`.

## Checklist Matrix

Load the structured item-level checklist JSON selected in Writing Policy. If the policy names only a
checklist card, resolve the JSON file through `../../_shared/checklists/items/index.md`.

Create one checklist compliance row per JSON item with:

| checklist | version | item_id | item | target_section | required_evidence | source_evidence | status | drafting_rule | manuscript_location |
|---|---|---|---|---|---|---|---|---|---|

Initialize each row from the JSON item: `status` starts as `needs_user_evidence`, and
`drafting_rule` must remain "ask user or insert TODO; do not invent" or a stricter equivalent.
Change status only when source material supplies the required evidence. Do not claim formal
compliance if the source material does not support it.

## Display-Item Plan

Plan every table/figure/supplement display before drafting:

- for observational cohort full drafts with available counts/effects, default to the minimum visual
  display set: Figure 1 cohort flow, Figure 2 outcome rate comparison, Figure 3 effect-estimate forest
  plot, Table 1 baseline characteristics, and Table 2 primary/secondary outcomes;
- participant flow / PRISMA flow / diagnostic flow / model development-validation flow when
  checklist-bound,
- baseline table with denominators and missingness,
- primary outcome table or figure,
- adverse-event/safety table when applicable,
- sensitivity/subgroup table only when source evidence exists,
- diagnostic accuracy table/ROC/calibration/decision curve when applicable,
- forest plot for meta-analysis or subgroup effect display when applicable,
- checklist/supplement table when required.

For JAMA-style Original Investigation planning, keep the main display budget at no more than 5 total
tables/figures. When evidence supports the minimum visual display set, use exactly 3 main figures and
2 main tables; place subgroup detail tables, missingness summaries, checklist matrices, and statement
inventories in the supplement/appendix. This display-item cap is provisional until exact target-journal instructions are verified for the confirmed JAMA-family journal and article type.

The display catalog must cover all applicable medical display classes, not only RCT displays:

- flow diagrams: CONSORT participant flow, PRISMA flow, diagnostic flow, model development and
  validation flow;
- trial/results displays: baseline table, primary/secondary outcome table, harms/adverse-event
  table, outcome bar/line plot, Kaplan-Meier/time-to-event plot, subgroup or sensitivity forest
  plot;
- evidence synthesis: study-characteristics/risk-of-bias table, forest plot, funnel plot;
- diagnostic/prediction: diagnostic 2x2 table, diagnostic metrics table, ROC plot, calibration
  plot, decision curve, prediction-model performance table;
- case/global/economics: case timeline figure or workup table, global-health data-source inventory
  and trend plot, health-economics cost/effect table, ICER plane, tornado sensitivity plot, model or
  trial schematic;
- submission package: display-item plan table, reporting-checklist matrix, and ICMJE-oriented
  statement table.

For each display, record: item ID, claim supported, source data, population/denominator, timeframe,
analysis population, uncertainty measure, target location, route-specific layout/upload handling,
table/figure styling plan, and fallback if evidence is missing.

For `word-first`, display layout labels must use Word/upload language such as `editable Word table`,
`main manuscript figure callout`, `separate figure upload asset`, `wide editable Word table`, or
`supplement file`; do not use `single-column` or `cross-column` in the terminal Display-Item Plan for word-first routes. Keep LaTeX width labels only for `latex-first` or optional PDF review artifacts.

Width planning is part of this stage for `latex-first` routes or optional PDF review artifacts:

- simple single-message plots and compact tables should be single-column;
- CONSORT/PRISMA flow, multi-panel outcomes, long-label forest plots, calibration plus decision
  curve panels, and wide clinical tables should be cross-column;
- compact single-panel heatmaps should remain single-column; use cross-column only for large
  matrices, long labels, clustering annotations, or multiple heatmap panels;
- Table 2-style outcome tables must reserve a wide effect-estimate column;
- Table 3-style harms tables must reserve enough width for event definitions or severity notes.
- risk-of-bias/study-characteristics tables and ICMJE statement tables are cross-column when they
  carry long explanatory text; allocate the widest column to risk signals or action notes.
- baseline and outcome tables must include a table aesthetics plan: compact labels, deliberate
  column widths, `booktabs`, small font, `\tabcolsep`/`\arraystretch`, table notes for abbreviations
  and caveats, and a rendered-PDF inspection requirement.
- main figures must include a visual display gate plan: real asset path under `paper/figures/`,
  expected `\includegraphics` placement, caption completeness, and final-size legibility check.

## Estimand / Temporal-Ordering Check

Before finalizing the Section Plan and Display-Item Plan, compare each exposure/intervention/index
definition with every primary and secondary outcome window. If an exposure and outcome share the
same measurement window or the same care-process definition, list a temporal-ordering decision in
Risks And Open Decisions.

Examples include an exposure such as `early_followup_7d` and a secondary process outcome such as
`med_reconciliation_7d`. Unless source definitions prove the exposure precedes the outcome, do not
write this as a treatment effect, clinical benefit, or causal improvement; downgrade to process/exploratory wording or mark user-needed until the author confirms timing, endpoint definition, and estimand role.

## Submission Format Route And Template Acquisition

Use `../../assets/templates/index.md` and `../../assets/templates/source-manifest.yaml`.

First decide the **Submission Format Route**:

1. `word-first`: the target journal expects Word or editable manuscript files as the primary
   submission. For JAMA/JAMA-style Original Investigation, use this route unless the user supplies a
   different official requirement. The primary submission file is `paper/manuscript.docx`; the working
   source may also include `paper/manuscript.md`. Load
   `../../_shared/submission/word-first-production.md`. A preview PDF is a review artifact only and
   is not a completion requirement.
2. `latex-first`: the target journal accepts or provides TeX/LaTeX source. The primary production
   artifacts are `paper/main.tex` and `paper/main.pdf`.
3. `generic-review`: the target journal or accepted source format is unresolved. Produce a reviewable
   manuscript package, but do not call it submission-ready.

After deciding the route, load the matching route fragment:

- `static/workflow/routes/word-first.md` for `word-first`;
- `static/workflow/routes/latex-first.md` for `latex-first`;
- `static/workflow/routes/generic-review.md` for `generic-review`.

Then select the route-specific template or shell:

1. If the target is Nature Portfolio / Springer Nature or the user asks for a Nature-style
   LaTeX submission source, use the official downloaded Springer Nature journal article template:
   `../../assets/templates/springer-nature-latex/sn-article-template/sn-article.tex` and
   `sn-jnl.cls`. Select `iicol` only for a requested or journal-appropriate two-column preview; do
   not assume Nature Medicine initial submission requires two-column production formatting.
2. If the target is JAMA-style Original Investigation, do not make
   `../../assets/templates/jama_original_investigation.tex` the primary submission template. Use it
   only as an optional review artifact if a PDF preview is explicitly useful, and label it as not an
   official JAMA class. The primary submission file remains `paper/manuscript.docx`.
3. If the target journal is unknown, use a generic review manuscript package and, only when a PDF
   preview is requested, `../../assets/templates/generic_medical_article.tex`.
4. If a named target journal has no package-local official template and no user-provided template,
   fetch the official author instructions or template from the journal source, record the URL/date,
   and report whether the route is Word, LaTeX, PDF-only, or unresolved.
5. Never represent a generic or instruction-derived shell as an official downloaded template.

## Statement Plan

Create a Statement Plan with the exact status of:

- ethics/IRB approval,
- consent,
- trial registration or protocol/SAP registration,
- data availability,
- code availability,
- funding,
- conflicts of interest,
- author contributions,
- acknowledgments,
- AI-use disclosure when required by the target journal.

Statement text can be drafted only from provided facts. Unknown identifiers stay unknown.

Run a Data Availability And FAIR Audit using `../../_shared/submission/data-availability.md`: data
repository or controlled-access route, third-party restriction status, code availability,
DataCite-ready metadata, and figure source data status.

## Reliability And Claim Verification Plan

Before confirming the framework, create a reliability and claim-verification plan:

- Result Reliability Audit from `../../_shared/checks/reliability.md`: design and bias, statistical and
  model risk, validation chain, and claim discipline;
- Claim Registry from `../../_shared/checks/claim-verification.md`: central claim, source tracing,
  evidence tier, status, and action;
- explicit downgrade rules for internal-only validation, missing sensitivity analysis, absent
  reference standard, or source-to-claim mismatch.

## Official-Source Plan

For named targets, record the official-source URL(s), date checked, article type, template status,
word/display-item constraints if known, and required statements/checklists. The final
`paper/submission-package.md` must later carry these fields.

## Required Framework File

Save to `writing-policies/<slug>-paper-framework.md` with:

1. **Inputs Used**: policy path, study type, checklist, target journal/article type, template source.
2. **Length Budget Summary**: active length unit, word/page/display/reference limits, source status,
   Abstract and Key Points Budget, and section-budget arithmetic.
3. **Structure vs article-type profile**: selected profile path, canonical profile section list,
   adopted section list, and deviation reasons or `matches profile`.
4. **Section Plan**: IMRaD/article-type section order, one-line message, section-level word budget,
   profile-derived role, and compression rule per section.
5. **Estimand / Temporal-Ordering Check**: exposure/intervention/index timing, outcome windows,
   same-window ambiguities, writing downgrade rules, and user-needed decisions.
6. **Checklist Matrix**: one row per item-level checklist JSON item with evidence/status/action.
7. **Display-Item Plan**: tables, figures, supplements, and data source status.
8. **Citation Plan**: clinical background, reporting guideline, registry, methods/statistics,
   comparable studies, target-journal instructions.
9. **Statement Plan**: statement inventory and source status.
10. **Data Availability And FAIR Audit**: repository/control route, third-party restrictions,
   DataCite metadata, code availability, figure source data, and blocker status.
11. **Reliability And Claim Verification Plan**: Result Reliability Audit items, Claim Registry
   scaffold, source tracing, and claim downgrade rules.
12. **Template And Submission Plan**: Submission Format Route, primary submission file, selected
   template/shell, official-source status, optional review artifact, single-column/two-column layout
   decision if LaTeX is used, submission-package fields.
13. **Risks And Open Decisions**: only blockers that would change section structure, checklist,
    statements, template, or central claim.

Update `writing-policies/workflow-state.json` after saving the framework. Use schema version
`medicine-workflow-state-v1`; set `policy_confirmed` according to the confirmed policy gate, keep
`framework_confirmed` as `false` until the user confirms this Paper Framework, and record
`submission_format_route`, `primary_submission_file`, required display IDs, required closing audits,
and `blocking_gaps`. This state file is the machine-readable companion to the framework, not a
replacement for the visible checkpoint.

Terminal-facing Paper Framework checkpoint: mirror the user's interaction language. In a Chinese
conversation, translate the overview headings, section summaries, display summaries, blockers, and
user action request into Chinese. Keep file paths, LaTeX commands, checklist names, item IDs,
figure/table IDs, and machine-parsed markers unchanged.

The terminal checkpoint is invalid unless all three visible planning blocks are present: Length Budget Summary, Section Plan, and Display-Item Plan. In Chinese terminal output, the visible planning blocks are `篇幅预算`, `章节计划`, and `图表计划`. Do not replace any of these blocks with a prose statement that the plan exists in the saved file, a file path, or a validation summary.

The checkpoint must show planned manuscript content before process status. Do not substitute a workflow/provenance report for the framework overview. Do not lead with stage completion, file path,
line count, validation status, source URLs, or "no paper/ created"; those belong only in the brief
stage ledger after the content summary.

Use this terminal structure:

```text
Checkpoint: Paper Framework
Stage result: <one sentence>
Output: <framework artifact path>

Framework overview:
- Article type / journal posture: <target journal, article type, study type, checklist>
- Template posture: <selected template and official/instruction-derived/generic status>
- Submission Format Route: <word-first / latex-first / generic-review>; primary submission file: <manuscript.docx / main.tex+main.pdf / manuscript.md>; review artifact: <none / review-preview.pdf / main.pdf>
- Submission constraints: <word/display/reference/checklist constraints and any non-submission-ready blockers>
- Structure vs article-type profile: <matches profile / canonical list -> adopted list with reasons>

Length Budget Summary:
- Active length unit: <words / pages / unresolved>
- target_length_budget: <official card/template/fallback ID, lower bound, upper bound, count scope>
- Page limit: <not specified / active page limit + source>
- Main-text word budget: <limit and source status>
- Abstract and Key Points Budget: <separate abstract/key-points limits or status; not counted in main text>
- Display/reference budget: <main display cap and reference cap>
- Section-budget arithmetic: <sum of planned section word budgets and compression rule>

Section Plan:

| # | Section | Role | Main content | Word budget | Evidence/source | Writing caution |
|---:|---|---|---|---:|---|---|
| 1 | Title / structured abstract | support | <one-line section message> | <n/a or words> | <source/evidence anchor> | <constraint or blocker> |
| ... | ... | ... | ... | ... | ... | ... |

Display-Item Plan:

| ID | Type | Layout | Section | Claim supported | Data/denominator | Evidence status |
|---|---|---|---|---|---|---|
| Tab. 1 | baseline table | editable Word table | Results | <claim supported> | <population/denominator> | <available / missing / TODO> |
| Fig. 1 | flow diagram | separate figure upload asset | Methods/Results | <claim supported> | <source> | <available / missing / TODO> |
| ... | ... | ... | ... | ... | ... | ... |

Statement/template/blocker summary:
- Statements: <ethics/consent/registration/data/code/funding/conflicts/contributions status>
- Template: <selected shell/template and verification status>; primary submission file: <...>
- Blockers: <none or concise list>

Decisions to confirm:
- Required: <exact target journal / article type / Submission Format Route / main-text budget /
  display budget / template status / statement blocker decisions that must be settled before paper/>
- Optional: <preview PDF, language variant, optional supplement or display preferences>

Unresolved blockers:
- <none, or concise blocker list that remains unresolved but does not change the next action>

Stage ledger:
- completed: Paper Framework
- not started: paper/, references.bib, manuscript.docx or main.tex/main.pdf, generated figures/tables, submission package

Example user replies:
- Confirm, proceed to paper/.
- Change: <specific section/table/budget/template decision>.
- Pause.

User action required: Please confirm whether to proceed to paper/, or what to change.
```

Every Paper Framework checkpoint must include Decisions to confirm, Unresolved blockers, and Example user replies. If exact target journal, article type, Submission Format Route, main-text budget, display budget, template status, or statement blockers remain unsettled, list them under Decisions to confirm rather than hiding them in prose. For Chinese terminal output, label these blocks `待确认决策`, `未解决阻塞项`, and `可直接回复`.

For Chinese terminal output, render `章节计划` as a Markdown table with this localized header:

```markdown
| # | 章节 | 角色 | 主要内容 | 字数预算 | 证据/来源 | 写作注意 |
|---:|---|---|---|---:|---|---|
```

Section Plan is mandatory terminal output; do not replace it with overview bullets, a slash-separated
section list, or prose such as `章节计划包含`. Section Plan must include a section-level word budget;
if a section is excluded from the main-text word budget, mark it `n/a` and explain why in the Length
Budget Summary.

For Chinese terminal output, render `篇幅预算` before `章节计划` with the active length unit, page-limit
status, main-text word budget, display/reference budget, and section-budget arithmetic. If the journal
uses a word limit rather than a page limit, state that directly instead of inventing pages.

For Chinese terminal output, render `图表计划` as a Markdown table with this localized header:

```markdown
| ID | 类型 | 版式 | 位置章节 | 支持的主张 | 数据/分母 | 证据状态 |
|---|---|---|---|---|---|---|
```

Display-Item Plan is mandatory terminal output; do not replace it with display count bullets, a prose
list such as `图表计划包含`, or source-check notes. Keep the table brief by showing only the main
planned displays; detailed display metadata remains in the saved framework artifact.

When the user requests changes at the Paper Framework gate, apply the changes to the framework
artifact and stay inside the same gate. Re-render the full checkpoint with the updated Section Plan
table and updated Display-Item Plan table before asking for confirmation again. Do not answer only
with a change summary, file path, or validation note.

Stop after this stage unless the framework has already been confirmed.
