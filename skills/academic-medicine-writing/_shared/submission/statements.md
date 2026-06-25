# Medicine Statements And Submission Package

Medical manuscripts usually need more than a main PDF. Plan each item early.

| Item | Required when | Do not invent |
|---|---|---|
| Ethics / IRB approval | human participants, patient data, biological samples | committee name, approval number |
| Consent | identifiable patient data, case reports, images, interventions | consent wording or waiver |
| Trial registration | clinical trial, intervention study, protocol | registry, registration ID, date |
| Protocol / SAP availability | RCT, protocol, many clinical studies | protocol location |
| Data availability | all empirical studies | repository DOI, accession, access committee |
| Competing interests | most journals | financial relationships |
| Funding | most journals | grant numbers |
| Author contributions | most journals | CRediT roles |
| Completed checklist | most medical article types | item status |
| ICMJE authorship approval | journal submission package | all-author approval |
| ORCID | title page / editorial system when required | author identifiers |
| Permissions | reused figures, tables, questionnaires, images | permission status |
| Suggested reviewers | optional or journal-requested submission metadata | names, affiliations, emails |
| Previous submission or reviewer comments | resubmission or transferred submission | prior decision history |

Submission package plan format:

| File / statement | Status | Source evidence | Required action |
|---|---|---|---|

For data/code availability, load `_shared/submission/data-availability.md` and complete the Data
Availability And FAIR Audit before submission-ready wording. Unknown repository identifiers,
controlled-access procedures, third-party restrictions, DataCite metadata, or figure source data
must remain `user-needed` or `blocking`.

Editorial-system checklist items such as `cover-letter.md`, `title-page.md`, and
`editorial-system-checklist.md` are submission artifacts, not manuscript science. Draft them only
from provided facts. Unknown author identities, ORCID values, permissions, suggested reviewers, or
previous submission history must remain `user-needed` or `blocking` rather than being filled from
inference.

## Status Vocabulary

Use only these statuses:

- `provided`: source text or identifier is present.
- `unknown`: source material does not provide the fact.
- `not applicable`: study type or target journal does not require it.
- `user-needed`: the author must supply the fact before submission.
- `blocking`: the manuscript cannot be called submission-ready without it.

## Drafting Rules

- Write statement prose only from provided facts.
- Use neutral placeholders such as `[AUTHOR: provide IRB approval number]` only in drafts, and list
  them as unresolved in `paper/submission-package.md`.
- Never convert an unknown into "not applicable" for convenience.
- If ethics, consent, trial registration, data sharing, or conflicts are unknown for a target that
  requires them, the final review verdict cannot be PASS.
