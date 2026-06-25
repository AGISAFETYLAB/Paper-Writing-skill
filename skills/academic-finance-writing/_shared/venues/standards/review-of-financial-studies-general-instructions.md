# Review of Financial Studies General Instructions

Official source: https://academic.oup.com/rfs/pages/General_Instructions

Source snapshot checked: 2026-06-22. Re-check before real submission.

## Applicability

Use when the target is Review of Financial Studies or an SFS/RFS-style finance journal submission.

## Page Window

```yaml
target_page_window:
  min_pages: 40
  max_pages: 55
  source_type: field_convention_fallback
  source_url: https://sfs.org/guidelines-for-submissions/
  count_scope: anonymous main manuscript PDF; Internet Appendix included in the PDF but recorded separately for the page-window decision
```

Use the page-window pass/fail statuses defined in `_shared/submission/submission-standards.md`.
Record `below min_pages` and `above max_pages` as blocking page-window states before any completion claim.
Current SFS guidance fixes abstract, line-spacing, and font rules; because no
local hard page cap is recorded here, use the field convention fallback unless the live portal says
otherwise.

## Required Shape

- manuscript prepared against the current RFS/SFS instructions
- abstract, JEL codes, references, appendices, and data/code materials checked against the current
  official instructions
- current SFS submission portal and review/refund policies checked before submission-ready wording

## Template Role

No package-local RFS template is bundled. Use target instructions as the authority and start from the
finance journal shell only when no official template is required.

## Blocking Checks

- Verify the current RFS/SFS author instructions and portal requirements.
- Do not infer RFS limits from JF, JFE, or OUP economics journals.
- Record whether the manuscript is initial submission, revision, or accepted-paper source work.
