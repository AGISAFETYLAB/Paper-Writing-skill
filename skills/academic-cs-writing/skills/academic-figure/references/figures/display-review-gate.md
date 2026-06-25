# Display Review Gate

Use this reference after a figure, schematic, picture, or qualitative composite has been rendered.
Do not use it to plan the Figure Plan or choose chart families.

## Ownership Boundary

This file owns executable rendered-output inspection and failure signatures.
It does not own Figure Plan composition, chart-family selection, or plotting helper implementations.

## Display Review Gate

A figure is not done when the script runs without error. It is done when its rendered PNG has been
opened and inspected. Judging a figure from code alone is the main reason generated figures ship
ugly. After every figure render, and after any change to a figure, run this loop:

1. Render the required formats for the route: SVG/PDF/PNG for data plots and deterministic
   schematics, PNG plus paper-facing PDF wrapper for picture-style figures, and compiled PDF for
   LaTeX tables.
2. Open the PNG or compiled PDF page. Do not infer quality from source code, dimensions, or a
   successful command exit.
3. Score against the failure signatures below. Any hit means revise the source and regenerate.
4. Reopen the regenerated artifact and repeat the check before accepting the item.

## Data-Driven Plot Failure Signatures

| Signature | What to look for in the rendered artifact | Fix |
|---|---|---|
| **Muddy overlap** | Filled radar, area, or multi-series shapes blur into an indistinct blob and methods cannot be separated. | Radar: use the `CS_RADAR_PALETTE` marker/linestyle grammar, keep fills at `alpha <= 0.04`, cap reference radars at six traces and body-compact radars at four, or switch to grouped bars / heatmap. Area plots: lower alpha or switch to lines. |
| **Clipped elements** | Error-bar whiskers, caps, value labels, markers, or annotations touch or cross the axis or figure edge. | Compute limits from `values +/- error`, add label headroom, and re-render. Never set y-limits from bar heights alone when error bars or labels exist. |
| **Low contrast / color-only** | Foreground series is washed out; text disappears into its background; identity depends only on hue; rainbow/jet is used. | Use palette names from `palette-system.md`, add redundant markers or hatches, select text color by luminance, and reserve grey for neutral/receding series. |
| **Label collision** | Tick labels, spoke labels, radial ticks, legends, or annotations overlap data or each other. | Offset spoke labels, rotate or align ticks, move legends below, remove default polar ticks, or split the panel. |

## Schematic And Picture Failure Signatures

| Signature | What to look for in the rendered artifact | Fix |
|---|---|---|
| **Wrong schematic semantics** | A module is missing, edge direction is reversed, grouping implies the wrong dependency, or novelty is not identifiable. | Edit the FigureSpec/Mermaid/TikZ/SVG source and re-render. Do not hide a semantic error in the caption. |
| **Garbled / wrong picture text** | A rendered label is misspelled, uses the wrong term, is duplicated, or a prompt header leaked into the figure. | Verify each word against the Writing Policy terms; regenerate with the correct spelling or use the TikZ overlay fallback in `picture-generation.md`. |
| **Boxy illustration** | The picture route produced only rounded rectangles in a row with arrows. | If the paper needs a formal diagram, reroute to `schematic-design.md`; if it needs an illustration, rewrite the prompt toward a real scene, UI, iconography, or actors. |
| **Empty bands / off-center / too tall** | A large blank strip appears while content crowds one area, or a banner is so tall that it consumes too much page space. | Re-prompt for a wide, short, edge-to-edge banner; cap height with `keepaspectratio`; trim empty bands; resize schematic canvas and redistribute nodes. |
| **Out of bounds / overflow** | The figure runs past the column or text edge, or the LaTeX log reports an overfull box for the figure. | Clamp the image or overlay to the declared width, inset edge labels, cap the width, and recompile. |
| **Overlay misalignment** | After TikZ overlay, a label floats away from its element or leaves the image boundary. | Open the PDF, nudge normalized `(x,y)` coordinates, keep label boxes inside `[0,1]`, recompile, and re-inspect. |

## Contract Checks

Confirm all of the following before accepting a display item:

- All planned panels appear and serve the core conclusion.
- No extra claim, dataset, metric, module, method name, or paper-specific term was invented by the
  renderer.
- Visible text is readable at paper scale and matches the allowed labels from the Writing Policy.
- The item fits its declared single-column or double-column width and does not overflow into the
  margin.
- The height is reasonable for its role and the image fills its frame without empty bands.
- Arrows, relationships, metric directions, and data directions are correct.
- The item is paper-ready rather than slide-deck decorative.
- The generated file is non-empty and stored at the recorded output path.

After every figure passes its individual Display Review Gate, run the submission-readiness checklist
in `qa-contract.md` for cross-figure checks: unified visual family, statistics minimum,
image-integrity, and export bundle.
