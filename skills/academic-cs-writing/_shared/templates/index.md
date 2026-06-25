# Venue Template Index

Use this file only when a workflow needs to initialize a LaTeX paper project or record the selected
venue template in the Paper Framework. Do not load template `.tex`, `.cls`, or `.bst` files as
writing references unless editing the LaTeX project itself.

## Template Mapping

| Venue target | Primary template | Required companion files | Citation style | Notes |
|---|---|---|---|---|
| Generic / venue TBD | `generic_article.tex` | `math_commands.tex` | natbib numeric | Non-submission single-column draft template used only when the target venue is not selected. Soft drafting budget: 6-8 main-text pages, excluding references and appendix. Replace with the official target-venue template before submission. Its default section inputs are placeholders; replace them with the confirmed Paper Framework section list. Includes the portable `array` / `tabularx` table toolbox for bounded tables. |
| ICLR | `iclr2026.tex` | `iclr2026_conference.sty`, `iclr2026_conference.bst`, `math_commands.tex` | natbib-style author-year | ICLR 2026 official template and style companions are preloaded. |
| NeurIPS | `neurips2026.tex` | `neurips_2026.sty`, `checklist.tex` | natbib-style author-year | NeurIPS 2026 official template, style file, and checklist are preloaded. Keep `neurips2025.tex` only for reproducing older drafts. |
| ICML | `icml2026.tex` | `icml2026.sty`, `icml2026.bst`, `algorithm.sty`, `algorithmic.sty` | natbib-style author-year | ICML 2026 official example, style file, and bundled algorithm helpers are preloaded. Keep `icml2025.tex` only for reproducing older drafts. |
| ACL / EMNLP / NAACL | `acl2026.tex` | `acl.sty`, `acl_natbib.bst` | ACL natbib author-year | Shared *ACL official style files. Use the exact year/venue variant if the target venue provides one. |
| CVPR | `cvpr2026.tex` | `preamble.tex`, `cvpr.sty`, `ieeenat_fullname.bst` | numeric `\cite{}` | CVPR 2026 official author-kit files are preloaded. The raw official template has fixed sample inputs; replace them with the confirmed Paper Framework section list. |
| AAAI | `aaai2026.tex` | `aaai2026.sty`, `aaai2026.bst`, `aaai2026.bib` | natbib numeric | AAAI 2026 anonymous-submission LaTeX files are preloaded. |
| IJCAI / IJCAI-ECAI | `ijcai26.tex` | `ijcai26.sty`, `named.bst`, `ijcai26.bib` | named author-year | IJCAI-ECAI 2026 formatting-guideline LaTeX files are preloaded. Do not substitute AAAI formatting for IJCAI. |
| ACM / KDD / WWW / SIGIR / CHI / UIST | `acm_mm2026.tex` | `acmart.cls`, `acm.bst` | ACM author-year or numeric depending on venue instructions | Generic ACM `sigconf` starter. Update conference metadata and review/camera-ready options from the target venue guidance before submission. |
| IEEE conference | `ieee_conference.tex` | `IEEEtran.cls`, `IEEEtran.bst` | numeric `\cite{}` | References usually count toward the page limit. |
| IEEE journal / TPAMI | `ieee_journal.tex` | `IEEEtran.cls`, `IEEEtran.bst` | numeric `\cite{}` | Journal (`\documentclass[journal]{IEEEtran}`), double column, not anonymous. TPAMI: Regular 12-18 pages (MOPC), Survey 20, Short 8, references and biographies included; Abstract one paragraph 150-250 words; Index Terms required; supplemental material is separate files. Journal-specific limits vary — verify the target journal author guide. |
| JMLR | `jmlr2024.tex` | `jmlr2e.sty`, `math_commands.tex` | natbib author-year (in `jmlr2e`) | Single column, no hard page limit, not anonymous. `jmlr2e.sty` is the official JMLR style (fetched verbatim, CC-BY) — do not modify it. `jmlr2024.tex` is a local wrapper; fill author/editor/`\jmlrheading` blocks and replace placeholder section inputs. Appendices go at the very end of the same PDF, after acknowledgments, before references. Also used for the JMLR OSS/MLOSS short track. |

## Common File

- `math_commands.tex`: common math macro starter copied into the output `paper/` project.

## Selection Rules

**When the user named a target venue (conference or journal), an official template is mandatory — never
draft a named-venue paper on the generic template silently.** Acquire it in this strict priority order
and stop at the first that applies:

1. **Preloaded `templates/` first.** Look the named venue up in the Template Mapping above. If it maps
   to a bundled template, copy that local file and **all** its required companions. This is the first
   and authoritative source — when a venue maps to a bundled template, **do not web-search or
   download**; the file is already here.
2. **User-provided official template.** If the user supplied template files for this project, use
   those (they take precedence over a web fetch).
3. **Targeted web fetch for a named-but-unbundled venue.** If the named venue has **no** preloaded
   mapping and the user provided no template, **search the web for and download the official template**
   from the venue's official source (CFP / author kit / official style files). Record the source URL
   as provenance and note it as a template risk to re-verify before submission.
4. **Generic fallback — only as a reported stopgap.** If web acquisition also fails (no network, or no
   official template can be found), use `generic_article.tex` as a non-submission single-column draft
   shell **and report this to the user explicitly**: state that the official template for the named
   venue could not be obtained locally or online, that the generic template is a temporary stopgap, and
   that it must be replaced with the official template before submission. Record the soft 6-8
   main-text-page drafting budget (excluding references and appendix) and the unresolved-template risk.

When the user did **not** name a venue, use `generic_article.tex` directly as the unspecified-venue
draft template (record venue as TBD; no web fetch and no special report needed). Its default section
inputs are placeholders; replace them with the confirmed Paper Framework section list before drafting.

Further rules:

5. Never invent or reconstruct venue formatting from memory.
6. Official venue templates are format shells, not prose sources. After copying a template, remove
   official sample or instruction body text and keep only the format setup, required commands,
   bibliography hooks, and verified post-main hooks.
7. When the selected template has fixed default section includes, update `main.tex` to match the
   confirmed Paper Framework section list.
8. When the generated draft contains nontrivial tables and the selected official template does not
   already load `array` / `tabularx`, add the portable table toolbox to the generated `paper/main.tex`
   preamble. Treat this as generated-project support, not as an edit to the canonical official
   template stored in this skill.
9. For journal targets (Venue Kind: journal), select the journal template (TPAMI → `ieee_journal.tex`;
   JMLR → `jmlr2024.tex`; any other journal → a user-provided official template or the closest
   journal shell, recorded as unresolved). Journal templates are typically not anonymous and do not
   share conference page-limit assumptions; calibrate length, columns, abstract format, and required
   statements from the target journal author guide and the matching venue card. Do not modify the
   official `jmlr2e.sty`.
