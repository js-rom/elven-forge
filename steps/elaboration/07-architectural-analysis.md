# Step 7 — Architectural Analysis

## Inputs
- `Vision and Business Case`, `Use Case Model`, `Supplementary Specification`.
- Existing `Architectural Analysis` and `Technical Memo` artifacts.
- Skill `architectural-analysis`, schema instruction and templates for analysis and memos.

## Output contract
- `Architectural Analysis`: FURPS+ factor tables, prioritized factors, architectural decisions with trade-offs and rationale, variation and evolution points, over/under-engineering risks, unresolved issues.
- `Technical Memo`: one file per significant decision or issue, using the memo template. Do not embed memos inside the analysis document.
- Refine `Supplementary Specification` when the analysis changes a quality requirement.

## Preconditions
- Requirements from the iteration approved (`OK 4`; step 5/6 resolved or skipped).
- Architectural drivers identified from the scope.

## Rubric
- Every prioritized factor has scenario, response and measure.
- Every decision states the alternatives considered and why they were rejected.
- Variation and evolution points are explicit, not implied.

## Evidence required
- Factor table summary and top drivers.
- List of technical memos created or updated.
- `OK 7` request.

## Anti-patterns
- Writing decisions without alternatives.
- Duplicating memo content in the analysis document.
- Prioritizing every factor as critical.
