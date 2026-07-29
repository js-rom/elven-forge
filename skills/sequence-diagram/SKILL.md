---
name: sequence-diagram
description: Create UML sequence diagrams in PlantUML to model object interactions and message flow for design-level scenarios, based on Craig Larman's Applying UML and Patterns.
metadata:
  author: js-rom
  version: "1.0"
---

## Purpose

Create Design Sequence Diagrams (DSDs) in PlantUML to model software object interactions that fulfill a system operation. Based on the principles from Craig Larman's "Applying UML and Patterns."

A Design Sequence Diagram shows how software objects collaborate through message passing to satisfy the postconditions of an operation contract. It bridges the gap between System Sequence Diagrams (SSDs) — which show actor-system interaction at the boundary — and Design Class Diagrams (DCDs), which show static structure.

Key concepts from Larman:
- Interaction diagrams model dynamic behavior as object collaborations.
- Sequence diagrams emphasize time ordering of messages.
- Each SSD system operation expands into an interaction diagram showing domain-layer objects fulfilling the contract.
- The Controller pattern (GRASP) receives the system operation and delegates to domain objects.
- Information Expert drives message routing: send the message to the object that has the data.

## Required inputs

- System Sequence Diagram (SSD) for the scenario (entry point: system operation message).
- Operation Contracts for the system operations involved (postconditions to satisfy).
- Domain Model (conceptual classes as inspiration for software domain objects).
- Design Class Diagram (if available) for class names and relationships.
- Logical View package structure (for package-qualified object naming).
- Supplementary Specification constraints (security, auditing, performance, validation).
- Glossary terms for consistent domain naming.

## Design Concern Routing

- Use [../design-principles/SKILL.md](../design-principles/SKILL.md) for responsibility assignment (Information Expert, Controller, Low Coupling, High Cohesion) and pattern decisions.
- Use [../class-diagram/SKILL.md](../class-diagram/SKILL.md) to materialize the discovered classes and relationships into static structure.
- Use this skill to realize interaction flows and message-level design.

## Mandatory workflow (Driver/Navigator)

1. Start from the SSD system operation: identify the incoming message to the controller.
2. Identify the domain objects that must collaborate to fulfill each operation contract postcondition.
3. Assign responsibilities using Information Expert: who has the data needed to fulfill each sub-responsibility?
4. Draw lifelines for each participating object:
   - Controller (receives the system operation).
   - Domain objects (entities, value objects).
   - Pure fabrications when justified (services, factories).
5. Add messages in time order, from top to bottom, showing method calls and returns.
6. Use activation bars to show the period during which an object has focus of control.
7. Add interaction frames for structured control flow:
   - `loop` for repetition,
   - `alt/else` for conditional branching,
   - `opt` for optional fragments,
   - `ref` for referencing another sequence diagram.
8. Use `ref` frames to reference sub-diagrams for complex sub-interactions.
9. Validate that every operation contract postcondition is explicitly satisfied by the message flow.
10. Review and refine with the user.

## Execution rules (MUST / MUST NOT)

- MUST use PlantUML sequence diagram syntax (`@startuml` ... `@enduml`).
- MUST start each scenario DSD from the system operation message entering the controller.
- MUST treat SSD system operations as the entry point for the design sequence diagram.
- MUST show object lifelines for software objects, not the actor or the System boundary.
- MUST use activation bars to indicate object focus of control.
- MUST use synchronous messages (`->`) for method calls and return messages (`-->`) when they clarify responsibility completion.
- MUST use found messages (`[->`) for the initial system operation and lost messages (`->]`) for terminal responses when no specific receiver/sender lifeline exists.
- MUST use interaction frames for structured control logic: `loop`, `alt`, `opt`, `ref`.
- MUST name lifelines using the pattern `name : ClassName` or `: ClassName` for anonymous instances.
- MUST keep one scenario per diagram; do not merge main success and alternate flows into a single diagram.
- MUST validate that every operation contract postcondition is satisfied by explicit messages or combined message effects.
- MUST reflect Supplementary Specification constraints (audit logging, validation, authorization checks) as explicit messages or notes.
- MUST use consistent naming from the Domain Model and Glossary.
- MUST NOT include implementation detail (SQL, ORM calls, HTTP, framework internals).
- MUST NOT overload a diagram with too many objects; for complex collaboration, split into sub-diagrams using `ref`.
- MUST NOT use aliases that obscure domain meaning; prefer readable object names.
- MUST NOT contradict the operation contracts or omit required postconditions.
- MUST NOT use square brackets `[...]` as lifeline/participant names — `[` and `]` are reserved for PlantUML gate syntax (`[->`, `->]`). Use notes for exception types and self-calls for catch blocks.

## PlantUML Sequence Diagram Syntax

### Basic structure

```
@startuml
title DSD - UC{{#}} {{use-case.name}} - {{scenario.name}}

participant ": {{Controller}}" as C
participant ": {{EntityA}}" as EA
participant ": {{EntityB}}" as EB

[-> C : systemOperation(param)
activate C
C -> EA : domainMessage(param)
activate EA
EA --> C : result
deactivate EA
C -> EB : domainUpdate(data)
activate EB
EB --> C : result
deactivate EB
[<-- C : response
deactivate C

@enduml
```

### Interaction frames

```
@startuml
loop for each item
  C -> EA : processItem(item)
end

alt [condition A]
  C -> EB : handleCaseA()
else [condition B]
  C -> EB : handleCaseB()
end

opt [optional condition]
  C -> S : applyOptionalBehavior()
end

ref over C, EA, EB : UC{{#}} Sub-interaction Name
@enduml
```

### Object naming conventions

```
participant ": Sale"             // anonymous instance
participant "s : Sale"           // named instance
participant ": SaleController"   // controller (pure fabrication)
participant ": IInventoryService" // interface / abstraction
```

### Notes and constraints

```
note right of C : System operation:\nenterItem(upc, qty)
note over EA, EB : Postcondition:\nInstance created and\nassociated to parent
note left of EB #red : Constraint: audit-log every\nmodification
```

## File Naming Convention

- DSD files MUST follow this pattern:
  `DSD UC{{#}} {{use-case.name}} - S{{scenario.#}}.sequenceDiagram.plantuml`
- Storage path: `openspec/artifacts/{domain}/03 Design/Logical View/`
- Example: `DSD UC1 Register Sale - S1.sequenceDiagram.plantuml`
- Scenario numbering: S1 = main success, S2 = first alternate, S3 = second alternate, etc.

## Output contract

The generated output MUST include:

- One PlantUML block with `@startuml` and `@enduml`.
- Title identifying the use case and scenario.
- Lifelines for controller and domain objects (no actor, no System boundary).
- Messages in time order with activation bars for focus of control.
- Interaction frames for structured control flow where applicable.
- Notes documenting postcondition satisfaction and constraint compliance.
- Consistent naming aligned with Domain Model and Glossary.

## Validation checklist

1. Does the DSD start from the SSD system operation entering the controller?
2. Are all lifelines software objects (no actor, no `System` boundary lifeline)?
3. Are messages ordered chronologically from top to bottom?
4. Do activation bars correctly show focus of control?
5. Are return messages used where they clarify responsibility?
6. Are interaction frames used for loops, conditionals, and alternatives?
7. Is every operation contract postcondition satisfied by explicit messages?
8. Are Supplementary Specification constraints reflected (audit, validation, authorization)?
9. Are object names consistent with Domain Model and Glossary?
10. Is the diagram limited to one scenario only?
11. Is implementation detail avoided (no SQL, no framework internals)?
12. Is the file name compliant with the naming convention?
13. Is the `@startuml` / `@enduml` block valid PlantUML syntax?
