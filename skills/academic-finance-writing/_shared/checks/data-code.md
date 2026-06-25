# Finance Data, Code, And Appendix Planning

Finance manuscripts often rely on licensed or restricted data. Plan disclosure without inventing
access rights.

Load `_shared/checks/research-workflow.md` when the task needs dataset profiling, code-output mapping,
replication planning, or a data-code readiness verdict.

| Item | Required detail |
|---|---|
| Data source | vendor/database/official source, access route, restrictions |
| Sample construction | dates, universe, inclusion/exclusion, survivorship handling |
| Variables | definitions, transformations, winsorization, lagging |
| Code | scripts, environment, replication sequence, proprietary constraints |
| Internet appendix | variable definitions, extra robustness, proofs, tables, data cleaning |
| Disclosure | funding, conflicts, financial relationships |

## Data-Code And Replication Plan

The Paper Framework must include:

- source inventory and access boundary
- sample construction and variable-definition inventory
- table/figure to code-output map
- replication package status
- Internet Appendix contents
- unresolved permissions or repository blockers

Use `needs_user_evidence` for missing code, permissions, or repository records. Do not invent
replication status.

Data/code statement patterns:

- public source: name source, stable URL/DOI/access date if available
- licensed source: state restrictions and that data cannot be redistributed
- proprietary/confidential source: state access constraints and replication limits
- synthetic/demo data: label it synthetic and non-investment, not evidence about real markets
