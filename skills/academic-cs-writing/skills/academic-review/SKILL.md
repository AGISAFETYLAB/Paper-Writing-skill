---
name: academic-review
description: Use when reviewing, auditing, or checking a research paper draft for submission readiness — skeptical two-round defect review, reviewer-risk analysis, writing-craft audit, page-budget and mechanical static audits, claim-evidence and metric soundness, and the final submission-readiness verdict. Triggers with or without a full draft, including Chinese phrasings like 审稿、审一遍、论文 review、投稿前自检、提交前检查、reviewer 视角、查问题、稿件体检. Part of the academic-writing collection; the academic-writing hub delegates the closing review and audits here.
---

# Academic Review — Router

This skill runs the **closing review, static audits, and submission-readiness gate** for a paper
draft. It is independently invokable ("review my paper", "is this submission-ready?") and is the
subsystem the **`academic-writing`** hub hands off to once the first complete `paper/` draft exists.

It is split into two layers:

- A **static layer** at `static/closing-gates.md` — the mandatory closing sequence (Draft Completion
  Review Gate → Final Static Audits → Submission Readiness → Before-Returning Compliance Self-Check).
- A **dynamic layer** (this file + `manifest.yaml`) plus deep references (`paper-review.md`,
  `reviewer-risk.md`, `submission-readiness.md`, `writing-craft.md`,
  `journal-submission-elements.md`, `data-code-availability.md`,
  `high-impact-journal-review.md`) and the mechanical gate `scripts/audit_draft.py`.

Cross-skill stance/integrity and the shared claim-evidence / metric-design rubrics live in
`../../_shared/`. Review is **writing-only**: it surfaces defects and risks; it never invents
results or strengthens unsupported claims.

## Intake boundary

When a complete `paper/` draft is available, run the full closing sequence below. When the user
provides only a partial manuscript packet (PDF only, selected sections, abstract, notes, or an
uncompiled TeX fragment), run the **Bounded Review Intake** in `references/sections/paper-review.md`
instead: report the input scope, assessment boundary, visible evidence base, missing materials, and
review risks. Do not run the full static-audit/readiness gate or produce a `PASS` submission-ready
verdict until a complete local `paper/` draft can be checked.

## ⚠️ Reviewer independence

Round 2 of the review must run in a fresh, isolated context: pass only the reviewer role, venue/format
constraints (including the content-page limit and Limitations placement), review dimensions, neutral
required-move rubrics, and the LaTeX/PDF paths — never the author's section plans, Round 1 findings,
or fix summaries. Mirror the user's interaction language (`../../_shared/core/stance.md`).

## Routing protocol

1. **Load the core layer.** Read `manifest.yaml`, the `always_load` files
   (`../../_shared/core/stance.md`, `static/closing-gates.md`).
2. **Run the closing sequence in order** per `static/closing-gates.md`:
   - Draft Completion Review Gate (Round 1 self + Round 2 independent subagent) → load
     `references/sections/paper-review.md`; pull reviewer-risk and writing-craft rubrics as needed.
   - Final Static Audits (BLOCKING) → run `scripts/audit_draft.py` and, via the `academic-citation`
     skill, `audit_citations.py`; both must report `PASS`.
   - Final Submission Readiness Gate → load `references/checks/submission-readiness.md` (and
     `references/checks/journal-submission-elements.md` when `venue_kind=journal`).
   - Before-Returning Compliance Self-Check.
3. **For claim or metric soundness**, load the shared rubrics `../../_shared/checks/claim-evidence.md`
   and `../../_shared/checks/metric-design.md`.

```bash
python3 "<path-to-this-skill>/scripts/audit_draft.py" paper --framework writing-policies/<slug>-paper-framework.md [--max-content-pages <limit>]
```

## Why this split

- Review and submission QA are a self-contained task that authors run repeatedly and often alone, so
  they live in their own skill with the draft-audit script alongside.
- The hub delegates the closing gates here instead of duplicating them, keeping responsibilities
  non-overlapping.
