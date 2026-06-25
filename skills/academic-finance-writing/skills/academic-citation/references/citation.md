# Finance Citation And Data-Source Checks

Finance citation work covers papers, methods, datasets, software, data vendors, institutional facts,
and target-journal policy pages. This file is the package-level overview. The runnable workflow lives
in `skills/academic-citation/static/citation-workflow.md`; source choice lives in
`references/search/source-routing.md`; bibliography and claim-context
checks live in `references/checks/citation-integrity.md`.

## Source hierarchy

Prefer primary finance/economics sources:

- DOI or publisher page for journal articles
- SSRN, NBER, CEPR, RePEc, arXiv, or author pages for working-paper identity and version history
- SEC/EDGAR, FRED, WRDS, CRSP, Compustat, Audit Analytics, Refinitiv/LSEG, Bloomberg, exchange,
  central-bank, or vendor documentation for data
- official software documentation or package citation for code dependencies
- official target-journal instructions for submission claims

## Target-venue citation style

When the user specifies a target journal, conference, or platform, use the current official author
instructions as the authority for in-text citation and reference-list format. Author-year natbib is
only the finance/economics default when the target does not specify another style. If the target
requires numbered, footnote, Vancouver, IEEE, ACM, APA, Chicago, or any other explicit style, update
the manuscript commands, bibliography style, and reference order accordingly before calling citation
or format work complete.

Record the target-required citation style, source URL, date checked, and implemented LaTeX/BibTeX or
Word/reference-manager setting in the Paper Framework and `paper/submission-package.md`. If the
required style is unknown or cannot be implemented with available files, mark the format gate
`blocked` or `partial`; do not silently ship a generic author-year bibliography.

## Citation Evidence Ledger

For every central claim and every live-lookup citation change, maintain:

| Claim ID | Claim text / clause | Citation key | Source identity | metadata_source | support_grade | evidence basis | version/data-software status | Action |
|---|---|---|---|---|---|---|---|---|
| C-001 | [claim text] | [key] | DOI/URL/WP ID/vendor page | Crossref/SSRN/NBER/official source/etc. | supported/partial/not verified/unsupported_until_verified | abstract/publisher page/official docs/full text | published/working paper/data docs/software docs/restricted data | insert/weaken/remove/block |

Required statuses: `supported`, `partial`, `not verified`, `unsupported_until_verified`.

## Do not generate BibTeX from memory

Do not invent author lists, titles, years, DOI values, journal issues, SSRN IDs, NBER numbers, data
vendor names, software versions, or URLs. If a source cannot be verified in the current materials,
perform live lookup using `source-routing.md`. If it still cannot be verified, write a placeholder
with `not verified` or `unsupported_until_verified` status and a retrieval plan.

## Working paper vs published version

Check whether a cited working paper has a published version. Prefer the published version unless:

- the working paper contains current methods/results not in the published version
- the manuscript is citing a specific working-paper version
- the source is itself a working-paper series requirement

Do not use working-paper circulation as proof that a result is accepted or established.

Ledger field: working paper vs published version.

## Data and software citation

Data and software citation must cover:

- data source/vendor
- access route and restriction
- sample period and universe
- variable construction or identifier source
- package or software name and version when material to replication

If data cannot be redistributed, cite documentation and state the access boundary rather than
claiming public replication.

Ledger field: data and software citation.

## Claim-strength check

For each high-risk claim, verify:

| Check | Required |
|---|---|
| Reference identity | DOI, working-paper ID, publisher, or official data source |
| Data anchor | sample period, universe, variable definition, transformation |
| Model anchor | regression, factor model, event study, portfolio sort, or backtest specification |
| Robustness | alternative benchmark/window/specification when claimed |
| Claim strength | economic significance and statistical support separated |

If any item fails, mark the claim `unsupported_until_verified` or weaken it.
