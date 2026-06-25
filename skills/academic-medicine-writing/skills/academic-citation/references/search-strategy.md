# Biomedical Literature Search Strategy

Use this reference when building or auditing literature searches for medical manuscripts, systematic
reviews, claim support, citation completion, or reference management.

## Workflow Types

| Workflow | Output |
|---|---|
| `pubmed-mesh-strategy` | Concept table, MeSH/free-text groups, final PubMed query, unverified MeSH warnings. |
| `multi-source-search` | Search plan across PubMed, Embase, Web of Science, Cochrane, CrossRef, publisher pages, and registries as needed. |
| `citation-verification` | Source identity, DOI/PMID/registry check, claim support status, and metadata completeness. |
| `citation-file-mgmt` | Convert or audit `.nbib`, `.ris`, and `.bib` files using `scripts/convert_citation_file.py` when useful. |

## Concept Mapping

For each PICO/PECO/PIT/prediction concept, record:

| concept | controlled vocabulary | free-text synonyms | field tags | mapping status |
|---|---|---|---|---|

Use PubMed/MeSH for biomedical concepts when possible. If a MeSH term is not verified, do not
present it as confirmed. Write:

```text
MeSH mapping for <concept> is unverified; used as free-text pending author/search-specialist check.
```

For systematic review or PRISMA routes, a query with three or more concepts should show the mapping
table before the final combined query unless the user explicitly requests one-shot drafting.

## Query Rules

- Use `OR` within a concept and `AND` across concepts.
- Include both controlled vocabulary and title/abstract free text when recall matters.
- Add study-design filters only when the manuscript question justifies them.
- Do not fabricate result counts or claim that a query was run if it was only drafted.
- Record database, date searched, exact query, filters, and limitations.

## Citation File Conversion

Use `scripts/convert_citation_file.py` for lightweight local conversion or inspection:

```bash
python scripts/convert_citation_file.py input.ris --format ris --output references.bib
python scripts/convert_citation_file.py input.nbib --format nbib --output references.bib
```

The helper is a convenience parser for common RIS/NBIB fields. It does not verify the literature
search, MeSH correctness, journal abbreviations, or source support for claims.

## Verified Citation And Evidence Gaps

Formal manuscript citations must be directly verified through PubMed/PMC, DOI/Crossref metadata, an
official publisher page, a registry record, or an official repository/instruction page. If a searched
source cannot be verified well enough to support a final reference, do not output a guessed citation.
Record the unresolved slot as an evidence gap:

| claim_or_module | sources_searched | candidate_or_query | missing_metadata_or_anchor | required_next_action |
|---|---|---|---|---|

Use evidence-gap rows for missing DOI/PMID/PMCID/registry identity, unresolved source anchors,
unverified MeSH/Embase mappings, and methods or guideline claims whose official source has not been
located.

## Required Search Audit Fields

For manuscript-facing searches, keep a table with:

| purpose | database/source | exact strategy | date searched | limits | records exported | output file | unresolved issue |
|---|---|---|---|---|---|---|---|

For PRISMA submission-ready wording, missing databases, search dates, full search strings, screening
counts, or excluded-study reasons remain blockers.
