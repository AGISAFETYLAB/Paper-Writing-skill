# Journal Overlay: Abstract

Apply on top of `references/sections/abstract.md`. Keep the base pre-writing
questions, the Challenge/Insight/Contribution templates, and the quality
checklist. Adjust for journals as follows.

## Respect The Venue Abstract Cap (Hard Constraint)

The base guide is length-agnostic. Journals usually impose a hard abstract cap.
Read the active venue card's `Length And Counting` → `Abstract limit` first and
treat it as a gate:

- IEEE TPAMI: one paragraph, 150-250 words, **no citations, no numbered equations**.
- JMLR: a single concise self-contained block (no hard word cap, but do not pad).
- Generic journal: `not verified` — confirm the word/character cap and whether the
  journal mandates a **structured** abstract before drafting.

If the drafted abstract exceeds the venue cap, it is a blocker, not a stylistic
preference. Count words against the cap before returning the draft.

## Single Unstructured Paragraph By Default

Default to one unstructured paragraph. Only use a **structured abstract**
(Background / Methods / Results / Conclusions headings) when the target journal
explicitly requires it — confirm from the venue card or author guidelines, do not
invent the format.

## No Citations, Self-Contained Terminology

For most journals (TPAMI explicit), the abstract carries no citations and no
reference markers. Spell out abbreviations at first use; the abstract must read
standalone because editors triage on it.

## Lead With The Finding, Attach Numbers

Editors and reviewers decide relevance from the abstract. Lead with the
contribution or finding, then support it. Where evidence exists, attach
quantitative results to the strongest claim (for example "X% improvement on N
benchmarks", not "significant improvement"). This refines, not replaces, the base
Challenge → Contribution movement.

## Choosing The Movement For The Venue

- Field journals (JMLR, TPAMI, most ML transactions): keep the base
  Challenge → Insight → Contribution templates, tightened to the cap and the
  no-citation rule. Reviewers are specialists; technical framing is expected.
- Broad-audience / high-impact venues: shift toward a **significance / summary
  paragraph** movement so a reader outside the subfield can follow:
  `broad field need → sharper background → exact unresolved gap → here we show
  → what the result changes → bounded significance`. Make the first one or two
  sentences survivable for a non-specialist; reserve one explicit gap sentence;
  let the main result arrive by the middle; spend more space interpreting the
  result than naming method steps; end on bounded significance, not a slogan.

Pick exactly one movement based on the venue, the same way the base guide picks a
template version internally.

## Abstract Quality Add-Ons (Journal)

In addition to the base checklist:

1. Is the abstract within the venue's word/character cap?
2. Is it free of citations and undefined abbreviations (if the venue requires)?
3. Does the first sentence carry the finding or significance, not just background?
4. For broad-audience venues, could a reader from an adjacent field follow the
   first two sentences?
