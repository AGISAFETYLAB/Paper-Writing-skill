# Journal Section Overlays

## What This Directory Is

The base section guides in `references/sections/*.md` are written with a conference
default (page-budgeted, single novel contribution, anonymous single-shot review).
This directory does **not** replace them. Each file here is a thin **overlay** that
states only the journal-specific deltas to apply on top of the base guide.

Composition rule:

1. Load the base section guide first (for example `references/sections/abstract.md`).
2. Then load the matching overlay here (for example
   `references/sections/journal/abstract.md`).
3. Keep all base structure, templates, and checklists. Apply the overlay as
   adjustments, not as a rewrite. Where the overlay conflicts with the base on a
   journal-specific point (length, anonymity, abstract rules, methods placement),
   the overlay wins for journals.

Only load these overlays when `Venue Kind: journal`. For conferences, use the base
guides alone.

## When Each Overlay Loads

| Drafting / revising | Base guide | Journal overlay |
|---|---|---|
| Abstract | `references/sections/abstract.md` | `journal/abstract.md` |
| Introduction | `references/sections/introduction.md` | `journal/introduction.md` |
| Method / System | `references/sections/method.md` | `journal/method.md` |
| Results / Experiments / Evaluation | `references/sections/experiments.md` | `journal/results.md` |
| Discussion / Conclusion | `references/sections/conclusion.md` | `journal/discussion.md` |
| Figures (sizing) | `academic-figure` skill: `references/figures/plot-style.md` (shared) | `academic-figure` skill: `references/figures/journal/figure-sizing.md` |
| Figures (contract) | `academic-figure` skill: `references/figures/figure-planning.md` (shared) | `academic-figure` skill: `references/figures/journal/figure-contract.md` |

Sections without an overlay here (Related Work, Figures/Tables section-level
insertion rules, paragraph flow) use the base guide directly. The
journal posture for those is covered by
`_shared/venues/journal-vs-conference.md` (complete, self-contained story;
thorough evaluation; written to survive multi-round review) and the active venue
card.

For figures, the shared `plot-style.md` (rcParams, colors, chart-type rules) and
`figure-planning.md` (Display Item Contract, Display Review Gate, generation routes)
are venue-agnostic. Journal papers load `journal/figure-sizing.md` for
journal-specific column widths and `journal/figure-contract.md` for composition patterns and
reviewer-risk assessment — no conference venue names enter context.

## Cross-References

- `_shared/venues/journal-vs-conference.md` — overall journal drafting posture.
- `academic-review` skill: `references/checks/journal-submission-elements.md` — mandatory statements,
  display-item caps and tiers, methods placement, and word-budget mechanics that
  are journal-wide rather than per-section.
- The active venue card under `_shared/venues/` (`jmlr.md`, `ieee-tpami.md`,
  `nature.md`, `nature-communications.md`, `journal-generic.md`) — the
  authoritative length, abstract cap, blinding, display tier, and post-main order
  facts the overlays defer to.
