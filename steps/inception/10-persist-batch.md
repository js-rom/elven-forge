# Step 10 — Persist Batch (automatic)

## Inputs
- All artifacts approved in steps 1-9.
- Domain config values refined during steps 1-9.
- Storage skill and the active schema.

## Output contract
- Invoke the storage skill once, with the full batch of approved artifacts.
- Pass each artifact by `artifact_id` plus the placeholders its path requires; storage resolves the paths.
- Persist the approved domain config values in the same batch.
- After storage succeeds, set every persisted artifact to `status: persisted` in `state.yaml`.
- Write one journal record with the batch result. No approval token.

## Preconditions
- `OK 9` approved.
- `state.yaml` has the approved artifacts marked `approved`.

## Rubric
- Only approved artifacts are persisted.
- No hardcoded paths reach storage.
- Artifacts not in the batch keep their previous status.

## Evidence required
- Storage result and list of files written.
- Artifacts left out and why.
- Journal record.

## Anti-patterns
- Persisting unapproved content.
- Writing per artifact outside the batch.
- Handing storage a hardcoded path.
