# Finance Data And Institutional Setting

## Data Readiness Gate

Before drafting, confirm:

- data source, vendor, access boundary, and citation;
- sample period, frequency, universe, filters, and exclusions;
- unit of observation, panel key, and merge keys;
- treatment, signal, outcome, controls, returns, factors, and transformations;
- winsorization, lagging, scaling, event-window, benchmark, and missing-data rules;
- whether restricted data, licenses, confidentiality, or proprietary inputs affect disclosure.

If these are missing, mark the data section as `needs_user_evidence`.

## Section Movement

1. Setting: explain the institutional or market environment only insofar as it makes the design,
   variable, or model meaningful.
2. Data sources: identify source, coverage, timing, and access boundary.
3. Sample construction: show how the analysis sample is built. The sample construction must
   reconcile with code outputs, tables, and figures; sample construction must reconcile before the
   data section is treated as draftable.
4. Variables: define outcomes, treatments, signals, controls, and model inputs with units.
5. Summary evidence: report the distributions or balances that matter for interpretation.
6. Limitations: state coverage gaps, selection concerns, survivorship, reporting changes, or
   measurement error.

## Avoid

- vendor name without coverage and access boundary;
- summary statistics with no interpretation;
- sample filters that cannot be traced to code;
- institutional background that does not affect the design or interpretation.
