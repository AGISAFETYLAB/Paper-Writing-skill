# Schematic Workflow

Execution-only workflow for deterministic technical diagrams: framework, pipeline, architecture,
workflow, flowchart, taxonomy, benchmark-construction flow, and system overview figures.

## Default Route

Use a deterministic editable route by default:

1. **FigureSpec -> SVG/PDF/PNG** for most paper framework, pipeline, architecture, taxonomy, and
   benchmark-construction diagrams. Use the built-in templates (`pipeline`, `architecture`,
   `taxonomy`, `benchmark`, `minimal`) as starting points, then replace placeholder labels with
   exact paper terms.
2. **Mermaid** for quick flowcharts, state machines, or sequence diagrams when publication styling
   is secondary or the figure is a planning artifact.
3. **TikZ** when LaTeX-native editing, exact math labels, or final typeset consistency matters.

Do not send formal framework/pipeline/architecture diagrams to an image model by default. Use the
picture workflow only when the user explicitly asks for an illustrative or scene-like rendering
rather than a technical schematic.

A teaser or concept overview is not a formal technical schematic solely because it has arrows,
devices, or short labels. If an API-visible picture renderer exists and the Figure Plan says teaser,
overview illustration, conceptual method picture, or scene-like visual, route to
`workflows/picture.md`; keep this schematic route for exact technical node/edge diagrams.

## Workflow

1. Read the confirmed Figure Plan entry when present. Record or update the item's row in
   `paper/framework-execution-report.md` for paper-level runs.
2. Load `references/figures/figure-planning.md` and `references/figures/schematic-design.md`.
   Use the Display Item Contract to pin the message, supported claim, exact labels, source files,
   expected nodes/modules, and edge semantics before drawing.
3. Decide the schematic route: FigureSpec, Mermaid, or TikZ. Prefer FigureSpec for
   medium-complexity paper-ready editable SVG diagrams. If the figure needs dense callouts,
   nonstandard geometry, or exact typesetting, use the FigureSpec template as a sketch and move to
   hand-authored SVG or TikZ.
4. Draft the source artifact first (`paper/figures/specs/<figure-id>.json`, `.mmd`, or `.tex`).
   Keep source files so the figure can be revised.
5. Render to a paper-includable artifact under `paper/figures/`:
   - SVG primary for FigureSpec or hand-authored SVG,
   - PDF for LaTeX inclusion when available,
   - PNG preview for visual inspection.
6. Inspect the rendered preview and check semantic accuracy: every module exists, labels match the
   paper terminology, arrow direction is correct, groups/layers are legible, and no text overflows.
7. Insert only at the Paper Framework's target section and width. In two-column papers, main
   left-to-right framework/pipeline diagrams normally use `figure*`; in one-column papers size by
   `\linewidth`.

For prose placement and captions, load `references/prose/display-in-prose.md`.
