# Finance Paper Type Index

Select `paper_type` for manuscript structure only. Do not use this axis for finance domain
(`asset-pricing`, `corporate-finance`, `banking`, `behavioral-finance`, `fintech`) or for method
(`event study`, `DiD`, `IV`, `RD`, `factor model`, `portfolio sort`, `structural estimation`,
`ML/text`, `backtest`). Those belong in domain and method references.

If the user names a paper type, use it when it matches a structural profile. If the request only
names a domain or method, select the closest structural profile and record the domain/method as a
separate planning field. Use `generic-finance-paper.md` as a provisional fallback when the type is
unknown, mixed, early-stage, or not safely captured by a specific profile.

Paper-type profiles are section-structure references only. They help the agent decide which sections
a finance paper probably needs and what each section must do. They are not venue templates, and they
do not set page limits.

## Source Basis

This index is grounded in official or publisher author guidance checked on 2026-06-23:

- Journal of Finance submissions describe ordinary article submission plus a Replications and
  Corrigenda section.
- Journal of Finance: Insights and Perspectives distinguishes concise Insights from commissioned
  Perspectives.
- AEA policy and AER guidance describe comments, replies, errata, and corrigenda.
- Elsevier financial-economics journal descriptions distinguish theoretical, empirical, policy,
  full-length, short-letter, review/survey, software/tool, and replication formats.
- Finance/accounting author guidelines from CRIBFB distinguish research, theoretical, review, and
  short communication manuscripts with section structures.
- JRFM author instructions define original research articles with IMRaD-like structure.
- Elsevier Research Elements, Data in Brief, MethodsX, and research-software journals define data,
  method, protocol, and software article routes.

## Type Selection Map

Use the most specific matching profile. If a paper has multiple contribution types, choose the one
that controls the main section structure, then borrow individual rows only after recording the
deviation.

| Paper type | Profile | Story center |
|---|---|---|
| Generic finance research paper | `generic-finance-paper.md` | Flexible research structure when the manuscript type is unknown, mixed, or early-stage. |
| Empirical research paper | `empirical-research-paper.md` | Original empirical finance/economics evidence, data construction, design, results, interpretation. |
| Theoretical model paper | `theoretical-model-paper.md` | Formal model, assumptions, equilibrium/result statements, proofs, intuition, implications. |
| Short insight / letter paper | `short-insight-letter-paper.md` | One concise original insight or short high-impact result. |
| Review / survey / perspective paper | `review-survey-perspective-paper.md` | Literature synthesis, organizing framework, active line of research, future agenda. |
| Comment / replication / corrigendum paper | `comment-replication-corrigendum-paper.md` | Post-publication comment, reply, replication, robustness sensitivity, correction, or erratum. |
| Data / method / software paper | `data-method-software-paper.md` | Reusable data, method/protocol, or software/resource contribution supporting finance research. |

## Common Mappings

| If the manuscript looks like... | Prefer this profile | Adjustment note |
|---|---|---|
| Corporate-finance, banking, asset-pricing, household-finance, market-microstructure, accounting, or fintech study with data and estimates | `empirical-research-paper.md` | Record the finance domain separately; load method references for identification and econometrics. |
| Formal asset-pricing, corporate-finance, banking, behavioral, or market-design model | `theoretical-model-paper.md` | Keep assumptions, equilibrium/results, proof plan, and economic intuition in the main structure. |
| Finance Research Letters style paper, JF: I&P Insight, or short letter built around one result | `short-insight-letter-paper.md` | Compress literature and robustness; keep the single insight and evidence self-contained. |
| JF: I&P Perspective, review article, survey article, research agenda, or field synthesis | `review-survey-perspective-paper.md` | Protect organizing framework and synthesis; do not write a paper-by-paper annotated bibliography. |
| Comment, reply, replication, corrigendum, erratum, or sensitivity analysis of a published article | `comment-replication-corrigendum-paper.md` | Make the target article, disputed claim, replication materials, and correction boundary explicit. |
| Data descriptor, method article, protocol, reusable code/software, or research object article | `data-method-software-paper.md` | Separate resource description from causal/economic claims; emphasize reuse, access, validation, and licensing. |
| Mixed or unclear finance draft | `generic-finance-paper.md` | Use provisionally and ask for confirmation at the Paper Framework gate. |
