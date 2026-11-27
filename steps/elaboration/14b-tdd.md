# Step 14B — TDD (code + tests)

## Inputs
- `Iteration Plan` as a hard scope gate: implement only the approved use cases, scenarios or slices.
- `Use Case Realization` and the reviewed `Logical View` from steps 8-11, as the design-to-code contract.
- `System Sequence Diagrams`, `Operation Contracts`, `SW Architecture Document`, `Supplementary Specification`, `Glossary`.
- If persistence: `Data Model` and `JPA Mapping` from 12. If UI: `Design System`, `Visual Specs`, `Interaction Spec`, `UI Technology Mapping`, and the linked screen assets. If architecturally risky: `Architectural Analysis` and `Technical Memo`.
- Skill `tdd`.

## Output contract
- `Test Plan` with test items grouped by scenario. Each item records the acceptance scenario(s) from 14A that it satisfies.
- Every item traces to: Iteration Plan item, use case/scenario, UCR section, SSD reference, Operation Contract postcondition; plus architecture, persistence or UI references when applicable.
- Every item declares `Scope IDs`, `Status` (`implemented` or `deferred`), `Test file` and `Evidence`. Deferred items appear in `Deferred Items` with a reason and approval.
- At the final `OK 14B`, re-persist the `Test Plan` with the actual status and evidence of every item.
- The final review covers the whole scope, not only UI: implemented, deferred and not covered items.
- For UI scope: at least one fidelity item per target view, traced to `state_id`, `transition.id`, the Vaadin Mapping section and the mock path.
- Code and tests are file-based TDD outputs; only `Test Plan` is a persisted artifact.
- For multi-batch TDD, the worker drafts the test slice and batch plan under `.atl/staging/{domain}/{iteration}/14B/`; the orchestrator presents it, and storage persists the approved `Test Plan`. Code and tests are written in place only after `OK 14B.IMPL`.

## Preconditions
- `OK 14A` approved.
- Selected scenario passed step 11 with no blocking design issue.
- `design-consistency.ps1` re-run over the iteration slice with updated `-NewPackages`: zero `[ERROR]`.
- For UI scope: present the implementation baseline (views, state ids, mocks, transitions, Vaadin sections, deferred states) before the gate.

## Rubric
- Each cycle has a failing test first, a minimal change, and a green suite with evidence.
- Every approved test item has a status and evidence at close; deferred items are justified.
- No behavior outside the approved scenario slice.
- A discovered issue is routed to its owning artifact instead of being absorbed into code silently.

## Evidence required
- Test slice and TDD plan, then `OK 14B` (or `OK 14B.CASES` when automatic case selection is requested).
- After `Test Plan` is persisted: `OK 14B.IMPL` before real edits and test execution.
- RED/GREEN evidence per cycle, with commands and counts.
- Re-persisted `Test Plan` with status and evidence for every item; no `planned` item remains.
- Final `OK 14B` when the implementation is complete, before 14C.

## Anti-patterns
- Implementing out-of-scope work because "it was easy".
- Writing tests after the code in the same cycle.
- Editing code before `OK 14B.IMPL`.
- Leaving `planned` or `pending` items in the Test Plan at the close.
