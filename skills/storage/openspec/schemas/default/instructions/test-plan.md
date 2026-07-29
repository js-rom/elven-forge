# Test Plan Purpose

The Test Plan captures the explicit output of Step 1 of the TDD loop before any RED-GREEN-REFACTOR cycle starts. It documents the reasoning used to select tests (factors, equivalence classes, boundaries, and combinatorial reductions), the agreed test list, the execution approval policy, and the explicit traceability that ties each test item to the iteration and design artifacts that define the approved implementation slice.

## Instructions for the Agent

### 1. Input Baseline

- Build the plan from the active use-case context and the selected scenario slice.
- If available, align with `Use Case Realization` and `Iteration Plan` artifacts.
- Produce one Test Plan artifact per elaboration iteration from TDD Step 1, before any `RED -> GREEN -> REFACTOR` cycle starts.
- Keep explicit traceability per test item to the selected implementation slice and its requirement/design sources.

### 2. Test Design Rationale

- Identify relevant factors for the scenario.
- Define valid and invalid equivalence classes.
- Define boundary values and include just-below/at/just-above cases when applicable.
- Apply combinatorial reduction (pairwise/orthogonal/explicit set) when combinations are large.
- Explain why each selected case is included and why excluded combinations are acceptable.

### 3. Agreed Test List (Step 1 Output)

- Persist the agreed test list as the formal output of Step 1.
- Each test item must include preconditions, trigger/input, and expected result.
- Include priority and rationale for each selected test item.

### 4. Traceability Requirements

- Each agreed test item must record explicit traceability to:
  - the `Iteration Plan` item or slice that authorizes the work,
  - the selected use case and scenario,
  - the relevant `Use Case Realization` section,
  - the `System Sequence Diagram` operation or extension being exercised,
  - the `Operation Contract` postcondition being validated.
- When the selected slice touches additional approved concerns, also record the relevant references for that test item:
  - `SW Architecture Document`, and when applicable `Architectural Analysis` or `Technical Memos`,
  - `Data Model` and `JPA Mapping`,
  - `Design System`, `State Visual Specs`, `Interaction Spec`, and `Vaadin Mapping`.
- When one of those optional concerns does not apply, record it as `N/A` instead of leaving the traceability ambiguous.

### 5. Approval and Execution Policy

- Record the chosen implementation mode:
  - `Guided mode`: per-case approval before RED.
  - `Automatic mode`: sequential execution of the agreed list (one case at a time, full `RED -> GREEN -> REFACTOR` per case) without per-case approval.
- Record approval evidence (message, token, or equivalent confirmation).

### 6. Quality and Scope Rules

- Keep the plan focused on behavior and verification intent, not on implementation details.
- Exclude infrastructure and algorithm details that do not affect test intent.
- If information is missing, keep sections and mark them as `TBD`.

## Storage Convention

- Persist the test plan artifact once per elaboration iteration under:
  - `05 Test/{{#}} {Iteration} Test plan.md`
- In this file name, `{{#}}` is the zero-padded numeric part of `{Iteration}` (for example `E1 -> 01`, `E11 -> 11`).

## Validation Checklist

1. Is the test scope clearly bounded (in/out of scope)?
2. Are factors, equivalence classes, and boundary values explicit?
3. Is combinatorial strategy stated and justified?
4. Does the agreed test list include rationale and expected results?
5. Is approval/execution mode documented with evidence?
6. Does each test item trace to the `Iteration Plan` item, use case/scenario, `Use Case Realization` section, SSD reference, and `Operation Contract` postcondition?
7. Are architecture, persistence, and UI references captured when applicable?
8. Is the storage path and file name compliant?
