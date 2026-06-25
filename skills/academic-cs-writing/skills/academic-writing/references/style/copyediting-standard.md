# Copyediting and Language Standard

The single source of truth for sentence-level English style when drafting or polishing
prose. Apply it **while writing or revising** (it shapes every sentence), and verify the
mechanical subset again in the final review. This standard governs *how* text is written;
it never changes the research content, claims, or evidence (see `_shared/core/contract.md`).

When a rule here would force a change to meaning, results, or claims, do not apply it
silently — keep the wording bounded and flag it, per the writing-only scope.

## 1. Rigor and sentence craft (the core task)

- **Formality and rigor**: shape sentences to match top-tier conference writing — formal
  register, explicit logical connectives, and coherent sentence-to-sentence flow.
- **Sentence polishing**: rewrite long or convoluted sentences so they read smoothly;
  remove stiff or unidiomatic phrasing typical of non-native drafting, without changing
  the technical meaning.
- **Zero-error principle**: fix every spelling, grammar, punctuation, and article (a / an
  / the) error.

## 2. Vocabulary and register control

- **Formal written register only.** Never use contracted forms. Always expand them:
  `it is` not `it's`, `does not` not `doesn't`, `cannot` is acceptable, `do not` not
  `don't`, `we will` not `we'll`, `is not` not `isn't`.
- **Simple and clear vocabulary.** Do not pile on ornate or obscure words. Use common,
  widely understood scientific vocabulary so the text stays clear and concise. Prefer the
  plain word over the fancy synonym (`use` over `utilize`, `show` over `elucidate`).
- **Avoid the possessive `'s`, especially on method, model, or system names.** Use an
  `of`-construction, a noun modifier, or a passive form instead:
  - `the performance of METHOD` — not `METHOD's performance`
  - `the output of the model` / `the model output` — not `the model's output`
  - `the accuracy of the system` — not `the system's accuracy`

## 3. Content and formatting preservation

- **Keep common domain abbreviations as-is.** Do not expand well-known acronyms: keep
  `LLM`, `RAG`, `GPU`, `API`, `MLP` unexpanded (unless the draft itself defines them on
  first use and the user asks to follow that convention).
- **Preserve LaTeX commands verbatim.** Do not alter, drop, or reformat commands such as
  `\cite{}`, `\citep{}`, `\citet{}`, `\ref{}`, `\eqref{}`, `\label{}`, `\eg`, `\ie`,
  `\textbf{}`, math, or environments. Edit the surrounding prose, not the commands.
- **Inherit existing formatting; never add new emphasis when *copyediting*.** Keep emphasis
  the author already used (existing `\textbf{}`, `\emph{}`, `\textit{}` stay). When polishing
  existing prose, do **not** introduce any emphasis the source did not have — no new bold,
  italics, underlining, or quotation marks for emphasis. (This restraint applies to copyediting;
  the name-styling convention below is a deliberate part of *first drafting*.)

- **Method / system / benchmark name styling (when first drafting).** Give the work's own name a
  single, stable presentation across the paper:
  - **Bold (`\textbf{Name}`) at its first mention in the Abstract and again at its first mention in
    the Introduction** — typically the "we present / we propose \textbf{Name}" sentence and the
    matching contribution bullet. This is the one place emphasis is expected; do not leave the name
    unformatted there.
  - After those first mentions, write the name as plain text (no bold, no small caps). Keep its
    capitalization identical everywhere (e.g. `MethodName`, never alternating with
    `Methodname` or `METHODNAME`).
  - **Do not wrap names in `\textsc{}`.** Small caps renders lowercase identifiers
    (`\textsc{modelx}`) as ugly all-lowercase glyphs and clashes with the bold first-mention
    convention. Write model, system, and method names in their canonical capitalization as plain
    text (for example, `Model-X` or `SystemName`), matching the Writing Policy's stabilized term list.

## 4. Structural requirements

- **Never convert prose into lists.** Do not rewrite a paragraph into an `itemize` /
  `enumerate` list or a bullet sequence. Preserve the full paragraph structure; improve it
  in place.

## Verification subset (mechanical, for the final review)

These are the items most likely to drift during generation and are cheap to re-check on
the finished draft. Several can be grep-checked on the LaTeX source:

| Check | How to scan | Pass condition |
|---|---|---|
| No contractions | search for `'t`, `'s` (verb), `'re`, `'ll`, `'ve`, `'m`, `'d` | none in prose (apostrophes only inside strings/quotes that must stay) |
| No possessive `'s` on names | search `[A-Z][A-Za-z0-9-]*'s` | none; rewritten as `of` / noun modifier |
| Abbreviations not expanded | check `LLM`, `RAG`, etc. | kept in short form |
| LaTeX commands intact | diff against source | every `\cite`/`\ref`/`\eg`/`\ie`/emphasis command preserved |
| No emphasis added | diff against source | no `\textbf`/`\emph`/`\textit` that was not in the original |
| No list-ification | diff against source | paragraphs not turned into `itemize`/`enumerate` |
| Zero errors | proofread / spell-check | no spelling, grammar, punctuation, or article errors |

Report violations as fix-needed items; apply the fixes within the writing-only scope.
