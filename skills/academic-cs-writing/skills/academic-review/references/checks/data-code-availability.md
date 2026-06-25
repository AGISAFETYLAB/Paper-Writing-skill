# Data/Code Availability Workflow

Use this reference for journal drafts that mention datasets, source data, custom
code, model checkpoints, materials, protocols, or reproducibility artifacts. It is
a planning and readiness workflow, not a place to invent missing identifiers.

## Workflow

1. **Inventory every supporting dataset**: raw data, processed data, figure source
   data, benchmark splits, model outputs, annotation files, trained checkpoints,
   software, scripts, protocols, and third-party datasets.
2. **Classify the Access route** for each item: public repository, controlled
   access, available on request, third-party only, generated at runtime, bundled
   with code, or not shareable.
3. **Choose repository and identifier strategy** before drafting: DOI, accession
   number, archival release, stable URL, or controlled-access request path.
4. **Map artifacts to manuscript locations**: figure/table IDs, Method steps,
   benchmark descriptions, supplementary files, and claims that depend on them.
5. **Draft Data Availability and Code Availability text** only from confirmed
   facts. Do not invent DOIs, accession numbers, repository URLs, or embargo terms.
6. **Add dataset/software citations** when the venue expects formal references.
7. **Run a FAIR-style metadata check**: discoverability, access conditions,
   license/restriction, version, contact, and reuse limits.
8. **Return unresolved items as OPEN_DECISION** or `BLOCKED` if a required
   availability artifact is missing for a claim the manuscript already makes.

## Availability Ledger

| Artifact | Supports | Access route | Identifier/status | Statement text source | Risk |
|---|---|---|---|---|---|
| <dataset/code/source data> | <claim/figure/table/section> | <public/controlled/request/third-party/missing> | <DOI/accession/URL/version/missing> | <source path/user supplied/none> | <PASS/OPEN_DECISION/BLOCKED> |

## Blocking Rules

- A Data Availability statement that says "available" without a repository,
  accession, DOI, URL, or controlled-access process is not submission-ready.
- A Code Availability statement for custom code must point to a repository and,
  when the journal expects archiving, an archival DOI or versioned release.
- Private, embargoed, sensitive, or restricted data require who/why/how access
  wording; vague "upon request" text is an Open Decision unless the venue accepts it.
- Pre-publication or non-resolving accessions are blockers when the venue requires
  valid identifiers before production.
- Do not make reproducibility claims in Abstract, Method, or Results unless the
  availability plan supports them.

## Output

Return ready-to-paste statement text only for confirmed facts. For missing facts,
return the ledger plus exact fields needed from the user or repository owner.
