# SW Architecture Document

- [Vision and Business Case](../02%20Requirements/vision.md)
- [Supplementary Specification](../02%20Requirements/supplementary-specification.md)
- [Use Case Model](../02%20Requirements/Use%20Case%20Model.md)
- [Domain Model](../01%20Business%20Modeling/Domain%20Model.md)

## 1. Scope and Architecture Drivers

- System scope: {{scope}}
- In-scope iteration goals: {{iteration-goals}}
- Out of scope: {{out-of-scope}}

### Key Drivers

{for driver in architecture-drivers}
- {{driver.name}}: {{driver.description}}
{end driver}

## 2. Significant Decisions and Rationale

{for decision in architecture-decisions}
### Decision {{decision.id}}: {{decision.title}}

- Context: {{decision.context}}
- Decision: {{decision.choice}}
- Rationale: {{decision.rationale}}
- Alternatives considered: {{decision.alternatives}}
- Consequences: {{decision.consequences}}
{end decision}

## 3. Architecture Overview

### Processing Elements

{for processing-element in processing-elements}
- {{processing-element.name}}: {{processing-element.responsibility}}
{end processing-element}

### Data Elements

{for data-element in data-elements}
- {{data-element.name}}: {{data-element.responsibility}}
{end data-element}

### Connectors

{for connector in connectors}
- {{connector.name}}: {{connector.type}} - {{connector.contract}}
{end connector}

```plantuml
/' High-level architecture overview with processing, data, and connectors '/
```

## 4. 4+1 Views

### 4.1 Use Case View

- Architecturally significant scenarios:
{for scenario in significant-scenarios}
	- {{scenario.name}}
{end scenario}

```plantuml
/' Use-case-driven architecture behavior (sequence/activity/state as needed) '/
```

### 4.2 Logical View

- Main packages: {{logical-packages}}
- Key interfaces: {{logical-interfaces}}

```plantuml
/' Package/component diagram for logical architecture '/
```

### 4.3 Development View

- Build/deployable units: {{development-units}}
- Versioning boundaries: {{versioning-boundaries}}

```plantuml
/' Component diagram for implementation/build structure '/
```

### 4.4 Process View

- Concurrency model: {{concurrency-model}}
- Synchronization strategy: {{synchronization-strategy}}

```plantuml
/' Runtime process/thread view '/
```

### 4.5 Physical View

- Deployment topology: {{deployment-topology}}
- Node constraints: {{node-constraints}}

```plantuml
/' Deployment view (nodes and runtime mapping) '/
```

## 5. Style and Pattern Decisions

### Evaluated Styles

{for style in evaluated-styles}
- {{style.name}}:
	- Context fit: {{style.context-fit}}
	- Constraints imposed: {{style.constraints}}
	- Quality impact: {{style.quality-impact}}
	- Status: {{style.status}} (selected/rejected)
{end style}

## 6. Package Principles and Dependency Governance

- ADP compliance (acyclic dependencies): {{adp-status}}
- SDP compliance (depends on stable packages): {{sdp-status}}
- SAP compliance (stable packages are abstract): {{sap-status}}
- CRP compliance (reused together): {{crp-status}}
- CCP compliance (change together): {{ccp-status}}
- REP compliance (release/reuse granularity): {{rep-status}}

### Dependency Rules

- Allowed dependencies: {{allowed-dependencies}}
- Forbidden dependencies: {{forbidden-dependencies}}
- Cycle break strategy: {{cycle-break-strategy}}
- Coupling notes (efferent/aferent): {{coupling-notes}}

```plantuml
/' Package dependency graph (must be acyclic) '/
```

## 7. Quality Attributes and Scenarios

### Priority Attributes

{for attribute in prioritized-quality-attributes}
- {{attribute.name}} (priority: {{attribute.priority}})
{end attribute}

### Quality Scenarios

{for scenario in quality-scenarios}
#### {{scenario.id}} - {{scenario.attribute}}

- Source: {{scenario.source}}
- Stimulus: {{scenario.stimulus}}
- Environment: {{scenario.environment}}
- Artifact: {{scenario.artifact}}
- Response: {{scenario.response}}
- Response measure: {{scenario.response-measure}}
{end scenario}

## 8. Risks, Trade-offs, and Technical Debt

{for risk in architecture-risks}
- {{risk.id}}: {{risk.description}}
	- Impact: {{risk.impact}}
	- Mitigation: {{risk.mitigation}}
{end risk}

## 9. Validation and Evolution Plan

- Validation approach: {{validation-approach}}
- Architecture fitness checks: {{fitness-checks}}
- Evolution strategy: {{evolution-strategy}}

## 10. Traceability Matrix

| Requirement / Attribute | View(s) | Decision(s) | Evidence |
|---|---|---|---|
| {{traceability-row-1}} | {{views-1}} | {{decisions-1}} | {{evidence-1}} |

## Validation Checklist

- [ ] Architecture drivers are explicit and prioritized
- [ ] Significant decisions include rationale and trade-offs
- [ ] Processing, data, and connector elements are explicit
- [ ] All 4+1 views are present
- [ ] Package principles (ADP, SDP, SAP, CRP, CCP, REP) are addressed
- [ ] Style selection is justified with context and quality impact
- [ ] Quality scenarios are measurable
- [ ] Risks and evolution strategy are explicit
- [ ] Traceability from requirements/attributes to views/decisions is explicit
