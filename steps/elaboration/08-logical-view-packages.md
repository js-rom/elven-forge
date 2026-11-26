# Step 8 — Logical View (packages)

## Inputs
- `Iteration Plan`, `Domain Model`, `Architectural Analysis`, `Supplementary Specification`, `Glossary`.
- Skill `packages-logical-view` and the existing master logical view.

## Output contract
- Package catalog for the iteration scope: name, responsibility, inbound and outbound dependency rules, and the use cases or scenarios expected to touch it.
- UML package diagrams per package, subsystem or layer, in PlantUML, at package level only.
- Explicit package-to-scenario traceability list, consumable by step 9A.
- Layer and dependency-direction rules stated and enforced.

## Preconditions
- `OK 7` approved.
- Scope scenarios are known.
- If a scenario cannot be placed cleanly, resolve it here before 9A.

## Rubric
- No cycles; dependency direction matches the declared layers.
- Every scenario in scope is placed in at least one package.
- No class-level, method-level or sequence detail.

## Evidence required
- Package catalog and traceability list.
- Diagram list with paths.
- `OK 8` request.

## Anti-patterns
- Designing classes or methods in this step.
- One package per class.
- Leaving a scenario without a package assignment.
