# Rubric — Mutation Quality (steps 14B/14D)

Use with `.opencode/agents/up-reviewer.md` when the Iteration Plan enables
`Test Quality`. The reviewer judges the **triage**, not the score: a low score
with a complete triage is conditional; a high score with survivors hidden
behind an allowlist is a failure.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Reproducibility | 15 | The command, the target classes and the report path are recorded and reproduce the score |
| Survivor triage | 25 | Every survivor has exactly one class; no `UNCLASSIFIED` remains |
| Protected invariants | 20 | Zero survivors on invariants declared in the Iteration Plan |
| Measures with effect | 20 | Every measure has an owner and evidence that the mutant died or was allowlisted |
| Allowlist justification | 10 | Each entry states why it is equivalent and references a test or a contract |
| Trend | 10 | The delta against the baseline is explained, or the baseline is declared as the first |

## Verdict

- `YES`: zero `UNCLASSIFIED`, zero protected-invariant survivors, every measure
  has an owner and effect evidence, and the score meets the policy.
- `CONDITIONAL`: complete triage, but the score is below target or debt is
  recorded with a Scope ID or a mutation debt ID. Allowed only under `advisory`.
- `NO`: an `UNCLASSIFIED` survivor, a protected-invariant survivor, missing
  reproducibility, a silent re-baseline, or an allowlist entry without evidence.

## Routing

- `WEAK_ASSERTION` / `MISSING_BEHAVIOR_TEST` -> 14B test-author, recorded re-open.
- `DEAD_CODE` -> 14B implementer.
- `DESIGN_GAP` -> 04 Operation Contracts, 10 Use Case Realization or 11 review.
- `EQUIVALENT` / `ENVIRONMENT` -> allowlist or exclusion, orchestrator.
- Out-of-scope debt -> Iteration Plan with a Scope ID; never an invisible TODO.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [
    { "criterion": "string", "evidence": "survivor or command output", "fix": "string" }
  ],
  "confidence": "high | medium | low"
}
```
