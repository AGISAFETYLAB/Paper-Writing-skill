# JMLR Venue Profile

## Venue Kind

- journal

## Source Status

- Official sources:
  - JMLR Formatting Instructions: https://www.jmlr.org/format/format.html
  - JMLR Author Information: https://www.jmlr.org/author-info.html
  - JMLR Authors Guide: https://www.jmlr.org/format/authors-guide.html
  - Official style file: https://raw.githubusercontent.com/JmlrOrg/jmlr-style-file/master/jmlr2e.sty
- Access date: 2026-06-09
- Verified for: JMLR regular article and Open Source Software (OSS/MLOSS) track submission planning.
- Drift risk: medium; verify the current author information page before submission.

## Scope

- Applies to: JMLR full research articles and JMLR OSS/MLOSS software papers.
- Submission version: review submission; the action editor assigns final volume, pages, and dates for the published version.

## Length And Counting

- Layout: single column, 11pt, `jmlr2e` style.
- Main text limit: no hard page limit; the standard is "concise and complete". Do not pad; do not inflate.
- References count: not page-limited.
- Appendix count: no separate limit; appendix is placed at the very end of the same PDF.
- Abstract limit: not a hard word cap; keep it short, single-block, and self-contained.
- OSS track: software papers are short (~8 pages); keep the design and usage focus tight.
- Supplementary material count: code/data linked externally; authors maintain the links.
- Word budget: JMLR is length-by-evidence, not word-capped, so the Methods-in-cap trap does not apply. Still propose a proportional per-section budget before drafting to avoid padding. See the `academic-review` skill's `references/checks/journal-submission-elements.md` (Length And Word Budget).

## Blinding

- Single-blind / non-anonymous. Author names, affiliations, acknowledgments, and self-citations appear in the submission. The skill may reference the authors' own prior work directly.

## Revision Model

- Action-editor-managed review with revision rounds; an `\editor{...}` command is required and the `\jmlrheading` carries submitted/revised/published dates.
- No anonymized rebuttal phase like conferences; write for a thorough, multi-round review rather than a single-shot decision.
- No camera-ready page-limit crunch; final version is the complete article.

## Supplementary And Extension

- Source code and data are linked rather than embedded; reproducibility is expected and weighted.
- For a paper extended from a conference version, state the new contribution over the prior version explicitly; JMLR expects substantial new content.
- See `journal-vs-conference.md` for the journal drafting posture (complete story, thorough evaluation, written to survive multi-round review).

## Post-Main Order

- Required order: main body, Acknowledgments and Disclosure of Funding (`\acks{}`), appendices, then references.
- Optional sections: appendices (placed at the very end of the same PDF, titled "Appendix").
- Not verified: any track-specific front-matter beyond title, author, editor, abstract, and keywords.

## Drafting Implications

- Do not apply a conference page budget. Plan a complete, self-contained article and let evidence and clarity set the length.
- Theory papers must also discuss practical utility; system/tool papers must describe the underlying principles, not only the implementation (per JMLR author info).
- Keep the abstract a single concise block; put keywords in the `keywords` environment.
- Place all appendices after acknowledgments and before references in the same PDF; long proofs and extra experiments go there.
- Fill author and editor blocks; this venue is not anonymous.

## Final Gate

- Before submission-ready: confirm the current JMLR author information page, compile with the official `jmlr2e.sty` via latexmk/pdflatex, verify `\jmlrheading`/`\ShortHeadings`/`\editor` are correctly filled, confirm references are complete and in natbib format, and confirm code/data links resolve.

## Do Not Infer

- Do not infer acceptance bar, reviewer tastes, or topical scope from this profile.
- Do not invent volume, page, or date values; the action editor assigns them.
