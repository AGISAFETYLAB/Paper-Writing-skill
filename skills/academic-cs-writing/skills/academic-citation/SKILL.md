---
name: academic-citation
description: Use when searching for, writing, verifying, or auditing citations and the BibTeX bibliography of a research paper — finding sources for named methods/datasets/benchmarks, completing author lists and stable identifiers (DOI/URL/arXiv), checking citation coverage, and running the blocking bibliography audit. Triggers with or without a full draft, including Chinese phrasings like 查引文、补引用、引用核对、参考文献、文献检索、bib 核查、引文审计. Part of the academic-writing collection; the academic-writing hub delegates all citation work here.
---

# Academic Citation — Router

This skill searches, writes, verifies, and audits every **citation and bibliography entry** for a
paper. It is independently invokable ("find sources for this related-work paragraph", "audit my
references.bib") and is the subsystem the **`academic-writing`** hub delegates to whenever a draft
needs citation support.

It is split into two layers:

- A **static layer** at `static/citation-workflow.md` — when to search, the citation/bibliography
  integrity rules, the evidence ledger, the static-audit boundary, and how to run the blocking audit.
- A **dynamic layer** (this file + `manifest.yaml`) plus the deep reference
  `references/search/source-routing.md`, `references/checks/citation-integrity.md`, and the
  mechanical gate `scripts/audit_citations.py`.

Cross-skill stance and integrity rules live in `../../_shared/core/`. Never fabricate a citation —
weaken or mark the claim instead.

## ⚠️ Integrity

**Do not generate BibTeX from memory.** Use verified project sources or live lookup; if reliable
support is not found, weaken/remove the claim or leave `% CITATION_NEEDED: <reason>`. Do not copy the detailed BibTeX rules into this router; they live in `static/citation-workflow.md` and `references/checks/citation-integrity.md`. Mirror the user's interaction language (`../../_shared/core/stance.md`).

## Audit command owner

static/citation-workflow.md owns the concrete `audit_citations.py` commands, citation-floor
arguments, and repeat-until-PASS audit loop. This router only decides when the `audit` workflow
axis is active and which files to load.

## Routing protocol

1. **Load the core layer.** Read `manifest.yaml`, the `always_load` file
   (`../../_shared/core/stance.md`), and `static/citation-workflow.md`.
2. **Select the workflow axis** from `manifest.yaml`:
   - `search` — find support for a concrete claim or missing citation.
   - `verify` — check an existing citation, BibTeX entry, or citation context.
   - `audit` — run the blocking static bibliography audit.
   Combined requests may load more than one workflow value.
3. **Source routing.** For `search` or metadata-heavy `verify`, load
   `references/search/source-routing.md` before lookup so source choice and fallback are explicit.
4. **Claim support.** For search/verify, open `references/checks/citation-integrity.md`, run targeted
   live lookup before writing any final citation, and log added/changed citations to
   `paper/citation-evidence.md`.
5. **Static audit.** For `audit`, follow the command contract in
   `static/citation-workflow.md`; fix every reported `references.bib` or rendered-bibliography
   error until the audit reports `PASS`.

## Why this split

- Citation search and bibliography integrity are a self-contained, frequently standalone task, so
  they live in their own skill with the audit script alongside.
- The hub and the `academic-review` closing gates invoke this skill rather than duplicating its rules.
- The router stays short on purpose; update the workflow, source-routing, integrity reference, or
  audit script rather than expanding this file.
