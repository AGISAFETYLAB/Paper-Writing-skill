# Schematic Design

Use this reference for deterministic technical diagrams: framework, pipeline, architecture,
workflow, flowchart, taxonomy, benchmark-construction flow, and system overview figures.

## Boundary

Schematic diagrams explain technical structure. They should be editable, reproducible, and
semantically exact. Use them when the reader must reconstruct modules, inputs/outputs, data flow,
system components, benchmark construction, task taxonomy, or evaluation protocol.

Do not route a formal technical schematic to an image model by default. Use
`picture-generation.md` only when the user explicitly asks for an illustrative, scene-like, or
raster concept picture instead of a node-edge technical diagram.

## Schematic Contract

Before drawing, record:

- Figure ID and target section.
- One-sentence message.
- Supported claim.
- Source files or confirmed Paper Framework facts.
- Exact nodes/modules/stages.
- Edge semantics: data flow, control flow, dependency, evaluation linkage, or grouping.
- Required labels and forbidden labels.
- Layout target: single-column fraction, full `\linewidth`, or two-column `figure*`.
- Output route: FigureSpec, Mermaid, TikZ, or hand-authored SVG.

## Route Selection

| Route | Use when | Output |
|---|---|---|
| FigureSpec | Medium-complexity paper-ready pipeline, framework, architecture, taxonomy, or benchmark-construction diagram that fits the built-in templates | JSON spec + SVG/PDF/PNG |
| Mermaid | Fast flowchart, sequence, state, or planning diagram where exact publication styling is less important | `.mmd` plus rendered preview when possible |
| TikZ | LaTeX-native schematic, math-rich labels, or exact typeset integration | `.tex` figure source + compiled PDF |
| Hand-authored SVG | Small schematic requiring direct manual tuning | SVG + PDF/PNG export |

FigureSpec is the default for formal paper schematics because it keeps node/edge structure explicit
and editable. Start from a built-in template when possible: `pipeline`/`framework`, `architecture`,
`taxonomy`, `benchmark`, or `minimal`. Replace placeholder node labels with exact paper terms before
rendering.

FigureSpec's built-in renderer is intentionally conservative. It handles clean node-edge diagrams
with groups, highlights, short labels, and mostly left-to-right or top-down flow. If the diagram
needs dense annotations, unusual geometry, many crossing links, precise math typesetting, or
publication art direction beyond the template, use the FigureSpec output as a sketch and finish the
figure in hand-authored SVG or TikZ.

## Layout Rules

- For left-to-right pipelines, use a wide horizontal layout. In two-column papers, this usually
  belongs in `figure*`; in one-column papers use `0.90--1.00\linewidth`.
- Use single-column only when the schematic has few nodes and no horizontal comparison task.
- Keep stage order visually obvious: input -> process/module(s) -> output -> evidence/evaluation.
- Group related modules with subtle background regions. Do not nest groups unless hierarchy is
  essential.
- Highlight novelty by emphasizing the novel module, task component, metric, or interface rather
  than making every box visually loud.
- Use exact paper terminology. Do not introduce new module names in the diagram.
- Keep labels short. Expand terms in the caption/prose instead of packing sentences into nodes.
- Use a small, consistent palette across the paper: neutral background regions, one signal color for
  the novel component, and quiet supporting colors for input/output/evidence.
- Do not draw a redundant figure title inside the schematic unless the venue or paper style
  explicitly wants it. The caption carries the title/message in normal research papers.

## Review Gate

Inspect the rendered schematic before accepting it:

- Every load-bearing module from the method or benchmark plan appears exactly once unless repetition
  is intentional.
- Arrow direction and edge labels are correct.
- Input/output/evaluation linkage is reconstructable without reading the full caption.
- Novel contribution is visually discoverable.
- Labels match the Writing Policy / Paper Framework spelling.
- Text is readable at final insertion size.
- No text, arrowhead, group label, or node crosses the canvas edge.
- The figure fits its declared width and produces no figure-related `Overfull \hbox`.

If any check fails, edit the source spec and re-render. Do not patch a semantic error only in the
caption.
