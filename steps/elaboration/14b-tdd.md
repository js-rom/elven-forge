# Step 14B — TDD (code + tests)

## Roles

- Test author: writes the `Test Plan` and the test code, and produces RED.
- Implementer: writes production code only after `OK 14B.IMPL`; tests and features are read-only.
- The test author never writes `src/main`; the implementer never writes `src/test`.

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
- For multi-batch TDD, the test author drafts the batch plan under `.atl/staging/{domain}/{iteration}/14B/`; the orchestrator presents it, and storage persists the approved `Test Plan`.
- After `OK 14B`, the test author writes the tests in place and produces RED; the implementer starts only after `OK 14B.IMPL`.
- If the Iteration Plan enables `Test Quality`, the mutation loop runs after GREEN and before the final `OK 14B`:
  - `runner` executes PIT over the slice and `mutation_report.py` produces the score, the triage and the suggested classes.
  - `test-author` strengthens weak tests under a recorded re-open; `implementer` removes dead code; `orchestrator` owns equivalents and design gaps.
  - Re-run the affected tests and the affected mutation classes; a measure closes only when the survivor dies.
  - The re-open **strengthens, never widens scope**: a new scenario returns to 14A.
- If the Iteration Plan enables `Code Quality`, the quality loop runs after GREEN and before mutation:
  - `runner` runs the Sonar analysis over the new code, plus ArchUnit and Trivy, and `quality_report.py` emits the scorecard and the triage.
  - `implementer` fixes critical bugs and vulnerabilities; `test-author` closes coverage gaps; `orchestrator` owns allowlists, architecture routing and debt IDs.
  - Re-run the analysis; a finding closes only when it disappears or is allowlisted with evidence. The baseline is not a pass.

## Preconditions
- `OK 14A` approved.
- The feature baseline exists from 14A.
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
- After `OK 14B`: the test author writes the tests and runs RED; record the test baseline with `test_guard.py --tests --record`.
- After `Test Plan` is persisted: `OK 14B.IMPL` before production edits; tests and features are read-only.
- RED evidence produced by the test author (command + output).
- GREEN evidence from the implementer.
- `test_guard.py --features --verify` and `test_guard.py --tests --verify` OK; the orchestrator runs `gate.py --guard` for `OK 14B.IMPL` and the final `OK 14B`.
- Re-persisted `Test Plan` with status and evidence for every item; no `planned` item remains.
- If mutation is enabled: the PIT report path, `mutation_report.py` summary, the triage table and the effect evidence per measure.
- If quality is enabled: the Sonar gate, the `quality_report.py` scorecard, the triage and the effect evidence per measure.
- Test changes after the 14B baseline only through `test_guard.py --tests --record --reopen --reason`; the reason stays in the baseline.
- Final `OK 14B` when the implementation is complete, before 14C.

## Anti-patterns
- Implementing out-of-scope work because "it was easy".
- Writing tests after the code in the same cycle.
- Editing code before `OK 14B.IMPL`.
- Leaving `planned` or `pending` items in the Test Plan at the close.
- The implementer editing tests or features.
- The test author writing production code.
- Changing a test after `OK 14B` without a new approval.
- Silently re-baselining tests to hide a mutation finding.
- Chasing 100% mutation score or allowlisting without evidence.
- Treating the first quality baseline as a pass or blocking on legacy debt.
