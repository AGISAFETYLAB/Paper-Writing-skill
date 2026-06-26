# Academic Medicine Writing

<p>
  <a href="README.md"><strong>简体中文版</strong></a>
  &nbsp;|&nbsp;
  <a href="README_EN.md">English</a>
</p>

`academic-medicine-writing` 是 `Paper Writing Skill` 中可单独下载和安装的医学论文写作包，适用于临床研究、生物医学、公共卫生、诊断研究、治疗/安全性研究、预测模型、系统综述、case report 和 health-economics manuscript。

## 单独安装

从完整仓库中只安装医学包：

```bash
git clone <repo-url> Paper-Writing-Skill
cd Paper-Writing-Skill
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/academic-medicine-writing/ "$CODEX_HOME/skills/academic-medicine-writing/"
```

如果已经进入 academic-medicine-writing 包目录：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-medicine-writing"
rsync -a --delete ./ "$CODEX_HOME/skills/academic-medicine-writing/"
```

Claude Code 全局安装：

```bash
mkdir -p "$HOME/.claude/skills/academic-medicine-writing"
rsync -a --delete skills/academic-medicine-writing/ "$HOME/.claude/skills/academic-medicine-writing/"
```

Windows PowerShell：

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\academic-medicine-writing"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path "skills\academic-medicine-writing\*" -Destination $Target -Recurse -Force
```

## 包结构

```text
academic-medicine-writing/
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
| `academic-writing` | 医学 manuscript 主流程：研究类型判断、Writing Policy、Paper Framework、正文/投稿包组织。 |
| `academic-figure` | 临床图表、baseline table、flow diagram、forest plot、Kaplan-Meier-style display 和图表 QA。 |
| `academic-citation` | 医学引用检索、Vancouver/AMA-style 参考文献、指南/试验注册/报告规范引用审计。 |
| `academic-review` | 投稿前检查、报告规范、伦理/注册/数据共享/利益冲突声明和 reviewer-risk。 |

## 核心流程

```text
Evidence / Protocol / Results
  -> Writing Policy -> 用户确认
  -> Paper Framework -> 用户确认
  -> manuscript / tables / references
  -> reporting checklist / submission review
```

该包只写作和修订 manuscript artifact，不提供医疗建议，不诊断或治疗，不运行分析，不编造患者数据、批准号、注册号、结果或引用。

## 会议和期刊支持

- Venue families：通用医学期刊、高影响临床期刊、公共卫生期刊、Nature-family biomedical journals。
- Reporting standards：CONSORT、STROBE、PRISMA、STARD、TRIPOD 等。
- Submission checks：ICMJE-style ethics、consent、trial registration、data availability、funding、competing interests、supplementary/source data。

真实投稿前必须核对目标期刊最新 author instructions；不确定的伦理、注册、数据和格式要求会被标记为 open decision 或 blocked。

## 示例请求

```text
请用 academic-medicine-writing 根据这个队列研究目录生成 Writing Policy，目标期刊是 JAMA，先不要写正文。
请用 academic-medicine-writing 把这个 Results section 改成医学论文风格，但不要改变任何数值。
Use academic-medicine-writing to audit this manuscript for STROBE and data availability.
请用 academic-medicine-writing 做 PRISMA flow diagram 和投稿前引用检查。
```
