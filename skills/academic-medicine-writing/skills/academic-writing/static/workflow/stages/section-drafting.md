# Stage: Section Drafting — Medicine

Draft by section using IMRaD logic, the confirmed Paper Framework, the selected checklist, and the
Statement Plan.

Load `references/sections/index.md`, `references/sections/paragraph-flow.md`, the
section-specific guide, the selected checklist card, the selected item JSON under
`../../_shared/checklists/items/`, and `../../_shared/submission/statements.md` when drafting statement
material. Invoke `academic-figure` for every display and `academic-citation` for every external
source.

Section-specific guide routing:

| Section task | Required guide |
|---|---|
| Title, structured abstract, Key Points, summary box | `references/sections/title-abstract.md` |
| Introduction | `references/sections/introduction.md` |
| Literature positioning, Background, Related Work, prior-work comparison | `references/sections/literature-positioning.md` |
| Methods | `references/sections/methods.md` |
| Results | `references/sections/results.md` |
| Discussion, limitations, conclusion | `references/sections/discussion.md` |
| Appendix, supplement, eTables/eFigures, extended methods, supplemental analyses | `references/sections/appendix-supplement.md` |
| Ethics, consent, registration, data sharing, funding, conflicts, author contribution, AI use | `references/sections/statements.md` |

## Section Evidence Boundary

For each section:

1. Define the section's role and main claim.
2. Map claims to source evidence, manuscript evidence, or verified citation support.
3. Set the medical claim grammar: population/setting, intervention/exposure/index test/predictor,
   comparator/reference standard, outcome, timeframe, analysis population, uncertainty.
4. Identify statements/checklist items the section must satisfy.
5. Decide which display items support the section.
6. After drafting or revising the section, update the working checklist matrix item status and
   manuscript location from actual source evidence only.

Do not show internal section plans unless the user asks or a blocking risk must be surfaced.

## Section Rules

- **Title and Abstract**: follow `references/sections/title-abstract.md`. Make study design
  visible; keep objective, design/setting, participants, exposure/intervention/index test, main
  outcome, primary result, and conclusion aligned with source evidence. Do not turn association into
  causation or validation into clinical deployment.
- **Introduction**: follow `references/sections/introduction.md`. Move from
  clinical/public-health/biomedical problem to precise evidence gap to study objective. Avoid broad
  disease burden filler unless it supports the target question.
- **Literature positioning**: follow `references/sections/literature-positioning.md` when a
  paragraph's job is background, related work, prior-work comparison, or Discussion comparison. Use
  current knowledge -> unresolved gap -> study contribution, with verified citations and
  design-appropriate contribution verbs.
- **Methods**: follow `references/sections/methods.md`. Include design, setting, dates,
  eligibility, intervention/exposure/index test/predictor, comparator/reference standard, outcomes,
  sample-size/power when applicable, missing-data handling, bias/confounding control, statistical
  analysis, software/version when provided, ethics/consent/registration as required. Every
  variable/result in Results must have a Methods anchor.
- **Results**: follow `references/sections/results.md`. Use Results-only language. Open with
  participant/sample flow and baseline characteristics when applicable, then primary result, then
  secondary/sensitivity/subgroup/safety or validation layers. Do not explain mechanisms, speculate,
  or make practice recommendations here.
- **Discussion**: follow `references/sections/discussion.md`. Start with principal findings,
  compare with prior work using verified citations, explain plausible interpretation without
  overclaiming, state limitations, and close with scoped implications that match design strength.
- **Appendix and supplement**: follow `references/sections/appendix-supplement.md`. Every
  supplemental item must have a main-text anchor, first-citation order, evidence status, and a
  reason it belongs outside the main manuscript.
- **Statements**: follow `references/sections/statements.md` and `../../_shared/submission/statements.md`.
  Write only from confirmed facts. Unknown IDs remain `[AUTHOR: specify ...]` or a blocking issue,
  depending on submission status.

Introduction and Discussion must not be citation-thin when a clinical target journal is named.
For a JAMA-style Original Investigation draft, use enough verified clinical and reporting sources to
support the problem, prior work, guideline/reporting context, and interpretation. If sources cannot
be verified in the run, weaken the background and record the citation gap in `paper/review-report.md`
instead of returning a polished but under-supported manuscript.

## Medical claim grammar

Every results or conclusion sentence must be checkable:

```text
In <population/setting>, <intervention/exposure/index test/predictor> compared with <comparator or
reference standard>, was associated with / improved / predicted / detected <outcome> over
<timeframe>, in <analysis population>, with <effect estimate and uncertainty>.
```

Use only the parts relevant to the study design. If a part is missing from source material, weaken
the sentence or mark it.

## Citation Search Trigger

Invoke `academic-citation` when drafting needs:

- clinical/background sources in Introduction or Discussion,
- reporting guideline citations,
- trial registration, protocol/SAP, or data repository source,
- methods/statistical references,
- comparable studies,
- claims about disease burden, standard of care, diagnostic thresholds, model evaluation standards,
  or prior systematic reviews.

Do not fabricate references. A central clinical claim without source support must be weakened,
removed, or marked as missing evidence.

## Display Handling

Invoke `academic-figure` for every table/figure. Every display must support one manuscript claim and
state denominator, analysis population, timeframe, uncertainty, and missingness when applicable.
Legends must be self-contained: define abbreviations, sample size, statistical test, error bars, and
representative/panel notes where relevant.

Do not refer to internal files in manuscript body prose, captions, or table titles. Examples such as
`main.tex`, `tables/outcome_table.csv`, generator script names, source folder names, or skill/package
paths may appear in `submission-package.md` or validation reports, but not in the article text unless
the manuscript is explicitly an engineering methods report about those files.

## Missing-Support Markers

Use precise markers only when the underlying evidence genuinely does not exist:

```tex
% EVIDENCE_NEEDED: <missing result/source>
% CITATION_NEEDED: <source needed and not yet verified>
% FIGURE_NEEDED: <display cannot be produced from available data>
% TABLE_NEEDED: <table cannot be produced from available data>
% STATEMENT_NEEDED: <ethics/registration/data-sharing fact missing>
```

Markers are not placeholders for routine work. If a citation is findable or a table can be created
from provided data, resolve it through the sibling skill in this run.

## Drafting Rules

- One paragraph has one message. Apply `references/sections/paragraph-flow.md`.
- The first sentence states the paragraph function or claim.
- Preserve study type, endpoint definitions, denominator, and analysis population.
- Use past tense for completed studies.
- Define abbreviations at first use.
- Do not add p values, confidence intervals, sample sizes, or adverse events absent from source
  material.
- Do not write medical advice, diagnosis, treatment instructions, or clinical recommendations.
- Do not hide limitations in generic language; tie them to design, data, bias, sample, follow-up,
  missingness, external validity, or residual confounding.
- Do not mark a checklist item satisfied unless all required evidence for that JSON item is present
  or the missing part is explicitly justified as not applicable.

## Full-Draft Length Enforcement

Before returning a full draft, calculate the main-text word count from Introduction through
Conclusions, excluding abstract, Key Points, tables, figures, article information, references, and
appendices. Compare it with the Paper Framework's Length Budget Summary and section-level word
budgets.

A full-draft response is incomplete if it reports a draft length gate without the numeric count and budget comparison. If the draft is under the lower bound and evidence-supported expansion is possible, revise the manuscript before packaging. Do not mark draft length gate: PASS for an under-target draft because it is polished, compiled, or has a complete file set.

- If the manuscript is below the lower bound, expand only evidence-supported content: design
  rationale, data source boundary, eligibility details, exposure/outcome definitions, bias and
  missingness handling, statistical analysis detail, results interpretation tied to denominators,
  prior-work comparison, and specific limitations.
- Do not pad with unsupported background statistics, clinical recommendations, generic filler, or
  repeated caveats.
- For JAMA-style Original Investigation, treat fewer than 2500 main-text words as a draft length
  gate failure unless the saved framework explicitly justifies a conservative under-target.
- Add the calculated `Actual main-text word count` and `draft length gate: PASS` or a justified
  `draft length gate: BLOCKED` line to `paper/submission-package.md`.

Before returning a full draft, delegate to `academic-review` for checklist, statement, citation,
official-source, and format-specific production gates. Word-first routes require `manuscript.docx`;
LaTeX-first routes require compiled PDF; generic-review routes must not be called submission-ready.
