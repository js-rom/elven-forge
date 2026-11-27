# Rubric — Acceptance Execution (step 14C)

Use with `.opencode/agents/up-reviewer.md`. The reconciliation table is the gate: every agreed scenario must appear as executed and green.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Reconciliation completeness | 40 | Every `A-xx` from 14A appears in the Scenario Reconciliation table |
| No skipped or failed scenarios | 25 | `Executed = yes` and `Result = GREEN` for every row |
| Evidence per scenario | 20 | Command, report or run reference per row, not a global claim |
| Traceability | 15 | Each scenario keeps its `Scope ID` and UC step/extension |

## Verdict

- `YES`: all scenarios present, all `yes`/`GREEN`, evidence non-empty, full unit suite green.
- `NO`: a missing scenario, a `no`/`skip`, a `RED`, or missing evidence.

## Routing

- RED scenario -> 14B TDD defect loop, then re-run 14C.
- Scenario mismatch with the Interaction Spec or design -> route to 5, 9A, 9B, 10 or 11.
- Missing feature file -> 14A, not a silent pass.

## Output

```json
{
  "verdict": "YES | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "row or command output", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
