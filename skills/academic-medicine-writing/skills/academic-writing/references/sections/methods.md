# Methods

## Required Inputs By Study Type

Methods is the highest-risk section for checklist failure. Before drafting, collect the required
inputs for the selected study type.

| Study type | Required inputs |
|---|---|
| randomized trial | design, setting, dates, participants, randomization, allocation concealment, blinding, interventions, outcomes, sample size, analysis population, harms |
| protocol | planned design, eligibility, interventions, outcomes, sample size, recruitment, monitoring, ethics, registration |
| observational study | design, setting/dates, eligibility, data sources, exposure, outcome, covariates/confounders, bias handling, missing data, statistical model |
| systematic review | protocol/registration, databases, search dates, eligibility, screening, extraction, risk of bias, synthesis model, certainty assessment |
| diagnostic accuracy | participants, index test, reference standard, blinding, thresholds, indeterminate results, accuracy metrics |
| prediction model | source population, predictors, outcome horizon, missing data, development, internal/external validation, calibration, discrimination |
| case report | patient information, timeline, diagnostic assessment, intervention, follow-up, patient perspective and consent when available |
| health economics | perspective, time horizon, costing source, effectiveness source, model, discounting, uncertainty and sensitivity analysis |
| global health estimates | data sources, inclusion criteria, adjustment model, uncertainty propagation, validation, limitations of source coverage |

## Section Order

Use target journal and article-type order when available. Generic order:

1. study design and oversight,
2. setting, data sources, dates, and participants,
3. intervention, exposure, index test, predictor, or comparison,
4. outcomes and definitions,
5. covariates, confounders, and bias control,
6. sample size or power when applicable,
7. statistical analysis,
8. ethics, consent, registration, data/code availability pointers when journal style keeps them in
   Methods.

## Methods-Results Anchor Rule

Every variable, endpoint, subgroup, sensitivity analysis, table, and figure in Results must have a
Methods anchor. If Results contains a metric not defined in Methods, revise Methods or remove the
unsupported result.

## Statistical Analysis

Report the model family, effect measure, uncertainty interval, multiplicity handling if applicable,
missing-data approach, subgroup/sensitivity status, software and version when provided, and the
analysis population. Do not add software, tests, or adjustment variables absent from source
material.

## Translational / Laboratory / Omics Inputs

For translational, laboratory, wet-lab, preclinical, biomarker, imaging, pathology, genomics,
transcriptomics, proteomics, metabolomics, microbiome, or other omics studies, collect these inputs
before drafting Methods:

- specimen, cell line, animal model, tissue source, cohort linkage, inclusion/exclusion logic, and
  collection/storage conditions;
- assay, platform, instrument, kit/reagent, sequencing or imaging protocol, reference genome or
  annotation version, and laboratory site;
- sample allocation, randomization, blinding, batch structure, plate/lane/run effects, and whether
  case/control or exposure groups were balanced across batches;
- quality-control thresholds, excluded samples/features, contamination checks, read depth/coverage,
  missingness, replicate handling, and outlier rules;
- normalization, transformation, feature selection, multiple-testing control, pathway/gene-set
  method, and statistical model;
- positive/negative controls, technical replicates, biological replicates, validation cohort,
  orthogonal assay, or external dataset status;
- repository/accession numbers, code or pipeline availability, versioned workflow, and data-sharing
  limits when provided.

Do not claim clinical utility, diagnostic readiness, therapeutic effect, or mechanism proof from an
exploratory laboratory or omics signal alone. Link every biological endpoint to the confirmed
sample/source, assay platform, QC rule, and validation status.

## Reporting Checklist Alignment

Draft Methods against the selected item-level checklist. Each Methods paragraph should satisfy one
or more concrete checklist items. Do not mark a checklist item satisfied unless the required source
evidence exists or the item is explicitly not applicable.

## Common Failures

- Results report outcomes or subgroups not defined in Methods.
- Observational Methods omit confounding, missingness, or bias handling.
- Diagnostic Methods omit reference standard, blinding, threshold, or indeterminate results.
- Prediction-model Methods omit calibration or validation status.
- Review Methods omit search date, screening/extraction process, or risk-of-bias method.
