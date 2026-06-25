# Medicine Word Template Index

Use this directory for Word-first manuscript routes. The DOCX files here are reference packages for
Word styles, settings, themes, numbering, and editable-table behavior; they are not prose sources.

| Target | Template | Status | Use |
|---|---|---|---|
| BMJ Case Reports clinical case report | `bmj-case-reports/bmj-clinical-case-report-template.docx` | official Word template downloaded from BMJ Case Reports | CARE/case-report route when the confirmed target is BMJ Case Reports clinical case report |
| BMJ Case Reports global health case report | `bmj-case-reports/bmj-global-health-case-report-template.docx` | official Word template downloaded from BMJ Case Reports | GATHER/global-health case-report route when the confirmed target is BMJ Case Reports global health case report |
| BMJ Case Reports Images In | `bmj-case-reports/bmj-images-in-template.docx` | official Word template downloaded from BMJ Case Reports | Images In route when the confirmed target is BMJ Case Reports |
| generic medical Word-first manuscript | `generic-medical-word-reference.docx` | package-local generic Word reference shell, not an official Word template | Fallback for JAMA/JAMA-style, BMC/Springer, BMJ, or unspecified Word-first manuscripts when no valid official/user-provided Word template is available |

Selection priority for Word-first routes:

1. preloaded official Word template -> user-provided official template -> official web fetch -> package-local generic Word reference shell.
2. If official web fetch fails, record `download-blocked`, `not-found`, or the exact failure in
   `paper/submission-package.md`; do not call the package-local shell official.
3. JAMA/JAMA-style routes must not claim an official Word template. Use JAMA/JAMA Network official
   author instructions plus `generic-medical-word-reference.docx` as a generated DOCX reference shell
   unless the user supplies an official/current Word template.
4. Template sample body text, local source paths, and generator provenance must never enter the
   manuscript body. Keep provenance in `submission-package.md` or `review-report.md`.

Use `skills/academic-writing/scripts/fetch_medical_word_templates.py` to attempt official-template downloads into a staging
directory and validate downloaded DOCX packages before promoting them into this directory.
