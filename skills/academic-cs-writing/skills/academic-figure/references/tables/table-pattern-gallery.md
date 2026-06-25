# Table Pattern Gallery

Use this only after the Table Contract is filled. The gallery is a local style reference, not a
prompt bank and not a mandate to force templates onto sparse or unusual tables.

## Core Skeletons

Default generation uses six core skeletons in `assets/table-patterns/`:

| Reader task | Start from | Avoid |
|---|---|---|
| headline method comparison | `full_width_numeric_scorecard.tex` | numeric `tabularx` with stretch labels |
| cross-dataset or cross-metric comparison | `multi_dataset_metric_matrix.tex` | ungrouped flat metric headers |
| ablation or sensitivity | `compact_ablation_or_sensitivity.tex` | stretching a small table full width |
| paired interventions or modes | `matched_condition_delta.tex` | repeated long condition names |
| taxonomy or protocol definitions | `wrapped_taxonomy_or_protocol.tex` | prose in `l/c/r` columns |
| split, setup, or source composition | `setup_or_split_summary.tex` | performance highlighting for protocol facts |

Preview the skeletons with:

```bash
python3 skills/academic-figure/scripts/render_table_patterns.py --output-dir /tmp/table-pattern-previews
```

Do not ship generated previews as paper output; render them in a paper workspace, temporary
directory, or test output directory.

## Local Reference Gallery

The 15-table CS reference gallery is copied into the skill at
`assets/table-patterns/reference-gallery/cs-table-type-overview/`. It contains PDFs, PNG previews,
source TeX, a manifest, and the contact sheet. Load it only for style regression, visual comparison,
or when the six skeletons are too coarse.

| # | Category | Use when |
|---:|---|---|
| 1 | Main Result Scorecard | headline method-vs-baseline comparison |
| 2 | Multi-Dataset Matrix | generality across datasets, tasks, or domains |
| 3 | Multi-Metric Tradeoff Table | quality, cost, robustness, or efficiency tradeoffs |
| 4 | Ablation Table | component necessity |
| 5 | Hyperparameter Sensitivity Table | robustness to thresholds or settings |
| 6 | Matched-Condition Delta Table | paired prompts, modes, or interventions |
| 7 | Data Split And Setup Table | train/dev/test or source composition |
| 8 | Benchmark Taxonomy Or Protocol Table | codes, phases, or protocol attributes |
| 9 | Training Or Inference Configuration Table | reproducibility settings |
| 10 | Error Or Failure Analysis Table | failure modes, counts, diagnostics |
| 11 | Qualitative Example Table | representative cases or outputs |
| 12 | Leaderboard, Complexity, Or Resource Table | ranking with efficiency/resource metrics |
| 13 | Confusion Or Transition Matrix Table | compact class-to-class counts |
| 14 | Appendix Audit Or Inventory Table | denominators, inclusion, checklist status |
| 15 | Remote-Sensing MLLM Scorecard | wide benchmark scorecard with dataset spanners |

Do not copy example claims, captions, labels, or numbers. Copy only the structural idea, then replace
all content from the current paper's source-backed evidence.
