# Finance Identification And Methods

## Identification Readiness Gate

Before drafting empirical methods, confirm:

- estimand or target quantity;
- method family guide from `_shared/checks/identification-strategies.md`;
- identifying assumption or descriptive boundary;
- treatment or signal timing;
- unit of observation and fixed effects;
- standard-error treatment and dependence structure;
- diagnostics, placebo tests, or balance checks needed by the method family;
- whether causal language is permitted.

If causal language is not supported, use descriptive or predictive wording.

## Section Movement

1. Target: state what the method estimates in economic terms.
2. Design intuition: explain why the variation, shock, discontinuity, instrument, model, or sorting
   procedure is informative.
3. Specification: present the equation, portfolio sort, event-time design, structural model,
   simulation, or prediction setup.
4. Assumptions: name the identifying assumption and the threats.
5. Inference: specify clustering, dependence adjustment, bootstrap, multiple-testing treatment, or
   model uncertainty.
6. Diagnostics: preview the evidence that makes the design credible.

Use the selected method family guide for exact checks. Do not let the equation arrive before the
economic intuition.
