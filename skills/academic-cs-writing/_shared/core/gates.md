# Gates And Protocols

Apply these to every workflow.

## Critical Decision Rule: STOP, NEVER GUESS

This is the highest-priority rule in this skill. It overrides all other instructions,
defaults, efficiency preferences, and autonomy settings. No exception.

**When the agent encounters a decision that materially affects the paper, it MUST stop
and ask the user. The agent MUST NOT guess, assume, default, infer silently, or proceed
past the decision.**

"Materially affects the paper" means the decision changes any of:

- **Paper identity**: what kind of paper this is, who it is for, what it claims.
- **Core claims**: what the paper asserts as true, and the evidence boundary around
  those assertions.
- **Key terminology**: terms that appear in the title, abstract, contribution
  statement, method name, dataset/task name, benchmark name, or metric definition.
- **Evidence conflicts**: two or more sources that disagree on counts, denominators,
  model names, method names, key terms, metrics, baselines, dataset splits, protocols,
  or central claims.
- **Venue / template**: target venue selection or template choice that changes page
  budget, section order, citation style, or required statements.
- **Section structure**: which sections exist, what order they appear in, and what
  each section's main content is.
- **Figure / table plan**: which figures appear in the main paper, what message each
  carries, and how each is generated.

**The agent MUST stop and ask when ALL of these are true:**

1. The answer affects one or more of the paper-material categories above.
2. No conservative default can preserve correctness — guessing wrong would produce
   a false claim, wrong paper identity, wrong terminology, or a large downstream rewrite.
3. The answer cannot be recovered from the provided workspace materials, Writing Policy,
   or user's explicit prior instructions.

**The agent MUST NOT stop for:**

- Routine prose choices that don't change claims or identity.
- Package installation, environment setup, or file path decisions.
- Decisions that have a clear conservative default that preserves correctness.
- Decisions the user has already explicitly answered.

**When stopping, the agent MUST:**

- State exactly which paper-material category is affected.
- State what it infers and from what basis.
- State why guessing wrong would cause harm.
- Propose a safe default if one exists, or state "cannot proceed without your answer".
- Wait for explicit user response before continuing.

**The agent MUST NOT:**

- Guess the answer and proceed.
- Pick a "reasonable default" when the default could be wrong.
- Say the step was "compressed", "batched", "assumed", or "implicitly confirmed".
- Treat silence, prior intent, or an initial "write the paper" request as confirmation.
- Proceed past the decision without explicit user response.

This rule applies at every stage of every workflow. It is never overridden by
efficiency concerns, token budget, or user requests for one-shot generation.

## Workflow Planning Protocol

Before executing any workflow, create a visible workflow-derived plan when the agent runtime provides
a plan/progress facility. If no such facility exists, show a compact plan in the conversation before
starting substantial work.

Plan rules:

- Derive the plan from the selected workflow, not from a generic writing checklist.
- Keep it short: 3-6 steps for Full Draft Workflow and 1-4 steps for Draft Revision Workflow.
- The plan must include mandatory confirmation gates as stop points.
- Do not include internal reference-loading details, file-search minutiae, package setup, smoke tests,
  or environment checks unless they directly block the writing artifact.
- Update the plan when a workflow stage starts, completes, or stops at a confirmation gate.
- For Full Draft Workflow, the initial plan should normally map to:
  `workspace evidence -> Writing Policy -> checkpoint -> Paper Framework -> checkpoint -> paper/`.
- If the user asks for a full paper in one request, plan the whole workflow but mark only the current
  pre-gate stage as active.

## Entry Routing

Every request must be routed into exactly one workflow before work begins:

- **Full Draft Workflow** for writing a complete paper from project/workspace materials.
- **Draft Revision Workflow** for rewriting, polishing, diagnosing, reviewing, or compressing
  existing paper text.

After routing, follow the selected workflow exactly. A user request for a final deliverable, a
complete paper, a polished rewrite, or a one-shot output authorizes starting the matching workflow;
it does not authorize skipping workflow steps, loading downstream references early, generating
downstream files early, or bypassing mandatory checkpoints.

## Mandatory Checkpoint Semantics

- If the selected workflow contains a confirmation gate: **STOP HERE and wait for user response.**
  Do not proceed until explicit user confirmation is received.
- Treat a checkpoint as completed only after the user replies with confirmation, correction, or a
  clear instruction for that checkpoint.
- Do not treat silence, prior intent, an initial "write the full paper" request, or the agent's own
  assumptions as confirmation.
- At every stop, return a concise substantive stage summary, evidence/results snapshot when relevant,
  output artifact, decisions needing confirmation, unresolved blockers, and the exact next user
  action. Do not show internal reference-loading details by default.
- `Unresolved blockers` are paper blockers only: missing/contradictory evidence, claim boundary,
  paper identity, metric definition, taxonomy, citation, section structure, template, or user
  decisions that block the next writing stage. Do not list local runtime, package, `.venv`, smoke
  test, or source-directory writeability issues unless they prevent writing the requested artifact or
  directly invalidate evidence.
- Do not continue past a mandatory gate by saying the step was "compressed", "batched",
  "assumed", "implicitly confirmed", or "handled internally".

At every confirmation gate, use this user-facing checkpoint shape. Always localize user-facing
checkpoint labels to the interaction language. Keep file paths, stage names, artifact names, and
machine-parsed markers in their original form.

```text
Checkpoint: <Writing Policy | Paper Framework | workflow-specific gate>
Stage result: <1 sentence about the substantive content completed, not file existence>
Output: <main artifact path or deliverable>
Summary: <compact table or short paragraph showing the substantive stage result>
Decisions to confirm:
- Required: <identity, framing, claim boundary, or structure decisions needed for the next stage>
- Optional: <venue, template, additional language artifact, wording preference, or other non-blocking defaults>
Unresolved blockers: <none or concise list>
Recommended next action: confirm / request changes / pause
User action required: Please confirm whether to proceed to <next stage>, or tell me what to change.
```

## Clarification Protocol

Use this protocol in every workflow. Clarification prevents wrong paper contracts, false claims,
wrong revision targets, and large downstream rewrites. It is not a front-loaded questionnaire.

Always infer from the supplied workspace, draft, or user text first. Ask only when all are true:

1. the answer affects the current workflow stage,
2. no conservative default can preserve correctness,
3. a wrong guess would cause a false claim, wrong paper identity, wrong terminology, wrong revision
   strategy, or large downstream rewrite,
4. the answer cannot be recovered from available materials.

If a question does not meet these criteria, proceed with a stated assumption, weaken the claim,
defer the decision, or record it as an unresolved note according to the selected workflow.

Before asking, build these fields internally:

- target: paper identity, core claim, evidence boundary, key term, evidence conflict, revision
  target, venue/template, or blocking framework decision,
- inference and basis,
- why the answer is decisive,
- safe default if unanswered.

Do not show the full internal fields by default. Use a concise user-facing question:

```text
Before <workflow stage>, I need one decision: <question>.
I infer <short answer> from <short basis>. Please confirm or correct.
Default if unanswered: <safe fallback or "cannot proceed">.
```

If 2-3 questions are needed, use a short numbered list with one-line inference and default for each.
Show the full reasoning fields only when the user asks why, or when a high-risk evidence conflict
requires transparency.
