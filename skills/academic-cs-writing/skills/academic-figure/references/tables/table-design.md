# Table Design

Use this reference when a confirmed Figure Plan or standalone request contains a table. Keep the
table type, visual grammar, width strategy, and QA evidence explicit before writing LaTeX. Placement
belongs in `table-placement.md`.

## Table Contract

Record this compact contract in working notes or `paper/framework-execution-report.md`:

```text
Table ID:
Table kind:
Message:
Data source:
Source artifact:
Placement summary:
Visual grammar:
Column strategy:
Numeric precision:
Metric direction status:
Highlight rule:
Fallback:
```

One table carries one message. Split mixed taxonomy, aggregate metrics, and error-analysis content.
Glossary, inventory, complete task-list, and denominator-audit tables usually belong in the appendix.

## Classify First

Classify from evidence role before data shape:

| Evidence role | Likely table kind |
|---|---|
| headline method comparison | central scorecard |
| generality across datasets/tasks | multi-dataset matrix |
| quality/cost/robustness tradeoff | multi-metric comparison |
| component necessity | ablation |
| ordered threshold or setting sweep | sensitivity |
| paired prompts, modes, or interventions | matched-condition delta |
| train/dev/test/source composition | split/setup |
| codes, phases, protocol attributes | taxonomy/protocol |
| reproducibility settings | configuration |
| failure modes or examples | error/qualitative analysis |

If no Figure Plan exists, record the classification as provisional and revise after rendered QA.

## Visual Grammar

- Use `booktabs`; never use `\hline`, vertical rules, boxes, or harsh row striping.
- Use the shared CS table palette: header `#EEF3F8`, focus row `#F2F6FB`, rules `#4D4D4D`, group text `#374151`.
- Bold all header levels in comparison tables: first semantic column, spanners, and leaf metrics.
- Use `\multicolumn` + `\cmidrule` only for real metric, dataset, or outcome groups.
- Put the proposed/full method in the final block when it is the comparison conclusion; insert a
  separator before it.
- Use one pale row/cell shade only when it is redundant with bold and supports the main comparison.
- For setup, taxonomy, configuration, and protocol tables, do not use performance-table highlighting.
- Captions state evidence role, source scope, notation, and metric directions; they do not discuss results.

## Column width budget

Choose columns before writing LaTeX. Do not let stretch mechanics decide the layout.

Mostly numeric scorecards, ablations, and matrices:

- use compact `r`, `c`, or `S` numeric columns;
- use a bounded first semantic column such as `p{0.18\linewidth}` to `p{0.28\linewidth}`;
- abbreviate long row labels and expand them in caption/prose;
- prefer `tabular*` with `@{\extracolsep{\fill}}...` for full-width numeric tables;
- avoid `tabularx` layouts like `@{}Yrrrr...@{}` or `YZZZZZ` for numeric scorecards because the
  stretch label column narrows the numeric block and can wrap the first column.

Prose-heavy taxonomy, setup, qualitative, and audit tables:

- use `tabularx` only when a real prose column should absorb width;
- keep counts, flags, and metric columns compact;
- group repeated axis/phase/source labels instead of printing long phrases on every row.

A declared `\linewidth`, `\columnwidth`, or `\textwidth` table must have real fill: either
`@{\extracolsep{\fill}}` in `tabular*` or a true `X`/`Y`/`Z` prose column in `tabularx`. Otherwise use
a centered natural-width `tabular`.

## Repeated-label compression

Before finalizing rows, compress consecutive repeated group or setting names:

- insert an italic group row with `\multicolumn{...}{@{}l}{\textit{Group}}`;
- use short variant labels such as `Base`, `+A`, `Default`, or `Full`;
- expand abbreviations once in the caption or nearby prose;
- keep repeated labels only when sorting is non-consecutive or the venue requires self-contained rows.

Repeated long row labels are a design defect because they waste horizontal space and hide contrast.

## Pattern Library

Load `table-pattern-gallery.md` only after the Table Contract is filled. Default to the six core
skeletons; use the local 15-table reference gallery only for style regression or a hard-to-classify
layout.

| Table kind | Default design | Emphasis |
|---|---|---|
| central scorecard | bounded method column, metric spanners, compact numeric columns | final proposed block, bold best values, optional pale shade |
| multi-dataset/multi-metric | dataset or metric-family spanners | bold per declared metric direction |
| ablation | compact natural-width rows progressing toward full method | full/default row or decisive delta |
| sensitivity | ordered setting sweep | selected/default row, not every numeric maximum |
| matched delta | italic group rows, base-plus-variant rows, compact deltas | deltas tied to each base row |
| split/setup/config | counts/key-value/protocol notes | no performance highlighting |
| taxonomy/protocol/error/qualitative | wrapping prose columns and compact counts | group labels, totals, or status only |
| appendix audit/inventory | source scope, denominator, status, action | no performance highlighting |

## Metric Direction

When a table uses best-value emphasis, put directions in headers or captions (`$\uparrow$`,
`$\downarrow$`). If direction is not in the source, record `Metric direction unknown` and ask, mark
unknown, or omit best-value styling. Counts, IDs, hyperparameters, latency, and configuration values
are not automatically performance metrics.

## Cross-Table Consistency

Before returning a draft, check method order, public method names, abbreviation expansion, metric
precision, baseline family labels, row highlighting, and best-value conventions across all tables.

## QA Gate

After compilation, run the `academic-review` skill's `scripts/inspect_compiled_layout.py` and inspect
every rendered page containing a table. Keep `paper/layout-qa/layout_qa_summary.md` plus page PNGs or
a contact sheet. A table fails if:

- it crosses margins, clips, overlaps text, or is unreadable;
- a declared full-width table is left-packed or underfilled;
- a numeric scorecard uses unconstrained `X`/`Y`/`Z` stretch for labels;
- the first semantic column wraps when abbreviation would avoid it;
- prose appears in non-wrapping `l/c/r` columns;
- repeated labels are not grouped or abbreviated;
- numeric precision, metric direction, or highlighting is inconsistent;
- QA has only source/log checks and no rendered-page evidence.
