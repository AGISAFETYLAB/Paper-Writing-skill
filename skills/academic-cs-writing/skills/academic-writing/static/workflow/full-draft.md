# Full Draft Workflow — Orchestrator

Use this workflow when the user provides a workspace or asks for a complete first paper draft from
project materials.

This file is the **orchestrator**: it owns the state machine, the two confirmation gates, the
re-entry logic, and the stage ledger. The detailed execution rules for each stage live in separate
fragments under `stages/`, and the figure/table, citation, and review/audit subsystems live in
sibling skills. Load each one only when its stage is reached.

## Stage And Subsystem Loading Map

| When you reach | Load |
|---|---|
| Writing Policy stage | `stages/writing-policy.md` |
| Paper Framework stage | `stages/paper-framework.md` |
| LaTeX project setup | `stages/latex-project.md` |
| Section drafting | `stages/section-drafting.md` |
| Any figure or table is produced | sibling skill **`academic-figure`** (figure/table handling, plot style, table design, QA) |
| A citation must be searched, written, or verified | sibling skill **`academic-citation`** (citation integrity, `audit_citations.py`) |
| The first complete `paper/` draft exists | sibling skill **`academic-review`** (Draft Completion Review Gate, Final Static Audits, Submission Readiness, Before-Returning checklist, `audit_draft.py`) |

The figure, citation, and review rules are **not duplicated here** — when a stage needs them, load
the sibling skill's `SKILL.md` and follow it. The orchestrator only says *when* each subsystem is
invoked; the subsystem owns *how*.

**Path convention (applies to this fragment and every `stages/*.md`):** a path beginning with
`_shared/` is relative to the **collection root** (the parent of `skills/`); a path beginning with
`references/` is relative to **this hub skill** (`skills/academic-writing/`); a sibling skill is
named (e.g. `academic-figure`) rather than path-referenced.

## State Machine

```text
Workspace
  -> Workspace Discovery
  -> Writing Policy
  -> User confirmation
  -> Paper Framework
  -> User confirmation
  -> Full Draft LaTeX Project
```

## Stage Outputs

Create each output only when its stage is reached and its upstream gate has been satisfied.

| Stage | Output |
|---|---|
| Writing Policy | `writing-policies/<paper-slug>-writing-policy.md`; optional complete translated sibling artifacts only when requested |
| Paper Framework | `writing-policies/<paper-slug>-paper-framework.md`; optional complete translated sibling artifacts only when requested |
| Full Draft | complete `paper/` LaTeX project with `main.tex`, `sections/*.tex`, `references.bib`, and `math_commands.tex`; add `paper/citation-evidence.md` when live citation search is performed |

## Execution Contract

| Stage | Required output | Hard stop |
|---|---|---|
| Writing Policy | `writing-policies/<paper-slug>-writing-policy.md` | **STOP HERE and wait for user response.** Do not generate Paper Framework until confirmed. |
| Paper Framework | `writing-policies/<paper-slug>-paper-framework.md` | **STOP HERE and wait for user response.** Do not create `paper/` until confirmed. |
| Full Draft | complete `paper/` LaTeX project | **Not complete until the closing gates pass, regardless of entry path (including re-entry from an existing policy+framework):** Draft Completion Review Gate (Round 1+2), Final Static Audits (`audit_citations.py` **and** `audit_draft.py` both `PASS`), Final Submission Readiness Gate, and Compliance Self-Check (all owned by the `academic-review` skill). Only then return generated files, unresolved markers, and citation/template/compile risks. Returning `paper/` before these gates pass is a workflow violation. |

**Completion means the whole chain, not a skeleton.** A request to "write the draft" / "produce the
first draft" / "help me write the paper" (写初稿 / 写论文 / 帮我写论文) is a request to complete the whole
chain in this same run — not to emit a marker-only outline.

**The full chain has four mandatory parts; all of them must run before the draft is returned:**

1. **Hub (this skill)** — drafts the prose through the pipeline (Writing Policy → Paper Framework →
   LaTeX project → per-section drafting).
2. **`academic-figure`** — generates, inserts, and QA-gates every planned figure and table.
3. **`academic-citation`** — searches, writes, and audits every needed citation and the bibliography.
4. **`academic-review`** — runs the closing review (Round 1 + Round 2), the Final Static Audits, and
   the Submission Readiness gate.

**Skipping or deferring any of these four parts is a workflow violation, not a shortcut the user
authorized.** Returning a draft whose figures, tables, or citations are left as `% FIGURE_NEEDED` /
`% TABLE_NEEDED` / `% CITATION_NEEDED` markers and deferring them to the user "for later via
academic-figure / academic-citation" is the most common form of this violation: `audit_draft.py` fails
on any leftover marker, so such a draft cannot pass the Final Static Audits and is not done. A marker
is reserved for evidence that genuinely does not exist (see `stages/section-drafting.md`), not for
producible work.

Mandatory gate behavior:

- A user request for a complete paper draft authorizes the workflow, not automatic passage through
  the gates.
- Do not "compress", "batch", "assume", or "silently satisfy" the Writing Policy or Paper
  Framework confirmation gates.
- After writing the Writing Policy, return only the concise policy summary, stage ledger, and the
  required user action. **STOP HERE and wait for user response.** Do not load venue cards, specific
  paper-type profiles, templates, section guides, figure/table references, citation references,
  style references, example references, or review references until the user
  confirms the Writing Policy. Ask exactly for confirmation or corrections to the Writing Policy
  before moving to Paper Framework.
- After writing the Paper Framework, return only the concise framework summary, stage ledger, and
  the required user action. **STOP HERE and wait for user response.** Do not create `paper/`, draft
  sections, generate figures/tables, or write BibTeX until the user confirms the Paper Framework.
  Ask exactly for confirmation or corrections to the Paper Framework before creating `paper/`.
- If the user asks for autonomous or one-shot full-draft generation, still stop at both gates. Treat
  the request as permission to complete each stage after confirmation, not as permission to skip
  confirmation.

## Re-entry: User Requests Changes At The Paper Framework Gate

If the last completed stage is Paper Framework and the user asks to change, revise, adjust, remove,
add, or reorder any section, figure, table, page budget, template, venue field, or open decision
before `paper/` exists, stay inside the Paper Framework gate. This is a Paper Framework gate
revision, not a generic file edit and not Draft Revision Workflow.

For this re-entry:

1. **Reload `stages/paper-framework.md`.** Apply its terminal checkpoint schema again; do not rely on
   memory of the previous checkpoint.
2. **Update the saved framework artifact first**, preserving the saved artifact schema.
3. **Re-render the terminal checkpoint in full before asking for confirmation again.** The terminal
   response must include the updated Section Plan table and updated Figure Plan table, localized to
   the interaction language. This is true even when the user changed only one figure/table, one
   section, or one budget number.
4. **Do not answer with only a change list.** A bullet summary, file path, validation note, or "file
   updated" message is not a checkpoint. It may appear only as a short preface before the two
   required tables, not as a substitute for them.
5. **Do not create `paper/` after a revision request** until the user confirms the revised tables.

In Chinese terminal output, the revised checkpoint still needs the `章节计划` Markdown table and the
`图表计划` Markdown table from `stages/paper-framework.md`; it is not a bullet summary.

## Re-entry: Resuming From a Confirmed Writing Policy + Paper Framework

A very common request is **"the Writing Policy and Paper Framework already exist — just generate the
paper"** (or "regenerate `paper/`"). This enters the workflow at the **Full Draft LaTeX Project**
stage. Re-entry **skips only the two confirmation gates** (the policy and framework are already
confirmed) — it does **not** skip the drafting discipline or the closing gates. Treat a re-entry
request exactly like reaching the Full Draft stage through the linear flow.

When entering at the Full Draft stage:

1. **Load and trust the confirmed artifacts.** Read the existing `writing-policies/<slug>-writing-policy.md`
   and `writing-policies/<slug>-paper-framework.md`. If either is missing, ambiguous, or was never
   confirmed, do **not** invent it — fall back to the appropriate earlier stage and its confirmation
   gate. If the framework conflicts with the current workspace evidence on a decision that changes
   paper identity/claims, stop and ask.
2. **Load the paper/ drafting fragments and subsystems — they are NOT optional on re-entry.** Creating or
   regenerating `paper/` requires the same material the linear flow loads while drafting:
   `_shared/templates/index.md` (Template Acquisition — local-first via `stages/latex-project.md`),
   the per-section guides for every section being written (`references/sections/<section>.md` +
   `references/sections/paragraph-flow.md` via `stages/section-drafting.md`), and the
   **`academic-figure`** skill whenever any figure/table is produced (this is where the table
   width/overflow, column-type, and appendix placement/ordering rules live). Skipping these is the
   direct cause of tables overflowing (`r`/`l` prose columns), wide matrices left single-column, and
   a dropped or sparse/scrambled appendix.
3. **Run the LaTeX Project Setup, Section Drafting, and (via `academic-figure`) Table/Figure Handling
   steps** exactly as in the linear flow.
4. **Run the closing gates unconditionally** via the **`academic-review`** skill — the Draft
   Completion Review Gate (Round 1 + Round 2), the Final Static Audits BLOCKING GATE
   (`audit_citations.py` and `audit_draft.py` must both report `PASS`), the Final Submission Readiness
   Gate, and the Compliance Self-Check (Before Returning).
   **These bind to any `paper/` output regardless of how the stage was entered.** A re-entry that
   produces `paper/` without these gates is a workflow violation, not a shortcut the user authorized.

The user saying "policy and framework are done, just build the paper" authorizes skipping the two
*confirmation* checkpoints — it never authorizes skipping the section guides, the table/figure
rules, or the closing audits/review.

At every stage, keep a brief stage ledger in the user-facing summary: output artifact, decisions
needing confirmation, unresolved paper blockers, and next required user action. Do not make a
checkpoint summary primarily about process mechanics, file existence, line counts, or which folders
were avoided.

Do not create a separate confirmation file. User approval happens through the conversation
checkpoint summary.

## 1. Intake And Workspace Discovery

Ask only the most blocking question. If the user provides a workspace path, use it. If the
workspace is ambiguous, ask for the paper project workspace.

Minimum discovery targets:

- venue kind (`conference` or `journal`; default `conference` unless the user explicitly specifies
  journal),
- paper type,
- core contribution and central claim,
- evidence boundary: available results, source evidence, and unsupported claims,
- key terms and naming conflicts,
- disclosure boundary: internal identifiers that must be renamed for publication (checkpoint /
  training-run / sweep / wandb names, internal tool names, unreleased model names) and entities the
  authors do not want in the paper (withheld baselines or competing methods, internal tools,
  unreleased datasets, partner/product names),
- source conflicts affecting claims, evidence, terminology, or paper identity.

Optional context, record only when visible:

- target venue, otherwise `generic / venue TBD` under `venue_kind=conference`,
- existing draft files and progress,
- figures, tables, bibliography, code/data artifacts,
- Image Renderer Preference for picture figures: user-configured `GPT-image2`, user-configured
  `Gemini`, current executing agent, or other explicit renderer,
- style sources or previous papers supplied by the user,
- existing weakness or review notes found in workspace materials.

Inspect compact, high-signal files before large logs or source trees:

- `NARRATIVE_REPORT.md`, `STORY.md`, `PAPER_PLAN.md`, `CLAIMS_FROM_RESULTS.md`
- `EXPERIMENT_LOG.md`, `EXPERIMENT_TRACKER.md`, `findings.md`
- `docs/research_contract.md`, `README.md`, `CLAUDE.md`, `AGENTS.md`
- `paper/`, `sec/`, `sections/`, `*.tex`, `*.bib`
- `results/`, `outputs/`, `figures/`, `tables/`, `logs/`, `configs/`
- JSON, CSV, TSV, Markdown result tables, manifests, metric scripts, baseline configs, and raw
  result or annotation files.

If no usable workspace evidence exists, ask the user for a 3-5 sentence contribution and evidence
summary before writing the Writing Policy. Do not infer a paper story from an empty workspace or
from generic repository metadata.

Do not run environment setup, dependency installation, registry smoke checks, benchmark execution,
or `.venv` creation during Writing Policy generation. Writing Policy may read scripts, configs,
metadata, and existing result files as evidence, but it should not execute experiments or test the
runtime unless the user explicitly asks for execution verification.

## 2. Full Draft Clarification Boundaries

Use the global Clarification Protocol from `_shared/core/gates.md`. The global protocol decides
whether to ask; this section decides which Full Draft stage owns the question.

Stage boundaries:

| Stage | Ask now only for | Defer or default |
|---|---|---|
| Writing Policy | paper identity, core story, claim/evidence boundary, key terminology, disclosure boundary (internal names to rename, entities to withhold) when an exclusion could affect comparison honesty, decisive source conflict | venue kind defaults to conference unless explicit journal; venue if unspecified, page budget, section order, figure placement, caption wording, optional ablations |
| Paper Framework | user-required venue-specific planning with missing/contradictory venue, missing official/preloaded template, blocking Writing Policy decision that changes section structure | template choice, page budget, section order, and figure/table plan when the agent can choose conservatively |
| Section Drafting | facts needed to write the section correctly without false claims | weaken the claim, defer the decision, or insert a precise LaTeX marker |

Ask about venue at most once. If the user does not explicitly specify journal, set
`venue_kind=conference`. If venue is unspecified, use `generic / venue TBD` and
`generic_article.tex (non-submission single-column draft template)`.

Ask at most 1-3 questions per round. Normal Writing Policy generation should need at most one round.

Prefer confirm/correct questions over open-ended questions:

```text
Before Writing Policy, I need one decision: should this be treated as a method paper?
I infer method paper from the README and ablation-heavy results. Please confirm or correct.
Default if unanswered: use `method-paper.md` because the evidence strongly supports it; correct this
before Paper Framework if the paper identity is different.
```

## Stage Execution

Proceed through the stages in order, loading each fragment as you reach it:

1. **Writing Policy** → `stages/writing-policy.md` (ends at a blocking confirmation gate)
2. **Paper Framework** → `stages/paper-framework.md` (ends at a blocking confirmation gate)
3. **Full Draft LaTeX Project**:
   - `stages/latex-project.md` — project setup, template acquisition, core section budget
   - `stages/section-drafting.md` — per-section drafting loop, citation triggers, writing rules
   - **`academic-figure`** skill — every figure and table
   - **`academic-citation`** skill — every searched/written/verified citation and the bibliography
   - **`academic-review`** skill — the closing review + audits + submission readiness, run
     unconditionally before any `paper/` is returned
