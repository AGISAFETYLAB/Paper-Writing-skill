---
name: academic-citation
description: Use when searching, writing, verifying, or auditing citations and bibliography entries for finance, financial economics, accounting, asset-pricing, corporate-finance, banking, fintech, event-study, theory-model, data, software, or econometrics manuscript claims.
---

# Academic Citation — Finance Router

Owns citation search, verification, and bibliography auditing for the standalone finance package.
It is used directly for citation tasks and by `academic-writing` / `academic-review` whenever a
draft needs finance/economics citation support.

This skill has two layers:

- Core workflow: `static/citation-workflow.md` defines the search/verify/audit split, Citation
  Evidence Ledger, and blocking `audit_citations.py` command.
- Deep checks: `references/search/source-routing.md` chooses official source routes for live lookup;
  `references/checks/citation-integrity.md` owns missing/wrong/orphan/over/under/recency/self-cite
  checks and data/software citation rules.

## Integrity Rule

Do not generate BibTeX from memory. Use verified project sources, user-provided verified materials,
or live lookup. Never invent DOI values, SSRN IDs, NBER numbers, data vendors, database names,
software versions, sample windows, author lists, URLs, or target-venue policies. If reliable support
cannot be verified, mark the claim `unsupported_until_verified`, weaken/remove it, or leave a
specific blocker.

## Routing Protocol

1. Read `manifest.yaml`, `references/citation.md`, and `static/citation-workflow.md`.
2. Select the `workflow` axis:
   - `search`: find support for a concrete finance/economics claim or missing source.
   - `verify`: check an existing citation, BibTeX entry, data/software source, or claim context.
   - `audit`: run the blocking static bibliography audit.
3. For `search` or metadata-heavy `verify`, load `source-routing.md` before lookup. All professional
   content must come from live lookup or user-provided verified materials, not model memory.
4. For citation context and BibTeX cleanup, load `citation-integrity.md`.
5. For replication/data/software citations, also load `../../_shared/checks/data-code.md`.
6. For methods, identification, factor models, event studies, portfolio sorts, or backtest
   citations, also load `../../_shared/checks/identification-strategies.md` and
   `../../_shared/checks/econometrics.md`.
7. For target venue or working-paper venue policy, load `../../_shared/venues/standards/index.md`
   and the target-specific venue card when available.

For full manuscripts, ensure `paper/references.bib`, in-text citations, and
`paper/citation-evidence.md` agree. When the user specifies a target journal, conference, or
platform, verify and implement that target's required in-text citation and reference-list style
before calling citation work complete. Use author-year finance/economics style only when no target is
specified or the target's official instructions allow it. A static audit `PASS` is necessary but does
not prove claim support; claim support requires live lookup plus a Citation Evidence Ledger row.
