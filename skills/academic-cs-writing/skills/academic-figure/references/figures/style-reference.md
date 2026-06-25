# Figure Style Reference

Use this reference when the user supplies an example figure, PDF, screenshot, or prior paper figure
as a style reference for a new paper figure.

If the reference is a bundled local asset under `assets/chart-atlas/` or `assets/gallery/`, also
load `references/figures/asset-reference.md` and follow its asset-specific content-import boundary.

## Style Reference Boundary

A style reference is not a content source. It may shape how the new figure looks, but it must not
shape what the new paper says.

## Style-Only Extraction

Extract only visual grammar:

- palette family and exact reusable colors,
- line weights, marker shapes, fill alpha, hatch or redundant encodings,
- grid, ring, axis, spine, and separator treatment,
- typography scale, panel-label position, title/caption placement,
- legend position, legend columns, direct-label strategy,
- panel layout, aspect ratio, whitespace, and figure width/height behavior.

Record the extraction as `style-only extraction` in the chart design row or
`paper/framework-execution-report.md`.

## Content Import Ban

Do not import research content from the reference figure:

- domain terms,
- metric names,
- result values,
- caption claims,
- paper-specific labels,
- dataset, model, method, benchmark, task, taxonomy, or product names,
- figure IDs, panel titles, abbreviations, or code words from the reference paper.

Treat all labels in the reference image as placeholders to discard. Replace them with the current
paper's own Writing Policy terms, Figure Plan message, data source, and verified labels.

## Neutral Naming

Name reusable style presets by visual function, not by the source paper or research topic.

Use names such as:

- `shared-legend-radar`,
- `coverage-donut-muted`,
- `paired-opposing-scorecard`,
- `muted-categorical`,
- `journal-panel-grid`.

Do not name a preset after the user's project, dataset, metric, model, task, app, venue-specific
example, file stem, or reference-figure subject.

## Adaptation Check

Before rendering, answer internally:

1. Did I keep only palette, layout, typography, marker, legend, and spacing decisions?
2. Did I replace every reference label and metric with the current paper's own labels and metrics?
3. Did every plotted value still come from the current workspace source file?
4. Would removing the reference figure leave the scientific claim unchanged?

Any "no" means the figure is borrowing content, not style; revise the design before plotting.
