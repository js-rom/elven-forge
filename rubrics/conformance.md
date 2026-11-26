# Rubric — Conformance (step 14D)

Use with `.opencode/agents/up-reviewer.md`. A single non-`MATCH` row blocks the gate.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Package conformance | 25 | Every declared package exists; no undeclared package in the source tree |
| Classifier conformance | 25 | Same identifier and kind; operations/attributes cover the DSD messages |
| Interaction conformance | 30 | Every lifeline and message resolves to an existing classifier and operation |
| Build evidence | 10 | Compile command and result over a tree that compiles |
| Matrix completeness | 10 | One row per checked element with a verdict and an action |

## Verdict

- `YES`: every row is `MATCH` and the build compiles.
- `NO`: any `MISSING`, `EXTRA` or `DIVERGENT` row, or no build evidence.

## Routing

- Implementation deviation -> 14B TDD item.
- Stale diagram -> 9B (or 9A if the naming contract is wrong).
- Package or layer deviation -> 8.

## Output

```json
{
  "verdict": "YES | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "row or command output", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
