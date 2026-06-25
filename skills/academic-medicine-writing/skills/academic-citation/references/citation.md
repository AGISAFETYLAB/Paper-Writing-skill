# Medicine Citation Checks

Use PubMed first for biomedical and clinical claims, then CrossRef or publisher pages for DOI and
final metadata. Clinical trial claims may also require registry records.

## Biomedical Source Hierarchy

1. Official target-journal author instructions for submission requirements.
2. Official reporting guideline pages and explanation papers.
3. Trial registry, protocol, SAP, or repository records for registration/data claims.
4. Peer-reviewed biomedical articles for clinical background and comparable studies.
5. Peer-reviewed methods/statistics references for named analysis methods.
6. Publisher or DOI records for metadata completion.

For each high-risk claim, verify:

| Check | Required |
|---|---|
| Reference identity | DOI, PMID, trial registry ID, or publisher record |
| Source anchor | page, section, table, figure, or short passage |
| Population match | same population and setting |
| Outcome match | same endpoint, metric, timeframe, and comparator |
| Conclusion strength | source limitation preserved |
| Clinical boundary | research/manuscript wording, not patient advice |

If any item fails, mark the claim `unsupported_until_verified` or weaken it.

Never cite a guideline/checklist as evidence for a clinical effect. Reporting guidelines support
reporting completeness, not efficacy, diagnostic accuracy, safety, or policy conclusions.

## Metadata Requirements

For final bibliography entries, prefer complete DOI and PMID/PMCID where available. For official
instructions, registries, reporting guidelines, and repositories, include URL and access date.

Do not invent DOI, PMID, PMCID, registry identifiers, author lists, or issue/page metadata. Mark
uncertain metadata as `not verified`.

## Three-Layer Citation Gate

Treat citation readiness as three separate gates:

| Gate | What it checks | Tool / evidence |
|---|---|---|
| Metadata integrity | Reference exists; title, author/group, year, journal/source, DOI/PMID/PMCID/URL/registry fields are complete and not malformed. | `scripts/audit_medical_citations.py`, PubMed/PMC, DOI resolver, registry, publisher page |
| Style and rendered-reference integrity | Vancouver/AMA numbering, author shortening, visible identifiers, and biomedical acronym/proper-name preservation in rendered references. | `scripts/audit_medical_citations.py`; for JAMA/JAMA-family word-first routes also `scripts/audit_ama_citations.py` |
| Claim support | The cited source contains the exact claim anchor and matches population, outcome, metric/timeframe, method, and conclusion strength. | Claim Registry from `_shared/checks/claim-verification.md` |

Passing a metadata or style gate is not proof that a clinical claim is supported. A final PASS or
submission-ready verdict also requires the claim-support gate for central claims.

## Verified Citation And Evidence-Gap Rule

A source may be promoted to a formal final citation only when its identity is directly verified from
PubMed/PMC, DOI/Crossref metadata, an official journal/publisher page, a registry record, or an
official repository/instruction page. If a needed source cannot be verified, do not fill the slot
with a guessed citation. Record an evidence gap instead: claim/module, sources searched, missing
metadata or anchor, and the required next action.

## Biomedical Title Preservation

AMA/Vancouver article titles may use sentence case, but biomedical acronyms and proper names must not
be lowercased by BibTeX or rendered references. Preserve terms such as `{STROBE}`, `{CONSORT}`,
`{PRISMA}`, `{TRIPOD}`, `{STARD}`, `{SPIRIT}`, `{COVID-19}`, `{SARS-CoV-2}`, `{ICD-10}`, `{NIHSS}`,
`{AUC}`, and `{ROC}` in BibTeX titles when a renderer might lowercase them. If a `.bbl` or rendered
reference changes them to `strobe`, `covid-19`, `sars-cov-2`, or similar, fix the title field and
rerun the bibliography build.

## Structural Medical Citation Audit

Run the medical structural audit on final or reviewable manuscript packages that contain
`paper/references.bib`:

```bash
python scripts/audit_medical_citations.py paper
```

The audit checks local bibliography integrity: missing/uncited citation keys in LaTeX routes,
placeholder authors, malformed DOI/PMID/PMCID fields, missing stable identifiers for modern medical
entries, rendered `.bbl` placeholder authors, rendered references without visible identifiers, lost
biomedical acronym/proper-name capitalization, and the required medical citation evidence schema when
`paper/citation-evidence.md` or `paper/claim-registry.md` exists. It does not prove claim support;
claim support still requires source tracing through the Claim Registry.

## AMA/JAMA Numeric Style Gate

For JAMA/JAMA-family word-first manuscripts, run `scripts/format_ama_manuscript.py` before rendering
and `scripts/audit_ama_citations.py` after normalization. The manuscript source must use AMA
superscript numeric citations, not square-bracket citations, and reference numbers must follow
first-citation order. Number references in the order cited in the text; do not alphabetize.

For the reference list, follow AMA-compatible journal formatting: abbreviate journal names when
verified, include year, volume, issue, page range or article number, and DOI when available. List all
authors/editors up to 6; if there are more than 6, list the first 3 followed by et al. Official
instructions, reporting guidelines, registries, repositories, and committee documents should include
URL and access date rather than fabricated PMID/DOI values.
