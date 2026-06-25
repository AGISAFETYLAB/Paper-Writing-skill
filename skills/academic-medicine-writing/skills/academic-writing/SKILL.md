---
name: academic-writing
description: Use when planning, drafting, revising, or reviewing a medical, clinical, biomedical, public-health, diagnostic, treatment, cohort, prediction-model, systematic-review, case-report, or health-economics paper with study-type, reporting-guideline, statement, citation, figure/table, or submission-readiness constraints.
---

# Academic Medicine Writing — Hub

This hub owns the medical writing pipeline:

`workspace -> Writing Policy -> Paper Framework -> Manuscript Package -> reviewed submission package`

It owns orchestration and medical prose. It delegates specialized work to sibling skills:

- `../academic-figure/SKILL.md` for every clinical figure and table.
- `../academic-citation/SKILL.md` for biomedical citations, Vancouver/AMA references, and citation audits.
- `../academic-review/SKILL.md` for checklist compliance, statements, and final submission readiness.

The hub says when to invoke each sibling; the sibling owns how. Do not duplicate figure, citation, or
review rules here. Do not apply the writing logic from memory; load the files on disk.

Do not fragment full-draft orchestration into section-only micro-skills or ad hoc writing helpers. The hub remains the single state-machine owner: it decides when the workflow is at Writing Policy, Paper Framework, Manuscript Package, section drafting, display production, citation audit, and review gates.
Section-level, figure, citation, and review skills are delegated subsystems, not competing workflow
entry points.

## Scope: Writing Only, Never Research Or Medical Advice

This skill writes and revises manuscript artifacts. It does not provide medical advice, run research,
or change the study design. Apply `../../_shared/core/stance.md` and
`../../_shared/checks/research-veto.md` for the full no-fabrication and claim-boundary contract instead
of restating it in each workflow file.

## Critical Decision Rule: STOP, NEVER GUESS

When a decision materially affects paper identity, study type, reporting checklist, article type,
target journal/template, central claim, endpoint definition, analysis population, ethics/consent,
trial registration, data sharing, or whether a result exists, stop and ask. Do not silently default
past a decision that could create false clinical meaning or force a large rewrite.

Ask the smallest possible question. If the missing fact can be safely marked unknown without
changing manuscript structure, proceed with an explicit unknown. If the missing fact changes study
type, checklist, title/abstract claim strength, or submission package, wait for the user's answer.

## Interaction Language Rule

Mirror the user's interaction language in conversation output, checkpoint summaries, warnings, and
status notes. If the user writes in Chinese, answer in Chinese. Manuscript prose remains English by
default unless the user asks otherwise. File paths, LaTeX commands, citation keys, registry IDs, and
source titles stay in their original form. Terminal-facing checkpoint summaries follow the user's
interaction language even when the saved Writing Policy / Paper Framework artifact is English by
default. This rule is not overridden by any other policy.

## Template Provenance Rule

Medical journals often specify article structure rather than a dedicated LaTeX class. Use
package-local templates only as provenance-labeled manuscript shells unless
`../../assets/templates/index.md` marks a file as an official downloaded template.

- JAMA-style Original Investigation defaults to a Word-first manuscript package with
  `paper/manuscript.docx` as the primary submission file. The local
  `../../assets/templates/jama_original_investigation.tex` file is only an optional
  instruction-derived review shell; it is not an official JAMA class or required submission template.
- Word-first routes use this selection order:
  preloaded official Word template -> user-provided official template -> official web fetch ->
  package-local generic Word reference shell. The package-local
  `../../assets/templates/word/generic-medical-word-reference.docx` file is a reference shell, not an
  official Word template. JAMA/JAMA-style routes must not claim an official Word template unless the
  user supplies one or an official source provides one.
- Nature Portfolio / Springer Nature journal submissions may use the official downloaded Springer
  Nature journal article template at
  `../../assets/templates/springer-nature-latex/sn-article-template/sn-article.tex` with
  `sn-jnl.cls`.
- For any named target journal, verify current official instructions before saying
  submission-ready. Record source URL and date checked in `paper/submission-package.md`.

Do not web-fetch if a suitable official downloaded template already exists locally. Web fetch is
allowed only for a named target journal with no local official or user-provided template.

## Routing Protocol

### 1. Load the manifest and core layer

Read `manifest.yaml`, then read every file listed under `always_load`:
`../../_shared/core/stance.md`, `../../_shared/core/gates.md`, and
`../../_shared/core/output-format.md`. These hold the medical stance, gates, and output contract.

### 2. Route into exactly one workflow

#### Workflow Intent Classifier

Classify the user's intent before loading a workflow. Use exactly one intent class:

| Intent class | Trigger | Route | Output scope |
|---|---|---|---|
| `full-draft-from-evidence` | User gives a work directory/source materials and asks to write, generate, or start a first medical manuscript. | `full-draft` | Build a complete draft package from evidence after the two confirmation gates. |
| `package-completion` | A partial `paper/`, incomplete manuscript package, or confirmed policy/framework already exists and the user asks to continue, complete, fill missing parts, or generate the rest. | `full-draft` re-entry | Complete existing package components from the earliest missing stage. |
| `draft-revision` | Existing prose, section, manuscript, Word, Markdown, or LaTeX is supplied and the user asks for polish, rewrite, compression, diagnosis, or local text checking. | `draft-revision` | Revise within the requested edit boundary; do not create a new package unless asked. |
| `figure-table-only` | The user only asks to create, revise, plan, or audit a figure, table, caption, flow diagram, or display set. | `academic-figure` | Produce or audit display artifacts only. |
| `citation-only` | The user only asks for reference search, bibliography repair, citation formatting, or citation audit. | `academic-citation` | Produce or audit citation artifacts only. |
| `submission-review` | The user asks to review/check an existing package for submission readiness, reviewer risk, checklist compliance, or final gates. | `academic-review` | Audit the existing package; do not generate a new first draft. |

If source evidence and an old manuscript/package coexist and the user intent is unclear, ask one route-selection question and stop. The concrete options should be clean-slate from evidence,
complete existing package, revise existing package, audit existing package, figure/table-only,
citation-only, or submission-review as applicable.

Decide the `workflow` axis before writing:

- `full-draft`: the user provides a workspace/source materials or asks for a complete first medical
  manuscript, or the user asks to complete a partial package.
- `draft-revision`: the user provides existing prose or LaTeX and asks to revise,
  polish, compress, diagnose, or prepare a version.
- `revision-response`: the user provides reviewer comments, editor decision letters, revision notes,
  or asks for a point-by-point response package, response letter, or resubmission plan.

If ambiguous and the route affects outputs, ask one concise question and stop. Then load
`static/workflow/full-draft.md`, `static/workflow/draft-revision.md`, or
`static/workflow/revision-response.md`.

### 3. Detect medical axes

Detect `study_type` before strengthening claims, choosing section moves, planning displays, or
selecting a reporting checklist. Use the manifest values: CONSORT, SPIRIT, STROBE, PRISMA, STARD,
TRIPOD, CARE, GATHER, or CHEERS. If two checklists plausibly change manuscript structure, ask.

Detect `section` only when drafting/revising a named section or creating a full manuscript. Load
`references/sections/index.md`, `references/sections/paragraph-flow.md`, the
section-specific guide under `references/sections/`, and the checklist card needed for that
section.

### 4. Build using the loaded material

Apply loaded material in this order:

1. Core stance and gates: scope, language, clarification, and integrity rules.
2. Workflow fragment: full-draft orchestrator or draft-revision workflow.
3. Stage fragments as reached: Writing Policy, Paper Framework, Manuscript Package, Section Drafting.
4. Package references on demand: templates, journal standards, statements, checklists, examples.

### 5. Delegate sibling subsystems

Invoke sibling skills whenever the stage needs them:

- Any clinical figure, table, flow diagram, or supplement display -> `academic-figure`.
- Any searched/written/verified citation, guideline source, registry source, or bibliography audit
  -> `academic-citation`.
- The first complete `paper/` draft exists, or a submission-readiness/checklist review is requested
  -> `academic-review`.

The returned full draft is always the reviewed, revised, format-specific, and
submission-package-checked draft. A Markdown-only output is allowed only when explicitly requested.
