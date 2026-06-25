# Finance Submission Standards

Official-source snapshot checked: 2026-06-22.

Finance is usually not a fixed-template conference workflow. The blocking standard is the version
target: working paper circulation, conference submission, or journal submission. For journal
submission, the final artifact must be a compiled PDF plus data/code, appendix, disclosure, and
venue-format checks.

## Page-Window Gate

Every full draft must define a `target_page_window` before section drafting starts. Use official first:
current target-venue page or current CFP when it gives a page or word limit. If no official page
limit is available, use the field convention fallback (`field_convention_fallback`) recorded in the
selected version-target card and selected venue card.

The gate is hard in both directions:

- below min_pages -> `page_window_status: below_min_pages`
- above max_pages -> `page_window_status: above_max_pages`
- missing compiled page count -> `page_window_status: blocked_uncounted`

Do not call a manuscript complete or submission-ready unless `page_window_status: pass` is recorded
in `paper/submission-package.md`. Do not pad or invent evidence to reach min_pages; unresolved
legitimate content should be marked `needs_user_evidence`.

## Official Anchors

| Source | Use in this skill |
|---|---|
| Journal of Finance submissions: https://afajof.org/submissions/ | Title page, disclosure statement, page limit, Internet Appendix placement, and code-sharing policy. |
| Journal of Financial Economics submissions: https://www.jfinec.com/submissions | Anonymous manuscript PDF, short abstract, double-spaced 12-point manuscript, margin expectations, online appendix placement, and disclosure upload. |
| Review of Financial Studies general instructions: https://academic.oup.com/rfs/pages/General_Instructions | RFS/SFS author-instruction and portal checks; no package-local RFS template. |
| Journal of Financial and Quantitative Analysis submissions: https://jfqa.org/submissions/ | JFQA plus Cambridge author/contributor policy checks. |
| Review of Finance general instructions: https://academic.oup.com/rof/pages/General_Instructions | Review of Finance/OUP author-instruction checks, including normal versus fast-track route when relevant. |
| Management Science submission guidelines: https://pubsonline.informs.org/page/mnsc/submission-guidelines | INFORMS/ScholarOne workflow, anonymous files, electronic companions, data disclosure, and department fit. |
| AEA Journal Policies: https://www.aeaweb.org/journals/policies | AEA disclosure, data/code, data legality, RCT registry, and journal-specific policy routing. |
| AEA Data and Code Availability Policy: https://www.aeaweb.org/journals/data/data-code-policy | Data/code deposit planning, permissions, repository, replication package, and data-editor review expectations. |
| Quarterly Journal of Economics instructions: https://academic.oup.com/qje/pages/Instructions_To_Authors | QJE title page, author metadata, word count, and abstract-limit checks. |
| Econometrica information for authors: https://www.econometricsociety.org/publications/econometrica/information-authors | Econometric Society submission, membership, data editor, replication, and LaTeX support routing. |
| Review of Economic Studies submissions: https://www.restud.com/submissions/ | REStud submission guidelines, data availability, Editorial Express route, and resubmission restrictions. |
| AFA annual meeting: https://afajof.org/annual-meeting/ | Current-year finance conference call checks, not journal formatting. |
| WFA submissions: https://westernfinance.org/submit-a-paper/ | Current-year WFA call, deadline, and portal checks. |
| EFA annual meeting submission: https://efa2026.efa-finance.org/submission/ | Current-year EFA call, PDF, author-name, and membership checks. |
| SFS Cavalcade: https://sfs.org/sfs-cavalcade-north-america-2026/ | Current SFS Cavalcade call, eligibility, and journal-acceptance restrictions. |
| FMA annual meeting: https://www.fma.org/tampa | Current FMA call and conference-submission status checks. |
| SSRN submission guidance: https://www.elsevier.support/ssrn/answer/get-started | Working-paper/preprint posting requirements; not journal submission. |
| NBER working paper information: https://www.nber.org/nber-help-working-papers-general-information | NBER working papers as preliminary circulation, not refereed publication. |
| CEPR Discussion Papers: https://cepr.org/publications/discussion-papers | CEPR Research Fellow/Affiliate discussion-paper circulation. |
| Elsevier elsarticle LaTeX instructions: https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions | Official Elsevier elsarticle template package and LaTeX source-file submission rules for JFE-style accepted-paper production. |

## Required Submission Package

A full finance output must include:

- `main.tex` and compiled PDF `main.pdf`
- version target: working paper, conference submission, or journal submission
- target journal or venue and date-checked official instructions
- `target_page_window`, `actual_pdf_pages`, count scope, and page-window verdict
- title page/anonymity/disclosure handling matched to venue policy
- abstract, keywords, and JEL codes when expected
- data and code availability statement with replication boundary
- Internet Appendix or Online Appendix when robustness, definitions, or additional tables exceed the main paper
- citation audit for methods, datasets, software, and institutional facts
- visual asset QA and compiled layout QA with manual contact-sheet inspection status
- central-result uncertainty status for headline estimates and contrasts
- machine-readable submission attachment status for title page, anonymity, conflict-of-interest,
  funding, and acknowledgement handling
- final submission-readiness verdict tied to the official source and date checked

## Blocking Checks

- Do not call the manuscript submission-ready until the target venue's current official
  instructions have been checked in this run or the user explicitly accepts a dated local snapshot.
- Do not call the manuscript complete when the compiled PDF is below min_pages, above max_pages, or
  missing a reliable page count.
- Do not treat a working paper as journal-ready without title page, disclosure, appendix, data/code,
  and venue formatting checks.
- Do not invent JEL codes, proprietary data permissions, code repository records, standard errors,
  alphas, or robustness results.
- Do not stop at Markdown. A complete full-draft request must produce a compiled PDF unless the
  user explicitly asks for prose-only output.
- Do not record `compiled_layout_qa_status: pass` unless the contact sheet or page PNGs have been
  inspected and `layout_manual_inspection_status: pass` is also recorded.
- Do not mark placeholder title-page or conflict-of-interest files as submission-ready attachments.
  Workflow-test fixtures may keep placeholders only with `submission_attachment_status: partial` or
  `blocked`.
- Do not use headline high-minus-low, long-short, event-window, alpha, or treatment-effect rows
  without SE, t-stat, p-value, confidence interval, bootstrap interval, or an explicit
  descriptive-only downgrade.
