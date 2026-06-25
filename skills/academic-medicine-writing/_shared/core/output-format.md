# Medicine Output Format

Unless the user asks for another format, return or write a format-specific full manuscript package.
The target journal's current author instructions decide the primary output route; do not force every
medical manuscript through LaTeX/PDF.

```text
Format-specific full manuscript outputs:

word-first route:
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

latex-first route:
  paper/main.tex
  paper/references.bib
  paper/main.pdf
  paper/figures/
  paper/tables/
  paper/title-page.md
  paper/cover-letter.md
  paper/editorial-system-checklist.md
  paper/submission-package.md

generic-review route:
  paper/manuscript.md
  paper/title-page.md
  paper/editorial-system-checklist.md
  paper/submission-package.md
```

The editorial-system checklist records ICMJE authorship approval, ORCID fields, permissions,
suggested reviewers, and previous submission or reviewer comments when applicable.

Interactive replies must mirror the user's interaction language. Use localized labels for
conversation-facing headings and status lines; keep workflow values, study-type values, file paths,
checklist IDs, LaTeX commands, and citation keys unchanged.

For Chinese interactive replies, use localized labels such as:

```text
路由判断：workflow=<...>；study_type=<...>；sections=<...>。
阻塞缺口：<无，或简要列表>。
输出文件/计划文件：<paths or planned files>。
```

For English interactive replies, lead with:

```text
Detected route: workflow=<...>; study_type=<...>; sections=<...>.
Blocking gaps: <none or concise list>.
Output artifacts: <paths or planned files>.
```

## Route Output Templates

For every routed request, keep the terminal reply short and use this route output template before
adding route-specific details:

```text
A. Input Match Check
   workflow=<...>; intent=<...>; study_type=<...>; input_sufficiency=<enough|partial|insufficient>.
B. Route Output
   <the artifact, revision, figure/table result, citation audit, or review verdict requested by this route>
C. Blocking Gaps
   <none, or P0/P1/P2 items with severity and correction priority>
D. Next Action
   <user confirmation, missing input, or generated artifact path>
```

Route-specific output scope:

- `full-draft-from-evidence` and `package-completion`: checkpoint or package artifacts, plus the
  submission-ready verdict when a complete draft package exists.
- `draft-revision`: revised prose or localized edit report within the requested boundary.
- `figure-table-only`: display artifact, caption/table text, or visual audit only.
- `citation-only`: citation search result, bibliography repair, or citation audit only.
- `submission-review`: findings first, ordered by severity, then residual risk and next action.

For citation or review workflows, lead with blocking issues and evidence gaps before revised prose.

If a full-draft workflow writes files, create the route-appropriate manuscript package. Generate and
compile LaTeX only for `latex-first` routes or when the user explicitly requests a PDF preview.

## Local Path Leak Gate

Do not return a `paper/` package that contains absolute local paths, raw workspace roots, local
source paths, generator script paths, or package provenance in manuscript text, submission metadata,
review-facing reports, DOCX XML, LaTeX, BibTeX, Markdown, or extracted PDF text. Use relative source
labels or redacted source IDs instead.

Run `skills/academic-review/scripts/audit_local_path_leaks.py paper` before calling a package complete and record:

```yaml
local_path_leak_status: pass | blocked
```
