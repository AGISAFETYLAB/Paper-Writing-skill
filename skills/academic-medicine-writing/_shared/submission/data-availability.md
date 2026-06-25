# Data Availability And FAIR Audit

Use this reference for data/code availability statements, repository planning, sensitive-data access
routes, dataset citations, source data, and submission package audits.

## Access Route Classification

Use controlled-access wording for restricted human, sensitive, legal, consent, or institutional data
when public release is not possible.

Assign each dataset or code artifact to one route:

| Route | Use when | Required evidence |
|---|---|---|
| `public_repository` | Data/code can be public. | Repository name, DOI/accession/stable URL, version, licence, file list. |
| `controlled_access` | Human, sensitive, legal, consent, or institutional limits apply. | Restriction reason, metadata route, access committee/procedure, eligibility and conditions. |
| `within_paper_or_supplement` | Small source data are fully represented in manuscript/source-data files. | Exact figure/table/source-data file mapping. |
| `reused_public_data` | Public third-party datasets support results. | Source, accession/DOI, version/release/date accessed, dataset citation. |
| `third_party_restricted` | Data are licensed or controlled by another owner. | Provider, licence boundary, reader request route, shareable derived data if any. |
| `request_based_restricted` | No repository is possible but restriction is justified. | Specific reason, institutional contact route, review conditions, public metadata if possible. |
| `not_applicable` | No datasets or code were generated or analysed. | Explicit reason; do not use for empirical studies unless true. |

## FAIR Checklist

| Principle | Practical check |
|---|---|
| Findable | Persistent identifier, searchable repository record, clear title/description/keywords. |
| Accessible | Identifier resolves; access conditions and restrictions are explicit; metadata remain public. |
| Interoperable | Files use community formats where possible; variables, units, and identifiers are defined. |
| Reusable | Licence, provenance, methods, quality-control notes, version, and data dictionary are present. |

## DataCite Metadata

For DOI-style dataset records, check at least:

- Identifier
- Creator
- Title
- Publisher / repository
- Publication year
- Resource type
- Version when files may change
- Licence / rights
- Related identifiers for manuscript, preprint, protocol, code, and reused data

## Dataset README Minimum

Require a README or metadata record that states:

- what the dataset contains and which manuscript conclusions it supports;
- file names, formats, sizes, and related figures/tables;
- variables, units, missing-value codes, and allowed values;
- collection or generation methods and processing provenance;
- software/script versions for derived tables and figures;
- access conditions, licence, embargo, or data-use agreement;
- preferred dataset citation.

## Blocking Rules

Block submission-ready wording when:

- original research has no Data Availability statement;
- data supporting central conclusions have no identifier, source-data file, or stable access route;
- sensitive data are restricted but no access procedure or metadata route is described;
- reused public data are not cited or versioned;
- public data have no licence or README/data dictionary;
- the manuscript says data are in the paper but figure source data or table inputs are absent;
- manuscript statement, repository record, supplementary files, and `paper/submission-package.md`
  disagree.

Do not invent repository DOIs, accession numbers, licences, access committees, embargo dates, or
data-use conditions.
