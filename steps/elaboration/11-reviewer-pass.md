# Step 11 — Reviewer Pass (Logical View)

## Inputs
- Approved outputs of steps 8, 9A, 9B and 10.
- `Domain Model`, `System Sequence Diagrams`, `Operation Contracts`, `Supplementary Specification`, `Glossary`, `Architectural Analysis`.
- Skills `design-principles`, `architectural-design`; schema instruction/template for use case realization.

## Output contract
- Mechanical consistency pass first: `design-consistency.ps1` over steps 8, 9A, 9B and 10 with the 9B arguments. Any `[ERROR]` blocks the gate.
- Structural review of step 8: package catalog, scenario traceability, layer rules, dependency direction.
- Transition review of 9A: transformation map, responsibility matrix, postcondition traceability, pattern evidence and rationale.
- Scenario review of 9B: one DSD per scenario, DCD deltas only in touched packages, collaborations consistent with 9A, controller/view separation, postconditions satisfied.
- Documentation review of 10: complete scenario mapping, references, SVG integrity, no new design elements.
- Per use case: principles applied, blocking issues, refactors, remaining risks, readiness for 12: `YES`, `CONDITIONAL` or `NO`.

## Preconditions
- `OK 10` approved.
- Iteration slice known; do not review the whole Logical View folder.

## Rubric
- A single `NO` blocks step 12.
- Every blocking finding has a citation and an owning step.
- Warnings are accepted only with a written rationale.

## Evidence required
- `up-reviewer` verdict using `rubrics/logical-view.md`; a `NO` blocks the gate.
- Validator output (0 errors).
- Findings table with route: 8, 9A, 9B or 10.
- Readiness statement per use case.
- `OK 11` request.

## Anti-patterns
- Approving with unresolved `NO`.
- Fixing design issues here instead of routing them to the owning step.
- Reviewing packages untouched by the iteration.
