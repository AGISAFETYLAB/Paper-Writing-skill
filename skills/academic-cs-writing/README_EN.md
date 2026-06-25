# Academic CS Writing

<p>
  <a href="README.md">简体中文版</a>
  &nbsp;|&nbsp;
  <a href="README_EN.md"><strong>English</strong></a>
</p>

`academic-cs-writing` is the standalone computer-science package inside `Academic Writing Skill`. It supports CS, AI/ML, NLP, CV, HCI, systems, data mining, benchmark, dataset, and software-tool papers.

The default README is Chinese so repository viewers show the Chinese entry first.

## Install

Install only the CS package from the full repository:

```bash
git clone https://github.com/AI45Lab/Academic-Writing-skill.git
cd Academic-Writing-skill
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/academic-cs-writing/ "$CODEX_HOME/skills/academic-cs-writing/"
```

If you are already inside `skills/academic-cs-writing/`:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-cs-writing"
rsync -a --delete ./ "$CODEX_HOME/skills/academic-cs-writing/"
```

Claude Code global install:

```bash
mkdir -p "$HOME/.claude/skills/academic-cs-writing"
rsync -a --delete skills/academic-cs-writing/ "$HOME/.claude/skills/academic-cs-writing/"
```

Windows PowerShell:

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\academic-cs-writing"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path "skills\academic-cs-writing\*" -Destination $Target -Recurse -Force
```

## Layout

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

| Sub-skill | Responsibility |
|---|---|
| `academic-writing` | Main pipeline: Writing Policy, Paper Framework, LaTeX project, section drafting, and delegation. |
| `academic-figure` | Paper figures and tables, including plots, schematics, picture-style figures, table design, and QA. |
| `academic-citation` | Citation search, BibTeX, citation coverage, and bibliography audits. |
| `academic-review` | Pre-submission review, static audits, claim-evidence checks, and readiness gates. |

## Core Workflow

```text
Workspace / Draft
  -> Writing Policy -> user confirmation
  -> Paper Framework -> user confirmation
  -> LaTeX / section drafting
  -> figure / citation / review gates
```

This package writes and revises paper artifacts only. It does not run experiments or invent results, citations, metrics, datasets, or repositories.

## Venue Support

- Conferences: ICLR, NeurIPS, ICML, ACL, EMNLP, NAACL, CVPR, ICCV/ECCV, AAAI/IJCAI, KDD/WWW/SIGIR, CHI/UIST.
- Journals: JMLR, IEEE TPAMI, Nature, Nature Communications, and generic journal profile.

The target venue's latest CFP or author instructions remain authoritative.

## Example Prompts

```text
Use academic-cs-writing to draft a Writing Policy for this AI benchmark paper.
Use academic-cs-writing to revise the Introduction and Related Work for an ICLR submission.
Use academic-cs-writing to check citation coverage and claim-evidence risk for this EMNLP paper.
```
