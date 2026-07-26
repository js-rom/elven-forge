---
name: test-cases
description: "Use when selecting unit test cases in pair-programming mode (driver role). Triggers: casos de prueba unitarias, clases de equivalencia, valores limite, pairwise, vector ortogonal, caja negra, caja blanca, cobertura de caminos."
---

# Unit Test Cases Driver Skill

## Purpose

Guide the user, in pair-programming mode (agent as driver), to choose correct and sufficient unit test cases with strong coverage and controlled test-suite size.

## Source Basis

- black-box and white-box test design,
- equivalence partitioning,
- boundary value analysis,
- orthogonal/pairwise reduction,
- SUT-for-testability design considerations.

## Driver Mode (MANDATORY)

- The agent acts as the driver and the user as navigator.
- The agent proposes test-case selection decisions, trade-offs, and rationale.
- The agent MUST not jump to implementation before test-case agreement.
- For each stage, respond in this order:
  1. Proposed test-case slice.
  2. Open assumptions/questions.
  3. Explicit approval request: `Escribe OK CASOS N para continuar`.

## Test-Case Selection Workflow (MANDATORY)

1. Clarify behavior and acceptance scope.
	- Confirm the exact requirement and expected behavior.
	- If requirement is unclear, stop and refine with user first.

2. Identify test factors (input/output state space).
	- Input parameters for SUT exercise.
	- SUT state and DOC state needed in setup.
	- Relevant environment/configuration inputs.
	- Expected outputs, resulting state, and expected exceptions.
	- Preconditions and error classes.

3. Choose design strategy by objective.
	- Prefer black-box for behavior-driven selection.
	- Add white-box only when internal risk/paths justify it.

4. Build Equivalence Classes per factor.
	- Partition each factor into finite valid/invalid classes.
	- Pick one representative value per class.
	- Combine representatives across factors to produce baseline cases.

5. Apply Boundary Value Analysis where ordered domains exist.
	- Replace arbitrary representatives with boundary representatives.
	- Include near-boundary valid/invalid values when meaningful.

6. Control combinatorial explosion.
	- If combinations are large, reduce with orthogonal/pairwise strategy.
	- Keep explicit rationale of what interaction coverage is preserved.

7. Add white-box path coverage (when needed).
	- Analyze control flow and independent paths.
	- Ensure each selected path maps to at least one concrete test case.

8. Validate unit-test feasibility.
	- Cases MUST be executable at unit level (no external coupling unless doubled).
	- Prefer SUT design that exposes controllable seams (DI for DOCs, [mocks](../mocks/SKILL.md)/stubs).

9. Finalize minimal sufficient suite.
	- Keep only cases that add unique behavioral/path value.
	- Remove redundant cases while preserving coverage intent.

## Selection Rules (MUST)

- MUST start from requirements, not from current implementation details.
- MUST include both nominal and error classes.
- MUST include exception/precondition-driven cases where defined.
- MUST justify each retained case with a coverage reason.
- MUST detect and flag over-testing by duplicate intent.
- MUST detect and flag under-testing (missing class, limit, or critical path).

## Pair-Programming Guardrails

- Do not generate giant exhaustive Cartesian suites by default.
- Do not skip boundary analysis for ordered input domains.
- Do not force white-box coverage when behavior-level risks are already controlled.
- Do not ignore DOC-controlled inputs/outputs; model them via injectable seams or [mocks](../mocks/SKILL.md).

## Output Contract (MANDATORY)

The agent output MUST include:

- Scope summary (feature/behavior under test).
- Factor table (inputs, state, DOC, env).
- Equivalence class table (valid/invalid per factor).
- Boundary set (if applicable).
- Combination strategy used (full, orthogonal, pairwise) with rationale.
- Final test-case catalog, each case with:
  - id,
  - objective,
  - setup/preconditions,
  - input values,
  - expected output/state/exception,
  - coverage rationale (class/limit/path).
- Coverage gap note (what is intentionally out of scope and why).

## Done Criteria

- All relevant equivalence classes are covered by at least one case.
- Critical boundaries are covered where domains are ordered.
- Required interactions are covered with controlled case count.
- User has approved the final catalog.

