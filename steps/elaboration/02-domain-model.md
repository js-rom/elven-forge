# Step 2 — Domain Model

## Inputs
- `Iteration Plan` (scope and selected use cases).
- `Use Case Model` and the brief or fully dressed use case for each selected use case.
- `Glossary`, `Supplementary Specification` and the existing master `Domain Model`.
- Active schema instruction and template for the domain model.

## Output contract
- Update the master `Domain Model` with the iteration delta; never a new file per iteration.
- General model diagram in PlantUML with concepts, attributes, associations and multiplicities.
- Invariants with stable ids (I..), traceable to business rules.
- Sub-domain diagrams only when they add clarity; workflow trace when the model changes lifecycle.
- No software classes, no JPA annotations, no persistence choices.

## Preconditions
- `OK 1` approved.
- Domain Model from previous iterations read before editing.

## Rubric
- Every concept in scope has attributes, associations and multiplicity.
- Every invariant is testable and has a stable id.
- Vocabulary matches the Glossary; new terms are proposed for it.

## Evidence required
- Draft in chat.
- List of added/changed concepts and invariant ids.
- Proposed Glossary updates.
- `OK 2` request.

## Anti-patterns
- Including controllers, repositories, entities or table names.
- Renaming domain concepts without updating the Glossary.
- Creating an iteration-specific domain model file.
