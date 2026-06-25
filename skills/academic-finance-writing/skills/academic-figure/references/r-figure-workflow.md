# R Figure Workflow

Use this file when the user chooses R, provides R scripts, or provides an R-centered data workflow
for finance manuscript figures. Keep the finance figure contract: claim first, source data second,
drawing code third.

For chart-family selection after R is chosen, load `references/r-chart-catalog.md`.
For paper-level color consistency, load `references/finance-palette.md` and use one palette profile
for all figures in the manuscript.
For final size and manuscript placement, load `references/figure-layout.md`.

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
| Core plotting and data shaping | `ggplot2`, `dplyr`, `tidyr`, `data.table`, `ggrepel` |
| Regression and econometric output | `fixest`, `broom`, `modelsummary`, `sandwich`, `clubSandwich` |
| DiD, event studies, and causal panels | `fixest`, `did`, `eventstudyr`, `bacondecomp`, `ggplot2` |
| Portfolio, returns, and backtests | `PerformanceAnalytics`, `xts`, `zoo`, `tidyquant`, `ggplot2` |
| Maps, networks, and composite layouts | `sf`, `igraph`, `ggraph`, `ggalluvial`, `patchwork`, `cowplot` |
| Tables | `modelsummary`, `tinytable`, `kableExtra`, `stargazer`, LaTeX `booktabs` |
| Export | `svglite`, `grDevices::cairo_pdf`, `ragg`, `ggsave` |

## Minimal R Export Scaffold

```r
library(ggplot2)

finance_palette_profile <- "finance-muted"

# Mirror academic-finance-writing/scripts/finance_palette.py. If the canonical
# registry changes, update this R scaffold before producing final R figures.
finance_palette_profiles <- list(
  "finance-muted" = c(
    primary = "#4EAB90",
    secondary = "#8EB69C",
    accent = "#D94F33",
    warm = "#EEBF6D",
    support = "#EDDCC3",
    deep = "#834026",
    sand = "#EED5B7",
    mist = "#ECF6FD",
    blush = "#FEEEED",
    neutral_text = "#2F3540",
    neutral_grid = "#D9DCE1",
    neutral_muted = "#6B7280"
  ),
  "finance-soft-contrast" = c(
    primary = "#5E82A2",
    secondary = "#BFC7E5",
    accent = "#D15354",
    warm = "#E8B86C",
    support = "#ABD8E5",
    deep = "#8887CB",
    sand = "#F9AD95",
    mist = "#ECF6FD",
    blush = "#FEEEED",
    neutral_text = "#2F3540",
    neutral_grid = "#D9DCE1",
    neutral_muted = "#6B7280"
  ),
  "finance-warm-deep" = c(
    primary = "#44757A",
    secondary = "#B7B5A0",
    accent = "#D44C3C",
    warm = "#DD6C4C",
    support = "#E5855D",
    deep = "#452A3D",
    sand = "#EED5B7",
    mist = "#F7F1E8",
    blush = "#FCEAE6",
    neutral_text = "#2F3540",
    neutral_grid = "#D9DCE1",
    neutral_muted = "#6B7280"
  )
)

finance_discrete_tokens <- list(
  "finance-muted" = c("primary", "secondary", "warm", "support", "accent", "deep"),
  "finance-soft-contrast" = c("primary", "support", "warm", "secondary", "accent", "deep"),
  "finance-warm-deep" = c("primary", "secondary", "sand", "support", "warm", "accent", "deep")
)

finance_small_n_tokens <- list(
  "finance-muted" = c("primary", "secondary", "warm", "support", "accent"),
  "finance-soft-contrast" = c("primary", "support", "warm", "secondary", "accent"),
  "finance-warm-deep" = c("primary", "secondary", "sand", "support", "warm", "accent")
)

finance_palette <- finance_palette_profiles[[finance_palette_profile]]

finance_categorical_values <- function(n, include_deep = FALSE) {
  stopifnot(n >= 0)
  tokens <- if (include_deep || n > 4) {
    finance_discrete_tokens[[finance_palette_profile]]
  } else {
    finance_small_n_tokens[[finance_palette_profile]]
  }
  values <- unname(finance_palette[tokens])
  if (!include_deep && n <= 4) {
    values <- values[values != finance_palette[["deep"]]]
  }
  rep(values, length.out = n)
}

finance_size_presets_mm <- list(
  inline = c(width = 70, height = 45),
  single_column = c(width = 89, height = 65),
  mid_width = c(width = 130, height = 85),
  double_column = c(width = 178, height = 105),
  appendix_full_width = c(width = 178, height = 120)
)

theme_set(
  theme_classic(base_size = 7, base_family = "Arial") +
    theme(
      text = element_text(colour = finance_palette[["neutral_text"]]),
      axis.line = element_line(linewidth = 0.35, colour = finance_palette[["neutral_text"]]),
      axis.ticks = element_line(linewidth = 0.35, colour = finance_palette[["neutral_text"]]),
      axis.text = element_text(colour = finance_palette[["neutral_text"]]),
      legend.title = element_text(size = 6.5),
      legend.text = element_text(size = 6),
      strip.text = element_text(size = 6.5, face = "bold"),
      panel.grid = element_blank()
    )
)

finance_discrete_scale <- function(...) {
  scale_colour_manual(
    values = finance_categorical_values(6, include_deep = TRUE),
    ...
  )
}

finance_fill_scale <- function(...) {
  scale_fill_manual(
    values = finance_categorical_values(6, include_deep = TRUE),
    ...
  )
}

save_finance_figure_r <- function(plot, filename, width_mm = 170, height_mm = 100, dpi = 600) {
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

Palette usage rules for generated R scripts:

- Keep `finance_palette_profile` fixed across a paper unless a journal or author style override is
  documented.
- Use `finance_categorical_values(n)` for generic grouped bars, lines, and categories. For `n <= 4`,
  this avoids the dark `deep` token by default.
- Use semantic tokens directly when color encodes meaning, such as `finance_palette[["accent"]]`
  for drawdowns, rejection, or risk.
- Use muted sequential or diverging scales that mirror `scripts/finance_palette.py`; do not use
  default rainbow, saturated red/green, or unrelated package palettes.

## Finance Figure QA

Before marking the figure complete, record:

| field | required content |
|---|---|
| source-data-to-panel | Source file/table/model output for every plotted element. |
| palette profile | Paper-level palette profile and semantic color map from `references/finance-palette.md`. |
| small-N color check | For 1-4 categorical colors, confirm `finance_categorical_values(n)` did not use `deep` unless justified. |
| layout contract | Placement width, float environment, final size, panel grid, text anchor, and layout risk from `references/figure-layout.md`. |
| R script | Path to the script used for drawing. |
| export files | SVG/PDF plus PNG preview when possible. |
| visual QA | not blank, not cropped, final-size text legible, no overlapping labels, colors consistent with the paper palette, width matches the layout contract. |
| finance linkage | sample, unit, model, benchmark, economic magnitude, and uncertainty visible in plot, table note, or caption. |
| blocker | Missing source data, missing R runtime/package, or failed preview inspection. |

If source data, R runtime, package dependencies, or visual QA evidence are missing, report the visual
display gate as BLOCKED rather than substituting a Python render or claiming the R figure is done.
