# Data Resource / Data Descriptor Profile

Use this profile for biomedical data descriptors, dataset/resource papers, registry/resource
descriptions, database papers, biobank/resource profiles, and reusable data or software-resource
manuscripts.

## Source Anchors

- Scientific Data submission guidelines: https://www.nature.com/sdata/submission-guidelines
- Scientific Data Data Descriptor archive: https://www.nature.com/sdata/articles?type=data-descriptor
- BMC Research Notes submission guidelines: https://link.springer.com/journal/13104/submission-guidelines

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Data descriptors and data notes use
journal-specific structures and may prohibit ordinary Results/Discussion claims.

## Checklist / Study-Type Pairing

Use data-availability, FAIR, repository, metadata, ethics/consent, and domain checklist rules. If
the manuscript reports new clinical findings from the dataset, use an empirical profile instead.

## Priority Contract

- Primary core: Methods and Data Records / Resource Description.
- Evidence core: Technical validation, reuse value, and access/FAIR metadata.
- Compress first: exploratory analyses, broad background, and claims about scientific findings.
- Core floor: data provenance, collection methods, processing, quality control, file/metadata
  structure, access conditions, usage notes, ethics, and reuse limitations cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / abstract | outside main budget unless target counts it | Identify the dataset/resource, scope, repository/access route, and reuse value. |
| 1 | Background and Summary | 10-14% | Explain the resource purpose, coverage, and intended use. |
| 2 | Methods | 24-34% | Describe collection/generation, participants/samples, instruments, processing, quality control, and ethics. |
| 3 | Data Records / Resource Description | 24-34% | Specify files, variables, metadata, repository identifiers, formats, versions, and access restrictions. |
| 4 | Technical Validation | 18-26% | Demonstrate quality, completeness, reproducibility, validation checks, and known limitations. |
| 5 | Usage Notes / Reuse Conditions | 8-14% | Explain how to access, cite, interpret, and reuse the resource safely. |
| Back | Code/data availability / metadata / supplement | outside main text unless target counts it | Carry data dictionaries, schemas, protocols, checksums, and extended validation. |

## Flexible Adjustment Notes

- Do not add ordinary Results/Discussion sections when the target data-descriptor format forbids
  them.
- If the resource paper also makes clinical effect claims, split or retarget the manuscript.
