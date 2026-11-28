# Step 14D — Iteration Verification

## Inputs
- `Iteration Plan`: Scope IDs and Iteration Exit Criteria.
- `Test Plan`: Test IDs, Scope IDs, Status, Test file and Evidence.
- `Acceptance Test Plan`: A-IDs, Scope IDs, Feature file, Executed and Result.
- Approved `Logical View` diagrams, `Use Case Realization`, `Domain-to-Design Transition Map`, `SW Architecture Document`.
- Feature and test baselines from 14A and 14B.
- Production source tree and the project build layout.
- If mutation is enabled: the `Test Quality` block of the Iteration Plan, the PIT report from 14B, `mutation-baseline.json`, the allowlist and the triage table.
- If quality is enabled: the `Code Quality` block of the Iteration Plan, the Sonar gate, `quality-baseline.json`, the allowlist and the triage table.

## Output contract
- Produce the `Iteration Verification` artifact for the iteration (master path, iteration-scoped). Do not write it into the Test Plan.
- **Design Conformance**: one row per checked element: element | source | implementation | verdict (`MATCH`, `MISSING`, `EXTRA`, `DIVERGENT`) | action.
- **Iteration Plan Coverage**: one row per `Scope ID`: UC/scenario | design | implementation | Test IDs | A-IDs | evidence | verdict (`COVERED`, `DEFERRED`, `MISSING`, `PARTIAL`).
- **Iteration Exit Criteria**: one row per criterion: evidence | verdict (`MET`, `NOT MET`).
- **Build Evidence** and **Verdict** (`Overall: READY` or `NOT READY`).
- **Test Quality (Mutation)** when the Iteration Plan enables it: one row per slice with score, target, killed, survived, no coverage, trend and verdict; a survivor triage with class, measure, owner and status. Omit the section when mutation is off.
- **Code Quality** when the Iteration Plan enables it: one row with the gate, coverage, duplication, issues, critical findings and verdict; a finding triage with class, measure, owner and status. Omit the section when quality is off.
- No code edits. The Test Plan is not modified here; it closes in 14B.

## Preconditions
- `OK 14C` approved.
- `test_guard.py --features --verify` and `test_guard.py --tests --verify` pass.
- The build tree compiles before reviewing: run the project's compile command.
- Scope IDs and exit criteria are present in the Iteration Plan.
- If mutation is enabled: `mutation_report.py` produced a triage with no `UNCLASSIFIED` survivor and the protected invariants are clean.
- If quality is enabled: `quality_report.py` produced a triage with no `UNCLASSIFIED` finding, the gate is green and there are no new critical findings.

## Rubric
- Design Conformance: every row `MATCH`; no `MISSING`, `EXTRA` or `DIVERGENT`.
- Plan Coverage: every Scope ID `COVERED` or `DEFERRED` with approval; no `MISSING` or `PARTIAL`.
- Exit Criteria: every criterion `MET`.
- `Overall: READY` only when the three checks above are green.
- A `COVERED` item without tests is valid only with an explicit no-test rationale in `Evidence`.
- A design element that contradicts an approved postcondition is a stale diagram: route it to 9B, not to code.
- Test Quality: the `rubrics/mutation-quality.md` verdict is `YES`, or `CONDITIONAL` with recorded debt under advisory. Under blocking, `CRITICAL` or `REGRESSION` blocks `READY`.
- A high score with high `no_coverage` is `BLIND_SPOTS`, not `PASS`.
- Code Quality: the `rubrics/code-quality.md` verdict is `YES`, or `CONDITIONAL` with recorded debt under advisory. Under blocking, a new critical finding, an ArchUnit violation or coverage below the floor blocks `READY`.
- The first quality baseline is a debt record, not a pass.

## Evidence required
- Build command and result.
- Design conformance matrix.
- Plan coverage matrix.
- Exit criteria table.
- Test and feature guard OK; the orchestrator runs `gate.py --guard` for `OK 14D`.
- `up-reviewer` verdict using `rubrics/conformance.md`; a `NO` blocks the gate.
- If mutation is enabled: the report path, the triage table and the effect evidence per measure; `up-reviewer` verdict using `rubrics/mutation-quality.md`.
- If quality is enabled: the gate, the scorecard, the triage and the effect evidence per measure; `up-reviewer` verdict using `rubrics/code-quality.md`.
- Non-`MATCH` rows with route: 14B TDD item, 9B, 9A or 8.
- `OK 14D` request.

## Anti-patterns
- Using the Test Plan as the home of the coverage matrix.
- Marking a `MISSING` item as `DEFERRED` without approval.
- Re-running test suites here; 14C owns execution and the Test Plan owns unit/integration evidence.
- Declaring `READY` with an uncovered Scope ID or a `NOT MET` criterion.
- Reviewing the whole Logical View folder on every iteration.
- A test or feature changed after approval.
- Hiding blind spots behind a high score, or allowlisting without evidence.
- Blocking on legacy debt or treating the first quality baseline as a pass.
