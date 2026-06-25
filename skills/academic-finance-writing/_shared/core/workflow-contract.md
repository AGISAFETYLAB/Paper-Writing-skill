# Finance Core Workflow

This always-loaded core file owns cross-stage invariants and ledger schemas. Workflow route files
own the state machine, stage-specific loading, and stop gates.

## Core Ledger Contract

For full-draft and major revision workflows:

1. Establish paper identity: version target, target venue if any, paper type, selected finance
   domain adapter, economic setting, data source, sample window, unit of observation, method/model,
   method family, identification strategy, benchmark, evidence boundary, and data/code disclosure
   status.
2. Build the Finance Evidence Ledger with source, sample, model, benchmark, economic magnitude, and
   robustness status for every central claim.
3. Choose section architecture from the selected structural paper-type reference. Do not treat a
   finance domain or method as `paper_type`; record the selected finance domain adapter and method
   family separately and load their references only after the structural profile is selected.
4. Build a Display-Item Plan before drafting results. Apply the backend-neutral Display Choice Gate
   before choosing Python or R: decide whether each claim needs a figure, editable LaTeX table,
   composite, or appendix display; record `primary_evidence_role`, `display_choice_rationale`,
   `alternative_considered`, and `duplication_check`; then choose display families from the selected
   R/Python finance chart catalog when rendering is needed. For tables, apply the Finance Table
   Design Gate: record table family, skeleton, payoff sentence, venue override, content hygiene,
   source_table_to_script_map, page_budget_cost, and appendix destination.
5. Draft from the economic question outward: puzzle -> setting/identification -> data/model ->
   evidence -> economic interpretation -> limitations.
6. Apply the Finance Writing Craft Gate before approving Writing Policy, Paper Framework, and the
   final draft: record the one-sentence contribution contract, `belief_update_status`,
   `results_narrative_status`, and `writing_craft_status`; enforce the Paragraph Evidence Contract;
   require the Results Narrative Gate for results prose; and use the
   Title-Abstract-Introduction Scorecard before submission-readiness wording.
7. Build a Citation Evidence Ledger for finance/economics papers, methods, data, software, and
   institutional facts before treating a claim as supported.
8. Build a Research Workflow Ledger for dataset profile, code-output map, Script Registry / Code
   Sweep status, replication package, data/code availability, title page, JEL codes, disclosures,
   and Internet Appendix.
9. Build visual/layout and submission attachment status rows: `visual_asset_qa_status`,
   `compiled_layout_qa_status`, `layout_manual_inspection_status`,
   `central_result_uncertainty_status`, `submission_attachment_status`, and
   `replication_package_status`.
10. Run reviewer-risk checks for contribution, execution, exposition, bias, benchmark,
   identification, backtest, and reproducibility.

Do not run econometric analyses, alter results, or invent missing results. If the user asks for a
demo or test paper with synthetic data, label all data as synthetic and keep claims non-advisory.

## Finance Evidence Ledger

| claim | data/model source | sample/window | benchmark/specification | economic magnitude | robustness | status |
|---|---|---|---|---|---|---|

Allowed statuses: `supported`, `partial`, `unsupported_until_verified`, `needs_user_evidence`.

## Display-Item Plan

| display | type | primary_evidence_role | manuscript location | claim supported | display_choice_rationale | alternative_considered | duplication_check | source asset/code | table_family/source_table_to_script_map | page_budget_cost/appendix destination | palette profile | placement width | float env | final size | QA notes | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Allowed statuses: `planned`, `source_available`, `asset_rendered`, `audited`, `blocked`.

## Citation Evidence Ledger

| claim/source need | citation key | source identity | verification status | action |
|---|---|---|---|---|

Allowed statuses: `supported`, `partial`, `not verified`, `unsupported_until_verified`.

## Research Workflow Ledger

| item | evidence | status | blocker |
|---|---|---|---|
| dataset profile | source/window/unit/variables | needs_user_evidence | yes/no |
| code-output map | table/figure to script | needs_user_evidence | yes/no |
| Script Registry / Code Sweep | registry path, drift status, stale/orphan output status | needs_user_evidence | yes/no |
| replication package | README/data/code/license | needs_user_evidence | yes/no |

## Writing Craft Status

| gate | evidence | status | blocker |
|---|---|---|---|
| one-sentence contribution contract | reader belief update and closest benchmark | partial | yes/no |
| belief_update_status | pass / partial / blocked | partial | yes/no |
| results_narrative_status | pass / partial / blocked | partial | yes/no |
| writing_craft_status | pass / partial / blocked | partial | yes/no |

## Package QA Status

| gate | evidence | status | blocker |
|---|---|---|---|
| visual_asset_qa_status | `audit_visual_assets.py` output or not_applicable rationale | pass / blocked / not_applicable | yes/no |
| compiled_layout_qa_status | layout summary plus contact sheet/page PNGs | pass / partial / blocked | yes/no |
| layout_manual_inspection_status | contact sheet or page PNG inspection note | pass / partial / blocked / not_performed | yes/no |
| central_result_uncertainty_status | SE/t-stat/p-value/CI/bootstrap interval or descriptive downgrade | pass / partial / blocked / not_applicable | yes/no |
| submission_attachment_status | title page, anonymity, COI, funding, acknowledgements | pass / partial / blocked / not_applicable | yes/no |
| replication_package_status | script registry, code sweep, environment manifest, repository plan | pass / partial / blocked / not_applicable | yes/no |
