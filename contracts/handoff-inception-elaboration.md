# Handoff — Inception to Elaboration

Inception ends with `status: completed` and a persisted artifact set. Elaboration inherits it; it does not recreate it.

## What elaboration inherits

- `Vision and Business Case` (living document).
- `Use Case Model`, `Use Case brief`, `Use Case fully dressed`.
- `Requirements Ranking`.
- `Supplementary Specification` and `Technical Memo`.
- Glossary terms added during inception.
- Domain config (schema, rules, tdd) and state (artifact statuses).

## What elaboration must do at start

1. Read the router, the domain state and the journal tail.
2. Read the inherited artifacts from the paths in `state.yaml`; do not copy their content.
3. Switch state to `phase: elaboration`, `iteration: E1`, `status: in_progress`, and the E1 pending steps. Keep artifact ids, statuses and `created_at_step`.
4. Create the E1 `Iteration Plan` (step 1). Do not repeat vision or use case discovery.
5. Refine inherited artifacts only when the iteration requires it, in master-only mode.

## Invariants

- Never create a second domain for the same project.
- Never rename or renumber use cases.
- Never reset artifact statuses to `not_started`.
- New artifacts go to master paths, never to iteration folders.
- History goes to `journal/E1/` (and later iterations), not to `state.yaml`.

## Evidence

- List of inherited artifacts with their status.
- New state snapshot (`phase: elaboration`, `iteration: E1`).
- Journal record for the transition.
