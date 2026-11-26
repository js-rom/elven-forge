# Step 12 — Data Model + JPA Mapping

## Inputs
- `Domain Model`, `System Sequence Diagrams`, `Operation Contracts`.
- Reviewed `Logical View` and `Use Case Realization` from steps 8-11.
- `Supplementary Specification`, `Glossary`, existing master data model and JPA mapping.
- Skills `data-model`, `jpa-mapping`; PlantUML template and JPA mapping template.

## Output contract
- Physical data model in PlantUML, framework-agnostic: entities, keys, relationships, constraints, indexes.
- `JPA Mapping`: entity boundaries, ownership, identifiers, inheritance, fetch/loading strategy, concurrency, migration notes and persistence trade-offs.
- Both artifacts in master-only mode: apply the iteration delta to the same files.
- If the iteration has no data scope, record the skip rationale and still request the gate.

## Preconditions
- `OK 11` approved and no use case marked `NO`.
- Persisted artifacts refined in 11 reloaded before drafting.

## Rubric
- Every persistence touchpoint of the scenario slice is covered.
- Constraints and indexes are justified by a query or invariant.
- No framework annotation appears in the domain model artifact.

## Evidence required
- Data model and mapping paths.
- Constraint/index list tied to invariants.
- Skip rationale when not applicable.
- `OK 12` request.

## Anti-patterns
- Mixing JPA annotations into the domain model.
- Creating per-iteration copies of the data model.
- Skipping the step silently.
