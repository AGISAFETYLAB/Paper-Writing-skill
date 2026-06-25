---
name: academic-review
description: Use when reviewing, auditing, or checking a finance, financial economics, accounting, asset-pricing, corporate-finance, banking, fintech, event-study, theory-model, backtest, or econometrics manuscript for submission readiness.
---

# Academic Review — Finance

Owns the closing gates for a finance manuscript.

Load `references/review.md` before reviewing. For major reviews, run the Seven-Audit Review,
the Edmans Contribution-Execution-Exposition Audit, and the three-reviewer lens: Methodologist,
Field Expert, and Writing Critic.

## Required Gates

1. Manuscript completeness: title page, abstract, JEL codes, keywords, main text, limitations,
   references, tables/figures, data-code statement, appendix note.
2. Identification/econometrics audit: estimand, model, unit, sample, uncertainty, clustering or
   dependence treatment, robustness boundary, and economic magnitude are explicit.
3. Citation audit: no unsupported central claim, missing citations, wrong citations,
   orphaned references, over-citation, under-citation, recency gaps, or self-citation balance
   problems. Run
   `../academic-citation/scripts/audit_citations.py` on `paper/` when a LaTeX draft exists, require
   the Citation Evidence Ledger for every live-lookup citation, and remember that a static audit
   pass does not prove claim support.
4. Data-code audit: data source, sample window, access restrictions, code/repository/README plan, and
   online appendix mapping are explicit.
5. Referee-risk audit: alternative explanations, multiple testing, data snooping, external validity,
   and backtest realism are addressed or bounded.
6. Writing craft audit: load `../academic-writing/references/writing-craft.md`; confirm the Finance Writing Craft
   Gate, Contribution And Belief-Update Gate, Results Narrative Gate, Paragraph Evidence Contract,
   and Title-Abstract-Introduction Scorecard. Run `../academic-writing/scripts/lint_finance_prose.py paper` when
   editable text exists and record `finance_prose_lint_status`, `belief_update_status`,
   `results_narrative_status`, and `writing_craft_status`. A blocked belief update, table-tour
   results narrative, unsupported causal language, or unwaived prose lint finding blocks
   submission-ready wording.
7. Compile and page-window audit: `paper/main.pdf` exists for full-draft outputs, run
   `scripts/audit_page_window.py` on `paper/`, and confirm that `paper/submission-package.md`
   records `target_page_window`, `actual_pdf_pages`, and `page_window_status: pass`; below min_pages
   and above max_pages are blocking.
8. Table design, static lint, and compiled layout QA: load `../academic-figure/references/table-design.md`;
   every main and appendix finance table has a payoff sentence, `source_table_to_script_map`,
   page-budget cost, appendix destination, deliberate width plan, no crowded numeric columns, no
   repeated-label bloat, no right-side underfill, and no unresolved `Float too large`, large
   `Overfull \vbox`, or margin-crossing `Overfull \hbox` signal. For LaTeX full drafts, run
   `../academic-figure/scripts/lint_finance_tables.py paper` and then run
   `../academic-figure/scripts/inspect_compiled_layout.py` on `paper/main.pdf` and record the
   `table_static_lint_status`, `paper/layout-qa/layout_qa_summary.md` path, contact sheet path, and
   table-page inspection status. Table aesthetics audit is blocking when static lint fails, table
   provenance is absent, or the contact sheet shows clipped cells, unreadable fonts, sparse
   full-width pages, or right-side underfill.
9. Visual asset QA: run `../academic-figure/scripts/audit_visual_assets.py paper/figures` when
   plotted assets exist. Cropped titles, clipped axis labels, blank previews, or extreme unused
   margins block `visual_asset_qa_status: pass`.
10. Central result uncertainty audit: headline differences, event-window contrasts, high-minus-low
   rows, long-short spreads, alphas, and treatment effects require SE, t-stat, p-value, confidence
   interval, bootstrap interval, or explicit descriptive-only downgrade. A
   `central_contrast_missing_uncertainty` table-lint finding blocks inferential headline wording.
11. Submission attachment audit: for journal submissions, title-page, anonymity,
   conflict-of-interest disclosure, funding, acknowledgements, and venue-specific attachment
   handling must be real or explicitly partial/blocked. Placeholder attachment files cannot be
   marked pass.
12. Submission package integrity audit: run `scripts/audit_submission_package.py paper` before any
   submission-ready claim and align `submission_readiness_verdict` with synthetic evidence,
   placeholder attachments, layout manual inspection, central-result uncertainty, and replication
   status.
13. Research workflow audit: dataset profile, code-output map, Script Registry / Code Sweep status,
   replication package, and Internet Appendix boundary are explicit.

If any gate fails, revise or return a blocking issue list. Do not call an incomplete manuscript
submission-ready.
