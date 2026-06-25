# Conference Figure Sizing

Load this file for **conference papers** after `plot-style.md`. It contains the
conference-calibrated figure sizes, font size hierarchy, LaTeX inclusion rules,
and height budget. All other plotting rules (rcParams, colors, per-chart-type
rules, legend rules, multi-panel architecture) are in `plot-style.md`.

## Figure Sizes

Match figure width to the target venue's column layout. "Single-column" means
different things in different venues: ~3.0–3.4 in for a two-column conference
(ICML, ACL, CVPR), but ~5.5 in for a one-column venue (NeurIPS, ICLR). Always
check the selected template's actual column width before picking a `figsize`.
The values below assume standard US Letter CS venues; A4 venues (ACL) are
slightly narrower — reduce the width by ~0.2 in.

| Layout context | Example venues | `figsize` (width, height) | Notes |
|---|---|---|---|
| Two-column venue, single column | ICML, CVPR, AAAI, IJCAI, ACL | `(3.25, 2.2)` to `(3.5, 2.8)` | Narrow; ≤4–5 bars side by side; use `\columnwidth` |
| One-column venue, full text width | NeurIPS, ICLR | `(5.5, 3.0)` to `(6.0, 4.5)` | Wider column; can fit more bars or a wider heatmap; use `\textwidth` or `\linewidth` |
| Two-column venue, cross-column (`figure*`) | ICML, CVPR, AAAI (full page) | `(6.5, 3.5)` to `(7, 5)` | Wide enough for grouped bars, heatmaps, radar; use `\textwidth` |
| Square (radar, scatter matrix) | Any | `(5, 5)` to `(6, 6)` | Keep legend inside or directly below the axes |
| Wide multi-panel figure (3+ panels) | Any (full page or cross-column) | `(12, 8)` to `(22, 17)` | Scale proportionally to panel count; see `chart-patterns.md` |

### LaTeX Inclusion

Apply the Display Width Contract from `figure-planning.md`. Conference templates usually insert
single-column figures with `width=\columnwidth` / `width=\linewidth`; reserve
`figure*` + a `\textwidth` fraction for the cross-column cases in the matrix below. Cross-column
placement gives the figure more room, but moderate single-panel charts should still be centered at a
sub-full width instead of being stretched.

### Column-Span Quick Rule (see `figure-planning.md` for the full decision)

In a two-column venue, decide span by role and width need, not figure number:

- **Single-column** (`figure` + `\columnwidth`): the teaser / first concept figure that fits ~3 in, a
  single small plot, a narrow taxonomy/setup table.
- **Cross-column** (`figure*` + `\textwidth`, top/bottom of page): pipeline / framework / architecture
  / system-overview diagrams; multi-panel figures (e.g. two radars side by side); wide grouped-bar /
  heatmap / radar comparisons or wide result tables that go illegible at column width. A small
  single-panel radar or 4x6 heatmap should be tried as a normal one-column `figure` before promotion.

A pipeline/framework diagram squeezed into one narrow column is the most common span mistake — give it
`figure*`. Two related comparison charts go in one `figure*` multi-panel with a shared legend, not two
single-column floats. In one-column venues (NeurIPS, ICLR) there is no `figure*`; size by fraction of
`\linewidth` instead.

### Span Decision Matrix

Use this as the deterministic insertion rule after the Figure Plan has recorded the chart family,
panel count, and evidence role.

| Venue/template mode | Figure role / width need | LaTeX insertion | Plot/export target |
|---|---|---|---|
| ACL / EMNLP two-column | compact single-message plot, <=1 panel, <=5 short labels, no shared legend needed | `figure` + `width=\columnwidth` | ~3.0--3.3 in wide; base font 9--10 pt |
| ACL / EMNLP two-column | moderate single-panel radar/heatmap with short labels and readable text | `figure` + `width=\columnwidth` | keep native column-size export; promote only after rendered QA fails |
| ACL / EMNLP two-column | grouped comparison, dense heatmap, dense radar, Pareto/scatter pair, distribution family, pipeline/framework, or >=2 panels that need a shared legend | `figure*` + `width=0.90--1.00\textwidth` | ~6.4--6.8 in wide; base font 9--11 pt |
| Other two-column conference | same compact criteria as above | `figure` + `width=\columnwidth` | ~3.25--3.5 in wide; check final rendered text >=7 pt |
| Other two-column conference | moderate single-panel radar/heatmap with short labels and readable text | `figure` + `width=\columnwidth` | native column-size export; do not use `figure*` just because the chart is polar or matrix-shaped |
| Other two-column conference | wide comparison, dense result matrix, architecture, or multi-panel evidence | `figure*` + `width=0.90--1.00\textwidth` | ~6.5--7.0 in wide; keep height below half a page when possible |
| One-column template | low-density plot, compact story/teaser, secondary plot, or small qualitative example | `figure` + `width=0.45--0.70\linewidth` | no `figure*`; center the image |
| One-column template | pipeline/framework, multi-panel comparison, dense heatmap/table-like plot, or load-bearing result figure | `figure` + `width=0.90--1.00\linewidth` | no `figure*`; use the full line when legibility depends on width |

Overall, a one-column template always uses `figure` + `width=0.45--1.00\linewidth`; choose the
smaller or larger end of the range from content density, role, and legibility.

For two-column `figure*` plots, use sub-full width for moderate density:

- `width=0.65--0.78\textwidth` for a single radar chart, a small heatmap, or a grouped comparison that
  only needs to escape a narrow column;
- For body compact mode with two radar panels, use `width=0.78--0.86\textwidth` and do not fill the
  full `\textwidth` by default; promote wider only after rendered inspection shows labels or legend
  fail at the compact width.
- `width=0.80--0.90\textwidth` for wider labels, longer legends, or dense annotations;
- `width=0.90--1.00\textwidth` for dense multi-panel figures, framework/pipeline diagrams, or the
  main result figure.

If the proposed insertion would require text below 7 pt, rotated labels beyond ~30 degrees, or a
legend that consumes more than one-third of the plot area, promote the figure to the next wider
layout or split the evidence into a table/appendix figure.

### Appendix Figure Sizing

Appendix figures use the same rendered QA as body figures. Do not treat the appendix as a place to
dump oversized plots. In a two-column conference appendix:

- compact inventories, protocol visuals, and secondary single plots stay `figure` +
  `width=\columnwidth` when readable;
- an appendix single-panel heatmap or small result matrix should first be tested at column width; if
  it needs to escape the column, use `figure*` with `width=0.60--0.70\textwidth` or at most
  `0.65--0.78\textwidth` for moderate density;
- reserve `0.90--1.00\textwidth` for dense multi-panel appendix figures, wide full-result matrices,
  or displays whose labels/cell text are unreadable otherwise;
- inspect the rendered appendix page. A float-only or half-empty page created by sparse full-width
  appendix figures is a layout defect, not an acceptable side effect of moving material after the
  references.

### Single-column paper quick rule

For one-column conference templates and single-column journal drafts, `figure*` is unavailable and
should not appear in generated LaTeX. Use a regular `figure` and choose width by role:

- `0.45--0.65\linewidth` for a low-density single plot such as a small bar, simple horizontal
  ablation, pie/donut composition snapshot, or simple secondary scatter;
- `0.55--0.75\linewidth` for a compact story/teaser figure, medium-density secondary plot, or small example
  panel;
- `0.90--1.00\linewidth` for a pipeline, framework, architecture, multi-panel comparison, or dense
  result figure;
- combine paired analyses into one multi-panel figure with one shared legend instead of stacking
  several small floats.

### Height Budget

At `\textwidth` a 16:9 image is ~9–10 cm tall — too tall for a teaser or
picture-style banner. For picture banners target aspect ~3:1 to 4:1
(~4.5–6 cm tall at double-column width); see `picture-generation.md` for height
and trim mechanics. For deterministic framework/pipeline schematics, size the
canvas from node count and reading path; see `schematic-design.md`. For data
figures, a useful starting ratio is width ≈ 1.5–2× height for comparison plots,
1:1 for radar/scatter, and width ≈ 3–4× height for bar panels with many
categories.

## Font Size Hierarchy

Choose the base `font.size` according to figure type, panel count, and the
venue's column width. Start from the table below; adjust per-figure for
readability at the target column width. The values assume the figure is placed
at the column's native width (`\columnwidth` or `\linewidth`) without shrinking.

| Figure type | Base `font.size` | Axis label | Tick label | In-bar / cell annotation |
|---|---|---|---|---|
| Dense multi-panel (3+ panels, two-column venue single-column) | 7–8 | 8 | 7 | 7–8 |
| Standard single-panel (bar, line, scatter — two-column venue) | 9–10 | 9–10 | 8–9 | 8–9 |
| Standard single-panel (bar, line, scatter — one-column venue: NeurIPS, ICLR) | 10–12 | 10–12 | 9–10 | 9–10 |
| Hero / teaser figure (full page width, single-column venue or `figure*`) | 11–12 | 11–12 | 10 | 10–11 |
| Heatmap with cell text | 8–9 | 9 | 8 | 7–8 (contrast-adaptive) |
| Radar / polar (6+ spokes) | 9 | 9 | 8 | — |

### Venue Adaptation

Two-column venues (ICML, CVPR, AAAI, ACL, IJCAI) have narrow single columns
(~3.0–3.4 in) — start from the "two-column venue" rows above. One-column venues
(NeurIPS, ICLR) have a ~5.5 in text block — use the "one-column venue" row;
9 pt base is the floor, 10–12 pt is typical and reads more comfortably. When a
figure is placed in `figure*` spanning both columns of a two-column venue, use
the "hero / teaser" font row.

Use the shared legibility floor in `plot-style.md`. For conference figures, treat any non-secondary
label under 7 pt at final insertion size as a blocking readability defect.

## QA Notes

- **NeurIPS / ICLR (single-column)**: figures fill the 5.5 in text block; base
  font 10–12pt. No `figure*` needed. Use `width=\textwidth`.
- **ICML / CVPR / AAAI / IJCAI (two-column)**: single-column figures ~3.25 in
  wide; use `figure*` only for genuine full-page figures. Most data figures stay
  in one column.
- **ACL (two-column, A4)**: single-column ~3.0 in wide (narrower than US Letter
  venues); reduce figsize width ~0.2 in and check wrapping.
- **IEEE (two-column, US Letter)**: similar to ICML/CVPR; journal mode may be
  single-column.

## Cross-Reference

- `plot-style.md` — rcParams, colors, per-chart-type rules, legend rules,
  multi-panel architecture (load first)
- `chart-patterns.md` — reusable Python plotting helpers
- `schematic-design.md` — deterministic framework, pipeline, architecture, workflow, and taxonomy diagrams
- `picture-generation.md` — AI-generated picture workflow
- `figure-planning.md` — Display Item Contract, Display Review Gate, generation
  routes
- `qa-contract.md` — submission-readiness checklist
