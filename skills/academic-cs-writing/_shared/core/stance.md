# Core Stance

Apply these rules to every writing job regardless of workflow.

## Language Policy

**⚠️ The agent MUST mirror the user's interaction language.** This is a hard rule,
not a preference. If the user writes in Chinese, the agent MUST respond in Chinese
for all conversation output: clarification questions, checkpoint summaries, status
updates, policy rationale, self-review notes, and warnings. Technical terms in
English are preserved.

- File paths, shell commands, LaTeX commands, BibTeX keys, citation keys, template names,
  schema fields, and machine-parsed markers stay in their original language.
- Paper prose is English academic prose by default, regardless of interaction language.
- Terminal-facing checkpoint summaries mirror the user's interaction language, including Writing
  Policy and Paper Framework overviews, section summaries, Figure Plan summaries, risks, and user
  action requests. Do not use the artifact language as the terminal interaction language.
- Treat the framework overview, Section Plan, Figure Plan, decisions, blockers, and confirmation
  request shown in the terminal as conversation output: localize their labels and natural-language cells to the user's interaction language while preserving paths, IDs, code, LaTeX, BibTeX keys, and
  manifest values. Only the Section Plan and Figure Plan are mandatory terminal Markdown tables. Do not render Display-Item Page Budget as a terminal table; keep display-item page costs in the saved Paper Framework artifact and summarize only blockers or required decisions in prose. For terminal
  Figure Plan tables, chart-form cells are human-facing and should be localized to the interaction
  language; the saved artifact may keep canonical English chart-form values.
- Full Draft Workflow outputs a venue-formatted English LaTeX paper project when a target venue is
  confirmed; otherwise it outputs a non-submission generic English LaTeX draft. Do not generate a
  Chinese or Chinese-English parallel paper unless the user explicitly requests it.
- Saved Writing Policy and Paper Framework artifacts stay English by default. Before each stage,
  ask about additional full-language artifact versions only when the question can be batched with
  another required clarification; otherwise default to English only. If the user asks for another
  language, create a complete same-content translated sibling artifact such as
  `writing-policies/<paper-slug>-writing-policy.zh-CN.md` or
  `writing-policies/<paper-slug>-paper-framework.zh-CN.md`. The translated artifact must preserve
  the same sections, tables, claims, page budgets, figure plans, and open decisions; only the natural
  language changes.
- Do not create separate confirmation files. User approval happens through the conversation
  checkpoint summary.
- Draft Revision Workflow may include an interaction-language explanation when useful. Add a
  parallel-language version only when the user requests it or when it is necessary to verify intent.

## User-Facing Output Contract

Default to user-facing outputs. Load and check only the artifacts available in the selected
workflow.

In Full Draft Workflow, return the confirmed artifacts and the complete `paper/` LaTeX project
specified by the workflow fragment. Do not output paragraph-role reports, claim-evidence maps,
or review tables by default.

During Full Draft Workflow, infer from workspace materials first, then ask the user directly only
for decisive unknowns or decisive conflicts at the stage they affect. Writing Policy questions are
limited to paper identity, central claim, evidence boundary, key terminology, and central result
conflicts. Venue/template questions are deferred to Paper Framework unless the user already supplied
them. Ask about venue at most once; if the user has not specified one, use `generic / venue TBD`
with `generic_article.tex` as a non-submission single-column draft template and do not ask again
unless the user proactively changes the venue. In this fallback, use a soft drafting budget of 6-8
main-text pages, excluding references and appendix; do not call it a venue page limit or
submission-ready format. Treat non-decisive uncertainty as an assumption, default, deferred decision,
or drafting note.

When figures or tables are needed, use the Figure Plan in the Paper Framework and the
`academic-figure` skill's `references/figures/figure-planning.md`. The Figure Plan must declare the
layout target for each figure or table (`single-column`, `double-column`, `appendix`, or
`supplement`) before drafting. Use a configured paper-figure MCP only for figure classification,
FigureSpec skeletons, validation, rendering, or figure metadata; do not let figure tooling invent
claims or results.
For Full Draft data-driven plots, data-driven plots default to Python and are drawn directly by the
current agent from workspace result files. For non-data picture or illustration figures, always
create a Picture Brief at `paper/figures/prompts/<figure-id>.md` before any rendering attempt. If
the user explicitly configures a picture API such as GPT-image2 or Gemini, use that renderer after
the brief; otherwise the current executing agent draws the picture from the brief and inserts it.

In Draft Revision Workflow, output revised text plus necessary notes. Do not generate a Writing
Policy, Paper Framework, or files by default. For section-level revisions, run the internal Section
Drafting Protocol in the workflow fragment: build a compact Section Plan, Paragraph Plan, reverse
outline, and claim-evidence check internally, but do not show those internal artifacts unless the
user asks, the task is diagnostic/review-oriented, or a blocking evidence/citation risk must be
surfaced.

Keep internal checks internal unless the user asks for reasoning, debug output, or a formal review,
or unless a blocking evidence/citation issue remains unresolved.

## Mechanical Non-Negotiables (always in effect)

These hard rules apply to every generated paper regardless of which reference files are loaded. They
are repeated in the workflow fragments, but they hold even if a fragment is not loaded.

- **No `\footnote{...}` in prose.** Move the content inline or delete it.
- **No file names or code artifacts in prose.** Do not write `\texttt{*.json}`, `\texttt{*.py}`,
  `\texttt{*.csv}`, or raw code identifiers; use descriptive natural language.
- **No local filesystem paths or directory names in prose.**
- **No internal identifiers in prose, captions, tables, or figures.** Checkpoint tags,
  training-run / sweep / wandb names, internal tool names, and unreleased model names (e.g. a
  `..._step380` tag) are scaffolding, not publication names. Write the public display name from the
  Naming Map instead; the internal identifier must never appear.
- **No do-not-disclose entities anywhere.** Entities the user withholds (a withheld baseline or
  competing method, an internal tool, an unreleased dataset, a partner/product name, a
  not-for-publication result) must not appear — not positively, not in passing, and **not by
  negation or exclusion** (never "the protocol that excludes X" or "unlike X"). Suppressing a name
  must not turn a comparison claim into a misleading one; if it would, stop and ask (contract point 7).
- **No leftover missing-support markers** (`% CITATION_NEEDED`, `% EVIDENCE_NEEDED`,
  `% FIGURE_NEEDED`, `% TABLE_NEEDED`) in a draft called clean; list any that remain in the summary.
- **Paper-type profile is the default structure** (Full Draft): match its section list and count;
  surface and justify every deviation at the Framework checkpoint.
- **Subsection budget:** 0 subsections for short sections, at most 4 per main section.
- **Run the static gates before declaring a draft clean:** the `academic-citation` skill's
  `scripts/audit_citations.py` and the `academic-review` skill's `scripts/audit_draft.py` must both
  report `PASS`.

## Integrity Rules

- Do not fabricate citations.
- If a citation has not been verified against source content, mark it as `not verified`.
- Do not claim that a paper supports a point unless the source content has been checked.
- Weaken or remove claims that are not supported by available evidence.
- Treat metrics as evidence for research questions, not decorative numbers.
- Learn structure, density, and rhetorical moves from user/reference papers; do not copy distinctive phrasing.
