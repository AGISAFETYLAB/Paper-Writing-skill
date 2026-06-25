# Finance Citation Integrity Checks

Use this file for citation context, BibTeX entries, bibliography cleanup, and final review.

## Defect Types

| Defect | Finance-specific check | Required action |
|---|---|---|
| missing citation | A substantive claim, data source, method, institutional fact, or policy statement lacks support. | Search live, cite verified support, or weaken/remove the claim. |
| wrong citation | The cited source does not support the clause, uses a different sample, method, market, regulation, or version. | Replace the citation or narrow the sentence to what the source supports. |
| orphaned reference | `references.bib` contains entries that are not cited in the manuscript. | Remove unused entries from the final bibliography. |
| over-citation | A routine sentence carries a broad pile of loosely related citations. | Keep only sources with a clear shared role and log the support role. |
| under-citation | Introduction, literature, methods, data, or policy paragraphs rely on field knowledge without enough verified sources. | Add targeted verified sources; do not pad with irrelevant references. |
| recency | A field, method, dataset, or regulation claim relies only on stale sources when current status matters. | Check current official or recent literature sources and record `date_checked` for policies/data. |
| self-citation | The bibliography leans on author/self/team sources where independent field evidence is expected. | Balance with independent peer-reviewed, working-paper, or official sources. |

## Entry Requirements

- Do not generate BibTeX from memory. Use user-provided verified BibTeX, Crossref, publisher pages,
  official series pages, official data/vendor pages, software citation files, or live lookup.
- Every cited entry needs a stable source locator: DOI, URL, arXiv ID, SSRN page, NBER/CEPR/RePEc
  page, EDGAR filing URL, official vendor/data page, or software/repository DOI/URL.
- Every cited entry needs enough metadata for the selected venue style: author or institutional
  author, year, title, and source/venue or source identity. Do not use `and others`, `et al.`, placeholder
  titles, placeholder years, guessed DOI values, guessed SSRN IDs, guessed NBER numbers, or guessed
  vendor URLs.
- Use author-year / natbib style in finance/economics only when no target venue is specified or the
  selected target format permits it. If a target journal, conference, or platform requires a
  different citation style, implement that required style and record the source.
- Keep `paper/references.bib` limited to entries actually cited.

## Claim-Support Rules

- A citation attached to a sentence must support that sentence, not merely concern the same topic.
- Separate statistical significance, economic significance, robustness, mechanism, and external
  validity claims; they often require different support.
- Do not cite working paper circulation as proof of peer-reviewed acceptance or consensus.
- For working paper vs published status, prefer the published version unless the draft cites a
  specific working-paper version or the working paper contains the relevant current result.
- For data and software citations, cite documentation or citation instructions, not just the vendor
  name in prose. Record access restrictions and version/sample boundaries.
- Abstract citations (`abstract citations`) are normally avoided in finance/economics manuscripts. Use them only for a
  rare direct factual puzzle or source-defining phrase and keep the abstract readable without a
  citation pile.

## Completion Rules

Before returning a full draft or submission-ready package:

1. Resolve every `% CITATION_NEEDED`, `% EVIDENCE_NEEDED`, `not verified`, and
   `unsupported_until_verified` marker that is producible through live lookup.
2. Fill `paper/citation-evidence.md` for every added/changed/accepted live-lookup citation.
3. Run `scripts/audit_citations.py paper --require-ledger` with the applicable `--min-citations`
   floor.
4. Treat static audit `PASS` as bibliography integrity only. The Citation Evidence Ledger is still
   the claim-support record.
