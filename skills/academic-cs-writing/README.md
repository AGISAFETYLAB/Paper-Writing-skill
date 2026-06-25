# Academic CS Writing

`academic-cs-writing` 是 `Academic Writing Skill` 中可单独下载和安装的计算机学科论文写作包，适用于 CS、AI/ML、NLP、CV、HCI、系统、数据挖掘、benchmark、dataset 和 software-tool paper。

English: [README_EN.md](README_EN.md)

## 单独安装

从完整仓库中只安装 CS 包：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-cs-writing"
rsync -a --delete ./ "$CODEX_HOME/skills/academic-cs-writing/"
```

如果在仓库根目录执行：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/academic-cs-writing/ "$CODEX_HOME/skills/academic-cs-writing/"
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
