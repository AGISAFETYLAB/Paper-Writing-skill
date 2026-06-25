# Table Placement

Use this reference for body-vs-appendix decisions, span, overflow, appendix float discipline, and
supplement routing. Use `table-design.md` for visual grammar and LaTeX table patterns.

## Body-vs-Appendix Decision Checklist

Before placing a nontrivial table, decide whether the reader needs it in the main argument or only as
supporting material. Record the decision in the table contract or execution report.

| Check | Keep in body when... | Move out of body when... |
|---|---|---|
| claim criticality | The table directly proves a central claim, main contribution, or headline result. | The table only completes a secondary claim or lists supporting details. |
| reader necessity | The reader cannot follow the method, benchmark, protocol, or experiment story without seeing it immediately. | The table is useful for verification but not needed to understand the main narrative. |
| density | The body version is compact enough to scan without interrupting prose flow. | The full table is a many-row/many-column matrix, a dump, or needs rotation/splitting. |
| novelty | The table exposes a new task, metric, dataset structure, core design choice, or surprising pattern. | The table reports routine setup, standard hyperparameters, or exhaustive variants. |
| page pressure | The table earns scarce body space after the main display-item budget is considered. | The paper is over budget or the same claim is already carried by a better body display. |
| full-version need | A compact body summary can carry the claim while the appendix holds the full evidence. | The full version is necessary but too detailed for the main text. |

Decision rule:

- Use the outcome `keep in the body` when the table is claim-critical, reader-necessary, and compact enough to scan.
- Use a compact body summary plus appendix full version when the claim matters but the complete
  evidence is too dense.
- Use the outcome `move to appendix` when the table supports reproducibility, completeness, robustness, or detailed
  verification but is not needed on the main reading path.
- Use the outcome `move to supplement` when the table is too wide, dense, or exhaustive to remain readable in the paper
  PDF even after rotation or splitting.

## Span And Width Contract

- `single-column`: fit within `\linewidth` / `\columnwidth`.
- `double-column`: allowed only with a span justification. In a two-column template use `table*`
  bounded by `\textwidth`; in a one-column template use regular `table` plus
  `tabular*{\textwidth}` or `tabularx{\textwidth}`.
- `appendix`: apply the same width contract and overflow ladder as the body. Appendix placement is
  not permission to exceed the printable area.
- `supplement`: use when even an in-paper rotated or split table remains unreadable.

Default to single-column for compact ablations, taxonomy/definition tables, setup/protocol tables,
and qualitative examples. Use double-column for load-bearing main results, genuine wide matrices, or
tables that remain unreadable after abbreviation and right-sized columns. Do not stretch sparse
content; a `table*` must fill `\textwidth` with useful comparison structure.

In a one-column paper, do not use `table*`. Use a normal `table`; small tables keep natural width or
a centered fraction of `\linewidth`, while dense central scorecards and wide matrices may use full
`\linewidth` / `\textwidth`.
Full-width means the cell block uses the declared width, not merely that the top/bottom rules span
the width. A table with full-width rules and left-packed cells is underfilled; switch to natural width
or use a real fill mechanism from `table-design.md`.

For a **sparse headline result**, do not stretch sparse content across both columns just because the
result is important. If that table is the paper's central scorecard, use the width responsibly by
adding supported comparison structure such as counts next to rates, grouped outcomes, coverage, or
confidence intervals. If it remains sparse, keep it single-column or summarize it in prose.

For a **secondary multi-metric table**, the default remains single-column unless it is unreadable.
Five or six numeric metrics trigger a fit check, not automatic `table*`. Abbreviate headers, trim
spacing, use a readable small font if needed, and shorten display names with caption expansion
before promoting. Promote only if those steps still leave the table unreadable or the table is the
headline scorecard / genuine wide matrix. In short: **do not stretch sparse content**.

## Never let a table overflow

A table wider than its declared container is a hard defect in body, appendix, and supplement. Apply
this ladder:

1. Exceeds `\columnwidth` but fits `\textwidth`: use `table*` only if the table is body-worthy and
   full-width-justified; otherwise split, abbreviate, or move detail to appendix.
2. Still exceeds `\textwidth`: rotate, split by column groups, or transpose.
3. Only after the layout is correct, use `\small`, `\footnotesize`, or `\resizebox` as a last touch
   for numeric short-cell tables. Do not resize prose-heavy tables as the primary fix.

Long task IDs, definitions, examples, and notes need wrapping columns (`tabularx` or fractional
`p{...}` widths tied to `\linewidth` / `\textwidth`). Numeric columns use `r`, `c`, or `siunitx S`,
not `tabularx` `Y`/`Z`.

## Appendix Plan

Before writing appendix material, create `paper/appendix-plan.md`. Each item records `Claim backed`,
`Source availability`, `Fill status`, and `Fallback`. Do not fabricate missing appendix snippets.

The appendix has the opposite failure from the body: short floats can scatter across half-empty pages.
Prevent table dumps:

- Keep appendix tables that fit one column as single-column tables.
- **Appendix display parity**: appendix tables must pass the same width, overflow, header,
  wrapping, caption, and rendered-page checks as body tables.
- Do not promote compact appendix protocol tables to `table*`; label definitions, small inventories,
  and key-value reproducibility notes should stay single-column or natural-width unless rendered QA
  proves they are unreadable.
- Watch for appendix float scatter: sparse `table*` / `figure*` floats can create half-empty pages
  even when each individual item compiles. Use single-column tables, tighter subsection prose,
  `\FloatBarrier`, or deliberate ordering before widening the float.
- Anchor every appendix subsection with a 2-4 sentence lead paragraph, not a one-line pointer.
- Pin float order deliberately; never use bare `[h]`. Use `[H]` if the venue allows `float`, or
  `[ht]` / `[tbp]` plus `\FloatBarrier` or a deliberate `\clearpage` where needed.
- Do not over-pin. `[H]` and `\clearpage` can create empty pages; use them only for float-heavy
  sections that would otherwise reorder.
- Carry the full version, never a stub, when the body summarizes a taxonomy, protocol, proof, result
  matrix, prompt, configuration, robustness sweep, or qualitative example set.
