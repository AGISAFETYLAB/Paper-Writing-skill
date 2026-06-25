# Finance Writing Craft Gate

Use this reference when drafting, revising, auditing, or approving finance manuscript prose. It is
the gate-level companion to `prose-style.md` and `references/sections/index.md`: those files control
prose rhythm and section formulas; this file controls whether the argument is publication-facing
enough to advance.

## Contribution And Belief-Update Gate

Before Writing Policy approval, record a one-sentence contribution contract:

```text
This paper changes what finance/economics readers believe about <object/relation/mechanism> by
showing <finding> using <data/model/design>, relative to <closest benchmark literature or prior
belief>.
```

The contract is not a slogan. It must identify:

- the finance object or friction;
- the closest benchmark literature, institution, model, or empirical belief;
- what changes in reader belief;
- the evidence source that makes the update credible;
- whether the contribution is data, identification, mechanism, theory, measurement, external
  validity, or synthesis.

Set `belief_update_status` to `pass`, `partial`, or `blocked`. Block stronger contribution language
when the paper only says that it studies an important topic, uses a new sample, fills a gap, or
contributes to the literature without saying what belief changes.

## Paragraph Evidence Contract

Every central paragraph in the abstract, introduction, results, mechanisms, robustness, and
conclusion should have one message:

1. economic claim or question;
2. data/model/design anchor;
3. estimate, spread, comparative static, or qualitative result when available;
4. uncertainty, benchmark, or identifying comparison;
5. economic interpretation or limit.

If one of these fields is missing from source materials, keep the sentence conservative and record
the missing field as `needs_user_evidence`. Do not invent estimates, robustness, citations, data
permissions, or mechanism tests to make a paragraph feel complete.

## Results Narrative Gate

Do not write a table tour. A results subsection should start with the economic conclusion, then
explain the evidence:

1. headline result and economic magnitude;
2. display reference and sample/model boundary;
3. uncertainty and benchmark or omitted group;
4. robustness threat addressed by the next specification;
5. interpretation, limitation, or next mechanism test.

Record `results_narrative_status` as `pass`, `partial`, or `blocked` in the Paper Framework and
submission package. Block results prose that begins with "Table X reports", lists coefficients
without interpretation, treats statistical significance as economic significance, or repeats the
same key result in both a table and figure without a distinct evidence role.

## Mechanisms, Heterogeneity, And Robustness

Mechanism and heterogeneity tests must have theory -> observable implication -> test. Do not list
many subsamples merely because they are available. For each mechanism, heterogeneity split, placebo,
or robustness check, record:

- which alternative explanation or channel it addresses;
- why the variable/split/test is theoretically motivated;
- what result would support or weaken the mechanism;
- whether multiplicity, power, or sample-size limits make the result only suggestive.

Null results are usable only when the confidence interval, power, or model precision makes the lack
of an economically meaningful effect interpretable.

## Title-Abstract-Introduction Scorecard

Use this scorecard before approving Paper Framework and again during final review:

| Item | Pass condition |
|---|---|
| Title | names the finance object/relation/friction, not only the method |
| Abstract | states question, data/model/design, finding with magnitude, and belief update |
| Introduction | shows the main result in the first three paragraphs |
| Contribution | says what belief changes relative to closest work or prior view |
| Literature positioning | groups closest papers by what remains unresolved |
| Roadmap | tells the reader what each section proves, not just where sections appear |

Record `writing_craft_status` as `pass`, `partial`, or `blocked`. A compiled PDF, clean citations,
and attractive tables do not override a blocked scorecard.

## Prose Lint Gate

Run `scripts/lint_finance_prose.py` on `paper/` for full drafts and submission-review packages when
editable text exists. The script catches static warning signs: banned AI phrase, empty contribution
phrase, causal language without identification cue, significance without magnitude cue, and table
tour sentence. Treat lint findings as review blockers unless the submission package records a
reasoned waiver for a false positive.
