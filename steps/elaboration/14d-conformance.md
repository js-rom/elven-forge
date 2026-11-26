# Step 14D — Conformance (implementation vs Logical View)

## Inputs
- Approved `Logical View` diagrams for the scope: `*.packageDiagram.plantuml`, `*.classDiagram.plantuml`, `*.sequenceDiagram.plantuml`.
- `Use Case Realization` from 10, `Domain-to-Design Transition Map` from 9A, `Iteration Plan`, `SW Architecture Document`.
- The project build layout: production source tree and build command.

## Output contract
- Conformance matrix, one row per checked element: diagram element | `.plantuml` source | implemented counterpart (namespaced id or operation) | verdict (`MATCH`, `MISSING`, `EXTRA`, `DIVERGENT`) | action.
- Scope: packages/subsystems and scenarios selected by the Iteration Plan, plus any package touched by 14B or 14C.
- No code edits in this step.

## Preconditions
- `OK 14C` approved.
- Build tree compiles before reviewing: run the project's compile command.

## Rubric
- Package conformance: declared packages exist with the same namespaced identifier; no implemented classifier in an undeclared package; layer rules hold.
- Classifier conformance: same identifier and kind; visible operations and attributes cover those invoked by the DSDs; relationships match.
- Interaction conformance: every lifeline and message resolves to an existing classifier and operation.
- `OK 14D` is valid only with a fully `MATCH` matrix.

## Evidence required
- Build evidence (compile command and result).
- Conformance matrix.
- Non-`MATCH` rows with route: new TDD item in `Test Plan` -> 14B -> 14C -> 14D.

## Anti-patterns
- Bending code to a stale diagram that contradicts an approved postcondition; route it to 9B instead.
- Reviewing the whole Logical View folder on every iteration.
- Declaring 14B/14C complete without this gate.
