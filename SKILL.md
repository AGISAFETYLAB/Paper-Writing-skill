---
name: academic-writing-skill
description: >-
  Route academic paper-writing requests to the correct standalone discipline package in this
  repository: academic-cs-writing for computer science/AI/ML systems papers,
  academic-medicine-writing for medical/clinical/biomedical papers, and academic-finance-writing for
  finance/econometrics/markets papers. Use when the user downloaded the full academic-writing-skill bundle
  and asks to write, revise, cite, figure, review, or prepare an academic paper. Always classify the
  discipline before task type. This router delegates only; each discipline package must remain
  independently installable.
---

# Academic Writing Skill — Bundle Router

This is the optional entry router for the full `academic-writing-skill` bundle. It is not required when a
user installs only one discipline package.

## Discipline-First Hard Gate

- For every user request, first decide the discipline before classifying task type.
- Do not route by task type before discipline.
- This applies even when the user asks only to draw a table, draw a figure, polish prose, revise
  text, cite sources, or review a manuscript, and even when the user provides content only with no
  working directory.

Infer discipline from explicit skill or domain names, title, abstract, prose, venue, terminology,
data type, variables, methods, citations, article/reporting standards, or requested output. If
exactly one of CS, medicine, or finance is clear, load that discipline package and let it classify
the task type internally.

If no clear CS/medicine/finance signal is present, pause immediately and ask one concise discipline-selection question. Do not load any discipline package, classify task type, draft content, create figures or tables, cite sources, or review the manuscript. Continue only after the user answers the discipline question. Do not default silently to a discipline.

Route to exactly one standalone package:

| Request | Package |
|---|---|
| Computer science, AI, ML, NLP, CV, HCI, data mining, systems, benchmark, dataset, software-tool paper | `skills/academic-cs-writing/SKILL.md` |
| Medical, clinical, biomedical, public-health, diagnostic, treatment, safety, patient/cohort paper | `skills/academic-medicine-writing/SKILL.md` |
| Finance, asset pricing, markets, accounting, corporate finance, risk, portfolio, trading/backtest, econometrics paper | `skills/academic-finance-writing/SKILL.md` |

Do not mix discipline packages in a single paper unless the user explicitly asks for an
interdisciplinary workflow.

Each package under `skills/` must be self-contained: copying one package folder should be enough to
install and run that discipline skill. The finance package ships reusable templates and provenance
metadata only; do not include generated finance manuscript packages or private compiled paper
artifacts there.
