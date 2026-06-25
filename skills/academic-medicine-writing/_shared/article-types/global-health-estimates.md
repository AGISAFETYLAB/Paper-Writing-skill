# Global Health Estimates Profile

Use this profile for studies that generate global, regional, national, or subnational health
estimates across populations, geographies, or time using multiple data sources and statistical
estimation models.

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Protect input data, case definitions,
modeling, uncertainty, validation, and reproducibility information.

## Checklist / Study-Type Pairing

Pair with GATHER. Use STROBE only for a single observational study that does not produce population
health estimates across sources, places, or time.

## Priority Contract

- Primary core: Methods.
- Evidence core: Results with estimates, uncertainty, and validation/sensitivity.
- Compress first: broad background, country-by-country narrative detail, and secondary maps/tables
  that can move to supplement.
- Core floor: data sources, inclusion/exclusion, case definitions, harmonization, modeling,
  uncertainty propagation, validation, data/code availability, and limitations cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / structured abstract | outside main budget unless target counts it | State indicator, populations, time/geography, methods, headline estimate, and uncertainty. |
| 1 | Introduction | 8-12% | Explain the policy/scientific need for updated estimates and the evidence gap. |
| 2 | Methods | 38-46% | Describe input data, case definitions, data processing, model structure, covariates, geographic/time hierarchy, uncertainty, validation, and reproducibility. |
| 3 | Results | 30-38% | Present headline burden/trend estimates, uncertainty intervals, geography/subgroup patterns, validation, and sensitivity analyses. |
| 4 | Discussion | 14-20% | Interpret policy meaning, compare with prior estimates, discuss uncertainty, data limitations, and use constraints. |
| 5 | Conclusions | 1-3% | State the estimate-supported conclusion. |
| Back | Data/code/statements / GATHER checklist / supplement | outside main text unless target counts it | Carry data-source inventory, model appendix, source data, code, and extended tables/maps. |

## Flexible Adjustment Notes

- A data-source inventory and trend or map display are usually load-bearing.
- Do not hide sparse-data or model-dependent uncertainty; it is part of the central evidence.
