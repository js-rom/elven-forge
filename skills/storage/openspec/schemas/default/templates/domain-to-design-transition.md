# Domain-to-Design Transition — {{iteration}}

- [Iteration Plan]({{iteration-plan-path}})
- [Domain Model]({{domain-model-path}})

## Scenario Queue

| # | Use Case | Scenario | SSD Ref | OC Ref |
|---|---|---|---|---|
| 1 | {{uc-name}} | {{scenario-name}} | {{ssd-ref}} | {{oc-ref}} |

## 1. Domain-to-Software Transformation Map

| Domain Concept | Software Class/Interface | Divergence | Rationale |
|---|---|---|---|
| {{domain-concept}} | {{software-class}} | {{none / renamed / split / merged / attribute-to-method}} | {{why}} |

## 2. Responsibility Assignment Matrix

| Software Class | Knowing Responsibilities | Doing Responsibilities | Driven By |
|---|---|---|---|
| {{class}} | {{what it knows}} | {{what it does}} | {{postcondition refs}} |

## 3. Postcondition Traceability Matrix

| OC Ref | Postcondition | Satisfied By | Status |
|---|---|---|---|
| {{oc-ref}} | {{postcondition-text}} | {{design-element}} | {{Assigned / TBD}} |

## 4. Pattern Candidate List

| Hotspot | Domain Evidence | Candidate Pattern | Intent Fit | Participant Mapping |
|---|---|---|---|---|
| {{hotspot}} | {{domain-evidence}} | {{pattern}} | {{why}} | {{roles → classes}} |

## 5. Transformation Rationale

<!-- Document each divergence from the domain model: what changed, why, which design principle justifies it, and what trade-off is accepted. -->

## Validation Checklist

- [ ] Every domain concept in scope mapped to a software class/interface
- [ ] Every divergence from the domain model explicitly justified
- [ ] Every software class has at least one responsibility assigned
- [ ] Every Operation Contract postcondition covered in the traceability matrix
- [ ] Unassigned postconditions explicitly marked as TBD with rationale
- [ ] Every pattern candidate has problem evidence from the domain model
- [ ] Pattern participants mapped to domain concepts
- [ ] Transformation consistent with package boundaries from step 8
- [ ] Traceability preserved from design elements back to domain concepts
- [ ] Method signatures, algorithms, and implementation details are absent
