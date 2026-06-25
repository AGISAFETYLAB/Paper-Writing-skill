# Guideline / Consensus / Position Statement Profile

Use this profile for clinical practice guidelines, consensus statements, Delphi consensus reports,
expert recommendations, position statements, and society guidance manuscripts.

## Source Anchors

- RIGHT Statement on EQUATOR: https://www.equator-network.org/reporting-guidelines/right-statement/
- AGREE Reporting Checklist on EQUATOR: https://www.equator-network.org/reporting-guidelines/the-agree-reporting-checklist-a-tool-to-improve-reporting-of-clinical-practice-guidelines/
- ACCORD consensus reporting guideline on EQUATOR: https://www.equator-network.org/reporting-guidelines/accord-accurate-consensus-reporting-document-a-reporting-guideline-for-consensus-methods-in-biomedicine/
- CREDES Delphi guidance on EQUATOR: https://www.equator-network.org/reporting-guidelines/credes/

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Society statements and guideline
journals often impose custom formats; use the named journal or organization instructions when given.

## Checklist / Study-Type Pairing

Use RIGHT or AGREE for clinical practice guidelines, ACCORD for consensus methods, and CREDES for
Delphi studies when applicable. A position statement without formal consensus must not claim
consensus-method compliance.

## Priority Contract

- Primary core: Evidence-to-recommendation or consensus methods.
- Evidence core: Recommendations/positions with evidence strength and rationale.
- Compress first: generic background, exhaustive evidence tables, and implementation detail that can
  move to supplement.
- Core floor: scope, target population, panel composition, evidence methods, consensus/voting
  methods, recommendation strength, conflicts management, and update plan cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / abstract / executive summary | outside main budget unless target counts it | State scope, audience, method, headline recommendations, and evidence basis. |
| 1 | Background / Scope | 10-14% | Define clinical problem, intended users, target population, and why guidance is needed. |
| 2 | Methods | 26-36% | Describe panel selection, evidence review, rating framework, consensus/Delphi process, conflicts management, and external review. |
| 3 | Recommendations / Consensus Statements | 32-42% | Present recommendations or statements with rationale, evidence strength, and implementation notes. |
| 4 | Implementation / Equity / Monitoring | 8-14% | Address applicability, resource implications, equity, audit criteria, and update plans. |
| 5 | Discussion / Limitations | 10-16% | Explain uncertainty, disagreement, evidence gaps, and maintenance needs. |
| Back | Evidence tables / checklist / supplement | outside main text unless target counts it | Carry evidence profiles, voting results, conflicts, and full appendices. |

## Flexible Adjustment Notes

- Do not call a manuscript a guideline unless evidence review and recommendation-development
  methods support that label.
- For an opinion-only position paper, use `review-perspective.md` or this profile with
  `consensus method: not used`.
