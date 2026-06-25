# Metric Design Check

Metrics must validate research questions. A paper with many metrics can still fail if the
metrics do not support the core claim.

## Mapping Rule

For each research question, create:

| Research question | Metric / experiment | Required evidence | Why this metric matters | Failure if missing |
|---|---|---|---|---|

## Outcome Semantics Rule

Define outcome labels before naming metrics. A metric may not split or group labels in a way that
hides the paper's actual success/failure semantics.

- **Outcome semantics first**: list each label (`success`, `failure`, `partial`, `stalled`,
  `invalid_run`, etc.), whether it counts as success, failure, unresolved, or infrastructure
  failure, and why.
- If `partial` means the target failure condition partly occurred, it belongs in the failure
  bucket. Report a **failure rate** such as `(failure + partial) / denominator`, not only a
  completed-run rate.
- State every **denominator**: all assigned tasks, scorable tasks, completed tasks, or another
  declared base. Do not compare metrics with different denominators without saying so.
- Keep residual buckets honest. `Other` may group stalled or infrastructure-failed runs, but it must
  not hide failed or partially failed outcomes.

## Formal Count Notation

Rate equations should look like paper equations, not working notes. Do not use `#` as a count operator
in equations or polished prose (`#failure`, `# partial`, `# scorable`, etc.). Define count variables
with `N_{\mathrm{...}}` or `n_{\mathrm{...}}` and use them consistently:

```tex
R_{\mathrm{failure}} =
\frac{N_{\mathrm{failure}} + N_{\mathrm{partial}}}
     {N_{\mathrm{scorable}}},
\qquad
R_{\mathrm{success}} =
\frac{N_{\mathrm{success}}}
     {N_{\mathrm{scorable}}}.
```

If a table column or source file uses a literal hash sign, translate it in the manuscript to
"number of ..." or a defined count variable. Keep raw `#` notation out of equations, captions, and
paper prose unless the hash character itself is the object being discussed.

## Checks

- Does the metric directly measure the claimed capability?
- Is it only a proxy metric?
- Are outcome labels mapped to success, failure, unresolved, and infrastructure failure before
  rates are named?
- Do any residual buckets hide partially failed runs or other claim-relevant failures?
- Are denominators explicit and consistent across the table, figure, caption, and prose?
- Do equations use formal count variables such as `N_{\mathrm{failure}}` and
  `N_{\mathrm{scorable}}`, with no raw `#` count notation?
- Are strong and fair baselines included?
- Are cost, latency, or compute needed?
- Is robustness or generalization needed?
- Is human evaluation needed?
- Is failure analysis needed?
- Are only favorable results shown?

## Common Metric Risks

- Proxy metric improves but task outcome does not.
- Average score hides severe failure modes.
- Main metric ignores cost.
- Benchmark is too easy or saturated.
- Ablation does not isolate the claimed mechanism.
