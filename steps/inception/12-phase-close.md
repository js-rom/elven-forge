# Step 12 — Phase Close (automatic)

## Inputs
- `state.yaml` for the domain.
- The storage batch result from step 10 and the environment step 11.
- Handoff contract `.agents/contracts/handoff-inception-elaboration.md`.

## Output contract
- Verify that every artifact approved in steps 1-9 is `persisted`.
- Set `status: completed` and update `date`.
- Confirm to the user that artifacts are persisted under `openspec/artifacts/{domain}/...`.
- Do NOT create, move or archive `openspec/iterations/` folders and do NOT run delta merges.
- Do NOT create new artifacts.
- Point the user to the handoff contract; elaboration starts from it, not from a blank phase.

## Preconditions
- Step 11 completed.
- All approved artifacts are `persisted`; no pending persistence.

## Rubric
- The state is consistent: `phase: inception`, `status: completed`, all approved artifacts `persisted`.
- No artifact is left `approved` but unpersisted.
- The handoff is explicit.

## Evidence required
- State snapshot.
- File list.
- Handoff reference.
- Journal record.

## Anti-patterns
- Closing with pending artifacts.
- Archiving or merging in master-only mode.
- Starting elaboration implicitly without the handoff.
