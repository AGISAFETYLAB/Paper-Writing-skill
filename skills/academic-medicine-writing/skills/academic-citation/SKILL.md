---
name: academic-citation
description: Use when searching, writing, verifying, or auditing citations and bibliography entries for medical, clinical, biomedical, public-health, diagnostic, treatment, systematic-review, reporting-guideline, trial-registration, data-sharing, or ethics-related manuscript claims.
---

# Academic Citation — Medicine

Owns all citation and bibliography work for the standalone medicine package.

Intent class: `citation-only`. Use this route for a bibliography-only request: reference search,
source verification, citation formatting, BibTeX/RIS/NBIB conversion, or citation audit. Do not
create or complete a manuscript package from a citation-only request. For citation-only requests, do not create or complete a manuscript package. If citation repair is one part
of an incomplete manuscript package, return to the medicine hub and use `package-completion` or the
active full-draft stage.

## Protocol

1. Read `manifest.yaml`.
2. Load `references/citation.md`.
3. For live or planned biomedical search, load `references/search-strategy.md`.
4. For central claims, citation drift, or final manuscript audits, load
   `../../_shared/checks/claim-verification.md` and maintain a Claim Registry.
5. For reporting guidelines or statements, also load the relevant checklist and
   `../../_shared/submission/statements.md`.
6. Use verified biomedical sources only.
7. Use Vancouver/AMA-compatible numeric citation style unless the user specifies another target.

Never fabricate citations, DOI values, PMID values, trial identifiers, guideline names, or author
lists. Mark uncertain entries as `not verified` instead of making them look complete.

## Biomedical Source Hierarchy

Prefer sources in this order:

1. Official target-journal author instructions for submission requirements.
2. Official reporting guideline pages/checklists and explanation papers.
3. Trial registries or protocol/SAP records for registration claims.
4. Peer-reviewed biomedical articles for clinical background, comparable studies, and methods.
5. Official dataset/repository records for data availability/accession claims.
6. Software/statistical-method references when the method claim depends on a named tool/model.

Use PubMed/PMC, DOI resolver, journal pages, clinical trial registries, EQUATOR/CONSORT/STROBE/
PRISMA/STARD/TRIPOD sources, ICMJE, and target-journal pages when live lookup is needed.

## Search Strategy And Citation-File Imports

For systematic reviews, guideline-heavy manuscripts, or any search-sensitive claim, follow
`references/search-strategy.md` before writing the citation result into the manuscript:

- record databases, date ranges, exact query strings, MeSH/free-text terms, filters, and search
  date;
- keep PubMed, MeSH, Embase, registry, and repository searches separate unless the method explicitly
  combines them;
- label incomplete mappings, missing database coverage, or unverified translation between MeSH and
  Embase terms as `not verified`;
- when the user provides `.ris`, `.nbib`, or exported citation text, use
  `scripts/convert_citation_file.py` to convert it to auditable BibTeX before editing
  `paper/references.bib`.

Do not treat imported citation metadata as verified just because the file parses. Check DOI, PMID,
PMCID, registry IDs, and source alignment against the manuscript claim before final PASS wording.
If a needed formal citation cannot be directly verified, write an evidence-gap row rather than a
guessed reference.

## Required Fields

For each final source, capture enough information for the target style:

- authors,
- title,
- journal/source,
- year,
- volume/issue/pages or article number when available,
- DOI when available,
- PMID or PMCID when available for biomedical articles,
- URL and access date for official instructions, reporting guidelines, registries, and repositories,
- registry identifier for trial identifiers.

## Citation Audit

For full manuscripts:

- ensure `paper/references.bib` and all in-text citations agree;
- run `scripts/audit_medical_citations.py` for structural metadata/rendered-reference checks when a
  manuscript package has `paper/references.bib`;
- verify no orphaned bibliography entries and no missing cited keys;
- ensure every central clinical claim has a source or a clear manuscript-evidence anchor;
- maintain a Claim Registry with source tracing, evidence tier, alignment status, and action for
  every central clinical claim;
- flag `MAJOR_DISTORTION`, `UNVERIFIABLE`, and citation-drift cases using
  `../../_shared/checks/claim-verification.md`;
- mark unverified DOI/PMID/registry values as `not verified`;
- preserve biomedical acronyms and proper names in BibTeX/rendered reference titles, including
  `STROBE`, `CONSORT`, `PRISMA`, `TRIPOD`, `COVID-19`, `SARS-CoV-2`, `ICD-10`, `NIHSS`, `AUC`, and
  `ROC`;
- check that reporting guideline, ethics/registry, and target-journal instruction citations point to
  official sources rather than secondary summaries.
