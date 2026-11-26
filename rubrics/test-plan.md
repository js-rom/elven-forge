# Rubric — Test Plan (step 14B)

Use with `.opencode/agents/up-reviewer.md`. The Test Plan is the TDD contract for the iteration slice.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Scope traceability | 25 | Every iteration item has a test item; no out-of-scope item |
| Technique coverage | 25 | Factors, equivalence classes, boundaries and reduction documented |
| Contract traceability | 25 | Item -> UC/scenario -> UCR -> SSD -> postcondition |
| Conformance section | 15 | 14D matrix present and consistent with the last run |
| Execution evidence | 10 | RED/GREEN commands and counts per cycle |

## Verdict

- `YES`: no blocking item and score >= 80.
- `CONDITIONAL`: 60-79 with no missing traceability.
- `NO`: an item without traceability, or no execution evidence.

## Blocking examples

- A test item that does not map to a scenario or postcondition.
- An out-of-scope item implemented without routing back to step 1.
- A UI fidelity item without state id, transition id or mock path.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "quoted item or command", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
