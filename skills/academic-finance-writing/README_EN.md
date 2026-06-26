# Academic Finance Writing

<p>
  <a href="README.md">简体中文版</a>
  &nbsp;|&nbsp;
  <a href="README_EN.md"><strong>English</strong></a>
</p>

`academic-finance-writing` is the standalone finance package inside `Paper Writing Skill`. It supports financial economics, asset pricing, market microstructure, corporate finance, accounting, banking, risk, portfolio, trading/backtest, fintech, event-study, policy-evaluation, theory-model, and econometrics papers.

The default README is Chinese so repository viewers show the Chinese entry first.

## Install

Install only the finance package from the full repository:

```bash
git clone https://github.com/AGISAFETYLAB/Paper-Writing-skill.git
cd Paper-Writing-skill
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/academic-finance-writing/ "$CODEX_HOME/skills/academic-finance-writing/"
```

If you are already inside `skills/academic-finance-writing/`:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-finance-writing"
rsync -a --delete ./ "$CODEX_HOME/skills/academic-finance-writing/"
```

Claude Code global install:

```bash
mkdir -p "$HOME/.claude/skills/academic-finance-writing"
rsync -a --delete skills/academic-finance-writing/ "$HOME/.claude/skills/academic-finance-writing/"
```

Windows PowerShell:

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\academic-finance-writing"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path "skills\academic-finance-writing\*" -Destination $Target -Recurse -Force
```

## Layout

```text
academic-finance-writing/
  SKILL.md
  _shared/
  assets/templates/
  skills/
    academic-writing/
    academic-figure/
    academic-citation/
    academic-review/
```

| Sub-skill | Responsibility |
|---|---|
| `academic-writing` | Finance writing pipeline: Writing Policy, Paper Framework, LaTeX project, section drafting, and revision response. |
| `academic-figure` | Regression tables, summary statistics, event-study plots, portfolio/factor panels, robustness/appendix displays, and QA. |
| `academic-citation` | Finance/economics citations, data and software citations, BibTeX/reference-list integrity. |
| `academic-review` | Submission review, identification/econometrics risk, data-code, online appendix, and page-window gates. |

## Core Workflow

```text
Evidence / Draft / Tables
  -> Writing Policy -> user confirmation
  -> Paper Framework -> user confirmation
  -> LaTeX package / revision
  -> citation / data-code / submission review
```

This package writes and revises paper artifacts only. It does not provide investment advice, run trades/backtests/simulations, or invent alphas, standard errors, data permissions, robustness results, citations, or repositories.

## Venue Support

- Journals: Journal of Finance, Journal of Financial Economics, Review of Financial Studies, Journal of Financial and Quantitative Analysis, Review of Finance, Management Science, AEA journals, QJE, Econometrica, Review of Economic Studies.
- Conferences/platforms: AFA, WFA, EFA, SFS Cavalcade, FMA, SSRN, NBER, CEPR.
- Templates/packages: generic finance working paper, AEA journal shell, Elsevier `elsarticle` assets.

The target venue's current instructions remain authoritative.

## Example Prompts

```text
Use academic-finance-writing to build a Paper Framework from this event-study result, targeting a working-paper version first.
Use academic-finance-writing to revise this asset-pricing manuscript for Journal of Finance style.
Use academic-finance-writing to check identification, robustness, and data-code risks.
```
