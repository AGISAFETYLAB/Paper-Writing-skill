# R Chart Catalog For Medical Figures

Use this catalog only after R has been selected by the Backend Language Gate. Each row maps a
medical display need to the normal R route, required source data, and blocking QA checks.

## Catalog Parity Contract

This catalog must stay one-to-one with `references/python-chart-catalog.md`: use the same display
family names and the same row order. If adding, removing, or renaming a display family, update both
catalogs and run `scripts/validate_chart_catalog_parity.py`.

## Core Clinical And Study-Flow Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| clinical outcome rate plot | Event rates or means must be compared across groups. | `ggplot2::geom_col`, `geom_point`, `geom_errorbar`, `geom_line` | group, denominator, event count or estimate, CI/SD/SE, timeframe | Denominator, uncertainty, and direction of benefit must be visible. |
| adverse-event plot | Harms or safety events need readable comparison. | horizontal `ggplot2::geom_col`, dot plot, or faceted bar chart | event name, severity/seriousness, group denominator, event count | Do not hide denominator or severity; long labels must not overlap. |
| forest plot | Effect estimates with confidence intervals support subgroup, sensitivity, or meta-analysis claims. | `forestplot`, `metafor`, or `ggplot2::geom_pointrange` | estimate, lower CI, upper CI, group/stratum, reference line | Reference line and scale must match the effect measure. |
| Kaplan-Meier curve | Time-to-event survival or event-free probability is central. | `survival`, `survminer::ggsurvplot` | time, event indicator, group, censoring, numbers at risk | Include censoring/risk table or document why unavailable. |
| cumulative incidence curve | Competing risk or cumulative event probability is central. | `cmprsk`, `tidycmprsk`, `ggsurvfit` | time, event type, competing event, group | Do not use simple Kaplan-Meier when competing risks change interpretation. |
| case timeline | Case report or clinical course needs event timing. | `ggplot2::geom_segment`, `geom_point`, `ggrepel` | date/day, event label, category, treatment/status | Events must come from source records; do not invent dates. |
| PRISMA flow diagram | Review search and screening flow must be shown. | `PRISMA2020`, `DiagrammeR`, `ggplot2` boxes | records identified, duplicates, screened, excluded, included | Counts must reconcile across stages. |
| CONSORT/cohort flow diagram | Participant flow, exclusion, allocation, or analytic cohort is needed. | `DiagrammeR`, `ggplot2`, `ggforce` | screened, excluded reasons, randomized/exposed groups, analyzed counts | Counts and exclusion reasons must match Methods/Results. |

## Diagnostic, Prediction, And Model Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| ROC curve | Diagnostic or prediction discrimination is reported. | `pROC`, `yardstick`, `ggplot2` | true label, predicted score, group/model, AUC with CI if claimed | Label threshold direction and avoid unsupported AUC claims. |
| precision-recall curve | Positive-class performance, class imbalance, or retrieval-style model behavior is central. | `yardstick`, `precrec`, `PRROC`, `ggplot2` | true label, predicted score, positive-class definition, prevalence, threshold grid | State the positive class and prevalence; do not substitute ROC AUC for PR performance. |
| calibration plot | Predicted risk must be compared with observed risk. | `rms`, `val.prob`, `ggplot2`, `yardstick` | predicted risk, observed outcome, bins or smoother, validation cohort | Distinguish apparent, internal, and external validation. |
| decision curve | Net benefit across thresholds supports model usefulness. | `rmda`, `dcurves`, `ggplot2` | predicted risk, observed outcome, threshold grid, treat-all/treat-none | Do not claim utility when net benefit is absent or unvalidated. |
| confusion matrix | Classifier threshold performance is needed. | `yardstick`, `caret`, `ggplot2` tile/table | true class, predicted class, threshold, counts | Show threshold and class prevalence. |
| risk stratification plot | Risk groups or score bands need outcome comparison. | `ggplot2` bar/dot/line plot | risk group, observed event rate, denominator, predicted risk | Groups must be pre-specified or clearly exploratory. |

## Review And Evidence-Synthesis Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| funnel plot | Publication bias or small-study effects are discussed. | `metafor::funnel`, `meta`, `ggplot2` | study effect, standard error/sample size | Do not overinterpret asymmetry without method caveats. |
| risk-of-bias plot | Review quality or evidence appraisal must be shown. | `robvis`, `ggplot2` | study, domain, judgment, rationale | Domain labels must match the review method. |
| evidence summary plot | Certainty or grade across outcomes is summarized. | `ggplot2`, table-style heatmap | outcome, certainty, effect direction, study count | Must not imply certainty beyond evidence assessment. |

## Observational-Study Diagnostics

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| covariate balance plot | Matching, weighting, or adjusted groups need comparability evidence. | `cobalt::love.plot`, `ggplot2` | covariate, standardized difference before/after, threshold | Show before and after adjustment when applicable. |
| missingness map | Missing data pattern affects analysis credibility. | `naniar`, `VIM`, `ggplot2` | row/variable missingness, group/time if relevant | Missingness coding must distinguish true zero from missing. |
| propensity-score overlap | Propensity score support/positivity must be inspected. | `ggplot2::geom_density`, `MatchIt`, `WeightIt` | score, group, weights/matching status | Flag non-overlap rather than smoothing it away. |
| distribution/paired-change plot | Continuous biomarker or repeated measure must be compared. | box, violin, jitter, paired slope with `ggplot2` | value, group, subject ID when paired, timepoint | Use paired lines only when subject IDs support pairing. |

## Biomarker, Omics, And Mechanism Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| annotated heatmap | Matrix plus sample/feature annotations are central. | `ComplexHeatmap`, `circlize` | matrix, row/column annotations, scaling method | State normalization/scaling; do not cluster unverified data. |
| clinical triptych | A clinical claim needs aligned longitudinal, effect-estimate, and compact summary panels in one figure. | `ggplot2` plus `patchwork` or `cowplot` | repeated-measure table, effect estimates with intervals, binary/percentage summary counts, shared group definitions | Keep columns semantically parallel, center the outer grid, reserve vertical spacing, and avoid outside-crop panel labels. |
| image plate + quantitative companion | Representative imaging, histology, microscopy, spatial overlay, segmentation, or blot-like panels must be quantified. | `ggplot2`, `patchwork`, `magick`, `EBImage` when needed | image paths, crop/scale-bar metadata, channel/overlay labels, quantification table, denominator | Images need scale bars, traceable quantification, reserved image/quant widths, and a visible gutter; no decorative image plates. |
| volcano plot | Differential feature results need effect-vs-significance view. | `EnhancedVolcano`, `ggplot2`, `ggrepel` | feature, log fold change, p/q value | Must show multiple-testing status and label rules. |
| enrichment bubble plot | Pathway or ontology enrichment is summarized. | `clusterProfiler`, `enrichplot`, `ggplot2` | term, ratio, adjusted p value, gene count | Do not treat enrichment as mechanism proof. |
| UpSet plot | Feature/set intersections are important. | `ComplexUpset`, `UpSetR` | set membership by feature/sample | Label set definitions and universe. |

## Global-Health And Economic Displays

| Display family | Use when | R route | Required source data | Blocking QA |
|---|---|---|---|---|
| choropleth map | Burden, rate, or coverage varies by geography. | `sf`, `tmap`, `ggplot2` | geography ID, value/rate, shapefile/source, year | Map denominator and projection/source must be recorded. |
| uncertainty ribbon | Time trend has uncertainty intervals. | `ggplot2::geom_ribbon`, `geom_line` | time, estimate, lower/upper uncertainty, group | Ribbon must match interval definition. |
| ICER plane | Health-economic uncertainty needs cost/effect scatter. | `BCEA`, `heemod`, `ggplot2` | incremental cost, incremental effect, willingness-to-pay threshold | Axes and threshold line must be interpretable. |
| cost-effectiveness acceptability curve | Probability cost-effective varies by threshold. | `BCEA`, `ggplot2` | threshold, probability, strategy | Do not omit threshold units or perspective. |
| tornado plot | One-way sensitivity analysis drives conclusions. | `heemod`, `ggplot2::geom_col` | parameter, low/high result, base case | Sort by impact and label direction. |
| budget impact plot | Costs over time or payer budget must be shown. | `ggplot2::geom_area`, `geom_col`, `geom_line` | time, cost component, scenario, population | Perspective, currency year, and time horizon must be explicit. |
