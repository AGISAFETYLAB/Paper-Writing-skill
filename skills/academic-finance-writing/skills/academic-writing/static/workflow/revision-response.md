# Referee Response Workflow — Finance

Use when the user provides referee reports, editor letters, seminar comments, an R&R decision, or
an internal review that requires a response package.

## Load Order

1. Load `references/referee-response.md`.
2. Load `../academic-review/references/review.md` for severity and contribution/execution/exposition risk.
3. Load `../../_shared/checks/econometrics.md`,
   `../../_shared/checks/identification-strategies.md`, and
   `../../_shared/checks/research-workflow.md` when comments touch methods, data, code, or
   replication.

## Required Outputs

Create or update:

- `response-letter.md`
- `revision-backlog.md`
- `paper/revision-map.md` when a manuscript package exists

## Procedure

1. Extract every distinct referee/editor concern.
2. Classify each concern: contribution, identification, robustness, data, citation, exposition,
   formatting, or submission policy.
3. Map each concern to an existing or required manuscript change.
4. Verify whether the manuscript or source materials already contain the change.
5. Draft a respectful point-by-point response.
6. Mark unresolved work in `revision-backlog.md`.

Do not claim completed analyses, new tables, robustness checks, data access, code release, or
repository deposits unless the evidence exists. If not complete, write the planned response and mark
the item `needs_user_evidence`.

Rule: do not claim completed analyses when the manuscript, code, tables, or user-provided evidence
do not prove they are complete.
