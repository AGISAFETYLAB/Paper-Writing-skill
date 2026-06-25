# Generic-review Route

Use when the target journal, article type, or accepted source format is unresolved.

This route is not submission-ready.

## Required Production Artifact

The primary review artifact is `paper/manuscript.md`. This route may include figures, tables,
references, title page, editorial checklist, and `paper/submission-package.md`, but it is not
submission-ready.

## Assembly Requirements

- Label the target journal and template status as unresolved.
- Do not create the impression that a generic shell satisfies a target journal.
- Keep checklist, statement, citation, data availability, and display blockers visible.
- Use route-neutral manuscript structure until the exact target journal or submission format is
  confirmed.

## PASS Gate

There is no submission-ready PASS for this route. Record a reviewable package status only:

- `format-specific production gate: BLOCKED` or `generic-review package: reviewable`;
- primary file: `paper/manuscript.md`;
- unresolved target journal and format decisions;
- concrete next decision needed to move to `word-first` or `latex-first`.
