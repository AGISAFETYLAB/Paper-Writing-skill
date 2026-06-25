# Stage: Manuscript Package — Medicine

Load this fragment after the Paper Framework is confirmed and you begin creating `paper/`. Pair it
with `stages/section-drafting.md`, `academic-figure`, `academic-citation`, and `academic-review`.
The confirmed Paper Framework must specify a Submission Format Route: `word-first`, `latex-first`, or
`generic-review`.

Load the route fragment that matches the confirmed Submission Format Route before creating files:

- `static/workflow/routes/word-first.md` for `word-first`;
- `static/workflow/routes/latex-first.md` for `latex-first`;
- `static/workflow/routes/generic-review.md` for `generic-review`.

Also load `../../_shared/core/package-gates.md`. For `word-first`, load
`../../_shared/submission/word-first-production.md`; it owns the detailed DOCX, AMA, JAMA-family,
`submission-clean`, `review-preview-inline.docx`, and component-order rules. Copy the current
`writing-policies/workflow-state.json` to `paper/workflow-state.json` when `paper/` is created, then
update it as package artifacts and gates are produced. The state file must use schema version
`medicine-workflow-state-v1`.

## Route Selection

Before creating files, read the confirmed Paper Framework's Template And Submission Plan. Build the
route selected there:

```text
word-first:
  paper/manuscript.docx
  paper/manuscript.md
  paper/references.bib
  paper/figures/
  paper/tables/
  paper/supplement/
  paper/title-page.md
  paper/cover-letter.md
  paper/editorial-system-checklist.md
  paper/submission-package.md

latex-first:
  paper/main.tex
  paper/references.bib
  paper/main.pdf
  paper/figures/
  paper/tables/
  paper/title-page.md
  paper/cover-letter.md
  paper/editorial-system-checklist.md
  paper/submission-package.md

generic-review:
  paper/manuscript.md
  paper/references.bib
  paper/figures/
  paper/tables/
  paper/title-page.md
  paper/editorial-system-checklist.md
  paper/submission-package.md
```

Do not require `paper/main.pdf` for word-first routes. A PDF generated from Word or Markdown may be
named `paper/review-preview.pdf`; it is a review artifact, not the primary submission file and not a
completion requirement unless the user asks for it.

## Template And Source Rules

1. **Word-first route**: for JAMA/JAMA-style Original Investigation or any target whose official
   instructions expect Word/editable manuscript files, make `paper/manuscript.docx` the production
   artifact. Keep `paper/manuscript.md` as an auditable source when useful. Tables should be editable
   Word tables or companion CSV/XLSX files under `paper/tables/`; figures remain separate assets under
   `paper/figures/`. Select the Word reference/template in this order: preloaded official Word
   template -> user-provided official template -> official web fetch -> package-local generic Word
   reference shell. JAMA/JAMA-style routes must not claim an official Word template unless an
   official source or user-supplied file proves one.
2. **Official downloaded LaTeX template**: for Nature Portfolio / Springer Nature journal article
   submissions where LaTeX is accepted and appropriate, copy the full directory
   `../../assets/templates/springer-nature-latex/sn-article-template/` into `paper/` or copy at least
   `sn-article.tex`, `sn-jnl.cls`, `sn-bibliography.bib`, and required companion files. Preserve the
   class and bibliography setup; replace sample body text with the manuscript. Use `iicol` only when
   the confirmed Paper Framework requests a two-column preview or the target journal requires it.
3. **Instruction-derived shell**: `../../assets/templates/jama_original_investigation.tex` is never an
   official JAMA template. Use it only for an optional PDF review artifact if the Paper Framework
   explicitly requests one.
4. **Generic review route**: when the accepted submission source is unresolved, produce
   `paper/manuscript.md` and label the package as not submission-ready.
5. **Named target without local template**: use a user-provided template if available; otherwise fetch
   the official target-journal instructions/template source and record the result. If only a shell is
   available, report that final submission may require DOCX or journal-system formatting.

Never hand-write an official class/preamble from memory. Never call a generic or instruction-derived
shell an official template. Never convert a word-first target into LaTeX merely because a local shell
exists.

## LaTeX Compile Environment Check

Run this only for `latex-first` routes or optional PDF review artifacts:

```bash
latexmk -version
```

If `latexmk` is unavailable, try `pdflatex --version`. If no engine is available, tell the user in
one line that PDF compilation cannot be verified in this environment, then still produce source and
run static checks. Do not silently skip a required LaTeX compile gate on `latex-first` routes.

## Word Document Generation

For `word-first` routes, create `paper/manuscript.docx` directly.

For JAMA-style word-first routes, `paper/manuscript.docx` is mandatory even if an optional PDF preview exists. An optional `paper/main.pdf` or `paper/review-preview.pdf` does not satisfy the word-first production gate.

Preferred generation path:

```bash
pandoc paper/manuscript.md -o paper/manuscript.docx
```

If `pandoc` is unavailable, use an available Word-writing library such as `python-docx` to create the
document from the drafted manuscript structure. The Word file must contain editable text, editable
tables, figure callouts, and either a documented separate-upload figure package or a preview file with
embedded figures;
do not satisfy the route by exporting a PDF or raster screenshots of tables. If no DOCX-capable tool
is available, leave `format-specific production gate: BLOCKED`, keep `paper/manuscript.md`, and tell
the user that `manuscript.docx` could not be generated in the current environment.

For JAMA/JAMA-family routes, use a `submission-clean` primary manuscript by default: figures should
be submitted as separate files, 1 file per figure, and should not be embedded in `paper/manuscript.docx`.
Keep Figure Legends in the manuscript and keep upload-ready PNG/SVG/TIFF assets under `paper/figures/`.
If a reader-friendly file is useful, create `paper/review-preview-inline.docx` using embedded figures
and record it as a preview artifact only. Do not mark the preview file as the primary submission file.

When `python-docx` is available and no user-provided Word template is supplied, use the package-local
renderer `scripts/render_medical_word_docx.py` with
`../../assets/templates/word/generic-medical-word-reference.docx` or an equivalent valid reference
DOCX. The reference is a package-local generic Word reference shell, not an official Word template.
The renderer must create a normal Word package with editable tables, embedded or upload-ready figure
evidence, captions, and standard Word package parts. Run it with an audit output when possible:

```bash
python scripts/render_medical_word_docx.py paper/manuscript.md paper/manuscript.docx --reference-docx ../../assets/templates/word/generic-medical-word-reference.docx --figures-dir paper/figures --figure-mode upload-only --audit-json paper/docx-structure-audit.json --sync-package-reports
python scripts/render_medical_word_docx.py paper/manuscript.md paper/review-preview-inline.docx --reference-docx ../../assets/templates/word/generic-medical-word-reference.docx --figures-dir paper/figures --figure-mode embed-preview --audit-json paper/review-preview-docx-audit.json
```

Before rendering a JAMA/JAMA-family word-first manuscript, follow
`../../_shared/submission/word-first-production.md`: normalize the Markdown source to AMA
superscript citation style and first-citation order:

```bash
python ../academic-citation/scripts/audit_medical_citations.py paper
python ../academic-citation/scripts/format_ama_manuscript.py paper/manuscript.md --in-place --audit-json paper/ama-citation-audit.json --sync-citation-reports
python ../academic-citation/scripts/audit_ama_citations.py paper/manuscript.md
python ../academic-review/scripts/audit_jama_components.py paper/manuscript.md --json
```

The structural medical citation audit must block malformed DOI/PMID/PMCID fields, placeholder
authors, missing stable identifiers for modern medical entries, missing/uncited LaTeX cite keys,
rendered references that hide identifiers, and rendered biomedical acronyms/proper names that are
lowercased. The AMA citation audit must enforce the Citation And Component Order rules in
`../../_shared/submission/word-first-production.md`, including the exact blocker text
`Tables section is not the final manuscript component` when that order defect is present.
The JAMA component audit must also block nontrial/non-meta-analysis titles that include study type
or design, and must block fixture-derived adjusted estimates in the main Table 2 or main figure set.
Place non-fitted adjusted placeholders only in a supplement/provenance table or omit them.

If `python-docx` cannot be installed but the user, journal, or workspace supplies a valid reference
DOCX, use the same renderer with `--reference-docx <template.docx>`. The reference document must be a
valid Word package that preserves settings, theme, numbering, and styles; still run the DOCX
structure audit after rendering.

Do not hand-write a minimal OOXML ZIP as a substitute for a Word production renderer. A package with
document.xml and styles.xml only, missing `word/settings.xml`, `word/theme/`, or `word/numbering.xml`,
or containing only a tiny `word/styles.xml` is a minimal OOXML shell, not a reviewable Word-first
manuscript. Such a file may be kept only as a diagnostic artifact; do not mark
`format-specific production gate: PASS (word-first)` from it.

After creating `paper/manuscript.docx`, run the package-local DOCX structure audit:

```bash
python ../academic-review/scripts/audit_word_docx.py paper/manuscript.docx --expected-figures <n> --allow-separate-figures
```

Use the correct relative path from `paper/`; if needed, call
`../academic-review/scripts/audit_word_docx.py` directly from this hub skill package. Record the audit result in
`paper/submission-package.md` and `paper/review-report.md`; when using the renderer, prefer
`--sync-package-reports` so those reports cannot keep stale gate text after DOCX regeneration. The
DOCX structure audit must inspect at least `word/settings.xml`, `word/styles.xml`, `word/theme/`,
`word/numbering.xml`, paragraph style coverage, table style coverage, `word/media`, and
`w:drawing`. It must also include a DOCX layout audit for core title and heading style sizes,
cell border coverage, table grid coverage, `w:tcBorders`, `w:tblGrid`, and continuous page numbering;
a structurally valid DOCX
with inherited oversized title styles or borderless cells is not a passing word-first artifact. If
the named journal follows JAMA-style Word submission, the DOCX must also use 10-, 11-, or 12-point
font, double-space text outside tables, leave right margins ragged, start the title page, Key
Points/Abstract, main text, References, Figure Legends, and Tables on a new page where applicable,
render numeric citations as AMA superscript references rather than literal brackets, and use
continuous page numbering beginning with the title page. If
the audit reports minimal OOXML, document.xml and styles.xml only, absent media/drawing evidence for
planned preview figures without a documented separate-upload route, weak table styling, missing cell borders, missing table grids, or
nonconforming title/section style sizes, weak double spacing, missing new page breaks, or bracketed
citations, do not mark `format-specific production gate: PASS (word-first)` and do not mark `visual
display gate: PASS`; use `format-specific production gate: BLOCKED` or the corresponding
visual/table/citation blocker.

## Layout And Float Rules

When the selected route is `latex-first` and the selected template is two-column:

- use `figure`/`table` with `\columnwidth` for compact plots and compact tables;
- use `figure*`/`table*` with `\textwidth` for CONSORT/PRISMA flows, multi-panel outcome figures,
  long-label forest plots, calibration plus decision curve panels, and wide tables;
- do not scale all figures to the same width;
- avoid equal-width `tabularx` columns for clinical outcome/harms tables when that compresses
  effect estimates or definitions;
- assign wider fixed-width columns to effect, uncertainty, and definition/notes fields;
- keep compact one-panel heatmaps, ROC plots, funnel plots, ICER planes, tornado plots, and
  time-to-event plots single-column unless labels or panel count make them unreadable;
- make high-information tables cross-column when they contain long risk-of-bias signals, statement
  actions, interpretation boundaries, or multiple text-heavy columns;
- use a non-floating cross-column block when a `table*` would separate a statement/checklist table
  from its section heading or make following sections appear before the table;
- add a float barrier such as `\clearpage` before Discussion if double-column Results floats would
  otherwise appear after Discussion.

Specific table safeguards:

- baseline tables can be single-column only if all labels, denominators, units, and missingness fit;
- Table 1-style cohort/baseline tables for JAMA/STROBE should include an Overall column when
  source-supported, missing values or a missingness footnote/eTable linkage, variable units/ranges,
  and a standardized difference definition;
- primary/secondary outcome tables should normally be cross-column, with a wide effect-estimate
  column;
- Table 2-style outcome tables for JAMA/STROBE should include primary/secondary role labels, risk
  difference 95% CI, crude OR with 95% CI, and source-status caveats when these are missing;
- if an adjusted estimate is deterministic, fixture-derived, placeholder, or not produced by a real
  fitted model, do not include it in main Table 2 or a main effect-estimate figure; use a supplement
  provenance table or omit it from the display set;
- harms/adverse-event tables should normally be cross-column when they include severity, seriousness,
  definitions, or denominator notes;
- checklist matrices and statement tables may be appendix/supplement cross-column tables when they
  would crowd the main Results.

## Assembly Rules

Create `paper/` as a route-specific manuscript package:

- back up an existing `paper/` to `paper-backup-<timestamp>/` before replacing it,
- create the primary manuscript file for the confirmed route,
- create `paper/references.bib`, `paper/figures/`, and `paper/tables/` when displays are present,
- create `paper/title-page.md`, `paper/cover-letter.md` when a target journal is named, and
  `paper/editorial-system-checklist.md`;
- keep author names, ORCID, corresponding-author contact, ICMJE authorship approval, permissions,
  suggested reviewers, and previous submission or reviewer comments as author-supplied facts; do not
  invent them;
- create `paper/tables/` for reusable polished table fragments when main tables are complex enough
  that inline manuscript text would obscure the source,
- use structured abstract headings when the article type requires them,
- include Key Points when required or planned,
- include the checklist matrix or a checklist appendix/supplement note,
- for checklist-bound outputs, include the full selected item-level checklist matrix, not a short
  core-item excerpt. A STROBE observational package must expose all 22 STROBE items with status,
  evidence location, and missing evidence/action columns before any formal-compliance wording.
- include statement text or explicit unknown markers from the Statement Plan,
- include trial registration and protocol/SAP language only when source evidence exists,
- Do not represent a planned figure as a table when source data can render a figure asset. A planned
  `Fig.` display should create a file under `paper/figures/` and be linked from the manuscript unless
  the Paper Framework explicitly downgrades it to a table. For `latex-first`, link means
  `\includegraphics`; for `word-first`, link means a figure callout plus a separate figure file.
- For observational cohort full drafts, satisfy the minimum visual display set when source evidence
  exists: cohort flow, outcome rate figure, effect-estimate forest plot, polished baseline table, and
  polished outcomes table. If a required display is blocked, record the exact missing source instead
  of silently returning a table-only Results section.
- Generate vector figure assets for quantitative displays when tooling permits, with a PNG preview or
  rendered preview check for visual QA. Do not reuse a tiny or margin-heavy flow diagram when it is
  unreadable at the target manuscript size.
- Main manuscript tables must pass the table aesthetics gate: `booktabs`, compact typography,
  deliberate `\tabcolsep` and `\arraystretch`, custom column widths, compact clinical labels, table
  notes for abbreviations/caveats, and no stacked-word rendering in the target output. For Word-first
  routes, use editable Word tables or companion table files rather than rasterized table images, and
  require table style coverage in the DOCX structure audit before reporting the table aesthetics gate
  as PASS.
- For LaTeX-first routes, table aesthetics also requires actual compiled-output inspection
  (`compiled layout QA`). Run
  `python3 <academic-medicine-writing>/skills/academic-figure/scripts/inspect_compiled_layout.py paper --pages tables --out-dir paper/layout-qa`
  after compiling `paper/main.pdf`; record `paper/layout-qa/layout_qa_summary.md`, rendered table
  pages or contact sheet, and whether any table still shows right-side underfill, clipped cells,
  unreadable effect estimates, sparse full-width pages, or stacked-word rendering.
- The table aesthetics gate is BLOCKED when `main.log` has unresolved `Float too large`, large
  `Overfull \vbox`, or margin-crossing `Overfull \hbox` signals on display pages, even if the PDF
  exists.
- keep denominators, analysis population, and uncertainty aligned between prose, tables, and
  figures,
- keep statement and checklist material in the target-journal order when the journal standard card specifies
  one.
- keep the whole `paper/` package free of internal local file names, generator script names,
  workspace paths, absolute local paths, and package provenance. Use relative source labels or
  redacted source IDs instead. Private engineering validation notes, if needed, must live outside
  `paper/`.

## Local Path Leak Gate

Before returning any manuscript package, run:

```bash
python3 <academic-medicine-writing>/skills/academic-review/scripts/audit_local_path_leaks.py paper
```

The gate is BLOCKED if any artifact in `paper/` contains absolute local paths, raw workspace roots,
generator script paths, or package provenance. Rewrite the artifact with relative source labels or
redacted source IDs, then rerun `../academic-review/scripts/audit_local_path_leaks.py`.

## Aggregate Package Gate

After route-specific production, citation, display, table, statement, review, and local-path gates
have been recorded in `paper/submission-package.md`, run the aggregate gate:

```bash
python ../academic-review/scripts/audit_submission_package.py paper
```

The aggregate gate checks `paper/submission-package.md` and `paper/workflow-state.json` for
route-specific consistency. It must pass before returning the package, even when
`Submission-readiness verdict: BLOCKED` is the correct final verdict.

## Format-specific production gate

Record one of these statuses in `paper/submission-package.md`:

- `format-specific production gate: PASS (word-first)` only when `paper/manuscript.docx` exists,
  `paper/manuscript.md` or another auditable source exists, figures/tables are separately available,
  any PDF is only `review-preview.pdf`, and the DOCX structure audit passes.
- `format-specific production gate: PASS (latex-first)` only when `paper/main.tex` and compiled
  `paper/main.pdf` exist and the compile status is recorded.
- `format-specific production gate: BLOCKED` with the exact missing artifact or official-format
  uncertainty.

Do not require `paper/main.pdf` for word-first routes. Do not call `generic-review` packages
submission-ready.

## Submission Package

Create `paper/submission-package.md` with:

- target journal/article type,
- Submission Format Route,
- primary submission file,
- selected template and source status,
- official-source URL and date checked,
- selected reporting checklist,
- checklist matrix status,
- `Actual main-text word count`,
- `draft length gate: PASS` or a justified `draft length gate: BLOCKED`,
- statement status,
- format-specific production gate status,
- `local_path_leak_status: pass` or `local_path_leak_status: blocked`,
- for `latex-first`, compile command and `main.pdf` status,
- for `word-first`, `manuscript.docx` creation status and any optional `review-preview.pdf` status,
  plus DOCX structure audit metrics and blocker reasons,
- visual display gate: PASS/BLOCKED with main figure asset count, route-specific manuscript callout
  count, and any blocked planned figures,
- table aesthetics gate: PASS/BLOCKED with target-output inspection status and any table that still
  wraps, overlaps, crowds effect estimates, leaves right-side underfill, or lacks the required
  `layout_qa_summary.md` for a LaTeX-first route,
- unresolved submission risks.

The draft length gate must compare the calculated main-text word count against the saved Length
Budget Summary. Do not write `draft length gate: PASS` when the count is below the recorded lower
bound, above the recorded upper bound, or only "near" the budget. Use `draft length gate: BLOCKED`
with the exact count and budget unless the confirmed framework explicitly records an accepted
under-target exception.

For JAMA/JAMA-family routes, create a single supplement Word document or record a blocker explaining
why only Markdown/CSV supplement fragments are available. Markdown/CSV eTables may remain as
auditable source files, but they do not by themselves satisfy a submission-clean supplement package.

`paper/editorial-system-checklist.md` must include: title-page completeness, ICMJE authorship
approval, ORCID status, ethics/consent/registration, data/code availability, conflicts, funding,
author contributions, AI-use disclosure, permissions, suggested reviewers, previous submission or
reviewer comments, cover-letter status, and journal-system upload notes.

For `latex-first`, compile with:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

If `latexmk` is unavailable but `pdflatex` exists, run `pdflatex` enough times to resolve references.
If compilation fails, fix source errors before review when possible. If the target journal does not
accept LaTeX, do not force a clean LaTeX/PDF package; produce the word-first package and record any
optional preview artifact separately.
