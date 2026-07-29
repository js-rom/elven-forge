---
name: mocks
description: "Use when designing unit tests with test doubles (DOC): stub, mock, spy, dummy, and fake. Triggers: mocks, test doubles, DOC, stub, mock, spy, dummy, fake, behavior tests, state tests."
---

# Test Doubles In Unit Testing Skill

## Purpose

Guide the agent to select and use test doubles correctly in unit tests, maximizing isolation and speed without losing behavioral validity.

## Source

Based on:
- `4-pruebas/4-doblesPruebasUnitarias/index.html` ("Test Doubles in Unit Tests", USantaTecla).

## When To Use Doubles (MUST)

Use doubles when a DOC (dependency/collaborator object) makes the test:
- slow,
- erratic (time, randomness, sensor input),
- interventional (UI/manual),
- expensive to prepare,
- dependent on external infrastructure,
- unavailable.

## Core Principles (MUST)

- The double MUST implement the same interface as the real DOC.
- The test MUST define which DOC methods are simulated and with what responses/expectations.
- During execution, SUT calls to the real DOC MUST be intercepted by the configured double.
- Doubles exist for testing; they are not production artifacts.

## Double Types And Selection

### Stub

- Returns preconfigured outputs for given inputs.
- Ideal for state-based/black-box tests.
- Must not contain unnecessary logic for the scenario.

### Mock

- Defines interaction expectations (arguments, call counts, sequence when relevant).
- Ideal for behavior-based/white-box tests.
- Fails when actual interaction does not match expectations.

### Spy

- Combines stub behavior with interaction verification.
- Useful when state and collaboration must be validated together.

### Dummy

- Only fills argument lists; it does not participate in behavior.

### Fake

- Simplified functional implementation (for example, in-memory).
- Not suitable for production; use only with clearly documented limits.

## Decision Rule (MUST)

- If the main assertion is output/state of the SUT: prefer `Stub`.
- If the main assertion is SUT-DOC collaboration: prefer `Mock`.
- If both evidences are required: use `Spy`.
- If DOC does not really participate in the case: use `Dummy`.
- If a realistic but simplified in-memory behavior is needed: evaluate `Fake`.

## Lifecycle And Strategy

- In Test Last and Test First, doubles are introduced when the DOC harms test quality (speed, availability, etc.).
- In TDD inside-out, doubles usually appear as collaborations increase.
- In TDD outside-in, doubles may be mandatory to progress from outer layers.

## Trade-Offs (MUST be explicit)

### With Doubles

- Benefits:
	- SUT isolation,
	- higher speed and control,
	- stronger focus on pure unit scope.
- Risks:
	- coupling to implementation details,
	- fragility after internal refactors,
	- false greens caused by incorrect expectations.

### Without Doubles

- Benefits:
	- less coupling to internal implementation,
	- higher integrated validation of real collaborations.
- Costs:
	- slower execution,
	- environment and availability dependency.

## Agent Operational Workflow (MANDATORY)

1. Identify the SUT and all DOCs involved in the test case.
2. Classify DOC risk: slowness, nondeterminism, unavailability, infrastructure coupling, UI/manual dependency, setup cost.
3. Decide real DOC vs double and justify the decision.
4. Select the double type using the decision rule.
5. Define the double contract:
	- expected inputs,
	- expected response/effect,
	- interaction expectations (if applicable).
6. Design the test with dependency injection/test seams.
7. Verify SUT result and/or DOC interactions according to chosen type.
8. Review test fragility against internal SUT refactoring.
9. Recommend complementary coverage (mini-integration) when false-green risk exists.

## Anti-Patterns To Avoid (MUST)

- Mocking everything without criteria (over-specifying interactions).
- Verifying irrelevant interactions for the target behavior.
- Using a mock when a simple stub is sufficient.
- Keeping fakes that diverge from real behavior without documentation.
- Claiming green with doubles without validating expectation-correctness risk.

## Output Contract (MUST)

Agent output MUST include:

- DOC inventory per case.
- Decision per DOC: real vs double, with rationale.
- Double type chosen per DOC (stub/mock/spy/dummy/fake).
- Double contract per method (input -> response/expectation).
- Fragility risks and proposed mitigations.
- Recommended complementary coverage note (when relevant).

## Completion Criteria

- Every used double has a clear justification.
- Assertions are aligned with the selected double type.
- False-green and fragility risks are explicit.
- The test remains fast, repeatable, independent, and automatable.

