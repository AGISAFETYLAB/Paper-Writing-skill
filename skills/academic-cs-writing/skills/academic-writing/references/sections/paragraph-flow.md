# Paragraph Flow Principles

Use this file with any section-specific guide when drafting or revising prose.

## What Flow Means

"Does my writing flow?", "does this make sense?", and "can readers understand this?" are checks for
clarity, coherence, and conciseness. Treat flow as the reader's ability to follow the paper's train
of thought without needing the author's private context.

## Reader Perspective Check

Read the draft as an external reader who is not familiar with the topic, not as the author who built
the work. Ask:

1. Is the vocabulary understandable for the target research audience?
2. Do body paragraphs connect back to the section thesis, and is the connection easy to see?
3. Could someone outside the immediate project understand what the paragraph is trying to say?

If the author starts losing sight of the train of thought, assume readers will be confused and
revise the paragraph order, topic sentence, or support.

## One Paragraph, One Message

Each paragraph should have one clear message: one paragraph, one message. The first sentence should usually state the paragraph
role or claim.

## Salience And Compression

Good prose is not "everything that is true about the work"; it is the **load-bearing** subset,
ordered and weighted by importance. Most messy, unfocused drafts fail here, not at grammar.

**Lead with the point.** A paragraph's skeleton is: first sentence = the point (claim/result/decision),
middle = support, last = reinforcement or transition. **Never bury the key sentence in the middle.**
If the first sentence could be deleted without the reader losing the paragraph's purpose, rewrite it.

**Allocate length by importance, not by availability.** Spend words in proportion to how much a piece
of content supports the paper's claims. Novel, surprising, or claim-supporting content earns its own
paragraph; routine setup earns a clause; content that supports no claim is cut. Do not give an
unimportant fact a full sentence just because it is true.

**Do not enumerate in the body.** Inventories, taxonomies, per-category counts, exhaustive option
lists, and "one item per line" content do **not** belong in running text. In the body, *mention them
in one stroke* — name the dimension, give the total, and call out only the **few salient or novel
members** — then send the **full list to a table or the appendix**. Reasons to put a list in the
body must be argumentative, never completeness:

- ❌ Listing every category `V1…Vn` / `H1…Hn` with its definition and task count in the body.
- ❌ Making a subsection whose main content is a glossary-style itemize/enumerate list
  (`V1 -- Email: ...`, `H1 -- Phishing: ...`). This is still enumeration even when no counts appear.
- ✅ "We define `n` categories spanning `<short span>`; two are novel (`Ck`, `Cj`, motivated
  below). The full taxonomy with per-category counts is in Table/Appendix X."

For taxonomy sections, the prose job is **argument and design logic**, not dictionary coverage:
why this axis is needed, how the categories separate failure modes, what is novel or surprising, and
which table/appendix carries the complete definitions. If every category receives a sentence of the
same shape, the section has failed the salience test.

**Every number must carry a point.** A statistic in prose must support a claim (a total, a dominant
or surprising share, a headline coverage figure). Numbers that merely report "how much of each kind"
go in a table; never transcribe a table into sentences.

**The "so what?" test.** For each paragraph, sentence, or list, ask: if I delete this, does any claim
weaken? If not, compress it to a clause or cut it. Compress by removing repeated background,
collapsing redundant statements, and keeping only the one or two most decision-relevant points —
never by deleting the actual claim or its key evidence.

### Before / After (enumeration)

Before (body text, unfocused — full inventory inline):

```text
We define 8 categories. C1 -- Source A: ... 20 items. C2 -- Source B: ... 16 items.
C3 -- Source C: ... 21 items. [... five more bullets ...]
```

After (body text, one stroke + pointer; full list moved to a table/appendix):

```text
The benchmark spans 8 categories, from common input conditions to two newly introduced stress
conditions. Table~\ref{tab:categories} lists all categories with per-category item counts.
```

## Before Drafting

Create a `Paragraph Plan` before writing prose. First list the key points as bullet points, then
order them by dependency (what must the reader understand first?). Convert the ordered bullets into
paragraphs, one per message.

| Paragraph | Role | Message | Evidence / Source | Risk |
|---|---|---|---|---|

The plan should make the section thesis visible and prevent mixed-message paragraphs.

## Sentence-Level Rules

- **Keep sentences short.** If a sentence spans more than three clauses, split it.
- **Concrete before abstract.** State the specific finding or design first, then generalize.
  Avoid opening with abstract claims the reader hasn't been prepared for.
- **Avoid jargon when plain words work.** Use technical terms only when they carry precise
  meaning needed for the argument.
- **Prefer active voice for your own work.** "We propose / We evaluate / We find." Passive
  voice is acceptable for describing existing work or objective experimental outcomes.
- **Avoid ambiguous relative pronouns.** Replace bare "this / these / that / which" with
  explicit noun phrases: "this method / this result / this limitation / these baselines."
  The reader must never guess what a pronoun refers to.

## Continuation Markers

At the start of each section and subsection, tell the reader what follows and how it connects
to the contribution or previous section. These markers act as re-entry points for skim readers
and reviewers. Example: "Having established the benchmark design, we now evaluate each baseline
against the three criteria defined in §2."

## Headings And Sections As Flow Check

When a complete outline is hard to produce, use temporary sections and subsections with headings as
a drafting and revision diagnostic. Headings expose the main parts of the paper, show how those
parts work together, and tell the reader what each part is about. Keep only headings that help the
final paper's argument; remove scaffolding headings that were useful only during revision.

## Sentence-To-Sentence Flow

Every sentence should connect to the previous sentence through one of these relations:

- cause,
- contrast,
- consequence,
- refinement,
- example,
- evidence.

If the relation is unclear, revise the transition or split the paragraph.

## Transition Cues

Use transition cues when the logical relation between sentences or paragraphs is not already clear.
Do not stuff transitions into every sentence; choose the cue that names the actual relation:

| Relation | Useful cues |
|---|---|
| cause and effect | accordingly, as a result, because, consequently, hence, so, then, therefore, thus |
| comparison | also, in the same way, likewise, similarly |
| contrast or exception | although, but, even though, however, in contrast, instead, nevertheless, nonetheless, on the contrary, on the one hand ... on the other hand, still, yet |
| example | even, for example, for instance, indeed, in fact, of course, such as |
| place or position | above, adjacent to, below, beyond, finally, furthermore, last, moreover, next, too |
| time | after, as soon as, at first, at the same time, before, eventually, finally, immediately, later, meanwhile, next, simultaneously, so far, soon, then, thereafter |
| summary or conclusion | as a result, as we have seen, finally, in a word, in any event, in brief, in conclusion, in other words, in short, in the end, in a final analysis, on the whole, therefore, thus, to summarize |

## Reverse Outline Check

After drafting a section, write:

1. section thesis or thesis statement,
2. each paragraph topic sentence,
3. main points of evidence or explanation under each paragraph,
4. evidence mapping from paragraph to source or experiment,
5. mapping from paragraph to section thesis.

Check that every topic sentence clearly relates to the section thesis and that every point of
evidence or explanation supports the paragraph topic. If a paragraph does not map cleanly, revise it or remove it.
If the reverse outline is hard to create, the section thesis, topic sentences, or supporting points
are probably unclear.

## During Revision

Revise paragraph-by-paragraph. For each paragraph, preserve supported claims, weaken unsupported
claims, and keep one role per paragraph. If one paragraph contains multiple roles, split it.

Required revision note:

| Paragraph | Original role | Revised role | Main change | Reason |
|---|---|---|---|---|

## Term Consistency

Define important terms before reuse. Keep names stable across the paper unless the Writing Policy
explicitly changes terminology.

## Self-Check

- Does this paragraph have one message?
- Is the first sentence doing the right job (the point, not buried)?
- Is length allocated by importance — no full sentence wasted on a non-load-bearing fact?
- Are inventories/taxonomies/per-category counts mentioned in one stroke with the full list in a
  table or appendix, rather than enumerated in the body?
- Does every number in prose support a claim, instead of transcribing a table?
- Are nouns self-contained for an external reader?
- Does each sentence have a visible relation to the previous one?
