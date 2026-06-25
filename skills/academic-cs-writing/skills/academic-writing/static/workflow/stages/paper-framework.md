# Stage: Paper Framework

Load this fragment when the Writing Policy has been confirmed and you reach the Paper Framework
stage. It ends at a **blocking confirmation gate**: do not create `paper/` until the user confirms.

The Paper Framework is a concise section-level plan. It is not a paragraph plan and not prose.

#### Profile Structure Adherence (the profile is a hard default)

The resolved manifest-mapped paper type profile path defines the **default
section list, order, naming, and count**. Treat it as binding by default, not as loose inspiration.

- **Default = reproduce the profile's structure.** Match its section list, order, names, and section
  count. Do not split one profile section into two, add a section the profile does not list (e.g., a
  standalone Discussion), merge sections, rename, or reorder **for convenience**.
- **Deviation is allowed only when necessary** — when the actual contribution, evidence, venue
  requirement, or explicit user request genuinely cannot fit the profile structure. A deviation that
  is merely "cleaner" or "more standard" does not qualify.
- **Every deviation must be surfaced and approved.** At the Paper Framework checkpoint, show the
  profile's canonical section list next to the adopted section list, and give a one-line reason for
  **each** split / merge / rename / addition / reorder. Do not apply a structural deviation silently;
  the user must be able to see and approve it before `paper/` is created. If the structure matches the
  profile, state "matches profile" explicitly.

#### Subsection Granularity (avoid over-fragmentation)

Plan and present the framework at **section level**. Within-section structure is content blocks and
paragraph roles, not a numbered table of contents.

- **Do not pre-commit a deep numbered subsection breakdown** (e.g., §3.1–§3.6, §4.1–§4.6) in the
  framework. Listing every step as its own subsection fragments a section into thin pieces and reads
  like an outline dump.
- **Subsections are expected where a section is genuinely large; they are not banned.** Short
  sections (Abstract, Introduction, Related Work, Conclusion) normally use **0 subsections** and run
  as flowing prose. Large sections (Method, Benchmark/Dataset Construction, Experiments) normally use
  **2–4 subsections**.
- Promote a content block to an actual `\subsection` only when it spans multiple paragraphs or owns a
  distinct figure, table, protocol, or formal result that needs its own heading. A block that is only
  one paragraph long should stay a paragraph (optionally a `\paragraph{}` run-in or a `\textbf{}`
  lead-in), not become a subsection.
- **Subsection budget:** **0 for short sections, at most 2–4 for any one main section. Five or more
  subsections in one section is a smell** — merge related steps into one subsection, demote
  single-paragraph items to paragraphs, or move fine-grained detail to the appendix.
- In the checkpoint **Main Content** cell, describe each section as a short phrase or a few content
  blocks (e.g., "construction pipeline, quality control, coverage comparison"), **not** an enumerated
  `3.1 … 3.2 … 3.3 …` subsection list.

#### Core Section Budget (protect the paper's center of gravity)

Every Paper Framework must identify where the paper's main contribution lives before assigning page
budgets. A page plan is invalid if it fits the venue limit by shrinking the core contribution below
the floor required by the paper type.

- **Primary core section**: the section that explains the central contribution itself (e.g.,
  Method, Benchmark / Dataset Construction, System Design, Taxonomy, Main Results).
- **Evidence core section**: the section that proves the central contribution works or matters
  (e.g., Results and Analysis, Benchmark Experiments, Empirical Findings, Comparative Summary).
- **Compress-first sections**: sections to shorten before touching core sections, usually
  Conclusion, broad background, extended related work, secondary analysis, and implementation detail
  that can move to an appendix when the venue permits it.
- **Minimum floor**: the smallest acceptable prose budget for each core section. Use the loaded
  paper-type profile's Priority Contract as the default floor; if the venue is shorter than the
  profile assumes, scale the floor conservatively and surface the tradeoff in the checkpoint.
- For method / algorithm papers, Method is the primary core. In an 8-page generic or conference
  draft, plan Method at 2.0-3.0 pages and do not reduce it below 1.5 pages or roughly 25% of the
  main prose budget unless the user explicitly approves the tradeoff. In a 4-page short paper,
  Method may shrink to about 0.8-1.0 pages, but the framework must say what technical detail moved
  to appendix or was omitted.
- Do not compress a primary-core section below its floor to solve overflow. First compress
  compress-first sections and move nonessential detail to appendix/supplement when allowed. If the
  draft still cannot fit, return to the Paper Framework checkpoint and ask the user to approve a
  changed core-section floor, target venue, or scope.

Load only the references needed to resolve paper structure and physical format:

- Template selection: `_shared/templates/index.md`,
- Venue framework constraints: `_shared/venues/<venue>.md` when a target venue is confirmed,
- Paper type family index and profile: load `_shared/paper-types/index.md` or
  `_shared/paper-types/journal/index.md` for the **Framework Main Content Contract**, then load the
  manifest-mapped paper type profile path under `_shared/paper-types/`,
- Figure/table planning: load the **`academic-figure`** skill (its figure-planning reference); for
  table span decisions also use its table-design reference,
- Journal-only (when `venue_kind=journal`): `_shared/venues/journal-vs-conference.md` for drafting
  posture, and the **`academic-review`** skill's `journal-submission-elements` reference for the
  mandatory statements and display-item caps/tiers that shape the Venue Assembly Plan and the Figure
  Plan, the **`academic-review`** skill's `data-code-availability` reference when empirical data,
  code, source data, repositories, accession numbers, or reproducibility statements are involved,
  plus the **`academic-figure`** skill's journal figure-contract for journal-specific figure
  composition patterns and panel logic that inform the Figure Plan's panel count and evidence hierarchy.

**Template Acquisition (local-first — do not web-fetch when a preloaded template exists).** The
official templates for the major venues are bundled in `_shared/templates/`. Acquire the template in
this strict priority order, stopping at the first that applies:

1. **Preloaded `_shared/templates/`** — when the target venue maps to a bundled template in
   `_shared/templates/index.md`, copy that local file and all its companions. This is the **first and
   authoritative** source.
2. **User-provided official template** — when the user supplied template files for this project,
   use those (they take precedence over a web fetch).
3. **Targeted web fetch for a named-but-unbundled venue** — when the named venue has **no** preloaded
   mapping **and** the user provided no template, **search the web for and download the official
   template** from the venue's official source (CFP / author kit / official style files). Record the
   source URL as a Paper Framework template risk to re-verify before submission.
4. **Generic fallback — only as a reported stopgap** — if web acquisition also fails (no network, or
   no official template can be found), use `generic_article.tex` **and report this to the user
   explicitly**: the official template for the named venue could not be obtained locally or online, the
   generic template is a temporary stopgap, and it must be replaced before submission. Record the
   unresolved-template risk in the Paper Framework.

**A named venue forces a real template.** If the user named a venue, it MUST be resolved through tiers
1→2→3 above; for a bundled venue that means its mapped files (EMNLP / ACL / NAACL → `acl2026.tex` +
`acl.sty` + `acl_natbib.bst`; ICLR → `iclr2026.tex`; NeurIPS → `neurips2026.tex`; ICML →
`icml2026.tex`; AAAI → `aaai2026.tex`; etc.), so set the `venue` axis to that value and select its
mapped template. Silently falling back to `generic_article.tex` while a venue was named is a template
error, not an acceptable default — the generic template is allowed only as the **reported** tier-4
stopgap or for the genuinely unspecified-venue case.

**Do NOT search the web or download a template when `_shared/templates/index.md` maps the target venue
to a preloaded file** — that is the failure mode this rule exists to prevent. The official-source URLs
in venue cards and in `maintenance/venue-template-sources.md` are **provenance records (how the
bundled assets were obtained), not draft-time fetch instructions**. The venue card's "verify the
current official style file before submission" is a *pre-submission* check against the official page,
not a license to re-download the template during drafting. Never reconstruct venue formatting from
memory.

Build the framework in this order:

1. **Venue first**: apply venue constraints as a framework constraint card. If no target venue is
   confirmed, use a generic framework with `generic_article.tex` and a soft 6-8 main-text-page
   drafting budget.
2. **Paper type second — the profile section list is a HARD DEFAULT, not inspiration.** Use the
   paper type profile's candidate sections, order, and naming **as the structure**. Reproduce its
   section count and granularity unless an adaptation is genuinely required (see Profile Structure
   Adherence above). Do not silently split, merge, rename, add, or reorder sections, and do not
   inflate the profile's section count for convenience. For each `Main Content` cell, apply the
   paper-type family index's Framework Main Content Contract: compress the profile's section role
   into a brief argument movement, not a component checklist.
3. **Writing Policy last**: keep only sections and claims supported by available evidence.

#### Draft-stage page budget

Before writing any numeric page budget, resolve the draft stage as
`submission / camera-ready / custom / unresolved`.

- **Submission**: use the venue's submission-stage content-page limit as the active bound.
- **Camera-ready**: use the camera-ready allowance only when the user explicitly says the paper is
  accepted, camera-ready, proceedings-final, or reviewer-response final.
- **Custom**: use only when the user explicitly requests a non-venue page target for a local draft,
  technical report, class project, or stress test. Label it as custom and do not call it the venue
  limit.
- **Unresolved**: stop at the Paper Framework gate and ask; do not create `paper/` with guessed
  page arithmetic.

Do not promote a camera-ready allowance into the submission limit. For ACL-family / ARR venues such
as ACL, EMNLP, and NAACL, long-paper submissions normally use the submission limit, while accepted
final versions may receive an additional content page. If a user-provided page count conflicts with
the loaded venue card, resolve the conflict explicitly: either relabel it as `camera-ready`, relabel
it as `custom`, or ask the user to choose. Never write "EMNLP long paper = 9 content pages" unless
the framework also says the draft stage is camera-ready or custom.

Page-budget arithmetic must be explicit. Start with the venue or generic total budget, subtract
fixed front/back matter only when it counts toward the limit, assign a `Page budget` to each planned
section, and ensure the total planned pages must not exceed the venue limit or generic drafting
budget. For a strict page-limited full-paper venue, the framework must also define a **content-page
target**: set `Content-page target` equal to `Active content-page bound`, because the first complete
draft should use the available body budget for substantive supported content rather than stopping
several pages early. Do not create `paper/` with a lower content-page target unless the user
explicitly approves that lower target as a framework tradeoff. If the user says only "must not exceed
X pages", treat that as "reach page X without exceeding it" for a strict full-paper venue, not as
permission to stop at page X-2. If the draft would overflow, compress or move lower-priority
material to appendix before creating `paper/`; if the draft would underfill the target, expand the
primary/evidence core with supported analysis, protocol detail, or result interpretation before
padding support sections.

File format:

1. **Inputs Used**: Writing Policy path, target venue, selected template, venue format summary,
   page/length budget, paper type, evidence snapshot.
2. **Page Budget Summary**: state the draft stage and the numeric content-page limit as a bound
   value. Include these fields explicitly: **Draft stage**, **Submission content-page limit**,
   **Camera-ready allowance**, **Active content-page bound**, and **Content-page target**. For
   example, an EMNLP/ARR long-paper submission records `Submission content-page limit: 8`, while the
   separate `Camera-ready allowance` is `up to 9 after acceptance`; the active submission bound
   remains `8`. State exactly what is excluded from the active bound (references always; plus
   Limitations / Acknowledgments / Ethics for venues that exclude them). Record the planned main-text
   total and any overflow or compression decisions. The active bound is the `--max-content-pages`
   value; the target is the `--min-content-pages` value when the venue/framework says the draft
   should fill the page budget. For strict page-limited full papers, the terminal checkpoint must
   show the downstream audit command with `--max-content-pages <limit> --min-content-pages <target>`.
   Both are blocking gates once confirmed.
3. **Core Section Budget**: name the `Primary core section`, `Evidence core section`, and
   `Compress-first sections`; state each core section's Minimum floor and any venue-driven tradeoff.
4. **Section Framework**: ordered section list with section name, role
   (`primary-core` / `evidence-core` / `support` / `compress-first`), main content, Prose budget,
   Minimum floor, Compression rule, key evidence or figure/table, and writing cautions. Keep this at
   section level. The `Main Content` cell is a one-sentence phrase from the paper-type contract: it
   should preserve the section's argument movement and evidence/display anchor, not a component
   checklist or mini-outline. It is a drafting anchor, not a paragraph plan or prose recipe; the
   section guide controls the actual rhetorical movement during drafting. Abstract and Introduction
   rows preserve the paper-type Main Content movement, not component inventories. List subsections only when a section genuinely needs them,
   and respect the Subsection Granularity budget (0, or at most 2–4 per section); do not enumerate
   every paragraph as a numbered subsection.
5. **Figure Plan**: a short table with `ID`, `type`, `chart form`, `layout`, `section`, `message`,
   `source`, and `generation route`. Keep only likely main-paper figures and tables. The `layout`
   value must be `single-column`, `double-column`, `appendix`, or `supplement`; the `chart form`
   records the actual visual encoding (`schematic`, `grouped bar`, `donut`, `heatmap`, `table`,
   etc.). Run a cross-figure visual variety check for all numeric plots: do not let every numeric
   result figure default to bar charts when the evidence includes composition, coverage, trend,
   matrix, or tradeoff claims better served by another chart form.
   For teaser, overview illustration, conceptual method picture, or scene-like visual rows, apply
   the `academic-figure` Teaser Picture Route Gate: if an API-visible picture renderer exists, set
   `generation route` to `AI picture illustration`, not `deterministic schematic`. Reserve
   `deterministic schematic` for exact pipeline/framework/architecture/workflow diagrams.
6. **Display-Item Page Budget**: saved-artifact-only table estimating each planned display item's
   main-paper page cost and compression fallback. Keep this table in the saved framework artifact
   and use it for page arithmetic and later audit commands; do not render it as a terminal table.
7. **Venue Assembly Plan**: post-main order, required statements or checklists, optional appendices,
   and `not verified` venue fields. Record that the appendix begins on a fresh page (`\clearpage`
   before `\appendix`). When the venue requires a Limitations section (ACL family), plan it as a
   single dedicated `\section{Limitations}` placed after Conclusion and before References — it is the
   only home for limitations in the paper, and it is excluded from the content-page budget. When the
   venue does **not** require a pre-reference Limitations section and permits appendices, record
   whether Limitations may be moved to an appendix if the compiled draft exceeds the page limit. When
   appendix pages count against the limit or appendices are forbidden, record that appendix movement
   is not an available compression path.
8. **Journal Submission Package Plan**: include only when `venue_kind=journal`; otherwise state
   `n/a`. Materialize journal companion artifacts early in a table with `Item`, `Required?`,
   `Source/status`, `Owner/reference`, and `Blocker?`. Saved artifact table header:
   `| Item | Required? | Source/status | Owner/reference | Blocker? |`. Include Data/Code Availability, Author
   Contributions, Competing Interests, Funding/Acknowledgments, Ethics / IRB / consent, Reporting Summary / checklist, Cover letter, graphical abstract / highlights / key points, source-data
   files, and any venue-specific submission forms. Mark real repository identifiers, DOI/accession
   status, and embargo/restriction wording as source/status facts; missing required identifiers are
   blockers or Open Decisions, not prose to invent later.
9. **Appendix / Supplement Plan**: list every planned appendix or supplement item, or state `none`.
   This plan becomes `paper/appendix-plan.md` during LaTeX project setup. Each item must record
   `Item ID`, `Type`, `Claim backed`, `Source availability`, `Fill status`, `Main-text anchor`, and
   `Fallback`. Include appendix-only full lists, proofs, protocol details, full result matrices,
   prompts, configurations, robustness sweeps, and qualitative example sets only when the source is
   available or the item is explicitly omitted. Do not use appendix movement to hide main evidence
   needed for the central claim.
10. **Open Decisions**: only blocking missing evidence, uncertain section choices, terminology,
   figure/table choices, or user decisions.

For the Figure Plan, use the **`academic-figure`** skill's figure-planning reference. Deciding whether
the main paper needs figures or tables, their layout target, and how they will be generated is part of
the framework. Do not generate figures or tables during framework writing.

Generic fallback: keep the main Figure Plan to 3-5 figures/tables for the generic draft.

Optional translated output files, only when requested before generation:

```text
writing-policies/<paper-slug>-paper-framework.<language-code>.md
```

Terminal-facing Paper Framework checkpoint: mirror the user's interaction language. In a Chinese
conversation, translate the overview headings, section summaries, Figure Plan summaries,
decisions, blockers, and user action request into Chinese. Keep file paths, LaTeX commands,
BibTeX/citation keys, manifest values, figure/table IDs, and machine-parsed markers in their
original form; the saved framework artifact remains English by default unless the user requested a
translated sibling artifact.

**Language routing invariant:** the saved framework artifact may keep the English schema below, but
the checkpoint displayed in the terminal is the interaction-language version. Do not paste the
English schema labels into a Chinese terminal checkpoint. For Chinese conversations, the terminal
checkpoint must use at least these labels:

| English saved-artifact label | Chinese terminal label |
|---|---|
| `Checkpoint: Paper Framework` | `检查点：Paper Framework` |
| `Stage result` | `阶段结果` |
| `Output` | `输出文件` |
| `Summary` / framework overview | `框架概览` |
| `Paper Title` | `论文标题` |
| `Section Plan` | `章节计划` |
| `Core Section Budget` | `核心章节预算` |
| `Figure Plan` | `图表计划` |
| `Structure vs paper-type profile` | `结构与 paper type profile 对齐` |
| `Decisions to confirm` | `待确认决策` |
| `Unresolved blockers` | `未解决阻塞项` |
| `User action required` | `请确认或修改` |

Terminal checkpoints must include the Section Plan table (`章节计划` in Chinese) after the framework
overview. Section Plan is mandatory terminal output; do not replace it with overview bullets. Keep it
brief by showing each section's role, one-line Main Content, prose budget, floor, and compression
rule. For Chinese terminal output, render `章节计划` as a Markdown table with this localized header:

```markdown
| # | 章节 | 角色 | 主要内容 | 主文预算 | 底线 | 压缩规则 |
|---:|---|---|---|---:|---:|---|
```

Do not write `章节为` plus a slash-separated section list, or any prose-only section summary, as a substitute for the table.

For Chinese terminal Figure Plan tables, localize human-facing headers such as `Type`, `Chart form`,
`Layout`, `Section`, `Message`, `Source`, and `Generation route` to `类型`, `图形形式`, `版式`,
`位置章节`, `信息点`, `来源`, and `生成路径`; keep `ID`, `Fig. 1`, `Tab. 1`, `single-column`,
`double-column`, `appendix`, and `supplement` unchanged. Chinese terminal chart-form values must be localized, while the saved framework artifact keeps canonical English chart-form values. Use this
minimum mapping when applicable: `schematic -> 示意图`, `donut -> 环形图`, `pie -> 饼图`,
`bar -> 柱状图`, `grouped bar -> 分组柱状图`, `stacked bar -> 堆叠柱状图`, `horizontal bar -> 横向条形图`,
`heatmap -> 热力图`, `line -> 折线图`, `scatter -> 散点图`, `radar -> 雷达图`,
`distribution -> 分布图`, and `table -> 表格`. The final user action line should be Chinese, e.g.,
`请确认是否继续创建 paper/，或告诉我需要修改的内容。`

For Chinese terminal output, render `图表计划` as a Markdown table with this localized header:

```markdown
| ID | 类型 | 图形形式 | 版式 | 位置章节 | 信息点 |
|---|---|---|---|---|---|
```

Do not write `图表计划包含` plus a prose list of figures/tables, or any prose-only figure summary, as a substitute for the table.

Terminal Paper Framework checkpoints have exactly two mandatory Markdown tables: Section Plan and Figure Plan. These are the only Markdown tables in the terminal checkpoint. After the Figure Plan table, do not output any additional Markdown table in the terminal checkpoint. Do not render `Display-Item Page Budget` as a terminal table; keep display-item page costs in the saved framework artifact and use them for page arithmetic, framework self-checks, and later audit commands. The terminal checkpoint must not contain a `Display-Item Page Budget:` heading; display-item page costs must never appear as a third terminal table. If display-item costs affect confirmation, mention the tradeoff in prose only under the framework overview, Core Section Budget, `待确认决策`, or `未解决阻塞项`.
Journal Submission Package Plan and Appendix / Supplement Plan also stay in the saved framework
artifact by default; if they create a required decision or blocker, summarize that issue in the
framework overview, `待确认决策`, or `未解决阻塞项`, not as extra tables.

When the user requests changes at the Paper Framework gate, apply the changes to the framework
artifact and stay inside the same gate. The revision pass must re-render the full Paper Framework
checkpoint in the terminal using the same interaction-language schema; revision pass must re-render the full Paper Framework checkpoint before asking for confirmation again. It must include the updated
Section Plan table and updated Figure Plan table, even if only one figure, section, or page budget
changed; every revision pass must include the updated Section Plan table and updated Figure Plan table. Do not answer only with a change summary, bullet list, or "file updated" note. The workflow
cannot proceed to paper/ until the revised tables have been shown and confirmed.

Show the framework to the user for confirmation using this terminal structure. Do not use a generic
dimension/content table or any other structure. The English labels below name the terminal checkpoint
schema; terminal-facing labels and natural-language cell content must be translated to the user's
interaction language when different. Saved framework artifacts still keep the full File format above,
including saved-only display-item page costs.
```text
Checkpoint: Paper Framework
Stage result: <one sentence>
Output: <framework artifact path>

Paper Title: <confirmed working name / title from Writing Policy>

Section Plan:

| # | Section | Role | Main Content | Prose budget | Minimum floor | Compression rule |
|---:|---|---|---|---:|---:|---|
| 1 | Abstract | support | <main content, one sentence> | <pages> | n/a | <compress / keep> |
| 2 | Introduction | support | <main content, one sentence> | <pages> | n/a | <compress / keep> |
| ... | ... | ... | ... | ... | ... | ... |

Keep `Main Content` as a one-sentence phrase or a few content blocks from the paper-type contract.
It should name the section's argument movement and evidence/display anchor in passing, not expand
into a paragraph plan. Do not list a numbered subsection breakdown (no `3.1 … 3.6`) here;
subsections, if any, follow the Subsection Granularity budget and are decided at drafting time.

Core Section Budget:
- Primary core section: <section + minimum floor + reason>
- Evidence core section: <section + minimum floor + reason>
- Compress-first sections: <sections to cut before touching core sections>
- Core tradeoffs: <none, or explicit venue/scope tradeoff needing confirmation>

Figure Plan:

| ID | Type | Chart form | Layout | Section | Message |
|---|---|---|---|---|---|
| Fig. 1 | <teaser/pipeline/result/...> | <schematic/donut/grouped bar/heatmap/...> | <single-column/double-column> | Introduction | <what the figure shows> |
| Tab. 1 | <taxonomy/result/...> | <table> | <single-column/double-column/supplement> | Method | <what the table shows> |
| ... | ... | ... | ... | ... | ... |

Structure vs paper-type profile:
- Profile: <paper-type name> → <the profile file's section table, its section column copied verbatim in order — not paraphrased>
- Adopted: <the section list above, in order>
- Deviations: <"matches profile", OR one line per split / merge / rename / addition / reorder with its reason>

Decisions to confirm:
- Required: <section order / core-section floors / prose page budget / display-item cost tradeoff if it changes compression / venue assembly>
- Structure basis: <which paper type drove the structure; if any deviation is listed above, why it is necessary and not just "cleaner">
- Optional: <template / language variant defaults>
Unresolved blockers: <none or concise list>
User action required: Please confirm whether to proceed to paper/, or what to change. If any
structural deviation or core-section floor tradeoff is listed, confirm it explicitly before paper/ is
created. In Chinese terminal output, render this as: 请确认是否继续创建 paper/，或告诉我需要修改的内容；如果上面列出了结构偏离或核心章节底线权衡，请明确确认后再创建 paper/。
```

Do not output a separate `Content snapshot` bullet list.

**Compliance Self-Check (Paper Framework) — complete before showing the checkpoint.** Answer each
item yes/no internally; **any "no" means this stage is not complete — fix it before stopping at the
gate.**

1. Is the `Profile:` line copied verbatim from the paper-type file's section table (its section
   column, in order) rather than paraphrased, and does the adopted section list match it, OR is every
   split / merge / rename / addition / reorder listed with a necessity reason in the "Structure vs
   paper-type profile" block? (A deviation that is only "cleaner" is not allowed.)
2. Is the `Main Content` cell free of numbered subsection dumps (no `3.1 … 3.6`), and is each
   section's planned subsection count within budget (0 for short sections, ≤4 for main sections)?
3. Is the page-budget arithmetic shown explicitly and within the venue/generic limit, including both
   prose and display-item page cost, and does it name the draft stage, Submission content-page limit,
   Camera-ready allowance, active content-page bound, and content-page target for the first full
   draft?
4. Does the plan name the Primary core section, Evidence core section, Compress-first sections, and
   Minimum floor for each core section, and do all prose budgets respect those floors?
5. Does the Figure Plan declare both `layout` and `Chart form` for every figure/table, does the
   Display-Item Page Budget estimate each item's main-paper page cost, and does each item map to a
   confirmed section?
5b. Did the framework run the cross-figure visual variety check: if two or more numeric result
   figures are planned, are their chart forms justified by claim-to-chart fit rather than all
   defaulting to bars?
6. Does the Appendix / Supplement Plan either list every planned appendix item with `Claim backed`,
   `Source availability`, `Fill status`, `Main-text anchor`, and `Fallback`, or explicitly state
   `none`?
7. For a strict page-limited conference venue, does the plan leave a practical compression margin
   rather than spending the whole limit on planned prose and floats?
8. Are all checkpoint fields filled, including the "Structure vs paper-type profile" comparison?
9. Do Abstract and Introduction rows preserve the paper-type Main Content movement, and are they
   not component inventories?

Gate: the user must confirm the Paper Framework before full-draft writing.
