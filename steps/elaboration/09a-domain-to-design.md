# Step 9A — Domain-to-Design Transition

## Inputs
- `Domain Model` (concepts, attributes, associations, invariants).
- `System Sequence Diagrams` (system operations per scenario).
- `Operation Contracts` (postconditions in domain vocabulary).
- Approved package boundaries and dependency rules from step 8.
- `Supplementary Specification`, `Glossary`, skill `design-principles`.

## Output contract
- **Transformation map**: DomainModelConcept -> SoftwareClass or Interface. Note divergences and why.
- **Responsibility matrix**: knowing/doing responsibilities per class, justified with Information Expert and driven by contract postconditions.
- **Postcondition traceability matrix**: every contract postcondition -> the design element(s) that will satisfy it. Unassigned postconditions are `TBD` with a rationale.
- **Pattern candidates**: hotspots (versioning, state machines, policy variation) with problem evidence, intent fit and participant mapping.
- **Transformation rationale**: each divergence from the domain model, aligned with `design-principles`.
- **Operation name registry**: one row per system operation in scope: SSD operation -> design operation / entry point -> classifier that declares it (or `NEW in {iteration}`).

## Preconditions
- `OK 8` approved.
- Scenario queue from the iteration plan already built; do not rebuild it.

## Rubric
- Every postcondition is assigned or explicitly TBD with a reason.
- Every domain concept used by the scope is mapped or its absence justified.
- No pattern is proposed without problem evidence.

## Evidence required
- The six matrices/tables above.
- `OK 9A` request.

## Anti-patterns
- Designing sequence or class diagrams here.
- Assigning responsibilities without Information Expert justification.
- Inventing operation names outside the registry.
