# Journal Theory Paper Type

Use this profile for journal papers whose main contribution is a provable result: a formalization,
a theorem/lemma with proof, a convergence/generalization analysis, or a mechanism made rigorous.
Representative shape: JMLR theory articles (e.g., analysis of in-context learning as linear
regression — formalize the setting, prove convergence and generalization, then stress-test under
distribution shift with experiments).

## Profile Boundary

This paper-type profile owns section structure and budget only. Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`; this file contributes the profile-specific section table, priority contract, and budget/floor guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Length: Defer To The Venue Card

This is a journal paper. Do NOT use a conference soft page budget. Take the absolute length from the
venue card (JMLR: no hard limit, concise and complete; TPAMI: manuscript-type page limits). Plan the
sections as proportions of main text first, then fit them to the venue's absolute budget. Long, full
proofs go to the appendix (JMLR) or supplemental material (TPAMI), outside the main argument budget.
Also load `_shared/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Main Results.
- Evidence core: Proof Ideas / Proof Sketches and Empirical Validation when present.
- Compress first: Conclusion, broad Related Work, full derivations, auxiliary lemmas, and secondary experiments.
- Core floor: protect formal setup, theorem statements, interpretation, and proof intuition in main
  text; move full proofs to appendix before shrinking Main Results below its proportional floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State the problem, the formal setting, the main theoretical result in words, and what it implies/limits. |
| 1 | Introduction | ~12-18% | Motivate the phenomenon, state the question precisely, summarize the formal result and its consequences, list contributions. |
| 2 | Related Work | ~8-12% | Position against prior theory and the empirical observations being explained; clarify what is newly proven. |
| 3 | Preliminaries / Problem Setup | ~12-18% | Define notation, the model class, assumptions, the data/task distribution, and the exact objects the theorems are about. |
| 4 | Main Results | ~25-35% | State theorems and lemmas, grouped by topic (e.g., convergence; prediction/generalization; behavior under shift); give precise statements and interpretation. |
| 5 | Proof Ideas / Proof Sketches | ~10-15% | Give the key lemmas and the intuition of each proof; defer full proofs to the appendix. |
| 6 | Empirical Validation | ~8-15% | Validate assumptions and predictions, and probe where the theory's boundary lies (e.g., larger or nonlinear models, stress tests). |
| 7 | Conclusion | ~3-5% | Restate what is proven, the practical utility (JMLR expects this), and open theoretical questions. |
| Back | Appendix: Full Proofs | outside main budget | Complete proofs, auxiliary lemmas, extended derivations, and additional experiments. |

## Flexible Adjustment Notes

- Keep theorem statements in the main text and full proofs in the appendix; the main text carries
  statements + intuition, not page-long derivations.
- Group results so each theorem answers a named sub-question; do not present a flat list of lemmas.
- Make assumptions explicit and discuss when they hold; reviewers attack hidden or unrealistic
  assumptions first.
- JMLR specifically expects theoretical results to discuss practical utility — include it.
- Use the empirical section to mark the boundary of the theory (where it holds, where it breaks),
  not to claim new empirical state of the art.
