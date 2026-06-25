# ACL Venue Profile

## Venue Kind

- conference

## Source Status

- Official sources:
  - ACLPUB Paper Formatting Guidelines: https://acl-org.github.io/ACLPUB/formatting.html
  - ACL Rolling Review Author Guidelines: https://aclrollingreview.org/authors
  - ACL 2026 Main Conference CFP: https://2026.aclweb.org/calls/main_conference_papers/
- Access date: 2026-06-08
- Verified for: ACL-style review submissions using current ACLPUB formatting plus ACL 2026 planning.
- Drift risk: medium; verify the target conference call and ARR requirements before submission.

## Scope

- Applies to: ACL-family review submissions when the target uses ACLPUB and ARR-style policies.
- Submission version: review submission; camera-ready deltas must be rechecked.

## Length And Counting

- Main text limit: long papers up to 8 content pages; short papers up to 4 content pages.
- References count: no.
- Appendix count: no, but appendices are optional for reviewers and the main paper must be self-contained.
- Checklist count: target-year responsible NLP checklist handling is not verified in this card.
- Ethics/limitations count: `Limitations` and optional ethical considerations are outside the main content page limit under ACLPUB formatting guidance.
- Supplementary material count: not verified; treat as optional support.

## Post-Main Order

- Required order: main content, `Limitations`, optional ethical considerations, references, appendices.
- Optional sections: ethical considerations, appendices, supplementary material.
- Not verified: target-year checklist submission mechanism and exact disclosure-section placement.

## Required Limitations Section (enforced)

- A dedicated `\section{Limitations}` is **required** for ACL submissions and is the single home for
  all limitations. Plan it in the Paper Framework, place it after Conclusion and before References.
- Limitations must NOT appear as a `\textbf{Limitations …}` run-in, `\subsection`, or `\paragraph`
  inside Experiments or any other body section, and must not be re-listed in the Conclusion. A
  misplaced or duplicated Limitations unit is a blocking defect (`scripts/audit_draft.py` flags it).
- Because `Limitations` and ethical considerations sit outside the 8/4-page content budget, moving a
  stray limitations block into the dedicated section both fixes placement and reclaims page budget.
  The page audit (`audit_draft.py --max-content-pages 8`/`4`) counts content only up to the first
  post-matter heading, so a correctly placed Limitations section is excluded automatically.

## Drafting Implications

- Select long or short paper before page budgeting; use 8 or 4 content pages for review drafts.
- Keep limitations outside the main content page budget when the official ACL formatting rule applies.
- Put appendices and supplementary details after references, and keep the main paper self-contained.
- Add checks for title/abstract plain-text metadata, A4 output, line numbers, and DOI or ACL Anthology links where possible.

## Final Gate

- Before submission-ready: confirm the current target call, ARR policy, style files, paper length, post-main order, checklist handling, anonymity, citation style, and abstract length.

## Do Not Infer

- Do not infer ACL-specific topical or reviewer preferences from this profile.
