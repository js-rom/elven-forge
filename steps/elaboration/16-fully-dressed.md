# Step 16 — Use Case Fully Dressed (10%)

## Inputs
- Refined `Requirements Ranking` and `Use Case Model`.
- Candidate pool: only use cases still in brief format.
- Schema instruction and template for fully dressed use cases.

## Output contract
- Select 10% of the pending brief use cases (at least one), justified from the ranking by architectural significance, risk and business value.
- Explain the selection reasons before drafting.
- Write each selected use case in fully dressed format, one at a time, refined with the user before moving to the next.
- Keep the use case structure required by the template: goal, scope, level, actors, stakeholders, preconditions, success guarantee, main success scenario, extensions, special requirements, variations, frequency, miscellaneous.

## Preconditions
- `OK 15` approved.
- The candidate pool excludes any use case already fully dressed.

## Rubric
- Selection comes from the pending brief pool, not ad hoc.
- Every section is complete; unresolved items are `TBD` with a reason, never omitted.
- Special requirements trace to the Supplementary Specification when applicable.

## Evidence required
- Selection list with ranking justification.
- One draft per selected use case.
- `OK 16` request.

## Anti-patterns
- Choosing deep-dive use cases without the ranking.
- Fully dressing a use case already documented.
- Inventing a new use case in this step.
