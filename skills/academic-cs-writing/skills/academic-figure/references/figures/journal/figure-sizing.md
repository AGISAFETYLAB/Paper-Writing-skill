# Journal Figure Sizing

Load this file for **journal papers** after `plot-style.md`. It contains the
journal-calibrated figure sizes, font size hierarchy, height budget, display-item
caps, and export format additions. All other plotting rules (rcParams, colors,
per-chart-type rules, legend rules, multi-panel architecture) are in `plot-style.md`.

## Column Widths (Journal)

The column width for a journal figure comes from the active venue card and the
journal's template, not from any conference default.

- **JMLR**: single-column, `\textwidth = 6.0 in` → the full text block is the
  maximum available width, not the default for every figure. Use a regular
  `figure` and set `width` as a `\linewidth` fraction from the content-density
  gate below. No `figure*` is needed.
- **TPAMI**: IEEEtran two-column → single-column ≈ 3.5 in, full-page ≈ 7.0 in.
  Use `figure*` with `width=\textwidth` for cross-column figures. Same
  `\columnwidth` / `\textwidth` discipline as ICML/CVPR.
- **journal-generic**: column layout is `not verified` in the venue card. Confirm
  single vs double column from the target journal's template before picking a
  `figsize`. Record the actual `\textwidth` / `\columnwidth` values as a working
  note.

## Figure Sizes

The `figsize` values assume the figure is placed at the column's native width
without shrinking.

| Layout context | Example venues | `figsize` (width, height) | Notes |
|---|---|---|---|
| Single-column journal, low-density/supporting plot | JMLR, journal-generic one-column | `(3.8, 2.2)` to `(4.8, 3.0)` | Include at `0.45--0.70\linewidth`; do not let sparse plots dominate the page |
| Single-column journal, dense/central evidence | JMLR | `(5.5, 3.0)` to `(6.5, 5.0)` | Wider than NeurIPS; use `0.80--1.00\linewidth` only when density or role justifies it |
| Two-column journal, single column | TPAMI, other IEEE/ACM transactions | `(3.5, 2.5)` to `(4.0, 3.5)` | Slightly wider than conference single-column (~3.25 in); adjust per template |
| Two-column journal, cross-column (`figure*`) | TPAMI, other IEEE/ACM transactions | `(7.0, 4.0)` to `(7.5, 6.0)` | Full page width; use only when content genuinely needs the span |
| Square (radar, scatter matrix) | Any | `(5, 5)` to `(6, 6)` | Keep legend inside or directly below the axes |
| Wide multi-panel figure (3+ panels) | Any (full page) | `(14, 10)` to `(24, 18)` | Journals have more room; scale proportionally to panel count |

### LaTeX Inclusion

Apply the Display Width Contract from `figure-planning.md`. Journal layouts may be single-column,
two-column, or full-page; choose `\linewidth`, `\columnwidth`, or `figure*` + `\textwidth` from the
verified template rather than assuming one universal insertion form.

For single-column journals, decide the `\linewidth` fraction by content density:

- `0.45--0.60\linewidth`: pie/donut composition snapshots, simple bars, short horizontal ablations,
  and other supporting low-density plots;
- `0.60--0.78\linewidth`: standard line/scatter/distribution/Pareto plots and moderate grouped bars;
- `0.80--1.00\linewidth`: dense heatmaps, multi-panel evidence, framework/pipeline diagrams, or the
  main quantitative figure when readability depends on width.

If a supporting single-panel chart is wider than `0.70\linewidth`, treat that as a review point:
verify on the compiled page that the extra width improves readability rather than just enlarging a
sparse graphic.

### Height Budget

Journals do not have the extreme page crunch of a conference, so the height
budget is slightly more relaxed. A teaser/pipeline banner can be ~5–7 cm tall
(conference: ~4.5–6 cm). Data figures can use more vertical space for clarity —
a full-page double-column result figure can be ~8–10 cm tall when the content
justifies it. The same anti-empty-band rule applies: the image must fill its
frame without baked-in blank bands.

## Font Sizes

Journals with wider columns or single-column layouts can use slightly larger
base font sizes than conferences:

| Figure type | Base `font.size` | Notes |
|---|---|---|
| Standard single-panel (JMLR single-column 6.0 in) | 10–12 | Wider column; 9 pt is the floor |
| Standard single-panel (TPAMI two-column, single column) | 9–10 | Same as conference two-column |
| Dense multi-panel (journal full-page) | 8–9 | Slightly more room than conference equivalent |
| Hero / teaser (journal full-page) | 11–13 | Wider canvas allows larger text |

Use the shared legibility floor in `plot-style.md`. Journal figures should normally sit above that
floor because wider columns leave room for 9--12 pt base text; dense secondary labels are the only
routine exception.

## Display-Item Caps

Journals may cap the total number of figures and tables combined. See the
`academic-review` skill's `references/checks/journal-submission-elements.md` §2 (Display Items: Caps And
Tiers) and the active venue card. Plan main-paper display items within the cap;
overflow goes to supplementary material per the venue card's supplementary model.

## Export Formats

The standard SVG (primary, editable text) + PDF (LaTeX inclusion) + PNG (raster
preview, ≥300 DPI) triplet from `plot-style.md` remains the default. For journals
that require it (especially life-sciences, imaging, or microscopy venues), add:

```python
fig.savefig('figure.tiff', dpi=600, bbox_inches='tight', pil_kwargs={'compression': 'tiff_lzw'})
```

Confirm the requirement from the venue card or author guidelines; do not generate
TIFF by default for CS journals (JMLR, TPAMI) unless asked.

## QA Notes

- **JMLR (single-column, 6.0 in text block)**: use the full text width only for
  dense or central figures; low-density/supporting figures should be centered at
  a fraction of `\linewidth`. No `figure*` needed. Base font 10–12pt. No hard page
  limit — let evidence set the figure count, but every figure must carry unique
  evidence (anti-redundancy checklist in `references/figures/journal/figure-contract.md`).
  Appendices in the same PDF after acknowledgments.
- **TPAMI (IEEEtran two-column)**: single-column ~3.5 in, cross-column ~7.0 in.
  Hard page limits by manuscript type (Regular 12–18pp, Survey 20pp, Short 8pp)
  — figures count toward the page budget. Move extra figures to separate
  supplemental files. See `_shared/venues/ieee-tpami.md` for current limits.
- **journal-generic**: column layout `not verified` — confirm from the target
  journal template before setting `figsize`. Apply the journal figure composition patterns
  and reviewer-risk checklist from `references/figures/journal/figure-contract.md`.
  Resolve display-item caps and supplementary model from the venue card.

## Cross-Reference

- `plot-style.md` — rcParams, colors, per-chart-type rules, legend rules,
  multi-panel architecture (load first)
- `chart-patterns.md` — reusable Python plotting helpers
- `references/figures/journal/figure-contract.md` — journal figure composition patterns,
  panel logic, aesthetic integration, reviewer-risk checklist
- `figure-planning.md` — Display Item Contract, Display Review Gate, generation
  routes
- `qa-contract.md` — submission-readiness checklist
- `academic-review` skill: `references/checks/journal-submission-elements.md` — display-item caps and tiers
