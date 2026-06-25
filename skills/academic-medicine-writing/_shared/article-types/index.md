# Medical Article Type Index

Use this index after Writing Policy has identified the study type and checklist. The `study_type`
axis selects the reporting checklist; the `article_type` axis selects the manuscript structure. They
often align, but they are not interchangeable: a JAMA Research Letter can report an observational
study, and a Nature Medicine Article can report a trial, prediction model, or analysis.

Article-type profiles set section structure and proportional budget only. Absolute word, page,
display-item, abstract, key-points, and reference limits come from the active target journal or the
Generic Medical Length Fallbacks in `_shared/submission/templates.md`.

## Article Type Selection Map

| Article type | Profile | Typical checklist pairing | Structure center |
|---|---|---|---|
| Generic medical article | `generic-medical-article.md` | Checklist unresolved or selected separately | Fallback for unknown, mixed, early-stage, or locally reviewable manuscripts |
| Original Investigation / Article | `original-investigation.md` | CONSORT, STROBE, STARD, TRIPOD, CHEERS, GATHER as applicable | IMRaD original research with complete Methods and Results |
| Clinical Trial | `clinical-trial.md` | CONSORT for trial results; SPIRIT for protocols | intervention, randomization, outcomes, harms |
| Study Protocol | `study-protocol.md` | SPIRIT, PRISMA-P, or design-specific checklist | planned design, outcomes, analysis, ethics, dissemination |
| Observational Study | `observational-study.md` | STROBE | cohort/case-control/cross-sectional exposure-outcome evidence |
| Systematic Review / Meta-analysis | `systematic-review.md` | PRISMA | search, screening, synthesis, certainty/risk of bias |
| Scoping / Rapid Review | `scoping-rapid-review.md` | PRISMA-ScR, PRISMA 2020 plus Cochrane rapid review guidance | evidence map, rapid synthesis, method shortcuts made explicit |
| Diagnostic Accuracy | `diagnostic-accuracy.md` | STARD | index test, reference standard, accuracy metrics |
| Prediction Model | `prediction-model.md` | TRIPOD / TRIPOD+AI | development, validation, calibration, utility |
| Case Report | `case-report.md` | CARE | patient timeline, diagnostic assessment, intervention, outcome, consent |
| Research Letter / Brief Report | `research-letter.md` | Any applicable checklist in compressed form | short original-research report with minimal displays |
| Review / Perspective | `review-perspective.md` | PRISMA only if systematic; otherwise narrative review conventions | synthesis, argument, implications |
| Qualitative / Mixed Methods | `qualitative-mixed-methods.md` | SRQR, COREQ, plus quantitative design checklist when mixed | sampling, reflexivity, themes, integration/joint display evidence |
| Methods / Statistical Methodology | `methods-paper.md` | SAMPL plus design-specific guidance as applicable | method, assumptions, simulation/validation, reproducibility |
| Guideline / Consensus / Position Statement | `guideline-consensus.md` | RIGHT, AGREE, ACCORD, CREDES as applicable | evidence-to-recommendation or consensus methods and statements |
| Editorial / Commentary / Correspondence | `editorial-commentary-letter.md` | Usually none unless original data are reported | thesis or response, evidence/counterpoint, concise implication |
| Data Resource / Data Descriptor | `data-resource-paper.md` | FAIR/data availability plus domain guidance | data records, technical validation, access/reuse conditions |
| Health Economics | `health-economics.md` | CHEERS | perspective, costs, utilities, model/trial evaluation, uncertainty |
| Global Health Estimates | `global-health-estimates.md` | GATHER | input data, estimation model, uncertainty, reproducibility |

## Source Basis

Use the official or authority source matching the selected type before drafting: ICMJE for generic
medical article structure; CONSORT/SPIRIT and PRISMA-P for protocols; PRISMA/PRISMA-ScR and Cochrane
rapid review guidance for reviews; COREQ/SRQR for qualitative reports; SAMPL and methodology-journal
instructions for methods papers; RIGHT/AGREE/ACCORD/CREDES for guideline or consensus manuscripts;
target-journal article-type instructions for editorials, commentaries, correspondence, research
letters, and data/resource papers; Scientific Data or BMC Research Notes guidance for data
descriptors and data notes.

## Selection Rules

- Prefer the exact target-journal article type when known.
- If the target journal is unknown, infer from evidence and mark the inference as provisional in the
  Writing Policy and Paper Framework.
- Use `generic-medical-article.md` as the default fallback when article type is unknown, mixed, or
  only locally reviewable. Do not use `original-investigation.md` as the global fallback.
- Use `original-investigation.md` for full original empirical research when the journal's article type
  is "Original Investigation", "Article", or similarly broad.
- Use design-specific profiles when they materially change structure: trial, observational,
  protocol, observational, systematic review, scoping/rapid review, diagnostic, prediction, case
  report, qualitative/mixed methods, methodology, guideline/consensus, data resource, health
  economics, or global estimates.
- Use `research-letter.md` only when the user or target journal has selected a short original
  research format.
- Use `review-perspective.md` only for non-systematic reviews, perspectives, comments, or narrative
  synthesis. Use `systematic-review.md` for systematic reviews and meta-analyses.

## Framework Main Content Contract

During Paper Framework, each Section Plan row should compress the selected profile's `Section role`
into a short planning cue. Do not paste checklist item inventories into the Section Plan. Item-level
evidence belongs in the Checklist Matrix.
