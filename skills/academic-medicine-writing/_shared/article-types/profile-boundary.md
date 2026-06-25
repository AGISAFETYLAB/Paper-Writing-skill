# Medical Article-Type Profile Boundary

Article-type profiles define the default manuscript structure for a medical article type. They own
section structure and budget only: section list, order, naming, count, proportional word budget,
priority contract, compression order, and minimum floors for sections that carry the study's main
evidence.

Profiles do not own reporting-checklist item evidence, writing style, citation policy, clinical
claim admissibility, figure design, statement truth, journal rules, or final submission checks. Route
those concerns to the checklist cards, section guide, citation, figure, statement, journal-standard,
and review files.

## Paper Framework Hard Default

At the Paper Framework stage, the selected article type profile is a hard default, not loose
inspiration. By default, reproduce the profile's section table as the Section Plan's structure,
including section names and order, then quote it as the canonical list in the Paper Framework's
"Structure vs article-type profile" comparison.

Deviate only when actual evidence, target-journal instructions, selected reporting checklist,
statement requirements, or explicit user instructions genuinely require a split, merge, rename,
addition, or reorder. Every deviation must be surfaced in the Paper Framework checkpoint with a
one-line reason. Silent structural deviation is a workflow violation.

## Budget Boundary

Absolute length comes from the active `target_length_budget`: official target-journal instructions
first, journal standard card or official template text second, and the Generic Medical Length Fallbacks in
`_shared/submission/templates.md` third. Profiles provide proportional allocation and compression priority
only.

If the active source gives a word limit, use a section-level word budget. If it gives a page limit,
use a page budget. Do not invent pages when the official source specifies words.
