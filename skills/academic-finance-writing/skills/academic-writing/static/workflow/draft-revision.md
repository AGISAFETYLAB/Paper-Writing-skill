# Draft Revision Workflow — Finance

Use when the user provides existing finance prose or LaTeX and asks for a revised draft, or
when the user asks for a local audit without changing files.

Intent classes covered: `draft-revision` and `audit-only`.

## Revision Modes

- `polish-only`: improve language while preserving all estimates, identifiers, sample windows,
  model labels, JEL codes, disclosure text, and file/package boundaries.
- `audit-only`: return findings and risks only; do not rewrite prose, modify files, create a new
  `paper/` package, or run full submission gates unless explicitly requested.
- `revision-with-review`: revise the requested draft boundary and then run the relevant review gate
  before calling a complete version clean.

This workflow does not create a new `paper/` package. If the user asks to fill missing package
components, route to `package-completion`.

## Steps

1. Identify grain: full paper, section, paragraph, abstract, title, caption, regression table, appendix.
2. Detect version target and paper type only when it affects the revision.
3. Preserve data window, sample filters, variable construction, model specification, estimates, standard errors, and JEL/disclosure text.
4. Load `references/prose-style.md` for meaning-preserving finance polish; load
   `references/writing-craft.md` for the Finance Writing Craft Gate, contribution
   language, Results Narrative Gate, and Title-Abstract-Introduction Scorecard; load
   `references/sections/index.md`, `references/sections/paragraph-flow.md`,
   and the selected section guide for section work; load
   `../../_shared/checks/econometrics.md` and
   `../../_shared/checks/identification-strategies.md` when identification or statistical wording
   is touched.
5. Delegate citations, figures/tables, or final review to the sibling skill when the edit touches that subsystem.
6. For a complete versioned manuscript, compile `main.pdf` and run the review gate before calling it clean.

## Polish Passes

Run these passes in order:

1. Meaning-preserving finance polish: preserve all numeric estimates, sample windows, model names,
   standard errors, p-values, alphas, event windows, JEL codes, and disclosure text.
2. Anti-AI and prose-style pass: remove filler, throat-clearing, generic contribution claims, and
   advisory market language.
3. Finance Writing Craft Gate pass: enforce the one-sentence contribution contract, replace empty
   contribution phrases with the actual belief update, and mark `belief_update_status`,
   `results_narrative_status`, and `writing_craft_status`.
4. Claim-strength pass: weaken causal, benchmark, or trading language when evidence is incomplete.
5. Results Narrative Gate pass: rewrite table-tour results paragraphs so the economic conclusion,
   magnitude, benchmark, and uncertainty precede table or figure references.
6. Section-formula pass: align abstract, introduction, results, conclusion, and appendix wording
   with `references/sections/index.md`, `references/sections/paragraph-flow.md`,
   and the selected section guide.
7. Citation/display pass: mark missing citation and table/figure support rather than inventing it.

The claim-strength pass is mandatory for causal, benchmark, trading/backtest, policy, and
mechanism language.

When a complete editable manuscript is revised, run `scripts/lint_finance_prose.py` on
the edited boundary or `paper/` and record `finance_prose_lint_status` unless the user requested
audit-only text output with no file changes.

## Edit Boundary

Do not add data vendors, sample windows, alphas, t-statistics, identification assumptions, or
robustness checks unless they are present in source materials or the user provides them. If stronger
wording would require new evidence, weaken the claim instead.

For any revision summary, name what changed and what did not change. Explicitly state that estimates
and identifiers were preserved when applicable.
