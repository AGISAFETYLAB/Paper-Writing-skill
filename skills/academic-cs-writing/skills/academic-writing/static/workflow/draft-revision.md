# Draft Revision Workflow

Use this workflow when the user provides existing prose and asks to revise, rewrite, polish,
diagnose, review, compress, weaken claims, or improve flow.

Default behavior: load the fewest references needed for the requested grain. Do not generate a
Writing Policy, Paper Framework, or output file unless the user explicitly asks.

## State Machine

```text
Existing draft / section / paragraph / sentence / caption
  -> identify grain and task
  -> load minimal references
  -> section drafting protocol when revising a section
  -> rewrite / polish / diagnose / review
  -> output revised text + necessary notes
```

## Path Convention

In this fragment, paths beginning with `references/` are relative to the hub skill
(`skills/academic-writing/`), and paths beginning with `../../_shared/` point to the
collection-root shared layer. Sibling references are written as
`<sibling skill>: <path inside that skill>` so they are not mistaken for paths relative
to this workflow file.

## State 1: Identify Grain And Task

Identify the object: full draft, section, paragraph, sentence, caption, title, abstract,
figure/table description.

Identify the task: grammar polish, academic tone, clarity improvement, flow diagnosis, claim
weakening, caption rewrite, compression, reviewer-friendly rewrite, structural rewrite, whole-paper
review.

Identify the revision mode, because it changes what edits are allowed:

- **open revision** (default): free to restructure, add/remove citations, add figures/tables, and
  reframe claims within the writing-only scope.
- **resubmit / camera-ready / rebuttal-bound**: the paper structure and claims are frozen by an
  external constraint. Apply text-only microedits and respect an Edit Boundary (see State 1b). Use
  this mode when the user mentions resubmission, camera-ready, page-limit shrink with frozen
  content, or "only fix wording, do not change the paper".

If the user does not state a mode and the request is ordinary polishing, use open revision and say
so in one line.

Use the global Clarification Protocol from `../../_shared/core/gates.md`. If missing context can be
handled conservatively, proceed and state assumptions briefly. Ask only when the missing
information changes the revision strategy.

## State 1b: Edit Boundary (resubmit / camera-ready mode only)

Skip this state in open revision. In resubmit / camera-ready / rebuttal-bound mode, establish an
Edit Boundary before touching the draft and honor it on every edit. Default boundary unless the
user relaxes it:

- **Allowed**: rewording, tightening, compression, clarity and flow fixes, fixing typos and broken
  cross-references, caption wording, and shortening to fit a page limit.
- **Forbidden additions**: new `\cite{}` / `\citep{}` / `\citet{}` or new `\bibitem`, new theorem
  / lemma / proposition / corollary environments, and new numerical claims, metrics, or percentages
  not already in the draft.
- **Forbidden mutations**: editing `.bib`, `.sty`, `.bst`, `.cls`, or any prior-submission
  directory; deleting an existing citation or theorem environment.
- **Needs explicit user approval**: rewriting the whole abstract, rewriting the first Introduction
  paragraph, or deleting a section.

If the user supplies their own boundary (paths to touch, operations to block, a maximum number of
edits), use it instead of the default. When an intended edit would cross the boundary, do not apply
it silently: list it as a deferred edit with the reason and the reviewer concern that motivated it,
and let the user decide. The boundary protects a frozen paper from drift; surfacing rejected edits
is the point, not hiding them.

## State 2: Load Minimal References

Choose references by grain. For any task that writes or polishes English prose (every row
below except pure structural diagnosis), load `references/style/copyediting-standard.md`
and apply it while revising — it is the sentence-level language standard, not an optional
extra.

| Grain / task | Required references | Conditional references |
|---|---|---|
| Sentence polish | `references/style/copyediting-standard.md` | `../../_shared/checks/claim-evidence.md` |
| Paragraph polish / flow | `references/sections/paragraph-flow.md`, `references/style/copyediting-standard.md` | style references, `../../_shared/checks/claim-evidence.md` |
| Caption rewrite | `academic-figure: references/prose/display-in-prose.md` | `../../_shared/checks/claim-evidence.md`, `../../_shared/checks/metric-design.md` |
| Abstract rewrite | `references/sections/abstract.md`, `references/sections/paragraph-flow.md` | `references/sections/examples/abstract-examples.md`, `../../_shared/checks/claim-evidence.md`, `academic-review: references/checks/reviewer-risk.md` |
| Introduction rewrite | `references/sections/introduction.md`, `references/sections/paragraph-flow.md` | `references/sections/examples/introduction-examples.md`, `../../_shared/checks/claim-evidence.md`, `academic-review: references/checks/reviewer-risk.md` |
| Related Work rewrite | `references/sections/related-work.md`, `references/sections/paragraph-flow.md` | `academic-citation: references/checks/citation-integrity.md` |
| Method rewrite | `references/sections/method.md`, `references/sections/paragraph-flow.md` | `references/sections/examples/method-examples.md`, `academic-figure: references/prose/display-in-prose.md`, `academic-figure: references/tables/table-design.md`, `academic-review: references/checks/reviewer-risk.md` |
| Experiments rewrite | `references/sections/experiments.md`, `references/sections/paragraph-flow.md` | `../../_shared/checks/metric-design.md`, `academic-figure: references/prose/display-in-prose.md`, `academic-figure: references/tables/table-design.md`, `academic-figure: references/tables/table-placement.md`, `academic-review: references/checks/reviewer-risk.md` |
| Conclusion rewrite | `references/sections/conclusion.md`, `references/sections/paragraph-flow.md` | `../../_shared/checks/claim-evidence.md` |
| Appendix / Supplement rewrite | `references/sections/appendix.md`, `references/sections/paragraph-flow.md` | `academic-figure: references/tables/table-placement.md`, `academic-review: references/checks/submission-readiness.md` |
| Whole-paper review | `academic-review: references/sections/paper-review.md`, `references/sections/paragraph-flow.md` | `academic-review: references/checks/reviewer-risk.md`, `../../_shared/checks/claim-evidence.md`, `../../_shared/checks/metric-design.md`, `academic-citation: references/checks/citation-integrity.md` |

**Journal overlay (only when the revision target is a journal paper).** For a section rewrite against
a journal target, after loading the base section guide above also load the matching overlay under
`references/sections/journal/` and apply it on top: Abstract → `journal/abstract.md`; Introduction →
`journal/introduction.md`; Method → `journal/method.md`; Conclusion/Discussion → `journal/discussion.md`.
Treat a target as journal only when the user names a journal venue or says journal paper; otherwise do
not load any `references/sections/journal/` file.

For section rewrites, load matching example files only when the section guide points to a specific
example, the section structure is uncertain, or the user asks for examples. Learn structure, not
phrasing.

Do not load full-draft-only references by default: venue profiles or paper type profiles. Load those
only when the user asks to revise using project evidence or venue-specific expectations.

## Paper Content Edit Transaction

Any revision that changes manuscript content - prose, captions, table text, section headings,
appendix text, displayed equations, or claim wording - is a paper-content edit. Before applying the
edit, identify the touched section(s) and re-read from disk the matching
`references/sections/<section>.md` guide, `references/sections/paragraph-flow.md`, any journal
overlay required by the target, and any conditional metric/claim/display references triggered by
the changed text. Do not rely on a section guide loaded earlier in the run.

After the edit, rerun the relevant Section-Method Adherence check and reverse-outline check for the
touched section(s). When revising a complete `paper/` project, update `paper/section-compliance.md` with the section, guide loaded, required moves checked, result, and residual risk. When revising only a snippet or isolated section, return a compact compliance note
instead of writing a project ledger. This is a reread/self-check procedure, not a freshness gate. Do not add hash, mtime, timestamp, or source-hash requirements.

## State 3: Section Drafting Protocol

Use this protocol for any section-level draft or rewrite. Do not use it for sentence, paragraph,
caption, light compression, local claim weakening, or local flow diagnosis.

Build these internal artifacts before writing prose:

1. **Section Plan**: 3-7 bullets that state the section's argument in order.
2. **Paragraph Plan**: each paragraph has one role, one message, evidence or source, and risk.
3. **Claim-Evidence Check**: every major claim maps to supplied evidence, citation support, or a
   weakened/removed claim.
4. **Risk Notes**: unresolved evidence, citation, metric, terminology, or reviewer-facing risks.

Section-writing rules:

- One paragraph has one message; the first sentence should state the paragraph role or claim.
- Key terms must be self-contained and stable across the revised text.
- Sentence-to-sentence flow must show cause, contrast, consequence, refinement, example, or evidence.
- For Method subsections, include motivation, design, and technical advantage when applicable.
- For Abstract and Introduction, map central claims to available evidence before strengthening them.
- For Experiments, make metric direction, denominator, comparison setting, and result scope explicit.
- For figures/tables, treat the visual as evidence: one visual has one message and a caption that
  states the supported claim.

After drafting the section, run reverse outlining internally:

1. section thesis,
2. each paragraph topic sentence,
3. evidence or explanation under each paragraph,
4. mapping from paragraph to section thesis,
5. unsupported or mixed-message paragraphs to revise, split, weaken, or remove.

Also run the Section-Method Adherence check: verify the rewritten section against its section guide's
required moves (e.g., Method: motivation/design/advantage per module; Experiments: setup + claim-to-
experiment mapping; one paragraph one message; topic-sentence first) and mark each `present` /
`missing`; a `missing` move means the rewrite is not done. When revising a complete `paper/` project
(not a snippet), also run the `academic-citation` skill's `scripts/audit_citations.py` and the
`academic-review` skill's `scripts/audit_draft.py` before calling it
clean.

Do not show the internal Section Plan, Paragraph Plan, reverse outline, or claim-evidence map by default.
Show them only when the user asks, when the task is explicitly diagnostic/review-oriented, or when a
blocking evidence/citation risk must be surfaced.

## State 4: Decide Whether To Show A Plan

No visible formal plan for: sentence polish, paragraph polish, caption rewrite, light compression,
local claim weakening, local flow diagnosis.

Generate a compact local plan before rewriting when the task is broad enough that the user may need
to see the intended change before reading the revision: rewriting a whole section, changing section
structure, revising a full draft, reorganizing figures/tables, changing contribution or claim
framing, responding to reviewer-style risks.

The local plan should be brief:

```markdown
## Revision Plan
- Object:
- Goal:
- Main issue:
- Structure change:
- Claims to preserve:
- Claims to weaken:
- Evidence / citation risk:
```

Do not save this plan to a file by default.

## State 5: Revise Or Diagnose

For sentence-level tasks: revised sentence, one short note only if the change affects claim strength
or meaning.

For paragraph-level tasks: revised paragraph, interaction-language explanation when useful, main
change notes only if needed.

For caption tasks: improved caption, figure message, reviewer concern only if relevant.

For section-level tasks: revised section, concise interaction-language revision notes, remaining
evidence/citation risks.

Do not output the Section Plan, Paragraph Plan, reverse outline, or full claim-evidence map
by default. Include them only when requested, when the user asked for diagnosis/review, or when a
blocking risk affects the revision.

For whole-paper review: run the two-round Post-Draft Review Loop from
`academic-review: references/sections/paper-review.md`
by default — Round 1 self-review, then Round 2 an independent reviewer subagent launched in a fresh,
isolated context under the Reviewer Independence rules (pass only the reviewer role, venue/format
constraints, review dimensions, and the LaTeX/PDF paths; never the section plans, the Round 1 finding
list, fix summary, or "what changed" notes). Skip Round 2 only if the user opts out; if the runtime
cannot launch a subagent, use the fresh self second-pass fallback. Report concise findings ordered by
severity, required revision, and evidence/citation risks.

## Revision Rules

- Apply `references/style/copyediting-standard.md` to every prose edit: formal register,
  no contractions, no possessive `'s` on method/model/system names, simple and clear
  vocabulary, common abbreviations kept unexpanded, LaTeX commands preserved verbatim,
  no emphasis added beyond the source, and paragraphs never turned into lists.
- Preserve the user's intended meaning unless explicitly asked to change it.
- Improve logic, not just wording, when the task asks for rewrite or flow.
- Keep one paragraph to one message.
- Make topic sentences clear.
- Keep paragraph roles explicit internally during section-level work.
- Keep terminology consistent.
- Do not strengthen unsupported claims.
- Mark unverified citations as `not verified`.
- Do not fabricate citations, results, or experimental details.
- Do not output Writing Policy, Paper Framework, or full review tables unless requested.
- In resubmit / camera-ready mode, honor the State 1b Edit Boundary; surface boundary-crossing
  edits as deferred items with their reason rather than applying or silently dropping them.
