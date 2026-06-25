# Draft Revision Workflow — Medicine

Use when the user provides existing medical prose, Word, Markdown, or LaTeX and asks for a revised
draft version.

Intent class: `draft-revision`.

Default behavior for local prose polish/check: load the fewest files needed for the requested grain.
This route does not create a Writing Policy, Paper Framework, or new manuscript package unless the
user explicitly asks.

If the user asks to fill missing package components, route to `package-completion` under the full-draft workflow instead of absorbing that work here.

## State Machine

```text
Existing draft / section / paragraph / sentence / caption / statement
  -> identify grain and task
  -> establish Edit Boundary when the paper is frozen
  -> load minimal references
  -> revise / diagnose / compress / review
  -> output revised text + boundary notes
```

## State 1: Identify Grain And Task

Identify the object: title, abstract, full draft, section, paragraph, sentence, caption, figure
legend, statement, checklist response, reviewer-response paragraph, or complete versioned
manuscript.

Identify the task: medical English precision edit, structure rewrite, claim weakening, section
draft/rewrite, statement or checklist update, submission-fit tightening, citation cleanup, display
caption rewrite, page/word compression, or whole-paper review.

Use open revision by default. Use frozen revision mode when the user says resubmission,
camera-ready, revision response, already submitted, page-limit shrink with fixed content, or "only
fix wording".

## Edit Boundary

In frozen revision mode, establish an Edit Boundary before editing and honor it on every change.
Default boundary:

- Allowed: grammar, precision, flow, journal tone, local compression, cross-reference repair,
  statement wording from existing facts, checklist location wording, caption wording.
- Forbidden additions: new numerical results, new outcomes, new effect sizes, new subgroup findings,
  new adverse events, new ethics/IRB numbers, new consent claims, new registry IDs, new citations or
  bibliography entries, and new statistical methods not already in the draft or source materials.
- Needs explicit approval: rewriting the whole abstract, changing title claim strength, changing
  study type/checklist, deleting a section, changing the primary endpoint, or adding a new statement
  category.

If the user provides a stricter boundary, use it. When a desirable edit would cross the boundary, do
not apply it silently; list it as a deferred edit with the reason and the risk it would address.

## State 2: Load Minimal References

| Grain / task | Required references | Conditional references |
|---|---|---|
| sentence or paragraph medical English | `references/sections/paragraph-flow.md` | checklist card when claim wording depends on study type |
| title / structured abstract | `references/sections/title-abstract.md`, `references/sections/paragraph-flow.md` | target journal standard card, checklist card |
| Introduction section | `references/sections/introduction.md`, `references/sections/paragraph-flow.md` | citation review for background and gap claims |
| Background / related work / prior-work comparison | `references/sections/literature-positioning.md`, `references/sections/paragraph-flow.md` | citation review for external claims |
| Methods section | `references/sections/methods.md`, selected checklist card | `../../_shared/submission/statements.md` |
| Results section | `references/sections/results.md`, `../academic-figure/SKILL.md` when displays are involved | selected checklist card |
| Discussion / limitations | `references/sections/discussion.md`, `references/sections/paragraph-flow.md`, `../academic-review/references/review.md` | citation review for external comparison claims |
| appendix / supplement / eTables / eFigures | `references/sections/appendix-supplement.md`, selected checklist card | target journal standard card, `../../_shared/submission/data-availability.md` |
| statements | `references/sections/statements.md`, `../../_shared/submission/statements.md`, `../../_shared/submission/submission-standards.md` | target journal standard card |
| complete versioned manuscript | full-draft closing references plus `academic-review` | target journal standard card, template reference |

For any edit touching citations, invoke `academic-citation`. For any edit touching figures, tables,
legends, or display-in-prose, invoke `academic-figure`. For any whole-paper or submission-readiness
revision, invoke `academic-review`.

## State 3: Preserve Meaning And Evidence Boundary

Before revising, identify the medical claim boundary:

- population/setting,
- intervention/exposure/index test/predictor,
- comparator/reference standard when relevant,
- outcome/endpoint,
- timeframe,
- analysis population,
- uncertainty/effect measure,
- source evidence.

The revision must not create meaning drift. Do not make association sound causal, exploratory
analysis sound prespecified, internal validation sound external validation, diagnostic performance
sound clinical utility, or a safety observation sound a treatment recommendation.

If stronger wording would require new clinical evidence, weaken the claim instead.

## State 4: Revise Or Diagnose

For local edits, return the revised text and only the notes needed to explain claim-boundary changes.
For section edits, revise prose using the section guide and report remaining evidence/citation risks.
For statement or checklist edits, separate text that can be written from existing facts from items
that remain unknown.

For a complete versioned manuscript, run the route-appropriate production gate and `academic-review`
before calling it clean. Word-first routes require `manuscript.docx`; LaTeX-first routes require
`main.pdf`; generic-review routes must remain explicitly not submission-ready. If a required
production check is unavailable, state the unverified gate and run static checks instead.

## Hard Rules

- Do not add ethics approval numbers, registration numbers, sample sizes, adverse events,
  confidence intervals, p values, or citations unless they are present in source materials or the
  user provides them.
- Do not convert missing science into elegant prose.
- Do not claim formal checklist compliance from partial sections.
- Do not call a complete versioned manuscript clean until citation, display, statement, checklist,
  and format-specific production gates are handled or explicitly blocked.
