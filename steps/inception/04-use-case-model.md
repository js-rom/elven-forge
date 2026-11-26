# Step 4 — Use Case Diagram and List

## Inputs
- Actor-goal table from step 3.
- `Vision and Business Case` for actors and scope.
- Active schema instruction and template for the Use Case Model.

## Output contract
- Continue the master `Use Case Model` with:
  - a use case context diagram in PlantUML: actors outside the system boundary, use cases inside;
  - the use case list required by the template, with links to each use case file;
  - relationships (`include`, `extend`, generalization) only when they are true in the domain.
- Use exactly the names agreed in step 3.

## Preconditions
- `OK 3` approved.

## Rubric
- Every actor-goal row appears as a use case or is explicitly deferred.
- No UI step is modeled as a use case.
- The list is compatible with the template and later becomes the source for briefs.

## Evidence required
- PlantUML block and list in chat.
- Deferred or ambiguous goals recorded.
- `OK 4` request.

## Anti-patterns
- Modeling screens, buttons or navigation.
- Renaming use cases to fit the diagram.
- Adding actors that the Vision does not support.
