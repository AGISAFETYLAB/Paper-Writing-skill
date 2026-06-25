# Display In Prose

Prose-only display guidance. Use this file after a figure or table has been selected for the paper
story. It does not decide body-vs-appendix placement, table span, table width, or table mechanics.
For table placement decisions, load `references/tables/table-placement.md`; for table visual grammar
and LaTeX patterns, load `references/tables/table-design.md`.

## Section Role

Figures and tables are visual arguments, not decoration. Each display item should make one claim
easier to understand, verify, or remember.

## Teaser Figure

Use a teaser when the Introduction benefits from an immediate visual summary of task, failure case,
method idea, benchmark setting, or surprising result. A teaser should be concrete and memorable,
align with the Introduction story, and avoid overcrowded text.

## Pipeline Figure

A pipeline figure should highlight novelty. If the whole pipeline is novel, show the full
input-to-output structure. If only one module is novel, highlight that module and avoid making the
rest look like the contribution.

## Result Figures

Use result figures for qualitative differences, failure modes, stress tests, trends, or application
potential that tables cannot communicate. Each result figure needs matched comparison conditions,
clear labels, and a caption with setting and notation.

## Tables In Prose

When a table is in the body, the surrounding paragraph should explain why the reader should look at
it and what pattern to notice. Do not use a table as a prose substitute. Do not introduce a table
whose only purpose is to dump definitions, filenames, or exhaustive variants.

## Caption Rules

Captions should state the setting, notation, and reading instruction. They should not become long
discussion paragraphs that duplicate the main text.

## Reference Contract

Every generated figure, table, equation, main section, appendix section, and referenced subsection
must receive a stable `\label{...}`. Prose must refer to structural items with `\ref`
(`Table~\ref{...}`, `Figure~\ref{...}`, `Section~\ref{...}`, `Appendix~\ref{...}`), never manual
numbers such as `Table 2`.

## Self-Check

- Does each display item carry one message?
- Does it serve the section's argument rather than decorate the page?
- Is the surrounding prose enough to tell the reader how to interpret it?
- Is the caption concise: setting, notation, and reading instruction?
- Are appendix-only or supplement-only items kept out of the main reading path?
