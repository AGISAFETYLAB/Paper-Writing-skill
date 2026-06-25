# Figure Planning

Use this reference only when a Paper Framework, full draft, or revision needs figures or tables.
Do not load it for purely textual Writing Policy work unless the user explicitly asks about figures.

## Contents

- Purpose and ownership boundary
- Display Item Contract, chart-form diversity, and width/height contracts
- Figure Plan format and terminal localization
- What to draw, insertion rules, generation routes, MCP contract, and caption rule

## Purpose

Figure and table planning decides four things:

1. what visual asset the paper needs,
2. where it should be inserted,
3. which layout width it targets,
4. how it should be generated or sourced.

It does not decide the paper's core claims. Claims and evidence come from the Writing Policy.

## Ownership Boundary

This file owns Display Item Contract, Figure Plan format, layout target selection, and generation-route routing.
It does not own chart-type selection, plotting code, palette definitions, or the executable Display Review Gate.

## Display Item Contract

A publication-quality academic figure or table is a visual argument, not decoration. Before filling
the Figure Plan routing table, establish the contract below for each planned display item. This
applies to data plots, architecture diagrams, pipeline figures, teaser pictures, qualitative grids,
and LaTeX tables.

### The Five-Point Display Contract

Before assigning a generation route or writing code, establish:

1. **Core conclusion**: the one-sentence claim this figure must support. Every panel, label, and
   visual choice must serve this conclusion. If a planned panel does not carry a unique piece of
   evidence for the conclusion, drop it or merge it.

2. **Evidence chain**: map each planned panel/subfigure to a specific piece of evidence from the
   Writing Policy. A panel without a mapped claim or evidence source is decoration and should be
   removed. The chain must trace back to concrete workspace result files or confirmed paper facts.

   For data-driven plots, load `chart-taxonomy.md` immediately after this contract and record a
   chart design row for each panel: chart family, source file, statistic/interval, layout target,
   palette preset, label strategy, and export formats. This includes the full chart families in
   `type.md`: vertical/horizontal bars, grouped bars, stacked bars, line charts, scatter plots,
   Pareto frontiers, radar charts, heatmaps, box plots, histograms, violin plots, density plots,
   pie charts, and donut charts.

3. **Display type**: classify the item into one of:
   - `quantitative comparison`: bar, line, scatter, heatmap, or table driven by result data,
   - `pipeline-architecture`: ordered stages, system components, or workflow with node-edge
     relationships,
   - `teaser-composite`: overview illustration combining problem, method, and evidence visually,
   - `qualitative-grid`: example cases, screenshots, or image panels showing representative outputs,
   - `latex-table`: taxonomy, result matrix, qualitative examples, or benchmark statistics rendered
     directly in LaTeX.
   The display type determines the generation route, not the other way around.

4. **Backend / route**: for data-driven plots, confirm the plotting backend. Python
   (matplotlib/seaborn) is the default unless the user explicitly requests another plotting stack.
   For pipeline, framework, architecture, workflow, taxonomy, benchmark-construction, and
   system-overview diagrams, default to a deterministic schematic route (FigureSpec, Mermaid, TikZ,
   or hand-authored SVG; see `schematic-design.md`). For teaser and conceptual method pictures,
   use `picture-generation.md`; an image renderer may render labels directly, but every label must
   be verified. Do not hand-draw pipeline boxes in matplotlib; use the schematic route instead.

   **Teaser Picture Route Gate.** When the Figure Plan names a teaser, overview illustration,
   conceptual method picture, or scene-like visual, do not downgrade it to `deterministic schematic`
   merely because it contains arrows or labels. If an API-visible renderer is configured
   (`GEMINI_API_KEY`, `OPENAI_API_KEY`, or an explicitly available image bridge), the generation
   route must be `AI picture illustration` and the full draft must actually render the Picture Brief
   before returning. Use `deterministic schematic` only for formal technical diagrams whose main
   purpose is exact node/edge structure.

5. **Export contract**: set final dimensions (single-column or double-column), primary output format
   (PDF for LaTeX data charts; PNG for AI-generated pictures; SVG for editable diagrams), target
   DPI, color space, and whether editable text is required. For data charts, PDF is the canonical
   output with PNG as raster fallback.

### Chart Form Diversity Gate

For a full paper or any Figure Plan with two or more numeric plots, run this gate before confirming
the framework and again before rendering:

1. List every numeric display item and its `Chart form` (`bar`, `grouped bar`, `line`, `heatmap`,
   `radar`, `donut`, `pie`, `scatter`, `distribution`, `table`, etc.).
2. Check whether the planned set uses the same chart form for every result plot. If yes, revise at
   least one item unless the data semantics truly require the same encoding.
3. **claim-to-chart fit beats visual novelty**: do not choose donut/pie/heatmap just to look varied.
   Use a different form only when it better serves the conclusion.
4. Use composition or coverage forms for single whole-part snapshots: `donut` or `pie` for <=5 main
   slices plus total `n`, stacked bar for comparable shares, heatmap for matrix coverage. A taxonomy
   or benchmark coverage plot often fits this class better than another bar chart.
5. Keep bars for exact comparisons across models/categories, especially when the reader must compare
   values precisely. The rule is that not every numeric display item should be a bar chart, not that
   bar charts are disallowed.

### Display Width Contract

Every planned figure or table must declare one layout target:

- `single-column`: insert with `\includegraphics[width=\linewidth]`, `\columnwidth`, or a table
  whose tabular environment is bounded by `\linewidth`.
- `double-column`: use `figure*` or `table*` and bound content by `\textwidth`.
- `appendix`: still choose `single-column` or `double-column`; appendix material must not exceed
  the printable area, and appendix placement does not lower the visual standard.
- `supplement`: use when the item is too wide or dense to stay readable in the paper.

#### Column-Span Decision (decide span by role + width need, not by figure number)

Span is a real design decision — do not default everything to one column, and do not span everything.
Decide per item:

**First-figure vs. main-process rule.** In a two-column paper, the opening story / teaser figure
usually stays single-column when it is a compact problem-setting visual; the main process,
framework, pipeline, or architecture diagram normally spans both columns because the reader follows a
horizontal structure. These may be the same figure only when the opening figure is also the real
framework/pipeline figure; otherwise keep the teaser compact and let the later framework figure use
the cross-column slot. In a one-column paper, both are ordinary `figure` floats: the teaser is usually
`0.55--0.75\linewidth`, while the process/framework/pipeline figure is usually
`0.90--1.00\linewidth`.

**Two-column venues (ACL/EMNLP, ICML, CVPR, AAAI, IJCAI, IEEE-conf).** Default is single-column
(`figure`/`table` + `\columnwidth`). Promote to cross-column (`figure*`/`table*` + `\textwidth`,
placed at the top or bottom of the page) when ANY of these hold:

- the item is a **pipeline / framework / architecture / system-overview / benchmark-construction
  diagram** with left-to-right horizontal flow — these read as cramped, illegible strips in a ~3 in
  column and belong full-width;
- it is a **multi-panel figure** (≥2 panels side by side — e.g. a per-condition and a per-subgroup radar, or
  grouped small-multiples);
- it is a **wide comparison**: a grouped-bar/heatmap/radar with enough labels, cells, or legend
  complexity to become unreadable in one column, or a table that the table-placement contract
  classifies as wide enough to need full width.

Do not promote a radar/heatmap merely because of chart family. A single radar with 5--6 spokes and
up to 4 methods, or a small heatmap such as 4x6 cells with short labels, should first be tested as a
single-column figure at the venue's native column width. Promote only if the rendered text falls
below the legibility floor or the legend consumes too much of the axes.

For a `figure*`, still choose the actual `\textwidth` fraction by density. A cross-column float is a
placement decision, not a command to fill the whole page width:

- `0.65--0.78\textwidth`: moderate single-panel radar/heatmap/grouped comparison that needs more than
  one narrow column but is not a central evidence figure;
- `0.80--0.90\textwidth`: wide comparison with long labels, a shared legend, or dense annotations;
- `0.90--1.00\textwidth`: dense multi-panel evidence, framework/pipeline diagrams, or the primary
  quantitative result where readability depends on the full span.

If a single-panel radar or a small 4x6 heatmap is inserted at `>0.85\textwidth`, treat that as a
review point unless the Figure Plan explicitly marks it as load-bearing central evidence.

**Keep single-column** when the item reads comfortably at ~3 in: the **teaser / first concept figure**
that conveys the idea in a compact (often vertical) composition; a single small plot (one bar/line/
scatter, ≤4–5 categories); a narrow taxonomy/definition/setup table (≤~4 short columns). A teaser that
genuinely fits one column stays single-column rather than being stretched across the page. For a
two-column conference paper, the story/teaser Fig. 1 defaults to single-column unless it is also the
paper's pipeline / framework / architecture figure and truly needs a horizontal reading path; record
that exception in the Paper Framework instead of silently stretching the first image.

**One-column venues (NeurIPS, ICLR) and single-column journals.** There is no `figure*`/`table*`; the
text block is one wide column (~5.5 in). Decide width as a fraction of `\linewidth` instead of span:

- full `\linewidth` only for pipelines, architectures, multi-panel figures, dense heatmaps, and wide
  comparisons whose labels or legend become unreadable when narrower;
- a centered fraction (`0.50--0.70\linewidth`) or a `subfigure` row for a small/secondary single plot,
  so it does not dominate the column;
- combine related small charts into one multi-panel figure rather than stacking many tiny floats.

**Single-column papers have no cross-column float class.** Do not write `figure*` or `table*` in a
single-column template. Instead, size by role as a fraction of `\linewidth`: story/teaser figures
usually sit at `0.55--0.75\linewidth` when they are illustrative and compact; pipeline/framework/
architecture figures and multi-panel evidence figures use `0.90--1.00\linewidth`; small secondary
plots use `0.50--0.70\linewidth`; wide numeric comparisons use full `\linewidth` only when the
reader must compare many columns or panels at once. If two small related charts explain one claim,
merge them into a single multi-panel figure with a shared legend instead of scattering them as
separate floats.

**Content-density sizing gate.** Do not equate available column width with needed figure width. In a
one-column paper or single-column journal, size by evidence density after the layout target is set:

- low-density single plots (one small bar chart, horizontal ablation with <=6 rows, pie/donut
  composition snapshot, one simple scatter) usually sit at `0.45--0.65\linewidth`;
- medium-density single plots (line, distribution, Pareto, 4-series grouped bar) usually sit at
  `0.60--0.78\linewidth`;
- dense matrices, multi-panel plots, long legends, framework/pipeline diagrams, and central result
  figures may use `0.90--1.00\linewidth`.

If a low-density plot needs more than `0.70\linewidth`, first check whether the labels, legend, or
aspect ratio are the real problem. Widen only when the rendered page proves it is needed.

Compact single-column heatmaps, coverage matrices, and secondary data grids should normally be
inserted at `0.60--0.70\linewidth` in one-column templates. Treat `>0.70\linewidth` as a layout
defect unless the confirmed Paper Framework explicitly budgets the item as a large main evidence
figure.

**Appendix Display Parity Gate.** Appendix figures and tables are not second-class. Apply the same
Display Item Contract and rendered-page review used for body displays. For a two-column conference
appendix, keep compact protocol tables, inventories, label glossaries, and small secondary plots
single-column by default; do not promote them to `figure*` or `table*` only because they are in the
appendix. A single-panel appendix heatmap or small result matrix should first be tested as
single-column; if it truly needs cross-column placement, include it at `0.60--0.70\textwidth` or
`0.65--0.78\textwidth` rather than filling the whole span by habit. Promote to wider widths only
when labels, cell text, or a full result matrix fail the rendered legibility floor.

Appendix float pages are part of the paper QA surface. A half-empty page caused by sparse
cross-column floats, an oversized appendix heatmap, a full-width table with only a few short cells,
or a caption/table/figure that looks rougher than the body is a defect that must be revised before
returning the draft.

For a one-column template, the Figure Plan `Layout` should remain `single-column`; record the actual
width fraction in the message, display-item budget, or framework execution report (for example,
`single-column, 0.65\linewidth teaser` or `single-column, 0.95\linewidth pipeline`). Do not encode
one-column full-width figures as `double-column`.

**Multi-panel layout.** Prefer **one hero/primary panel plus subordinate evidence panels** over a grid
of equal-sized subplots; panels need not be equal when the evidence is not equally important. Give a
pipeline/schematic panel the dominant area; align panels on a shared baseline, use small bold lowercase
panel letters (a, b, c) at the top-left, and a **single shared legend** rather than one legend per
panel. **Two charts that compare the same methods on two related category axes (for example, the same
rate by category group and by outcome group) belong in one multi-panel `figure*` with a shared legend
— not two separate single-column floats**, which read as disconnected and waste space. A radar/polar comparison is hard to
read at single-column width with 6+ spokes and 3+ methods; use a cross-column multi-panel layout, or
switch to grouped bars / a heatmap if the radar still muddies.
`audit_draft.py --framework` treats multiple standalone radar/profile figures in the same section as
a blocking display-plan defect unless they are merged into one multi-panel display or one is moved out
of the main reading path.

For any figure with two or more panels, load `references/figures/multi-panel-patterns.md` before
composition. Use its CS templates when the panel roles match; otherwise record why a custom
layout is needed.

For table-specific span, wrapping, resize, appendix, and supplement decisions, load
`references/tables/table-placement.md`; Figure Planning only records the provisional layout target.

**Height also has a budget, not just width.** A picture set to `width=\textwidth` is as tall as its
aspect ratio dictates: a 16:9 render at double-column width is ~9–10 cm tall, which for a teaser or
pipeline banner is too tall and leaves empty bands. Plan concept figures as **wide, short banners**
(target aspect ~3:1 to 4:1 double-column, ~1.6:1 to 2:1 single-column) so they occupy ~4.5–6 cm of
height, and the rendered image must **fill its frame** (no baked-in empty top/bottom bands). When a
render is mis-shaped, cap the height (`height=...,keepaspectratio`) or trim whitespace
(`trim=... ,clip`) rather than shipping a tall box with a thin content strip. See
`picture-generation.md` for the height/trim mechanics.

**Overlays must not exceed the image.** For the AI-illustration + TikZ-overlay pattern, the figure
must not be wider than its `width=\textwidth` image. Clamp the `tikzpicture` bounding box to the
image (`\useasboundingbox`) and inset edge labels so no overlay node pushes the figure into the
margin. An `Overfull \hbox` for a figure is a hard defect, not a cosmetic warning.

### Display Review Gate Routing

Every planned figure must pass the executable review loop in
`references/figures/display-review-gate.md` after rendering. Figure Planning only records that the
planned item requires that gate; rendered-output inspection, failure signatures, and regenerate
decisions live in the review-gate reference.

### Unified visual family

All figures in one paper must read as a set, not as figures from different papers. Before
finalizing the figure set, confirm across every figure:

- **One palette**: the same method → the same color in every figure; reuse `CS_PEER_PALETTE`
  / `CS_HERO_BASELINE_PALETTE` consistently, never remap.
- **One type system**: the same font family and a consistent size hierarchy (axis vs tick
  vs annotation) across figures.
- **Consistent encodings**: the same metric uses the same axis orientation, unit, and
  colormap everywhere; shared legends use the same ordering.

After all figures pass the review gate, write a single `paper/figures/latex_includes.tex`
that collects each figure's `\includegraphics` + `\caption` + `\label` block, so the main
draft can `\input` them and inclusion stays consistent.

## Figure Plan Format

Use a compact table in the Paper Framework:

When this table is shown in a terminal-facing Paper Framework checkpoint, it follows the user's
interaction language. The saved framework artifact may keep the English schema, but the terminal
heading and human-facing column labels must be localized; for Chinese, use `图表计划` with columns
`ID`, `类型`, `图形形式`, `版式`, `位置章节`, `信息点`, `来源`, and `生成路径`. Keep figure/table IDs,
layout enum values, file paths, and generation route identifiers unchanged. Chinese terminal chart-form values must be localized, while the saved framework artifact keeps canonical English
chart-form values. Use at least this mapping when applicable: `schematic -> 示意图`,
`donut -> 环形图`, `pie -> 饼图`, `bar -> 柱状图`, `grouped bar -> 分组柱状图`,
`stacked bar -> 堆叠柱状图`, `horizontal bar -> 横向条形图`, `heatmap -> 热力图`,
`line -> 折线图`, `scatter -> 散点图`, `radar -> 雷达图`, `distribution -> 分布图`,
and `table -> 表格`.

Figure Plan must be rendered as a Markdown table in the terminal checkpoint. Do not replace it with a prose list such as `图表计划包含`; a short prose overview may appear before the table, but the table
itself must still be shown.

```markdown
| ID | Type | Chart form | Layout | Section | Message | Source | Generation route |
|---|---|---|---|---|---|---|---|
| Fig. 1 | overview / pipeline | schematic | double-column | Introduction | Shows the paper's problem-setting-method-evidence arc. | Writing Policy + method notes | FigureSpec MCP or manual SVG |
| Fig. 2 | main result plot | grouped bar | single-column | Experiments | Shows the primary comparison supporting C1. | `results/main.csv` | reproducible plot script |
| Fig. 3 | benchmark coverage plot | donut | single-column | Method | Shows the composition of task categories with total n. | benchmark manifest | reproducible plot script |
| Tab. 1 | taxonomy table | table | single-column | Method | Defines task categories with examples. | benchmark manifest | LaTeX `tabularx` |
```

Keep only likely main-paper figures and tables. Put appendix-only or optional visuals in drafting
notes, not the main framework. The framework should show enough chart-form variety that result
figures read as a designed evidence sequence rather than a row of default bars.

## What To Draw

Choose figures by paper need, not decoration:

| Need | Recommended visual | Usual section |
|---|---|---|
| Reader needs the whole idea early | teaser / overview figure | Introduction |
| Method has ordered stages | pipeline diagram | Method / System |
| System has components or interfaces | architecture diagram | Method / System |
| Benchmark has task/data construction | benchmark construction flow or taxonomy | Benchmark / Dataset |
| Claim depends on a comparison | bar, line, scatter, heatmap, or table | Experiments / Evaluation |
| Claim depends on robustness | stress-test plot, ablation table, failure taxonomy | Experiments / Analysis |
| Claim depends on examples | qualitative case grid or example table | Analysis / Discussion |

Avoid figures that only restate text, repeat a table without adding comparison value, or introduce
unsupported claims.

## Insertion Rules

- Put the first overview/teaser figure in the Introduction only when it helps a skim reader
  understand the contribution before Method.
- Put architecture and pipeline figures where the corresponding mechanism is defined.
- Put main-result figures before ablations and secondary analyses.
- Put failure cases near the claim they limit or explain.
- Do not reference a figure before the paper has defined the terms needed to understand it.
- If a figure would force a different section order, update the Paper Framework and ask the user to
  confirm.

## Generation Routes

Use the lightest reliable route:

| Route | Use for | Output |
|---|---|---|
| existing asset | screenshots, qualitative examples, already-drawn diagrams | copied asset under `paper/figures/` |
| reproducible plot script | numeric results, ablations, scaling, heatmaps | Python script following `plot-style.md` rules and `chart-patterns.md` patterns + SVG/PDF/PNG |
| LaTeX table | result tables, feature comparison, benchmark statistics | `.tex` table or inline table |
| deterministic schematic | pipeline, framework, architecture, workflow, taxonomy, benchmark construction, system overview | FigureSpec/Mermaid/TikZ/SVG source + SVG/PDF/PNG |
| AI picture illustration | teasers, conceptual method illustrations, scene-like overview pictures | Picture Brief + renderer route + labeled PNG from a separate renderer; TikZ overlay only as a fallback for a label the model misspells |
| current-agent picture drawing | fallback when no image API exists for a picture route | agent-created illustration plus Picture Brief; still verify or overlay text |

For plots, data-driven plots default to Python. Do not hardcode numbers from memory. Read from
result files and follow `plot-style.md`. For schematics, keep the source specification or source
file so the figure can be revised. For AI-generated pictures, follow `picture-generation.md`:
always write `paper/figures/prompts/<figure-id>.md` before rendering, and do not let the image
renderer invent claims, modules, datasets, results, or labels.

## MCP Contract

If a `paper-figure` or FigureSpec-compatible MCP is available, use it only for figure-specific
tasks:

- classify a proposed visual into a route,
- write a templated FigureSpec JSON skeleton,
- validate or render a medium-complexity deterministic diagram,
- write a Picture Brief and record the renderer route for a picture item,
- record figure metadata for later LaTeX insertion.

The MCP must not invent paper claims, experiment results, citations, or section structure. It works
from the confirmed Writing Policy, confirmed Paper Framework, and concrete source files. It also
must not call image-generation APIs; picture rendering happens in a separate renderer step or
current-agent fallback.

Suggested MCP outputs:

```text
paper/figures/figure-plan.md
paper/figures/specs/<figure-id>.json
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.svg
paper/figures/<figure-id>.pdf
paper/figures/<figure-id>.png
paper/figures/latex_includes.tex
```

If the MCP is unavailable, continue with current-agent drawing for pictures and direct Python
generation for data charts.

## Caption Rule

Every caption should state:

1. the figure's message,
2. the comparison or mechanism shown,
3. the claim or section argument it supports.

Avoid captions that merely list visual elements.
