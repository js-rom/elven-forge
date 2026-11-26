# Rubric — Vision (inception step 9)

Use with `.opencode/agents/up-reviewer.md`. Blocking at the inception phase gate.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Problem and business case | 25 | Problem statement, opportunity, expected value |
| Stakeholders and goals | 25 | Each stakeholder group with a goal and an interest |
| Scope | 20 | Explicit in-scope and out-of-scope boundaries |
| Success criteria | 15 | Business-level, measurable or clearly markable as TBD |
| Consistency | 15 | Aligned with the Use Case Model and Requirements Ranking |

## Verdict

- `YES`: no blocking item and score >= 80.
- `CONDITIONAL`: 60-79 with no scope contradiction.
- `NO`: no business case, contradictory scope, or new scope not reflected in the ranking.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "quoted text", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
