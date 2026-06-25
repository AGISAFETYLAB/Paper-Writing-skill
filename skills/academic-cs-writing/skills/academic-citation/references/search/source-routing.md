# Source Tier Routing

Use this reference before live lookup for a citation search or metadata-heavy verification task. It
does not replace `references/checks/citation-integrity.md`; it only decides where to search first and
how to handle fallback.

## Source Tiers

| Tier | Source | Best use | Boundary |
|---|---|---|---|
| T1 | DBLP | CS/ML conference and journal metadata, author lists, BibTeX | Strong for formal venues; weaker for preprint-only work |
| T1 | CrossRef | DOI lookup, publisher metadata, DOI-to-BibTeX checks | Metadata quality follows the DOI registration |
| T1 | arXiv | Preprint identity, arXiv IDs, versioned abstracts | Not a substitute for the published venue record |
| T1 | PubMed | Biomedical and life-science papers | Use for biomedical claims before broad web search |
| T2 | Semantic Scholar | Discovery, abstracts, citation graph, related papers | Good for candidates; verify metadata against T1 when possible |
| T2 | OpenAlex | Broad open metadata graph and cross-checking | Useful second source; normalize venue/title carefully |
| T3 | Google Scholar / general web | Last-resort discovery only | Google Scholar is not the default verification backbone |

## Routing Rules

Choose the source by citation need:

- Known DOI: use CrossRef or the DOI landing page first; cross-check title/authors/year before adding
  BibTeX.
- Known arXiv ID: use arXiv first, then check DBLP/CrossRef/Semantic Scholar/OpenAlex for a
  published version.
- CS/ML venue paper: use DBLP first; use CrossRef or the publisher page for DOI; use Semantic
  Scholar/OpenAlex only as discovery or second-source verification.
- Dataset, benchmark, model, environment, taxonomy, or standard: prefer the official paper, official
  dataset/model page, benchmark page, or standards body page; avoid citing a secondary survey when
  the primary source is available.
- Biomedical or clinical claim: use PubMed first; use CrossRef/publisher pages for DOI and final
  metadata.
- Ambiguous title or author/year mismatch: require at least two trusted sources before writing the
  final entry, or mark `% CITATION_NEEDED`.

## Fallback

1. Search the most specific T1 source.
2. If metadata is incomplete, cross-check another T1 source.
3. If T1 sources cannot discover candidates, use T2 discovery and then verify metadata against T1 or
   a publisher page.
4. Use T3 only as a pointer to a canonical source, and warn that results may be incomplete or stale.
5. If lookup remains inconclusive, leave `% CITATION_NEEDED` and record the gap.

## Metadata-Only Limit

A metadata-only candidate is a paper whose title/abstract/metadata appears relevant but whose content
has not been checked against the claim. Do not cite a metadata-only candidate as verified support.
Either check the abstract, publisher page, or full text, or narrow the sentence and mark the support
grade as `not verified` / `partially supports` in `paper/citation-evidence.md`.
