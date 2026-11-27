# Step 14A — Acceptance Tests (ATDD)

## Roles

- Owner: `test-author`. It writes the `.feature` files and their step definitions, in that order.
- The `implementer` never edits a feature or a step definition.
- `OK 14A` freezes the feature files; after that they are read-only.

## Inputs
- `Iteration Plan` as the scope contract.
- `System Sequence Diagrams` and `Operation Contracts` as the behavior contract; use case extensions.
- `Domain Model` invariants, with the promotion gate: legal rule, cross-layer integration, actor-visible effect or core domain contract.
- `domain-rules.md` for the rules compliance matrix.
- `Interaction Spec` and `UI Technology Mapping` as the UI acceptance source.
- `Use Case Realization` from step 10 as the design contract.
- Schema instruction and template for the acceptance test plan.

## Output contract
- One Gherkin feature per use case in scope, with one scenario per main-success step group and per extension, in domain vocabulary.
- Every `A-xx` row declares its `Scope ID`, `Feature file` and `Planned execution`, so 14C can reconcile what was agreed with what ran.
- Invariant coverage matrix: every in-scope invariant recorded with a decision (acceptance scenario or unit-only + rationale).
- Rules compliance matrix: `Cubierto`, `Pendiente` or `N-A`, with evidence. Organizational rules are traced, never faked as tests.
- RED evidence when the slice modifies existing code; for brand-new functionality, document the RED and materialize it in 14B.
- The step definitions bind the features to the system; they do not change the approved scenarios.
- After `OK 14A`, run `python .agents/scripts/test_guard.py --features --record` to freeze the feature files.

## Preconditions
- `OK 13` approved.
- Feature path under `src/test/resources/features/` and acceptance glue available.
- The test author owns the acceptance artifacts; the implementer is not involved.

## Rubric
- Every acceptance scenario traces to a UC step or extension and to a contract postcondition.
- Every scenario has a `Scope ID` and a feature file that 14C can reconcile.
- The promotion gate is applied; not every invariant becomes an acceptance test.
- Features are executable in principle, but not executed before the gate.

## Evidence required
- Scenario list and coverage counts.
- Invariant and rules matrices.
- Feature baseline recorded with `test_guard.py --features --record`.
- `OK 14A` request before persisting the plan.

## Anti-patterns
- Writing acceptance scenarios after the implementation is green.
- Turning legal or organizational duties into fake executable tests.
- Promoting every invariant to acceptance coverage.
- The implementer editing a feature or a step definition.
- Changing a feature after `OK 14A` without a new approval.
