# Rubric — Use Case Model (inception steps 3-6)

Use with `.opencode/agents/up-reviewer.md`. Advisory at step 6; blocking only if the user promotes it.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Actor-goal coverage | 30 | Every actor in the Vision has at least one goal |
| Naming | 20 | Goal-oriented names, stable across steps 3-5 |
| Diagram and list consistency | 20 | Every diagram use case appears in the list and vice versa |
| Ranking justification | 20 | 10% selection justified by risk, coverage and criticality |
| Brief completeness | 10 | Every in-scope use case has a brief |

## Verdict

- `YES`: no blocking item and score >= 80.
- `CONDITIONAL`: 60-79 with no missing actor goal.
- `NO`: an actor without goals, a use case renamed between steps, or a selection without ranking.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "quoted text", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
