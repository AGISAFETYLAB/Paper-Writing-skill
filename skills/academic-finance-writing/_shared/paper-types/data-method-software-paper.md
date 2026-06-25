# Data / Method / Software Finance Paper Type

Use this profile for finance data descriptors, research data articles, method/protocol articles,
software papers, reusable code resources, and research-object papers that support finance or
financial-economics research.

## Source Anchors

- Elsevier Research Elements describes brief peer-reviewed articles for research outputs including
  data, methods, protocols, software, and hardware:
  https://www.elsevier.com/researcher/author/tools-and-resources/research-data
- Elsevier co-submission guidance describes separate Data in Brief or MethodsX manuscripts for
  research data, methods, or protocols:
  https://www.elsevier.support/publishing/answer/cosubmission-to-data-in-brief-and-methodsx
- MethodsX reviewer guidance focuses on technical steps, reproducibility, and usefulness:
  https://legacyfileshare.elsevier.com/promis_misc/751614reviewer_guidelines.pdf
- Journal of Open Research Software describes software metapapers for reusable research software:
  https://openresearchsoftware.metajnl.com/
- Data Science Journal guidance describes research papers with formally cited supporting data and
  software:
  https://datascience.codata.org/about/submissions

## Profile Boundary

Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`.
This file contributes the profile-specific section table, priority contract, and budget-allocation
guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Section And Budget Reference

Take absolute length from the active venue, template, or version-target card. Allocate the active
budget by section priority; do not create a page limit here.

## Priority Contract

- Primary core: Resource Description and Access / Reproducibility.
- Evidence core: Validation, reuse demonstration, benchmark, or technical evaluation.
- Compress first: broad finance motivation, generic literature review, speculative implications,
  and nonessential implementation narrative.
- Core floor: protect resource identity, availability, licensing/permissions, reproducible steps,
  validation, and intended reuse.

| Order | Candidate section | Budget rule | Section role |
|---|---|---|---|
| Front | Abstract | venue-bound | State the data/method/software object, scope, availability, validation, and reuse value. |
| 1 | Introduction | support/core bridge | Explain the finance research need, resource contribution, intended users, and relation to a regular research article if any. |
| 2 | Resource Overview | primary-core | Define dataset, method, protocol, software, codebase, or research object and its coverage. |
| 3 | Construction / Technical Method | primary-core | Describe collection, processing, algorithm, protocol, architecture, dependencies, or implementation steps. |
| 4 | Access, Licensing, And Reproducibility | primary-core | Record repository, DOI/URL, license, data permissions, installation, environment, and reproducibility instructions. |
| 5 | Validation / Quality Checks | evidence-core | Present data-quality checks, method validation, software tests, benchmark use case, or reproduction evidence. |
| 6 | Reuse Example Or Finance Application | evidence/support | Demonstrate how the resource supports a finance question without overstating causal or investment conclusions. |
| 7 | Limitations And Maintenance | support | State coverage limits, update policy, known failure modes, restricted data boundaries, and maintenance plan. |
| 8 | Conclusion | compress-first | Summarize resource value and proper reuse boundary. |
| Back | Supplement / Repository Materials | venue-bound | Put metadata, schemas, README, code-output map, test logs, and extended examples in the repository or appendix. |

## Flexible Adjustment Notes

- If the main contribution is a substantive empirical finding, use `empirical-research-paper.md` and
  put data/code details in appendices or repository materials.
- For data articles, avoid unsupported interpretation beyond what the data/resource demonstrates.
- For software papers, cite and archive the software; reviewers need access, tests, documentation,
  and reuse evidence.
