# LaTeX-first Route

Use when the confirmed Submission Format Route is `latex-first`.

## Required Production Artifact

The primary production files are `paper/main.tex` and compiled `paper/main.pdf`. Keep
`paper/references.bib`, figure assets, table fragments, and submission-package records alongside the
source.

## Assembly Requirements

- Use an official downloaded LaTeX class/template when available, such as the package-local Springer
  Nature article template when it fits the confirmed journal route.
- Never hand-write an official class or preamble from memory.
- Link figure assets with `\includegraphics` and use display widths that fit the claim and final
  layout.
- Use `booktabs`, deliberate column widths, compact notes, and rendered inspection for clinical
  tables.

## PASS Gate

Record `format-specific production gate: PASS (latex-first)` only when:

- `paper/main.tex` exists;
- `paper/main.pdf` exists and is generated from the source;
- the compile gate is recorded with the command and status;
- references, figures, tables, statements, and checklist material are included or explicitly
  blocked;
- no required display, citation, or statement marker remains unresolved when the package is called
  submission-ready.

If no LaTeX engine is available, keep the source package and mark compile status blocked or
unverified rather than silently passing.
