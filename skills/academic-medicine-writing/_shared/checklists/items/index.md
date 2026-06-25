# Checklist Item Evidence Slots

These JSON files are package-local item-level evidence-slot templates for medical manuscript writing.
They use local paraphrases of official reporting-guideline items to support checklist-driven drafting
and review. They are not verbatim official checklists; the official source must still be checked
before a submission-ready claim.

Load the selected checklist card first, then load the matching item JSON:

| Study type key | Checklist card | Item JSON |
|---|---|---|
| `consort-rct` | `_shared/checklists/consort-rct.md` | `consort-2025.json` |
| `spirit-protocol` | `_shared/checklists/spirit-protocol.md` | `spirit-2025.json` |
| `strobe-observational` | `_shared/checklists/strobe-observational.md` | `strobe.json` |
| `prisma-review` | `_shared/checklists/prisma-review.md` | `prisma-2020.json` |
| `stard-diagnostic` | `_shared/checklists/stard-diagnostic.md` | `stard-2015.json` |
| `tripod-prediction` | `_shared/checklists/tripod-prediction.md` | `tripod.json` |
| `care-case-report` | `_shared/checklists/care-case-report.md` | `care.json` |
| `gather-global-health` | `_shared/checklists/gather-global-health.md` | `gather.json` |
| `cheers-health-economics` | `_shared/checklists/cheers-health-economics.md` | `cheers-2022.json` |

## Item Schema

Each item in `items[]` must include:

- `checklist`, `version`: inherited from the file header.
- `item_id`: stable local slot ID.
- `item`: compact semantic name.
- `target_section`: manuscript section or artifact where the evidence belongs.
- `required_evidence`: concrete facts the user/source material must provide.
- `status`: initial status, normally `needs_user_evidence`.
- `status_allowed`: `satisfied`, `partial`, `missing`, `not_applicable`,
  `needs_user_evidence`.
- `drafting_rule`: must forbid invention and require asking the user or inserting a precise marker.
- `blocking_if_missing`: whether the gap blocks submission-readiness.

The item list must be broad enough to function as a submission-facing checklist matrix. Do not use a
short "core items only" checklist to claim formal STROBE, CONSORT, PRISMA, STARD, TRIPOD, CARE,
GATHER, SPIRIT, or CHEERS compliance. If the package only has a compressed local checklist, name it
as a core evidence-slot screen and mark formal checklist compliance as blocked.

## Status Lifecycle

Start each row as `needs_user_evidence`. During Paper Framework and Section Drafting, update the
working checklist matrix to `satisfied`, `partial`, `missing`, or `not_applicable` only from source
evidence. Never mark an item satisfied from inference alone.
