# Finance Research Workflow Governance

Use this reference when a manuscript task touches datasets, code, output provenance, replication
packages, or data-code statements. The finance writing skill does not run analyses by default, but it
must know what evidence would make a manuscript claim supportable.

## Dataset Profiling Protocol

Before drafting data or results sections from a new dataset, require or reconstruct a dataset
profile:

| Profile field | Required detail |
|---|---|
| Source | vendor, database, official source, or proprietary provider |
| File inventory | raw files, processed files, formats, date received |
| Unit of observation | row meaning and candidate panel key |
| Sample window | date range, frequency, entry/exit, filters |
| Identifiers | PERMNO, GVKEY, CUSIP, LEI, ticker, account, loan, deal, fund, or event ID |
| Variables | outcome, treatment/signal, controls, transformations, winsorization |
| Missingness | missing-by-variable and structural missingness |
| Merge feasibility | linking tables, match rates, duplicates, survivorship risk |
| Data-quality flags | impossible values, stale identifiers, outliers, coding conventions |

If this profile is missing, the Writing Policy must mark the data section as `needs_user_evidence`.

## Research Code Audit

Use a read-only audit before treating code outputs as manuscript evidence:

- data integrity: duplicate checks, merge cardinality, row-count checks, filters, sample selection
- econometric integrity: fixed effects, clustering, identification implementation, bad controls,
  weak instruments, pre-trends, bandwidth or benchmark sensitivity
- reproducibility: relative paths, seeds, package versions, execution order, intermediate outputs
- code quality: hardcoded sample periods, repeated variable definitions, ambiguous names, scripts
  that are too long to audit

Do not execute licensed-data pipelines unless the user explicitly asks outside the writing workflow.

## Script Registry

For an empirical finance project, the manuscript should be able to map every table and figure to
source code. Maintain or request a registry with:

```yaml
registry:
  purpose: "Produce Table 3 main DiD estimates"
  inputs:
    - data/processed/panel.parquet
  outputs:
    - paper/tables/table3_main_results.tex
  paper_target: "Table 3"
  notes: "Clusters by firm; alternative clustering in Table IA.4"
  status: active
  seed: 42
```

The registry is not a decoration. It is the evidence map for data-code statements, review, and
replication planning.

## Code Sweep

Before calling a finance manuscript submission-ready, audit drift between manuscript, code, and
outputs:

- every referenced table/figure exists
- every referenced table/figure has a producing script
- every active script has declared inputs and outputs
- stale outputs are flagged when inputs are newer
- orphan outputs are either archived or explained
- random scripts declare and use seeds
- environment manifests mention required packages
- TODO/FIXME items in code are either resolved or disclosed as blockers

If the sweep is not performed, the review gate must say the data-code status is incomplete.

## Replication Package Map

For journal-submission and serious working-paper versions, plan:

- data availability statement
- raw and processed data inventory
- code execution order
- software versions and operating system
- expected runtime and hardware
- mapping from each manuscript table/figure to code
- restricted-data access process when redistribution is impossible
- license choices for code and public data
- README for replicators

Do not invent repository URLs, data permissions, or code completeness. Mark them as blockers until
the user provides evidence.

