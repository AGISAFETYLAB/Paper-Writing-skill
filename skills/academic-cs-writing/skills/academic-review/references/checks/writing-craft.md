# Writing Craft Check

Use this file during final full-paper review or when the user asks for a
writing quality audit. Do not load it during routine section drafting.

Run each check against the complete draft. Mark passed, fix needed, or
not applicable.

## Language And Clarity

| Check | What to look for |
|---|---|
| Sentences short and clear | No sentences spanning more than 3 clauses. Logic easy to follow on first read. |
| Concrete before abstract | Specific findings or designs stated before generalizing. No abstract claims without preparation. |
| Jargon controlled | Technical terms only when they carry precise meaning. Plain words preferred otherwise. |
| Active voice for own work | "We propose / evaluate / find." Passive voice only for existing work or objective outcomes. |
| No ambiguous pronouns | No bare "this / these / that / which." Every pronoun has an explicit noun phrase: "this method / this result / this limitation." |

## Structure And Flow

| Check | What to look for |
|---|---|
| One idea per paragraph | Each paragraph has a single clear message. Split paragraphs that mix roles. |
| Continuation markers present | Each section and subsection opens with a sentence telling the reader what follows and how it connects to the contribution. |
| Paragraphs ordered by dependency | Reader understands each paragraph before needing the next. No forward references to undefined concepts. |
| Introduction roadmap (optional) | Not required for conference papers; the default conference Introduction has no roadmap. Only expect a short "rest of this paper" navigation paragraph when the venue or paper structure calls for it (most often journals — see the journal Introduction overlay). |

## Claim Calibration

Calibrate the strength of every claim to the strength of its evidence. Reviewers read overclaiming
as a soundness problem, not a style problem.

### Verb-to-evidence ladder

| Evidence available | Allowed verbs | Avoid |
|---|---|---|
| Strong direct evidence (controlled comparison, full ablation, statistically clear gap) | `show`, `demonstrate`, `establish`, `prove` (only for formal proofs) | — |
| Trend-level, partial, or indirect evidence | `suggest`, `indicate`, `point to`, `is consistent with` | `show`, `demonstrate`, `prove` |
| Plausible but unverified mechanism or interpretation | `may`, `could`, `we hypothesize`, `we conjecture` | any assertive verb |
| No evidence in this paper | state as open question, future work, or delete | any claim verb |

Match the verb to the weakest link in the support chain, not the best single result. If a headline
claim rests on one dataset or one seed, bound it ("on X" / "in this setting") instead of using a
universal verb.

### Universal-claim and novelty sweep

Sweep the full draft (especially Abstract, Introduction, Conclusion) for these words and either
bound them with evidence or remove them:

`first`, `the first to`, `novel` (when used as the proof of contribution), `unique`,
`unprecedented`, `comprehensive`, `complete`, `fully`, `entirely`, `always`, `never`, `any`,
`all`, `guarantees`, `optimal`, `best`, `state-of-the-art` (without a named comparison).

| Pattern | What to look for | Fix |
|---|---|---|
| Priority claim (`first to ...`) | Is the scope narrow enough to be defensible, and is prior work actually surveyed? | Add the precise scope and a difference-from-prior-work sentence, or drop the priority framing. |
| Universal quantifier (`always`, `all`, `never`, `any`) | Does the evidence cover every case implied? | Replace with the tested range, or weaken to `typically`, `in our experiments`, `for the settings we evaluate`. |
| Superlative (`best`, `optimal`, `state-of-the-art`) | Is there a named, fair comparison that supports it? | Name the comparison and metric, or downgrade to `competitive` / `improves over`. |
| Completeness (`comprehensive`, `complete`, `fully`) | Does the paper actually cover the whole space? | Scope it to what was covered, or remove the adjective. |

Do not delete a contribution claim that the evidence supports; only bound the claims the evidence
does not reach.

## Contribution Integrity

| Check | What to look for |
|---|---|
| Contribution stated early | Abstract and Introduction explicitly state the contribution. |
| Every section serves the contribution | No background, method descriptions, or experiments unrelated to the core contribution. Remove or move to appendix. |
| Difference from prior work explicit | At least one paragraph (normally in Related Work) states at a high level how this paper differs from the closest prior work. This positioning is not required as a dedicated Introduction section. |

## Prose Hygiene

| Check | What to look for |
|---|---|
| No footnotes | Replace every `\footnote{...}` with inline parenthetical text or move the content into the main body. CS/ML conference papers should not use footnotes; they distract readers and are often missed by reviewers. If the footnote content matters, it belongs in the text. If it does not matter, delete it. |
| No file names or code artifacts in prose | Replace `\texttt{filename.ext}` with descriptive natural language. For example, write "the benchmark manifest" instead of `\texttt{BENCHMARK_MANIFEST.json}`, "the released evaluation script" instead of `\texttt{compute_asr.py}`. File names, script names, and code identifiers are implementation details that break the reader's attention. |
| No local paths or directories in prose | Remove any local filesystem paths, directory names, or repository-relative paths from prose. These are artifacts of the author's development environment and have no place in a published paper. |

## Copyedit and Language

The sentence-level language standard is defined in the `academic-writing` hub's
`references/style/copyediting-standard.md` and is applied while writing. This is the terminal verification pass for the items that
most often drift during generation; do not restate the full standard here. Confirm on the
finished draft (several are grep-checkable on the LaTeX source):

| Check | What to look for |
|---|---|
| No contractions | No `it's`, `don't`, `doesn't`, `we'll`, `isn't`, etc. in prose. Expand all. |
| No possessive `'s` on names | No `METHOD's` / `the model's`. Use `the performance of METHOD`, a noun modifier, or passive. |
| Common abbreviations kept | `LLM`, `RAG`, `GPU`, etc. not expanded. |
| LaTeX preserved | Every `\cite`/`\ref`/`\eg`/`\ie`/emphasis command from the source is intact. |
| No emphasis added | No `\textbf`/`\emph`/`\textit` introduced that the source did not have. |
| No list-ification | Paragraphs not rewritten into `itemize`/`enumerate`. |
| Zero errors | No spelling, grammar, punctuation, or article errors. |
