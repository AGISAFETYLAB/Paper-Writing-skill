# Appendix And Supplement Guide

Use this guide when drafting, revising, or assembling appendix / supplement material.

## Appendix Is Support, Not A Second Main Paper

The appendix carries material that supports verification, reproducibility, completeness, or reader
trust without being required for the main argument's first-pass comprehension.

Put here:

- full taxonomy, inventory, prompt, protocol, or configuration lists after the body states the
  argumentative summary,
- full proofs when the main body gives the statement and proof sketch,
- extended result matrices, robustness sweeps, secondary ablations, or qualitative example sets,
- extra implementation or dataset details needed for reproducibility.

Do not hide main evidence. If a result is needed to believe the Abstract, Introduction, central
Method claim, or headline experiment, keep the compact evidence in the main text and move only the
full version to the appendix or supplement.

## Benchmark / Dataset / Evaluation Appendix Evidence Package

For benchmark, dataset, evaluation, or empirical-system papers, the appendix should normally be a
source-backed evidence package rather than a short parking lot. Include every item for which the
source exists and the body only has room for a compressed summary:

- corpus or task inventory with counts and selection boundaries,
- taxonomy or label protocol definitions with decision rules and edge cases,
- denominator audit for every headline rate, including excluded or infrastructure-failed cases,
- full result matrix or per-group result table that backs aggregate plots,
- prompt, verifier, annotation, or adjudication details needed to reproduce the measurement,
- representative success/failure examples when qualitative claims or failure modes appear in the
  body,
- reproducibility and artifact-boundary notes that distinguish generated assets, source data, and
  claims not supported by available evidence.

If one of these package slots is source-backed and directly supports a body claim, fill it rather
than leaving a placeholder. If the source is missing, weaken or remove the body claim and record the
item as omitted in `paper/appendix-plan.md`.

## Required Appendix Plan

Before writing appendix content, create or update `paper/appendix-plan.md`. Each row records:

| Item ID | Type | Claim backed | Source availability | Fill status | Main-text anchor | Fallback |
|---|---|---|---|---|---|---|

- `Claim backed`: the exact claim, section, figure, or table this item supports.
- `Source availability`: existing source path, confirmed user-provided source, or missing.
- `Fill status`: `filled`, `partial`, or `omitted`.
- `Main-text anchor`: the body sentence/table/figure that points to the item.
- `Fallback`: compress, omit, move to separate supplement, or mark evidence missing.

No stubs. Do not write "see supplementary material", "details omitted", or an empty appendix section
when the source exists. If the source is missing, omit the claim or mark the evidence risk instead of
inventing content.

## Writing Shape

Every appendix subsection needs a 2-4 sentence lead paragraph before any float, list, or proof. The
lead says what the item is, how to read it, and which main-text claim it backs.

Keep appendix prose concise:

1. Lead paragraph.
2. Full table/proof/list/example set.
3. Optional one-sentence note on scope or interpretation.

Do not repeat the main paper's motivation or result narrative. Cross-reference labels normally:
`Appendix~\ref{...}`, `Table~\ref{...}`, `Figure~\ref{...}`.

## Placement And Venue Rule

Follow the confirmed Venue Assembly Plan. Some venues allow appendices after references; some journals
require separate supplementary files; some venues count appendix pages or forbid main-PDF appendices.
If appendix movement is forbidden or counted against the active limit, do not use appendix movement as
a page-budget fix.

For figures and tables, use the `academic-figure` table placement and figure planning references for
span, overflow, and float-order rules. Appendix placement is not permission to exceed the printable
area.

## Appendix Display Parity Gate

Appendix figures and tables are not second-class displays. They must pass the same visual contract as
body displays: clear evidence role, concrete source, explicit denominator or unit, readable labels,
caption with the supported claim, width/span justification, and rendered-page inspection.

Do not use `figure*` or `table*` just because the item is in the appendix. Compact protocol tables,
small inventories, and glossary-like label references should stay single-column or natural-width.
Small heatmaps and secondary matrices should use a moderate width unless legibility proves they need
the full span. A cross-column appendix float must earn its width with dense labels, multiple panels,
or a full result matrix that would be unreadable at column width.

Before returning a draft, inspect the appendix pages, not only the main text. A large blank page,
float-only page caused by sparse `table*` / `figure*`, oversized heatmap, unreadable table, or
appendix float that looks visually rougher than the body is a revision defect.

## Self-Check

- Is every appendix item listed in `paper/appendix-plan.md`?
- Is every item source-backed or explicitly omitted?
- Does each item have a main-text anchor?
- Does each subsection have a real lead paragraph?
- Is no central evidence hidden outside the main reading path?
- Does the appendix include the source-backed evidence package needed for this paper type, including
  denominator audit and full matrix/protocol material when relevant?
- Do appendix figures and tables pass the Appendix Display Parity Gate?
