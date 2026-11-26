# Step 17 — Cycle Close

## Inputs
- `state.yaml` for the domain.
- Approved and persisted artifacts of the iteration.
- `Iteration Plan` for the scope contract.

## Output contract
- Confirm that every approved artifact is persisted directly under `openspec/artifacts/{domain}/...`.
- List the files updated in this cycle.
- Do NOT create, move or archive `openspec/iterations/` folders.
- Do NOT run delta-merge operations.
- Do NOT create new artifacts and do NOT set `status: completed`: the Elaboration phase is not closed.
- Treat this as an automatic step, not a user-driven action, but still request `OK 17`.

## Preconditions
- `OK 16` approved.
- No pending persistence for artifacts approved in this cycle.

## Rubric
- The reported file list matches the artifacts touched in the cycle.
- The domain state still has `status: in_progress` and the phase remains elaboration.
- No iteration folder was created.

## Evidence required
- File list grouped by discipline.
- State snapshot: phase, iteration, `status: in_progress`.
- `OK 17` request.

## Anti-patterns
- Archiving or merging deltas in master-only mode.
- Treating cycle close as phase close.
- Starting the next cycle before step 18.
