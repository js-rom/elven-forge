# Step 14A — Acceptance Tests (ATDD)

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

## Preconditions
- `OK 13` approved.
- Feature path under `src/test/resources/features/` and acceptance glue available.

## Rubric
- Every acceptance scenario traces to a UC step or extension and to a contract postcondition.
- Every scenario has a `Scope ID` and a feature file that 14C can reconcile.
- The promotion gate is applied; not every invariant becomes an acceptance test.
- Features are executable in principle, but not executed before the gate.

## Evidence required
- Scenario list and coverage counts.
- Invariant and rules matrices.
- `OK 14A` request before persisting the plan.

## Anti-patterns
- Writing acceptance scenarios after the implementation is green.
- Turning legal or organizational duties into fake executable tests.
- Promoting every invariant to acceptance coverage.
