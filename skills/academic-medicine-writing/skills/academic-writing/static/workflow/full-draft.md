# Full Draft Workflow — Medicine

Use when the user provides source materials or a workspace and wants a complete medical manuscript,
or when an existing manuscript package is incomplete and the user asks to finish it.

Intent classes covered: `full-draft-from-evidence` and `package-completion`.

This file is the orchestrator. It owns the state machine, the two confirmation gates, re-entry
rules, stage ledger, and submission-standard gate. Detailed stage execution rules live in
`stages/`. Figures/tables, citations, and review/audits are delegated to sibling skills.

Use centralized contracts before expanding this orchestrator:

- Use the centralized Input Sufficiency Check in `../../_shared/core/gates.md`.
- Use the Route Output Template in `../../_shared/core/output-format.md`.
- Apply core stance and Research veto instead of restating the no-fabrication list:
  `../../_shared/core/stance.md` and `../../_shared/checks/research-veto.md`.
- Use `../../_shared/core/package-gates.md` for `workflow-state.json`, behavior eval assertions, and
  the aggregate package gate.

## Stage And Subsystem Loading Map

| When you reach | Load |
|---|---|
| Writing Policy stage | `stages/writing-policy.md` |
| Paper Framework stage | `stages/paper-framework.md` |
| Manuscript Package setup | `stages/manuscript-package.md` |
| Section drafting | `stages/section-drafting.md` |
| Workflow state or aggregate package gate | `../../_shared/core/package-gates.md` |
| Any figure, table, flow diagram, checklist table, or supplement display is produced | sibling skill `academic-figure` |
| Any citation, reporting guideline source, registry source, or bibliography entry is searched, written, or verified | sibling skill `academic-citation` |
| The first complete `paper/` manuscript package exists | sibling skill `academic-review` |

The sibling skills own how their subsystem works. This orchestrator only decides when they must be
loaded. A path beginning with `../../references/` is package-local to
`academic-medicine-writing/`; a path beginning with `static/workflow/` is local to this hub skill.

## State Machine

```text
Workspace / source evidence
  -> Workspace Discovery
  -> Writing Policy
  -> User confirmation
  -> Paper Framework
  -> User confirmation
  -> paper/ Manuscript Package
  -> figure/table + citation + review gates
  -> format-specific production gate
  -> aggregate package gate (`../academic-review/scripts/audit_submission_package.py`)
  -> submission package + official-source gate

partial `paper/` or incomplete manuscript package
  -> Workspace Discovery
  -> Package Completion Intake
  -> earliest missing stage
  -> missing package components
  -> figure/table + citation + review gates
  -> format-specific production gate
  -> aggregate package gate (`../academic-review/scripts/audit_submission_package.py`)
  -> submission package + official-source gate
```

## Stage Outputs

| Stage | Output |
|---|---|
| Writing Policy | `writing-policies/<slug>-writing-policy.md` with medical claim boundary, study type, target article type, selected article type profile path, reporting checklist, ethics/registration/data-sharing unknowns |
| Workflow State | `writing-policies/workflow-state.json` during checkpoints, then `paper/workflow-state.json` after package creation, using schema version `medicine-workflow-state-v1` |
| Paper Framework | `writing-policies/<slug>-paper-framework.md` with article type profile structure comparison, IMRaD/article-type section plan, item-level checklist matrix, display-item plan, citation plan, Submission Format Route, and template choice |
| Package Completion Intake | A concise inventory of existing `paper/`, `writing-policies/`, source evidence, missing route artifacts, unresolved blockers, and the earliest missing stage; save it in `paper/package-completion-intake.md` when `paper/` exists |
| Full Draft | Complete `paper/` Manuscript Package: route-appropriate manuscript source (`paper/manuscript.docx` for `word-first`, `paper/main.tex` + `paper/main.pdf` for `latex-first`, or `paper/manuscript.md` for `generic-review`), references, figures/tables, checklist/statement text, and `paper/submission-package.md` |

## Execution Contract

| Stage | Required output | Hard stop |
|---|---|---|
| Writing Policy | `writing-policies/<slug>-writing-policy.md` | **STOP HERE and wait for user response.** Do not generate Paper Framework until confirmed, unless an existing policy has already been confirmed. |
| Paper Framework | `writing-policies/<slug>-paper-framework.md` | **STOP HERE and wait for user response.** Do not create `paper/` until confirmed, unless an existing framework has already been confirmed. |
| Full Draft | Complete `paper/` Manuscript Package | Not complete until figures/tables, citations, review, the route-appropriate production artifact, submission package, and official-source checks pass or are reported as blocking risks. |

Every first-draft package must run the submission-ready check before it is returned. The
submission-ready verdict may be `PASS` or `BLOCKED`; `BLOCKED` is expected when target-journal,
ethics/registration, author, data-sharing, template, figure, citation, or production facts remain
unknown or unresolved. Skipping the submission-ready check is a workflow failure. A complete draft
package is not automatically submission-ready, but it must include the submission-ready verdict and
the blockers that prevent PASS.

After specialized figure, citation, review, production, and local-path checks have run, run:

```bash
python ../academic-review/scripts/audit_submission_package.py paper
```

This aggregate gate must pass for internal consistency even when the final
`Submission-readiness verdict` remains `BLOCKED`.

`full-draft-from-evidence` means complete draft package, not submission-ready. `package-completion`
means complete existing package components from the earliest missing stage, not lightly polish prose
or re-run every gate that has already been explicitly confirmed and remains consistent.

Completion means the whole chain, not a skeleton. A request to "write the draft", "produce the
medical manuscript", "help me write the paper", "写论文", or "医学论文初稿" is a request to complete the
whole chain in this run, while still respecting the two confirmation gates. A request to complete
existing package content means fill missing package artifacts, rerun affected checks, and preserve
confirmed decisions unless they conflict with the current evidence.

The full chain has four mandatory parts:

1. Hub writing: Writing Policy -> Paper Framework -> Manuscript Package -> section drafting.
2. `academic-figure`: every clinical figure/table, flow diagram, baseline table, outcome table,
   adverse-event table, diagnostic/prediction plot, forest plot, and checklist/supplement display.
   For source-supported observational cohort drafts, this includes the minimum visual display set and
   table aesthetics gate.
3. `academic-citation`: every needed source, reporting guideline, registry source, target-journal
   instruction, and bibliography entry.
4. `academic-review`: manuscript completeness, checklist compliance matrix, statement audit,
   medical claim audit, visual display gate, table aesthetics audit, official-source gate, and final
   submission-readiness verdict.

Maintain `workflow-state.json` throughout this chain. It records `medicine-workflow-state-v1`,
confirmed gates, `study_type`, `article_type`, `submission_format_route`, required displays,
required audits, and current `blocking_gaps`. It is not a prose substitute: update it only from
confirmed checkpoints, source-supported package facts, and audit outputs.

## Draft Length Gate

A complete full draft must be close to the confirmed Paper Framework's active length budget, not
merely below the journal maximum. For word-budgeted medical articles, count the main text from
Introduction through Conclusions, excluding abstract, Key Points, tables, figures, article
information, references, and appendices.

- Record `Actual main-text word count` in `paper/submission-package.md`.
- Record the active `target_length_budget` source, lower bound, upper bound, and count scope in
  `paper/submission-package.md`.
- Record `draft length gate: PASS` only when the main text is within the framework budget band, or
  when a deliberate under-target is justified by missing evidence that cannot be invented.
- If `target_length_budget` uses official maximum plus field-convention completion floor, the maximum
  is still hard and the floor is the expected completion target unless evidence is genuinely missing.
- For JAMA-style Original Investigation with an approximately 3000-word main-text budget, a
  reviewable full draft should normally be at least 2500 main-text words and no more than 3000 main
  text words.
- If the draft is below the lower bound and evidence exists, expand evidence-supported sections
  before compiling. Do not pad with generic disease burden, unsupported clinical claims, or repeated
  synthetic-data disclaimers.

Never return a full medical draft with unresolved producible markers such as `CITATION_NEEDED`,
`TABLE_NEEDED`, `FIGURE_NEEDED`, missing ethics/registration/data-sharing statement text, or a
missing route-required production artifact. If the evidence genuinely does not exist, weaken/remove
the claim or leave a precise blocking marker and report it as a risk, not as routine follow-up.

Mandatory gate behavior:

- Do not compress, batch, or silently satisfy the Writing Policy or Paper Framework confirmation
  gates.
- Mirror the user's interaction language at both confirmation gates. `STOP HERE and wait for user
  response` is an internal gate marker, not terminal-facing text. In Chinese conversations, render the stop line as Chinese, for example: `在此停止并等待你的确认。`
- After Writing Policy, return only a concise medicine policy checkpoint: policy snapshot first,
  then stage ledger, top unresolved risks if not already covered, and the required user action.
  The checkpoint must show the policy content before process status. Do not lead with workflow
  completion, file path, line count, validation status, or source URLs. **STOP HERE and wait for
  user response.** Do not generate Paper Framework until confirmed. Do not load journal standard cards,
  templates, section examples, figure/citation references, or review references until the user
  confirms. Writing Policy checkpoints must include Confirmation Matrix, Workflow Progress, and Example user replies, so the user can see what is confirmed, inferred, required, blocking,
  optional, and what exact response will move the workflow forward.
- After Paper Framework, return only a concise medicine framework checkpoint: framework overview first,
  then the length budget and section-level word budget, the Section Plan table and Display-Item Plan table,
  statement/template/blocker summary, stage ledger, and required user action. The checkpoint
  must show the planned manuscript content before process status. Do not lead with workflow
  completion, file path, line count, validation status, or source URLs. **STOP HERE and wait for user
  response.** Do not create `paper/`, draft sections, generate figures/tables, or write BibTeX until
  the user confirms. Do not create `paper/` until confirmed. Paper Framework checkpoints must include Decisions to confirm, Unresolved blockers, and Example user replies, especially for target journal,
  article type, Submission Format Route, length/display budgets, template status, and statement
  blockers.
- If the user asks for autonomous or one-shot full-draft generation, still stop at both gates. The
  request authorizes the workflow; it does not authorize skipping confirmation.

## Re-entry: Resuming From a Confirmed Writing Policy + Paper Framework

When the user says the Writing Policy and Paper Framework already exist and asks to generate or
regenerate `paper/`, enter at the Full Draft Manuscript Package stage. Re-entry skips only the two
confirmation checkpoints; it does not skip drafting discipline or closing gates.

For `package-completion`, first run Package Completion Intake. If `paper/` exists but is partial,
inventory manuscript source, references, display assets, checklist matrix, statement files, review
report, production audit output, and `paper/submission-package.md`. Then resume from the earliest
missing stage. If confirmed policy/framework artifacts are absent or too thin to determine section
budgets, display plan, article type, or Submission Format Route, rebuild or repair the missing
framework checkpoint before drafting new package material.

On re-entry:

1. Read and trust the confirmed policy and framework. If either is missing, ambiguous, or conflicts
   with current source evidence on paper identity, study type, endpoint, analysis population, or
   target journal, stop and ask.
   If an existing Paper Framework lacks section-level word budgets, a Length Budget Summary, or a
   display-item plan with source status, repair the framework artifact first and re-render the
   framework checkpoint before drafting. Do not use an old short framework as permission to produce
   a short scaffold.
2. Load `stages/manuscript-package.md`, `stages/section-drafting.md`, `../../_shared/submission/templates.md`,
   `references/sections/index.md`, `references/sections/paragraph-flow.md`, the selected
   checklist card, the selected item JSON under `../../_shared/checklists/items/`, and the
   sibling skills as needed.
3. Produce the complete `paper/` package, not only a single manuscript file.
4. Run the `academic-review` closing gates unconditionally before returning `paper/`.

The user saying "policy and framework are done" authorizes skipping confirmation only. It never
authorizes skipping figures/tables, citations, checklist/statements, route-specific production,
or submission-package review.

Keep a brief stage ledger in user-facing summaries: output artifact, decisions needing confirmation,
unresolved blockers, and next required user action. Do not make checkpoint summaries primarily about
process mechanics, file existence, line counts, which files were read, source-check details, or
folders avoided.

## Intake And Workspace Discovery

Ask only the most blocking question. If the user provides a workspace path, use it. If no usable
workspace evidence exists, ask for a 3-5 sentence study and evidence summary before writing the
Writing Policy.

### Workspace Discovery Questions

During workspace discovery, do not silently choose among plausible workspace meanings. If the
workspace contains source evidence plus an existing manuscript or paper package, list the issue under
Workspace Discovery Questions and ask the user to choose the intended route before Paper Framework.

Trigger a user-choice question when any of these are found:

- an existing manuscript or paper package such as `paper/`, `manuscript_*`, `main.tex`,
  `manuscript.docx`, `submission-package.md`, `review-report.md`, or prior `writing-policies/`;
- a source-evidence conflict, for example README says no manuscript-specific artifacts but the
  directory contains `manuscript_jama_network_open/` or another manuscript package;
- multiple plausible evidence roots, output roots, target-journal packages, or prior drafts;
- target journal is a family name such as `JAMA` but the exact JAMA-family journal affects route,
  word/display/reference limits, or file format;
- source evidence supports both a clean new paper and a revision/audit of an existing package.

For these cases, the checkpoint must ask the user to choose one of the concrete routes:

- `clean-slate from evidence`: ignore old paper artifacts and build Writing Policy from experiment
  evidence only;
- `complete existing package`: run Package Completion Intake, keep consistent confirmed decisions,
  and fill the missing `paper/` components from the earliest missing stage;
- `revise existing package`: use the existing manuscript package as draft material and enter
  `draft-revision` or later full-draft re-entry;
- `audit existing package`: route to `academic-review` before writing new policy/framework;
- `use existing policy/framework`: resume only if the existing policy/framework is explicitly
  confirmed and consistent with source evidence.

Do not silently choose clean-slate from evidence, revise existing package, or audit existing package
when an existing manuscript package creates ambiguity. If the user already gave an explicit clean
slate instruction, record that as confirmed; otherwise ask the user to choose.

Minimum discovery targets:

- target article type and journal status, otherwise `medical journal / target TBD`,
- selected article type profile path from `../../_shared/article-types/index.md`, otherwise
  `article type profile unresolved`,
- study type and likely reporting checklist,
- clinical/biomedical question and central manuscript claim,
- PICO / PECO / PIT / prediction frame as applicable,
- available source evidence: protocol, SAP, analysis report, tables, figures, registry record,
  ethics/consent documents, data dictionary, reviewer comments, existing draft, and bibliography,
- unsupported claims, missing values, and source conflicts,
- statement inventory: ethics/IRB, consent, trial registration, data/code availability, funding,
  conflicts, author contributions, acknowledgments, AI-use disclosure when needed,
- target-journal instructions or user-provided template files.

Writing Policy may inspect scripts and result files to understand evidence boundaries, but it does
not perform the research.

## Full Draft Clarification Boundaries

Use the global clarification protocol from `../../_shared/core/gates.md`. Ask now only when the
missing fact changes manuscript identity, checklist, claim boundary, article type, template, or
statements. Otherwise use a conservative unknown.

| Stage | Ask now only for | Defer or default |
|---|---|---|
| Writing Policy | study type/checklist conflict, paper identity, central claim, endpoint definition, analysis population, result/source conflict, ethics/registration fact that changes claim wording | exact section page lengths, final figure placement, optional supplement ordering |
| Paper Framework | target-journal/article-type conflict, missing official-source basis for named journal, checklist requirements that change section structure, Submission Format Route, template choice when multiple local options fit | caption wording, exact table row order, final supplementary file labels |
| Section Drafting | facts needed to write a section without false medical claims | weaken claim, mark unknown, or insert precise marker |

Ask about target journal at most once unless the user later changes it. If unknown, use the generic
medical draft template and label the target as unresolved.

## Stage Execution

Proceed in order:

1. Writing Policy -> `stages/writing-policy.md`.
2. Paper Framework -> `stages/paper-framework.md`.
3. Full Draft Manuscript Package:
   - `stages/manuscript-package.md`,
   - `stages/section-drafting.md`,
   - `academic-figure` for every display item,
   - `academic-citation` for every searched/written/verified source,
   - `academic-review` for closing review, audits, official-source gate, and submission readiness.

## Submission-Standard Gate

Before saying the draft is submission-ready, load `_shared/submission/submission-standards.md` and the
target journal standard card when available. Record the official source URL, date checked, target article type,
Submission Format Route, primary submission file, selected template status, checklist status, and
statement status in `paper/submission-package.md`.

Submission Format Route values:

- `word-first`: target journal expects Word or editable manuscript files as the primary submission.
  The production artifact is `paper/manuscript.docx`; `paper/main.pdf` is optional and may be absent.
  Do not require `paper/main.pdf` for word-first routes.
- `latex-first`: target journal accepts or provides TeX/LaTeX source. The production artifacts are
  `paper/main.tex` and compiled `paper/main.pdf`.
- `generic-review`: target journal format is unresolved. The production artifact is a reviewable
  `paper/manuscript.md`; do not call it submission-ready.

The gate fails if:

- the format-specific production gate is missing or inconsistent with the confirmed route,
- `word-first` route lacks `paper/manuscript.docx`,
- `latex-first` route lacks `paper/main.pdf` or the compile status is unknown,
- `generic-review` route is called submission-ready,
- `Actual main-text word count` is absent from `paper/submission-package.md`,
- the `draft length gate: PASS` or justified `draft length gate: BLOCKED` status is absent from
  `paper/submission-package.md`,
- the `visual display gate: PASS` or justified `visual display gate: BLOCKED` status is absent from
  `paper/submission-package.md`,
- the `table aesthetics gate: PASS` or justified `table aesthetics gate: BLOCKED` status is absent
  from `paper/submission-package.md`,
- the target journal/article type is unknown but the output is called submission-ready,
- the reporting checklist compliance matrix is absent,
- ethics/consent/registration/data-sharing statements are invented or unresolved,
- a generic or instruction-derived shell is represented as an official journal template,
- the official-source check was not performed in this run and the user did not explicitly accept the
  dated local snapshot.
