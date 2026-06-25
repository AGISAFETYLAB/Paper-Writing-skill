# paper-figure MCP

Chinese: [README.md](README.md)

Narrow MCP display helper for the `academic-writing` skill.

It is intentionally limited to display-specific work:

- classify a figure/table idea into a plot, schematic, picture, or table route,
- write a FigureSpec JSON skeleton from built-in templates for pipeline/framework, architecture, taxonomy, benchmark-construction, or a minimal custom diagram,
- validate and render a medium-complexity FigureSpec JSON to an editable academic-style SVG diagram,
- write a Picture Brief Markdown file with a Direct Image Prompt for AI-generated paper pictures.

It does not write paper prose, invent claims, invent results, manage the paper workflow, or call an image-generation API. The Picture Brief records the renderer route; a separate renderer or current agent performs the actual picture generation.

## Register

```bash
codex mcp add paper-figure -- python3 /path/to/academic-writing/mcp-servers/paper-figure/server.py
```

Use the equivalent MCP registration command for non-Codex hosts.

## Tools

- `classify_figure`
- `write_figurespec_skeleton` accepts optional `template` values: `pipeline`, `architecture`, `taxonomy`, `benchmark`, or `minimal`.
- `write_picture_brief`
- `render_figurespec` renders a FigureSpec JSON to an editable SVG diagram suitable for paper inclusion.

## Output Policy

The server only writes under the provided `cwd`. Recommended paths:

```text
paper/figures/specs/<figure-id>.json
paper/figures/<figure-id>.svg
paper/figures/<figure-id>.pdf
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.png
```

`write_picture_brief` records the picture route from standard provider environment variables; it does not call the provider.

`render_figurespec` is best for deterministic architecture, pipeline, workflow, and taxonomy schematics after the spec's semantic accuracy has been verified.
