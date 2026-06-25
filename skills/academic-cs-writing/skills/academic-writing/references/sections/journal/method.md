# Journal Overlay: Method

Apply on top of `references/sections/method.md`. Keep the base module triad,
the pipeline-figure sketch, the overview/design/motivation/advantage templates,
and the clarity checks. Adjust for journals as follows.

## Methods Placement Is Venue-Driven

Conferences keep Method inline by default. Journals vary:

- Inline within the main text (JMLR, TPAMI, most ML transactions) — the default
  here.
- After the references with its own word allowance (Nature-style life-science
  and some multidisciplinary journals).

Read the active venue card's `Post-Main Order` before placing the section. Do not
hard-code one order. If the venue uses an after-references Methods block, plan its
budget separately from the main-text limit.

## Higher Reproducibility Bar

Journals weight reproducibility more heavily and have looser length pressure than
conferences. Details a conference would push to an appendix often belong in the
main Method or in a clearly referenced supplement:

- full hyperparameters, optimization settings, and schedules,
- exact data splits, preprocessing, and selection criteria,
- compute environment and resource cost,
- annotation or task-construction protocol for dataset/benchmark work.

Tie these to the Data Availability and Code Availability statements (see the
`academic-review` skill's `references/checks/journal-submission-elements.md`); a reproducibility claim in
Method that has no backing statement is a reviewer risk.

## Self-Contained Derivations; Long Proofs Out Of Line

Keep the main Method readable. Place long proofs and heavy derivations where the
venue expects them:

- JMLR: in appendices, placed after acknowledgments and before references in the
  same PDF.
- TPAMI: in separate supplemental files (must not be in the main PDF).
- Generic: confirm from the venue card.

State each theorem/result in the main text with a proof sketch; defer the full
proof to the venue-correct location with an explicit pointer.

## Quality Add-Ons (Journal)

In addition to the base self-check:

1. Is the Method placed per the venue's `Post-Main Order` (inline vs after
   references)?
2. Can an independent reader reproduce the work from the Method plus the named
   supplement, without missing critical settings?
3. Are long proofs/derivations in the venue-correct location with pointers, and is
   each reproducibility claim backed by a Data/Code Availability statement?
