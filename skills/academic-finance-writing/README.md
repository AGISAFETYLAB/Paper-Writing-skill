# Academic Finance Writing

<p>
  <a href="README.md"><strong>简体中文版</strong></a>
  &nbsp;|&nbsp;
  <a href="README_EN.md">English</a>
</p>

`academic-finance-writing` 是 `Paper Writing Skill` 中可单独下载和安装的金融论文写作包，适用于金融经济学、资产定价、市场微观结构、公司金融、会计、银行、风险、portfolio、trading/backtest、fintech、event study、policy evaluation、theory model 和 econometrics paper。

## 单独安装

从完整仓库中只安装金融包：

```bash
git clone https://github.com/AI45Lab/Paper-Writing-Skill.git
cd Paper-Writing-Skill
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/academic-finance-writing/ "$CODEX_HOME/skills/academic-finance-writing/"
```

如果已经进入 `skills/academic-finance-writing/` 目录：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-finance-writing"
rsync -a --delete ./ "$CODEX_HOME/skills/academic-finance-writing/"
```

Claude Code 全局安装：

```bash
mkdir -p "$HOME/.claude/skills/academic-finance-writing"
rsync -a --delete skills/academic-finance-writing/ "$HOME/.claude/skills/academic-finance-writing/"
```

Windows PowerShell：

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\academic-finance-writing"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path "skills\academic-finance-writing\*" -Destination $Target -Recurse -Force
```

## 包结构

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

| 子 skill | 职责 |
|---|---|
| `academic-writing` | 金融论文主流程：Writing Policy、Paper Framework、LaTeX project、section drafting、revision response。 |
| `academic-figure` | 回归表、summary statistics、event-study plot、portfolio/factor panel、robustness/appendix display 和 QA。 |
| `academic-citation` | 金融/经济学引用、数据和软件引用、BibTeX/reference-list integrity。 |
| `academic-review` | 投稿前 review、identification/econometrics risk、data-code、online appendix 和 page-window gate。 |

## 核心流程

```text
Evidence / Draft / Tables
  -> Writing Policy -> 用户确认
  -> Paper Framework -> 用户确认
  -> LaTeX package / revision
  -> citation / data-code / submission review
```

该包只写作和修订论文 artifact，不提供投资建议，不运行交易、回测或模拟，不编造 alpha、标准误、数据权限、稳健性结果、引用或代码仓库。

## 会议和期刊支持

- Journals：Journal of Finance、Journal of Financial Economics、Review of Financial Studies、Journal of Financial and Quantitative Analysis、Review of Finance、Management Science、AEA journals、QJE、Econometrica、Review of Economic Studies。
- Conferences / platforms：AFA、WFA、EFA、SFS Cavalcade、FMA、SSRN、NBER、CEPR。
- Templates / packages：generic finance working paper、AEA journal shell、Elsevier `elsarticle` assets。

真实投稿前必须核对目标 venue 最新 instructions；页数、匿名、title page、appendix、data/code policy 和模板合规性会进入 submission package gate。

## 示例请求

```text
请用 academic-finance-writing 根据这个事件研究结果写 Paper Framework，目标是 working paper 版本，先停下来确认。
Use academic-finance-writing to revise this asset-pricing manuscript for Journal of Finance style.
请用 academic-finance-writing 检查这篇公司金融论文的 identification、robustness 和 data-code 风险。
请用 academic-finance-writing 把这些回归结果整理成 finance paper 的 LaTeX tables。
```
