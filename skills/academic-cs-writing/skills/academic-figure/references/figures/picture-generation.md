# Picture Generation

Use this reference when the confirmed Figure Plan contains a picture-style figure:
teaser, overview illustration, conceptual method picture, qualitative visual
summary, paper-ready raster illustration, screenshot composite, or an explicitly
requested AI-generated concept picture.

## Boundary

Picture generation supports visual communication. It must not create new
scientific content. Do not let the renderer invent paper claims, modules,
datasets, results, or labels. Every visible element must come from the
confirmed Writing Policy, confirmed Paper Framework, or concrete workspace
source files.

This route is for polished *illustrative* figures (devices, UI panels, icons,
actors, a scene), not formal framework or pipeline schematics. Formal pipeline,
architecture, workflow, taxonomy, and system-overview diagrams default to
`schematic-design.md` and `workflows/schematic.md`. Use this picture route for
such content only when the user explicitly wants an illustrative raster rendering
rather than an editable technical schematic. The image model may render labels
directly in the image; every visible label must then be verified.

Formal pipeline diagrams default to `schematic-design.md`.

## Text In The Image Is Allowed, But Must Be Verified (critical)

This skill's focus is the paper, not figure tooling, so the image model is allowed
to render the figure's labels directly in the image. The price is that raster
image models **sometimes misspell** — real generations from this skill produced
`Indulator` (Emulator), `Doicker` (Docker), `Missformation` (Misinformation), and
`pipeine` (pipeline). Garbled or wrong text in a paper figure is still fatal, so
the policy is *generate-then-verify*, not *forbid*:

- **Tell the model exactly which labels to render, spelled correctly.** List the
  exact label strings (from the Writing Policy / Paper Framework) in the prompt and
  ask for clean, legible, correctly spelled sans-serif text. Do not invent labels,
  numbers, claims, modules, or datasets the paper does not support.
- **Verify every visible word after generation (mandatory).** Open the rendered
  PNG and read each label. If any word is misspelled, garbled, duplicated, or does
  not match the paper's exact terminology, the figure fails — **regenerate** (re-emphasizing the exact label spelling), or fix that label with the overlay
  fallback below. A figure with a misspelled label must never ship.
- **Never paste the prompt scaffolding into the image.** The lines `Message:`,
  `Show exactly these components:`, and `Use exactly these labels:` are
  instructions to *you*, not text to be drawn. A clean Direct Image Prompt is a
  single visual description with the label strings woven in naturally, not a rubric
  dump (a past run drew the literal `Message:` sentence into the figure).

### Overlay Fallback Pattern (LaTeX/TikZ) — when the model cannot spell a label

The hybrid overlay is no longer mandatory; use it as a **fallback** when the model
keeps misspelling a specific label, when a label must stay editable, or when you
deliberately generate a text-free illustration and add all labels yourself. In that
case generate the illustration (text-free for that region), then place labels over
it with TikZ in a normalized 0–1 coordinate space, tuning anchor positions by
**looking at the rendered PNG** and adjusting:

```tex
\begin{figure*}[t]
\centering
\begin{tikzpicture}
  % background illustration drawn by the image model (text-free)
  \node[anchor=south west,inner sep=0] (img) at (0,0)
    {\includegraphics[width=\textwidth]{figures/fig1_teaser.png}};
  % CLAMP the picture's bounding box to the image so no overlay node can push the
  % figure past \textwidth into the margin (prevents the Overfull \hbox / "出界").
  \useasboundingbox (img.south west) rectangle (img.north east);
  % overlay exact labels in normalized (x,y) ∈ [0,1] over the image
  \begin{scope}[x={(img.south east)},y={(img.north west)}]
    \node[font=\sffamily\small\bfseries] at (0.10,0.52) {User};
    \node[font=\sffamily\small\bfseries] at (0.46,0.55) {GUI Agent};
    \node[font=\sffamily\footnotesize]   at (0.86,0.74) {HARM};
    % edge labels: inset and anchored INWARD so the label box stays on the image
    \node[anchor=west,font=\sffamily\scriptsize] at (0.04,0.90) {Email};   % left column
    \node[anchor=east,font=\sffamily\scriptsize] at (0.96,0.90) {Phishing}; % right column
    % ... place each label, then recompile and re-inspect alignment
  \end{scope}
\end{tikzpicture}
\caption{...}
\label{fig:teaser}
\end{figure*}
```

Requires `\usepackage{tikz}` in the preamble. Iterate: compile → look at the PDF
→ nudge coordinates until every label sits on its element. If precise overlay is
impractical for a dense figure, fall back to a clean deterministic figure (TikZ
schematic or a compact labeled illustration) rather than shipping garbled
in-image text.

#### Overlay Bounding-Box Rule (prevents 出界 / overfull \hbox)

A `figure*` image at `width=\textwidth` already fills the full text width, so a
TikZ overlay node whose box extends past the image edge enlarges the
`tikzpicture` bounding box and pushes the figure **into the margin** — LaTeX
reports it as `Overfull \hbox (... too wide)` and `audit_draft.py` blocks on it.
Two mandatory guards:

1. **Clamp the picture box to the image.** Immediately after the image node, add
   `\useasboundingbox (img.south west) rectangle (img.north east);`. This fixes
   the figure's size to the image regardless of overlay placement.
2. **Inset edge labels and anchor them inward.** Never place an outward-anchored
   label at the extreme edge (e.g. `anchor=east` at `x≈0.0`, or `anchor=west` at
   `x≈1.0`) — its box spills off the image. Keep every label's *box* inside
   `(x,y) ∈ [0,1]`: put left-edge labels around `x≈0.03–0.06` and right-edge
   labels around `x≈0.94–0.97`, anchoring **toward the image center**. Labels
   live on the image, not in the surrounding whitespace.

### Aspect, Height, And Whitespace (prevents tall figures / "上下边距太长")

The image model emits a fixed canvas (often 16:9, e.g. 1376×768). Forcing
`width=\textwidth` on a 16:9 image makes it ~9–10 cm tall — too tall for a teaser
or pipeline banner — and if the scene only occupies a central strip, the baked-in
empty top/bottom bands read as excessive vertical margin. Control this:

- **Prompt for the right shape.** For a double-column teaser or method-illustration **banner**,
  ask for a **wide, short composition that fills the whole canvas edge to edge**
  (target aspect roughly `3:1` to `4:1`, so at `\textwidth` the height is ~4.5–6
  cm). For a single-column figure target roughly `1.6:1` to `2:1`. State "fill the
  full frame, no empty margins or blank bands" in the Direct Image Prompt.
- **Cap the rendered height.** When in doubt, bound the height explicitly so a
  mis-shaped render cannot eat a third of the page:
  `\includegraphics[width=\textwidth,height=5.5cm,keepaspectratio]{...}` (use a
  larger cap only if the content genuinely needs it).
- **Trim baked-in whitespace instead of shipping it.** If the rendered PNG still
  has empty top/bottom (or side) bands, crop them — either re-export the PNG
  cropped to content, or trim at include time:
  `\includegraphics[trim=0 120 0 120,clip,width=\textwidth]{...}` (`trim` is
  `left bottom right top` in **bigpoints**; read the values off the PNG). Do not
  leave a thin content strip floating in a tall empty box.

## Required Output

Always create the planning artifact and both rendered formats before considering
the picture complete:

```text
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.png
paper/figures/<figure-id>.pdf
```

The PNG is the source raster returned by the image renderer and is the easiest
artifact to inspect for label spelling and visual defects. The PDF is the
paper-facing wrapper used by LaTeX/submission packages. This PDF is still a
raster illustration, not a vectorized reconstruction; if the figure must be
editable/vector, route it to schematic or plot instead.

Do not leave a planned picture blank. If the user does not provide an external
picture API, the current executing agent must draw the picture from the Picture
Brief and insert it into the paper. A lower-fidelity but accurate paper-safe
picture is better than an empty figure slot.

## Picture Brief

The Picture Brief is the agent's picture design plan generated from the paper.
It must be directly usable in two ways:

1. the user can copy it into another AI chat to generate the picture,
2. the current workflow can pass the same prompt to GPT-image2, Gemini, or
   another configured image API.

The Direct Image Prompt is the prompt passed to image APIs and the prompt copied
into another AI chat. Do not rewrite or summarize it before API submission.

Use this file shape:

```markdown
# Picture Brief: <figure-id>

## Figure Identity
- Figure ID:
- Title:
- Section:
- Figure type:
- One-sentence message:
- Supported claim:

## Evidence Boundary
- Source files:
- Confirmed concepts:
- Exact labels to render in the image (correct spelling, from the Writing Policy):
- Labels, numbers, or claims forbidden in the image:

## Visual Plan
- Canvas:
- Layout:
- Main visual elements:
- Data flow or relationships:
- Style:
- Accessibility:

## Direct Image Prompt
<A single clean paragraph describing the scene, with the exact label strings woven
in naturally and a request for clean, legible, correctly spelled sans-serif text.
No rubric headers. Include the visual style requirements below.>

## Label Verification Plan
- Exact labels that must appear, spelled correctly: ...
- After rendering, confirm each label reads correctly; list any that needed a
  regenerate or an overlay fix.

## Overlay Fallback Plan (only if the model misspells a label)
- Labels to overlay instead (exact spelling from Writing Policy): ...
- Approximate normalized positions (x,y in 0–1): ...

## Renderer Route
- Preferred renderer:
- Renderer status:
- Output path:
- PDF output path:
- API prompt source: use the exact `Direct Image Prompt` block above
- Review notes:
```

## Writing the Direct Image Prompt

The Direct Image Prompt is **one clean visual paragraph**, not a filled-in rubric.
Describe the scene the way you would commission an illustrator, and name the exact
labels that should appear, spelled correctly. Quality guardrails:

- **Illustrative, not a flowchart.** Aim for a scene with concrete objects that match the current
  paper — device or interface frames when relevant, process icons, source/target motifs, and outcome
  icons from the Writing Policy — connected by clean arrows. **Do not ask for "rounded rectangles",
  "boxes in a row", or a "flat box-and-arrow flowchart"**; that is exactly the look the user rejected.
- **Academic aesthetic**: flat vector illustration, clean lines, minimalist,
  generous but balanced whitespace (no large empty bands; fill the canvas evenly),
  similar in restraint and clarity to figures in DeepMind or OpenAI papers.
- **Layout**: use an organized flow suited to the content — left-to-right,
  top-to-bottom, circular, or another clear structure — and group related
  components logically.
- **Restrained color**: professional pastel tones on a white background; no
  oversaturated colors.
- **Text in the image**: name the exact labels to render and ask for *"clean,
  legible, correctly spelled sans-serif labels"*. Keep labels few and short (a word
  or two each) — short strings are far less likely to be misspelled than sentences.
  Render only the exact strings in the allowed label list, with identical spelling
  and capitalization. Do not draw example words, aliases, or near-spellings. Key
  method labels or equations mentioned in the methodology (for example, "Encoder",
  "Loss", or "Transformer") must appear only when they are exact allowed labels.
  After rendering, verify every word (see the Review Gate). If a label keeps coming
  out garbled, generate that region text-free and add the label with the overlay
  fallback.
- **Avoid**: photorealism, messy sketch lines, heavy drop shadows, rainbow
  gradients, 3D bevels, 3D shading artifacts, glow effects, unreadable text, and
  long sentences baked into the image.

The rest — palette, exact layout, icon choice — is decided per figure from the
Evidence Boundary and Visual Plan. Do not copy a fixed style string into every
prompt.

### Example Direct Image Prompt (illustrative method banner, with labels)

> A clean flat vector academic illustration of a left-to-right method story for
> constructing and evaluating a benchmark. Five evenly spaced circular icon
> medallions in a single horizontal row, equal spacing, connected by thin clean
> right-pointing arrows: a checklist clipboard, a device screen, an input message,
> a magnifier over a shield, and a compact results table. Below each medallion
> place one short, correctly spelled sans-serif caption, in order: "Tasks",
> "Inputs", "Checks", "Labels", "Metrics". Soft professional pastel palette of
> blue, teal, amber, and slate on a white background, minimalist. Compose as a
> wide, short banner (roughly 3:1) that fills the entire frame edge to edge, with
> no empty top or bottom bands and no wide blank margins. Render only these five
> short labels — clean and legible — and no other text. No photorealistic photos,
> messy sketches, unreadable text, or 3D shading artifacts.

## Image Renderer Preference

Resolve the picture renderer at the beginning of the workflow or as soon as the
user provides the preference:

1. If `GEMINI_API_KEY` is present in the process environment, record a Gemini-compatible route.
2. Otherwise, if `OPENAI_API_KEY` is present, record a GPT-image-compatible route.
3. If a local Codex image bridge or another renderer is explicitly available, record that route.
4. If no picture renderer is available, use the current-agent fallback.

Use standard provider environment variables only. Do not introduce project-specific picture env
prefixes. If an environment variable is exported after the MCP host starts, restart the host before
expecting route detection to change.

If the user says an image API was provided but `GEMINI_API_KEY` and `OPENAI_API_KEY` are not visible
to the current process, stop and report the environment mismatch before rendering or falling back.
Do not silently fall back to deterministic current-agent drawing in that case; the correct action is
to make the API visible to the running host or confirm that fallback drawing is acceptable.

This preference applies only to non-data pictures. Bar charts, line charts,
radar charts, heatmaps, scatter plots, and tables are generated directly by the
current agent from data.

## Renderer Route

After writing the Picture Brief, render the picture outside `paper-figure`.
`paper-figure` only writes the brief and records the route; it does not call
Gemini, OpenAI, Codex image bridge, or any other image API. Prefer the bundled
`scripts/render_picture_api.py` for Gemini/OpenAI-compatible APIs:

```bash
python3 skills/academic-figure/scripts/render_picture_api.py \
  --brief paper/figures/prompts/<figure-id>.md \
  --out paper/figures/<figure-id>.png
```

This writes `paper/figures/<figure-id>.png` and, by default, a sibling
`paper/figures/<figure-id>.pdf`. Use `--pdf-out <path>` to choose another PDF
path or `--no-pdf` only when the caller explicitly wants PNG-only output.

For a teaser, overview, or method-illustration banner where the model returns a
square canvas or excessive whitespace, render with lightweight postprocessing:

```bash
python3 skills/academic-figure/scripts/render_picture_api.py \
  --brief paper/figures/prompts/<figure-id>.md \
  --out paper/figures/<figure-id>.png \
  --trim-whitespace \
  --pad-aspect 3:1
```

Use `--pad-aspect 1.8:1` or `--pad-aspect 2:1` for a single-column picture when
the content is not meant to be a wide double-column banner.

If the picture is visually good but the image model misspells a short label, do
not accept the raster text. For a simple horizontal banner, re-render with exact
deterministic label overlay from the Picture Brief:

```bash
python3 skills/academic-figure/scripts/render_picture_api.py \
  --brief paper/figures/prompts/<figure-id>.md \
  --out paper/figures/<figure-id>.png \
  --trim-whitespace \
  --pad-aspect 3:1 \
  --overlay-labels-from-brief \
  --overlay-layout horizontal-bottom
```

This leaves the API responsible for the illustration style and uses local text
rendering only to enforce exact paper terminology. For non-horizontal layouts,
use the TikZ overlay fallback plan instead of guessing label positions.

If a custom relay is blocked by the host's global HTTP proxy, set
`IMAGE_API_NO_PROXY=1` for this script invocation so the renderer connects
directly to `GEMINI_BASE_URL` / `OPENAI_BASE_URL`.

For every renderer, use the exact `Direct Image Prompt` block as the image
prompt. Do not rewrite, shorten, translate, or embellish it for the API call
unless the user explicitly asks for a different image language or
renderer-specific syntax.

### Gemini API

Detected when `GEMINI_API_KEY` is set.

```bash
# Construct the endpoint from env vars
GEMINI_BASE_URL="${GEMINI_BASE_URL:-https://generativelanguage.googleapis.com}"
MODEL="${GEMINI_IMAGE_MODEL:-gemini-2.5-flash-image}"
URL="${GEMINI_BASE_URL}/v1beta/models/${MODEL}:generateContent"

# Call the API
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "<Direct Image Prompt here>"}], "role": "user"}],
    "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
  }'

# Extract base64 image from response: candidates[0].content.parts[*].inlineData.data
# Save as paper/figures/<figure-id>.png
```

### OpenAI / GPT-Image API

Detected when `OPENAI_API_KEY` is set (and `GEMINI_API_KEY` is not).

```bash
OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://api.openai.com}"
MODEL="${OPENAI_IMAGE_MODEL:-gpt-image-2}"
URL="${OPENAI_BASE_URL}/v1/images/generations"

curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "'"$MODEL"'",
    "prompt": "<Direct Image Prompt here>",
    "n": 1,
    "size": "1024x1024"
  }'
# Response: data[0].b64_json or data[0].url
```

### Codex Image Bridge

Detected only when the host has a local Codex image bridge registered. This route uses the signed-in
Codex app/server path rather than `GEMINI_API_KEY` or `OPENAI_API_KEY`. Pass the exact Direct Image
Prompt to the bridge and poll its status tool until an output path is returned.

### Current Agent Fallback

If no Gemini/OpenAI/Codex-bridge renderer is available, the current executing agent draws the
picture from the Direct Image Prompt. A lower-fidelity but accurate paper-safe picture is better
than an empty figure slot.

## Review Gate

Open the rendered PNG and inspect it (do not infer from the prompt). Reject and
regenerate or redraw if **any** of these fail:

- **Every label is spelled correctly and matches the paper's terminology.** Read
  each word in the image against the exact label strings from the Writing Policy.
  Any misspelling (e.g. `Indulator`, `Missformation`), wrong term, or duplicated
  label means reject — regenerate emphasizing the correct spelling, or fix that
  label with the overlay fallback. A misspelled label must never ship.
- **No leaked scaffolding and no invented text.** Check that no prompt header like
  `Message:` was drawn into the image, and that the model did not add labels,
  numbers, claims, or modules the paper does not support. Either means reject.
- **Illustrative, not a box-and-arrow flowchart.** If it is just rounded
  rectangles in a row, the prompt was wrong — rewrite it toward a scene.
- **No large empty bands**; the composition fills the canvas evenly. A banner with
  empty top/bottom strips reads as "too much vertical margin" — re-prompt for a
  wide, edge-to-edge composition or trim the bands (see Aspect, Height, And
  Whitespace).
- **The figure does not run into the margin.** After compiling, confirm there is
  **no `Overfull \hbox` for the figure** in `main.log` (`audit_draft.py` blocks on
  any overflow ≥10pt). If it overflows, the overlay box exceeds the image — add
  `\useasboundingbox` clamped to the image and inset the edge labels (Overlay
  Bounding-Box Rule).
- **The figure is not too tall.** At `\textwidth` a 16:9 image is ~9–10 cm; a
  teaser/pipeline banner should be ~4.5–6 cm. If it is too tall, fix the aspect,
  cap the height, or trim whitespace — do not let one figure eat a third of the
  page.
- All required components appear; no extra claim, dataset, metric, or module was
  invented; arrows and relationships are directionally correct.
- Every label — whether rendered by the model or added via the overlay fallback —
  **sits on its element**, stays inside the image, and is legible at paper scale.
- The generated file is non-empty and stored at the recorded output path.

If any check fails, revise the prompt (or the overlay coordinates, if used) and
regenerate. Keep rejected versions only when useful for audit.
