# Empirical Finance Research Paper Type

Use this profile for original empirical finance papers: asset pricing, corporate finance, banking,
household finance, fintech, market microstructure, accounting, risk, or policy-relevant empirical
financial economics. The domain does not change this structural profile by itself.

## Source Anchors

- Elsevier financial-economics journal descriptions identify empirical financial-economics work and
  emphasize replicability and data/program availability where relevant:
  https://shop.elsevier.com/subjects/journals/social-sciences-and-humanities/economics-and-finance/financial-economics
- JRFM author instructions define original research articles and require reproducible details:
  https://www.mdpi.com/journal/jrfm/instructions
- Journal of Economics and Finance submission guidance notes that authors may be asked to submit
  empirical data examined:
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

- Primary core: Data And Research Design.
- Evidence core: Main Results and Robustness / Mechanisms.
- Compress first: broad literature review, long institutional background, conclusion, and secondary
  robustness tables that can move to the appendix.
- Core floor: protect data construction, identification/design, main results, uncertainty, and
  economic magnitude before compressing background or secondary tests.

| Order | Candidate section | Budget rule | Section role |
|---|---|---|---|
| Front | Abstract | venue-bound | State the empirical question, setting, data, design, headline estimate, and economic interpretation. |
| 1 | Introduction | support/core bridge | Present the finance puzzle, contribution, empirical strategy preview, main result, and why the magnitude matters. |
| 2 | Literature And Institutional Setting | support | Locate the paper in related finance/economics work and explain institutions needed to interpret the design. |
| 3 | Data And Variable Construction | primary-core | Define data sources, sample window, unit of observation, filters, variables, outcomes, and replication boundary. |
| 4 | Empirical Design | primary-core | State research design, identifying variation, model specification, assumptions, standard errors, and threats to interpretation. |
| 5 | Main Results | evidence-core | Present central estimates, uncertainty, economic magnitude, and the display items supporting the main claim. |
| 6 | Robustness, Mechanisms, And Heterogeneity | evidence-core | Test robustness, mechanisms, channels, subgroup patterns, placebo/pre-trend diagnostics, and alternative explanations. |
| 7 | Discussion And External Validity | support | Interpret scope, welfare or market implications when supported, and limits to causal or predictive language. |
| 8 | Conclusion | compress-first | Summarize what the evidence supports and what remains unresolved. |
| Back | Online Appendix / Internet Appendix | venue-bound | Move extended variable definitions, extra tables, robustness grids, code-output maps, and supplementary figures. |

## Flexible Adjustment Notes

- Load `_shared/checks/identification-strategies.md` and `_shared/checks/econometrics.md` for DiD, IV, RD,
  synthetic control, event studies, portfolio sorts, factor models, structural estimation, ML/text,
  or backtests.
- Do not make an event-study or corporate-finance topic a separate paper type unless it changes the
  section structure beyond this empirical profile.
- Keep unsupported causal language marked `needs_user_evidence`.
