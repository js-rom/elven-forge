# Step 15 — Refine Requirements Ranking

## Inputs
- Current `Requirements Ranking` and `Use Case Model`.
- Iteration feedback: defects, discoveries, new features or use cases, priority changes.
- `Iteration Plan` and the acceptance/TDD evidence.

## Output contract
- Refined master `Requirements Ranking` based on risk, coverage and criticality.
- Updated coverage counts: implemented, pending, retired, refactor pending.
- Explicit rationale for every priority change; new candidates enter as brief items, not as detailed use cases.

## Preconditions
- `OK 14D` approved.
- Iteration evidence available.

## Rubric
- Every change is justified by evidence from the iteration.
- Coverage counts reconcile with the Use Case Model.
- No use case is marked implemented without 14C/14D evidence.

## Evidence required
- Diff summary of ranking changes.
- Coverage counts before and after.
- `OK 15` request.

## Anti-patterns
- Re-ranking by intuition without iteration evidence.
- Adding a new use case directly in fully dressed format.
- Inflating coverage without acceptance evidence.
