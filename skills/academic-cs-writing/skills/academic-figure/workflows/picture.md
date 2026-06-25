# Picture Workflow

Execution-only workflow for picture-style figures: teaser images, conceptual method illustrations,
scene-like overviews, paper-ready raster illustrations, qualitative composites, and screenshots.

## Workflow

1. Read the confirmed Figure Plan entry when present. Record or update the item's row in
   `paper/framework-execution-report.md` for paper-level runs.
2. Load `references/figures/figure-planning.md` and `references/figures/picture-generation.md`.
3. Confirm this is not a formal framework/pipeline/architecture schematic. If it is, route to
   `workflows/schematic.md` unless the user explicitly wants an illustrative raster rendering.
4. Write `paper/figures/prompts/<figure-id>.md` before rendering. The Picture Brief must include
   evidence boundary, exact allowed labels, forbidden labels/claims, Direct Image Prompt, label
   verification plan, overlay fallback plan, and renderer route.
5. Render outside `paper-figure` through the selected picture renderer when available, or use the
   current-agent fallback to produce an accurate paper-safe image. The `paper-figure` MCP helper can
   write the brief and record the route, but it does not call image APIs. For Gemini/OpenAI-compatible
   APIs, prefer `scripts/render_picture_api.py` and pass the Picture Brief unchanged. For teaser or
   method banners, use the script's `--trim-whitespace` and `--pad-aspect` options when the model
   returns a square canvas or excessive blank bands. The render step must keep the inspected PNG and
   write a sibling PDF wrapper for LaTeX/submission use. The picture route may never invent modules,
   datasets, numbers, paper claims, or labels.
   For any picture route with `GEMINI_API_KEY` or `OPENAI_API_KEY` visible, the render step is
   mandatory: call `scripts/render_picture_api.py` without `--dry-run`, inspect the resulting PNG,
   and record the renderer in `paper/framework-execution-report.md`. A `--dry-run` proves routing
   only; it is not a rendered figure. Do not record `no external image API was used` when a renderer
   key is visible.
6. Open the rendered image and verify every visible word. If a label is misspelled, garbled,
   duplicated, unsupported, or copied from prompt scaffolding, regenerate or use the overlay fallback.
   For simple horizontal banners, `render_picture_api.py --overlay-labels-from-brief --overlay-layout
   horizontal-bottom` is the preferred lightweight fallback.
7. Check aspect ratio, crop/trim, overflow, and page fit. A picture that is too tall, has empty
   bands, spills into margins, or is unreadable at paper scale is not accepted.
8. Insert only at the Paper Framework's target section and width. Captions must state the message and
   supported claim, not just describe the picture.

For qualitative composites built from existing screenshots/examples, record the source asset path
and do not use an image generator to fabricate examples.
