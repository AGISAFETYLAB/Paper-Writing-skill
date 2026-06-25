# Table Workflow

Execution-only table workflow. Do not repeat table-design or placement rules here; load the
referenced files when the decision is needed.

The deep references are:

- `references/tables/table-design.md` for table kind, visual grammar, LaTeX patterns, and QA.
- `references/tables/table-pattern-gallery.md` for optional polished table examples after the
  table is classified.
- `references/tables/table-placement.md` for body-vs-appendix, span, overflow, and appendix floats.
- `references/prose/display-in-prose.md` for how display items support prose and captions.
- `academic-review` skill's `scripts/inspect_compiled_layout.py` for compiled table pages, contact sheet
  creation, and the layout QA artifact required before closing a full draft.

## Workflow

1. Read the confirmed Figure Plan entry, especially `Layout`, `Section`, `Message`, `Source`, and
   `generation route`. Load `references/tables/table-design.md`. Load
   `references/tables/table-placement.md` whenever placement, span, appendix, or supplement decisions
   are involved.
2. For a standalone table task, if no Figure Plan is available, infer a provisional table type from
   the caption/request, row labels, column headers, metric directions, and evidence role. Record the
   assumption instead of treating every numeric matrix as a main-result table.
3. For a data-backed table source, run
   `python3 skills/academic-figure/scripts/inspect_table_data.py <source>` before writing LaTeX.
   Use the schema inspection JSON for row/column counts, numeric columns, long headers, precision,
   missing metric-direction markers, width risks, and suggested table kinds. The script reports facts;
   it does not decide the paper claim.
4. Fill the Table Contract from `table-design.md`: table kind, message, Data source / Source
   artifact, visual grammar, column strategy, numeric precision, metric direction status, highlight
   rule, Placement summary, and fallback. Fill the placement details from `table-placement.md`.
5. For nontrivial tables, consult `references/tables/table-pattern-gallery.md` after the Table
   Contract is filled and before writing LaTeX. Use the nearest pattern as a style and structure reference
   only when it matches the evidence role and density. Do not force a gallery pattern onto a simple,
   sparse, or unusual table.
6. Generate width-safe table source on the first pass. Run the column width budget from
   `table-design.md` before choosing `tabularx`/`tabular*`, and Run the repeated-label compression
   check before writing row labels. If a table declares `\linewidth`, `\columnwidth`, or
   `\textwidth`, it must include a real fill mechanism (`@{\extracolsep{\fill}}` for mostly numeric
   `tabular*`, or a real `X`/`Y`/`Z` prose column for `tabularx`); otherwise use a centered
   natural-width `tabular`. Use `booktabs`; never use `\hline` or vertical rules.
   Bold table headers as a general table-design default: model/setting headers, metric headers, and spanner
   headers all become visually firm when present.
7. Apply the correct design pattern from `table-design.md`. For category comparison rows, use
   restrained italic group labels and fine `\cmidrule` / `\midrule` grouping. Do not create boxed
   blocks.
8. Apply the placement contract from `table-placement.md`. Span follows reader task + table density class,
   not taste. In a two-column paper, a load-bearing main-results table may use `table*`; in a
   one-column paper, use regular `table` and size by `\linewidth`.
   Do not promote compact secondary result tables to `table*`; load the placement reference and
   split/abbreviate/move detail when a secondary table is too dense.
9. Mark metric direction in headers when known. If Metric direction unknown appears in the contract,
   do not guess metric direction; ask, mark unknown, or avoid best-value emphasis.
   Main paired-rate scorecards must not be emitted as a flat one-row header table: use group headers
   such as Coverage, Rates, and Outcome counts, and bold the declared extrema according to the table
   contract.
10. Run cross-table consistency before returning a draft: method order, metric precision, public
   method name, abbreviation expansion, and highlight conventions must match across the paper.
11. After compiling the full paper, run the compiled-layout QA script from the `academic-review` skill:
   `python3 <academic-review>/scripts/inspect_compiled_layout.py paper --pages tables --out-dir paper/layout-qa`.
   The run must leave a layout QA artifact (`paper/layout-qa/layout_qa_summary.md`) plus rendered pages or a contact sheet for the table pages. Use that artifact to inspect margin crossing,
   clipping, right-side underfill, first-column wrapping, unreadable font, sparse float pages, and
   float order before returning the draft.

## Hard Gates

- **Never let a table overflow.** A table wider than its declared container is a hard defect in body,
  appendix, and supplement. Apply the ladder in `table-placement.md` before returning the draft.
- **Never leave a declared full-width table underfilled.** `tabularx{\linewidth}{p{...}rrrr...}` or
  `tabularx{\textwidth}{L{...}rrrr...}` without `X`/`Y`/`Z` stretch or `\extracolsep{\fill}` is a
  hard defect: the rules span the page while the cells stay left-packed and leave a large blank band.
- **Long headers overflow narrow columns.** Verbose headers can break a single-column table even at
  low column counts. Abbreviate headers and expand them in captions/prose, or promote/split only when
  the placement rules justify it.
- **Own-method row highlight.** For baselines vs. ours tables, put the proposed method in the final
  block. If it is best on primary metrics, bolding alone is not enough for main or near-main
  comparisons unless color is forbidden.
- **Own-method separator.** Insert a booktabs separator before the own-method row so the final block
  reads as the conclusion of the comparison.
- **Do not special-case literal model names.** Reuse the visual grammar across future papers; classify
   each new table and adapt the pattern to its evidence role.
- **Never hard-code structural numbers in source.** Use `Table~\ref{...}`, `Figure~\ref{...}`,
  `Section~\ref{...}`, and `Appendix~\ref{...}` with generated labels.
- Compile, run `inspect_compiled_layout.py`, inspect every rendered page containing a table, and
  fix overfull boxes, unresolved `Table ??` / `Figure ??`, clipping, right-side underfill,
  unreadable text, float-page sparsity, or inconsistent numeric precision before returning the
  draft. Source/log checks alone are insufficient when a table exists; the compiled table pages
  and contact sheet must be available as review evidence.
