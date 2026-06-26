# Paper Writing Skill

<p><b>简体中文</b> · <a href="README_EN.md">English</a></p>

`Paper Writing Skill` 是一个面向 AI 论文写作助手的多学科 skill 包，覆盖论文规划、初稿生成、章节改写、论文润色、图表表达、引用核查和投稿前审查等常见写作任务。它不是简单的“润色模板”，而是把论文构思、证据组织、章节写作、语言表达、图表设计和审稿风险拆成可执行的写作流程，让 AI 在生成和修改论文 artifact 时更像一个真正理解学术写作约束的助手。

目前已开发学科：

- `academic-cs-writing`：计算机、AI/ML、NLP、CV、HCI、系统、数据挖掘等。
- `academic-medicine-writing`：医学、临床、生物医学、公共卫生、诊断、预测模型、系统综述等。
- `academic-finance-writing`：金融、金融经济学、资产定价、公司金融、会计、银行、风险、金融计量等。

后续还会继续开发和补充其他学科方向。

## 写作理念与参考来源

该 skill 的写作方式提炼自被广泛认可的科研写作经验，具体包括：

- learning_research — 彭思达的科研经验：<https://github.com/pengsida/learning_research/tree/master>
- Ten Tips for Writing CS Papers — Sebastian Nowozin：<https://www.nowozin.net/sebastian/blog/ten-tips-for-writing-cs-papers-part-1.html>
- Writing a Good Introduction — Henning Schulzrinne，源自 Jim Kurose：<https://www.cs.columbia.edu/~hgs/etc/intro-style.html>
- The Science of Scientific Writing — Gopen and Swan：<https://inpp.ohio.edu/~meisel/PHYS6751/file/ScientificWriting_GGopenJSwanAmSci1990.pdf>
- How to write a good CVPR submission — Bill Freeman：<https://www.cs.ryerson.ca/~wangcs/resources/How-to-write-a-good-CVPR-submission.pdf>
- How to Get Your SIGGRAPH Paper Rejected — Jim Kajiya：<https://www.siggraph.org/sites/default/files/kajiya.pdf>
- Writing Flow: How to Make Your Writing Flow — MasterClass：<https://www.masterclass.com/articles/writing-flow>
- The Four Levels of Flow in Writing — Anthony Risko：<https://www.grammarflip.com/blog/the-four-levels-of-flow-in-writing-what-it-means-when-writing-flows/>

我们的目标是让 AI 学习这些真实可用的论文写作经验，使生成的论文更贴近真实研究者的写作习惯与表达风格。

## 核心流程

Paper Writing Skill 会先根据用户请求进入对应学科包，再处理具体写作任务。完整初稿通常按 `Writing Policy -> 用户确认 -> Paper Framework -> 用户确认 -> 正文写作与修订` 推进；如果用户只需要章节改写、论文润色、图表、引用核查或投稿前审稿，也可以直接进入对应任务，不必走完整初稿流程。

为了避免“一键生成”的初稿不符合真实论文写作习惯，Paper Writing Skill 在生成完整初稿之前设置了两个检查点：agent 必须分别在 `Writing Policy` 和 `Paper Framework` 阶段停下来，将原本可能被静默决定的内容展示给作者确认或修改，包括论文身份、证据边界、目标 venue、section 结构和图表计划等。

<details>
<summary>查看核心流程图</summary>

```text
┌──────────────────────────────────────────────────────────────┐
│                    Paper Writing Skill 工作流                 │
│                                                              │
│   用户输入：材料 / 草稿 / 实验目录 / 写作任务                  │
│         │                                                    │
│         ▼                                                    │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐            │
│   │ 学科路由 │────▶│ 任务判断 │────▶│ 目标venue│            │
│   │ CS/医学/ │     │ 初稿/专项│     │ 模板约束 │            │
│   │ 金融     │     │          │     │          │            │
│   └──────────┘     └──────────┘     └──────────┘            │
│                            │                                 │
│              ┌─────────────┴─────────────┐                  │
│              ▼                           ▼                  │
│   ┌──────────────┐            ┌──────────────┐              │
│   │ 完整初稿流程 │            │ 专项任务流程 │              │
│   │ Writing      │            │ 润色 / 图表  │              │
│   │ Policy       │            │ 引用 / 审稿  │              │
│   │ Framework    │            │              │              │
│   └──────────────┘            └──────────────┘              │
│              │                           │                  │
│              └─────────────┬─────────────┘                  │
│                            ▼                                 │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐            │
│   │ 正文生成 │────▶│ 图表引用 │────▶│ 投稿前检查│            │
│   │ 与修订   │     │ 质量控制 │     │ 版面/规范│            │
│   └──────────┘     └──────────┘     └──────────┘            │
│         │                                                    │
│         ▼                                                    │
│   输出：manuscript / figures / references / submission checks│
└──────────────────────────────────────────────────────────────┘
```

</details>

## 使用建议

建议在开始前告诉 agent 你想投稿的会议或期刊，例如 `EMNLP`、`JAMA Network Open` 或 `Journal of Finance`。这能帮助 agent 选择更合适的模板、章节结构、篇幅约束、图表习惯和投稿前检查规则。

## 图表设计

我们对论文图表设计做了单独强化，覆盖计算机、医学、金融等多学科论文中的常见图表场景，包括结果对比、趋势变化、不确定性展示、诊断评估、生存分析、综述证据、组学与健康经济学展示等，并重点关注图表类型选择、版式、配色、信息密度和可读性。下表为部分展示。

<table>
  <thead>
    <tr>
      <th align="left">Chart family</th>
      <th align="center">PDF 示例</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Bar and comparison</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/01_bar_comparison.pdf">
          <img src="assets/readme/chart-gallery/png_previews/01_bar_comparison_page01.png" width="320" alt="Bar and comparison charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Line / longitudinal</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/02_line_longitudinal.pdf">
          <img src="assets/readme/chart-gallery/png_previews/02_line_longitudinal_page01.png" width="320" alt="Line and longitudinal charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Scatter / Pareto</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/03_scatter_pareto.pdf">
          <img src="assets/readme/chart-gallery/png_previews/03_scatter_pareto_page01.png" width="320" alt="Scatter and Pareto charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Distribution / uncertainty</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/05_distribution_uncertainty.pdf">
          <img src="assets/readme/chart-gallery/png_previews/05_distribution_uncertainty_page01.png" width="320" alt="Distribution and uncertainty charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Survival / time-to-event</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/06_survival_time_to_event.pdf">
          <img src="assets/readme/chart-gallery/png_previews/06_survival_time_to_event_page01.png" width="320" alt="Survival and time-to-event charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Profile summaries</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/07_profile_summaries.pdf">
          <img src="assets/readme/chart-gallery/png_previews/07_profile_summaries_page01.png" width="320" alt="Profile summary charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Effect / review evidence</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/07_effect_review.pdf">
          <img src="assets/readme/chart-gallery/png_previews/07_effect_review_page01.png" width="320" alt="Effect estimates and review evidence PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Diagnostic / extended</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/09_diagnostic_extended.pdf">
          <img src="assets/readme/chart-gallery/png_previews/09_diagnostic_extended_page01.png" width="320" alt="Diagnostic and extended charts PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Biomarker / omics</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/09_biomarker_omics.pdf">
          <img src="assets/readme/chart-gallery/png_previews/09_biomarker_omics_page01.png" width="320" alt="Biomarker and omics displays PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Qualitative / composite</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/10_qualitative_composites.pdf">
          <img src="assets/readme/chart-gallery/png_previews/10_qualitative_composites_page01.png" width="320" alt="Qualitative and composite panels PDF preview">
        </a>
      </td>
    </tr>
    <tr>
      <td><strong>Global health / economics</strong></td>
      <td align="center" width="72%">
        <a href="assets/readme/chart-gallery/pdfs/11_global_health_economics.pdf">
          <img src="assets/readme/chart-gallery/png_previews/11_global_health_economics_page01.png" width="320" alt="Global-health and economic displays PDF preview">
        </a>
      </td>
    </tr>
  </tbody>
</table>

## 安装方式

### 快速安装

您可以直接把项目地址 `https://github.com/AGISAFETYLAB/Paper-Writing-skill.git` 复制给你的 AI agent，让它按照本 README 安装完整包或某个学科包。

### 仓库下载：

```bash
git clone https://github.com/AGISAFETYLAB/Paper-Writing-skill.git
cd Paper-Writing-skill
```

### PDF 编译环境（可选）

`paper-writing-skill` 可以生成论文源码、图表和投稿前检查结果。如果需要把生成的 LaTeX 论文包继续编译成 PDF，运行环境需要具备 LaTeX 工具链，例如 `latexmk`、`xelatex` / `pdflatex` 以及模板所需字体。

Ubuntu / Debian 最小安装：

```bash
sudo apt-get update
sudo apt-get install -y latexmk texlive-xetex texlive-latex-extra fonts-noto-cjk
```

常用编译命令：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

部分会议或期刊模板可能还需要额外的 TeX Live 宏包或字体。如果安装后 agent 仍找不到编译环境，建议在对话中显式指定可用环境或命令路径，例如要求 agent 在某个 conda 环境、容器或系统路径下运行 `latexmk`。

### Codex 安装

完整安装，Mac / Linux：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/paper-writing-skill"
rsync -a --delete --exclude '.git/' ./ "$CODEX_HOME/skills/paper-writing-skill/"
```

完整安装，Windows PowerShell：

```powershell
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$Target = Join-Path $CodexHome "skills\paper-writing-skill"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path ".\*" -Destination $Target -Recurse -Force
Remove-Item -Path (Join-Path $Target ".git") -Recurse -Force -ErrorAction SilentlyContinue
```

安装后可以直接让路由 skill 选择学科：

```text
请用 paper-writing-skill 帮我根据这个实验目录写一篇 AI benchmark paper，先停在 Writing Policy。
Use paper-writing-skill to review this finance manuscript for submission readiness.
```

### Claude Code 安装

完整安装，Mac / Linux：

```bash
mkdir -p "$HOME/.claude/skills/paper-writing-skill"
rsync -a --delete --exclude '.git/' ./ "$HOME/.claude/skills/paper-writing-skill/"
```

完整安装，Windows PowerShell：

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\paper-writing-skill"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path ".\*" -Destination $Target -Recurse -Force
Remove-Item -Path (Join-Path $Target ".git") -Recurse -Force -ErrorAction SilentlyContinue
```

### 只安装一个学科包

每个学科包都必须能独立运行；复制 `skills/<学科包>/` 一个目录即可安装，不依赖仓库根目录或其他学科包。

下面以 CS 为例。医学或金融用户把 `academic-cs-writing` 替换为 `academic-medicine-writing` 或 `academic-finance-writing` 即可。

Mac / Linux：

```bash
SKILL_HOME="${CODEX_HOME:-$HOME/.codex}/skills"
# Claude Code 用户可改为：SKILL_HOME="$HOME/.claude/skills"
mkdir -p "$SKILL_HOME/academic-cs-writing"
rsync -a --delete "skills/academic-cs-writing/" "$SKILL_HOME/academic-cs-writing/"
```

## 三个学科包

| 学科包 | 适用任务 | 内部子 skill |
|---|---|---|
| `skills/academic-cs-writing/` | CS/AI 论文规划、写作、润色、修改、图表、引用、投稿前检查 | `academic-writing`、`academic-figure`、`academic-citation`、`academic-review` |
| `skills/academic-medicine-writing/` | 医学论文写作与润色、临床研究、公共卫生、系统综述、报告规范和投稿材料 | `academic-writing`、`academic-figure`、`academic-citation`、`academic-review` |
| `skills/academic-finance-writing/` | 金融论文写作与润色、金融计量、事件研究、资产定价、公司金融、working paper 和投稿包 | `academic-writing`、`academic-figure`、`academic-citation`、`academic-review` |

子 skill 的分工很简单：`academic-writing` 负责主流程，`academic-figure` 负责图表，`academic-citation` 负责引文和 BibTeX，`academic-review` 负责审稿视角和投稿前检查。

## 会议和期刊支持

| 学科 | 已内置或重点支持的 venue 类型 |
|---|---|
| CS | ICLR、NeurIPS、ICML、ACL、EMNLP、NAACL、CVPR、ICCV/ECCV、AAAI/IJCAI、KDD/WWW/SIGIR、CHI/UIST；JMLR、IEEE TPAMI、Nature、Nature Communications 和通用 journal profile。 |
| Medicine | 通用医学期刊、高影响临床期刊、公共卫生期刊、Nature-family biomedical journals；支持 CONSORT、STROBE、PRISMA、STARD、TRIPOD 等报告规范和 ICMJE-style statements。 |
| Finance | Journal of Finance、Journal of Financial Economics、Review of Financial Studies、JFQA、Review of Finance、Management Science、AEA journals、QJE、Econometrica、REStud；AFA/WFA/EFA/SFS/FMA、SSRN、NBER、CEPR 等会议和 working-paper 平台。 |

真实投稿前仍应以目标会议/期刊的最新 official instructions 为准。skill 会把未确认的格式、页数、匿名、数据代码和声明要求标记为 open decision 或 blocked。

## 示例请求

```text
请用 paper-writing-skill 根据 /path/to/project 写一篇 CS 论文，目标会议是 EMNLP。
请用 academic-medicine-writing 根据这个临床队列实验目录生成 JAMA 风格的初稿。
Use academic-finance-writing to revise my asset-pricing working paper and check citation coverage.
请用 academic-cs-writing 润色这篇论文的 Introduction，保持原意和实验结论不变。
请用 academic-cs-writing 帮我把这份实验结果画成图表。
请用 academic-medicine-writing 做投稿前自检，重点检查 STROBE、伦理声明、数据可用性和引用。
```

## 维护声明

本仓库仍在持续开发中，欢迎大家试用、反馈问题和提出改进建议。我们会第一时间处理影响安装、独立运行、学科路由、写作流程和输出质量的问题，并尽快更新 README、skill 指令和校验脚本。若在使用中发现某个 venue、学科场景或写作任务支持不足，也欢迎反馈具体场景和复现方式。

## 贡献者

<p>
  <a href="https://github.com/Ssjoo02"><img src="assets/readme/contributors/ssjoo02.png" width="60" alt="Contributor" /></a>
  <a href="https://github.com/KimiYukikaze"><img src="assets/readme/contributors/kimiyukikaze.png" width="60" alt="Contributor" /></a>
  <a href="https://github.com/tryedk"><img src="assets/readme/contributors/tryedk.png" width="60" alt="Contributor" /></a>
  <a href="https://github.com/adwardlee"><img src="assets/readme/contributors/adwardlee.png" width="60" alt="Contributor" /></a>
</p>
