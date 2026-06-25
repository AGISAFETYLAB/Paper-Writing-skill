# Finance Referee Response And Revision Workflow

Use this reference when responding to editors, referees, seminar feedback, R&R reports, or a prior
internal review.

## Point-by-point response

Create a response package with:

- `response-letter.md`: editor-facing or referee-facing response letter
- `revision-backlog.md`: all requested changes, status, evidence needed, and owner
- `paper/revision-map.md`: mapping from comment to manuscript location and changed table/figure

Each response must quote or paraphrase the comment, then answer directly.

## Comment-to-revision map

Maintain a comment-to-revision map before drafting final responses.

For every distinct concern:

| Field | Required content |
|---|---|
| Comment ID | referee/editor and number |
| Concern | concise statement of the issue |
| Category | contribution, identification, robustness, data, citation, exposition, formatting |
| Manuscript change | section/page/table/figure changed |
| Evidence status | completed, planned, needs user evidence, impossible, declined with reason |
| Response text | respectful explanation |

Do not merge multiple referee comments into one vague answer.

## Response tone

Use a calm, professional tone:

- thank the editor and referees briefly
- acknowledge valid concerns without over-apologizing
- state what changed and where
- when disagreeing, provide evidence or logic
- avoid emotional or defensive wording

## Do not be defensive

Never write "the referee is wrong" or "we already addressed this". Use:

- "We agree that the earlier draft did not make this point sufficiently clear."
- "We now clarify the identification assumption in Section 3."
- "We added Table IA.2 to show the result is not driven by the benchmark choice."
- "We respectfully retain the original specification because..., and we now explain this choice..."

## Evidence boundary

Do not claim completed analyses, robustness checks, code releases, data permissions, or new tables
unless the files or user-provided evidence exist. If a change is only planned, put it in
`revision-backlog.md` and mark it `needs_user_evidence`.
