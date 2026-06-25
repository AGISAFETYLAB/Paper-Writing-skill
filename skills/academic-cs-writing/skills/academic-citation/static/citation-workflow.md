# Citation And Bibliography Workflow

Execution rules for searching, writing, and verifying every citation in a paper draft, and for the
blocking bibliography audit. Source selection lives at `references/search/source-routing.md`; claim
support lives at `references/checks/citation-integrity.md`; the mechanical gate is
`scripts/audit_citations.py`.

## Workflow Selection

Use the `workflow` axis from `manifest.yaml`:

- `search`: find verified support for a concrete claim or missing citation. Load
  `references/search/source-routing.md` and `references/checks/citation-integrity.md`.
- `verify`: check existing citation metadata or claim support. Load
  `references/checks/citation-integrity.md`; add `source-routing.md` if live lookup is needed.
- `audit`: run the static bibliography audit. Use `scripts/audit_citations.py`; do not treat its
  `PASS` as proof that every citation supports its surrounding sentence.

## When To Search

Run targeted citation search whenever the draft needs external support not already covered by
workspace evidence or verified `.bib` entries. Do not run an unbounded survey, but do not under-cite
either. Proactive triggers (search rather than waiting for a `% CITATION_NEEDED`):

- Related Work and Introduction background are proactive by default — search for the prior methods,
  benchmarks, datasets, environments, and comparison lines they discuss.
- Every named entity (model, dataset, benchmark, environment, baseline, taxonomy/standard framework)
  needs a `\cite` to its source.
- A confirmed Paper Framework names prior work missing from local sources.
- A necessary sentence would otherwise require `% CITATION_NEEDED`.
- The user explicitly asks to find, add, or verify references.

Citation coverage is paper-type-scaled. Benchmark, survey, and method papers cite broadly; a 10-entry
bibliography for such a paper is a smell. The final audit is run with a paper-type `--min-citations`
floor (see below).

When searching, load `references/search/source-routing.md` first, then
`references/checks/citation-integrity.md`. Run targeted live lookup before writing a final citation.
If reliable support is not found, weaken/remove the claim or leave `% CITATION_NEEDED: <short reason>`
rather than inventing a source. References do not count toward the page limit, so breadth is cheap —
never fabricate to hit a count.

## Citation Evidence Ledger

Every citation added or changed through live lookup must add a compact row to
`paper/citation-evidence.md`. No ledger row means the citation is not verified.
The ledger is a claim-support table, not a source list. `audit_citations.py` checks the header when
`paper/citation-evidence.md` exists and fails three-column tables such as key/source/role because
they do not record support grade or evidence basis.

Use this table:

| Claim ID | Claim text / clause | Citation key | Source | metadata source | support grade | evidence basis | Action |
|---|---|---|---|---|---|---|---|
| C-001 | sentence or clause supported | `key2026` | title, first author/year, DOI/URL/arXiv | DBLP/CrossRef/arXiv/etc. | verified / not verified / partially supports / does not support | abstract / publisher page / full text / metadata-only candidate | insert / weaken / mark `% CITATION_NEEDED` / remove |

Keep one row per distinct claim-citation relationship. If a grouped citation supports a shared
background claim, one row may list multiple keys only when all cited sources share that same role.

## Citation And Bibliography Rules

**Every cited source must be verified, complete, traceable, and clean in the rendered
bibliography.** A draft with placeholder authors, missing identifiers, unverified entries, or a
generated `main.bbl` that prints `and N others`, omits visible DOI-URL-arXiv markers for modern
sources, or lowercases CS proper names/acronyms from titles is not complete. The citation audit
(`scripts/audit_citations.py`) enforces these rules mechanically — it must pass before the draft
leaves the agent's hands.

- Prefer existing workspace `.bib` files when available.
- Do not generate BibTeX from memory. Every entry must come from a trusted source (DBLP,
  CrossRef, Semantic Scholar, arXiv, publisher page) or from the user's verified `.bib`.
- **Complete author lists required.** Every BibTeX entry must list all authors by name.
  Never use `and others`, `et al.`, or similar placeholders in the `author` field. If
  the full author list is unavailable, mark the entry `% [VERIFY]` and do not cite it
  as verified.
- **Stable identifier required** for every entry published after 2000. At minimum: DOI,
  URL, or arXiv `eprint`. Conference papers without at least an arXiv link are not
  verified. An entry labeled `arXiv preprint arXiv:2025` (year substituted for ID) is
  malformed — fix or replace it.
- **Year consistency.** The citation key year (e.g., `smith2024`) must match the `year`
  field. Mismatched keys mean the entry was fabricated or botched — fix or replace.
- **Title preservation required.** Protect CS proper names, benchmark names, system names, and
  acronyms in BibTeX `title` fields with extra braces so BibTeX styles cannot lowercase them
  (`{AgentDojo}`, `{OSWorld}`, `{WebArena}`, `{LLM}`, `{API}`, `{MCP}`). If the rendered `.bbl`
  changes such terms to `Agentdojo`, `osworld`, `webarena`, `llm`, or similar, fix the title
  field and rerun BibTeX.
- If no verified `.bib` entry is available, use `% CITATION_NEEDED: <short reason>`.
- If citation lookup is performed, record the source, DOI/URL, and verification status
  in `paper/citation-evidence.md`.
- Mark unverified citations as `not verified`.
- Use `\citep{}` / `\citet{}` for natbib venues; use numeric `\cite{}` for IEEE templates.
- Keep `paper/references.bib` limited to entries actually cited. Remove uncited entries.
- After BibTeX runs, inspect the generated `paper/*.bbl` through `audit_citations.py`: the rendered
  bibliography must not contain `and N others`, every cited source from 2000 onward must render a
  visible DOI, URL, or arXiv marker, and CS proper names/acronyms in titles must keep their intended
  capitalization. If the `.bib` file has a stable identifier but the `.bbl` omits it, adjust the
  entry fields or template-compatible URL/DOI fields and rerun BibTeX.

**If any entry in `references.bib` or generated `*.bbl` violates these rules, the citation audit will fail.
Fix every error before returning the draft — the audit is a BLOCKING gate, not a
diagnostic.**

## Citation Audit (blocking)

### Static audit boundary

`audit_citations.py` checks local bibliography integrity. It catches unresolved cite keys, uncited
entries, missing fields, placeholder authors, missing stable identifiers, malformed year/key
signals, unresolved `% CITATION_NEEDED` markers, low coverage when `--min-citations` is set, and
rendered `.bbl` defects including lost title capitalization for CS terms. It **does not prove claim support**: a `PASS` means the bibliography is
structurally clean, not that every cited paper supports every surrounding sentence. Claim support is
verified through the search/verify workflow and the Citation Evidence Ledger above.

Run from the paper project directory (the script is path-agnostic; pass the `paper/` directory):

```bash
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper
# with the paper-type citation floor:
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper --min-citations <floor>
```

`<floor>` is a paper-type expectation (benchmark / survey / method papers cite broadly — use ~25–30;
otherwise ~12–15). When the caller passes `--min-citations`, the floor is a hard gate: a draft below
that count is under-cited for the declared paper type and must add verified, actually used sources or
weaken/remove unsupported prior-work claims. When `paper/*.bbl` exists, the same audit also checks the rendered bibliography for
placeholder authors and missing visible identifiers, because those are the defects readers see in
the compiled PDF.

**What `audit_citations.py` checks:** bibliography integrity — placeholder authors, missing required
BibTeX fields, missing DOI/URL/arXiv on modern entries, rendered `and N others` in generated `.bbl`
files, rendered modern items without a visible DOI/URL/arXiv marker, lost title capitalization for
CS proper names/acronyms, vague source labels, year-key mismatch, uncited entries, unresolved
`% CITATION_NEEDED` markers, and (with `--min-citations`) a blocking low-citation-coverage error
when the bibliography is thinner than the paper type expects.

**On failure:** fix every error in `references.bib` and the generated bibliography path (missing
authors, placeholder `and others`, rendered `and N others`, missing DOI/URL/arXiv, missing visible
DOI/URL/arXiv in `.bbl`, lost title capitalization in `.bbl`, year-key mismatch, malformed entries,
uncited entries), rerun BibTeX when needed, then **re-run the audit**. Repeat until `PASS`. Do not
return the draft while any error remains.
