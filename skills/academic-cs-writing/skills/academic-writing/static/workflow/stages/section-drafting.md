# Stage: Section Drafting

Load this fragment for the per-section drafting loop of the Full Draft Workflow. It pairs with
`stages/latex-project.md` (project setup), the **`academic-figure`** skill (every figure/table), the
**`academic-citation`** skill (every searched/written/verified citation and the bibliography), and
the **`academic-review`** skill (the closing gates).

Load section references when drafting each section:

| Draft target | Load |
|---|---|
| Abstract | `references/sections/abstract.md`, `references/sections/paragraph-flow.md` |
| Introduction | `references/sections/introduction.md`, `references/sections/paragraph-flow.md` |
| Related Work | `references/sections/related-work.md`, `references/sections/paragraph-flow.md`; invoke the `academic-citation` skill when citation support matters |
| Method / System | `references/sections/method.md`, `references/sections/paragraph-flow.md`; invoke the `academic-figure` skill when figures or tables are used |
| Experiments / Evaluation | `references/sections/experiments.md`, `references/sections/paragraph-flow.md`; load `_shared/checks/metric-design.md` and invoke the `academic-figure` skill when figures or tables are used |
| Conclusion / Limitations | `references/sections/conclusion.md`, `references/sections/paragraph-flow.md` |
| Appendix / Supplement | `references/sections/appendix.md`, `references/sections/paragraph-flow.md`; invoke the `academic-figure` skill for appendix figures/tables |

Metric definitions in any section: whenever a Method, Benchmark, Dataset, Experiments, Appendix, or
caption defines a rate, score, denominator, or outcome aggregation, also load
`_shared/checks/metric-design.md`. Equations must use formal count variables and no raw `#` count notation;
write `N_{\mathrm{failure}}`, `N_{\mathrm{partial}}`, and `N_{\mathrm{scorable}}` rather
than `#failure`, `# partial`, or `# scorable`.

**Journal section overlays (only when `venue_kind=journal`).** After loading each base section guide
above, also load the matching overlay and apply it on top of the base (it states only the journal
deltas; see `references/sections/journal/index.md`):

| Draft target | Base guide | Journal overlay to layer on top |
|---|---|---|
| Abstract | `references/sections/abstract.md` | `references/sections/journal/abstract.md` |
| Introduction | `references/sections/introduction.md` | `references/sections/journal/introduction.md` |
| Method / System | `references/sections/method.md` | `references/sections/journal/method.md` |
| Conclusion / Discussion | `references/sections/conclusion.md` | `references/sections/journal/discussion.md` |

Sections without an overlay (Related Work, Experiments, and Appendix / Supplement) use the base guide
alone.
When `venue_kind=conference`, do **not** load any file under `references/sections/journal/`.

Load a local example only when the section guide explicitly points to one, the section structure is
uncertain, or the user asks to learn from examples. Learn structure, not phrasing.

## Framework-vs-Section Guide Precedence

The confirmed Paper Framework is a content boundary, not a prose recipe. Use it to know the
section's topic, role, evidence anchors, display anchors, page budget, venue constraints, and
do-not-write boundaries. Do not treat the Framework `Main Content` cell as a paragraph plan,
sentence order, or wording model.

For writing logic, the section guide controls rhetorical movement. Build the internal Paragraph Plan
from `references/sections/<section>.md` plus `references/sections/paragraph-flow.md`, then fill it
with the Framework's confirmed topic/evidence/display anchors. If the Framework wording and section
guide seem to pull in different directions, follow this priority:

1. Framework controls topic, evidence anchors, display anchors, page budget, venue constraints, and do-not-write boundaries.
2. Section guide controls rhetorical movement, paragraph roles, opening/closing logic, and what
   counts as a complete section.
3. Paragraph-flow controls local prose quality: lead with the point, allocate length by importance,
   and avoid inventory-style writing.

Only override a section guide when the Framework records an explicit user decision, venue rule,
evidence boundary, or paper-type structure that makes the guide's normal movement impossible. Record
the residual risk in `paper/section-compliance.md`.

## Paper Content Edit Transaction

Any operation that writes, rewrites, compresses, expands, polishes, or renames manuscript prose,
captions, table text, section headings, or appendix text is a paper-content edit. Before every paper-content edit, re-read from disk the current target's section guide, any required journal
overlay, the conditional metric/claim/display references that apply to the edit, and
`references/sections/paragraph-flow.md`; do not rely on a guide loaded earlier in the run.

After the edit, rerun the Section-Method Adherence check for the touched section(s), revise until
all required moves are `present` or the residual risk is explicit, and update `paper/section-compliance.md`. This is a reread/self-check procedure, not a freshness gate. Do not add hash, mtime, timestamp, or source-hash requirements.

For each section, follow this drafting loop:

1. Read the confirmed Writing Policy, confirmed Paper Framework entry, and relevant source evidence.
2. Load only the current section guide and conditional references.
3. Build an internal Section Plan from the Framework anchors, then a Paragraph Plan from the section
   guide's required movement. Do not copy the Framework `Main Content` phrase as the paragraph order.
4. Write English LaTeX prose, preserving one paragraph per message. Apply
   `references/style/copyediting-standard.md`: formal register, no contractions, no
   possessive `'s` on method/model/system names, simple and clear vocabulary, common
   abbreviations kept unexpanded, LaTeX commands preserved, and no list-ification of prose.
   **Bold the work's own name (`\textbf{Name}`) at its first mention in the Abstract and in the
   Introduction; thereafter plain text with stable capitalization. Do not wrap names in `\textsc{}`.**
   **Apply Salience And Compression (`references/sections/paragraph-flow.md`): lead each paragraph
   and subsection with its point (never bury it); allocate length by importance; and do not
   enumerate taxonomies/inventories/per-category counts in the body — mention them in one stroke
   (dimension, total, salient/novel members) and move the full list to a table or appendix.**
   A taxonomy subsection must not become a glossary-style definition list (`V1 -- ...`, `H1 -- ...`);
   its prose must explain the design rationale, category boundaries, and the few salient/novel
   members, while complete definitions/counts live in a table or appendix.
5. Run reverse outlining and claim-evidence mapping internally; revise before moving to next section.
6. **Section-Method Adherence check (mandatory).** Before moving on, verify the section
   against the *required moves* of its section guide and mark each `present` / `missing`. A `missing`
   move means the section is not done — revise until resolved or record it as an explicit risk.
   **Reader-facing heading quality:** subsection titles must describe what the reader learns, not
   the artifact used or where extra material lives. Do not create a body subsection whose title is an appendix pointer such as `Appendix Matrix`, `Appendix Heatmap`, or `Supplementary Details`;
   make that a prose cross-reference near the relevant result instead. Every Experiments subsection title must name the finding, comparison, protocol, or analysis question, not an internal evidence state such as "snapshot" or "matrix".
   Minimum required moves per section:
   - **Method** (`references/sections/method.md`): every module subsection has motivation, design,
     technical advantage, and evidence hook; an overview/section-map opens the section; terms defined
     before use.
   - **Experiments** (`references/sections/experiments.md`): setup (datasets/metrics/baselines/
     protocol) stated; each contribution claim has a matching experiment; metric direction and scope
     explicit. **No Limitations block lives here** — limitations do not belong in a numbered body
     section; route them to the dedicated Limitations section below.
   - **Abstract**: problem -> challenge/gap -> insight/contribution -> advantage -> evidence
     chain present; contribution sentences state purpose or advantage, not only a component list;
     central claims map to available evidence; one high-level evidence sentence at most, with no
     model-specific deltas and no multiple percentage values.
   - **Introduction**: Introduction chain: task/application or setting -> target goal ->
     prior/current-practice failure -> root technical issue -> contribution/pipeline -> why it
     works -> contribution bullets -> optional evidence preview; no separate experiment paragraph;
     contribution sentences state purpose or advantage, not only a component list; central claims
     map to available evidence; contributions preview maps to later sections; no model-list or
     result-recap paragraph and no multiple-percentage score summary.
   - **Related Work**: organized by topic group with a stated distinction per group, not a citation
     list. **Every named prior method, benchmark, dataset, model, or framework carries a `\cite`**;
     proactively run the targeted citation search (see Citation Search Trigger) rather than leaving
     groups thin.
   - **Conclusion** (`references/sections/conclusion.md`): short close (contribution → strongest
     evidence → scoped implication); **no full limitations paragraph** (it has its own section) and
     **no future-impact / "we hope …" promotional closer**; no new claims or citations. Over-long or
     four-paragraph conclusions with a vision closer are a `missing`/over-length defect — compress.
   - **Limitations** (when the venue expects one, e.g. ACL family): a single dedicated
     `\section{Limitations}` after Conclusion holds all limitations, ~120–180 words, 3–4 material
     points; it is the only home for limitations in the paper (do not also enumerate them in
     Experiments or Conclusion).
   - **Appendix / Supplement** (`references/sections/appendix.md`): every item appears in
     `paper/appendix-plan.md` with `Claim backed`, `Source availability`, `Fill status`,
     `Main-text anchor`, and `Fallback`; every subsection has a real lead paragraph; no central
     evidence is hidden outside the main reading path; no "see supplementary" stub remains when the
     source exists.
   - **All sections**: one paragraph one message; first sentence states the paragraph role and
     leads with the point (not buried); stable terminology; **no taxonomy/inventory/per-category
     enumeration in the body** — such lists are mentioned in one stroke and the full list lives in a
     table or appendix; no glossary-style taxonomy subsection whose main content is one item per
     category; every prose number supports a claim rather than transcribing a table.

   Keep paragraph plans and section plans internal, but write a compact **Section Guide Compliance
   Ledger** to `paper/section-compliance.md` as the durable receipt. The ledger must include one row
   per drafted section: `Section`, `Guide loaded`, `Required moves checked`, `Result`, and
   `Residual risk`. Use `present` only when the required moves are actually present; do not write
   `missing`, `unchecked`, `not loaded`, `todo`, or `tbd` in a returned draft. The closing
   `audit_draft.py --framework ...` gate blocks if this ledger is absent or unresolved.
   Round 2 of the Post-Draft Review Gate (the independent subagent, owned by the `academic-review`
   skill) must independently re-verify these same required moves against the section guides — it is
   the external check that the self-assessment was honest.

**Mechanical non-negotiables while drafting:** apply `_shared/core/stance.md` exactly: no footnotes,
no file/code artifacts, no local paths, no internal identifiers, no do-not-disclose entities, no
leftover missing-support markers, no silent paper-type profile deviations, and no over-budget
subsections. This fragment adds drafting-specific extensions: do not add sections/subsections beyond
the confirmed Framework, and any equation that defines a metric, rate, or denominator must use formal
count notation, with no raw `#` count notation.
For taxonomies, inventories, and per-category counts, follow the Salience And Compression rule once:
the body gives the dimension, total, and salient/novel members; the full definitions/counts go to a
table or appendix. The ban includes the **disguised form**: a run of `\textbf{V1 (...)}.` /
`\textbf{H1 (...)}.` bold lead-in paragraphs that define each coded member one by one is a
glossary-style taxonomy subsection with the `\item` markers removed. **When a taxonomy table already
lists the members, do not also re-define every member in prose.** Put the full per-member definitions
in a dedicated appendix subsection with a real lead paragraph.

**Apply the Disclosure And Naming registries (Writing Policy section 7) to every section, caption,
table, and figure.** For every entity in the Naming Map, write only the public display name; the
internal identifier (checkpoint / training-run / sweep / wandb / tool / unreleased-model name, e.g.
a `..._step380` tag) MUST NOT appear anywhere — not in prose, captions, table cells, figure labels,
or comments meant to ship. For every entity on the Do-Not-Disclose list, write nothing that names or
points at it: not a positive mention, not a passing reference, and **not a negation or exclusion**
(do not write "the protocol that excludes X", "unlike X", or "we do not compare against X"). When a
comparison or protocol sentence would otherwise have named a withheld entity, describe the scope on
its own terms ("against the strongest publicly comparable baselines"), without implying a complete
comparison and without fabricating a result. If suppressing a withheld competing method would make a
comparison claim misleading, do not write the flattering claim — surface it as an `idea-level risk`
per contract point 7.

Do not show internal section plans, paragraph plans, or claim-evidence maps unless the user asks or
a blocking risk must be surfaced.

## Citation Search Trigger

Do not run an unbounded survey, but do not under-cite either. Run targeted citation search whenever
the draft needs external support not already covered by workspace evidence or verified `.bib`
entries. For a full draft, the following are **proactive** triggers — search for them rather than
waiting for a `% CITATION_NEEDED` to appear:

- **Related Work and Introduction background are proactive by default.** Drafting either one
  triggers targeted search for the prior methods, benchmarks, datasets, environments, and comparison
  lines they discuss; a Related Work group with one or zero citations is under-cited, not done.
- **Every named entity must be cited.** Each model, dataset, benchmark, environment, baseline, or
  taxonomy/standard framework named in the text (e.g. each evaluated model, each prior benchmark,
  any security/standard framework the taxonomy is "grounded in") needs a `\cite` to its source.
- **Citation coverage is paper-type-scaled.** Benchmark, survey, and method papers are expected to
  cite broadly; a 10-entry bibliography for such a paper is a smell. The final citation audit is run
  with a paper-type `--min-citations` floor (see the `academic-citation` skill).
- A confirmed Paper Framework names prior work that is missing from local sources.
- A necessary sentence would otherwise require `% CITATION_NEEDED`.
- The user explicitly asks to find, add, or verify references.

When any trigger fires, invoke the **`academic-citation`** skill: it owns the citation-integrity
search, verification, BibTeX completeness rules, `paper/citation-evidence.md` logging, and the
`audit_citations.py` blocking gate. References do not count toward the page limit, so breadth is
cheap; never fabricate to hit a count, and prefer weakening or removing an unsupported claim over a
guessed citation.

## Missing-Support Markers

A marker records a slot whose **underlying evidence genuinely does not exist** in the workspace and
cannot be produced by writing alone. It is a last resort, never a way to defer work the chain can do
now:

```tex
% EVIDENCE_NEEDED: <short reason>
% CITATION_NEEDED: <short reason>
% FIGURE_NEEDED: <short reason>
% TABLE_NEEDED: <short reason>
```

**A `% FIGURE_NEEDED` / `% TABLE_NEEDED` for a display item the confirmed Paper Framework Figure Plan
calls for, or a `% CITATION_NEEDED` for a claim whose source is findable, is NOT an acceptable end
state.** When the user asks for a draft, the Full Draft chain must *resolve* these in the same
session: invoke the **`academic-figure`** skill to generate every planned figure and table, and the
**`academic-citation`** skill to search and write every needed citation. Leaving them as comments and
telling the user to "complete them later" via the sibling skills is a workflow violation — the closing
`audit_draft.py` gate fails on any leftover `% *_NEEDED` marker, so such a draft cannot pass the Final
Static Audits and is not done.

A marker may survive into the returned draft **only** when the evidence is truly missing (an
experiment was never run, a result does not exist, no citable source exists). Even then, prefer
weakening or removing the unsupported claim, and list every surviving marker as a blocking risk in the
final summary — never as routine follow-up. Do not use markers as placeholders for routine prose.

## Writing Rules

- Each paragraph has one message.
- The first sentence states the paragraph's function or core information.
- Define terms before using them.
- Claims require evidence; unsupported claims are weakened or marked.
- Methods must not read as ad hoc patches.
- Captions state the message supported by the figure or table.
- Abstract and Introduction claims require extra caution.
- **No footnotes.** Do not use `\footnote{...}` anywhere. Move the content into the main body as
  inline parenthetical text, or delete it if it does not matter. CS/ML conference papers should
  not rely on footnotes.
- **No file names or code artifacts in prose.** Do not write `\texttt{filename.ext}` or raw
  code identifiers in the paper text. Replace with descriptive natural language: "the benchmark
  manifest" not `\texttt{BENCHMARK_MANIFEST.json}`, "the released evaluation script" not
  `\texttt{compute_asr.py}`. File names and code artifacts are implementation details that
  break the reader's attention and should not appear in published prose.
- **No local paths or directories in prose.** Remove any local filesystem paths, directory
  names, or repository-relative paths from the paper text.

After all sections are drafted and figures/tables/citations are in place, hand off to the
**`academic-review`** skill for the Draft Completion Review Gate, the Final Static Audits, the Final
Submission Readiness Gate, and the Before-Returning Compliance Self-Check. Do not return `paper/`
before those gates pass.
