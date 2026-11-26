# Step 19 — Phase Close

## Inputs
- `state.yaml` with `status: in_progress`.
- Requirements coverage report and `Elaboration Iterations History`.
- Explicit user decision to end the Elaboration phase.

## Output contract
- Close the phase only when requirements coverage target is achieved and the user explicitly approves.
- Set `status: completed` and update `date`.
- If coverage is below target, do NOT close: loop to step 1 for a new iteration.
- Closing one cycle never closes the phase; closing the phase never starts construction implicitly.

## Preconditions
- `OK 18` approved.
- Coverage target met.

## Rubric
- The coverage report is the one generated from the ranking and the iteration evidence.
- The approval to end the phase is explicit, not inferred from a cycle close.
- The state reflects the closure.

## Evidence required
- Coverage numbers.
- Explicit approval statement.
- State update (`status: completed`).

## Anti-patterns
- Closing the phase with pending requirements.
- Starting construction without an explicit phase decision.
- Treating 100% coverage as automatic approval.
