# Step 14D — Iteration Verification

## Inputs
- `Iteration Plan`: Scope IDs and Iteration Exit Criteria.
- `Test Plan`: Test IDs, Scope IDs, Status, Test file and Evidence.
- `Acceptance Test Plan`: A-IDs, Scope IDs, Feature file, Executed and Result.
- Approved `Logical View` diagrams, `Use Case Realization`, `Domain-to-Design Transition Map`, `SW Architecture Document`.
- Production source tree and the project build layout.

## Output contract
- Produce the `Iteration Verification` artifact for the iteration (master path, iteration-scoped). Do not write it into the Test Plan.
- **Design Conformance**: one row per checked element: element | source | implementation | verdict (`MATCH`, `MISSING`, `EXTRA`, `DIVERGENT`) | action.
- **Iteration Plan Coverage**: one row per `Scope ID`: UC/scenario | design | implementation | Test IDs | A-IDs | evidence | verdict (`COVERED`, `DEFERRED`, `MISSING`, `PARTIAL`).
- **Iteration Exit Criteria**: one row per criterion: evidence | verdict (`MET`, `NOT MET`).
- **Build Evidence** and **Verdict** (`Overall: READY` or `NOT READY`).
- No code edits. The Test Plan is not modified here; it closes in 14B.

## Preconditions
- `OK 14C` approved.
- The build tree compiles before reviewing: run the project's compile command.
- Scope IDs and exit criteria are present in the Iteration Plan.

## Rubric
- Design Conformance: every row `MATCH`; no `MISSING`, `EXTRA` or `DIVERGENT`.
- Plan Coverage: every Scope ID `COVERED` or `DEFERRED` with approval; no `MISSING` or `PARTIAL`.
- Exit Criteria: every criterion `MET`.
- `Overall: READY` only when the three checks above are green.
- A `COVERED` item without tests is valid only with an explicit no-test rationale in `Evidence`.
- A design element that contradicts an approved postcondition is a stale diagram: route it to 9B, not to code.

## Evidence required
- Build command and result.
- Design conformance matrix.
- Plan coverage matrix.
- Exit criteria table.
- `up-reviewer` verdict using `rubrics/conformance.md`; a `NO` blocks the gate.
- Non-`MATCH` rows with route: 14B TDD item, 9B, 9A or 8.
- `OK 14D` request.

## Anti-patterns
- Using the Test Plan as the home of the coverage matrix.
- Marking a `MISSING` item as `DEFERRED` without approval.
- Re-running test suites here; 14C owns execution and the Test Plan owns unit/integration evidence.
- Declaring `READY` with an uncovered Scope ID or a `NOT MET` criterion.
- Reviewing the whole Logical View folder on every iteration.
