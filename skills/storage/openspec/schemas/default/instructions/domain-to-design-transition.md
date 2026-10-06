# Domain-to-Design Transition Instructions

## Purpose

Bridge the conceptual Domain Model (business reality) to the software Design Model by producing an explicit, auditable transformation contract. Every design decision must be traceable to a domain concept or an operation contract postcondition.

This step closes the gap between "what the domain is" (steps 2-4) and "how the software realizes it" (step 9B). It does NOT produce sequence or class diagrams.

## Required Inputs

- Domain Model from step 2 (conceptual classes, attributes, associations, invariants, business rules).
- System Sequence Diagrams from step 3 (system operations per scenario).
- Operation Contracts from step 4 (postconditions in domain vocabulary).
- Logical View packages from step 8 (package boundaries, layer rules, dependency direction).
- Supplementary Specification and Glossary.

## Mandatory Workflow (Pair Programming)

The agent MUST process all scenarios in scope together in this step, producing one unified transformation contract.

1. Build scenario queue from the approved iteration plan.
2. Produce the Domain-to-Software Transformation Map.
3. Assign responsibilities and build the Responsibility Assignment Matrix.
4. Build the Postcondition Traceability Matrix.
5. Identify pattern candidates.
6. Document transformation rationale.

### Execution Mode (MANDATORY)

- Agent role: Driver.
- User role: Navigator.
- At each sub-step, the agent proposes and applies concrete changes, then asks/records navigator feedback before moving to the next sub-step.

## Output Sections (MUST produce all five)

### 1. Domain-to-Software Transformation Map

For every domain concept referenced by the scenarios in scope, produce a table:

| Domain Concept | Software Class/Interface | Divergence | Rationale |
|---|---|---|---|
| `Workday` | `Workday` | None | Direct mapping |
| `SchedulePolicyVersion` | `SchedulePolicy.Memento` | Renamed, pattern applied | Memento captures snapshot semantics; domain name was a hint |
| `/effectiveState` | `Workday.computeEffectiveState()` | Attribute → method | Computed value, not stored; derived attribute becomes computation |

Rules:
- MUST map every domain class, attribute, and association used in scope.
- MUST note every divergence (rename, split, merge, attribute→method, association→reference) with explicit rationale.
- SHOULD keep software names close to domain names unless a clear design reason justifies divergence.

### 2. Responsibility Assignment Matrix

Assign knowing/doing responsibilities to each software class using Information Expert:

| Software Class | Knowing Responsibilities | Doing Responsibilities | Driven By |
|---|---|---|---|
| `Workday` | its events, current state | compute effective state, compute total work time | I19, I20 postconditions |
| `SchedulePolicy.Memento` | modality, configs at snapshot time | — | I41 postcondition |

Rules:
- MUST assign responsibilities based on Operation Contract postconditions as the primary driver.
- MUST use Information Expert: assign to the class that has the information needed.
- MUST distinguish knowing (what it knows) from doing (what it does).

### 3. Postcondition Traceability Matrix

Map every Operation Contract postcondition to the software design element(s) that will satisfy it:

| OC Ref | Postcondition | Satisfied By | Status |
|---|---|---|---|
| UC01-OP1-PC1 | A new `TimeEvent` was created | `Workday.recordEvent()` → `TimeEvent` constructor | Assigned |
| UC03-OP1-PC3 | `Workday.effectiveState` changed | `Workday.computeEffectiveState()` | Assigned |
| UC12-OP1-PC4 | New `SchedulePolicyVersion` created | `SchedulePolicy.createMemento()` → `Memento` constructor | Assigned |

Rules:
- MUST cover every postcondition from every Operation Contract in scope.
- MUST mark as TBD any postcondition that cannot yet be assigned, with a rationale.
- MUST NOT leave postconditions unaddressed without explicit acknowledgment.

### 4. Pattern Candidate List

Identify design hotspots and propose pattern candidates:

| Hotspot | Domain Evidence | Candidate Pattern | Intent Fit | Participant Mapping |
|---|---|---|---|---|
| Policy versioning | `SchedulePolicyVersion` as immutable snapshot | Memento | Captures state snapshot without exposing internals | Originator: `SchedulePolicy`, Memento: `SchedulePolicy.Memento`, Caretaker: `SchedulePolicyRegistry` |
| Workday state machine | `WorkdayState` enum + transition table | State | Replaces conditional state logic with explicit state objects | Context: `Workday`, States: `SinFichar`, `EnJornada`, etc. |

Rules:
- MUST provide problem evidence from the domain model, not from implementation assumptions.
- MUST map pattern roles to concrete domain concepts.
- MUST explain why the pattern intent fits the hotspot.

### 5. Transformation Rationale

Document decisions where the software model diverges from the domain model:

- What changed and why.
- What design principle justifies the divergence (Information Expert, Low Coupling, etc.).
- What trade-off is accepted.

## Modeling Rules (MUST / MUST NOT)

- MUST use Operation Contract postconditions as the primary driver for responsibility assignment.
- MUST keep the transformation map at the class-and-responsibility level.
- MUST NOT design method signatures, algorithm steps, or implementation details.
- MUST NOT produce sequence diagrams or class diagram deltas in this step.
- MUST preserve traceability from every design element back to a domain concept or postcondition.
- If a domain concept has no clear software counterpart, MUST mark it and explain why.
- If a postcondition cannot be satisfied by the current package structure, MUST flag it before proceeding.

## Output Contract (MUST)

The produced artifact MUST contain:

- Domain-to-Software Transformation Map (table).
- Responsibility Assignment Matrix (table).
- Postcondition Traceability Matrix (table).
- Pattern Candidate List (table).
- Transformation Rationale (prose).

## Validation Checklist (MUST run before finish)

1. Is every domain concept in scope mapped to a software class/interface?
2. Is every divergence from the domain model explicitly justified?
3. Does every software class have at least one responsibility assigned?
4. Is every Operation Contract postcondition covered in the traceability matrix?
5. Are unassigned postconditions explicitly marked as TBD with rationale?
6. Does every pattern candidate have problem evidence from the domain model?
7. Are pattern participants mapped to domain concepts?
8. Is the transformation consistent with the package boundaries from step 8?
9. Is traceability preserved from design elements back to domain concepts?
10. Are method signatures, algorithms, and implementation details absent?
