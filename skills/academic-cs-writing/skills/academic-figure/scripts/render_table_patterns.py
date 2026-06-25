#!/usr/bin/env python3
"""Render reusable LaTeX table pattern snippets into preview PDFs.

Do not edit generated previews; update assets/table-patterns/*.tex instead.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SNIPPETS = (
    "full_width_numeric_scorecard.tex",
    "multi_dataset_metric_matrix.tex",
    "compact_ablation_or_sensitivity.tex",
    "matched_condition_delta.tex",
    "wrapped_taxonomy_or_protocol.tex",
    "setup_or_split_summary.tex",
)

PAGE_SIZES = {
    "full_width_numeric_scorecard": ("7.6in", "3.2in"),
    "multi_dataset_metric_matrix": ("7.6in", "3.1in"),
    "compact_ablation_or_sensitivity": ("6.2in", "2.8in"),
    "matched_condition_delta": ("6.0in", "3.0in"),
    "wrapped_taxonomy_or_protocol": ("7.2in", "3.4in"),
    "setup_or_split_summary": ("7.2in", "3.3in"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd() / "table-pattern-previews",
        help="Directory for generated preview PDFs and build files.",
    )
    parser.add_argument(
        "--snippet-dir",
        type=Path,
        default=None,
        help="Override the snippet directory. Defaults to assets/table-patterns next to this script.",
    )
    return parser.parse_args()


def latex_preamble(paper_width: str, paper_height: str) -> str:
    return "\n".join(
        [
            r"\documentclass[10pt]{article}",
            rf"\usepackage[paperwidth={paper_width},paperheight={paper_height},margin=0.25in]{{geometry}}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\usepackage{array}",
            r"\usepackage{booktabs}",
            r"\usepackage{tabularx}",
            r"\usepackage[table]{xcolor}",
            r"\pagenumbering{gobble}",
            r"\setlength{\parindent}{0pt}",
            r"\begin{document}",
            "",
        ]
    )


def standalone_document(snippet: str, stem: str) -> str:
    paper_width, paper_height = PAGE_SIZES.get(stem, ("7.2in", "3.2in"))
    return latex_preamble(paper_width, paper_height) + snippet + "\n\\end{document}\n"


def run_latexmk(latexmk: str, wrapper_path: Path, build_dir: Path) -> None:
    cmd = [
        latexmk,
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-outdir=.",
        wrapper_path.name,
    ]
    result = subprocess.run(
        cmd,
        cwd=build_dir,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-80:])
        raise SystemExit(f"latexmk failed for {wrapper_path.name}:\n{tail}")


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    snippet_dir = args.snippet_dir or (skill_dir / "assets/table-patterns")
    output_dir = args.output_dir.resolve()
    build_dir = output_dir / "build"
    output_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)

    latexmk = shutil.which("latexmk")
    if latexmk is None:
        raise SystemExit("latexmk is required to render table pattern previews.")

    rendered = []
    for snippet_name in SNIPPETS:
        snippet_path = snippet_dir / snippet_name
        if not snippet_path.exists():
            raise SystemExit(f"missing snippet: {snippet_path}")
        stem = snippet_path.stem
        wrapper_path = build_dir / snippet_name
        wrapper_path.write_text(standalone_document(snippet_path.read_text(encoding="utf-8"), stem), encoding="utf-8")
        run_latexmk(latexmk, wrapper_path, build_dir)
        pdf_path = build_dir / f"{stem}.pdf"
        if not pdf_path.exists():
            raise SystemExit(f"latexmk completed but did not create {pdf_path}")
        target_path = output_dir / pdf_path.name
        shutil.copy2(pdf_path, target_path)
        rendered.append(target_path)

    for path in rendered:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
