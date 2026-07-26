---
name: architectural-design
description: Design significant architecture decisions, styles, modularity rules, quality tactics, and trade-offs for the current iteration. 4+1 view documentation is explicitly out of scope and delegated to software-architecture-document.
license: MIT
metadata:
	author: js-rom
	version: "1.0"
---

## Purpose

Create or refine architecture design decisions for the current iteration at architecture level (packages/components/processes/deployment constraints), not class-level implementation.

## Scope

This skill owns architecture design decisions and rationale for:

- Architecture drivers and scope/context.
- Significant decisions and trade-offs.
- Style and pattern selection.
- Package principles and dependency governance.
- MVC and presentation architecture decisions.
- Quality attribute tactics and measurable scenarios.
- Risks, technical debt, and evolution strategy.

## Out of Scope (Delegated)

- Documenting architecture using 4+1 views.
- Writing the `4+1 Views` section in the SW Architecture Document.

These responsibilities belong to the `software-architecture-document` skill.

## Required Inputs

- Vision and Business Case.
- Supplementary Specification (especially non-functional constraints).
- Technical memos for architecturally significant issues.
- Use Case Model and selected iteration use cases/scenarios.
- Domain Model.
- SSDs and Operation Contracts for architecturally significant scenarios.
- Existing SW Architecture Document (if it exists).
- Current technology constraints, platform constraints, legacy constraints, and team/resource constraints.

## Mandatory Pair Programming Workflow

The agent MUST execute this flow in order.

1. Identify architecture drivers.
2. Define architecture scope and context.
3. Evaluate candidate styles and choose baseline style/hybrid.
4. Define package dependency and cohesion rules.
5. Define quality attribute tactics and measurable scenarios.
6. Record significant decisions, trade-offs, and risks.
7. Define architecture validation and evolution plan.
8. Prepare handoff package for software-architecture-document.

### Execution Mode (MANDATORY)

- Agent role: Driver.
- User role: Navigator.
- The agent proposes each step incrementally and requests feedback before moving to the next step.

## Architecture Rules (MUST / MUST NOT)

- MUST represent architecture using elements, externally visible properties, and relations between elements.
- MUST model three architecture element types: processing elements, data elements, and connectors.
- MUST describe interfaces and collaborations among components/subsystems.
- MUST separate logical layers from physical tiers.
- MUST keep traceability to use cases and quality attributes.
- MUST include constraints from non-functional requirements, technology, reusability, economics, and changeability.
- MUST include rationale for each significant decision.
- MUST NOT reduce architecture to class-level design patterns.
- MUST NOT include algorithmic implementation details.

## Package Principles and Modularity Rules (MUST)

The design MUST explicitly apply and assess:

- Acyclic Dependencies Principle: package dependency graph must be acyclic.
- Stable Dependencies Principle: dependencies should point toward stability.
- Stable Abstractions Principle: most stable packages should be most abstract.
- Common Reuse Principle: classes reused together should be packaged together.
- Common Closure Principle: classes that change together should be packaged together.
- Release/Reuse Equivalency Principle: reuse granularity equals release/version granularity.

The design MUST define dependency governance:

- Allowed dependency directions.
- Forbidden dependencies.
- Cycle breaking strategy.
- Coupling impact notes (efferent/afferent, at least qualitative; quantitative when available).

## Style and Pattern Selection Rules (MUST)

Evaluate style decisions against context and quality goals.

At minimum, evaluate relevant options from:

- Structural: Layered architecture.
- Persistence: Active Record, Row Data Gateway, Table Data Gateway/DAO, Data Mapper/ORM.
- Adaptable: Microkernel.
- Interaction:
	- Model/View/Controller
	- Model/View/Presenter with Presentation Model
	- Model/View/ViewModel
	- Model/View/Presenter with Passive View
	- Model/View/Presenter with Supervising Controller

For each considered style include:

- Context fit.
- Constraints imposed.
- Quality attributes improved/degraded.
- Why selected or rejected.

MUST distinguish:

- Architectural pattern/style (system level).
- Design pattern (subsystem/class level).

## MVC and Presentation Architecture Rules (MUST)

Define and compare MVC-family alternatives to support later documentation:

- Model/View/Controller.
- Evolution from classic MVC.
- Model/View/Presenter with Presentation Model.
- Model/View/ViewModel.
- Model/View/Presenter with Passive View.
- Model/View/Presenter with Supervising Controller.

Include:

- Responsibilities and boundaries.
- Testability implications.
- Selection rationale and rejected alternatives.

## Quality Attribute Rules (MUST)

Prioritize and define scenarios for:

1. Quality attributes
- Portability
- Changeability/adaptability
- Understandability
- Testability
- Usability
- Security
- Data integrity

2. Operational attributes
- Availability
- Hot update capability
- Reliability
- Recoverability
- Manageability/observability

3. Performance attributes
- Response time
- Elasticity
- Throughput/capacity

For top-priority attributes, define measurable quality scenarios:

- Source
- Stimulus
- Environment
- Artifact
- Response
- Response measure

## Output Contract (MUST)

Produce an Architecture Decision Package with:

1. Scope and Architecture Drivers.
2. Significant Decisions and Rationale.
3. Style and Pattern Decisions.
4. MVC and Presentation Architecture decisions.
5. Package Principles and Dependency Governance.
6. Quality Attributes and Scenarios.
7. Risks, Trade-offs, and Technical Debt.
8. Validation and Evolution Plan.

If information is missing, keep the section and mark as TBD.

## Handoff to software-architecture-document (MUST)

Pass the Architecture Decision Package as source of truth for final document assembly.

Do NOT produce or own the `4+1 Views` section.

## Anti-Patterns (MUST avoid)

- Confusing architecture with low-level class design.
- Mixing paradigms without explicit boundaries and rationale.
- Confusing logical layers with physical tiers.
- Omitting interfaces or connector semantics.
- Ignoring quality attributes and non-functional constraints.
- Choosing styles without context and trade-off analysis.
- Leaving dependency cycles unresolved.

## Validation Checklist (MUST run before finish)

1. Are architecture drivers explicit and prioritized?
2. Are significant decisions and rationale explicit?
3. Are processing, data, and connector elements clearly identified?
4. Are Acyclic Dependencies Principle, Stable Dependencies Principle, Stable Abstractions Principle, Common Reuse Principle, Common Closure Principle, and Release/Reuse Equivalency Principle addressed?
5. Are dependency directions/rules and cycle handling explicit?
6. Are style choices justified with context and trade-offs?
7. Are quality attributes prioritized and measurable scenarios defined?
8. Are risks and technical debt identified with mitigation direction?
9. Is traceability explicit from requirements to decisions?
10. Is 4+1 documentation excluded and delegated correctly?

