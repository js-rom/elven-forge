## System Sequence Diagram Purpose

- A System Sequence Diagram (SSD) models system events between external actors and the System under Design for one use case scenario.
- It focuses on actor-to-system messages and ordered responses at the system boundary.

## Required Inputs

- Use Case text for the selected scenario (main success scenario or extension).
- Use Case Model to confirm actors and system boundary.
- Supplementary constraints that affect interactions (security, validation, timeouts, etc.).

## Mandatory Workflow (Pair Programming)

1. Select one use case scenario to model.
2. Identify actors and system events from scenario steps.
3. Draw the SSD using PlantUML sequence syntax.
4. Validate traceability between messages and scenario steps.

### Execution Mode (MANDATORY)

- Agent role: Driver.
- User role: Navigator.
- The agent proposes and applies each step, then requests feedback before moving on.

## Modeling Rules (MUST / MUST NOT)

- MUST model system events for one single, specific scenario of one use case.
- MUST model only interactions crossing the system boundary.
- MUST represent the system as a single lifeline named `System`.
- MUST include actor lifelines as external participants.
- MUST keep message order consistent with scenario order.
- MUST label messages with domain language from the use case.
- MUST include alternate/exception messages when the selected scenario requires them.
- MUST NOT mix events from different scenarios in the same SSD.
- MUST NOT model internal design objects, repositories, services, or class-level collaborations.
- MUST NOT include implementation details (framework calls, SQL, HTTP plumbing) unless explicitly part of the domain interaction.

## Output Contract (MUST)

The artifact MUST include:

- A title identifying the use case and scenario.
- Exactly one scenario per SSD.
- A PlantUML sequence diagram block.
- Participants: actor(s) and `System`.
- Messages mapped to scenario steps.
- Optional notes for key validations or domain constraints.

## Storage Convention

- Persist each SSD under:
	`02 Requirements/SSDs/SSD UC{{#}} {{use-case.name}}.md`
- Keep one SSD file per use case scenario when scenarios are materially different.

## Validation Checklist

1. Is there exactly one `System` lifeline?
2. Are all external actors present?
3. Does each message map to a scenario step?
4. Is message order consistent with the scenario?
5. Are internal implementation objects excluded?
6. Is file naming/path compliant with storage convention?
7. Does the SSD model exactly one specific scenario (no mixed scenarios)?
