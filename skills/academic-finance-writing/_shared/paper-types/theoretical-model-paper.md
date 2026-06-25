# Theoretical Finance Model Paper Type

Use this profile for finance papers whose main contribution is a theoretical model, formal
mechanism, analytical result, equilibrium characterization, proposition, proof, or comparative
static.

## Source Anchors

- Journal of Financial Economics is described as covering theoretical and empirical topics in
  financial economics: https://shop.elsevier.com/subjects/journals/social-sciences-and-humanities/economics-and-finance/financial-economics
- CRIBFB finance/accounting guidelines define a Theoretical Paper and give a structure with
  Introduction, Theoretical Basis, Results, Discussions, and Conclusions:
  https://www.cribfb.com/journal/index.php/ijafr/AuthorGuide
- Journal of Economics and Finance guidance notes that derivations of complex mathematical results
  should be provided:
  https://link.springer.com/journal/12197/submission-guidelines

## Profile Boundary

Apply the shared hard-default and deviation rules in `_shared/paper-types/profile-boundary.md`.
This file contributes the profile-specific section table, priority contract, and budget-allocation
guidance.

## Section Structure (Paper Framework hard default)

Use the section table in this profile as the Paper Framework hard-default structure.

## Section And Budget Reference

Take absolute length from the active venue, template, or version-target card. Allocate the active
budget by section priority; do not create a page limit here.

## Priority Contract

- Primary core: Model Environment and Results / Propositions.
- Evidence core: Proof Logic / Comparative Statics and empirical or policy implications when used.
- Compress first: broad motivation, long literature review, full derivations, auxiliary lemmas, and
  secondary extensions that can move to an appendix.
- Core floor: keep assumptions, equilibrium/result statements, intuition, and proof map in the main
  paper; move full derivations before shrinking the formal core.

| Order | Candidate section | Budget rule | Section role |
|---|---|---|---|
| Front | Abstract | venue-bound | State the finance friction, model object, main result, mechanism, and implication. |
| 1 | Introduction | support/core bridge | Motivate the puzzle, explain the modeling contribution, preview the main result, and state implications. |
| 2 | Related Literature | support | Position the model against prior theory and empirical facts without turning the section into a survey. |
| 3 | Model Environment | primary-core | Define agents, timing, preferences, information, constraints, assets/contracts, institutions, and assumptions. |
| 4 | Equilibrium / Solution Concept | primary-core | State equilibrium definition, optimization problem, clearing conditions, or solution concept. |
| 5 | Results / Propositions | primary-core | Present propositions, lemmas, theorem-like claims, comparative statics, and their economic intuition. |
| 6 | Proof Logic And Robustness Of Mechanism | evidence-core | Provide proof sketches, mechanism checks, robustness of assumptions, and boundary cases; defer full proofs. |
| 7 | Empirical, Policy, Or Calibration Implications | support/evidence | Translate the model into testable predictions, calibration moments, policy implications, or observable patterns. |
| 8 | Conclusion | compress-first | Restate the theoretical contribution and open questions without adding new propositions. |
| Back | Appendix: Full Proofs And Extensions | venue-bound | Put full proofs, derivations, auxiliary lemmas, additional equilibria, and extended examples here. |

## Flexible Adjustment Notes

- If the paper is mostly empirical with a small model, use `empirical-research-paper.md` and include
  the model as a section or appendix.
- If the model supports a short one-result paper, use `short-insight-letter-paper.md` only when the
  target route is explicitly a short insight/letter format.
- Make hidden assumptions explicit; theory reviewers attack assumptions before prose style.
