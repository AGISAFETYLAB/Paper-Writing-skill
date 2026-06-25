# Finance Review Risks

Finance review must be skeptical. A clear paper can still fail if contribution, identification,
benchmark, data-code, or reproducibility support is weak.

Check for:

- look-ahead bias or survivorship bias
- weak benchmark or factor model
- transaction costs missing from trading/backtest claims
- data snooping or multiple-testing risk
- causal language without identification assumptions
- sample window chosen after seeing results
- proprietary data limits reproducibility
- statistical significance presented without economic magnitude

Map each issue to prose weakening, citation/data verification, open decision, or blocker.

## Seven-Audit Review

Run these audits in order:

1. Abstract: question, method, concrete finding, contribution, word economy.
2. Introduction: hook, research question, early result, identification/model preview, literature as
   story, roadmap.
3. Section-by-section: data, methods, results, robustness, mechanisms, conclusion, appendix.
4. Argumentation: premise, evidence, conclusion, alternative explanations, overclaiming.
5. Prose quality: active voice, units, magnitudes, jargon, paragraph unity, anti-AI patterns.
6. Citations: missing, wrong, orphaned, stale, working paper vs published version, data/software
   citations.
7. Holistic assessment: "So what?", target-audience fit, exhibit payoff, submission readiness.

Page-window status is part of the holistic assessment. A manuscript below min_pages is not merely
"concise"; it is under target window and incomplete unless the user explicitly changes the
target_page_window. A manuscript above max_pages is over target window. Both cases are blocking
until `paper/submission-package.md` records `page_window_status: pass`.

Every issue must name the section, table, figure, or file where it appears and say how to fix it.

## Writing Craft Review Gate

Load `../academic-writing/references/writing-craft.md` for finance prose and argument quality. A review PASS requires:

- the Contribution And Belief-Update Gate has a one-sentence contribution contract and
  `belief_update_status: pass`;
- the Results Narrative Gate has `results_narrative_status: pass` for every central result section;
- the Title-Abstract-Introduction Scorecard has `writing_craft_status: pass` or a documented
  `partial` waiver for an early working-paper draft;
- mechanism and heterogeneity tests follow theory -> observable implication -> test;
- `../academic-writing/scripts/lint_finance_prose.py paper` returns `PASS finance prose lint` or every finding is
  recorded as a justified false-positive waiver.

Do not treat clear formatting, clean tables, or a passing citation audit as a substitute for a
publication-facing argument.

## Table Review Gate

Load `../academic-figure/references/table-design.md` when reviewing finance tables. A table aesthetics PASS requires
more than a compiled PDF:

- each body table has a table payoff sentence that identifies the claim it changes;
- every final table has a `source_table_to_script_map`, table output path, page-budget cost, and
  appendix destination;
- venue-specific table overrides have been checked against the target venue card;
- regression, summary-statistics, portfolio-sort, factor-model, robustness, variable-definition,
  merge-diagnostic, calibration, and model-performance tables pass their family-specific hygiene
  requirements;
- LaTeX table sources pass `../academic-figure/scripts/lint_finance_tables.py` or the submission package records a
  blocker;
- compiled table pages pass layout QA for overflow, clipping, unreadable font, sparse full-width
  pages, and right-side underfill.
- `compiled_layout_qa_status: pass` appears only when `layout_manual_inspection_status: pass` is
  also recorded after contact-sheet or page-PNG inspection.

If a table is visually acceptable but lacks provenance, table payoff, or page-budget handling, mark
the table gate as BLOCKED, not PASS.

## Visual Asset QA Gate

For plotted PNG/JPG preview assets, run `../academic-figure/scripts/audit_visual_assets.py` on the
figure directory before accepting `visual_asset_qa_status: pass`. A blank image, content touching
the image edge, cropped title/axis label/legend, or extreme unused margin blocks figure acceptance.
Fix the source script with a larger canvas, `constrained_layout=True`, or `bbox_inches="tight"` plus
padding; do not hide the issue by shrinking the LaTeX `\includegraphics` width.

## Central Result Uncertainty Gate

Finance review must distinguish magnitude from uncertainty. Headline high-minus-low rows,
long-short spreads, event-window CAR contrasts, alphas, treatment effects, and main regression
coefficients need SE, t-stat, p-value, confidence interval, bootstrap interval, or an explicit
descriptive-only downgrade. A central result may be shown descriptively without uncertainty, but it
cannot be the inferential headline and must set `central_result_uncertainty_status` to `partial` or
`blocked`.

## Submission Attachment Gate

For journal-submission packages, inspect title-page, anonymity, conflict-of-interest disclosure,
funding, acknowledgements, and any venue-specific attachment files. Placeholder text such as "for a
real submission" or "would contain" cannot be marked pass. Workflow-test fixtures may keep such
files only with `submission_attachment_status: partial` or `blocked`, and the final readiness
verdict must remain `blocked` or `fail`.

## Edmans Contribution-Execution-Exposition Audit

For finance and financial economics submissions, also classify major issues under:

- Contribution: question, novelty, importance, belief update.
- Execution: sample, identification, alternative explanations, mechanism, robustness, measurement,
  economic magnitude.
- Exposition: introduction real estate, length efficiency, caveat placement, figure/table payoff.

Severity labels:

| Severity | Meaning |
|---|---|
| CRITICAL | likely desk rejection or fatal R&R issue |
| IMPORTANT | referee will raise it and fixing requires substantive work |
| MINOR | polish or clarity issue |
| STRENGTH | keep this feature |

Do not label every issue critical. Force-rank.

## Three-reviewer lens

Use three perspectives when the user asks for review or audit:

- Methodologist: identification, econometrics, uncertainty, robustness, data snooping.
- Field Expert: contribution, closest literature, economic significance, audience fit.
- Writing Critic: structure, prose, abstract/introduction quality, table/figure integration.

## Submission-Readiness Review

Use this verdict scale:

| Verdict | Meaning |
|---|---|
| PASS | Central claims have data/model/benchmark/robustness support and venue gates are checked |
| WARN | Non-critical wording, formatting, or appendix gaps remain |
| FAIL | A central claim, identification step, benchmark, or data/source anchor is incomplete |
| BLOCKED | Invented results, unresolved data permissions, missing causal identification, or advisory trading language |

Always separate statistical significance from economic magnitude in the review.

## Official-Source Gate

For any submission-readiness verdict, cite the target venue's official instructions, the date
checked, and the version target. A compiled PDF is required for full-draft readiness. If only
Markdown exists, or if title page/anonymity/disclosure/data-code/Internet Appendix handling is
unresolved, the submission-readiness verdict is FAIL even when the prose is strong.

For page-window review, use the selected version-target card, selected venue card, and
`paper/submission-package.md`. If `actual_pdf_pages` is below min_pages, above max_pages, or
missing, the submission-readiness verdict is BLOCKED. Do not treat page padding as a fix; missing
legitimate content must map to supported evidence or
`needs_user_evidence`.
Run `scripts/audit_page_window.py` whenever a compiled `paper/` package exists; do not accept a
natural-language "blocked" note as a substitute for machine-readable `page_window_status`.
Run `../academic-figure/scripts/lint_finance_tables.py` before treating the table aesthetics or table provenance gate
as pass. Missing `table_static_lint_status` is a submission-readiness blocker for LaTeX packages
with editable tables.
Run `scripts/audit_submission_package.py paper` before reporting submission-readiness. Missing
status fields, placeholder attachments marked pass, `compiled_layout_qa_status: pass` without
`layout_manual_inspection_status: pass`, synthetic evidence not reflected in a blocked/fail verdict,
or missing central-result uncertainty not reflected in the verdict are blockers.
