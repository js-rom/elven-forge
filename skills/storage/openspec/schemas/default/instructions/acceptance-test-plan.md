# Acceptance Test Plan Purpose

The Acceptance Test Plan captures the output of the ATDD acceptance step (PASO 14A) of the elaboration workflow: executable Gherkin acceptance scenarios for the iteration slice, their traceability to use case steps/extensions, domain invariants, legal rules and interaction specs, the invariant coverage and rules compliance matrices, and the RED/GREEN evidence collected in PASO 14C.

## Guidelines

### 1. Scope

- Produce one Acceptance Test Plan artifact per elaboration iteration from PASO 14A, before the TDD implementation cycles of PASO 14B start.
- Scope is the same implementation slice approved in the `Iteration Plan` and the `Test Plan`.
- Each scenario must be executable with `mvn test -Pacceptance` against the real stack.

### 2. Scenario List

- One row per Gherkin scenario, with explicit traceability to the use case step or extension, the domain invariant, and the interaction spec state/transition it exercises.
- Derive scenarios from: Use Case main success scenario + extensions, `Interaction Spec` transitions, and domain invariants selected by the promotion gate.

### 3. Invariant Coverage Matrix

- List every domain invariant in the iteration scope.
- Promote an invariant to acceptance coverage when at least one of these holds:
  1. It traces to a legal rule (`domain-rules.md`).
  2. It depends on cross-layer integration (UI -> controller -> service -> persistence).
  3. Its violation is visible to the actor.
  4. It is part of the core domain contract (state machine, immutability, computations).
- Otherwise keep it `unit-only`, always with an explicit decision rationale. No silent exclusions.

### 4. Domain Rules Compliance Matrix

- List the legal rules in scope with status `Cubierto`, `Pendiente` or `N-A` and the evidence (invariant, use case, test id, or an explicit non-automatable justification). Legal/organizational obligations are recorded as traceability, never faked as tests.

### 5. Evidence

- Record defects found by acceptance scenarios (RED) and their resolutions (GREEN) with reference to the TDD tests that fixed them.
- Record the final execution evidence of `mvn test -Pacceptance` and `mvn test`.

## Output

- Persist the Acceptance Test Plan artifact once per elaboration iteration using the storage skill by artifact id (passing `{{#}}` and `{{Iteration}}`; storage resolves the concrete path from the active schema). Do NOT hardcode artifact paths.
- Gherkin feature files and step definitions remain file-based code artifacts under `src/test/resources/features` and `src/test/java`, like TDD tests.

## Quality Checklist

1. Is the scenario list complete for the iteration slice (main scenario + all extensions)?
2. Does every scenario trace to UC step/extension, invariant and interaction spec?
3. Does the invariant matrix record an explicit decision for every invariant in scope?
4. Does the rules matrix avoid pretending non-automatable rules are tested?
5. Is the execution evidence (RED/GREEN) recorded?
