# Finance Citation And Bibliography Workflow

Execution rules for searching, verifying, and auditing citations in finance, accounting,
economics, econometrics, market, data, software, and institutional-fact manuscripts.
Source selection lives at `references/search/source-routing.md`; claim support and
bibliography-integrity checks live at `references/checks/citation-integrity.md`; the mechanical
gate is `scripts/audit_citations.py`.

## Workflow Selection

Use the `workflow` axis from `manifest.yaml`:

- `search`: find verified support for a concrete claim, missing citation, data source, method,
  working paper, policy source, software package, or institutional fact. Load
  `references/search/source-routing.md` and `references/checks/citation-integrity.md`.
- `verify`: check an existing citation, BibTeX entry, citation context, data/software source, or
  working-paper-versus-published status. Load `citation-integrity.md`; add `source-routing.md`
  whenever live lookup is needed.
- `audit`: run the static bibliography audit with `scripts/audit_citations.py`. A `PASS` means the
  local bibliography is structurally clean; it does not prove claim support.

Combined requests may load more than one workflow value. Full-draft and submission-readiness
workflows must complete search/verify before treating citation work as resolved, then run audit.

## When To Search

Run targeted citation search rather than inventing sources whenever a draft makes a substantive
claim not already supported by user-provided verified materials:

- literature positioning, field consensus, null/mixed prior results, or claimed novelty;
- named datasets, vendors, exchanges, filings, registries, data feeds, software, or APIs;
- econometric methods, identification assumptions, factors, benchmarks, event-study design,
  portfolio/backtest conventions, or inference corrections;
- journal, conference, working-paper platform, data-code, disclosure, or replication policy;
- institutional facts from regulators, central banks, exchanges, or vendors;
- any `% CITATION_NEEDED`, `% EVIDENCE_NEEDED`, `not verified`, or placeholder bibliography entry.

Search must be targeted to the claim. Do not do an unbounded survey, but do not leave finance
introductions, related-work paragraphs, methods, data sections, or data-code statements citation
thin. If reliable support is unavailable, weaken/remove the claim or mark
`unsupported_until_verified`; do not create a plausible-looking citation.

## Citation Evidence Ledger

Every citation added, changed, or accepted through live lookup must add a row to
`paper/citation-evidence.md`. No ledger row means the citation-support step was not verified.

Use this table:

| Claim ID | Claim text / clause | Citation key | Source identity | metadata_source | support_grade | evidence basis | version/data-software status | Action |
|---|---|---|---|---|---|---|---|---|
| C-001 | sentence or clause supported | `key2026` | title, first author/year, DOI/URL/WP ID/vendor page | Crossref/SSRN/NBER/CEPR/RePEc/EDGAR/FRED/vendor/etc. | supported / partial / not verified / unsupported_until_verified | abstract / publisher page / official docs / metadata-only candidate / full text | published / working paper / data docs / software docs / restricted data | insert / weaken / remove / mark blocker |

The ledger is a claim-support table, not a source list. One row covers one distinct
claim-citation relationship. Grouped citations are acceptable only when every listed source plays
the same support role for the same clause.

## Citation Audit

### Static audit boundary

`audit_citations.py` checks local bibliography integrity: unresolved cite keys, uncited BibTeX
entries, placeholder authors, missing required fields, missing stable locator fields, unresolved
`% CITATION_NEEDED` or `% EVIDENCE_NEEDED` markers, low citation count when `--min-citations` is
set, and ledger-schema problems when `--require-ledger` is set. It does not prove claim support;
claim support requires live lookup plus Citation Evidence Ledger rows.

Run from a manuscript workspace and pass the `paper/` directory:

```bash
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper --min-citations <floor>
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper --min-citations <floor> --require-ledger
```

Use `--min-citations` as a paper-type and section-scope floor, not as a target to pad. Empirical
full drafts, survey/review papers, and method/data papers usually require broader verified
coverage than short comments or research letters. If the floor fails, add only relevant verified
sources or weaken the unsupported prose.

Use `--require-ledger` before describing a full draft as citation-ready. It is a hard gate for
submission-readiness review because the static audit cannot decide whether sources support the
sentences around them.

On failure, fix every reported BibTeX, citation, marker, ledger, or coverage problem and rerun the
same command until it prints `PASS finance citation audit`.
