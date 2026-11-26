# Step 9B — Scenario Design (sequence + class)

## Inputs
- Approved `Domain-to-Design Transition Map` (fixed contract for this step).
- Package diagrams from step 8; `System Sequence Diagrams`; `Operation Contracts`.
- Skills `sequence-diagram`, `class-diagram`, `design-principles`.
- For existing slices: the production source tree, read to obtain exact names and signatures.

## Output contract
- One Design Sequence Diagram per scenario in scope, starting from SSD system operations and contract postconditions.
- Design Class Diagram deltas only for the packages touched by the scenario.
- Validation of every contract postcondition against the 9A traceability matrix.
- Concise design rationale: cohesion/coupling, controller/view separation, pattern realization.
- Every operation name comes from the 9A registry; new operations on existing types are marked `NEW in {iteration}` and recorded in the transition map.

## Preconditions
- `OK 9A` approved.
- Scenario queue reused from 9A; do not rebuild it.

## Rubric
- One scenario per DSD; every lifeline resolves to a classifier in an approved package.
- Every message resolves to a visible operation; collaboration order satisfies the postconditions.
- No package, subsystem or layer boundary is redesigned here.

## Evidence required
- `design-consistency.ps1` output: zero `[ERROR]`; warnings need a written rationale.
- Touched packages and scenario list.
- `OK 9B` request.

## Anti-patterns
- Redesigning packages or overriding 9A decisions.
- Inventing names for existing APIs from memory.
- Reviewing the whole Logical View instead of the iteration slice.
