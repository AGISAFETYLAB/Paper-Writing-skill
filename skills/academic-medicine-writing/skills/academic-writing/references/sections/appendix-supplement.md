# Appendix And Supplement

Use this guide when drafting appendices, supplements, eTables, eFigures, extended methods,
checklist appendices, data-source inventories, or supporting analyses. A supplement is not a place
to hide weak logic; every item needs a main-text anchor and a clear reason for being outside the
main manuscript.

## Writing Readiness

Before drafting, confirm:

- the main-text claim, method, table, figure, checklist item, or statement that each supplement item
  supports;
- whether the target journal requires a single supplement file, separate uploads, or named eTables
  and eFigures;
- the source evidence for each supplemental result or method detail;
- whether any supplemental material contains identifiable, restricted, copyrighted, or
  controlled-access data;
- whether the supplement changes the interpretation of the main text.

If a supplemental item is essential for understanding the primary result, consider whether it belongs
in the main text instead.

For JAMA/JAMA-family routes, plan a single supplement Word document for submission unless the
current official instructions or editorial system requires separate files. Markdown, CSV, or JSON
files may be kept as auditable source artifacts, but they do not by themselves satisfy the
submission-clean supplement package. Record a blocker when only source fragments exist.

## Main-Text Anchor Rule

Each appendix or supplement item must have a main-text anchor:

```text
Main-text anchor: <section/paragraph/table/figure claim supported>
Supplement item: <eTable/eFigure/Appendix section>
Reason outside main text: <length, detail, secondary analysis, checklist, source inventory, or method detail>
Evidence status: <confirmed / partial / missing>
```

Do not create orphan supplement sections. Do not place primary definitions, primary endpoint
results, ethics status, or essential eligibility criteria only in the supplement unless the journal
explicitly requires that layout and the main text still summarizes them.

## Recommended Order

Use target journal order when specified. Generic order:

1. supplemental methods and extended definitions;
2. additional data-source, eligibility, or cohort-flow details;
3. supplemental tables and figures in first-citation order;
4. sensitivity, subgroup, negative-control, or validation analyses;
5. checklist matrix, statement details, data/code availability details, or repository metadata.

For systematic reviews, place search strategies, screening details, risk-of-bias tables, and study
characteristics before secondary synthesis. For prediction or diagnostic studies, place model/test
specification, calibration/threshold details, and validation tables near the related main result.

## Labeling And Cross-Reference

- Use journal-compatible labels such as Appendix, Supplement, eTable, eFigure, or Supplementary
  Table only after the target format is known.
- Keep numbering stable with first citation in the manuscript.
- Include denominators, analysis populations, timeframes, uncertainty intervals, and missingness
  notes when they matter for interpretation.
- State when a supplemental analysis is exploratory, sensitivity, post hoc, or externally validated.
- Keep file names and internal generator paths out of manuscript prose unless the paper is
  explicitly about a software or data resource.

## Common Failures

- Supplement contains tables or figures that are never cited from the main text.
- A main claim depends on a supplement item but the main text does not summarize the relevant
  direction, magnitude, or limitation.
- Supplemental methods introduce variables, endpoints, or model changes not anchored in Methods.
- eTables omit denominators, missingness, or analysis population.
- Supplementary analyses are described as confirmatory without prespecification or source evidence.
