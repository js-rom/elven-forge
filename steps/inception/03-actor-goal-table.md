# Step 3 — Actor-Goal Table

## Inputs
- `Vision and Business Case` (stakeholders, goals, scope).
- Active schema instruction for use cases and the Use Case Model template.
- Domain vocabulary from the project idea and context.

## Output contract
- Actor-goal-use case table in chat, a preparatory view for the Use Case Model.
- One row per actor-goal pair; the use case name expresses the goal from the actor's perspective.
- Names are stable and will be reused in step 4 and step 5 without renaming.

## Preconditions
- `OK 2` approved.
- Stakeholders and scope from the Vision available.

## Rubric
- Every actor in the Vision appears with at least one goal.
- Use case names are goal-oriented, not UI steps.
- No duplicate goals under different names.

## Evidence required
- The table in chat.
- Naming decisions and synonyms rejected.
- `OK 3` request.

## Anti-patterns
- Inventing actors not present in the Vision.
- Naming use cases after screens or buttons.
- Renaming use cases later without updating the model.
