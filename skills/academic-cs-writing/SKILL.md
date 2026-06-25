---
name: academic-cs-writing
description: Use when planning, drafting, revising, reviewing, citing, or preparing figures/tables for computer science, AI, ML, NLP, CV, HCI, data mining, systems, benchmark, dataset, or software-tool research papers. Also trigger on CS paper-writing requests in Chinese such as 计算机论文写作、AI论文、机器学习论文、写paper、搭论文框架、写引言/摘要/方法/实验/相关工作、论文配图、补引用、审稿、投稿前自检. This standalone CS package writes and revises paper artifacts only; it does not run experiments or invent results.
---

# Academic CS Writing — Standalone Entry Router

This is the standalone computer-science package for paper writing. It can be installed by itself:
copy this `academic-cs-writing/` folder and no other discipline package is required.

It does no writing work itself. Its job is to route the request to exactly one internal sub-skill
under `skills/`, then **read and follow that sub-skill's `SKILL.md`**.

The package is a hub plus three specialized internal siblings, sharing one package-local layer:

| Sub-skill | Path | Owns |
|---|---|---|
| **`academic-writing` (hub)** | `skills/academic-writing/SKILL.md` | The CS writing pipeline (Writing Policy -> Paper Framework -> LaTeX project -> section drafting) and the two confirmation gates. Delegates figures/citations/review to the siblings. |
| `academic-figure` | `skills/academic-figure/SKILL.md` | Every figure and table: planning, plot style, table design, assets, and QA gate. |
| `academic-citation` | `skills/academic-citation/SKILL.md` | Every searched/written/verified citation and the BibTeX audit. |
| `academic-review` | `skills/academic-review/SKILL.md` | Closing review, static audits, submission-readiness, and before-returning checks. |

The shared layer lives inside this package under `_shared/` (core stance, gates, contract; bundled
CS/AI venue templates; paper-type and venue cards; shared rubrics). It is **not** a separate
downloaded dependency. Internal sub-skills load it by relative path (`../../_shared/...`), which
resolves inside this `academic-cs-writing/` folder.

## Routing — pick exactly one sub-skill, then follow its SKILL.md

Do not apply any writing, figure, citation, or review logic from memory or from this router.
Resolve the request to one sub-skill and open its `SKILL.md`:

1. **Write or revise a CS paper, or any section** — full first draft from a workspace; Writing Policy
   or Paper Framework only; rewrite/polish/diagnose/compress/weaken-claims/improve-flow on existing
   prose -> **read and follow `skills/academic-writing/SKILL.md`** (the hub). This is also the
   default when the request spans multiple subsystems or is ambiguous, because the hub already
   delegates to the other three at the right time.
2. **Only a figure or table** — "make this plot", "fix this table's layout", 画个图/做表 ->
   **read and follow `skills/academic-figure/SKILL.md`** directly.
3. **Only citations / bibliography** — "find sources for X", "audit my .bib", 补引用/查引文 ->
   **read and follow `skills/academic-citation/SKILL.md`** directly.
4. **Only a review / pre-submission check** — "review my paper", 审稿/投稿前自检 ->
   **read and follow `skills/academic-review/SKILL.md`** directly.

When in doubt, route to the hub (`skills/academic-writing/SKILL.md`); it owns the orchestration
and will pull in the siblings as each stage needs them.

## Scope

This package produces and revises the paper artifact; it does **not** do the research. It must not
change the research idea, design or run experiments, or invent/alter results or citations. The full
scope, the STOP-never-guess decision rule, the interaction-language rule, and the integrity rules
live in `_shared/core/` and are loaded by each internal sub-skill.
