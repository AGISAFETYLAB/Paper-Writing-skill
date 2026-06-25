#!/usr/bin/env python3
"""Static draft-hygiene audit for academic-writing LaTeX drafts.

This checks the *mechanical* writing rules the skill already mandates so that
adherence does not depend on the agent remembering them. It does NOT judge
writing quality, claim support, or section-writing method (those need semantic
review). Run it before describing a draft as clean, alongside audit_citations.py.

Checks (errors block; warnings inform):
- no \\footnote{...} anywhere in prose
- no file/code artifacts in prose (\\texttt{...ext}, \\verb, \\path)
- no local filesystem paths in prose (/mnt/, /home/, /Users/, /root/, ~/)
- disclosure: no internal identifiers or do-not-disclose entities in prose. Driven by an optional
  paper/.disclosure.yaml exported from the Writing Policy (see parse_disclosure_config for the
  format). Listed internal identifiers and do-not-disclose entities are errors; a heuristic also
  warns on internal-looking identifier tokens (e.g. ..._step380, long snake_case with digits) even
  when no list is present.
- no leftover missing-support markers (% CITATION_NEEDED / EVIDENCE_NEEDED /
  FIGURE_NEEDED / TABLE_NEEDED)
- limitations placement: no Limitations-titled subsection/paragraph/\\textbf run-in inside a
  body section, and at most one dedicated \\section{Limitations}
- content-page budget is venue-aware: the count ends at the first post-matter heading
  (References, or a venue-excluded section such as Limitations / Acknowledgments / Ethics);
  when a minimum is supplied, underfilled page-limited drafts are also blocking.
- subsection budget: at most 4 \\subsection per main section
- front-matter discipline: Abstract must not become a dense result/model-specific recap, and
  Introduction must not contain a model-list / result-recap paragraph
- heading quality: no body subsection whose title is only an appendix/supplement pointer, and no
  weak results heading such as "Aggregate Result Snapshot"
- table hygiene: no \\hline in tables (use booktabs); booktabs loaded when any
  table exists; warn on vertical rules and \\textsc{lowercase} names
- appendix starts on a fresh page (\\clearpage before \\appendix)
- appendix substance: warn on a sparse / table-dump appendix ("太空") — a section whose lead-in
  before its first float is under a few sentences, or several stacked full-width table*/figure*
  floats that scatter into half-empty pages
- appendix float ordering: warn on bare [h] placement on appendix floats — [h] defers and reorders
  across the separate figure/table queues, so floats stop following the section headings ("图顺序乱")
- salience: fail on taxonomy/inventory enumeration and per-category count dumps in body prose
  (full lists belong in a table or the appendix)
- wide tables: warn when a many-column plain tabular sits in a single-column float (body or
  appendix) and will overflow; suggest table*/rotate/split
- table design regressions: fail when a mostly numeric tabularx/table uses an unbounded first
  semantic column, when a declared-width tabularx/tabular* has no stretch/fill mechanism and leaves
  right-side whitespace, or when consecutive rows repeat the same group/setting label instead of
  using a grouped or abbreviated design
- prose in a non-wrapping column: warn when a multi-word cell sits in an l/c/r column (cannot
  line-break, runs off the page); suggest a wrapping column (tabularx Y/X or p{..})
- limitations length: fail when a standalone Limitations section is over-long (>180 words),
  over-enumerated (5+ points incl. bold-lead paragraphs), or wrapped in boilerplate opener/closer.
  Resolves the body across the main.tex-heading + \\input-body split.
- no invalid section environments such as \\end{section}; LaTeX sectioning commands are commands,
  not begin/end environments.
- no hard-coded structural reference numbers such as `Section~5.4` or `Table 2`; source must use
  \\label / \\ref so renumbering cannot render `??` or stale references.
- no duplicate \\label{...}
- \\input/\\include consistency between main.tex and section files
- Framework alignment when `--framework` is provided: every main-paper figure planned in the
  Paper Framework Figure Plan must materialize in `paper/`; planned picture/teaser figures must
  have both a Picture Brief and an output image, registry comments such as "not yet generated"
  are blocking errors, framework prose must not reference unplanned Fig./Tab. IDs, and related
  standalone radar/profile plots in one section must be merged into one multi-panel display.
- generated plot scripts: fail when paper-local matplotlib scripts define raw hex palettes without
  recording a registered CS palette name from the figure skill.
- Section guide compliance ledger when `--framework` is provided: `paper/section-compliance.md`
  must record that section guides were loaded and required moves were checked.
- appendix planning: if the draft has appendix content, `paper/appendix-plan.md` must record the
  planned appendix items, source availability, fill status, and fallback for missing evidence.
- compile-log signals when main.log exists (undefined refs/citations, multiply
  defined labels, rendered Table ?? / Figure ?? / Section ?? references; a large overfull hbox —
  content past the margin / "出界" — is a blocking error, minor overfulls are warnings)
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


SUBSECTION_BUDGET = 4

# An overfull hbox at or above this width (in points) is treated as a hard
# out-of-margin defect ("出界"), not a cosmetic warning. ~10pt ≈ 3.5mm past the
# edge: well beyond microtype tolerance and visible in the PDF. Smaller overfulls
# (long words, URLs) stay warnings.
OVERFULL_ERROR_PT = 10.0

FOOTNOTE_RE = re.compile(r"\\footnote\b")
ARTIFACT_RE = re.compile(
    r"\\(?:texttt|verb|path|lstinline)\b[^\n]*?"
    r"\.(?:json|py|csv|tsv|tex|sh|bash|yaml|yml|ipynb|cfg|ini|log|pkl|pt|ckpt|npy|md|txt)\b",
    re.I,
)
PATH_RE = re.compile(r"(?:/mnt/|/home/|/Users/|/root/|/tmp/|(?<![\w.])~/)")
# Heuristic for internal run/checkpoint identifiers that leaked into prose without being listed in
# .disclosure.yaml. Two signals: an explicit step/epoch/iter/ckpt + number suffix, or a long
# snake_case token (>= 2 underscores) that contains a digit (e.g. qwen3vl_rsmllm_top2_step380).
INTERNAL_STEP_RE = re.compile(
    r"\b\w*[_-](?:step|steps|epoch|epochs|ep|iter|iters|iteration|ckpt|checkpoint)[_-]?\d+\w*\b",
    re.I,
)
INTERNAL_SNAKE_RE = re.compile(r"\b[A-Za-z0-9]+(?:_[A-Za-z0-9]+){2,}\b")
# disclosure config filenames, checked in order
DISCLOSURE_FILES = (".disclosure.yaml", ".disclosure.yml")
MARKER_RE = re.compile(r"%\s*(CITATION_NEEDED|EVIDENCE_NEEDED|FIGURE_NEEDED|TABLE_NEEDED)\b")
SUBSECTION_RE = re.compile(r"\\subsection\b\s*\{")
SECTION_RE = re.compile(r"\\section\b\s*\{")
HEADING_COMMAND_RE = re.compile(r"\\(section|subsection|subsubsection|paragraph)\*?\s*\{([^}]*)\}")
APPENDIX_POINTER_HEADING_RE = re.compile(r"\b(?:Appendix|Supplement(?:ary)?)\b", re.I)
WEAK_RESULT_HEADING_RE = re.compile(r"\b(?:aggregate\s+)?results?\s+snapshot\b", re.I)
PERCENT_VALUE_RE = re.compile(r"\b\d+(?:\.\d+)?\s*\\?%")
RESULT_METRIC_RE = re.compile(
    r"\b(?:accuracy|F1|score|scores|rate|rates|success|failure|risk|capability|"
    r"task completion|completion|intervention|recovery|recovered)\b",
    re.I,
)
MODEL_NAME_RE = re.compile(
    r"\b(?:model|models|method|methods|baseline|baselines|system|systems|agent|agents|"
    r"variant|variants|checkpoint|checkpoints)\b",
    re.I,
)
RESULT_DELTA_RE = re.compile(
    r"\b(?:reduce[sd]?|drop(?:s|ped)?|increase[sd]?|improve[sd]?|rise[sn]?|raise[sd]?)\b"
    r"[^.\n]{0,120}\bfrom\b[^.\n]{0,80}\bto\b",
    re.I,
)
MODEL_LIST_CUE_RE = re.compile(r"\b(?:including|for|across|among|uses?|evaluates?)\b", re.I)
LABEL_RE = re.compile(r"\\label\s*\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]*)\}")
INVALID_SECTION_ENV_RE = re.compile(r"\\(?:begin|end)\s*\{(?:section|subsection|subsubsection|paragraph)\}")
HLINE_RE = re.compile(r"\\hline\b")
TABULAR_BEGIN_RE = re.compile(r"\\begin\{(tabular\*?|tabularx)\}")
TEXTSC_LOWER_RE = re.compile(r"\\textsc\s*\{\s*[a-z]")
APPENDIX_RE = re.compile(r"\\appendix\b")
CLEARPAGE_RE = re.compile(r"\\(?:clearpage|newpage|cleardoublepage)\b")
BOOKTABS_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\bbooktabs\b[^}]*\}")
REFERENCE_HEADING_RE = re.compile(r"(?m)^\s*(References|Bibliography)\s*$")
# Post-matter headings that, in most venues, sit outside the main-content page budget
# (ACL excludes Limitations and Ethics; most venues exclude Acknowledgments and impact
# statements). Matched only as a heading-only line so an inline "\textbf{Limitations ...}"
# run-in inside a body section does NOT falsely truncate the content-page count.
POSTMATTER_HEADING_RE = re.compile(
    r"(?m)^\s*(References|Bibliography|Limitations|Acknowledg(?:ments|ements)|"
    r"Ethics(?:\s+Statement)?|Ethical\s+Considerations|Broader\s+Impact|Impact\s+Statement)\s*$"
)
UNRESOLVED_RENDERED_REF_RE = re.compile(
    r"\b(?:Table|Figure|Fig\.|Section|Sec\.|Appendix|Eq\.|Equation)\s+\?\?"
)
HARDCODED_STRUCTURAL_REF_RE = re.compile(
    r"\b(?:Table|Figure|Fig\.|Section|Sec\.|Appendix|Eq\.|Equation)(?:~|\s)+\d+(?:\.\d+)?\b"
)
# Limitations declared as a structural unit. A dedicated \section{Limitations} (numbered or
# starred) is the correct home; a \subsection / \paragraph / \textbf run-in titled
# "Limitation(s)" inside another section is misplaced and must move to the dedicated section.
LIMIT_SECTION_RE = re.compile(r"\\section\*?\s*\{[^}]*[Ll]imitation[^}]*\}")
LIMIT_SUBSECTION_RE = re.compile(r"\\subsection\*?\s*\{[^}]*[Ll]imitation[^}]*\}")
LIMIT_PARAGRAPH_RE = re.compile(r"\\paragraph\*?\s*\{[^}]*[Ll]imitation[^}]*\}")
LIMIT_RUNIN_RE = re.compile(r"\\textbf\s*\{\s*[Ll]imitation[^}]*\}")
LIST_ENV_RE = re.compile(r"\\begin\{(itemize|enumerate)\}(.*?)\\end\{\1\}", re.S)
ITEM_RE = re.compile(r"\\item\b")
COUNT_RE = re.compile(
    r"\b\d+\s+(?:tasks|samples|examples|instances|images|cases|items|tokens|queries|prompts)\b",
    re.I,
)
# a parenthetical quantity: "(27 tasks)", "(50%)", or a multi-digit "(142)" — but NOT a bare
# single-digit list marker like "(1)" / "(4)" used for enumerating contributions or steps.
PAREN_COUNT_RE = re.compile(
    r"\(\s*\d[\d,]*\s*(?:tasks|samples|examples|instances|%)\s*\)|\(\s*\d{2,}[\d,]*\s*\)"
)

# files that hold macros / config, not prose
SKIP_PROSE = {"math_commands.tex", "preamble.tex"}

# enumeration of a taxonomy/inventory belongs in a table/appendix, not the body
ENUM_MIN_ITEMS = 5
ENUM_MIN_COUNTS = 3
TAXONOMY_LABEL_RE = re.compile(
    r"\\item\b[^\n]*(?:\\textbf\s*\{\s*[A-Z]{1,4}\d+\b|\b[A-Z]{1,4}\d+\s*(?:--|:))",
    re.I,
)
DEFINITION_ITEM_RE = re.compile(r"\\item\b[^\n]*(?:--|:)")
PROSE_COUNT_MIN = 4
# the disguised glossary: a run of \textbf{V1 (...)} / \textbf{H1 ...} bold lead-in paragraphs that
# define each coded taxonomy member one by one is an \item list with the markers stripped out. The
# coded-label shape (1-3 capitals then digits: V1, H7, RQ2, C3) avoids matching word leads like
# \textbf{Scope:} used in a short Limitations paragraph.
BODY_TAXONOMY_RUNIN_RE = re.compile(r"\\textbf\s*\{\s*[A-Z]{1,3}\d+\b[^}]*\}")
BODY_TAXONOMY_RUNIN_MIN = 4

# a wide table in a single-column float overflows; many columns need table*/rotate/split
TABLE_FLOAT_RE = re.compile(r"\\begin\{table(\*?)\}(.*?)\\end\{table\1\}", re.S)
TABLE_ENV_RE = re.compile(r"\\begin\{table(\*?)\}(.*?)\\end\{table\1\}", re.S)
TEXTWIDTH_RESIZEBOX_RE = re.compile(r"\\resizebox\s*\{\\textwidth\}\s*\{!", re.S)
FULLWIDTH_RESIZEBOX_RE = re.compile(r"\\resizebox\s*\{\\(?:textwidth|linewidth|columnwidth)\}\s*\{!", re.S)
DECLARED_WIDTHS = {r"\textwidth", r"\linewidth", r"\columnwidth"}
EXTRACOLSEP_FILL_RE = re.compile(r"\\extracolsep\s*\{\s*\\fill\s*\}")
FULL_WIDTH_TABLE_PLAN_RE = re.compile(
    r"\b(?:main results?|headline|leaderboard|sota|state-of-the-art|full[- ]width|"
    r"per-model|per-dataset|per-condition|per-subgroup|per-category|"
    r"model\s*[x×]\s*dataset|matrix|full matrix|aggregate results?)\b",
    re.I,
)
LOAD_BEARING_RESULTS_TABLE_RE = re.compile(
    r"\b(?:main results?|headline|overall results?|scorecard|leaderboard|"
    r"aggregate results?)\b",
    re.I,
)
COMPARISON_TABLE_READER_TASK_RE = re.compile(
    r"\b(?:per-model|per-method|model|method|baseline|system|agent|agents|"
    r"evaluated|comparison|compare|leaderboard)\b",
    re.I,
)
SINGLE_COLUMN_TABLE_PLAN_RE = re.compile(
    r"\b(?:taxonomy|definition|terminology|compact ablation|mini-ablation|"
    r"qualitative examples?|setup|protocol|notation|inventory|list)\b",
    re.I,
)
PLAIN_TABULAR_RE = re.compile(
    r"\\begin\{tabular\}\s*(?:\[[^\]]*\])?\s*\{((?:[^{}]|\{[^{}]*\})*)\}"
)
WIDE_SINGLE_COL_COLS = 6   # >= this many columns in a single-column float likely overflows
VERY_WIDE_COLS = 10        # >= this many columns usually needs rotation or splitting
LONG_HEADER_CHARS = 16     # a header cell longer than this overflows a narrow single column

# a standalone Limitations section must stay short and scannable, not exhaustive
LIMITATIONS_HEADING_RE = re.compile(r"\\section\*?\s*\{\s*Limitations\b[^}]*\}", re.I)
NEXT_HEADING_RE = re.compile(r"\\section\*?\s*\{")
# the Limitations section ends at the next section, the appendix, the bibliography, or end of document
LIM_NEXT_BOUNDARY_RE = re.compile(
    r"\\section\*?\s*\{|\\appendix\b|\\bibliography\b|\\begin\{thebibliography\}|\\end\{document\}"
)
LIMITATIONS_MAX_WORDS = 180   # target 120-180; block beyond the target cap
LIMITATIONS_MAX_POINTS = 5    # >= this many enumerated limitations is too many
LIM_ORDINAL_RE = re.compile(r"(?:^|(?<=[.\n]))\s*(?:First|Second|Third|Fourth|Fifth|Sixth)\b", re.M)
# bold-lead paragraphs (\textbf{Task coverage.} ...) are an enumeration form too
LIM_BOLD_LEAD_RE = re.compile(r"\\textbf\s*\{[^}]{0,40}?\}")
LIM_OPENER_RE = re.compile(r"we acknowledge\s+(?:several|a number of|the following|some)\s+limitation", re.I)
LIM_CLOSER_RE = re.compile(r"despite\s+(?:these|the above|the aforementioned)\s+limitation", re.I)

# a prose cell parked in a non-wrapping (l/c/r) column cannot line-break and runs off the page
PROSE_CELL_MIN_WORDS = 4   # a cell with >= this many word tokens is prose, not a label/number


class TabularBlock(NamedTuple):
    env_name: str
    width: str | None
    colspec: str
    body: str
    start: int


def _skip_ws(text: str, pos: int) -> int:
    while pos < len(text) and text[pos].isspace():
        pos += 1
    return pos


def _read_braced_group(text: str, pos: int) -> tuple[str, int] | None:
    pos = _skip_ws(text, pos)
    if pos >= len(text) or text[pos] != "{":
        return None
    depth = 0
    start = pos + 1
    for index in range(pos, len(text)):
        char = text[index]
        if char == "{" and (index == 0 or text[index - 1] != "\\"):
            depth += 1
        elif char == "}" and (index == 0 or text[index - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[start:index], index + 1
    return None


def _skip_optional_bracket_group(text: str, pos: int) -> int:
    pos = _skip_ws(text, pos)
    if pos >= len(text) or text[pos] != "[":
        return pos
    end = text.find("]", pos + 1)
    if end == -1:
        return pos
    return end + 1


def iter_tabular_blocks(text: str):
    """Yield parsed tabular/tabularx/tabular* blocks with width and colspec separated."""
    begin_re = re.compile(r"\\begin\{(tabularx|tabular\*|tabular)\}")
    for match in begin_re.finditer(text):
        env_name = match.group(1)
        pos = match.end()
        width: str | None = None

        if env_name in {"tabularx", "tabular*"}:
            width_group = _read_braced_group(text, pos)
            if width_group is None:
                continue
            width, pos = width_group
            pos = _skip_optional_bracket_group(text, pos)
            colspec_group = _read_braced_group(text, pos)
        else:
            pos = _skip_optional_bracket_group(text, pos)
            colspec_group = _read_braced_group(text, pos)

        if colspec_group is None:
            continue
        colspec, body_start = colspec_group
        end_re = re.compile(r"\\end\{" + re.escape(env_name) + r"\}")
        end_match = end_re.search(text, body_start)
        if end_match is None:
            continue
        yield TabularBlock(env_name, width, colspec, text[body_start:end_match.start()], match.start())

# the appendix should be substantive, not a sparse table dump. Two smells of a half-empty ("太空")
# appendix: (a) a section whose only content is a one-line pointer + a bare float, and (b) several
# stacked full-width floats that scatter across pages and leave empty bands. Warnings only.
APPENDIX_LEAD_MIN_WORDS = 25      # < this many prose words before a float in an appendix section = thin
APPENDIX_WIDE_FLOAT_SCATTER = 3   # >= this many table*/figure* floats in the appendix can scatter
SECTION_TITLE_RE = re.compile(r"\\section\b\s*\{[^}]*\}")
FLOAT_ENV_RE = re.compile(r"\\begin\{(table\*?|figure\*?)\}(.*?)\\end\{\1\}", re.S)
# a float environment with its placement spec, e.g. \begin{table}[h] or \begin{figure*}[!htbp]
FLOAT_PLACEMENT_RE = re.compile(r"\\begin\{(table|figure)(\*?)\}\s*\[([^\]]*)\]")
FIGURE_ENV_RE = re.compile(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", re.S)
FIGURE_ENV_WITH_STAR_RE = re.compile(r"\\begin\{figure(\*?)\}(.*?)\\end\{figure\1\}", re.S)
FRAMEWORK_FIGURE_PLAN_RE = re.compile(r"^#+\s*\d*\.?\s*Figure Plan\b", re.I)
FRAMEWORK_NEXT_SECTION_RE = re.compile(r"^#+\s+")
FRAMEWORK_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
FRAMEWORK_TARGET_LABEL_RE = re.compile(
    r"\bContent-page target\b|内容页目标|正文页目标|主文页数目标",
    re.I,
)
FRAMEWORK_BOUND_LABEL_RE = re.compile(
    r"\bActive content-page bound\b|有效内容页上限|正文页上限|主文页数上限",
    re.I,
)
FIG_ID_RE = re.compile(r"\bfig(?:ure)?\.?\s*(\d+)\b", re.I)
DISPLAY_REF_RE = re.compile(r"\b(Fig(?:ure)?|Tab(?:le)?)\.?\s*(\d+)\b", re.I)
APPENDIX_PLAN_REQUIRED_TOKENS = (
    "Claim backed",
    "Source availability",
    "Fill status",
    "Fallback",
)
PICTURE_ROUTE_RE = re.compile(
    r"\b(?:picture|ai illustration|teaser|pipeline|overview|architecture|workflow)\b",
    re.I,
)
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[([^\]]*)\])?\s*\{([^}]*)\}", re.S)
GRAPHICS_WIDTH_RE = re.compile(r"\bwidth\s*=\s*([^,\]]+)")
RELATIVE_WIDTH_RE = re.compile(r"^\s*(?:(\d+(?:\.\d+)?)\s*)?\\(?:line|text|column)width\s*$")
COMPACT_SINGLE_COLUMN_WIDTH_MAX = 0.70
COMPACT_FIGURE_RE = re.compile(r"\b(?:heatmap|coverage|matrix)\b", re.I)
STORY_TEASER_RE = re.compile(r"\b(?:story|teaser|overview|introductory|first\s+concept)\b", re.I)
WIDE_FIGURE_ROLE_RE = re.compile(
    r"\b(?:pipeline|framework|architecture|system|workflow|construction|multi-panel|"
    r"small[- ]multiples|grouped\s+bar|radar|heatmap|matrix)\b",
    re.I,
)
RADAR_FIGURE_RE = re.compile(r"\b(?:radar|polar|spider|profile)\b", re.I)
MULTIPANEL_FIGURE_RE = re.compile(r"\\begin\{subfigure\}|\\subfloat\b|\\subcaption\b|\\includegraphics.*\\includegraphics", re.S)
HEX_COLOR_RE = re.compile(r"#[0-9A-Fa-f]{6}")
PALETTE_ASSIGN_RE = re.compile(r"(?m)^\s*[A-Z0-9_]*PALETTE[A-Z0-9_]*\s*=")
REGISTERED_CS_PALETTE_RE = re.compile(
    r"CS_(?:PEER|BODY_PASTEL|HERO_BASELINE|COVERAGE|PAIRED_OPPOSING|"
    r"RADAR|QUALITATIVE_PANEL)_PALETTE|palette-system\.md|registered palette",
    re.I,
)


def count_columns(colspec: str) -> int:
    """Count column slots in a tabular colspec, tolerant of p{..}/>{..}/@{..} groups."""
    spec = re.sub(r"[><@!]\{(?:[^{}]|\{[^{}]*\})*\}", "", colspec)  # drop >{} <{} @{} !{}
    spec = re.sub(r"[pmb]\{(?:[^{}]|\{[^{}]*\})*\}", "p", spec)      # p{..}->one column
    return len(re.findall(r"[lcrpXYZS]", spec))


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        cut = len(line)
        for i, char in enumerate(line):
            if char == "\\":
                escaped = not escaped
                continue
            if char == "%" and not escaped:
                cut = i
                break
            escaped = False
        lines.append(line[:cut])
    return "\n".join(lines)


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_framework_display_items(framework_path: Path) -> list[dict[str, str]]:
    """Parse the Paper Framework Figure Plan table into compact display-item records."""
    text = framework_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    in_plan = False
    headers: list[str] = []
    items: list[dict[str, str]] = []

    for line in lines:
        if not in_plan:
            if FRAMEWORK_FIGURE_PLAN_RE.search(line.strip()):
                in_plan = True
            continue

        stripped = line.strip()
        if items and (FRAMEWORK_NEXT_SECTION_RE.match(stripped) or stripped == "---"):
            break
        if not stripped.startswith("|"):
            continue
        if FRAMEWORK_SEPARATOR_RE.match(stripped):
            continue

        cells = split_markdown_row(stripped)
        if not cells:
            continue
        if cells[0].lower() == "id":
            headers = [cell.lower().replace(" ", "_") for cell in cells]
            continue
        if not headers or len(cells) < len(headers):
            continue

        row = {headers[i]: cells[i] for i in range(len(headers))}
        item_id = row.get("id", "")
        if re.match(r"^(?:fig\.?|figure|tab\.?|table)\b", item_id.strip(), re.I):
            items.append(row)

    return items


def _ceil_page_value(text: str) -> int | None:
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return None
    return int(math.ceil(float(match.group(0))))


def parse_framework_page_budget(framework_path: Path) -> tuple[int | None, int | None]:
    """Return (content-page target, active content-page bound) parsed from a framework file.

    Decimal targets such as 7.75 mean "the draft must reach page 8", so they are rounded up for
    the integer page-reach audit.
    """
    text = framework_path.read_text(encoding="utf-8", errors="ignore")
    target: int | None = None
    bound: int | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        candidates: list[tuple[str, str]] = []
        if stripped.startswith("|"):
            cells = split_markdown_row(stripped)
            for index, cell in enumerate(cells[:-1]):
                candidates.append((cell, cells[index + 1]))
        else:
            candidates.append((stripped, stripped))

        for label, value_text in candidates:
            if target is None and FRAMEWORK_TARGET_LABEL_RE.search(label):
                target = _ceil_page_value(value_text)
            if bound is None and FRAMEWORK_BOUND_LABEL_RE.search(label):
                bound = _ceil_page_value(value_text)
        if target is not None and bound is not None:
            break

    return target, bound


def framework_item_number(item_id: str) -> str | None:
    match = FIG_ID_RE.search(item_id)
    return match.group(1) if match else None


def framework_display_key(item_id: str) -> str | None:
    match = DISPLAY_REF_RE.search(item_id)
    if not match:
        return None
    kind = "fig" if match.group(1).lower().startswith("fig") else "tab"
    return f"{kind}.{match.group(2)}"


def main_text_tex_files(paper_dir: Path) -> list[Path]:
    files = []
    for path in prose_tex_files(paper_dir):
        rel_name = rel(path, paper_dir).lower()
        if "appendix" in rel_name or rel_name == "checklist.tex":
            continue
        if rel_name.startswith("figures/"):
            continue
        files.append(path)
    return files


def graphics_relative_width(options: str | None) -> float | None:
    """Return includegraphics width as a fraction of line/text/column width when parseable."""
    if not options:
        return None
    match = GRAPHICS_WIDTH_RE.search(options)
    if not match:
        return None
    value = match.group(1).strip()
    width_match = RELATIVE_WIDTH_RE.match(value)
    if not width_match:
        return None
    return float(width_match.group(1) or "1.0")


def tabular_block_has_width_fill(block: TabularBlock) -> bool:
    if block.env_name == "tabularx":
        return any(t in "XYZ" for t in column_types(block.colspec)) or bool(EXTRACOLSEP_FILL_RE.search(block.colspec))
    if block.env_name == "tabular*":
        return bool(EXTRACOLSEP_FILL_RE.search(block.colspec))
    return False


def table_body_fills_textwidth(body: str) -> bool:
    if TEXTWIDTH_RESIZEBOX_RE.search(body):
        return True
    return any(
        block.width == r"\textwidth" and tabular_block_has_width_fill(block)
        for block in iter_tabular_blocks(body)
    )


def table_body_fills_declared_width(body: str) -> bool:
    if FULLWIDTH_RESIZEBOX_RE.search(body):
        return True
    return any(
        block.width in DECLARED_WIDTHS and tabular_block_has_width_fill(block)
        for block in iter_tabular_blocks(body)
    )


def table_plan_text(item: dict[str, str]) -> str:
    return " ".join(item.get(key, "") for key in ("id", "type", "layout", "message", "generation_route"))


def table_plan_needs_full_width(item: dict[str, str]) -> bool:
    return bool(FULL_WIDTH_TABLE_PLAN_RE.search(table_plan_text(item)))


def table_plan_should_stay_single_column(item: dict[str, str]) -> bool:
    return bool(SINGLE_COLUMN_TABLE_PLAN_RE.search(table_plan_text(item)))


def table_plan_is_load_bearing_results(item: dict[str, str]) -> bool:
    text = table_plan_text(item)
    return bool(LOAD_BEARING_RESULTS_TABLE_RE.search(text) and COMPARISON_TABLE_READER_TASK_RE.search(text))


def framework_declares_one_column(framework_text: str) -> bool:
    lowered = framework_text.lower()
    if "two-column" in lowered or "double-column" in lowered:
        return False
    return bool(re.search(r"\b(?:one-column|single-column)\s+(?:venue|paper|template|journal)\b", lowered))


def figure_body_is_standalone_radar(body: str) -> bool:
    if len(INCLUDEGRAPHICS_RE.findall(body)) != 1:
        return False
    if MULTIPANEL_FIGURE_RE.search(body):
        return False
    return bool(RADAR_FIGURE_RE.search(body))


def check_related_standalone_radars(main_text: str, errors: list[str]) -> None:
    """Related radar/profile plots in one section should be one multi-panel figure."""
    chunks = re.split(r"(?=\\(?:sub)?section\*?\s*\{)", main_text)
    for chunk in chunks:
        figures = FIGURE_ENV_WITH_STAR_RE.findall(chunk)
        radar_count = sum(1 for _starred, body in figures if figure_body_is_standalone_radar(body))
        if radar_count >= 2:
            heading_match = HEADING_COMMAND_RE.search(chunk)
            heading = ""
            if heading_match:
                heading = f" near `{heading_match.group(2).strip()}`"
            errors.append(
                f"related standalone radar figures{heading}: {radar_count} separate radar/profile "
                "figures appear in one section. Merge related radar/profile diagnostics into one "
                "multi-panel figure with shared legend, or move the weaker profile to appendix/supplement"
            )
            return


def check_framework_alignment(
    paper_dir: Path,
    framework_path: Path | None,
    errors: list[str],
    warnings: list[str],
) -> None:
    """Check that the confirmed Paper Framework's display plan reached paper artifacts."""
    if framework_path is None:
        return
    if not framework_path.exists():
        errors.append(f"framework alignment: missing framework file: {framework_path}")
        return

    items = parse_framework_display_items(framework_path)
    if not items:
        warnings.append(f"framework alignment: no Figure Plan display items parsed from {framework_path}")
        return
    planned_display_keys = {key for item in items if (key := framework_display_key(item.get("id", "")))}
    framework_text = framework_path.read_text(encoding="utf-8", errors="ignore")
    for match in DISPLAY_REF_RE.finditer(strip_comments(framework_text)):
        key = ("fig" if match.group(1).lower().startswith("fig") else "tab") + f".{match.group(2)}"
        if key not in planned_display_keys:
            line = framework_text.count("\n", 0, match.start()) + 1
            errors.append(
                f"framework alignment: unplanned display reference in framework: "
                f"{rel(framework_path, paper_dir.parent)}:{line}: {match.group(0)} is referenced "
                f"but not listed in the Figure Plan"
            )

    raw_text_by_file: dict[Path, str] = {
        path: path.read_text(encoding="utf-8", errors="ignore")
        for path in prose_tex_files(paper_dir)
    }
    registry = paper_dir / "figures" / "latex_includes.tex"
    if registry.exists():
        raw_text_by_file[registry] = registry.read_text(encoding="utf-8", errors="ignore")

    for path, text in raw_text_by_file.items():
        for lineno, line in enumerate(text.splitlines(), 1):
            if "not yet generated" in line.lower():
                errors.append(
                    f"framework alignment: unresolved display item registry entry contains "
                    f"'not yet generated': {rel(path, paper_dir)}:{lineno}: {line.strip()}"
                )

    planned_figures = [
        item for item in items if item.get("id", "").strip().lower().startswith(("fig", "figure"))
    ]
    planned_tables = [
        item for item in items if item.get("id", "").strip().lower().startswith(("tab", "table"))
    ]
    one_column_framework = framework_declares_one_column(framework_text)
    for item in planned_tables:
        layout = item.get("layout", "").lower()
        if "single-column" in layout and not one_column_framework and table_plan_is_load_bearing_results(item):
            errors.append(
                f"framework alignment: load-bearing main-results table {item.get('id', '').strip()} "
                f"is planned as single-column; in a two-column paper, the central results scorecard "
                f"should normally be double-column/full-width and use the span for grouped metrics, "
                f"counts, or other comparison cues rather than a narrow centered table"
            )
    main_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in main_text_tex_files(paper_dir)
    )
    actual_figures = FIGURE_ENV_WITH_STAR_RE.findall(strip_comments(main_text))
    actual_tables = TABLE_ENV_RE.findall(strip_comments(main_text))
    check_related_standalone_radars(strip_comments(main_text), errors)
    if len(actual_figures) < len(planned_figures):
        errors.append(
            f"framework alignment: planned figure missing; Framework plans {len(planned_figures)} "
            f"main-paper figure(s), but paper contains {len(actual_figures)} main-paper figure "
            f"environment(s)"
        )
    if len(actual_tables) < len(planned_tables):
        errors.append(
            f"framework alignment: planned table missing; Framework plans {len(planned_tables)} "
            f"main-paper table(s), but paper contains {len(actual_tables)} main-paper table "
            f"environment(s)"
        )
    planned_double_tables = [
        item for item in planned_tables if "double-column" in item.get("layout", "").lower()
    ]
    unjustified_double_tables = [
        item
        for item in planned_double_tables
        if table_plan_should_stay_single_column(item) or not table_plan_needs_full_width(item)
    ]
    for item in unjustified_double_tables:
        errors.append(
            f"framework alignment: unjustified double-column table plan for "
            f"{item.get('id', '').strip()}; compact, taxonomy, definition, setup, "
            f"qualitative, or otherwise sparse tables should stay single-column or move "
            f"to the appendix instead of being stretched full-width"
        )
    planned_full_width_tables = []
    for item in planned_tables:
        layout = item.get("layout", "").lower()
        if item in unjustified_double_tables or not table_plan_needs_full_width(item):
            continue
        if "double-column" in layout or "full-width" in layout or "full width" in layout:
            planned_full_width_tables.append(item)
    actual_wide_tables = [
        body
        for starred, body in actual_tables
        if (starred == "*" and table_body_fills_textwidth(body))
        or (starred != "*" and table_body_fills_declared_width(body))
    ]
    if planned_full_width_tables and not actual_wide_tables:
        ids = ", ".join(item.get("id", "").strip() for item in planned_full_width_tables)
        errors.append(
            f"framework alignment: planned full-width table(s) {ids} must fill "
            f"\\textwidth in a two-column template or \\linewidth/\\columnwidth in a one-column "
            f"template, but no main-paper full-width table with a real stretch/fill mechanism was found"
        )
    for item, body in zip(planned_full_width_tables, actual_wide_tables):
        if not table_body_fills_declared_width(body):
            errors.append(
                f"framework alignment: planned full-width table {item.get('id', '').strip()} "
                f"declares full-width layout but does not use a real stretch/fill mechanism; use "
                f"tabular*{{...}} with @{{\\extracolsep{{\\fill}}}} or tabularx{{...}} with a real X/Y/Z "
                f"prose column"
            )
    planned_double_figures = [
        item for item in planned_figures if "double-column" in item.get("layout", "").lower()
    ]
    for item in planned_double_figures:
        item_blob = " ".join(item.get(key, "") for key in ("id", "type", "section", "message", "generation_route"))
        if (
            framework_item_number(item.get("id", "")) == "1"
            and STORY_TEASER_RE.search(item_blob)
            and not WIDE_FIGURE_ROLE_RE.search(item_blob)
        ):
            errors.append(
                f"framework alignment: story/teaser figure should default to single-column for "
                f"{item.get('id', '').strip()}; reserve double-column for pipeline, framework, "
                f"architecture, system-overview, multi-panel, or genuinely wide comparison figures"
            )
    actual_wide_figures = [body for starred, body in actual_figures if starred == "*"]
    if planned_double_figures and len(actual_wide_figures) < len(planned_double_figures):
        ids = ", ".join(item.get("id", "").strip() for item in planned_double_figures)
        errors.append(
            f"framework alignment: planned double-column figure(s) {ids} must use figure* "
            f"and be bounded by \\textwidth in a two-column template; regular figure environments "
            f"are single-column and will squeeze or overflow wide displays"
        )

    for item in planned_figures:
        item_blob = " ".join(item.get(key, "") for key in ("id", "type", "layout", "message"))
        if "single-column" not in item.get("layout", "").lower():
            continue
        if not COMPACT_FIGURE_RE.search(item_blob):
            continue
        matching_bodies = [body for _starred, body in actual_figures if COMPACT_FIGURE_RE.search(body)]
        if not matching_bodies:
            continue
        for figure_body in matching_bodies:
            graphics = INCLUDEGRAPHICS_RE.search(figure_body)
            if not graphics:
                continue
            width = graphics_relative_width(graphics.group(1))
            if width is not None and width > COMPACT_SINGLE_COLUMN_WIDTH_MAX:
                errors.append(
                    f"framework alignment: oversized compact single-column figure for "
                    f"{item.get('id', '').strip()} uses width={width:.2f}\\linewidth; "
                    f"compact heatmap/coverage figures should be <= "
                    f"{COMPACT_SINGLE_COLUMN_WIDTH_MAX:.2f}\\linewidth or moved/reshaped"
                )
                break

    figures_dir = paper_dir / "figures"
    prompts_dir = figures_dir / "prompts"
    for item in planned_figures:
        text_blob = " ".join(
            item.get(key, "") for key in ("id", "type", "layout", "section", "generation_route")
        )
        if not PICTURE_ROUTE_RE.search(text_blob):
            continue
        number = framework_item_number(item.get("id", ""))
        if number is None:
            continue
        prefix = f"fig{number}"
        prompt_matches = sorted(prompts_dir.glob(f"{prefix}*.md")) if prompts_dir.exists() else []
        figure_matches: list[Path] = []
        if figures_dir.exists():
            for ext in ("png", "pdf", "svg"):
                figure_matches.extend(sorted(figures_dir.glob(f"{prefix}*.{ext}")))
        if not prompt_matches:
            errors.append(
                f"framework alignment: planned picture figure missing Picture Brief for "
                f"{item.get('id', '').strip()} (expected paper/figures/prompts/{prefix}*.md)"
            )
        if not figure_matches:
            errors.append(
                f"framework alignment: planned picture figure missing rendered artifact for "
                f"{item.get('id', '').strip()} (expected paper/figures/{prefix}*.png/pdf/svg)"
            )


def prose_tex_files(paper_dir: Path) -> list[Path]:
    files = []
    for path in sorted(paper_dir.rglob("*.tex")):
        if path.name in SKIP_PROSE:
            continue
        files.append(path)
    return files


def rel(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def parse_disclosure_config(paper_dir: Path) -> tuple[list[tuple[str, str]], list[str], Path | None]:
    """Parse paper/.disclosure.yaml into (naming_map, do_not_disclose, source_path).

    Expected shape (a small YAML subset; no external dependency required):

        naming_map:
          - internal: qwen3vl_rsmllm_top2_step380
            display: RsEvi-8B
        do_not_disclose:
          - RSThinker
          - SomeInternalTool

    `naming_map` entries pair an internal identifier with the public display name that must replace
    it. `do_not_disclose` is a flat list of entities that must not appear at all. Returns empty lists
    and a None path when no config file exists. The parser is intentionally forgiving: it reads the
    two top-level keys and ignores anything it does not recognize.
    """
    config_path = None
    for name in DISCLOSURE_FILES:
        candidate = paper_dir / name
        if candidate.exists():
            config_path = candidate
            break
    if config_path is None:
        return [], [], None

    naming_map: list[tuple[str, str]] = []
    do_not_disclose: list[str] = []
    section: str | None = None
    pending_internal: str | None = None

    def strip_value(raw: str) -> str:
        raw = raw.strip()
        if raw and raw[0] in "'\"" and raw[-1:] == raw[0]:
            raw = raw[1:-1]
        return raw.strip()

    for line in config_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        # drop comments
        hash_pos = line.find("#")
        if hash_pos != -1:
            line = line[:hash_pos]
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped in ("naming_map:", "naming_map :"):
            section = "naming"
            continue
        if stripped in ("do_not_disclose:", "do_not_disclose :"):
            section = "exclude"
            continue
        if section == "naming":
            m = re.match(r"-\s*internal\s*:\s*(.+)$", stripped)
            if m:
                pending_internal = strip_value(m.group(1))
                continue
            m = re.match(r"display\s*:\s*(.+)$", stripped)
            if m and pending_internal is not None:
                naming_map.append((pending_internal, strip_value(m.group(1))))
                pending_internal = None
                continue
            # tolerate "- internal: x, display: y" or "- x: y" one-liners
            m = re.match(r"-\s*(.+?)\s*:\s*(.+)$", stripped)
            if m and m.group(1) not in ("internal", "display"):
                naming_map.append((strip_value(m.group(1)), strip_value(m.group(2))))
                continue
        elif section == "exclude":
            m = re.match(r"-\s*(.+)$", stripped)
            if m:
                value = strip_value(m.group(1))
                if value:
                    do_not_disclose.append(value)
                continue

    return naming_map, do_not_disclose, config_path


def _entity_re(entity: str) -> re.Pattern[str]:
    """Whole-token match for an entity name, tolerant of LaTeX wrappers around it."""
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(entity) + r"(?![A-Za-z0-9_])")


def check_disclosure(
    path: Path,
    base: Path,
    naming_map: list[tuple[str, str]],
    do_not_disclose: list[str],
    errors: list[str],
) -> None:
    """Listed internal identifiers / do-not-disclose entities in prose are blocking errors."""
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    for lineno, line in enumerate(text.splitlines(), 1):
        for internal, display in naming_map:
            if internal and _entity_re(internal).search(line):
                errors.append(
                    f"internal identifier in prose: {name}:{lineno}: '{internal}' — use the public "
                    f"display name '{display}' (Naming Map)"
                )
        for entity in do_not_disclose:
            if entity and _entity_re(entity).search(line):
                errors.append(
                    f"do-not-disclose entity in prose: {name}:{lineno}: '{entity}' — remove it, "
                    f"including any negation/exclusion phrasing"
                )


# commands whose {...} arguments are keys/paths, not prose — their tokens must not trip the
# internal-identifier heuristic (e.g. \cite{smith_etal_2024}, \label{fig:abc_1})
REF_LIKE_RE = re.compile(
    r"\\(?:cite[a-zA-Z]*|[Cc]ref|autoref|nameref|ref|eqref|pageref|label|input|include|"
    r"includegraphics|bibliography|bibliographystyle|usepackage|url|href|texttt|verb|path|"
    r"lstinline)\b\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}",
)


def strip_ref_like(text: str) -> str:
    return REF_LIKE_RE.sub(" ", text)


def check_internal_id_heuristic(
    path: Path,
    base: Path,
    allow: set[str],
    warnings: list[str],
) -> None:
    """Warn on internal-looking identifier tokens not covered by an explicit list."""
    text = strip_ref_like(strip_comments(path.read_text(encoding="utf-8", errors="ignore")))
    name = rel(path, base)
    seen: set[str] = set()
    for lineno, line in enumerate(text.splitlines(), 1):
        candidates = set()
        for m in INTERNAL_STEP_RE.finditer(line):
            candidates.add(m.group(0))
        for m in INTERNAL_SNAKE_RE.finditer(line):
            tok = m.group(0)
            if any(ch.isdigit() for ch in tok):
                candidates.add(tok)
        for tok in candidates:
            if tok in allow or tok in seen:
                continue
            seen.add(tok)
            warnings.append(
                f"internal-looking identifier in prose: {name}:{lineno}: '{tok}'; if this is a "
                f"checkpoint/run/sweep name, map it to a public display name (Naming Map)"
            )


def check_prose(path: Path, base: Path, errors: list[str], warnings: list[str]) -> None:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    name = rel(path, base)
    for lineno, line in enumerate(raw.splitlines(), 1):
        if MARKER_RE.search(line):
            errors.append(f"unresolved missing-support marker: {name}:{lineno}: {line.strip()}")
    text = strip_comments(raw)
    for lineno, line in enumerate(text.splitlines(), 1):
        if FOOTNOTE_RE.search(line):
            errors.append(f"footnote in prose (banned): {name}:{lineno}")
        m = ARTIFACT_RE.search(line)
        if m:
            errors.append(f"file/code artifact in prose: {name}:{lineno}: {m.group(0).strip()}")
        m = PATH_RE.search(line)
        if m:
            start = max(0, m.start() - 20)
            errors.append(f"local path in prose: {name}:{lineno}: ...{line[start:m.end() + 20].strip()}...")


def check_subsection_budget(path: Path, base: Path, errors: list[str]) -> None:
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    sections = list(SECTION_RE.finditer(text))
    if len(sections) <= 1:
        count = len(SUBSECTION_RE.findall(text))
        if count > SUBSECTION_BUDGET:
            errors.append(
                f"subsection budget exceeded: {name} has {count} subsections (max {SUBSECTION_BUDGET})"
            )
        return
    # multiple \section in one file: count subsections per section span
    bounds = [m.start() for m in sections] + [len(text)]
    for i in range(len(sections)):
        span = text[bounds[i] : bounds[i + 1]]
        count = len(SUBSECTION_RE.findall(span))
        if count > SUBSECTION_BUDGET:
            label = text[sections[i].start() : sections[i].start() + 60].replace("\n", " ")
            errors.append(
                f"subsection budget exceeded: {name} section '{label.strip()}' has {count} "
                f"subsections (max {SUBSECTION_BUDGET})"
            )


def check_heading_quality(paths: list[Path], base: Path, errors: list[str]) -> None:
    """Block scaffolding headings that should be prose pointers or finding-led titles."""
    for path in paths:
        name = rel(path, base)
        lower_name = name.lower()
        if "appendix" in lower_name or lower_name == "checklist.tex":
            continue
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        for match in HEADING_COMMAND_RE.finditer(text):
            command, raw_title = match.groups()
            title = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", "", raw_title)
            title = re.sub(r"\s+", " ", title).strip()
            if not title:
                continue
            line = text.count("\n", 0, match.start()) + 1
            if command != "section" and APPENDIX_POINTER_HEADING_RE.search(title):
                errors.append(
                    f"appendix pointer heading in body: {name}:{line}: "
                    f"\\{command}{{{title}}}; make this a prose cross-reference, not a body subsection"
                )
            if WEAK_RESULT_HEADING_RE.search(title):
                errors.append(
                    f"non-reader-facing result heading: {name}:{line}: "
                    f"\\{command}{{{title}}}; use a finding-led title such as "
                    f"'Overall Performance-Robustness Tradeoff' or 'Denominator Effects'"
                )


def check_tables(path: Path, base: Path, errors: list[str], warnings: list[str]) -> None:
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    for tm in TABLE_ENV_RE.finditer(text):
        starred = tm.group(1) == "*"
        if starred and not table_body_fills_textwidth(tm.group(2)):
            lineno = text.count("\n", 0, tm.start()) + 1
            errors.append(
                f"narrow double-column table: {name}:{lineno}; table* must fill \\textwidth "
                f"with tabular*{{\\textwidth}} or tabularx{{\\textwidth}}, otherwise keep it single-column"
            )
    for lineno, line in enumerate(text.splitlines(), 1):
        if HLINE_RE.search(line):
            errors.append(f"\\hline in table (use booktabs \\toprule/\\midrule/\\bottomrule): {name}:{lineno}")
        if TEXTSC_LOWER_RE.search(line):
            warnings.append(f"\\textsc{{...}} on a lowercase name renders poorly: {name}:{lineno}")
    for block in iter_tabular_blocks(text):
        if "|" in block.colspec:
            lineno = text.count("\n", 0, block.start) + 1
            warnings.append(f"vertical rule (|) in table column spec; booktabs uses none: {name}:{lineno}")
    for block in iter_tabular_blocks(text):
        lineno = text.count("\n", 0, block.start) + 1
        check_declared_width_underfill(block, name, lineno, errors)
        check_numeric_table_first_column(block.env_name, block.colspec, name, lineno, errors)
        check_repeated_table_group_labels(block.body, name, lineno, errors)


def check_declared_width_underfill(
    block: TabularBlock,
    name: str,
    lineno: int,
    errors: list[str],
) -> None:
    """Block full-width tabularx/tabular* declarations that do not actually fill the width."""
    if block.env_name not in {"tabularx", "tabular*"}:
        return
    if block.width not in DECLARED_WIDTHS:
        return
    if tabular_block_has_width_fill(block):
        return
    errors.append(
        f"underfilled declared-width table: {name}:{lineno}; {block.env_name} declares "
        f"{block.width} but its column spec has no X/Y/Z stretch column and no "
        f"@{{\\extracolsep{{\\fill}}}} glue, so the rule spans the container while the cells "
        "remain left-packed with right-side whitespace"
    )


def check_numeric_table_first_column(
    env_name: str,
    colspec: str,
    name: str,
    lineno: int,
    errors: list[str],
) -> None:
    """Block mostly numeric tables whose first semantic column absorbs all spare width."""
    types = column_types(colspec)
    if len(types) < WIDE_SINGLE_COL_COLS:
        return
    if types[0] not in "XYZ":
        return
    numeric_like = sum(1 for t in types[1:] if t in "rSc")
    if numeric_like < max(4, len(types) - 2):
        return
    errors.append(
        f"unbounded first semantic column in numeric table: {name}:{lineno}; "
        f"{env_name} column spec starts with `{types[0]}` and then {numeric_like} numeric columns. "
        "Use a bounded L{...}/p{...} first column or tabular* with a fixed semantic column so "
        "the label column cannot consume the numeric block's width"
    )


def clean_table_cell(cell: str) -> str:
    cell = re.sub(r"\\(?:textit|emph|textbf|textsc)\s*\{([^{}]*)\}", r"\1", cell)
    cell = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", cell)
    cell = re.sub(r"[{}$~^_%#]", " ", cell)
    return " ".join(cell.split()).strip()


def check_repeated_table_group_labels(body: str, name: str, lineno: int, errors: list[str]) -> None:
    """Block consecutive repeated first-column group labels in rendered table rows."""
    previous: str | None = None
    for raw_row in re.split(r"\\\\", body):
        row = raw_row.strip()
        if not row:
            continue
        if "\\addlinespace" in row and "&" not in row:
            previous = None
            continue
        row = re.sub(r"\\(?:toprule|midrule|bottomrule|addlinespace)\b", " ", row)
        row = re.sub(r"\\cmidrule(?:\([^)]*\))?\s*\{[^{}]*\}", " ", row)
        if "&" not in row:
            continue
        if "\\multicolumn" in row:
            previous = None
            continue
        cells = _split_cells(row)
        if len(cells) < 2:
            continue
        first = clean_table_cell(cells[0])
        if not first or not re.search(r"[A-Za-z]", first):
            previous = None if not first else previous
            continue
        if previous == first:
            errors.append(
                f"repeated table group label: {name}:{lineno}: `{first}` appears in consecutive "
                "rows; use an italic group row, blank continuation cell, or compact variant labels "
                "with the group expanded once in the caption"
            )
            return
        previous = first


def check_booktabs_loaded(paper_dir: Path, files: list[Path], errors: list[str]) -> None:
    has_table = any(
        TABULAR_BEGIN_RE.search(strip_comments(p.read_text(encoding="utf-8", errors="ignore")))
        for p in files
    )
    if not has_table:
        return
    preamble = ""
    for cand in (paper_dir / "main.tex", paper_dir / "preamble.tex"):
        if cand.exists():
            preamble += cand.read_text(encoding="utf-8", errors="ignore")
    if not BOOKTABS_RE.search(preamble):
        errors.append("tables present but \\usepackage{booktabs} is not loaded in the preamble")


def check_appendix_page(paper_dir: Path, warnings: list[str]) -> None:
    main = paper_dir / "main.tex"
    if not main.exists():
        return
    text = strip_comments(main.read_text(encoding="utf-8", errors="ignore"))
    m = APPENDIX_RE.search(text)
    if not m:
        return
    preceding = text[:m.start()]
    tail = preceding.rstrip().splitlines()[-3:] if preceding.strip() else []
    if not any(CLEARPAGE_RE.search(line) for line in tail):
        warnings.append("\\appendix is not preceded by \\clearpage; appendix may not start on a fresh page")


def _prose_word_count(segment: str) -> int:
    """Count real prose words in a LaTeX fragment, ignoring commands, refs, and math punctuation."""
    s = strip_ref_like(segment)
    s = re.sub(r"\\[a-zA-Z@]+\*?", " ", s)   # drop control sequences
    s = re.sub(r"[{}\\$&~^_%#]", " ", s)
    return sum(1 for w in s.split() if any(c.isalpha() for c in w))


def _latex_to_plain(text: str) -> str:
    """Best-effort plain text for lightweight front-matter heuristics."""
    text = strip_ref_like(strip_comments(text))
    for _ in range(4):
        text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z@]+\*?", " ", text)
    text = re.sub(r"[{}$&~_^#]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _read_input_target(paper_dir: Path, target: str) -> str:
    path = paper_dir / target
    if path.suffix != ".tex":
        path = path.with_suffix(".tex")
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def _section_source(paper_dir: Path, section: str) -> tuple[str, str]:
    """Return (display name, LaTeX source) for a common front-matter section."""
    section_dir = paper_dir / "sections"
    candidates: list[Path] = []
    if section == "abstract":
        candidates.extend(
            [
                section_dir / "abstract.tex",
                section_dir / "0_abstract.tex",
                section_dir / "00_abstract.tex",
            ]
        )
    elif section == "introduction":
        candidates.extend(
            [
                section_dir / "introduction.tex",
                section_dir / "1_introduction.tex",
                section_dir / "01_introduction.tex",
            ]
        )
    for candidate in candidates:
        if candidate.exists():
            return rel(candidate, paper_dir), candidate.read_text(encoding="utf-8", errors="ignore")

    main = paper_dir / "main.tex"
    if not main.exists():
        return section, ""
    main_text = strip_comments(main.read_text(encoding="utf-8", errors="ignore"))
    if section == "abstract":
        env = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", main_text, re.S)
        if env:
            return "main.tex abstract", env.group(1)
        for m in INPUT_RE.finditer(main_text):
            target = m.group(1).strip()
            if "abstract" in target.lower():
                body = _read_input_target(paper_dir, target)
                if body:
                    return target, body
    else:
        for m in INPUT_RE.finditer(main_text):
            target = m.group(1).strip()
            if "intro" in target.lower():
                body = _read_input_target(paper_dir, target)
                if body:
                    return target, body
        intro = re.search(
            r"\\section\*?\s*\{\s*Introduction\s*\}(.*?)(?=\\section\*?\s*\{|\\appendix\b|\\bibliography\b|\\end\{document\})",
            main_text,
            re.S | re.I,
        )
        if intro:
            return "main.tex Introduction", intro.group(1)
    return section, ""


def check_front_matter_discipline(
    paper_dir: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    """Block common failures where front matter turns into a results dump.

    This is intentionally a narrow heuristic. It does not grade prose quality; it catches the
    stable, easy-to-measure failure mode where Abstract/Introduction violate the section guides by
    carrying multiple percentages, model-specific deltas, or a model-list result paragraph.
    """
    abstract_name, abstract_source = _section_source(paper_dir, "abstract")
    if abstract_source:
        plain = _latex_to_plain(abstract_source)
        percent_count = len(PERCENT_VALUE_RE.findall(abstract_source))
        model_count = len({m.group(0).lower() for m in MODEL_NAME_RE.finditer(plain)})
        has_delta = bool(RESULT_DELTA_RE.search(plain))
        has_metric = bool(RESULT_METRIC_RE.search(plain))
        if percent_count > 2 or (model_count and percent_count) or (has_delta and percent_count >= 2):
            errors.append(
                f"abstract result overload: {abstract_name} contains {percent_count} percentage "
                f"value(s), {model_count} model-specific name(s), and "
                f"{'a model/result delta' if has_delta else 'no explicit delta'}; Abstract should "
                f"follow problem -> challenge/gap -> insight/contribution -> advantage -> one "
                f"bounded evidence sentence, not a result recap"
            )
        elif has_metric and percent_count == 2:
            warnings.append(
                f"abstract evidence budget near limit: {abstract_name} has two numeric result values; "
                f"keep them as one bounded evidence sentence"
            )

    intro_name, intro_source = _section_source(paper_dir, "introduction")
    if intro_source:
        plain = _latex_to_plain(intro_source)
        percent_count = len(PERCENT_VALUE_RE.findall(intro_source))
        model_names = {m.group(0).lower() for m in MODEL_NAME_RE.finditer(plain)}
        model_count = len(model_names)
        has_metric = bool(RESULT_METRIC_RE.search(plain))
        has_delta = bool(RESULT_DELTA_RE.search(plain))
        has_model_list = model_count >= 3 and bool(MODEL_LIST_CUE_RE.search(plain))
        if (percent_count > 1 and has_metric) or has_delta or (has_model_list and (percent_count or has_metric)):
            errors.append(
                f"introduction result recap: {intro_name} contains {percent_count} percentage "
                f"value(s), {model_count} model-specific name(s), and "
                f"{'a result delta' if has_delta else 'no explicit delta'}; Introduction should "
                f"contain at most one high-level evidence preview sentence and no model-list or "
                f"result-recap paragraph"
            )


def check_section_compliance_ledger(
    paper_dir: Path,
    framework_path: Path | None,
    errors: list[str],
) -> None:
    """Require a durable record that section guides were loaded and checked.

    The drafting workflow can keep paragraph plans internal, but for a complete framework-backed
    paper the closing audit needs a small artifact proving each section was checked against its
    required moves. This prevents "the guide existed but was not actually applied" failures.
    """
    if framework_path is None:
        return
    ledger = paper_dir / "section-compliance.md"
    if not ledger.exists():
        errors.append(
            "section guide compliance ledger missing: paper/section-compliance.md must record "
            "the section guide loaded for each drafted section and the required moves checked"
        )
        return
    text = ledger.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    for token in ("abstract", "introduction"):
        if token not in lower:
            errors.append(f"section guide compliance ledger incomplete: missing {token} row")
    for bad in ("missing", "unchecked", "not loaded", "not applied", "todo", "tbd"):
        if bad in lower:
            errors.append(
                f"section guide compliance ledger has unresolved status token '{bad}'; "
                f"revise the affected section or record a blocking risk before returning"
            )
            break


def appendix_segments(paper_dir: Path) -> list[tuple[str, str]]:
    """Return (name, stripped-text) for appendix content.

    Covers both inline appendices (text after `\\appendix` in main.tex) and file-based appendices
    (files \\input after `\\appendix`, or any *.tex whose name contains 'appendix'). De-duplicated by
    display name so an inputted appendix file is not counted twice.
    """
    segments: list[tuple[str, str]] = []
    appendix_files: set[Path] = set()
    main = paper_dir / "main.tex"
    if main.exists():
        mtext = strip_comments(main.read_text(encoding="utf-8", errors="ignore"))
        am = APPENDIX_RE.search(mtext)
        if am:
            after = mtext[am.end():]
            segments.append(("main.tex", after))
            for im in INPUT_RE.finditer(after):
                target = im.group(1).strip()
                if not target.endswith(".tex"):
                    target += ".tex"
                appendix_files.add((paper_dir / target).resolve())
    for path in sorted(paper_dir.rglob("*.tex")):
        if path.name in SKIP_PROSE:
            continue
        if "appendix" in path.name.lower() or path.resolve() in appendix_files:
            segments.append((rel(path, paper_dir), strip_comments(path.read_text(encoding="utf-8", errors="ignore"))))
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for name, text in segments:
        if name in seen:
            continue
        seen.add(name)
        out.append((name, text))
    return out


def check_appendix_substance(paper_dir: Path, warnings: list[str]) -> None:
    """Heuristic: flag a sparse / table-dump appendix ("太空"). Warnings only.

    (a) An appendix \\section whose lead-in before its first float is under a few sentences reads as a
        bare pointer + float; nudge to add a real lead paragraph.
    (b) Several full-width table*/figure* floats in the appendix scatter into half-empty pages; nudge
        to anchor with prose, pin placement, or keep one-column tables single-column.
    (c) An appendix float placed with bare [h] ("here only") defers when it does not fit and, because
        figures and tables sit in separate float queues, resurfaces out of section order ("图顺序乱");
        nudge to pin with [H] (float pkg) or [ht]/[tbp] + \\FloatBarrier.
    """
    segments = appendix_segments(paper_dir)
    if not segments:
        return
    wide_locs: list[str] = []
    hplace_locs: list[str] = []
    for name, text in segments:
        for pm in FLOAT_PLACEMENT_RE.finditer(text):
            letters = pm.group(3).replace("!", "").strip()
            if letters == "h":  # bare [h] / [h!] / [!h] — the fragile, reorder-prone specifier
                kind = pm.group(1) + ("*" if pm.group(2) else "")
                hplace_locs.append(f"{name}:{text.count(chr(10), 0, pm.start()) + 1} ({kind})")
        sections = list(SECTION_RE.finditer(text))
        bounds = [m.start() for m in sections] + [len(text)]
        for i, sm in enumerate(sections):
            span = text[sm.start(): bounds[i + 1]]
            span_wo_head = SECTION_TITLE_RE.sub(" ", span, count=1)
            fm = FLOAT_ENV_RE.search(span_wo_head)
            if not fm:
                continue  # prose-only section, or no float here — not the table-dump smell
            words = _prose_word_count(span_wo_head[: fm.start()])
            if words < APPENDIX_LEAD_MIN_WORDS:
                lineno = text.count("\n", 0, sm.start()) + 1
                kind = "figure" if fm.group(1).startswith("figure") else "table"
                warnings.append(
                    f"thin appendix section ({words} words of prose before a {kind}): {name}:{lineno}; "
                    f"add a lead paragraph (what it is, how to read it, which claim it backs) instead "
                    f"of a one-line pointer + bare float"
                )
        for fm in FLOAT_ENV_RE.finditer(text):
            if fm.group(1).endswith("*"):
                wide_locs.append(f"{name}:{text.count(chr(10), 0, fm.start()) + 1}")
    if len(wide_locs) >= APPENDIX_WIDE_FLOAT_SCATTER:
        shown = ", ".join(wide_locs[:5]) + ("…" if len(wide_locs) > 5 else "")
        warnings.append(
            f"{len(wide_locs)} full-width (table*/figure*) floats in the appendix ({shown}); stacked "
            f"wide floats scatter into half-empty pages — anchor each with a lead paragraph, pin "
            f"placement ([H] or [tbp]+\\FloatBarrier), or keep one-column tables single-column"
        )
    if hplace_locs:
        shown = ", ".join(hplace_locs[:6]) + ("…" if len(hplace_locs) > 6 else "")
        warnings.append(
            f"{len(hplace_locs)} appendix float(s) use bare [h] placement ({shown}); [h] defers when "
            f"it does not fit and reorders across the separate figure/table queues, so floats stop "
            f"following the section headings (\"图顺序乱\") — pin with [H] (float pkg) under the "
            f"heading, or use [ht]/[tbp] + \\FloatBarrier (placeins) / \\clearpage per appendix "
            f"section (if the venue forbids float/\\clearpage, e.g. AAAI, use [!ht]/[tbp] instead — "
            f"never bare [h])"
        )


def check_appendix_plan(paper_dir: Path, errors: list[str]) -> None:
    """Require a lightweight source-aware appendix plan before appendix material is pasted."""
    segments = appendix_segments(paper_dir)
    substantive = [
        (name, text)
        for name, text in segments
        if _prose_word_count(text) > 0 or FLOAT_ENV_RE.search(text)
    ]
    if not substantive:
        return
    plan = paper_dir / "appendix-plan.md"
    if not plan.exists():
        errors.append(
            "missing appendix plan: paper/appendix-plan.md must list appendix items before "
            "appendix content is included, with claim backed, source availability, fill status, "
            "and fallback for missing evidence"
        )
        return
    text = plan.read_text(encoding="utf-8", errors="ignore")
    missing = [token for token in APPENDIX_PLAN_REQUIRED_TOKENS if token not in text]
    if missing:
        errors.append(
            "incomplete appendix plan: paper/appendix-plan.md is missing required field(s): "
            + ", ".join(missing)
        )


def check_enumeration(path: Path, base: Path, errors: list[str]) -> None:
    """Heuristic: flag taxonomy/inventory enumeration and per-category count dumps in body prose.

    Skips appendix files and generated venue checklists. The appendix is the correct home for full
    lists, and checklist.tex is not manuscript body prose. Errors because a body subsection that
    turns into a glossary/list of V1/H1-style terms is a structure defect, not a polish issue.
    """
    name = rel(path, base)
    if "appendix" in path.name.lower() or name.lower() == "checklist.tex":
        return
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    for m in LIST_ENV_RE.finditer(text):
        body = m.group(2)
        items = len(ITEM_RE.findall(body))
        counts = len(COUNT_RE.findall(body))
        taxonomy_labels = len(TAXONOMY_LABEL_RE.findall(body))
        definition_items = len(DEFINITION_ITEM_RE.findall(body))
        if items >= ENUM_MIN_ITEMS and counts >= ENUM_MIN_COUNTS:
            lineno = text.count("\n", 0, m.start()) + 1
            errors.append(
                f"taxonomy/inventory enumeration in body ({items} items, {counts} per-category "
                f"counts): {name}:{lineno}; mention in one stroke and move the full list to a "
                f"table or appendix"
            )
        elif items >= ENUM_MIN_ITEMS and (
            taxonomy_labels >= 3 or definition_items >= ENUM_MIN_ITEMS
        ):
            lineno = text.count("\n", 0, m.start()) + 1
            errors.append(
                f"taxonomy/inventory definition list in body ({items} items, {taxonomy_labels} "
                f"coded labels): {name}:{lineno}; do not write a subsection as one term per item "
                f"(e.g. V1/H1 definitions). State the taxonomy in one argumentative stroke and put "
                f"the full definitions/counts in a table or appendix"
            )
    runins = BODY_TAXONOMY_RUNIN_RE.findall(text)
    if len(runins) >= BODY_TAXONOMY_RUNIN_MIN:
        fm = BODY_TAXONOMY_RUNIN_RE.search(text)
        lineno = text.count("\n", 0, fm.start()) + 1
        errors.append(
            f"taxonomy definition dump via bold run-ins in body ({len(runins)} "
            f"\\textbf{{V1/H1...}} coded-label lead-ins): {name}:{lineno}; a run of "
            f"\\textbf{{coded-label}} paragraphs defining each member one by one is a glossary list "
            f"without \\item — give the taxonomy table a Description column and move the full "
            f"per-member definitions to an appendix subsection with a lead paragraph"
        )
    for lineno, line in enumerate(text.splitlines(), 1):
        hits = len(COUNT_RE.findall(line)) + len(PAREN_COUNT_RE.findall(line))
        if hits >= PROSE_COUNT_MIN:
            errors.append(
                f"per-category count enumeration in prose ({hits} counts on one line): "
                f"{name}:{lineno}; move the breakdown to a table and cite only load-bearing numbers"
            )


def check_wide_tables(path: Path, base: Path, errors: list[str], warnings: list[str]) -> None:
    """Heuristic: flag wide plain-`tabular` tables in single-column floats (likely overflow).

    Applies to body and appendix alike. Warnings only.
    """
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    for fm in TABLE_FLOAT_RE.finditer(text):
        starred = fm.group(1) == "*"
        body = fm.group(2)
        lineno = text.count("\n", 0, fm.start()) + 1
        for tm in PLAIN_TABULAR_RE.finditer(body):
            ncols = count_columns(tm.group(1))
            if not starred and ncols >= WIDE_SINGLE_COL_COLS:
                errors.append(
                    f"wide table ({ncols} columns) in a single-column float: {name}:{lineno}; "
                    f"use table* (fill \\textwidth), rotate, or split — it will overflow the column"
                )
            if ncols >= VERY_WIDE_COLS:
                errors.append(
                    f"very wide table ({ncols} columns): {name}:{lineno}; even table* may overflow "
                    f"\\textwidth — rotate (sidewaystable) or split by column groups"
                )
        # long headers overflow a narrow column even when the column count is small (e.g. a
        # tabular{lrrr} with verbose "Defend Rate (\%)" headers). The column-count heuristic misses
        # this; flag verbose headers in a single-column plain-tabular float as a likely overflow.
        for block in iter_tabular_blocks(body):
            colspec = block.colspec
            ncols = count_columns(colspec)
            if starred or not (3 <= ncols < WIDE_SINGLE_COL_COLS):
                continue
            if "X" in colspec.upper() or "p{" in colspec or "p {" in colspec:
                continue
            header = block.body.split(r"\\", 1)[0]
            header = re.sub(r"\\multicolumn\s*\{[^}]*\}\s*\{[^}]*\}", " ", header)
            header = re.sub(r"\\[a-zA-Z]+\*?", " ", header)
            cells = [re.sub(r"[{}$]", "", c).strip() for c in header.split("&")]
            longest = max((len(c) for c in cells), default=0)
            if longest > LONG_HEADER_CHARS:
                tlineno = text.count("\n", 0, fm.start(2) + block.start) + 1
                warnings.append(
                    f"long headers in a single-column table (longest ~{longest} chars, {ncols} "
                    f"cols): {name}:{tlineno}; verbose headers overflow \\columnwidth even at few "
                    f"columns — abbreviate (e.g. 'Defend Rate (\\%)' -> 'DR (\\%)') and expand in "
                    f"the caption, or promote to table*"
                )


def _flatten_inputs(paper_dir: Path, text: str, depth: int = 0, seen: set[Path] | None = None) -> str:
    """Inline \\input/\\include targets (recursively, depth-bounded) so a section whose heading sits
    in main.tex and whose body is pulled in via \\input is measured as one unit."""
    if seen is None:
        seen = set()
    if depth > 4:
        return text

    def repl(m: "re.Match[str]") -> str:
        target = m.group(1).strip()
        if not target.endswith(".tex"):
            target += ".tex"
        path = (paper_dir / target).resolve()
        if path in seen or not path.exists():
            return " "
        seen.add(path)
        sub = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        return _flatten_inputs(paper_dir, sub, depth + 1, seen)

    return INPUT_RE.sub(repl, text)


def check_limitations(paper_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Heuristic: a standalone Limitations section that is over-long / over-enumerated / boilerplate.

    Resolves the section body even when the heading lives in main.tex and the prose arrives via
    \\input (the common split that silently defeats a per-file check). Fails past 180 words, on 5+
    separate limitations (\\item, ordinals, or bold-lead paragraphs), or on boilerplate framing.
    Over-long or over-enumerated limitations are blocking for first-draft delivery because they are
    easy to fix in writing and otherwise hand reviewers avoidable objections.
    """
    main = paper_dir / "main.tex"
    if main.exists():
        text = _flatten_inputs(paper_dir, strip_comments(main.read_text(encoding="utf-8", errors="ignore")))
        where = "Limitations (via main.tex)"
    else:
        text = "\n".join(
            strip_comments(p.read_text(encoding="utf-8", errors="ignore")) for p in prose_tex_files(paper_dir)
        )
        where = "Limitations"
    m = LIMITATIONS_HEADING_RE.search(text)
    if not m:
        return
    nxt = LIM_NEXT_BOUNDARY_RE.search(text, m.end())
    section = text[m.end() : nxt.start() if nxt else len(text)]

    plain = re.sub(r"\\[a-zA-Z]+\*?", " ", section)
    plain = re.sub(r"[{}\\$&~^_%#]", " ", plain)
    words = len(plain.split())
    points = max(
        len(ITEM_RE.findall(section)),
        len(LIM_ORDINAL_RE.findall(section)),
        len(LIM_BOLD_LEAD_RE.findall(section)),
    )

    if words > LIMITATIONS_MAX_WORDS:
        errors.append(
            f"{where} section is long ({words} words); cap at ~120-180 words, keep the 3-4 most "
            f"material limitations, 1-2 sentences each"
        )
    if points >= LIMITATIONS_MAX_POINTS:
        errors.append(
            f"{where} enumerates {points} separate points; merge or cut to the 3-4 a reviewer would "
            f"actually raise"
        )
    if LIM_OPENER_RE.search(section) or LIM_CLOSER_RE.search(section):
        warnings.append(
            f"{where} has boilerplate framing; drop the \"we acknowledge several limitations\" opener "
            f"/ \"despite these limitations\" closer and lead directly with the first limitation"
        )


def column_types(colspec: str) -> list[str]:
    """Return the ordered column types of a tabular colspec, with p/m/b/X/Y/Z treated as wrapping."""
    spec = re.sub(r"[><@!]\{(?:[^{}]|\{[^{}]*\})*\}", "", colspec)   # drop >{} <{} @{} !{}
    spec = re.sub(r"[pmb]\{(?:[^{}]|\{[^{}]*\})*\}", "p", spec)       # p{..}/m{..}/b{..} -> wrapping 'p'
    spec = re.sub(r"[LC]\{(?:[^{}]|\{[^{}]*\})*\}", "p", spec)        # package-local fixed-width columns
    return [ch for ch in spec if ch in "lcrpXYZS"]


def _split_cells(row: str) -> list[str]:
    """Split a tabular row into cells on unescaped &."""
    return re.split(r"(?<!\\)&", row)


def check_prose_in_narrow_column(path: Path, base: Path, errors: list[str]) -> None:
    """Heuristic: a prose cell sitting in a non-wrapping l/c/r column cannot break and overflows.

    Targets the defect where a 'Description'/'Notes' column is declared r/l/c instead of a wrapping
    Y/X/p{..} column, so its text runs off the page (a frequent source of margin overflow that the
    column-count check misses because the table has few columns). Warnings only.
    """
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    for block in iter_tabular_blocks(text):
        types = column_types(block.colspec)
        if not types or not any(t in "lcr" for t in types):
            continue
        body = block.body
        offending: set[int] = set()
        for raw_row in re.split(r"\\\\", body):
            if "\\multicolumn" in raw_row or "\\midrule" in raw_row or "\\toprule" in raw_row \
                    or "\\bottomrule" in raw_row or "\\cmidrule" in raw_row:
                continue
            cells = _split_cells(raw_row)
            for idx, cell in enumerate(cells):
                if idx >= len(types) or types[idx] not in "lcr":
                    continue
                plain = re.sub(r"\\[a-zA-Z]+\*?", " ", cell)
                plain = re.sub(r"[{}\\$&~^_%#]", " ", plain)
                nwords = sum(1 for w in plain.split() if any(c.isalpha() for c in w))
                if nwords >= PROSE_CELL_MIN_WORDS:
                    offending.add(idx)
        if offending:
            lineno = text.count("\n", 0, block.start) + 1
            cols = ", ".join(f"col {i + 1} ({types[i]})" for i in sorted(offending))
            errors.append(
                f"prose in a non-wrapping column: {name}:{lineno}; {cols} hold multi-word text in an "
                f"l/c/r column that cannot line-break and will run off the page — use a wrapping "
                f"column (tabularx Y/X or p{{...}}) for the prose column"
            )


def check_limitations_placement(files: list[Path], base: Path, errors: list[str]) -> None:
    """Limitations must live in one dedicated \\section{Limitations}, not scattered in body sections.

    Flags two defects: (1) a Limitations-titled \\subsection / \\paragraph / \\textbf run-in inside
    another section (e.g. an Experiments section), and (2) more than one dedicated Limitations
    section (a sign limitations are duplicated across, say, Conclusion and a standalone section).
    """
    dedicated: list[str] = []
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        name = rel(path, base)
        for lineno, line in enumerate(text.splitlines(), 1):
            if LIMIT_SECTION_RE.search(line):
                dedicated.append(f"{name}:{lineno}")
            for rx, kind in (
                (LIMIT_SUBSECTION_RE, "\\subsection"),
                (LIMIT_PARAGRAPH_RE, "\\paragraph"),
                (LIMIT_RUNIN_RE, "\\textbf run-in"),
            ):
                if rx.search(line):
                    errors.append(
                        f"misplaced Limitations unit ({kind}) inside a body section: {name}:{lineno}; "
                        f"move limitations into a single dedicated \\section{{Limitations}} (kept out "
                        f"of the main content-page budget for venues that exclude it)"
                    )
    if len(dedicated) > 1:
        errors.append(
            "more than one dedicated Limitations section: "
            + ", ".join(dedicated)
            + "; consolidate limitations into one section, do not repeat them"
        )


def check_invalid_latex_environments(files: list[Path], base: Path, errors: list[str]) -> None:
    """Flag sectioning commands written as environments.

    LaTeX has `\\section{...}` commands, not `\\begin{section}` / `\\end{section}` environments.
    An erroneous `\\end{section}` can leave labels unresolved and surface as `Table ??` in the PDF.
    """
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        name = rel(path, base)
        for lineno, line in enumerate(text.splitlines(), 1):
            if INVALID_SECTION_ENV_RE.search(line):
                errors.append(
                    f"invalid LaTeX section environment: {name}:{lineno}: "
                    f"use \\section{{...}} commands only; remove \\begin/\\end{{section}}"
                )


def check_hardcoded_structural_refs(files: list[Path], base: Path, errors: list[str]) -> None:
    """Flag hand-written Table/Figure/Section numbers in source.

    Drafts must use `\\label{...}` and `\\ref{...}` for structural references. Hard-coded numbers
    silently go stale after float movement or appendix insertion, and they hide missing labels until
    the rendered PDF shows `Table ??` / `Section ??`.
    """
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        name = rel(path, base)
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in HARDCODED_STRUCTURAL_REF_RE.finditer(line):
                errors.append(
                    f"hard-coded structural reference: {name}:{lineno}: '{m.group(0)}'; "
                    f"use \\label{{...}} and \\ref{{...}} instead of manual numbering"
                )


def check_labels(files: list[Path], base: Path, errors: list[str]) -> None:
    seen: dict[str, str] = {}
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in LABEL_RE.finditer(line):
                key = m.group(1).strip()
                loc = f"{rel(path, base)}:{lineno}"
                if key in seen:
                    errors.append(f"duplicate \\label: {key} ({seen[key]} and {loc})")
                else:
                    seen[key] = loc


def check_input_consistency(paper_dir: Path, errors: list[str], warnings: list[str]) -> None:
    main = paper_dir / "main.tex"
    if not main.exists():
        warnings.append("no main.tex found; skipped input-consistency check")
        return
    text = strip_comments(main.read_text(encoding="utf-8", errors="ignore"))
    inputs = set()
    for m in INPUT_RE.finditer(text):
        target = m.group(1).strip()
        if not target.endswith(".tex"):
            target += ".tex"
        inputs.add((paper_dir / target).resolve())
    for target in sorted(inputs):
        if not target.exists():
            errors.append(f"\\input references missing file: {rel(target, paper_dir)}")
    sec_dir = paper_dir / "sections"
    if sec_dir.is_dir():
        for path in sorted(sec_dir.glob("*.tex")):
            if path.resolve() not in inputs:
                warnings.append(f"orphan section file not \\input by main.tex: {rel(path, paper_dir)}")


def check_log(paper_dir: Path, errors: list[str], warnings: list[str]) -> None:
    log = paper_dir / "main.log"
    if not log.exists():
        return
    text = log.read_text(encoding="utf-8", errors="ignore")
    if "There were undefined references" in text or re.search(r"Reference `[^']+' on page", text):
        errors.append("compile log: undefined references present; rerun LaTeX or fix missing labels before returning")
    if re.search(r"Citation `[^']+' (?:on page .*?)?undefined", text):
        errors.append("compile log: undefined citations present; fix missing BibTeX entries before returning")
    if "multiply defined" in text:
        warnings.append("compile log: multiply-defined labels present")
    for m in re.finditer(r"Float too large for page by\s+([\d.]+)pt(?:.*?line\s+([\d-]+))?", text, re.I):
        pt = float(m.group(1))
        where = f" at line {m.group(2)}" if m.group(2) else ""
        errors.append(
            f"compile log: float too large for page by {pt:.0f}pt{where}; "
            "resize, split, move, or re-place the figure/table before returning the draft"
        )
    # Overfull \vbox = vertical content ran past the page bottom, commonly from an oversized
    # [H] float or a float/caption block that cannot fit in the available page height.
    small_vbox = 0
    for m in re.finditer(
        r"Overfull \\vbox \(([\d.]+)pt too high\)(?:.*?lines? ([\d-]+))?",
        text,
        re.I,
    ):
        pt = float(m.group(1))
        if pt < OVERFULL_ERROR_PT:
            small_vbox += 1
            continue
        where = f" at lines {m.group(2)}" if m.group(2) else ""
        errors.append(
            f"compile log: vertical overflow by {pt:.0f}pt{where} "
            "(figure/table/caption block exceeds the page height; resize, split, or adjust placement)"
        )
    if small_vbox:
        warnings.append(f"compile log: {small_vbox} minor overfull vbox warning(s) (< {OVERFULL_ERROR_PT:.0f}pt)")
    # Overfull \hbox = content pushed past the text/column edge into the margin
    # ("出界"). A large overfull is almost always a figure/table/overlay exceeding
    # \textwidth or \columnwidth and is a hard defect; tiny ones (long words, URLs)
    # are cosmetic. Block on the large ones, warn on the rest.
    small = 0
    for m in re.finditer(
        r"Overfull \\hbox \(([\d.]+)pt too wide\)(?: in paragraph at lines ([\d-]+))?", text
    ):
        pt = float(m.group(1))
        if pt < OVERFULL_ERROR_PT:
            small += 1
            continue
        where = f" at lines {m.group(2)}" if m.group(2) else ""
        errors.append(
            f"compile log: content overflows the margin by {pt:.0f}pt{where} "
            f"(figure/table/overlay wider than \\textwidth/\\columnwidth; cap width, trim "
            f"baked-in whitespace, or clamp the overlay bounding box)"
        )
    if small:
        warnings.append(f"compile log: {small} minor overfull hbox warning(s) (< {OVERFULL_ERROR_PT:.0f}pt)")


def check_generated_plot_scripts(paper_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Require generated plot scripts with raw hex palettes to name the registered palette."""
    scripts_dir = paper_dir / "scripts"
    if not scripts_dir.exists():
        return
    for path in sorted(scripts_dir.glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not HEX_COLOR_RE.search(text):
            continue
        if not (PALETTE_ASSIGN_RE.search(text) or "plt." in text or "matplotlib" in text):
            continue
        if REGISTERED_CS_PALETTE_RE.search(text):
            continue
        errors.append(
            f"unregistered plot palette: {rel(path, paper_dir)} defines raw hex chart colors but "
            "does not record a registered CS palette name from palette-system.md; choose a named "
            "palette such as CS_PAIRED_OPPOSING_PALETTE, CS_RADAR_PALETTE, "
            "CS_COVERAGE_PALETTE, or CS_BODY_PASTEL_PALETTE"
        )


def check_unresolved_pdf_refs(text_pages: list[str], errors: list[str]) -> None:
    for index, page_text in enumerate(text_pages, 1):
        for m in UNRESOLVED_RENDERED_REF_RE.finditer(page_text):
            snippet = " ".join(page_text[max(0, m.start() - 50): m.end() + 80].split())
            errors.append(f"unresolved rendered reference on PDF page {index}: ...{snippet}...")


def check_rendered_pdf_refs(paper_dir: Path, errors: list[str]) -> None:
    pdf_path = paper_dir / "main.pdf"
    if not pdf_path.exists():
        return
    page_count = pdf_page_count(pdf_path)
    if page_count is None:
        return
    pages = pdf_text_pages(pdf_path, page_count)
    if pages is None:
        return
    check_unresolved_pdf_refs(pages, errors)


def content_pages_before_references(text_pages: list[str]) -> int:
    """Return the last page counted as main content.

    Main content ends at the first post-matter heading (References/Bibliography, or a
    venue-excluded section such as Limitations / Acknowledgments / Ethics / impact
    statement). If that heading starts midway down a page, that page still counts because
    main text reached it. Matching heading-only lines avoids truncating on an inline
    "\\textbf{Limitations ...}" run-in that wrongly sits inside a body section.
    """

    for index, page_text in enumerate(text_pages, 1):
        match = POSTMATTER_HEADING_RE.search(page_text)
        if match:
            before_heading = page_text[: match.start()]
            if _prose_word_count(before_heading) > 0:
                return index
            return max(1, index - 1)
    return len(text_pages)


def pdf_page_count(pdf_path: Path) -> int | None:
    if shutil.which("pdfinfo") is None:
        return None
    proc = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if proc.returncode != 0:
        return None
    for line in proc.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def pdf_text_pages(pdf_path: Path, page_count: int) -> list[str] | None:
    if shutil.which("pdftotext") is None:
        return None
    pages: list[str] = []
    for page in range(1, page_count + 1):
        proc = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), str(pdf_path), "-"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode != 0:
            return None
        pages.append(proc.stdout.replace("\f", ""))
    return pages


def check_page_budget(
    paper_dir: Path,
    max_content_pages: int | None,
    min_content_pages: int | None,
    errors: list[str],
    warnings: list[str],
) -> None:
    if max_content_pages is None and min_content_pages is None:
        return
    pdf_path = paper_dir / "main.pdf"
    if not pdf_path.exists():
        errors.append("content-page budget was set, but paper/main.pdf is missing")
        return
    page_count = pdf_page_count(pdf_path)
    if page_count is None:
        errors.append("cannot check content-page budget because pdfinfo is unavailable or failed")
        return
    pages = pdf_text_pages(pdf_path, page_count)
    if pages is None:
        errors.append("cannot check content-page budget because pdftotext is unavailable or failed")
        return
    check_content_page_bounds_from_pages(
        pages,
        max_content_pages=max_content_pages,
        min_content_pages=min_content_pages,
        errors=errors,
        warnings=warnings,
    )


def check_content_page_bounds_from_pages(
    text_pages: list[str],
    max_content_pages: int | None,
    min_content_pages: int | None,
    errors: list[str],
    warnings: list[str],
) -> None:
    content_pages = content_pages_before_references(text_pages)
    start_errors = len(errors)
    if max_content_pages is not None and content_pages > max_content_pages:
        errors.append(
            f"content-page budget exceeded: main text reaches page {content_pages} "
            f"(limit {max_content_pages}; references page counts if main text reaches it)"
        )
    if min_content_pages is not None and content_pages < min_content_pages:
        errors.append(
            f"content-page budget underfilled: main text reaches page {content_pages} "
            f"(target {min_content_pages}; page-limited drafts should use the confirmed body-page "
            f"budget with substantive content, not stop early)"
        )
    if len(errors) == start_errors:
        target = max_content_pages if max_content_pages is not None else min_content_pages
        warnings.append(f"content-page budget ok: main text reaches page {content_pages}/{target}")


def audit(
    paper_dir: Path,
    max_content_pages: int | None = None,
    min_content_pages: int | None = None,
    framework_path: Path | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if framework_path is not None and framework_path.exists():
        framework_target, framework_bound = parse_framework_page_budget(framework_path)
        if max_content_pages is None and framework_bound is not None:
            max_content_pages = framework_bound
            warnings.append(
                f"framework content-page bound applied: --max-content-pages {max_content_pages}"
            )
        if min_content_pages is None and framework_target is not None:
            min_content_pages = framework_target
            warnings.append(
                f"framework content-page target applied: --min-content-pages {min_content_pages}"
            )

    files = prose_tex_files(paper_dir)
    if not files:
        errors.append(f"no .tex files found under {paper_dir}")
        return errors, warnings

    naming_map, do_not_disclose, disclosure_path = parse_disclosure_config(paper_dir)
    if disclosure_path is None:
        warnings.append(
            "no paper/.disclosure.yaml found; disclosure check runs in heuristic-only mode "
            "(export the Writing Policy Naming Map / Do-Not-Disclose tables to enable exact matching)"
        )
    # display names are legitimate; never warn on them via the heuristic
    allow = {display for _, display in naming_map if display}

    for path in files:
        check_prose(path, paper_dir, errors, warnings)
        check_subsection_budget(path, paper_dir, errors)
        check_tables(path, paper_dir, errors, warnings)
        check_enumeration(path, paper_dir, errors)
        check_wide_tables(path, paper_dir, errors, warnings)
        check_prose_in_narrow_column(path, paper_dir, errors)
        check_disclosure(path, paper_dir, naming_map, do_not_disclose, errors)
        check_internal_id_heuristic(path, paper_dir, allow, warnings)
    check_heading_quality(files, paper_dir, errors)
    check_front_matter_discipline(paper_dir, errors, warnings)
    check_limitations(paper_dir, errors, warnings)
    check_booktabs_loaded(paper_dir, files, errors)
    check_appendix_page(paper_dir, warnings)
    check_appendix_plan(paper_dir, errors)
    check_appendix_substance(paper_dir, warnings)
    check_limitations_placement(files, paper_dir, errors)
    check_invalid_latex_environments(files, paper_dir, errors)
    check_hardcoded_structural_refs(files, paper_dir, errors)
    check_labels(files, paper_dir, errors)
    check_input_consistency(paper_dir, errors, warnings)
    check_framework_alignment(paper_dir, framework_path, errors, warnings)
    check_section_compliance_ledger(paper_dir, framework_path, errors)
    check_generated_plot_scripts(paper_dir, errors, warnings)
    check_log(paper_dir, errors, warnings)
    check_rendered_pdf_refs(paper_dir, errors)
    check_page_budget(paper_dir, max_content_pages, min_content_pages, errors, warnings)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit mechanical draft-hygiene rules for a LaTeX paper.")
    parser.add_argument("paper_dir", nargs="?", default="paper", help="Paper directory containing main.tex")
    parser.add_argument(
        "--max-content-pages",
        type=int,
        default=None,
        help="Fail if compiled main text reaches beyond this page before references.",
    )
    parser.add_argument(
        "--min-content-pages",
        type=int,
        default=None,
        help="Fail if compiled main text ends before this page before references.",
    )
    parser.add_argument(
        "--framework",
        type=Path,
        default=None,
        help="Confirmed Paper Framework markdown file; enables Framework Figure Plan alignment checks.",
    )
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    errors, warnings = audit(
        paper_dir,
        max_content_pages=args.max_content_pages,
        min_content_pages=args.min_content_pages,
        framework_path=args.framework.resolve() if args.framework else None,
    )

    print(f"Draft hygiene audit: {paper_dir}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- WARN: {item}")
    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- ERROR: {item}")
        print(f"\nFAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
