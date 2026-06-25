# Writing Contract

A research paper is a structured argument, not a collection of results. Before any drafting or
framework work, establish the contract below. It defines what the paper claims, what supports
those claims, and what must stay bounded.

## Decision Ownership

gates.md owns the full STOP / clarification protocol, including when to ask, how to ask, and when
to wait for explicit user confirmation. This file owns only the seven paper-contract fields below:
what must be established before drafting, what each field contains, and which status vocabulary to
use when evidence is missing or conflicting. If a contract field is uncertain or conflicted, apply
the gate in `_shared/core/gates.md` instead of guessing.

## The Seven-Point Contract

Before writing any paper artifact, establish:

1. **Paper identity**: venue kind (`conference` or `journal`), target venue, paper type, intended
   reader, and core research question. Venue kind is decided before paper type; if the user has not
   explicitly specified a journal target, use `conference`. The paper type controls the evidence
   burden; method-paper and journal-method are not defaults.

2. **Core story**: problem → failure case or motivating gap → technical challenge → insight →
   proposed method/benchmark/system/study → one-sentence contribution → final takeaway.
   This chain must be complete before any section is drafted.

   Classify the contribution into one of these types early:
   - **Insight**: the paper reveals something previously unknown about how or why things work.
   - **Performance**: the paper achieves a new state of the art on established benchmarks.
   - **Capability**: the paper enables something that was previously impossible.
   The classification shapes how evidence is presented and what reviewers will look for.

3. **Contribution as the spine**: every section — Introduction, Related Work, Method, Experiments —
   must explicitly connect back to the core contribution. Remove background, method descriptions,
   or experiments that do not serve the contribution. A reader should be able to trace the
   contribution through every section without losing the thread.

4. **Claims and evidence boundary**: every major claim maps to available evidence, a source trace,
   and a drafting action (state / weaken / verify / defer / avoid). Unsupported claims are
   weakened or removed. The boundary between what the paper asserts and what it leaves open
   must be explicit.

5. **Key terminology**: terms that affect the title, abstract, contribution, method identity,
   dataset/task, benchmark, metric, or system components. Each term has a definition, a source,
   a use policy, and a status. Terminology must stay stable across the paper.

6. **Venue and format contract**: venue kind, target template, page/length budget, what counts
   toward the limit, required statements, post-main section order, and citation style. **Templates
   are local-first:** the official template for each major venue is preloaded in `templates/`; when
   the target venue maps to a bundled template (`templates/index.md`), use that local file — do not
   web-search, download, or reconstruct venue formatting from memory. If the venue
   is unconfirmed and venue kind is conference, use generic_article.tex with a soft 6-8
   main-text-page drafting budget and record that the official template is unresolved. If venue kind
   is journal but the target journal is not modeled, use `journal-generic` and keep journal-specific
   fields unresolved until the target journal guidelines are verified.

7. **Disclosure and naming boundary**: which entities may appear in the paper, under what name.
   This is distinct from the claims-and-evidence boundary (point 4): point 4 governs *what the paper
   may assert*, this point governs *what may appear at all*. The workspace artifacts the writing job
   reads (`NARRATIVE_REPORT.md`, `EXPERIMENT_LOG.md`, `findings.md`, `results/*.json`, run trackers)
   routinely carry internal scaffolding — checkpoint names, training-run / sweep identifiers, wandb
   run names, internal tool names, unreleased model names, and competing methods the authors do not
   intend to compare against — and none of these belong in the manuscript verbatim. Establish two
   registries before drafting:
   - **Naming Map**: internal identifier → the single public display name used in the paper. The
     internal identifier (e.g. a `..._step380` checkpoint tag) MUST NOT appear anywhere in prose,
     captions, tables, or figures; only the display name (e.g. the released model name) is written.
   - **Do-Not-Disclose list**: entities that must not appear at all — neither asserted, nor named in
     passing, nor referenced by negation or exclusion (do not write "the protocol that excludes X").
     Typical members: a baseline / competing method the authors deliberately withhold, an internal
     tool, an unreleased dataset, a partner or product name, or any not-for-publication result.

   **Integrity guard (overrides the disclosure default):** withholding a competing method is
   legitimate only when it is internal scaffolding, not when it hides a stronger comparison. If
   removing a Do-Not-Disclose entity would make a comparison claim misleading — e.g. a "state of the
   art" / "best" / "outperforms all" claim becomes true only because a stronger method was hidden —
   this is an `idea-level risk`: **stop and ask the user**; do not silently produce the flattering
   claim. Disclosure control suppresses names; it never manufactures a false comparison result.

## Evidence Classification

Classify important sources as:

- `raw evidence`: source data, experiment logs, annotation files
- `derived statistics`: computed metrics, aggregated results
- `draft-derived candidate`: numbers or claims inferred from drafts, not source data

## Status Vocabulary

For claims and evidence: `unknown`, `supported`, `partially supported`, `needs evidence`,
`not verified`, `should avoid`.

For disclosure status of an entity (model, method, baseline, dataset, tool, identifier):
`public` (may appear as written), `display-as:<name>` (must be renamed to the public display name;
the internal identifier is forbidden), `restricted` (only a bounded, agreed description may appear),
`do-not-disclose` (must not appear at all, including by negation or exclusion).

## Source Conflict Rule

If sources conflict on counts, denominators, model names, method names, key terms, metrics,
baselines, dataset splits, protocols, venue hints, or central claims, do not smooth the
conflict over.

- If the conflict is decisive, ask the user before finalizing the Writing Policy.
- If the conflict is not decisive, record it in Open Decisions with a conservative default.
- If the user does not answer a decisive evidence conflict, avoid exact numbers or strong claims
  and mark affected claims as `partially supported`, `needs evidence`, or `not verified`.
