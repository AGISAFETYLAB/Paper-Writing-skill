# CS Table Type Overview QA

- Backend: LaTeX (`booktabs`, `tabularx`, `array`, `xcolor`) compiled with `latexmk`.
- Data: synthetic values for table taxonomy and layout inspection only.
- Major table categories: 15.
- Approximate subtype/use-case coverage: 55.
- Scope: CS academic paper tables covered by the `academic-figure` table workflow and table-design reference.
- Width policy: numeric full-width tables use `tabular*` with `@{\extracolsep{\fill}}`; prose-heavy tables use real `X`/`Y` wrapping columns; compact tables stay natural-width.

| # | Category | Subtypes | PDF |
|---:|---|---:|---|
| 1 | Main Result Scorecard | 4 | `pdfs/01_01_main_scorecard.pdf` |
| 2 | Multi-Dataset Matrix | 3 | `pdfs/02_02_multi_dataset_matrix.pdf` |
| 3 | Multi-Metric Tradeoff Table | 4 | `pdfs/03_03_multi_metric_tradeoff.pdf` |
| 4 | Ablation Table | 3 | `pdfs/04_04_ablation_table.pdf` |
| 5 | Hyperparameter Sensitivity Table | 3 | `pdfs/05_05_sensitivity_table.pdf` |
| 6 | Matched-Condition Delta Table | 3 | `pdfs/06_06_matched_condition_delta.pdf` |
| 7 | Data Split And Setup Table | 4 | `pdfs/07_07_data_split_setup.pdf` |
| 8 | Benchmark Taxonomy Or Protocol Table | 4 | `pdfs/08_08_benchmark_taxonomy_protocol.pdf` |
| 9 | Training Or Inference Configuration Table | 4 | `pdfs/09_09_training_configuration.pdf` |
| 10 | Error Or Failure Analysis Table | 4 | `pdfs/10_10_error_failure_analysis.pdf` |
| 11 | Qualitative Example Table | 4 | `pdfs/11_11_qualitative_examples.pdf` |
| 12 | Leaderboard, Complexity, Or Resource Table | 4 | `pdfs/12_12_leaderboard_complexity_resource.pdf` |
| 13 | Confusion Or Transition Matrix Table | 3 | `pdfs/13_13_confusion_transition_matrix.pdf` |
| 14 | Appendix Audit Or Inventory Table | 4 | `pdfs/14_14_appendix_audit_inventory.pdf` |
| 15 | Remote-Sensing MLLM Scorecard | 4 | `pdfs/15_15_remote_sensing_mllm_scorecard.pdf` |
