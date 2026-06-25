# Package Gates And Workflow State

Use this reference whenever a full-draft or package-completion route creates, resumes, reviews, or
returns a `paper/` manuscript package.

## Machine-Readable Workflow State

Maintain a compact `workflow-state.json` alongside the human-readable checkpoint files. It prevents
resume steps from re-inferring paper identity, route, or confirmed gates from prose alone.

Use schema version `medicine-workflow-state-v1`.

Required fields:

| Field | Meaning |
|---|---|
| `schema_version` | Must be `medicine-workflow-state-v1`. |
| `workflow` | Active workflow, such as `full-draft-from-evidence` or `package-completion`. |
| `intent` | Routed intent class. |
| `study_type` | Selected reporting-checklist route, such as `strobe-observational`. |
| `article_type` | Selected article type profile, such as `original-investigation`. |
| `submission_format_route` | `word-first`, `latex-first`, or `generic-review`; unknown until Paper Framework if unresolved. |
| `policy_confirmed` | Boolean. `false` until the Writing Policy gate is confirmed. |
| `framework_confirmed` | Boolean. `false` until the Paper Framework gate is confirmed. |
| `primary_submission_file` | Route-specific primary file, such as `manuscript.docx`, `main.pdf`, or `manuscript.md`. |
| `selected_checklist` | CONSORT, STROBE, PRISMA, STARD, TRIPOD, CARE, GATHER, CHEERS, or unresolved. |
| `required_displays` | Planned main display IDs from the Paper Framework. |
| `required_audits` | Required closing audits, including checklist, citation, display, table, statement, production, and local-path gates. |
| `blocking_gaps` | Current unresolved blockers that prevent submission-ready wording. |

Location contract:

- During Writing Policy and Paper Framework checkpoints, write or update
  `writing-policies/workflow-state.json`.
- When `paper/` is created, copy the current state to `paper/workflow-state.json` and update it as
  package components and gates change.
- Do not mark a gate confirmed in `workflow-state.json` until the user has actually confirmed that
  stage.
- Do not store absolute local paths, raw workspace roots, generator script paths, or private package
  provenance in workflow-state values.

Minimal example:

```json
{
  "schema_version": "medicine-workflow-state-v1",
  "workflow": "full-draft-from-evidence",
  "intent": "full-draft-from-evidence",
  "study_type": "strobe-observational",
  "article_type": "original-investigation",
  "submission_format_route": "word-first",
  "policy_confirmed": true,
  "framework_confirmed": true,
  "primary_submission_file": "manuscript.docx",
  "selected_checklist": "STROBE",
  "required_displays": ["Figure 1", "Table 1"],
  "required_audits": ["DOCX structure audit", "citation audit", "local path leak audit"],
  "blocking_gaps": ["statement status unresolved"]
}
```

## Aggregate Package Gate

Before returning a full `paper/` package, run the aggregate gate after specialized scripts have
written their audit outputs:

```bash
python skills/academic-review/scripts/audit_submission_package.py paper
```

Use the correct relative path for the current working directory. The aggregate gate checks that
`paper/submission-package.md` and optional `paper/workflow-state.json` are internally consistent.

It must block false completion signals, including:

- `word-first` route with a passing production gate but no `paper/manuscript.docx`;
- `latex-first` route with a passing production gate but no `paper/main.pdf`;
- `generic-review` route called submission-ready;
- missing `Actual main-text word count`;
- `draft length gate: PASS` when `Actual main-text word count` is outside the recorded main-text
  word budget or lower-bound completion floor;
- missing draft length, visual display, table aesthetics, citation, statement, production, or local
  path gate status;
- `workflow-state.json` missing required fields or using an unsupported schema version.

A package may pass this aggregate contract while its `Submission-readiness verdict` remains
`BLOCKED`, as long as the blocker set is explicit and internally consistent. Use
`--require-submission-ready` only when the user specifically asks for a final submission-ready
package.

## Behavior Eval Harness

Use captured-output behavior checks for forward tests that cannot be reduced to static file
validation:

```bash
python tests/run_behavior_evals.py --evals evals/evals.json --outputs-dir evals/captured-outputs
```

Each eval case may define an `assertions` object:

```json
{
  "contains": ["写作策略摘要"],
  "not_contains": ["STOP HERE and wait for user response"],
  "regex": ["workflow=full-draft-from-evidence"],
  "not_regex": ["Submission-readiness verdict:\\s*PASS"],
  "artifact_exists": ["paper/submission-package.md"],
  "artifact_absent": ["paper/main.pdf"]
}
```

Use behavior evals for checkpoint language, confirmation-gate behavior, route-specific artifact
contracts, and PASS/BLOCKED wording. Keep semantic medical judgment in the review skill; use the
harness for observable behavior that can be asserted reliably.
