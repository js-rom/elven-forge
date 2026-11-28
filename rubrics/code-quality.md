# Rubric — Code Quality (steps 14B/14D)

Use with `.opencode/agents/up-reviewer.md` when the Iteration Plan enables
`Code Quality`. The reviewer judges the **triage and the evidence**, not the
absolute score. A baseline with legacy debt is not a failure; a hidden critical
finding is.

## Criteria

| Criterion | Weight | Evidence required |
|---|---|---|
| Reproducibility | 15 | Command, project key, Sonar version and runtime are recorded and reproduce the gate |
| Scope | 15 | The gate runs on the iteration's new code or slice; legacy debt is not used to block |
| Gate | 20 | Gate status and conditions are copied from the API, not inferred |
| Critical findings | 20 | 0 new critical bugs/vulnerabilities; every finding has a class, owner and measure |
| Coverage | 15 | New-code coverage >= 80% or an explicit, approved floor |
| Allowlist | 10 | Each entry states why it is a false positive and references evidence |
| Trend | 5 | Coverage, duplication and debt are compared against the baseline |

## Verdict

- `YES`: gate OK, zero new critical findings, coverage at or above the floor,
  complete triage, and every measure has an owner.
- `CONDITIONAL`: complete triage with recorded debt (Scope ID or debt ID) and
  no new critical findings. Allowed only under `advisory`.
- `NO`: a new critical finding, an unclassified issue, a missing gate or
  command, a baseline treated as a pass, or an allowlist entry without evidence.

## Routing

- `BUG` / `VULNERABILITY` -> 14B implementer.
- `CODE_SMELL` -> 14B implementer, or debt with a debt ID.
- `COVERAGE_GAP` -> 14B test-author.
- `ARCHITECTURE` -> 8 or 11.
- `DEPENDENCY_RISK` -> 14B implementer (upgrade).
- `FALSE_POSITIVE` -> allowlist, orchestrator.
- Out-of-scope debt -> Iteration Plan with a Scope ID or debt ID.

## Output

```json
{
  "verdict": "YES | CONDITIONAL | NO",
  "score": 0,
  "blocking": [
    { "criterion": "string", "evidence": "issue, gate or command output", "fix": "string" }
  ],
  "confidence": "high | medium | low"
}
```
