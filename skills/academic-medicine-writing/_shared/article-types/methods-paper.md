# Methods / Statistical Methodology Profile

Use this profile for biomedical methods papers: statistical methods, epidemiologic methods, research
methodology, measurement methods, simulation studies, validation methods, or methodological reviews
that propose or evaluate an approach rather than report a single clinical study.

## Source Anchors

- SAMPL statistical reporting guidance on EQUATOR: https://www.equator-network.org/2013/02/11/sampl-guidelines-for-statistical-reporting/
- BMC Medical Research Methodology submission guidelines: https://link.springer.com/journal/12874/submission-guidelines
- Statistical Methods in Medical Research author instructions: https://journals.sagepub.com/author-instructions/smm

## Profile Boundary

This profile owns section structure and proportional budget only. Apply
`_shared/article-types/profile-boundary.md` for hard-default and deviation rules.

## Length Budget Source

Take absolute length from the active `target_length_budget`. Methodology journals differ widely, so
do not inherit clinical original-research word/display caps without checking the target.

## Checklist / Study-Type Pairing

Use SAMPL for statistical reporting and add design-specific guidance when the methods paper includes
simulation, diagnostic/prediction validation, trial methods, qualitative methods, or software.

## Priority Contract

- Primary core: Method / methodological contribution.
- Evidence core: Demonstration, simulation, validation, or worked example.
- Compress first: broad textbook background, implementation details that can move to supplement,
  and secondary examples.
- Core floor: problem definition, assumptions, method description, comparison standard, evaluation
  design, limitations, and reproducibility material cannot be omitted.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Title / abstract | outside main budget unless target counts it | State the methodological problem, proposed approach, evaluation basis, and use case. |
| 1 | Introduction | 10-15% | Motivate the methodological gap and target users. |
| 2 | Method / Framework | 28-38% | Define assumptions, notation/inputs, procedure, estimand or target quantity, and implementation details needed for use. |
| 3 | Evaluation / Simulation / Worked Example | 28-38% | Test the method against benchmarks, simulations, empirical examples, sensitivity analyses, or validation datasets. |
| 4 | Practical Guidance / Software / Reproducibility | 8-14% | Explain use conditions, code/package availability, reporting guidance, and failure modes. |
| 5 | Discussion | 12-18% | Interpret strengths, limitations, generalizability, and comparison with alternatives. |
| 6 | Conclusions | 1-3% | State the method-supported conclusion. |
| Back | Supplement / code / extended derivations | outside main text unless target counts it | Carry proofs, full simulation grids, code, parameters, and extended examples. |

## Flexible Adjustment Notes

- If the manuscript mainly validates a clinical prediction model, use `prediction-model.md`.
- If the manuscript is a narrative explanation of an existing statistical method, consider
  `review-perspective.md` unless new methodological evidence is present.
