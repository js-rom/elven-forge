# Step 14C — Acceptance Execution (GREEN)

## Inputs
- `Acceptance Test Plan` from 14A and the implemented slice from 14B.
- Acceptance suite command from the domain config (`mvn test -Pacceptance` by default).
- Container runtime available when the suite needs Testcontainers.

## Output contract
- Per-scenario GREEN evidence from the acceptance suite.
- RED scenarios are defects: route each one through the 14B TDD loop (failing test -> fix -> green), then re-run the suite.
- Update `Acceptance Test Plan` with defects found (RED evidence + resolution) and final execution evidence: acceptance command and full unit suite.
- Do not change an approved scenario to make it pass.

## Preconditions
- `OK 14B` approved with the implementation complete.
- Docker/Testcontainers available if the suite requires it; otherwise stop and report.

## Rubric
- Every scenario in the iteration slice is GREEN, or has a documented defect with a route.
- The full unit suite also passes.
- Evidence is a command and its output, not a claim.

## Evidence required
- Acceptance command output with scenario and step counts.
- Full test suite output.
- Defect list with resolution.
- `OK 14C` request.

## Anti-patterns
- Declaring GREEN without running the suite.
- Editing scenarios to match the implementation.
- Hiding a RED scenario as "flaky" without evidence.
