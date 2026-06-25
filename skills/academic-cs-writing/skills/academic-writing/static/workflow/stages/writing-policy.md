# Stage: Writing Policy

Load this fragment when you reach the Writing Policy stage of the Full Draft Workflow. It ends at a
**blocking confirmation gate**: do not proceed to Paper Framework until the user confirms.

Load `references/principles/research-strategy.md`, `references/checks/workspace-logic-audit.md`
(required this stage — it drives the audit sub-step below), and `_shared/checks/claim-evidence.md`
(the audit uses its strength levels to cap claim wording), plus the paper-type family index needed to
classify the paper (`_shared/paper-types/index.md` for `venue_kind=conference`, or
`_shared/paper-types/journal/index.md` for `venue_kind=journal`). Do not load venue cards,
specific paper type profiles, template, section, figure, or style
references by default.

## Workspace Logic And Evidence Audit (run before the Claims table)

After Workspace Discovery and before filling the Claims-And-Evidence table, run the skeptical audit
in `references/checks/workspace-logic-audit.md`. Discovery only collects evidence; this step verifies
that each planned claim survives contact with the raw artifacts. It is a **writing-side audit only**:
it never re-runs, modifies, or redesigns experiments. Every finding resolves into one of four
writing-only actions — downgrade, mark (`needs evidence` / `not verified`), defer to Open Decisions,
or stop-and-ask when the issue is decisive for paper identity, a central claim, key terminology, or
an evidence conflict.

Run the seven checks (trace-to-artifact / cross-file consistency / result-to-conclusion logic /
scope-integrity smells / evidence-type labeling / terminology stability / disclosure-and-naming),
then run the **default-on
independent recheck** (Step D of the audit file): a fresh zero-context subagent receives only the
intended claims and paths to raw result files, and returns per-claim support verdicts. Fold its
findings back into the Claims-And-Evidence table and Open Decisions. Skip the recheck only if the
user opts out or the runtime cannot launch a subagent (then run the fresh self second-pass fallback).

The Writing Policy is a compact writing contract. Save it to:
`writing-policies/<paper-slug>-writing-policy.md`

File format:

1. **Source Snapshot**: project name, workspace path, files inspected, evidence snapshot date, and
   source traces for facts used in the paper contract.
2. **Paper Identity**: venue kind, target venue, paper type, manifest-mapped paper type profile
   path when available, intended reader, core research question, and venue/template constraints if
   already known. Do not encode numeric page counts in `Target venue`; `EMNLP long paper`, `ICLR
   submission`, or `journal-generic / target journal TBD` are venue identities, while `8 pages`, `9
   pages`, `camera-ready`, and other length/stage choices are physical-format inputs for the Paper
   Framework.
3. **Core Story**: problem, failure case or motivating gap, technical challenge, insight,
   proposed method/benchmark/system/study, one-sentence contribution, and final takeaway.
4. **Audit Findings**: the result of the Workspace Logic And Evidence Audit — a compact table with
   `item`, `check`, `verdict (pass/risk/blocking)`, `source trace`, and `writing action`. Include
   the independent recheck's per-claim verdicts here. Keep it short; this section justifies the
   `status` and `risk` values in the Claims-And-Evidence table below.
5. **Claims And Evidence**: a compact table with `claim`, `evidence`, `status`, `drafting action`,
   and `risk`. The drafting action must say whether to state, weaken, verify, defer, or avoid the
   claim. Each row's `status` and `risk` must be consistent with the Audit Findings above.
6. **Key Terms**: a compact table with `term`, `definition`, `source`, `use policy`, and `status`.
   Include only terms that affect the title, abstract, contribution, method identity, dataset/task,
   benchmark, metric, or system components.
7. **Disclosure And Naming**: the publication-boundary registries from contract point 7. Two compact
   tables. **Naming Map** — `internal identifier`, `public display name`, `source trace`; one row per
   internal checkpoint / training-run / sweep / wandb / tool / unreleased-model identifier found in
   the workspace that maps to a public name. **Do-Not-Disclose** — `entity`, `kind` (baseline /
   method / tool / dataset / partner / result), `reason`, `disclosure status`
   (`do-not-disclose` / `restricted`), and for any withheld competing method an
   `integrity check` cell stating whether removing it keeps comparison claims honest (if not, it is
   an `idea-level risk` → Open Decisions / stop-and-ask, not a silent removal). Leave a table empty
   only after actively checking the workspace; record `none found` rather than omitting it. After the
   user confirms the Writing Policy, export both tables to `paper/.disclosure.yaml` (the format the
   `audit_draft.py` disclosure check reads — see that script's header in the `academic-review` skill)
   so the static gate can enforce them mechanically.
8. **Assets And Constraints**: only visible assets or constraints that affect drafting.
   If the user mentions a page count or draft stage, record it here only as a Framework input with
   status `submission / camera-ready / custom / unresolved`; do not convert it into a venue fact or a
   confirmed page budget in the Writing Policy.
9. **Open Decisions**: only unresolved decisions that can change the paper identity, central claim,
   evidence boundary, key terminology, disclosure/naming boundary, figure/table plan, or
   venue/template choice. **Do NOT raise page/length budgets, per-section length, section page
   allocations, figure/table counts, or display-item budgets here — those are physical-structure
   decisions owned by the Paper Framework stage. If such a question comes up, defer it to Paper
   Framework rather than asking the user to confirm it at the Writing Policy gate.**

Do not add a short translated confirmation summary inside the Writing Policy. If the user requested
another language version before this stage was generated, create a complete same-content translated
sibling artifact instead.

Record venue kind as one of: `conference` or `journal`. If the user has not explicitly specified a
journal target, use `conference`.

Record venue status as one of: `confirmed: <venue>`, `generic / venue TBD`, `journal-generic /
target journal TBD`, or `conflict: <options>`.

Paper type must be resolved after venue kind and before confirming the Writing Policy. Use
`_shared/paper-types/index.md` for conference papers and `_shared/paper-types/journal/index.md`
for journal papers before defaulting. Do not use `method-paper.md` or `journal-method` as a global
default.

Writing Policy checkpoint summary must include:

- paper identity: working name, venue kind, paper type, and target
  venue status,
- research content: core research question, one-sentence contribution, and central claim boundary,
- evidence snapshot: key source-evidence types and what they support,
- experiment/result snapshot: current datasets/tasks/models/metrics/result ranges found,
- audit snapshot: the Workspace Logic And Evidence Audit verdict — any `blocking`/`risk` findings
  (phantom claims, cross-file conflicts, result-to-conclusion gaps, scope/integrity smells), the
  independent recheck outcome, and how each was resolved (downgraded / marked / deferred /
  stop-and-ask),
- disclosure snapshot: how many internal identifiers are mapped to public names, how many entities
  are marked do-not-disclose, and whether any withheld comparison was flagged as an integrity risk,
- top risks: 2-3 claim, evidence, terminology, result, disclosure, or citation risks,
- decisions to confirm: split into Required and Optional.

**Compliance Self-Check (Writing Policy) — complete before showing the checkpoint.** Answer each
item yes/no internally; **any "no" means this stage is not complete — fix it before stopping at the
gate.** Do not skip a field by leaving it blank.

1. Are all six contract points (`_shared/core/contract.md`) resolved or explicitly listed in Open
   Decisions — none silently guessed?
2. Is venue kind resolved first (`conference` unless explicit journal), and is the paper type
   resolved against the correct family index (not defaulted to method-paper or journal-method), and
   recorded with its manifest-mapped profile path?
3. Did I run the Workspace Logic And Evidence Audit (all seven checks) and record the results in the
   Audit Findings section, with every `blocking`/`risk` finding resolved into downgrade / mark /
   defer / stop-and-ask — and no claim left untraceable to a real artifact?
4. Did I run the independent zero-context recheck (or the fresh self second-pass fallback, or note
   an explicit user opt-out), and fold its per-claim verdicts into the table?
5. Does every claim in the Claims-And-Evidence table have a `status` and a `drafting action`, and is
   each `status`/`risk` consistent with the Audit Findings (no wording exceeding its evidence
   ceiling)?
6. Are all checkpoint-summary fields above filled (no empty field), including the audit snapshot and
   the disclosure snapshot?
7. Did I build the Disclosure And Naming registries (Naming Map + Do-Not-Disclose, each `none found`
   or populated after actually checking the workspace), confirm no internal identifier or
   do-not-disclose entity leaked into the Claims-And-Evidence or Key Terms tables, and flag any
   withheld comparison that would make a claim misleading as an `idea-level risk` / Open Decision?
8. Did I avoid loading downstream references (venue, section, figure, template) not allowed at this
   stage?
9. Did I keep all physical-structure decisions out of the Writing Policy — no page/length budget,
   per-section length, section page allocation, figure/table count, or display-item budget in the
   Open Decisions, the checkpoint summary, or the confirmation question? (These belong to Paper
   Framework.) Did I also keep `Target venue` free of numeric page counts, and if the user supplied a
   page count, did I mark it only as a `submission / camera-ready / custom` Framework input?

Gate: the user must confirm the Writing Policy before Paper Framework generation.
