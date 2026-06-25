# Finance Gates

Stop and ask before drafting or strengthening any claim when these are unresolved:

- data source or vendor
- sample period and inclusion/exclusion rules
- return construction or accounting variable definition
- benchmark or factor model
- transaction cost / slippage / turnover treatment for trading claims
- identification strategy for causal claims
- standard-error clustering or dependence structure
- out-of-sample or validation split for predictive claims

## Input Sufficiency Check

Run this before loading a long workflow or drafting long-form prose.

Input sufficiency: enough / partial / insufficient.

- `enough`: the route is clear and the available evidence, draft, package, table output, or display
  source is sufficient to act without inventing finance facts.
- `partial`: the route is clear but some facts constrain the output; proceed only within the safe
  boundary, list blockers, and avoid expanding the task.
- `insufficient`: the route, evidence anchor, manuscript identity, model/table source, or requested
  artifact is unclear; ask for the smallest missing input before long-form work.

Apply this check to `full-draft-from-evidence`, `package-completion`, `draft-revision`,
`audit-only`, `figure-only`, `table-only`, `citation-only`, `submission-review`, and
`revision-response`. For partial or insufficient inputs, report severity and correction priority
instead of burying the issue in process notes.

## Blocking Gates

Block "submission-ready" wording when any applies:

- version target or paper type is unknown
- a causal statement lacks explicit identification assumptions
- a backtest/trading claim omits transaction costs, turnover, slippage, or benchmark
- a return/alpha claim lacks sample window, universe, and factor/benchmark definition
- statistical significance is reported without economic magnitude for a central claim
- the Contribution And Belief-Update Gate is blocked or the paper lacks a one-sentence
  contribution contract
- central results are written as a table tour instead of passing the Results Narrative Gate
- `writing_craft_status`, `belief_update_status`, or `results_narrative_status` is blocked
- data/vendor permissions, replication package, or online appendix requirements are unresolved
