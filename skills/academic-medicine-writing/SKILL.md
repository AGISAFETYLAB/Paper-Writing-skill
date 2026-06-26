---
name: academic-medicine-writing
description: >-
  Use for medical manuscript artifacts: planning, drafting, revising, citing,
  figure/table preparation, checklist compliance, submission package review,
  reviewer response, and publication-readiness work for clinical, biomedical,
  public-health, diagnostic, treatment, safety, patient/cohort, prediction-model,
  systematic-review, case-report, global-health, or health-economics research
  papers. Also trigger on Chinese manuscript-writing requests such as
  医学论文写作、临床论文、公共卫生论文、生物医学论文、CONSORT、STROBE、PRISMA、STARD、TRIPOD、写摘要/方法/结果/讨论、临床引用核查、投稿前自检.
  This package writes and revises paper artifacts only; it does not provide
  medical advice, diagnose, treat, run analyses, or invent results.
---

# Academic Medicine Writing — Standalone Entry Router

This is the standalone medicine package of `paper-writing-skill`. It can be installed by itself:
copy this `academic-medicine-writing/` folder and no other discipline package is required.

It does no writing work itself. Its job is to route the request to exactly one internal sub-skill
under `skills/`, then **read and follow that sub-skill's `SKILL.md`**.

| Sub-skill | Path | Owns |
|---|---|---|
| **`academic-writing` (hub)** | `skills/academic-writing/SKILL.md` | Medical manuscript writing and revision orchestration. |
| `academic-figure` | `skills/academic-figure/SKILL.md` | Clinical figures/tables, CONSORT/STROBE/PRISMA/STARD/TRIPOD display logic, table/figure QA. |
| `academic-citation` | `skills/academic-citation/SKILL.md` | Biomedical citation search/write/verification, Vancouver/AMA-style reference integrity, trial/checklist citation audit. |
| `academic-review` | `skills/academic-review/SKILL.md` | Medical submission-readiness review, checklist compliance, statements, ethics/trial-registration/data-sharing gates. |

Package-local shared resources live under `_shared/` and `assets/templates/`. Sub-skill-specific
resources live under each internal sub-skill's own `references/` and `scripts/` directories.
Internal sub-skills load everything by relative path, so this folder remains self-contained when
downloaded alone.

## Routing

1. **Write or revise a medical manuscript, section, or manuscript plan** -> read
   `skills/academic-writing/SKILL.md`.
2. **Only a figure or table** — clinical flow diagram, baseline table, adverse-event table,
   diagnostic plot, PRISMA/CONSORT flow, forest plot, Kaplan-Meier-style display → read
   `skills/academic-figure/SKILL.md`.
3. **Only citations / bibliography** — source finding, Vancouver/AMA references, trial/reporting
   guideline citations, citation audit → read `skills/academic-citation/SKILL.md`.
4. **Only review / submission check** — reviewer-risk, checklist compliance, statements, final
   readiness → read `skills/academic-review/SKILL.md`.

When a request spans writing plus figures/citations/review, route to the hub; it delegates at the
right stage.

## Scope

This package writes and revises manuscript artifacts only. It does not provide medical advice, run
research, or invent facts. Detailed claim-boundary and integrity rules live in `_shared/core/stance.md`
and are loaded by the routed sub-skills.
