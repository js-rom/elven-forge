# Step 1 — Iteration Plan

## Inputs
- `Requirements Ranking`, `Use Case Model`, `Vision and Business Case`, `Supplementary Specification`.
- `Elaboration Iterations History` and `Elaboration Iterations Ledger`; run `get-calibration-baseline.ps1` against the ledger.
- Calibration sample: only `high` iterations and `full` or `slice` use cases. Exclude low, medium, open, refactor-only, support and retired records.
- Use the median effective days per UC as primary reference, the weighted average as secondary, and the min-max range as the uncertainty band. Report sample size and confidence.

## Output contract
- Master `Iteration Plan` for the iteration: scope, selected use cases or scenarios, tasks, estimates, risks and buffer.
- Every scope item has a stable `Scope ID` (`S1`, `S2`, ...). The Test Plan, the Acceptance Test Plan and the Iteration Verification use it as the traceability key.
- Deferred or out-of-scope items are listed with a `Scope ID` and a reason.
- `Historical Calibration` section with sample size, confidence and the three references; or `no historical baseline`.
- A task-based estimate outside 30% of the historical range must be justified, or the estimate adjusted before the gate.
- Refine `Requirements Ranking` if priorities changed.
- Open the iteration record in `Elaboration Iterations Ledger` with the calibration snapshot.

## Preconditions
- Phase is elaboration and there is no active iteration, or the previous cycle was closed.
- History and ledger loaded; active schema instruction and template for the iteration plan loaded.

## Rubric
- Scope selects the riskiest, most valuable and least covered items (the 10% rule).
- Every scope item traces to a use case or scenario and to a ranking row.
- Every scope item has a unique `Scope ID`; deferred items have a reason.
- Estimates follow the calibration contract, not intuition.

## Evidence required
- Calibration numbers, sample size and confidence.
- Scope list with exclusions and rationale.
- `OK 1` request.

## Anti-patterns
- Estimating from prose without opening the ledger.
- Averaging low-confidence, open or refactor-only iterations.
- Copying the previous iteration plan without re-ranking.
