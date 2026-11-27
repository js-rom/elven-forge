# Rubric — Iteration Verification (step 14D)

Use with `.opencode/agents/up-reviewer.md`. A single non-`MATCH`, non-covered item or `NOT MET` criterion blocks the gate.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Design conformance | 20 | Every package, classifier and interaction row is `MATCH` |
| Iteration Plan coverage | 30 | One row per `Scope ID`, `COVERED` or approved `DEFERRED`; no `MISSING`/`PARTIAL` |
| Exit criteria | 20 | Every criterion `MET` with a command, report or inspection |
| No-test rationale | 10 | A `COVERED` item without `Test IDs` has explicit evidence and a reason |
| Build evidence | 10 | Compile command and result over a tree that compiles |
| Matrix completeness | 10 | No invented Scope IDs, no missing rows, every row has a verdict |

## Verdict

- `YES`: all design rows `MATCH`, every Scope ID `COVERED` or approved `DEFERRED`, every criterion `MET`, `Overall: READY`.
- `NO`: any `MISSING`, `PARTIAL`, `NOT MET`, or a `COVERED` row without evidence.

## Routing

- Implementation deviation -> 14B TDD item.
- Stale diagram -> 9B (or 9A if the naming contract is wrong).
- Package or layer deviation -> 8.
- Plan scope change -> 1.

## Output

```json
{
  "verdict": "YES | NO",
  "score": 0,
  "blocking": [{ "criterion": "string", "evidence": "row or command output", "fix": "string" }],
  "confidence": "high | medium | low"
}
```
