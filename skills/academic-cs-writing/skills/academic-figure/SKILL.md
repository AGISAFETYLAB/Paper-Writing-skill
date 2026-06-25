---
name: academic-figure
description: Use when creating, revising, auditing, or polishing figures and tables for a research paper — data-driven plots (bar/line/heatmap/radar/scatter), deterministic schematic diagrams (pipeline/framework/architecture/flowchart/taxonomy), picture-style illustrations (teaser/concept/method illustration), qualitative composites, and publication LaTeX tables (booktabs, span/overflow/appendix layout). Triggers on figure/table requests with or without a full draft, including Chinese phrasings like 论文配图、科研绘图、画图、作图、出图、论文图表、画个图、配图、表格排版、做表. Part of the academic-writing collection; the academic-writing hub delegates all figure/table work here.
---

# Academic Figure & Table

This skill produces and audits every **figure and table** for a paper. It is independently
invokable ("just make this figure", "fix this table's layout") and is also the subsystem the
**`academic-writing`** hub delegates to whenever a draft needs a display item.

Display-item boundary:

- **Plot =** a data-driven figure: bar, line, heatmap, radar, scatter, distribution, or other chart
  rendered from result files.
- **Schematic =** a deterministic technical diagram: pipeline, framework, architecture, workflow,
  taxonomy, benchmark-construction flow, or system overview.
- **Picture =** a raster or illustrative visual: teaser, conceptual method illustration, scene-like
  overview, screenshot/qualitative composite, or image-model-generated picture.
- **Table =** a LaTeX tabular display: numeric result matrix, ablation, data split, taxonomy,
  configuration, protocol, or qualitative examples rendered as rows and columns.

Cross-skill stance and integrity rules live in `../../_shared/core/`. Do not draw figures from
memory or from this entry point. `manifest.yaml is the detailed routing table`; use it to load only
the workflow, reference, or script needed for the current display item.

## ⚠️ Scope and integrity

Figures and tables present existing evidence; they never invent it. Read data from workspace result
files; **do not hardcode numbers from memory**, and do not "improve" results. A figure with an
unsupported or fabricated value is a defect, not a polish. Mirror the user's interaction language
(see `../../_shared/core/stance.md`).

## Blocking palette rule

For every generated display item that uses color, default to this skill's local palette system.
Unless the user explicitly supplies a palette, provides a style reference, or asks to change colors,
data-driven plots must load `references/figures/palette-system.md` before plotting code is written
and must use `scripts/cs_palette.py` as the executable palette source.

Generated plotting code must import or mirror the registered `CS_*` palette names. Do not invent
local hex palettes, rely on the matplotlib/seaborn default cycle, use rainbow/jet colormaps, or
silently adapt external colors. If a requested style reference has useful colors, normalize them to
a named `CS_*` palette first unless the user explicitly asked for a new palette. Unregistered color
use is a blocking figure defect, not a visual preference.

## Routing protocol

1. **Load the core layer.** Read `manifest.yaml` and the `always_load` file
   (`../../_shared/core/stance.md`) for language and integrity policy.
2. **Classify the display item.** Decide which execution fragment applies:
   - Plot → `workflows/plot.md`.
   - Schematic → `workflows/schematic.md`.
   - Picture → `workflows/picture.md`.
   - Table → `workflows/table.md`.
   A request with multiple display items loads each matching fragment.
3. **Resolve the venue kind** (conference or journal) — it selects the sizing reference and, for
   journal, the figure-contract. Default to conference unless the caller says journal.
4. **Build the item using the loaded workflow**, then open on-demand references and scripts from the
   manifest only when their condition applies.
5. **Inspect every rendered item before accepting it.** A script that runs without error is not a
   passing figure; the looked-at PNG / compiled PDF page is. Run the Display Review Gate and, for
   tables, the overflow/appendix inspection.

For paper-level runs, the confirmed Paper Framework's Figure Plan is an execution contract. Track
planned display items in `paper/framework-execution-report.md`; do not return a draft with planned
main-paper items left as missing placeholders.

## Optional MCP display helper

`mcp-servers/paper-figure/` is a narrow display helper. It can classify display ideas, write
templated FigureSpec schematic skeletons, validate/render medium-complexity FigureSpec diagrams,
and write Picture Brief prompts. It does not call image APIs or invent paper content. For
picture-style illustrations, it records the renderer route only; the actual render happens in a
separate picture-renderer step or current-agent fallback.

## Why this split

- The figure/table subsystem is self-contained and heavy, so it lives in its own skill and can be
  invoked alone.
- Each invocation loads only the relevant workflow plus the references that step needs, instead of
  the whole figure corpus.
