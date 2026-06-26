# Academic CS Writing

<p>
  <a href="README.md"><strong>简体中文版</strong></a>
  &nbsp;|&nbsp;
  <a href="README_EN.md">English</a>
</p>

`academic-cs-writing` 是 `Paper Writing Skill` 中可单独下载和安装的计算机学科论文写作包，适用于 CS、AI/ML、NLP、CV、HCI、系统、数据挖掘、benchmark、dataset 和 software-tool paper。

## 单独安装

从完整仓库中只安装 CS 包：

```bash
git clone https://github.com/AGISAFETYLAB/Paper-Writing-skill.git
cd Paper-Writing-skill
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete --delete-excluded --exclude '_local/' --exclude 'SKILL-FLOW.md' skills/academic-cs-writing/ "$CODEX_HOME/skills/academic-cs-writing/"
```

如果已经进入 `skills/academic-cs-writing/` 目录：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-cs-writing"
rsync -a --delete --delete-excluded --exclude '_local/' --exclude 'SKILL-FLOW.md' ./ "$CODEX_HOME/skills/academic-cs-writing/"
```

Claude Code 全局安装：

```bash
mkdir -p "$HOME/.claude/skills/academic-cs-writing"
rsync -a --delete --delete-excluded --exclude '_local/' --exclude 'SKILL-FLOW.md' skills/academic-cs-writing/ "$HOME/.claude/skills/academic-cs-writing/"
```

Windows PowerShell：

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\academic-cs-writing"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path "skills\academic-cs-writing\*" -Destination $Target -Recurse -Force
```

## 包结构

复制整个 `academic-cs-writing/` 目录即可单独运行，不依赖医学、金融或仓库根目录：

```text
academic-cs-writing/
  SKILL.md
  _shared/
  skills/
    academic-writing/
    academic-figure/
    academic-citation/
    academic-review/
```

| 子 skill | 职责 |
|---|---|
| `academic-writing` | 主流程：Writing Policy、Paper Framework、LaTeX project、section drafting，并在需要时委托图表、引用和 review。 |
| `academic-figure` | 论文图和表，包括数据图、schematic、picture-style 图、表格设计和 QA。 |
| `academic-citation` | 引文检索、BibTeX、引用覆盖和参考文献审计。 |
| `academic-review` | 投稿前 review、静态审计、claim-evidence 检查和 readiness gate。 |

## 核心流程

```text
Workspace / Draft
  -> Writing Policy -> 用户确认
  -> Paper Framework -> 用户确认
  -> LaTeX / section drafting
  -> figure / citation / review gates
```

该包只处理论文 artifact 的写作和修订，不运行实验，不编造结果、引用、指标、数据集或代码仓库。

## 会议和期刊支持

- Conferences：ICLR、NeurIPS、ICML、ACL、EMNLP、NAACL、CVPR、ICCV/ECCV、AAAI/IJCAI、KDD/WWW/SIGIR、CHI/UIST。
- Journals：JMLR、IEEE TPAMI、Nature、Nature Communications，以及 generic journal profile。

目标 venue 的最新 CFP / author instructions 仍是最终依据；内置 venue card 主要用于规划页数、匿名、模板、补充材料和投稿前风险。

## 示例请求

```text
请用 academic-cs-writing 根据这个实验目录写一篇 AI benchmark paper，先停在 Writing Policy。
Use academic-cs-writing to revise the Introduction and Related Work for an ICLR submission.
请用 academic-cs-writing 检查这篇 EMNLP 论文的引用覆盖和 claim-evidence 风险。
请用 academic-cs-writing 把这组实验结果做成论文图表。
```
