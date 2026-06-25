# Finance Source Routing

Use this file before live lookup for finance and economics citation work. These source anchors were
checked on 2026-06-24 (`date_checked: 2026-06-24`). They define where to verify metadata or source
identity; they do not license inventing domain facts without checking the actual source.

## Source Anchors

| Need | First route | Notes |
|---|---|---|
| Journal article metadata and DOI | Crossref REST API, https://www.crossref.org/documentation/retrieve-metadata/rest-api/ | Use for DOI/title/author/year metadata. Confirm finance/economics article context with publisher or journal page when the claim is substantive. |
| Working-paper identity or version | SSRN, https://www.elsevier.support/ssrn/answer/get-started | Use for SSRN paper identity and current version metadata; do not treat posting as peer-reviewed acceptance. |
| NBER working papers | NBER Working Papers, https://www.nber.org/papers | Use for NBER number, title, author, version/download status, and working-paper identity. |
| CEPR discussion papers | CEPR Discussion Papers, https://cepr.org/publications/discussion-papers | Use for CEPR DP identity and version context. |
| Economics/finance bibliography and working-paper discovery | RePEc / IDEAS, https://repec.org/ and https://ideas.repec.org/ | Use to discover economics working papers, articles, software code, and version trails; verify central claims with the source page or full text. |
| Preprints and quantitative finance/econometrics metadata | arXiv API, https://info.arxiv.org/help/api/index.html | Use arXiv ID/version for preprint identity; do not substitute arXiv metadata for journal acceptance. |
| Company filings and regulatory documents | SEC EDGAR, https://www.sec.gov/edgar/search/ | Use official filings for issuer facts, filing dates, forms, and disclosure text. |
| Macroeconomic and public time-series data | FRED API, https://fred.stlouisfed.org/docs/api/fred/ | Use FRED source and series metadata for macro/financial variables; record series IDs and access date. |
| Security returns and market data | CRSP, https://www.crsp.org/research/ | Cite CRSP documentation or official data descriptions; record access route and restriction. |
| Accounting fundamentals and firm financials | Compustat, https://www.marketplace.spglobal.com/en/datasets/compustat-financials-%288%29 | Cite official S&P Global/Compustat documentation; record universe, sample, access, and variable construction. |
| Audit, restatement, disclosure, and accounting datasets | Audit Analytics, https://www.auditanalytics.com/ | Cite official Audit Analytics product or documentation pages; record module and access boundary. |
| Market, macro, reference, estimates, and time-series vendor data | LSEG Datastream, https://www.lseg.com/en/data-analytics/products/datastream-macroeconomic-analysis | Cite official LSEG/Datastream documentation; record feed/API/Workspace route and restrictions. |
| Bloomberg terminal or enterprise data | Bloomberg Data License, https://professional.bloomberg.com/products/data/data-management/data-license/ | Cite Bloomberg product/data documentation and record terminal/data-license access boundary. |
| Data-code and replication policy | AEA Data and Code, https://www.aeaweb.org/journals/data/data-code-policy | Use official journal or AEA-style policy pages for data/code availability statements. |
| Replication-package README structure | Social Science Data Editors, https://social-science-data-editors.github.io/template_README/ | Use for provenance, requirements, instructions, and output-list expectations in replication packages. |
| Software citation metadata | CITATION.cff, https://citation-file-format.github.io/ | Prefer package `CITATION.cff`, Zenodo DOI, or official package citation where available. |
| Software citation principles | FORCE11, https://force11.org/info/software-citation-principles-published-2016/ | Use to justify citing software as research infrastructure; still cite the specific package/version. |

## Routing Rules

1. Start from the source type named by the claim: article, working paper, data vendor, official
   filing, policy page, software, or replication package.
2. Use Crossref for structured article metadata, but confirm high-risk finance claims with the
   publisher/journal page, working paper, official data page, or full text.
3. For working papers, check whether a published version exists before citing the working-paper
   version. Record `working paper`, `published`, or `version conflict` in the Citation Evidence
   Ledger.
4. For data sources, cite the official data owner or vendor documentation when possible. Record
   vendor, dataset/module, access route, sample period, universe, restrictions, and variable source.
5. For software, cite the package's official citation instructions, `CITATION.cff`, DOI, repository
   release, or paper. Record version when it affects replication.
6. For journal policies, use the current official venue page or policy document. Record URL and
   `date_checked`.
7. If a source cannot be verified live and is not in the user's verified materials, mark the row
   `not verified` or `unsupported_until_verified`; do not fill author lists, DOI values, SSRN IDs,
   NBER numbers, series IDs, or vendor facts from memory.
