# Rubric — Use Case Realization (step 10)

Use with `.opencode/agents/up-reviewer.md`. This step assembles and validates; it does not design.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Scenario mapping | 30 | UC step -> SSD -> Operation Contract -> 9A/9B reference, per scenario |
| Postcondition checklist | 25 | Every in-scope postcondition checked against the 9A matrix |
| SVG integrity | 20 | Every embedded image resolves to an existing file under `out/` |
| No new design | 15 | No class, responsibility, package or interaction absent from 9A/9B |
| Rationale and alignment | 10 | Supplementary Specification and Glossary alignment noted |

## Verdict

- `YES`: no blocking item and score >= 80.
- `CONDITIONAL`: 60-79 with no broken diagram reference.
- `NO`: a missing scenario, a broken SVG, or new design introduced.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "quoted text", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
