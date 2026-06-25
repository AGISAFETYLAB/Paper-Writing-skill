# Figure Router

Compatibility router for figure tasks. New invocations should load the specific execution workflow
from `manifest.yaml`:

- `workflows/plot.md` for data-driven charts.
- `workflows/schematic.md` for deterministic framework, pipeline, architecture, workflow,
  flowchart, taxonomy, benchmark-construction, or system-overview diagrams.
- `workflows/picture.md` for teaser, conceptual method illustration, raster overview, screenshot,
  or qualitative composite figures.

For paper-level runs, the confirmed Paper Framework's Figure Plan is an execution contract. Track
planned main-paper display items in `paper/framework-execution-report.md`; do not leave a planned
main-paper item as `not yet generated`, a registry comment, or a missing placeholder.

After individual figure routes pass, run the cross-figure checklist in
`references/figures/qa-contract.md` and collect final inclusion blocks in
`paper/figures/latex_includes.tex`.
