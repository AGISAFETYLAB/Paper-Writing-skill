# Journal Results Overlay

Load this after `references/sections/experiments.md` when `Venue Kind: journal`
and the empirical evidence section is being drafted or revised. This overlay
changes the presentation posture; it does not replace the base rigor rules.

## Results narrative, not a conference dump

For journal articles, the empirical section should read as
`research questions -> findings -> evidence -> interpretation`, not as a list of
leaderboard tables followed by isolated ablations.

Use the base **Experiments / Evaluation** guide for evidence adequacy:
comparisons, controls, ablations, stress tests, failure cases, metric semantics,
and table/figure evidence roles still apply. The journal overlay adds three
requirements:

1. Start each major block with the finding or research question it resolves.
2. Pair each key result with interpretation: what the result means for the
   article's central claim, not only whether the number is higher.
3. Carry limitations and boundary conditions next to the relevant findings, or
   defer them to the dedicated Discussion / Limitations location required by the
   active venue.

## Naming And Section Role

Do not rename every empirical section to Results automatically. The active paper
type profile and venue card still control section naming.

- Use **Results** when the journal/paper type expects a finding-led article.
- Use **Experiments** or **Evaluation** when the field journal expects an ML/CS
  evaluation section, but write it with journal-level interpretation.
- Use **Results and Analysis** when the section owns both evidence and the
  meaning of that evidence.

When a conference-style draft is being extended to a journal article, keep the
evidence package but reorganize the prose so the reader sees complete findings,
not only experiment names.

## Display Items

Journal Results sections usually need fewer, stronger main display items:

- one main result or finding figure/table per load-bearing claim,
- supporting controls and robustness checks in appendix/supplement unless they
  are central to the claim,
- captions that state the conclusion and the evidence boundary.

Display design, span, caption mechanics, table overflow, export, and QA remain
owned by `academic-figure`.

## Checklist

- Does each Results block answer a research question or state a finding first?
- Is every main display item tied to a claim from the Writing Policy or Paper
  Framework?
- Are ablations interpreted, not merely reported?
- Are scope boundaries and negative findings placed where reviewers will see
  them?
- If the section is still named Experiments / Evaluation, does the prose still
  carry journal-style interpretation?
