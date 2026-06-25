# Journal vs Conference Drafting Posture

Load this file when the confirmed `Venue Kind` is `journal`. It captures how journal drafting differs
from conference drafting. It is a writing-posture reference only: it does not set absolute length
(the venue card does) and does not change the paper identity, claims, or evidence.

This file pairs with the journal paper-type files under `_shared/paper-types/journal/`. The
paper-type file controls section structure and proportional budget; this file controls tone, scope,
and what reviewers expect across a multi-round review.

Two companions carry the journal deltas that are not covered here:

- Section-level journal adjustments: the `academic-writing` hub's `references/sections/journal/`
  overlays (Abstract,
  Introduction, Method, Discussion/Conclusion). Load the base section guide first, then the
  matching overlay. See the `academic-writing` hub's `references/sections/journal/index.md`.
- Journal-wide submission requirements: the `academic-review` skill's `references/checks/journal-submission-elements.md`
  (mandatory statements, display-item caps and tiers, methods placement, word/length budget). Plan
  these at the planning stage, not after drafting.

## The core difference

- A conference paper is usually "one novel contribution, told clearly within a hard page limit."
- A journal paper is usually "a complete, self-contained story with thorough evidence, written to
  survive a multi-round review."

Most structural differences below follow from that one difference.

## What changes

### Completeness and scope
- Tell the whole story, not just the novel nugget. Include the evidence a skeptical reviewer needs
  to accept the central claim without a follow-up paper.
- More thorough evaluation is expected: fuller ablations, robustness checks, failure analysis,
  and (where relevant) cost/efficiency characterization.
- Related Work can be more comprehensive than in a short conference paper; a journal reader expects
  a fair, current map of the area.

### Length and budget
- Do not apply a conference soft page budget. Use the venue card for absolute length:
  - JMLR: no hard page limit; "concise and complete" — let evidence and clarity set the length.
  - TPAMI: double-column manuscript-type limits (Regular 12-18 with MOPC, Survey 20, Short 8),
    references and biographies included.
- Plan section sizes as proportions first, then fit them to the venue's absolute budget.

### Anonymity and self-reference
- Standard journal tracks here are single-blind / non-anonymous. Author identity, affiliations,
  acknowledgments, and self-citations appear in the submission.
- You may refer to the authors' own prior work directly ("our previous work", named systems).
- Still verify the current policy; some journals pilot double-blind options.

### Review cycle
- Write for major/minor revision rounds, not a single-shot decision. A response-to-reviewers
  letter is expected at revision (the skill writes the paper, not the letter, unless asked).
- Leave the structure able to absorb added experiments or clarifications without a full rewrite.
- There is no conference-style camera-ready page crunch; the accepted layout governs final length.

### Supplementary material and reproducibility
- Supplementary material is generally allowed as separate files (TPAMI: separate files, no page
  limit; JMLR: code/data linked externally). Move long proofs, extra tables, and extended results
  there rather than inflating the main text.
- Reproducibility (code, data, settings) is weighted; make access explicit.

### Conference-to-journal extension
- If the paper extends a prior conference version, state the new contribution over that version
  explicitly. Journals expect a substantial, non-trivial extension (often informally ~30%+ new
  material); confirm the specific journal's policy in the venue card or author guidelines.

## What does NOT change

- Paper identity, core claims, the evidence boundary, and key terminology are fixed by the user's
  research, not by the venue. Journal posture changes thoroughness and framing, never the facts.
- Integrity rules still apply: unsupported claims are weakened or marked `needs evidence`, never
  strengthened to look more complete.

## Checklist before drafting a journal paper

- Confirmed venue card loaded and `Venue Kind: journal`.
- Absolute length taken from the venue card, not from a conference budget.
- Journal paper-type file selected from `_shared/paper-types/journal/`.
- Decided what belongs in main text vs supplementary material.
- For an extended paper: the delta over the conference version is stated.
- Mandatory statements (data/code availability, contributions, conflicts, funding, ethics) planned
  from the `academic-review` skill's `references/checks/journal-submission-elements.md`.
- Section overlays under the `academic-writing` hub's `references/sections/journal/` queued for
  Abstract, Introduction, Method, and Discussion/Conclusion drafting.
