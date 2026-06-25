# Venue Profiles Index

Use venue profiles only after the Writing Policy has been confirmed and the workflow is building a
Paper Framework, drafting under a confirmed venue, or running a final submission-readiness check.
Do not load these files during Workspace Discovery or Writing Policy generation.

Venue profiles are dated constraint cards, not paper-story sources and not substitutes for the
current official call for papers. They may influence template choice, page-budget arithmetic,
anonymity, citation command style, required statements, figure/table planning, claim-strength
calibration, and final checklist risks. They must not invent claims, results, citations, or paper
identity.

**Template note:** the official LaTeX template for each modeled venue is **preloaded in
`templates/`** and is the authoritative source for formatting (see `templates/index.md`). The
`Official sources:` URLs in each venue card — and the URL table in
`maintenance/venue-template-sources.md` — are **provenance records and pre-submission verification
links, not draft-time fetch instructions**. When a venue maps to a bundled template, use the local
file directly; do not web-search or download a template to start the LaTeX project. A venue card's
`Final Gate` instruction to "confirm the current official style file" is a *pre-submission* check
against the official page, not a license to re-download during drafting.

The schema is strict; the facts are allowed to be incomplete. Prefer `not verified` or `verify
current official page` over filling a field from memory, old calls, search snippets, or another
venue's pattern. If a target venue is unavailable, choose the closest profile only for approximate
planning and mark the fit as approximate in the Paper Framework. If a venue fact affects compilation,
page counting, post-main section order, anonymity, or submission readiness and the profile does not
record a current verified value, record it as an Open Decision and verify against the official venue
page or a user-provided guideline before calling the draft submission-ready.

## Venue Kind: Conference vs Journal

Every venue card declares a `Venue Kind` of either `conference` or `journal`. The kind controls two
things:

- It changes which length/format/process fields matter (page limits and anonymity for conferences;
  manuscript-type length, blinding, revision cycle, and supplementary handling for journals).
- It selects the paper-type family. When `Venue Kind` is `journal`, choose the paper type from the
  journal set under `_shared/paper-types/journal/` (manifest `paper_type` values prefixed
  `journal-`). When it is `conference`, use the conference paper-type files at the top level of
  `_shared/paper-types/`.

For journals, also load `_shared/venues/journal-vs-conference.md` for the drafting-posture
differences (complete story, more thorough evaluation, written to survive multi-round review,
non-anonymous self-citation, supplementary material). Do not apply a conference page budget to a
journal draft.

## Required Profile Schema

Every venue profile should use these sections. Conference cards keep journal-only fields as `n/a`
and journal cards keep conference-only fields as `n/a`. If a value is unknown, keep the field and
write `not verified`.

```text
## Venue Kind
- conference | journal

## Source Status
- Official sources:
- Access date:
- Verified for:
- Drift risk:

## Scope
- Applies to:
- Submission version:

## Length And Counting
- Layout (single/double column):        # journals
- Main text limit:
- References count:
- Appendix count:
- Abstract limit:                        # journals (word/char cap, structured?)
- Checklist count:                       # conferences
- Ethics/limitations count:              # conferences
- Supplementary material count:

## Blinding                              # journals (conferences use Anonymity checks below)
- single-blind | double-blind | open:

## Revision Model                        # journals
- Review/revision cycle:
- Response-to-reviewers / rebuttal:
- Camera-ready:

## Supplementary And Extension           # journals
- Supplementary handling:
- Conference-to-journal extension:

## Post-Main Order
- Required order:
- Optional sections:
- Not verified:

## Drafting Implications
- Main paper self-contained:
- Appendix/supplement use:
- Anonymity checks:                      # conferences

## Final Gate
- Before submission-ready:

## Do Not Infer
- 
```

## Supported Venue Fact Cards

### Conferences

| Venue family | Profile file | Use for |
|---|---|---|
| ICLR | `iclr.md` | ML representation learning, deep learning, general ML method papers |
| NeurIPS | `neurips.md` | broad ML, theory-to-systems ML, empirical ML |
| ICML | `icml.md` | ML methods, theory, empirical learning systems |
| ACL | `acl.md` | NLP and computational linguistics |
| EMNLP | `emnlp.md` | empirical NLP |
| NAACL | `naacl.md` | NLP and computational linguistics |
| CVPR | `cvpr.md` | computer vision and vision-language |
| ICCV/ECCV | `iccv-eccv.md` | computer vision and vision-language |
| AAAI/IJCAI | `aaai-ijcai.md` | broad AI |
| KDD/WWW/SIGIR | `kdd-www-sigir.md` | data mining, web, search, recommender, IR |
| CHI/UIST | `chi-uist.md` | HCI, interaction, user studies, systems for people |

### Journals

| Venue family | Profile file | Use for |
|---|---|---|
| JMLR | `jmlr.md` | machine learning journal articles (theory, method, application) and OSS/MLOSS tool papers; single column, no hard page limit |
| IEEE TPAMI | `ieee-tpami.md` | pattern analysis, machine intelligence, computer vision; double column, Regular/Survey/Short types |
| Nature | `nature.md` | Nature or close Nature-family broad-interest research articles; verify current caps and reporting rules before submission |
| Nature Communications | `nature-communications.md` | Nature Communications Articles / Brief Communications; Methods-in-cap and display-item planning are early blockers |
| Generic journal | `journal-generic.md` | any journal not individually modeled (TMLR, IEEE TNNLS/TIP/TMM, ACM TODS/TOIS, Elsevier/Springer/Wiley); confirm all fields against the target journal |
