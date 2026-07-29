---
name: packages-logical-view
description: Build the logical architecture view using UML packages, subsystems, and layers, with explicit dependency and requirements traceability.
license: MIT
metadata:
	author: js-rom
	version: "1.0"
---

## Purpose

Represent the large-scale organization of software into UML packages, subsystems, and layers.

A layer is a coarse-grained grouping of packages or subsystems with a cohesive responsibility for a major system concern.

## Scope

This skill focuses on logical organization only:

- Package structure.
- Subsystem boundaries.
- Layer definitions.
- Dependency direction rules.
- Traceability to requirements and design inputs.

## Design Concern Routing

- Use [../architectural-design/SKILL.md](../architectural-design/SKILL.md) for architecture design decisions and rationale.
- Use this skill to realize those decisions into logical-view structure and diagrams.

## Required Inputs

- Supplementary Specification (especially non-functional constraints).
- Technical memos for architecturally significant issues.
- Use Case Model and selected iteration use cases/scenarios.
- Domain Model.
- SSDs and Operation Contracts for architecturally significant scenarios.

## Mandatory Pair Programming Workflow

This skill must always run in pair-programming mode.

- Agent role: Driver.
- User role: Navigator.
- Cadence: Propose one step, request feedback, then continue.

### Step-by-Step Execution

1. Identify candidate packages, subsystems, and layers from architecture drivers and technical memos.
2. Define responsibilities and interfaces for each package/subsystem/layer.
3. Define dependency direction rules and forbidden dependencies.
4. Create UML package diagrams to show organization and dependencies.
5. Document traceability to requirements, use cases, SSDs, operation contracts, and technical memos.
6. Review and refine with the user to ensure alignment with architectural-design decisions.

## Modeling Rules (MUST / MUST NOT)

- MUST use PlantUML for package diagrams.
- SHOULD use PlantUML for subsystem and layer diagrams when useful.
- MUST use fully qualified names for packages and subsystems.
- MUST NOT use PlantUML aliases for packages or subsystems (no `as ...`).
- MUST reference dependencies using fully qualified package/subsystem names directly.
- MUST keep logical view at package/subsystem/layer level.
- MUST NOT include class-level design detail.
- MUST NOT include implementation code.
- MUST draw package diagrams at one hierarchy level at a time.
- MUST use separate diagrams for different layers/subsystems to avoid clutter.
- MUST include cross-references between diagrams and hierarchy levels.
- MUST make dependencies explicit and directionally clear.
- MUST draw a PlantUML dependency between two packages when at least one class in the source package has a dependency on at least one class in the target package.
- MUST interpret package dependency as an aggregation of class-level dependencies (for example: use, call, reference, import, or creation), while keeping the diagram at package/subsystem/layer level.

## File Naming Convention

- Diagram files MUST use fully qualified names:
	- `<fully.qualified.package>.packageDiagram.plantuml`
	- `<fully.qualified.subsystem>.packageDiagram.plantuml`
- Examples:
	- `com.mycompany.sales.packageDiagram.plantuml`
	- `com.mycompany.billing.packageDiagram.plantuml`

## Output Contract

Produce a Logical View Package with:

1. Logical view narrative (scope and organization principles).
2. Package catalog with responsibilities and key interfaces.
3. Subsystem definitions and boundaries.
4. Layer model and layer responsibility definitions.
5. UML package diagrams (and optional subsystem/layer diagrams).
6. Traceability matrix from packages/subsystems/layers to:
	 - Requirements and constraints
	 - Use cases/scenarios
	 - SSDs
	 - Operation contracts
	 - Technical memos

If information is missing, mark as TBD and continue.

## Validation Checklist

1. Are package/subsystem/layer boundaries explicit?
2. Are names fully qualified and consistent?
3. Are diagrams limited to one hierarchy level each?
4. Are dependency directions explicit and coherent?
5. Is class-level detail excluded?
6. Is traceability to requirements and architecture inputs explicit?
7. Is alignment with [../architectural-design/SKILL.md](../architectural-design/SKILL.md) explicit?