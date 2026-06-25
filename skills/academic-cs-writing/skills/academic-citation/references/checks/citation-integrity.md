# Citation Integrity Check

Use citations as evidence, not decoration. Keep this check compact: citation work should prevent
false support and bibliography hallucination, not become a full literature-search pipeline.

## Citation Status

| Status | Meaning | Allowed use |
|---|---|---|
| verified | Source content has been checked and supports the point | may cite normally |
| not verified | Source has not been checked | mark as needs verification |
| partially supports | Source supports part of the claim | narrow the claim |
| does not support | Source does not support the claim | remove or replace citation |

## Citation Types

- Background citation: establishes context.
- Comparison citation: identifies prior methods or results.
- Evidence citation: supports a factual statement.
- Limitation citation: supports a claim about prior-work weakness.

## Claim-To-Citation Mini Workflow

For any sentence that needs a citation:

1. Identify the claim role: background, comparison, evidence, or limitation.
2. Match the source to the exact claim; do not cite a related paper for a stronger point than it
   supports.
3. Assign support strength: `verified`, `not verified`, `partially supports`, or `does not support`.
4. Adjust citation wording: state normally, mark unresolved, narrow the claim, or remove/replace.

## Source And BibTeX Rules

- Prefer existing project `.bib` entries and workspace-provided sources.
- Do not add a BibTeX entry from memory.
- Preserve CS proper names, benchmark names, system names, and acronyms in BibTeX `title` fields
  with extra braces, e.g. `{AgentDojo}`, `{OSWorld}`, `{WebArena}`, `{LLM}`, `{API}`, and
  `{MCP}`. If BibTeX renders them as `Agentdojo`, `osworld`, `webarena`, `llm`, or similar,
  the entry is not clean.
- If a source is plausible but metadata or support is incomplete, write
  `% CITATION_NEEDED: <reason>` instead of inventing a citation.
- If lookup is performed, record source, DOI/URL/arXiv ID when available, and verification status.
- Keep `references.bib` limited to entries actually cited in the draft.

## Citation Search Mini Workflow

Use targeted search only for a concrete citation need:

`claim -> query -> search -> verify metadata -> grade support -> insert or mark`

1. Convert the sentence into 1-3 search queries: exact title/name when known, then method/task terms,
   then a broader background query if needed.
2. Prefer structured sources for metadata: DBLP for CS venues, CrossRef for DOI records, arXiv for
   preprints, Semantic Scholar or OpenAlex for discovery and cross-checking.
3. Verify title, authors, year, venue, and DOI/URL/arXiv ID before adding BibTeX.
4. Check abstract, publisher page, or full text before claiming the source supports the sentence.
5. Insert only verified or explicitly marked support. Search failure is not permission to invent.

## Live Search Requirement

When a citation need cannot be satisfied from project sources, run live lookup before inserting a
final citation. Use web/API results as discovery, then verify against a stable source such as DBLP,
CrossRef, arXiv, DOI landing page, publisher page, Semantic Scholar, or OpenAlex. If lookup is
unavailable or inconclusive, leave `% CITATION_NEEDED` and report the gap.

## Citation Evidence Notes

For each citation added or changed through live search, record a compact note in
`paper/citation-evidence.md`:

- Claim: sentence or clause being supported.
- Source: title, first author/year, DOI/URL/arXiv ID, and verification source.
- Support grade: verified, not verified, partially supports, or does not support.
- Evidence basis: abstract, publisher page, full text, or metadata-only candidate.
- Citation wording: final sentence wording or required weakening.

No evidence note means not verified.

## Static Citation Gate

Before calling a draft citation-clean, run a local citation audit and fix every blocking finding:

- Every `\cite*{key}` must resolve to exactly one `references.bib` entry.
- Every `references.bib` entry must be cited in the manuscript.
- Modern sources should carry a stable DOI, URL, or arXiv ID.
- Use full verified author metadata; no `and others`, fake team names, or placeholder titles.
- When BibTeX has generated `paper/*.bbl`, treat it as part of the audit surface: no rendered
  `and N others`, and no modern bibliography item without a visible DOI, URL, or arXiv marker.
- Rendered `.bbl` titles must preserve obvious CS terms and acronyms from `references.bib`; lost
  capitalization means the BibTeX title needs protective braces and BibTeX must be rerun.
- Do not leave `% CITATION_NEEDED` in a final citation-clean draft.

## Source Verification Gate

A citation is verified only when both metadata and claim support have been checked.

- Metadata check: title, authors, year, venue, DOI/URL/arXiv ID match a trusted source.
- Support check: the cited source supports the exact sentence role: background, comparison,
  evidence, or limitation.
- If only metadata is visible, treat it as a metadata-only candidate and keep the sentence
  unresolved or weaken it.
- The draft cannot be called citation-clean if any cited source is `not verified`,
  `partially supports`, or metadata-only candidate without a visible note.

## Rules

- Never fabricate citations.
- Do not say a paper supports a point unless source content has been checked.
- Do not add citations to meet a numeric target; add them only for necessary claims, comparisons,
  definitions, benchmarks, datasets, metrics, or limitations.
- Do not hide weak support inside large citation groups; every grouped citation must share the
  sentence's stated role.
- If a paragraph has no citation but makes external background, history, comparison, or limitation
  claims, cite it, weaken it as paper-internal framing, or remove it.
- If one sentence carries more than five citations, split the claim or keep only representative
  sources.
- If only title/abstract is known, mark citation status as `not verified`.
- If source supports a narrower point, mark `partially supports` and narrow the sentence.
- If source contradicts or does not address the point, mark `does not support`.
