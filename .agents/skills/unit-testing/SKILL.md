---
name: unit-testing
description: "Use when creating, reviewing, or refactoring unit tests. Based on USantaTecla unit-testing criteria: easy to execute, maintain, read/write, and safety-net focused. Triggers: unit testing, pruebas unitarias, test quality, flaky tests, anti-patterns de pruebas, safety net tests."
---

# Unit Testing Skill

## Purpose

Define a practical workflow so an agent can create and improve unit tests that are executable, maintainable, readable, and reliable as a safety net.

## Source

Core source concepts integrated here:
- easy to execute tests,
- easy to maintain tests,
- easy to read/write tests,
- tests as specification and documentation,
- tests as quality feedback and risk reduction (safety net),
- anti-pattern catalog for test quality.

## Scope

Use this skill for:
- creating unit tests for classes/components,
- improving existing test suites,
- reviewing test quality and anti-patterns,
- reducing flaky, slow, or brittle tests.

When a scenario requires real persistence, network, external process, or environment coupling, classify it as non-unit and isolate it from this flow.

## Unit Testing Quality Model (MANDATORY)

### 1. Easy To Execute

Tests MUST be:
- automated,
- self-verifying,
- repeatable,
- independent,
- fast.

Practical rules:
- Run tests in one command/key action.
- No human input during execution.
- No manual console inspection to decide pass/fail.
- Consecutive runs on same code and data setup MUST yield same result.
- Tests MUST be environment-agnostic and not depend on hidden external state.
- Regression suite SHOULD complete in seconds whenever feasible.

### 2. Easy To Maintain

Test code MUST be professional code:
- apply design principles (SOLID/GRASP/KISS/DRY/YAGNI) to tests as well,
- minimize overlap between tests,
- isolate SUT from environment and slow collaborators via test doubles,
- centralize setup/teardown and repetitive construction via test utilities,
- use builders/object mother style helpers when constructor changes would cascade.

### 3. Easy To Read/Write

Tests MUST be:
- cohesive: one clear behavior per test,
- simple: low incidental complexity,
- expressive: intent-revealing names and assertions.

Practical rules:
- avoid "multi-personality" tests (multiple behaviors in one test),
- avoid conditional logic in tests unless unavoidable,
- avoid magic numbers and unexplained literals,
- use helper methods and custom assertions as a small domain-specific test language,
- keep tests compact; long tests require explicit rationale.

### 4. Improve Understanding Of The SUT

Tests MUST serve as:
- executable specification of behavior,
- living documentation for maintenance and extension.

### 5. Improve Quality

Tests SHOULD:
- repel regressions quickly,
- localize defects precisely.

### 6. Reduce Risk

Test suite MUST act as a real safety net:
- broad enough to protect expected behavior,
- robust enough to support safe change.

## Anti-Pattern Checklist (MUST detect and fix)

The agent MUST detect and report these anti-patterns when present:
- Prueba Interventora (needs human intervention),
- Prueba Bocazas (requires manual output reading),
- Prueba con Abundantes Sobras (leftover shared state/order dependency),
- Prueba con Dependencia Oculta (hidden external preconditions),
- Prueba Lenta,
- Comentario Enganoso,
- Dependiente de la Creacion,
- Prueba Extrana,
- Prueba Cotilla,
- Prueba de Multiple Personalidad,
- Prueba con Logica Condicional,
- Prueba Obscura,
- Prueba con Numeros Magicos,
- Prueba con Aserciones Sobreprotegidas.

## Agent Workflow (MANDATORY)

1. Identify SUT, behavior, and unit boundaries.
2. Build a behavior-focused test list (normal, edge, error, regression cases).
3. Implement/update tests ensuring executable-quality criteria first.
4. Ensure every test is self-verifying and deterministic.
5. Remove environment coupling and hidden dependencies.
6. Improve maintainability (utilities, builders, setup/teardown consolidation).
7. Improve readability and expressiveness (names, assertions, structure).
8. Run suite and capture evidence (pass/fail, duration, flaky signals).
9. Detect anti-patterns and apply fixes.
10. Produce a concise quality report and residual risks.

## Output Contract (MUST)

The agent output MUST include:
- SUT and test-scope summary,
- test inventory grouped by behavior,
- execution evidence (command, pass/fail, timing),
- anti-pattern findings with concrete fixes,
- maintainability decisions (utilities/builders/helpers),
- readability improvements applied,
- explicit statement on safety-net confidence and remaining risks.

## Completion Criteria

- Tests are automated, self-verifying, repeatable, independent, and fast enough.
- No blocking anti-pattern remains.
- Unit tests document expected behavior clearly.
- Suite provides actionable confidence for change.

