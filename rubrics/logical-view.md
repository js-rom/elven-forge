# Rubric — Logical View (step 11)

Use with `.opencode/agents/up-reviewer.md`. Every blocking item must quote the artifact.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Postcondition coverage | 30 | One row per Operation Contract postcondition, with the satisfying class/message |
| Responsibility assignment | 20 | Information Expert justification per responsibility |
| Dependencies and layers | 20 | Declared package edges, no cycles, no layer violations |
| Naming contract | 15 | Every operation traces to the 9A Operation Name Registry |
| Traceability UC -> DSD -> DCD -> UCR | 15 | Complete mapping table for the iteration slice |

## Verdict

- `YES`: no blocking item and score >= 80.
- `CONDITIONAL`: score 60-79 with no critical gap.
- `NO`: any blocking item or score < 60.

## Blocking examples

- A postcondition without a satisfying element.
- A class in a package that the approved diagrams do not declare.
- An operation name invented outside the registry.
- A use case scenario in scope without DSD or UCR coverage.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "quoted text", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
