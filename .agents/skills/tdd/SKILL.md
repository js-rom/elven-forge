---
name: tdd
description: "Use when implementing changes with TDD and unit testing. Triggers: tdd, test-driven development, red green refactor, write failing test, test list, unit tests first, pruebas unitarias, desarrollo guiado por pruebas."
---

# TDD Skill

## Purpose

Apply TDD to implement behavior changes safely, keep existing behavior stable, and leave the code ready for the next change.
This skill controls cycle sequencing; test design and test-quality criteria MUST be applied invoking [unit-testing skill](../unit-testing/SKILL.md).


## Scope

Use this skill for:
- new behavior development,
- bug fixes,
- incremental refactors protected by tests,
- unit testing in red-green-refactor cycles.

Do not use this skill as a rule to write all tests upfront.

## Code Language Rule (MANDATORY)

- All production code and test code created or modified during TDD cycles MUST be written in English.
- This includes class, method, variable, and test names, plus inline code comments and assertion messages.
- If existing code uses another language, normalize touched code to English unless the user explicitly requests otherwise.

## Implementation Slice Contract (MANDATORY)

- When TDD runs as the implementation step of an approved analysis/design flow, load and obey the approved implementation slice artifacts:
	- `Iteration Plan` when available, as the scope and sequencing contract.
	- `Use Case Realization` for the selected scenario when available, as the primary design-to-code contract.
	- Referenced `Logical View` artifacts when available.
	- `System Sequence Diagrams` and `Operation Contracts` when available.
	- `SW Architecture Document` when available.
	- `Supplementary Specification` and `Glossary` when available.
	- If persistence is affected, `Data Model` and `JPA Mapping` when available.
	- If UI scope exists, `Design System`, `State Visual Specs`, `Interaction Spec`, and `Vaadin Mapping` when available.
	- If the slice implements an architecturally significant or risky concern, `Architectural Analysis` and `Technical Memos` when available.
- When TDD runs inside PASO 14 of `up-elaboration`, the artifact set above is mandatory according to the approved step contract.
- Use the `Iteration Plan` as a hard scope gate when available; do not implement behavior outside the approved iteration slice.
- Use the `Use Case Realization` as the primary scenario contract when available; derive the implementation slice from the scenario mapping, referenced design artifacts, and postcondition checklist.
- Keep `Test Plan` traceability explicit: each test item should trace to the scenario or use case and, when available, to the `Iteration Plan` item, `Use Case Realization` section, SSD reference, Operation Contract postcondition, and any relevant architecture, persistence, or UI artifacts.
- If TDD discovers a conflict, route it back to the owning artifact instead of silently improvising in code.

## UI Fidelity Contract (MANDATORY when UI scope exists)

- Treat approved `State Visual Specs` as the normative visual contract, approved `Interaction Spec` as the normative behavioral UI contract, and approved `Vaadin Mapping` as the normative technical implementation contract.
- For every approved UI state in scope, load the assets referenced by the approved `State Visual Specs`, including the linked HTML mock and screenshot/image under `openspec/artifacts/{domain}/03 Design/UI/screens/...` when available.
- The HTML mock referenced by an approved `State Visual Spec` is a mandatory rendering anchor for:
	- top-level layout composition,
	- section hierarchy,
	- CTA placement and priority,
	- dialog vs inline decisions,
	- list/table/card choice,
	- feedback placement,
	- token/class intent when expressed by the mock.
- The screenshot/image referenced by an approved `State Visual Spec` is supporting visual evidence for spacing, density, emphasis, and hierarchy when the HTML mock does not fully express them.
- Before the first edit of a UI slice, extract and report a `UI Fidelity Checklist` for the active slice that covers at least:
	- target view(s),
	- approved visual state ids in scope,
	- root layout regions,
	- visible/hidden components by state,
	- enabled/disabled actions by state,
	- required dialog vs inline decisions,
	- feedback surfaces,
	- primary vs secondary CTA hierarchy,
	- minimum CSS/theme hooks required by the design artifacts.
- Do not replace an approved modal with inline editing, or a card/list design with a generic grid, unless the owning UI artifacts are updated first.
- If the linked mock, screenshot, `State Visual Spec`, and `Vaadin Mapping` disagree, do not improvise in code:
	- prefer `State Visual Specs` as the normative visual contract,
	- prefer `Vaadin Mapping` as the normative implementation contract,
	- route unresolved conflicts back to the owning UI artifacts before coding past the mismatch.
- The first UI-related Test List items MUST cover at least:
	- structural fidelity of the root view,
	- one critical base state,
	- one critical alternate state.
- Before closing a UI slice, run at least one executable validation of the view layer; presenter-only or service-only evidence is insufficient for UI fidelity.

## TDD Loop (MANDATORY)

1. Create and maintain a **Test List invoking [test-cases skill](../test-cases/SKILL.md)**.
	- Before elaborating, load the artifact in progress: `Use Case Realization` for the selected scenario and the implementation-slice artifacts required by the contract above.
	- When `Iteration Plan` exists, the active Test List MUST stay within the approved iteration scope.
	- When `Use Case Realization` exists, derive the Test List from the scenario mapping, referenced design artifacts, and Operation Contract postconditions.
	- Record traceability for each Test List item at least to the scenario or use case and, when available, to the `Iteration Plan` item, `Use Case Realization` section, SSD reference, and Operation Contract postcondition.
	- When UI scope exists, record UI traceability for each relevant Test List item to:
		- `State Visual Spec.state_id`,
		- `Interaction Spec.transition.id`,
		- the relevant `Vaadin Mapping` section,
		- the linked HTML mock path under `openspec/artifacts/{domain}/03 Design/UI/screens/...` when applicable.
	- Build the Test List collaboratively with the user one by one, using test-cases skill strategies:
		- factor identification,
		- equivalence classes (valid/invalid),
		- boundary value analysis,
		- combinatorial reduction (orthogonal/pairwise) when needed,
		- white-box paths only when risk justifies them.
	- After the Test List and its rationale are agreed, ask the user explicitly:
		- `Do you want implementation one by one with prior user approval, or automatically without per-case approval?`
	- Then ask the user to choose execution mode:
		- `Guided mode`: implement one case at a time with explicit user approval before RED.
		- `Automatic mode`: implement the agreed list end-to-end **one case at a time** without per-case approval.
		- In `Automatic mode`, no per-case approval is required, but strict sequencing is still mandatory: one active case, one RED, one GREEN, one REFACTOR, then next case.
	- Record the selected mode before starting RED/GREEN cycles.
	- If the user does not choose explicitly, default to `Guided mode`.
	- After the Test List, its rationale, and the execution mode are agreed, the TDD skill MUST invoke the storage skill itself using the active Artifact Store Policy before any `RED -> GREEN -> REFACTOR` cycle begins.
	- Persist the `Test Plan` artifact under: `openspec/artifacts/{domain}/05 Test/{{#}} {Iteration} Test plan.md`.
	- In this file name, `{{#}}` is the zero-padded numeric part of `{Iteration}` (`E1 -> 01`, `E11 -> 11`).
	- When TDD runs inside PASO 14 of `up-elaboration`, persist the artifact immediately after `OK PASO 14` and before `OK PASO 14 IMPLEMENTAR`.
	- Build the artifact from the active schema template `test-plan.md`.
2. Pick exactly one item from the list and **write one concrete automated test**.
	- In `Guided mode`, the selected item MUST be explicitly approved by the user.
	- In `Automatic mode`, the selected item MUST come from the previously agreed Test List.
	- For test design/quality decisions, **invoke [unit-testing skill](../unit-testing/SKILL.md)**.
	- The test MUST include setup, invocation, and assertions.
	- The test code MUST be written in English.
	- Prefer starting from assertions and working backwards when useful.
3. **RED (mandatory): run the new test and capture failing evidence before any production code change**.
	- The cycle MUST stop if no failing evidence is produced.
	- Do NOT write production code for this item before RED evidence exists.
4. **GREEN (mandatory): make only the minimal change to pass**.
	- Change code so the new test and all previous tests pass.
	- Production code changes in this step MUST be written in English.
	- Capture executable GREEN evidence.
5. **REFACTOR (mandatory decision every cycle)**.
	- Refactor only while all tests are green.
	- Keep behavior unchanged.
	- If no refactor is needed, explicitly record `No refactor in this cycle` with rationale.
	- After refactor (or no-op), re-run relevant tests and capture post-refactor GREEN evidence.
	- For refactoring guidance, **invoke the [design-principles skill](../design-principles/SKILL.md) **.
6. Mark the completed test item as done.
	- If new scenarios are discovered, add them to Test List (as new pending items).
7. Repeat from step 2 until Test List is empty.

## TDD + Unit Testing Integration (MANDATORY)

- For every active Test List item, apply the quality model from [unit-testing skill](../unit-testing/SKILL.md): automated, self-verifying, repeatable, independent, and fast.
- Before closing each cycle, detect and fix relevant test anti-patterns defined in [unit-testing skill](../unit-testing/SKILL.md).
- Keep this skill focused on sequencing (`RED -> GREEN -> REFACTOR`) and use unit-testing skill as the design-quality gate for tests.
- If a required check needs real DB/network/process coupling, classify it as non-unit and track it outside this unit-level TDD loop.

## Strict Sequencing Rules (MANDATORY)

- Exactly one Test List item may be active at a time.
- Case agreement MUST happen before coding the test for that item.
- One cycle MUST be completed in this exact order: `RED -> GREEN -> REFACTOR`.
- Do NOT start the next Test List item until the current item has post-refactor GREEN evidence and is marked done.
- Do NOT batch multiple new tests in one cycle.
- Do NOT run RED for multiple pending items before completing GREEN for the active item.
- Do NOT batch broad production implementation ahead of RED evidence.
- In `Guided mode`, do NOT execute RED for a new case without explicit user approval of that case.
- In `Automatic mode`, do NOT execute RED for cases outside the previously agreed Test List.
- In `Automatic mode`, process the Test List as a strict loop: select next agreed item, complete full `RED -> GREEN -> REFACTOR`, mark done, then continue.

## Interface vs Implementation Split (MANDATORY)

- During test writing, prioritize interface/behavior design.
- During make-pass, prioritize the minimal behavior change.
- During refactor, improve implementation design.
- Never implement production behavior before explicit RED evidence for the active item.
- Do not mix these concerns in the same micro-step unless strictly necessary.

## Anti-Patterns to Avoid (MUST)

- Starting TDD without loading the artifacts that define the approved implementation slice.
- Implementing or testing behavior outside the approved iteration slice when `Iteration Plan` or `Use Case Realization` exists.
- Discovering design, persistence, UI, or architecture decisions ad hoc in code without routing the issue back to the owning artifacts.
- Implementing a generic CRUD or generic form layout when approved UI artifacts define a distinct shell, card, list, table, footer bar, or modal composition.
- Ignoring approved UI screen assets referenced by `State Visual Specs` and implementing only from summarized YAML text.
- Translating only labels and actions while skipping layout hierarchy, feedback placement, state visibility rules, and CTA hierarchy defined by the approved UI artifacts.
- Closing a UI slice with only service or presenter tests and no view-structure or state-rendering validation.
- Writing all tests from the Test List before running any passing cycle.
- Running RED for several Test List items before finishing GREEN for the first one.
- Selecting cases without explicit factor/equivalence/boundary reasoning.
- Ignoring combinatorial control when factors explode (pairwise/orthogonal alternatives).
- Advancing to implementation without respecting the selected approval policy:
	- `Guided mode`: explicit per-case user approval.
	- `Automatic mode`: prior user consensus of the complete Test List and rationale.
- Implementing production code before obtaining RED evidence for the active test.
- Moving to the next Test List item without finishing post-refactor GREEN for the current item.
- Merging multiple Test List items into one combined RED/GREEN step.
- Writing tests without assertions only to increase coverage.
- Deleting assertions to fake green tests.
- Copying computed actual values into expected values (self-fulfilling checks).
- Refactoring while still in the red-to-green step.
- Abstracting too early; duplication is a hint, not an immediate command.
- Refactoring beyond what the current session/change requires.

## Heuristics (SHOULD)

- Choose the next test to maximize learning and reduce risk early.
- Prioritize cases that cover new equivalence classes, critical boundaries, or high-risk factor interactions.
- Prefer starting implementation from the class or component with lower efferent coupling (fewer outgoing dependencies) to minimize ripple effects and simplify isolated tests.
- When the selected slice is UI-first, prefer aligning the root view composition and the dominant visible state before broader backend refinement, unless a blocking backend defect prevents rendering the approved state.
- When blocked by test order, reconsider sequencing.
- If a discovered scenario invalidates the current approach, prefer restarting from a better order over compounding complexity.
- Keep cycles short to maintain feedback speed and confidence.

## Working Protocol (Agent Behavior)

For each cycle, the agent MUST report:
- active implementation baseline (iteration, design, architecture, data, and UI artifacts used by the active slice when applicable),
- when UI scope exists, the `UI Fidelity Checklist` and the linked screen assets loaded for the active state(s),
- proposed case slice derived from factors/equivalence classes/boundaries,
- rationale for selecting that slice now,
- selected execution mode (`Guided mode` or `Automatic mode`) and confirmation source,
- in `Guided mode`, explicit approval request and user response for the active case,
- current Test List (or compact active+pending view),
- traceability of the active test item to the approved slice and design artifacts,
- selected next test and why,
- unit-testing quality gate status for the active test (execute/maintain/readability + anti-pattern check),
- failing test evidence (RED) captured before production code changes,
- minimal change made to pass,
- green evidence (new + existing tests),
- refactor summary or explicit no-op refactor rationale,
- post-refactor green evidence,
- updated Test List.

The agent MUST NOT claim progress without executable test evidence.

## Output Contract (MUST)

When finishing a task, output:
- implementation-baseline summary (artifacts used as scope and design contract),
- case-selection summary based on test-cases skill (factors, equivalence classes, boundaries, and reduction strategy),
- execution mode used (`Guided mode` or `Automatic mode`) and how approvals were handled,
- final Test List with all items status,
- traceability summary linking Test List items to iteration and design artifacts,
- cycle-by-cycle RED -> GREEN -> REFACTOR evidence summary,
- summary of how [unit-testing skill](../unit-testing/SKILL.md) criteria were applied (quality model + anti-pattern findings/fixes),
- list of tests added/updated,
- list of production code changes linked to test items,
- list of documentation artifacts updated or flagged by TDD findings,
- when UI scope exists, summary of UI fidelity checks executed and any deferred visual mismatches,
- confirmation that full relevant suite is green,
- concise note on refactors performed and why,
- follow-up risks or pending scenarios (if any).

## Completion Criteria

- Test List is empty (or explicitly deferred items are justified).
- New behavior works.
- Previously working behavior still works.
- Code remains ready for the next change.

