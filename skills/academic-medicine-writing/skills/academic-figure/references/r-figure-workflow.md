# R Figure Workflow

Use this file when the user chooses R, provides R scripts, or provides an R-centered data workflow
for medical manuscript figures. Keep the normal medical figure contract: claim first, source data
second, drawing code third.

For chart-family selection after R is chosen, load `references/r-chart-catalog.md`.

## R-only Execution Rule

Contract phrase: R-only execution rule.

When R is selected, all figure drawing, previewing, exporting, and visual QA must be done in R. Do
not call Python, matplotlib, seaborn, plotly, or another non-R plotting backend to create a
temporary preview, fallback export, or layout approximation. If R, `Rscript`, or required packages
are missing, stop before rendering and report the blocker. You may still write the R script and
provide installation commands, but do not cross-render with another language.

Allowed non-R utilities are limited to non-visual work such as shell file inspection, CSV line
counts, archive extraction, or text search. They must not create image/vector outputs or alter visual
layout.

## Common R Packages

| Task | Preferred packages |
|---|---|
| Bar, line, dot, box, violin, rate, and forest-style plots | `ggplot2`, `ggrepel`, `dplyr`, `tidyr` |
| Multi-panel assembly | `patchwork` |
| Annotated heatmaps | `ComplexHeatmap`, `circlize`, `grid` |
| Survival and subgroup displays | `survival`, `survminer`, `forestplot`, `ggplot2` |
| Diagnostic and prediction displays | `pROC`, `yardstick`, `rms`, `rmda`, `dcurves`, `caret` |
| Review and meta-analysis displays | `meta`, `metafor`, `robvis`, `PRISMA2020`, `DiagrammeR` |
| Observational-study diagnostics | `cobalt`, `WeightIt`, `MatchIt`, `naniar`, `VIM` |
| Omics and biomarker displays | `EnhancedVolcano`, `clusterProfiler`, `enrichplot`, `ComplexUpset` |
| Global-health and economic displays | `sf`, `tmap`, `ggplot2`, `BCEA`, `heemod`, `hesim` |
| Export | `svglite`, `grDevices::cairo_pdf`, `ragg` |

## Minimal R Export Scaffold

```r
library(ggplot2)
library(patchwork)

theme_set(
  theme_classic(base_size = 7, base_family = "Arial") +
    theme(
      axis.line = element_line(linewidth = 0.35, colour = "black"),
      axis.ticks = element_line(linewidth = 0.35, colour = "black"),
      legend.title = element_text(size = 6.5),
      legend.text = element_text(size = 6),
      strip.text = element_text(size = 6.5, face = "bold"),
      panel.grid = element_blank()
    )
)

save_medical_figure_r <- function(plot, filename, width_mm = 170, height_mm = 110, dpi = 600) {
  width_in <- width_mm / 25.4
  height_in <- height_mm / 25.4

  svglite::svglite(paste0(filename, ".svg"), width = width_in, height = height_in)
  print(plot)
  dev.off()

  grDevices::cairo_pdf(paste0(filename, ".pdf"), width = width_in, height = height_in,
                       family = "Arial")
  print(plot)
  dev.off()

  ragg::agg_png(paste0(filename, ".png"), width = width_in, height = height_in,
                units = "in", res = dpi)
  print(plot)
  dev.off()
}
```

For `ComplexHeatmap` objects, open the graphics device, call `draw(...)`, and close the device; do
not wrap them as ordinary ggplot objects.

## R Palette Family Contract

Use a restrained visual system, not one literal color list for every chart. Keep the R route aligned
with `scripts/medical_palette.py`: the same `palette_families` and `display_palette_defaults` should
be used when translating package examples to R.

```r
palette_families <- list(
  teal_warm = list(
    group = c("#4EAB90", "#8EB69C", "#EDDCC3", "#EEBF6D", "#D94F33", "#834026"),
    use = "bar charts, flow diagrams, tables, clinical triptychs, image plate + quant"
  ),
  deep_teal_coral = list(
    group = c("#4F8589", "#8A6B7B", "#D44C3C", "#E5855B", "#B7B5A0", "#EDD5B7"),
    use = "bar, stacked-bar, lollipop, waterfall, categorical comparisons"
  ),
  scientific_blue_red = list(
    group = c("#5E82A2", "#D15354", "#E8B86C", "#8887CB", "#5094D5", "#F9AD95"),
    use = "line, longitudinal, diagnostic, prediction, survival, forest, economic curves"
  )
)

display_palette_defaults <- c(
  bar = "teal_warm",
  line = "scientific_blue_red",
  distribution = "scientific_blue_red",
  heatmap = "scientific_blue_red",
  diagnostic = "scientific_blue_red",
  survival = "scientific_blue_red",
  effect_review = "scientific_blue_red",
  flow = "teal_warm",
  biomarker = "deep_teal_coral",
  imaging = "teal_warm",
  economic = "scientific_blue_red",
  table = "teal_warm"
)
```

Use group colors for treatment/cohort/model groups within the selected family. Use sequential scales
for one-direction intensity such as counts, confusion matrices, annotated heatmaps, maps, and
enrichment intensity. Use diverging scales only for signed or midpoint-centered values such as
z-scores, correlations, and change-from-baseline matrices. Use missingness colors only for
observed/missing status. Use risk-bias colors only for ordered quality judgments. Do not mix ad hoc R
palettes such as viridis, Brewer sequential sets, package defaults, or rainbow-like palettes inside
one manuscript unless the style guide requires it.

Do not use near-black colors as categorical fills in bars, area charts, or group markers. Reserve
very dark colors for text, axes, and sparse reference lines.

For image/composite panels, use fixed `viewport`/`patchwork`/`cowplot` slots for internal image
thumbnails, segmentation overlays, dot plots, and quantification bars. Align all companion elements
to shared top, bottom, and baseline coordinates instead of allowing package defaults to resize one
sub-image independently of its neighbors. Quantification bars beside images should use compact
fixed-width marks rather than full-width bar charts.

## Layout-Safe R Patterns

For numeric-heavy clinical tables, render LaTeX as `booktabs` + `tabular*` with controlled
inter-column fill rather than raw equal-width `tabularx` numeric columns. Use `tabularx` only when
the table is text-heavy and the meaning-bearing text column truly needs wrapping.

For clinical triptych figures, assemble the longitudinal, effect-estimate, and summary bands with a
centered outer layout in `patchwork` or `cowplot`, reserve enough vertical spacing between bands, and
anchor panel labels inside or flush with the panel area. Labels placed outside the crop can make the
whole figure appear shifted after export.

For image plate + quantification figures, reserve most width for the representative image plate,
reserve a readable companion width for the quantification panel, and keep a visible gutter between
the two. Keep black backgrounds only inside image cells and anchor panel `a` near the image-plate
left edge.

When an R skill script generates a preview package, write a small layout audit record and run
`scripts/audit_display_layout.py` or an equivalent check before calling the route complete.

## Medical Figure QA

Before marking the figure complete, record:

| field | required content |
|---|---|
| source-data-to-panel | Source file/table for every plotted element. |
| R script | Path to the script used for drawing. |
| export files | SVG/PDF plus PNG preview when possible. |
| visual QA | not blank, not cropped, final-size text legible, no overlapping labels. |
| medical linkage | denominator, timeframe, group labels, uncertainty, and missingness visible in the plot or legend. |
| blocker | Missing source data, missing R runtime/package, or failed preview inspection. |

If source data, R runtime, package dependencies, or visual QA evidence are missing, report the visual
display gate as BLOCKED rather than substituting a Python render or claiming the R figure is done.
