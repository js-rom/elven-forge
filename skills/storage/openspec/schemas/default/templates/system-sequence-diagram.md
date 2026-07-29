# System Sequence Diagram - UC{{#}} {{use-case.name}}

[Use Case](../use-cases/UC{{#}}%20{{use-case.name}}.md)

{for scenario in scenarios}

## Scenario {{#}}

- Use case: `UC{{#}} {{use-case.name}}`
- Scenario: `{{scenario.name}}`

```plantuml
@startuml
title SSD - UC{{#}} {{use-case.name}} - {{scenario.name}}

actor "{{primary-actor}}" as Actor
participant "System" as System

' Messages must map to scenario steps in order
Actor -> System: <system event 1>
System --> Actor: <response 1>

Actor -> System: <system event 2>
System --> Actor: <response 2>

' Optional alternate/exception path
alt <condition>
	Actor -> System: <alternate event>
	System --> Actor: <alternate response>
end

@enduml
```

## Traceability

- Scenario step(s): `<list of step numbers>`
- Notes: `<constraints, validations, timing assumptions>`

{end scenario}
