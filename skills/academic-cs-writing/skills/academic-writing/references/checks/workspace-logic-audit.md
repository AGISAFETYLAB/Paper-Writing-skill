# Workspace Logic And Evidence Audit

Use this rulebook during the Writing Policy stage, after Workspace Discovery and before the
Claims-And-Evidence table is written. It is the skeptical pass that turns "files I found" into
"claims I am allowed to write". It exists because Workspace Discovery only *collects* evidence; it
does not *verify* that the planned claims survive contact with the raw artifacts.

## ⚠️ Scope: Writing-Side Audit Only, Never Research

This audit checks the **logic and evidence support of the paper the agent is about to write**. It
does **not** judge, fix, re-run, or redesign the research. It must not:

- run, modify, or re-execute experiments, evaluation scripts, or pipelines,
- recompute metrics, change results, baselines, datasets, or ablations,
- declare an experiment "fraudulent" or rewrite the research idea.

Every finding resolves into exactly one of four **writing-only** actions:

1. **downgrade** — lower the claim strength / scope the wording (per `claim-evidence.md`),
2. **mark** — tag the claim `needs evidence` / `not verified` / `partially supported`,
3. **defer** — record it in the Writing Policy's Open Decisions with a conservative default,
4. **stop-and-ask** — when the issue is decisive for paper identity, a central claim, key
   terminology, or an evidence conflict, stop and ask the user (per `_shared/core/gates.md`).

If correct writing appears to require changing the research itself, mark it as an `idea-level risk`
and stop and ask. Never strengthen an unsupported claim to make the audit pass.

## Step A — Build the shared fact base

Before checking anything, extract a compact fact base from the workspace (not from drafts or
summaries the agent itself wrote):

- **Main claim(s)** the paper intends to make.
- **Visible evidence**: which result files, tables, logs, or annotations exist.
- **Claimed significance / scope**: what breadth the wording would imply.
- **Visible limitations**: caveats, partial runs, single-seed results, missing baselines.

State the **assessment boundary** explicitly: if the workspace is partial, audit only what the
material supports and mark the rest `not assessable`. Do not invent evidence to close a gap.

## Step B — Audit checklist (seven checks)

Run all seven. Record each as `pass` / `risk` / `blocking`, with the source trace.

1. **Trace-to-artifact (phantom check).** Every number, comparison, or scope claim the paper plans
   to make must point to a concrete artifact in the workspace (a result file, table, or log). A
   claim that cannot be traced to a real file is `needs evidence` and **must not be written** as a
   fact. "The tracker says DONE" is not evidence; the output file is.

2. **Cross-file consistency.** When the same metric, count, denominator, model name, or dataset
   split appears in more than one place, the values must agree. On conflict, apply the Source
   Conflict Rule in `_shared/core/contract.md`: decisive conflict → stop-and-ask; non-decisive →
   Open Decision with a conservative default; unresolved → avoid the exact number and mark the
   claim `partially supported` / `not verified`.

3. **Result-to-conclusion logic.** The evidence's *actual* support level caps the claim strength.
   Map each planned claim to a strength level using `claim-evidence.md` (strong / moderate / weak /
   speculative / forbidden). If the planned wording exceeds what the data supports (e.g. data shows
   a within-setting gain but the wording says "generalizes"), downgrade the wording — do not add an
   experiment.

4. **Scope / integrity smells.** Flag, but do not "fix by re-running", the following writing-side
   smells. Convert each into a downgrade, a scope qualifier, or a stop-and-ask:
   - a small pilot described as "comprehensive", "extensive", "robust", or "across settings"
     (state the exact scope: N scenes / N seeds / N configs instead),
   - metrics normalized by the method's own max/min to look near-perfect, or scores rescaled to
     hide weakness (report the raw basis or mark the basis `not verified`),
   - model-generated or baseline outputs used as if they were dataset ground truth (label it a
     proxy, see Step C),
   - best-seed / best-run numbers presented as the typical result when multiple runs exist.

5. **Evidence-type labeling.** Tag each key evidence source by type (Step C) so the claim ceiling
   is explicit before drafting.

6. **Terminology stability.** Terms that will appear in the title, abstract, contribution, method
   name, dataset/task, benchmark, or metric must be consistent across the source material. A term
   that drifts between files is a key-terminology decision — resolve it or stop-and-ask.

7. **Disclosure / publication-name check.** Separate from terminology stability (which asks "is the
   term consistent?"), this asks "should this entity appear in the paper, and under what name?".
   Scan the planned claims, key terms, and the artifacts feeding them for two leak classes:
   - **Internal identifiers** that are not publication names: checkpoint tags, training-run / sweep
     identifiers, wandb run names, internal tool names, unreleased model names (e.g. a `..._step380`
     tag). Each maps to a single public display name in the Naming Map; the internal identifier is
     `display-as:<name>` and must never be written. If no public name exists yet, that is a
     key-terminology / paper-identity decision → stop-and-ask.
   - **Do-not-disclose entities**: baselines or competing methods the authors withhold, internal
     tools, unreleased datasets, partner/product names, not-for-publication results. Mark each
     `do-not-disclose` and ensure it never appears — including by negation or exclusion phrasing.
   **Integrity guard:** if removing a withheld competing method would make a comparison claim
   misleading (a "best"/"state of the art"/"outperforms all" claim that holds only because a stronger
   method was hidden), record it as an `idea-level risk` and **stop-and-ask**. Suppressing a name is
   a writing-only action; manufacturing a false comparison is not — never do the latter to make the
   audit pass.

## Step C — Evidence type to claim ceiling

Label key evidence and cap the wording accordingly. This bounds what the paper may assert; it does
not change the evidence.

| Evidence type | Meaning | Claim ceiling in the paper |
|---|---|---|
| `real_gt` | Dataset-provided / official ground truth | Full performance claims allowed (within evaluated scope) |
| `synthetic_proxy` | Model- or baseline-generated reference | "Proxy consistency" only; never "accuracy" against truth |
| `self_supervised_proxy` | No ground truth by design | Relative improvement only |
| `simulation_only` | Simulated environment | Always qualify with "in simulation" |
| `human_eval` | Human judges | Report N raters; subject to inter-rater caveats |

## Step D — Independent recheck (default ON)

After the agent fills the Claims-And-Evidence table, run a **zero-context independent recheck** to
catch confirmation bias. This reuses the Reviewer Independence rules in the
`academic-review` skill's `references/sections/paper-review.md` (the same model used for the Round 2 subagent there).

- Launch a fresh subagent in an isolated context. Pass it **only**: the list of claims the paper
  intends to make, and paths to the raw result/evidence files. Do **not** pass the Writing Policy
  draft, the agent's Audit Findings, any summary file (`findings.md`, `EXPERIMENT_LOG.md`,
  `NARRATIVE_REPORT.md`), or author framing.
- The subagent returns, per claim: `supported` / `partially supported` / `not supported` /
  `not assessable`, plus the specific file/number mismatch it found.
- Fold its findings back into the Claims-And-Evidence table and Open Decisions. A claim the
  recheck marks `not supported` must be downgraded, marked, or raised as stop-and-ask before the
  Writing Policy checkpoint.

Skip the recheck only when the user explicitly opts out, or when the runtime cannot launch a
subagent — in that case run it as a fresh self second-pass (re-read the raw files cold, ignoring the
table just written) and say so.

## Step E — Output

The audit does not produce a separate file. Its results feed the Writing Policy:

- **Audit Findings** section of `writing-policies/<paper-slug>-writing-policy.md`: a compact table
  with `item`, `check`, `verdict (pass/risk/blocking)`, `source trace`, and `writing action`.
- The **Claims-And-Evidence** table inherits each claim's `status`, `risk`, and `drafting action`
  from the audit.
- Decisive, unresolved findings become **Open Decisions** (or a stop-and-ask before the checkpoint).

## Red lines

- Do not re-run, modify, or redesign experiments to make a claim pass.
- Do not invent evidence, numbers, files, or baselines to close a gap; mark it `not assessable`.
- Do not pass any executor summary, draft, or prior finding to the independent recheck subagent.
- Do not strengthen an unsupported claim; only weaken, scope, mark, defer, or stop-and-ask.
