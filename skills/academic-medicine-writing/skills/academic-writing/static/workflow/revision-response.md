# Revision Response Workflow — Medicine

Use when the user provides reviewer comments, editor decision letters, revision notes, rebuttal
drafts, or asks for a point-by-point response package for a medical manuscript.

This workflow is distinct from ordinary `draft-revision`. Its goal is to produce a credible
revision plan and response package tied to actual manuscript changes, not polite response prose that
pretends unresolved work is complete.

## State Machine

```text
Review package / reviewer comments
  -> intake and manuscript context check
  -> comment triage
  -> revision backlog
  -> response mode selection
  -> revision linkage check
  -> point-by-point response draft
  -> response package review gate
```

## Required Inputs

Minimum useful input:

- editor decision type if available;
- reviewer comments or action items;
- current manuscript or at least title/abstract/methods/results summary;
- target journal and article type when known;
- what revisions, analyses, figures, tables, or wording changes have already been completed.

If reviewer comments exist but manuscript changes are unknown, produce a provisional triage and ask
which changes are completed before final response wording. Do not fabricate completed revisions.

## Comment Triage

Create `paper/revision-backlog.md` or `revision/revision-backlog.md` with one row per comment or
comment cluster:

| comment_id | source | issue_summary | severity | issue_type | required_action | feasibility | owner_fact_needed | status |
|---|---|---|---|---|---|---|---|---|

Severity values: blocker, major scientific issue, major reporting issue, moderate clarification,
minor wording/formatting, out-of-scope or not applicable.

Issue types: new evidence, new analysis, re-analysis, methods clarification, results clarification,
figure/table revision, statement/checklist repair, citation repair, claim-strength calibration,
bounded disagreement, editorial-system item.

## Response Mode

Classify each comment into one response mode:

- acceptance: the manuscript was revised as requested;
- clarification: the manuscript was unclear and now states the existing evidence better;
- additional analysis/re-analysis: analysis was completed and source evidence exists;
- figure/table revision: display was changed and manuscript callouts match;
- limitation handling: the requested evidence does not exist, so claims were weakened;
- bounded disagreement: the reviewer request is not appropriate or not feasible, and the response
  explains why respectfully;
- deferred/user-needed: author facts or analyses are required before a final response can be drafted.

Do not over-apologize, overpromise, or imply that a new experiment, analysis, ethics approval,
trial registration, citation, or figure has been added unless it exists in the revised manuscript or
source evidence.

## Revision Linkage

Every response must link to a real manuscript change or explicitly state why no change was made.

Required linkage fields:

| comment_id | response_mode | manuscript_change | location | evidence_source | unresolved_limit | response_status |
|---|---|---|---|---|---|---|

Allowed `response_status` values: complete, partial, provisional, user-needed, blocked.

When a change crosses the frozen revision boundary, stop and ask before applying it. Examples:
changing primary endpoint, adding unperformed analyses, adding new subgroup results, changing trial
registration or ethics status, or making title/abstract claims stronger than the evidence.

## Output Package

For a substantial R&R or resubmission request, produce:

- `revision/revision-backlog.md`,
- `revision/response-letter.md`,
- `revision/point-by-point-response.md`,
- `revision/change-location-map.md`,
- revised manuscript files only when the user supplied a manuscript and the needed changes can be
  made without inventing evidence.

Simple one- or two-comment requests may return inline response text plus a short linkage table.

## Response Drafting Rules

Each point-by-point response should:

1. acknowledge the comment;
2. state the action taken or the bounded reason no action was taken;
3. point to manuscript location or state `no manuscript change`;
4. avoid claiming completion for missing work;
5. preserve medical evidence boundaries and claim strength.

Use professional, direct language. Do not use generic gratitude to hide unresolved scientific,
ethical, statistical, citation, or checklist weaknesses.

## Review Gate

Before calling a response package ready, invoke `academic-review` when the response changes claims,
methods, results, figures/tables, statements, citations, or submission-readiness status. The review
must check:

- whether every reviewer concern is represented in the backlog;
- whether every response has revision linkage;
- whether any bounded disagreement is evidence-based and non-defensive;
- whether limitations are updated when a request cannot be fully satisfied;
- whether revised manuscript locations match the response letter;
- whether the response creates new claim, citation, checklist, or statement defects.

If a comment asks for data, analysis, ethics, registration, or author decisions that are unavailable,
mark the response package `blocked` or `provisional`; do not fabricate completed revisions.
