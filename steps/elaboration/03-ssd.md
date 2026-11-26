# Step 3 — System Sequence Diagrams

## Inputs
- `Iteration Plan` with the use cases and scenarios in scope.
- `Domain Model`, `Use Case Model` and the brief or fully dressed use case.
- Active schema instruction and template for system sequence diagrams.

## Output contract
- One SSD per scenario in scope.
- Actor, system boundary and system operations as messages; no internal objects.
- Operation names follow the use case vocabulary and will become the contract names.
- PlantUML source persisted at the schema path for the scenario.

## Preconditions
- `OK 2` approved.
- Domain Model refined for the iteration.

## Rubric
- One scenario per diagram; no merged flows.
- Every main-success step and every extension maps to a system operation.
- Names are stable and reusable by Operation Contracts and DSDs.

## Evidence required
- Scenario list and duplicate-name check.
- `OK 3` request.

## Anti-patterns
- Including controllers, services or domain objects in an SSD.
- Inventing operations that the use case does not describe.
- Merging two scenarios into one diagram.
