## Operation Contracts Purpose

- Operation Contracts define the state changes of the domain caused by a system operation.
- They specify what must be true after the operation (postconditions), not how to implement it.

## Required Inputs

- Use Case text for the selected scenario.
- System Sequence Diagram (SSD) for that specific scenario.
- Domain Model classes, attributes, and associations.

## Mandatory Workflow (Pair Programming)

1. Select one use case scenario and its SSD.
2. Identify system operations from actor-to-system messages.
3. Create one operation-contract section per system operation.
4. Validate traceability from Use Case -> SSD -> Operation Contract.

### Execution Mode (MANDATORY)

- Agent role: Driver.
- User role: Navigator.
- The agent proposes and applies each step, then asks for feedback before continuing.

## Modeling Rules (MUST / MUST NOT)

- MUST create contracts only for system operations.
- MUST keep each operation-contract section tied to one specific scenario.
- MUST define postconditions in terms of domain state changes.
- MUST express postconditions using Domain Model vocabulary.
- SHOULD include preconditions only when non-obvious and relevant.
- MUST record created/deleted instances when applicable.
- MUST record association links created/removed when applicable.
- MUST record attribute value updates when applicable.
- MUST NOT include algorithm steps or UI behavior details.
- MUST NOT describe infrastructure/technical implementation details.

## Recommended Postcondition Patterns

- `instance created`: `A new <Class> instance was created.`
- `instance removed`: `The <Class> instance <id/ref> was removed.`
- `association formed`: `<ClassA> was associated with <ClassB>.`
- `association removed`: `Association between <ClassA> and <ClassB> was removed.`
- `attribute updated`: `<Class>.<attribute> changed from <old> to <new>.`

## Output Contract (MUST)

The artifact MUST include:

- Use case and scenario identification.
- One consolidated file per use case.
- One section per system operation.
- For each operation:
	- Operation name/signature (conceptual).
	- Cross references to use case step(s) and SSD message(s).
	- Preconditions (optional, if noteworthy).
	- Postconditions (mandatory).

## Storage Convention

- Persist each operation-contract artifact under:
	`02 Requirements/Operation Contracts/UC{{#}} {{use-case.name}} - Operation Contracts.md`

## Validation Checklist

1. Are operations extracted from SSD system events?
2. Is each operation-contract section tied to one specific scenario?
3. Are postconditions written in Domain Model terms?
4. Are creations/deletions/links/attribute updates captured when applicable?
5. Are algorithm/UI/infrastructure details excluded?
6. Is traceability to use case steps and SSD messages explicit?
7. Is file naming/path compliant with storage convention?
