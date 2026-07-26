# Iteration Plan Purpose

The Unified Process is use case driven. Work is organized around completing use cases, but the practical unit of iteration planning is often a **use case scenario** rather than the full use case. When a complete use case is too large or risky for a single iteration, the iteration should select one or more scenarios or slices of that use case, together with any supporting features needed to deliver a meaningful increment.

## Instructions for the Agent

- Produce one Iteration Plan artifact per elaboration iteration.
- Persist the approved artifact under `08 Project Management/{{#}} {Iteration} Plan.md`.
- In that file name, `{{#}}` is the zero-padded numeric part of `{Iteration}` (`E1 -> 01`, `E11 -> 11`).

### 1. Time Box

- Treat each iteration as a **2-week time box** unless the user states otherwise.
- Record the iteration dates and goal clearly.

### 2. Team Capacity

- Ask for the available hours of each team member during the 2-week period.
- Sum the hours and use that total as the planning capacity.

### 3. Planning Unit

- Prefer planning around a **use case scenario** or a thin vertical slice.
- A full use case may be selected only when it is realistically deliverable within the iteration.
- Features not tied to a single use case may also be selected when they are necessary for architecture, infrastructure, or cross-cutting concerns.

### 4. Scope Clarification

- Describe each selected use case, scenario, or feature in enough detail to support planning.
- Record resolved questions and outstanding questions.
- State the expected result for the selected scope.

### 5. Task Breakdown

- Brainstorm a set of more detailed tasks with rough estimates.
- Include tasks across the relevant areas, such as UI, database, domain logic, testing, deployment, and external system integration.
- Keep the breakdown concrete enough to support a capacity decision, but do not over-engineer the estimates.

### 6. Running Total and Cut Line

- Sum all task estimates into a running total.
- Continue selecting and estimating work until the iteration is full enough to meet the goal without exceeding realistic team capacity.
- Make the cut line explicit so it is clear what work should be deferred first if estimates increase.

### 7. Risks and Dependencies

- Capture the main risks and dependencies that could threaten the iteration outcome.
- Note the mitigation or follow-up action for each one.