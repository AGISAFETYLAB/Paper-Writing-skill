# Stage: Full Draft LaTeX Project Setup

Load this fragment when the Paper Framework has been confirmed and you begin building the `paper/`
LaTeX project. Pair it with `stages/section-drafting.md` for prose, the **`academic-figure`** skill
for every figure/table, the **`academic-citation`** skill for the bibliography, and the
**`academic-review`** skill for the closing gates.

Use the confirmed Writing Policy, confirmed Paper Framework, relevant section guides,
`references/sections/paragraph-flow.md`, and relevant experiment/figure/table materials.

Before drafting prose, read the confirmed Core Section Budget from the Paper Framework. Draft or
internally outline the Primary core section and Evidence core section before finalizing the
Introduction and Abstract, so the framing is based on the actual technical payload rather than on
background prose. For method / algorithm papers, this means building the Method backbone first
(overview, modules, rationale, reproducibility details, and evidence hooks) and then writing the
Introduction around that contribution.

Do not compress a primary-core section below its floor during drafting. If the confirmed budget
cannot fit after compressing support and compress-first sections, stop and return to the Paper
Framework checkpoint; do not silently ship a draft whose Method, construction, system design,
taxonomy, or main-results section is too thin to carry the contribution.

## Compile Environment Check (run once, up front)

Before building the project, run the compile-environment check from the **`academic-review`** skill so
you know whether the compiled-PDF gates can run later:

```bash
python3 "<path-to-academic-review>/scripts/check_compile_env.py"
```

- **Exit 0 (a LaTeX engine is available):** plan to compile the assembled draft with the reported
  command (`latexmk -pdf main.tex` when available) and treat the compiled PDF as authoritative for the
  page-budget and layout checks in the closing gates.
- **Exit 1 (no LaTeX engine):** you MUST tell the user now, in one line, that PDF compilation is
  unavailable in this environment, so the page-budget / overfull / float-layout gates will run
  static-only and the compiled PDF cannot be verified. Still produce the LaTeX source and the static
  audits; never silently skip compilation without telling the user.

## LaTeX Project Setup

Default layout:

```text
paper/
  main.tex
  math_commands.tex
  references.bib
  sections/
    abstract.tex
    introduction.tex
    ...
  figures/
```

Before creating LaTeX files:

1. If `paper/` already exists, back it up to `paper-backup-<timestamp>/`.
2. **Resolve the template from the confirmed venue** (follow the tiered Selection Rules in
   `_shared/templates/index.md`). Look up the confirmed venue (recorded in the Paper Framework "Inputs
   Used" / the Writing Policy):
   - **Bundled venue** → copy the **mapped** template into `paper/main.tex` **verbatim** (do not
     hand-write or reconstruct the document class / preamble from memory): EMNLP / ACL / NAACL →
     `acl2026.tex`, ICLR → `iclr2026.tex`, NeurIPS → `neurips2026.tex`, ICML → `icml2026.tex`, AAAI →
     `aaai2026.tex`, IJCAI → `ijcai26.tex`, CVPR → `cvpr2026.tex`, etc.
   - **Named but unbundled venue** → use a user-provided template if given, else **search the web and
     download the official template** from the venue's official source; record it as a template risk.
   - **Web fetch also failed** → use `generic_article.tex` as a stopgap **and report to the user
     explicitly** that the official template could not be obtained and must be replaced before
     submission.

   **Silently falling back to `generic_article.tex` while a venue was named is a template error, not an
   acceptable default** — the generic template is only the reported stopgap above or for the genuinely
   unspecified-venue case.
3. Copy **every** required companion file for that template listed in `_shared/templates/index.md`
   (`.sty`, `.cls`, `.bst`, and any bundled helper) into `paper/`. For the ACL/EMNLP/NAACL template
   that means `acl.sty` and `acl_natbib.bst`; a missing companion makes the project fail to compile.
4. Replace official sample or instruction body text with the confirmed Paper Framework section
   inputs. Preserve the document class, venue options, package/style setup, and bibliography commands.
5. If the confirmed Figure Plan contains any nontrivial table, add the portable table toolbox to
   the generated preamble unless it is already present or the venue explicitly forbids it.
   `booktabs` is **required** whenever any table exists — without it the draft falls back to ugly
   `\hline` rules:

   ```tex
   \usepackage{booktabs}      % \toprule \midrule \bottomrule \cmidrule — REQUIRED for any table
   \usepackage{array}
   \usepackage{tabularx}
   \usepackage{colortbl,xcolor} % subtle highlight of best/target numbers
   \newcolumntype{Y}{>{\raggedright\arraybackslash}X}
   \newcolumntype{Z}{>{\centering\arraybackslash}X}
   ```

   Keep this as a generated-project support block; do not rewrite official source template files
   themselves just to add helper packages.
6. Create `paper/sections/` files matching the confirmed section list.
7. Update `paper/main.tex` input calls to match the confirmed section files.
8. Materialize the confirmed Appendix / Supplement Plan before writing appendix content. If the plan
   lists appendix items, create `paper/appendix-plan.md` with the exact fields `Item ID`, `Type`,
   `Claim backed`, `Source availability`, `Fill status`, `Main-text anchor`, and `Fallback`, and create
   `paper/sections/A_appendix.tex` (or the venue-specific appendix file named by the plan). If the
   confirmed plan is `none`, delete the template appendix hook (`\appendix` and its appendix `\input`)
   and remove stale appendix files rather than shipping an empty appendix.
9. Assemble post-main material according to the Venue Assembly Plan. **Start the appendix on a fresh
   page**: place `\clearpage` immediately before `\appendix` (most venues, including ACL, do not do
   this automatically). Keep the venue's required order for Limitations / Ethics / References /
   Appendix, and do not let the appendix run on the same page as the references or main body.
10. Remove stale section files not referenced by the updated `paper/main.tex`.

Once the project skeleton exists, proceed to `stages/section-drafting.md` for the per-section
drafting loop, and invoke the **`academic-figure`** skill for figure and table handling (project
preamble packages such as `float` / `placeins` for appendix float discipline are added there as
needed).
