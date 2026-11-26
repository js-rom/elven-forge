# Step 18 — Elaboration History + Flow Audit

## Inputs
- Closed `Iteration Plan`, `Requirements Ranking`, `Use Case Model`, `state.yaml`.
- Existing `Elaboration Iterations Ledger`, `Elaboration Iterations History`, `Flow Audit Ledger`, `Flow Audit Report`.
- Git repository metadata.
- Skills `elaboration-history`, `flow-audit`; schema instructions and templates.

## Output contract
- Verify `OK 17`; if missing, stop and return to 17.
- Capture `end_ref` from current `HEAD`; never use `git log --all` for the calculation.
- Classify every iteration item as `full`, `slice`, `refactor`, `support` or `retired`; mark `counts_for_average` explicitly.
- Compute effective days from unique author dates inside `start_ref..end_ref`.
- Record commit hashes, commit days, ancestry, working-tree cleanliness, reliability and exclusion reasons in the ledger.
- Render the Markdown history from the ledger; do not edit generated tables by hand.
- Persist ledger and history, then run the flow audit automatically: update sources, `build-flow-audit.ps1`, `render-flow-audit.ps1`, `validate-flow-audit.ps1`, persist ledger and report.
- The flow audit is non-blocking and does not request a separate approval.

## Preconditions
- `OK 17` approved.
- Ledger, history and audit artifacts loaded before computing.

## Rubric
- Dates and counts are reproducible from git evidence.
- Low-confidence, open, refactor-only or mixed-scope iterations are excluded from the average.
- The audit reports top steps, rework signals and recommended experiments.

## Evidence required
- Ledger record with refs, hashes and day count.
- Rendered history report.
- Flow audit output.
- `OK 18` request before persisting history.

## Anti-patterns
- Reconstructing dates from prose when git evidence exists.
- Counting uncommitted work as an effective day.
- Skipping the flow audit or treating it as a new gate.
