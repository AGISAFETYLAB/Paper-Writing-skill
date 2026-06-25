# Journal Survey Paper Type

Use this profile for journal survey/review articles whose main contribution is a taxonomy and
synthesis of a field: motivation, a unified comparison of method families, an application map, and
trends with open questions. Representative shape: TPAMI surveys (e.g., a self-supervised learning
survey organizing generative/contrastive/hybrid families under common dimensions, mapping
applications, and naming key trends and open problems). Journal surveys are long and authoritative.

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Length: Defer To The Venue Card

This is a journal survey and is long by nature. Take absolute length from the venue card (e.g.,
TPAMI survey ~20 double-column pages; JMLR concise but complete). Plan sections as proportions first.
The taxonomy/synthesis is the bulk; do not let the introduction or background dominate. Also load
`_shared/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Taxonomy / Method Families.
- Evidence core: Application Map and Trends, Open Questions, Future Directions.
- Compress first: Conclusion, broad Introduction, duplicated Background, and long paper-by-paper lists.
- Core floor: protect taxonomy, comparison, and trend/open-question synthesis as the majority of main
  prose; if the venue is short, narrow scope before shrinking the taxonomy below its proportional
  floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~2-4% | State scope, the organizing lens/taxonomy, the key trends, and open questions. |
| 1 | Introduction | ~8-12% | Motivate why another survey is needed, the novelty of the organizing perspective, and contributions. |
| 2 | Background / Scope and Method | ~8-12% | Define concepts, the survey scope, and (if systematic) the selection/corpus method and taxonomy-construction method. |
| 3 | Taxonomy / Method Families | ~35-45% | Organize the literature by families along consistent comparison dimensions (motivation, mechanism, assumptions, strengths/limits); compare across families rather than listing papers. |
| 4 | Application Map | ~12-18% | Map where the methods are used across domains/tasks, with what trade-offs. |
| 5 | Trends, Open Questions, Future Directions | ~10-16% | Distill the field's evolution, the cross-cutting limitations, and concrete open problems. |
| 6 | Conclusion | ~2-4% | Restate the organizing framework and its research implications. |
| End | Curated Resources | venue-dependent | Point to a curated, maintained resource list when applicable. |
| Back | Appendix | outside main budget | Full method/paper tables, selection details, and extended comparisons. |

## Flexible Adjustment Notes

- A survey synthesizes; it must expose evolution, commonalities, and shared limitations across
  method families, not stack one-paragraph paper summaries.
- Use consistent comparison dimensions so families are actually comparable (a comparison table is
  usually load-bearing).
- Protect the taxonomy and the trends/open-questions sections; those carry the contribution.
- This is the journal survey profile. A short conference/tutorial survey can instead use the
  top-level `survey-paper.md`.
