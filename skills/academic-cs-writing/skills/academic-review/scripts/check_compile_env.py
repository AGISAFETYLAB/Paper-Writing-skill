#!/usr/bin/env python3
"""Detect whether the environment can compile the LaTeX project to PDF.

The academic-writing workflow treats the compiled PDF as authoritative for the
page-budget, overfull-box, and float/layout gates. Those gates can only run when
a LaTeX engine (and, for page counting, a PDF reader) is installed. This script
reports what is available so the agent can either compile, or tell the user
explicitly that the compiled-PDF gates were skipped.

Usage
-----
    python3 check_compile_env.py            # human-readable report
    python3 check_compile_env.py --json     # machine-readable report

Exit codes
----------
    0  a LaTeX engine is available (the agent should compile)
    1  no LaTeX engine is available (the agent must warn the user and run
       static audits only)
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from typing import Callable

# Ordered by preference; the first available engine is the recommended compiler.
LATEX_ENGINES = ["latexmk", "pdflatex", "xelatex", "lualatex"]
BIB_TOOLS = ["bibtex", "biber"]
PDF_READERS = ["pdfinfo", "pdftotext"]  # poppler-utils — used for page counting
ALL_TOOLS = LATEX_ENGINES + BIB_TOOLS + PDF_READERS


def detect_tools(which: Callable[[str], str | None] | None = None) -> dict[str, str | None]:
    """Return {tool_name: resolved_path_or_None} for every tool we care about.

    `which` is resolved at call time (not bound as a default) so tests can patch
    ``shutil.which`` and ``main`` picks up the override.
    """
    if which is None:
        which = shutil.which
    return {tool: which(tool) for tool in ALL_TOOLS}


def _first_available(tools: dict[str, str | None], candidates: list[str]) -> str | None:
    for name in candidates:
        if tools.get(name):
            return name
    return None


def recommended_command(compiler: str | None) -> str | None:
    if compiler is None:
        return None
    if compiler == "latexmk":
        return "latexmk -pdf main.tex"
    # Plain engines need two passes (plus bibtex/biber) to resolve refs/citations.
    return f"{compiler} main.tex && {compiler} main.tex"


def evaluate(tools: dict[str, str | None]) -> dict:
    """Summarize detection into an actionable verdict."""
    compiler = _first_available(tools, LATEX_ENGINES)
    can_compile = compiler is not None
    can_read_pdf = _first_available(tools, PDF_READERS) is not None
    has_bib = _first_available(tools, BIB_TOOLS) is not None

    if not can_compile:
        message = (
            "PDF compilation UNAVAILABLE: no LaTeX engine (latexmk/pdflatex/xelatex/lualatex) "
            "on PATH. The agent must generate LaTeX source and run static audits only; it CANNOT "
            "verify the compiled PDF (page budget, overfull boxes, float/layout). Install TeX Live "
            "(e.g. 'apt-get install texlive-latex-extra latexmk' or MacTeX) to enable compiled-PDF "
            "gates, and tell the user explicitly that those gates were skipped."
        )
    elif not can_read_pdf:
        message = (
            f"PDF compilation available via '{compiler}', but no PDF reader (pdfinfo/pdftotext) is "
            "installed, so the compiled page count cannot be measured. Install poppler-utils to "
            "enable the page-budget gate; warn the user that page counting is unavailable."
        )
    else:
        message = f"PDF compilation available via '{compiler}'; page-budget and layout gates can run."

    return {
        "can_compile": can_compile,
        "compiler": compiler,
        "can_read_pdf": can_read_pdf,
        "has_bib_tool": has_bib,
        "recommended_command": recommended_command(compiler),
        "tools": tools,
        "message": message,
    }


def format_human(result: dict) -> str:
    lines = ["LaTeX compile-environment check", "=" * 32]
    for tool in ALL_TOOLS:
        path = result["tools"].get(tool)
        lines.append(f"  {tool:10s} {'found: ' + path if path else 'not found'}")
    lines.append("")
    lines.append(f"can_compile : {result['can_compile']}")
    lines.append(f"compiler    : {result['compiler'] or '(none)'}")
    lines.append(f"can_read_pdf: {result['can_read_pdf']}")
    lines.append(f"has_bib_tool: {result['has_bib_tool']}")
    if result["recommended_command"]:
        lines.append(f"compile with: {result['recommended_command']}")
    lines.append("")
    lines.append(result["message"])
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Detect LaTeX/PDF compile capability.")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report.")
    args = parser.parse_args(argv)

    result = evaluate(detect_tools())
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human(result))
    return 0 if result["can_compile"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
