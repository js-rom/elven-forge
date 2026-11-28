# Iteration Verification — instruction

Produce the iteration-level verification at step 14D. This artifact answers one question: **was everything planned for this iteration actually implemented and demonstrated, regardless of whether it has a test?**

## Inputs

- The Iteration Plan: Scope IDs and Iteration Exit Criteria.
- The Test Plan: Test IDs, Scope IDs, Status, Test file, Evidence.
- The Acceptance Test Plan: A-IDs, Scope IDs, Feature file, Executed, Result.
- The Logical View diagrams and the Use Case Realization for the iteration slice.
- The production source tree and the build command.

## How to build it

1. **Design Conformance:** copy the design-to-code matrix from the 14D review. One row per checked package, classifier or message. Verdict: `MATCH`, `MISSING`, `EXTRA` or `DIVERGENT`.
2. **Iteration Plan Coverage:** one row per Scope ID from the Iteration Plan. Fill:
   - `UC/Scenario` from the plan.
   - `Design` with the DSD/DCD/UCR references, or `n/a` for refactor/support items.
   - `Implementation` with the classifier/operation or `n/a` for documentary items.
   - `Test IDs` from the Test Plan.
   - `A-IDs` from the Acceptance Test Plan.
   - `Evidence` with the command, commit or inspection that proves it.
   - `Verdict`: `COVERED`, `DEFERRED`, `MISSING` or `PARTIAL`.
3. **Iteration Exit Criteria:** one row per criterion in the plan. Evidence must be a command, report or inspection, not a claim.
4. **Test Quality (Mutation):** only when the Iteration Plan enables it. Copy the score row and the survivor triage from the `mutation_report.py` output. Do not invent a verdict: the script computes it. Omit the section when mutation is off.
5. **Code Quality:** only when the Iteration Plan enables it. Copy the gate and the scorecard from the `quality_report.py` output, and triage every finding. Omit the section when quality is off.
6. **Verdict:** `READY` only when Design Conformance is all `MATCH`, Plan Coverage has no `MISSING`/`PARTIAL`, and every criterion is `MET`.

## Rules

- A `COVERED` item without tests is valid only with an explicit no-test rationale in `Evidence` (for example, a documentary item or a refactor covered by regression).
- A `DEFERRED` item must appear in Uncovered and Deferred with a reason and approval.
- Do not edit code in this step.
- Do not re-run the test suites; 14C owns execution and the Test Plan owns unit/integration evidence.
- Do not re-run PIT here either; 14B owns the mutation run and 14D only reports and applies the veto.
- Omit the Test Quality section when mutation is off. A high score with high `No coverage` is `BLIND_SPOTS`, not `PASS`.
- Do not re-run Sonar here; 14B owns the quality run. A first `BASELINE` is a debt record, not a pass; legacy debt is not a gate.
- If a design element is stale, route it to 9B; if a package or layer is wrong, route it to 8.

## Anti-patterns

- Copying the Test Plan as the coverage matrix instead of building the plan-to-implementation graph.
- Marking `COVERED` without evidence.
- Hiding a `MISSING` item as `DEFERRED` without approval.
- Re-running suites or editing code here.
