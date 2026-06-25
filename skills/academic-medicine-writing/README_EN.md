# Academic Medicine Writing

<p align="center">
  <a href="README.md">简体中文版</a>
  &nbsp;|&nbsp;
  <a href="README_EN.md"><strong>English</strong></a>
</p>

`academic-medicine-writing` is the standalone medicine package inside `Academic Writing Skill`. It supports clinical, biomedical, public-health, diagnostic, treatment/safety, prediction-model, systematic-review, case-report, and health-economics manuscripts.

The default README is Chinese so repository viewers show the Chinese entry first.

## Install

Install only the medicine package from the full repository:

```bash
git clone https://github.com/AI45Lab/Academic-Writing-skill.git
cd Academic-Writing-skill
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
rsync -a --delete skills/academic-medicine-writing/ "$CODEX_HOME/skills/academic-medicine-writing/"
```

If you are already inside the academic-medicine-writing package directory:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-medicine-writing"
rsync -a --delete ./ "$CODEX_HOME/skills/academic-medicine-writing/"
```

Claude Code global install:

```bash
mkdir -p "$HOME/.claude/skills/academic-medicine-writing"
rsync -a --delete skills/academic-medicine-writing/ "$HOME/.claude/skills/academic-medicine-writing/"
```

Windows PowerShell:

```powershell
$Target = Join-Path $env:USERPROFILE ".claude\skills\academic-medicine-writing"
Remove-Item $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path "skills\academic-medicine-writing\*" -Destination $Target -Recurse -Force
```

## Layout

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

| Sub-skill | Responsibility |
|---|---|
| `academic-writing` | Medical manuscript workflow: study-type inference, Writing Policy, Paper Framework, manuscript and submission-package organization. |
| `academic-figure` | Clinical figures/tables, baseline tables, flow diagrams, forest plots, Kaplan-Meier-style displays, and QA. |
| `academic-citation` | Biomedical citation search, Vancouver/AMA-style references, guideline/trial/reporting citation audits. |
| `academic-review` | Submission checks, reporting guidelines, ethics/registration/data-sharing/conflict statements, and reviewer risk. |

## Core Workflow

```text
Evidence / Protocol / Results
  -> Writing Policy -> user confirmation
  -> Paper Framework -> user confirmation
  -> manuscript / tables / references
  -> reporting checklist / submission review
```

This package writes and revises manuscript artifacts only. It does not provide medical advice, diagnose, treat, run analyses, or invent patient data, approval numbers, registration IDs, results, or citations.

## Venue Support

- Venue families: general medical journals, high-impact clinical journals, public-health journals, Nature-family biomedical journals.
- Reporting standards: CONSORT, STROBE, PRISMA, STARD, TRIPOD.
- Submission checks: ICMJE-style ethics, consent, trial registration, data availability, funding, competing interests, supplementary/source data.

The target journal's current author instructions remain authoritative.

## Example Prompts

```text
Use academic-medicine-writing to generate a Writing Policy from this cohort-study workspace for JAMA, without drafting the manuscript yet.
Use academic-medicine-writing to revise this Results section without changing any numbers.
Use academic-medicine-writing to audit this manuscript for STROBE and data availability.
```
