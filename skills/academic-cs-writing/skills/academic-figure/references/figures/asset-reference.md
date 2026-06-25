# Asset Reference Rules

Use this reference when the skill includes local visual examples under
`assets/chart-atlas/` or `assets/gallery/`, reusable table skeletons under
`assets/table-patterns/`, or when the user asks to match a bundled example.
Assets are visual/structural references, not paper evidence.

## Directory Roles

| Directory | Intended contents | How to use |
|---|---|---|
| `assets/chart-atlas/` | chart examples such as radar pairs, coverage donuts, grouped bars, heatmaps, scorecards, and multi-panel layouts | extract chart visual grammar only |
| `assets/gallery/` | finished-looking figure examples such as teaser, qualitative grid, schematic, and composite examples | extract layout, spacing, typography, and panel balance only |
| `assets/table-patterns/` | reusable LaTeX table skeletons for scorecards, ablations, matched deltas, taxonomy/protocol summaries, and setup/split summaries | extract table structure, spacing, grouping, and width strategy only |

Empty directories are acceptable while the skill is being developed. If an asset
directory is empty, continue from the written references instead of inventing an
example.

## Visual Grammar Only

Assets may inform:

- palette family or named palette choice,
- panel composition and aspect ratio,
- line weight, marker shape, hatch, fill alpha, and grid treatment,
- legend location and legend column count,
- label placement, whitespace, and panel-letter placement,
- relative sizing between a primary panel and supporting panels.

They must not supply the scientific content of the new paper.

## Content Import Ban

Do not copy labels, numbers, datasets, method names, claims, or captions from any
bundled asset. Treat visible text inside an asset as a placeholder to discard.
All paper-specific content must come from the current Writing Policy, confirmed
Paper Framework, Figure Plan, and concrete workspace data files.

## Required Record

When an asset influences a figure, record a short `style-only extraction` note in
the chart design row, Picture Brief, or `paper/framework-execution-report.md`.
The note should state:

| Field | Example |
|---|---|
| Asset | `assets/chart-atlas/two-radar-shared-legend.png` |
| Extracted visual grammar | two polar panels, shared legend below, white-filled markers |
| Content source | current paper result file or confirmed paper fact |
| Palette | named palette from `palette-system.md` |

If the asset suggests a palette that is not already named, do not scatter a new
hex list into the plotting file. Add or request a named palette in
`palette-system.md` first.
