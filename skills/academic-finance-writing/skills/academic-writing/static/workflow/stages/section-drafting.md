# Stage: Section Drafting — Finance

## Load Prerequisites

Load before drafting or revising a section:

- Confirmed Paper Framework for section content anchors and evidence boundaries.
- `references/prose-style.md` for paragraph-level finance prose.
- `references/sections/index.md` for section-guide routing.
- `references/sections/paragraph-flow.md` for one-message paragraphs and the
  reverse-outline audit.
- The selected section guide:
  `references/sections/title-abstract.md`,
  `references/sections/introduction.md`,
  `references/sections/literature-positioning.md`,
  `references/sections/data-institutional-setting.md`,
  `references/sections/identification-methods.md`,
  `references/sections/theory-model.md`,
  `references/sections/results.md`,
  `references/sections/mechanisms-robustness.md`,
  `references/sections/discussion-conclusion.md`, or
  `references/sections/appendix-online-appendix.md`.
- `references/writing-craft.md` for the Finance Writing Craft Gate, Paragraph
  Evidence Contract, Results Narrative Gate, mechanism/heterogeneity logic, and prose lint
  expectations.
- `../../_shared/checks/finance-domains.md` when domain terminology, variables, display
  pressure, literature positioning, or reviewer risks appear in section prose.
- `../../_shared/checks/identification-strategies.md` and
  `../../_shared/checks/econometrics.md` when method claims appear.
- `academic-citation` before inserting or repairing citations. For any professional finance,
  economics, accounting, data, method, software, or venue-policy content not already verified in
  the user's materials, use live lookup through `source-routing.md`, check context with
  `citation-integrity.md`, and update the Citation Evidence Ledger.
- `academic-figure` before inserting or repairing tables, plots, or appendix displays.
- `academic-review` before returning a full draft.

Draft by section using the selected version target and paper type.

For each section:

1. Select the section guide from `references/sections/index.md` and record the
   selected section guide in the working notes.
2. Define the section claim and evidence boundary.
3. Write one-message paragraphs with explicit data, model, uncertainty, and economic magnitude.
4. Apply the Paragraph Evidence Contract: each central paragraph must bind claim, data/model/design
   anchor, estimate or result when available, uncertainty or benchmark, and economic interpretation
   or limit.
5. Use numeric results only when present in the source materials or in a user-provided
   synthetic/demo workspace that is explicitly labeled as synthetic.
6. Insert citations through `academic-citation`; do not fabricate references. Every added or
   accepted live-lookup citation must have a Citation Evidence Ledger row with source identity,
   metadata source, support grade, and action.
7. Insert figures/tables through `academic-figure`; every display must support one manuscript claim.
8. End with limitations and data-code notes that match the evidence, not the desired conclusion.

For results sections, enforce the Results Narrative Gate. Do not write a table tour; start with the
economic result, magnitude, benchmark, and uncertainty, then cite the table or figure. Mechanism and
heterogeneity tests must have theory -> observable implication -> test before they appear in the
main text.

## Page-Budget Expansion Pass

After the first complete section draft, compare section length against the confirmed page-window
expansion budget. Synthetic/demo workspaces require the same budget discipline as real-data
workspaces. If the manuscript is tracking below `min_pages`, add supported expansion only:
institutional context from verified sources, method detail, data provenance, variable construction,
table/figure interpretation, robustness-boundary discussion, replication/code-output mapping, and
Internet Appendix material already approved in the Paper Framework. Do not compress below the confirmed page-window budget. Do not pad with repeated caveats, invented results, generic finance
background, or citation piles.

Use `references/prose-style.md`, `references/sections/index.md`,
`references/sections/paragraph-flow.md`, and the selected section guide before
drafting abstracts, introductions, results, conclusions, captions, or appendix text. Use
`references/writing-craft.md` before approving contribution paragraphs, results
subsections, mechanism/heterogeneity prose, and title/abstract/introduction quality. Use
`../../_shared/checks/identification-strategies.md` for method-specific paragraphs.

Do not leave unsupported markers in a final full draft. If a missing result, citation, or display is
not producible from the source materials, keep the manuscript conservative and record the blocker in
`paper/submission-package.md`.

Before returning a full draft, delegate to `academic-review`.
