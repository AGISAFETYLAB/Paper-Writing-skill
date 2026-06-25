# Journal Figure Contract

Load this file for **journal papers** after `figure-planning.md` and
`references/figures/journal/figure-sizing.md`. It covers journal-specific figure
composition patterns, panel logic, aesthetic integration rules, and reviewer-risk assessment
— the compositional and strategic decisions that differentiate journal figures
from conference figures.

## The Core Difference

A conference paper figure usually answers "is the novel contribution real?" under
a hard page limit. A journal paper figure answers "is this a complete,
self-contained piece of evidence that survives multi-round review?" with more
space but higher expectations. This changes three things:

1. **Composition**: journals reward deliberate panel hierarchy — not every panel
   deserves equal space. Let the hero panel dominate.
2. **Thoroughness**: reviewers expect the figure to anticipate their questions
   (sample size, error bars, axis comparability, quantification of qualitative
   panels). Conference figures can sometimes get away with "we'll explain in the
   rebuttal"; journal figures cannot.
3. **Integration**: a journal multi-panel figure must read as one argument, not
   a pasted collage. Schematic colors and data-plot colors should relate; the
   visual vocabulary set in panel (a) should carry through to panel (f).

## Journal Figure Composition Patterns

Replace the baseline "Display type" classification (which routes to a generation
method) with these **composition patterns** when planning journal figures.
The composition pattern drives panel count, sizing, and evidence hierarchy — choose it
before picking a generation route.

| Composition pattern | When to use | Hero panel | Supporting panels |
|---|---|---|---|
| `quantitative grid` | The claim is mainly numerical comparison; no schematic or image is needed | Optional; often a dominant summary metric or the proposed method's bar | Shared axes, aligned scales, compact legends; equal panel sizes acceptable here |
| `schematic-led composite` | A workflow, mechanism, device, or experimental design must be understood before the data makes sense | One wide story panel (top or left), 35–60% of total figure area | 2–4 quantitative validation panels — smaller, visually quieter, below or to the right |
| `asymmetric hero layout` | The figure combines a dominant visual (schematic, embedding, or key result) with smaller support plots | One panel spans multiple grid rows/columns | Small support panels ranked by evidence value; uneven panel sizes are intentional |
| `image plate + quant` | Microscopy, imaging, histology, spatial overlays, segmentation, or qualitative grids lead the evidence | Image plate or representative image(s) | Scale bars, zoom crops, channel overlays, companion quantification bar/scatter |

**Rule**: do not default to a grid of equal-sized panels. A journal reviewer
reading a 2×3 grid of same-size panels does not know where to look. One panel
should carry the core conclusion; the others validate, localize, or contextualize
it. Unequal panel sizes are a feature, not a layout bug.

## Journal Panel Logic

For a journal multi-panel figure, order panels so the reader builds understanding
incrementally. Use this order unless the manuscript story clearly requires
another:

1. **Establish the system** — sample, method, cohort, device, experimental design,
   or workflow. This panel defines the visual vocabulary (colors, symbols, scale)
   for the rest of the figure.
2. **Show the main effect** — primary comparison, key result, or core claim.
3. **Show mechanism or localization** — how/where the effect operates.
4. **Quantify** the representative image, qualitative observation, or case study
   shown earlier.
5. **Add robustness, controls, subgroup analysis, or sensitivity checks** —
   visually quieter panels that preempt reviewer questions.

Not every figure needs all five steps. A `quantitative grid` may collapse to
steps 2 + 5. A `schematic-led composite` typically uses 1 + 2 + 5. Drop steps
that do not carry unique evidence.

### Anti-Redundancy Checklist

Before finalizing a journal multi-panel figure, check:

- [ ] Panel (b) does **not** re-display the same data as panel (a) in a different
  visual form
- [ ] Panel (c) adds a dimension absent from (a) and (b)
- [ ] Each panel has its own axis-label vocabulary (different x/y quantities)

| Trap | Example | Fix |
|------|---------|-----|
| Absolute + absolute | Stacked bar (%) + heatmap of same % | Replace heatmap with z-score deviation |
| Subset of parent | Ranked bar is just one column of the stacked bar | Swap for scatter: category A vs category B |
| Two rankings | Two ranked bars on related metrics | Replace one with scatter or bubble |
| Different chart, same data | Pie + stacked bar | Merge, or replace one with a relationship plot |

### Z-Score Deviation (complement to composition)

When panel (a) shows absolute composition, panel (b) should show what is
**atypical** per group:

```python
z = (data - data.mean(axis=0)) / data.std(axis=0)
im = ax.imshow(z.values, cmap='RdBu_r', aspect='auto', vmin=-2.5, vmax=2.5)
cbar.set_label('Z-score vs pan-cohort mean')
```

`RdBu_r`: red = enriched above average, blue = depleted. Orthogonal to the
absolute view in panel (a) — not redundant.

## Aesthetic Integration (Journal)

Conference figures can sometimes read as independent charts pasted together;
journal figures must read as **one integrated argument**.

- **One visual vocabulary**: the schematic panel (a) defines colors, symbols,
  workflow direction, and sample classes. Reuse that vocabulary through every
  subsequent panel.
- **Schematic colors → data-plot colors**: if the schematic colors a module
  blue, the bar chart quantifying that module should use the same blue. A
  schematic-led composite should look like one figure, not a collage.
- **Unequal panel sizes are intentional**: let the hero panel span multiple grid
  cells. Equal-sized panels signal equal evidence weight — which is rarely true.
- **Direct labels over legends**: when line identities, channels, or spatial
  regions are stable across panels, label them directly rather than repeating a
  legend in each axis.
- **One shared legend strip**: for multi-axis figures, place one legend above the
  row (or a dedicated legend panel as the last subplot) rather than repeating it.
- **Keep one neutral family + one signal family + one accent family** per figure.
  See `plot-style.md` Colors for the palette system.

## Reviewer-Risk Checklist (Journal)

Before finalizing a journal figure, ask what a skeptical reviewer would
challenge. Conference rebuttals are single-shot; journal revision is multi-round
— a figure that invites an obvious question will generate a revision request.

- [ ] **Sample size visible** — is n stated in the legend, caption, or source-data
  note for every quantitative panel?
- [ ] **Error bars / intervals defined** — does the caption or methods text say
  whether whiskers are std, sem, CI, or IQR?
- [ ] **Axes comparable across panels** — if two panels invite comparison, are
  their y-axes on the same scale? If not, is the difference explicitly noted?
- [ ] **Representative images quantified** — if panel (c) shows "representative"
  microscopy/histology/screenshots, is there a companion quantification panel
  that turns the qualitative observation into numbers?
- [ ] **Image adjustments documented** — are brightness/contrast adjustments
  global (applied to the whole image) and recorded? Local selective edits are a
  red flag for reviewers.
- [ ] **Could the same conclusion be made from fewer panels?** — every panel must
  carry unique evidence. A panel that confirms what another panel already shows
  invites the reviewer to ask "why is this here?"
- [ ] **Color-only encoding has a fallback** — for ≥4 overlapping series, is
  there a redundant channel (marker, hatch, linestyle) so the figure survives
  grayscale print and colorblind readers?
- [ ] **No invented content** — every label, number, and module in the figure
  traces to the Writing Policy or concrete workspace files. Journal reviewers
  have more time to spot discrepancies than conference reviewers.

## Cross-Reference

- `figure-planning.md` — Display Item Contract, Display Review Gate, failure
  signatures, generation routes, unified visual family, caption rules
- `references/figures/journal/figure-sizing.md` — journal column widths, figsize,
  font sizes, display-item caps, export
- `plot-style.md` — rcParams, colors, per-chart-type rules
- `qa-contract.md` — submission-readiness checklist
- `_shared/venues/journal-vs-conference.md` — overall journal drafting posture
- `academic-review` skill: `references/checks/journal-submission-elements.md` — display-item caps and
  tiers, mandatory statements
