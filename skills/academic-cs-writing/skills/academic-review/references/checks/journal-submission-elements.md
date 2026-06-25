# Journal Submission Elements

Journal-wide requirements that are not tied to a single section. Load this when
`Venue Kind: journal`, both at the **planning** stage (so the artifacts are
planned early, not bolted on after drafting) and at the final readiness check.
For empirical availability obligations, also load `data-code-availability.md`;
this file decides that the statement is required, while that workflow inventories
the artifacts and identifiers.

This file holds the journal deltas; the authoritative per-journal facts (caps,
abstract rules, post-main order) live in the active venue card. Do not invent a
journal rule — if the venue card marks a field `not verified`, ask the user or
check the author guidelines, and record it as an Open Decision.

## 1. Mandatory Statements (Plan Early)

Most journals require statements that conferences do not. Decide which apply from
the venue card and author guidelines, and reserve a place for each at planning
time. Common set:

### Data/Code Availability

Use `data-code-availability.md` for the artifact inventory, access-route ledger,
repository identifiers, and unresolved availability blockers.

| Statement | When required | Planning note |
|---|---|---|
| Data Availability | almost always for empirical work | name the repository, accession number, or DOI; **invalid or pre-publication accessions block production**, so plan real, resolvable links |
| Code Availability | when custom code is used | repository URL plus an archival DOI (for example Zenodo); JMLR links code/data externally |
| Author Contributions | many journals | confirm the format (CRediT taxonomy or free text) |
| Competing Interests / Conflicts | almost always | explicit statement even when there are none |
| Funding / Acknowledgments | when applicable | JMLR uses `\acks{}` (Acknowledgments and Disclosure of Funding) before appendices |
| Ethics / IRB / consent | human-subjects, data-collection, dual-use work | confirm the journal's required wording |
| Reporting Summary / checklist | life-sciences and some venues | filled with manuscript-level rigor; reviewers see it |
| Cover letter / editorial summary | many journals, especially high-impact targets | plan the significance, scope, and difference from prior versions without overselling |
| Graphical abstract / highlights / key points | some publishers | confirm required format, word limits, and whether they are uploaded separately |

Rules:

- Surface these at the planning stage, not after drafting.
- A reproducibility claim in Method or Abstract that has no backing Data/Code
  statement is a reviewer risk; pair the claim with the statement.
- Use `data-code-availability.md` before drafting availability text when data,
  code, source data, checkpoints, or repository identifiers are involved.
- For `journal-generic`, confirm the exact required set from the target journal's
  author guidelines before declaring readiness.

## 2. Display Items: Caps And Tiers

Journals cap and tier figures and tables differently from conferences:

- Many journals cap **figures and tables combined** (for example a 6- or 10-item
  main cap at Nature-family venues). Confirm the cap from the venue card or author
  guidelines.
- Overflow goes to a supplementary / extended tier, which is venue-specific:
  - TPAMI: separate supplemental files only (must not be in the main PDF); long
    proofs and extra results go there.
  - JMLR: appendices in the same PDF after acknowledgments and before references;
    code/data linked externally.
  - Generic: confirm the supplementary model (`not verified`).
- Decide upfront which results justify a main display item versus the supplement.
  Reviewers tolerate fewer, clearer main items better than overcrowded ones.

## 3. Methods Placement Variant

Confirm Methods placement from the venue card's `Post-Main Order`:

- Inline within the main text (JMLR, TPAMI, most ML transactions) — default.
- After the references with its own allowance (Nature-style venues).

Mismatched placement (for example an after-references Methods block where the
venue expects inline) is a format blocker. See the `academic-writing` hub's
`references/sections/journal/method.md` for the drafting-side handling.

## 4. Length And Word Budget

Journals limit by **words** or by **pages**, depending on the venue. Read the
venue card's `Length And Counting` and plan accordingly.

### The Methods-in-cap trap

When a venue's word cap **includes Methods**, budget Methods inside the cap, not
on top of it. A draft that hits the body limit and then adds a full Methods block
can land far over. Propose a per-section budget before drafting and confirm with
the user, for example for a word-capped article:

| Section | Share of cap |
|---|---|
| Introduction | ~15% |
| Results | ~40% |
| Discussion | ~15% |
| Methods (if inside the cap) | ~30% |

Adjust the split by paper type (methods-heavy vs results-heavy). When Methods sits
after references with its own allowance, budget it separately.

### Page-based venues

For page-capped venues (for example TPAMI by manuscript type), use the venue
card's page budget and remember what counts toward it (TPAMI: references and
author biographies count). Treat overflow as a blocker or an overlength-charge
decision per the venue card.

### Abstract cap

Count the abstract against the venue's abstract cap (see the `academic-writing` hub's
`references/sections/journal/abstract.md`). Over the cap is a blocker.

## 5. Reference Style And Cap

Confirm from the venue card: citation style (numeric vs author-year), reference
format, and whether there is a reference cap or whether references count toward a
page limit. Do not assume a conference reference style for a journal target.

## Readiness Mapping

When running the final check, map each element to a verdict for
`submission-readiness.md`:

- Missing a required statement that applies → `BLOCKED`.
- Display items over the venue cap, or in the wrong tier → `BLOCKED`.
- Methods placed against the venue's post-main order → `BLOCKED`.
- Body over the word/page cap (including the Methods-in-cap case), or abstract over
  its cap → `BLOCKED`.
- A required rule that cannot be confirmed because the venue card marks it
  `not verified` → `OPEN_DECISION`.
