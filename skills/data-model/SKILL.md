---
name: data-model
description: Create and evolve the physical data model in PlantUML using the UML Data Model profile and persistence mapping heuristics.
license: MIT
metadata:
	author: js-rom
	version: "1.0"
---

## Purpose

Design and refine the master physical data model for the current elaboration iteration.

The result must stay technology-agnostic at framework level: capture tables, columns, keys, constraints, ownership, and persistence trade-offs without leaking JPA annotations, Java class design, repository APIs, or provider-specific details.

## Required Inputs

- Domain Model.
- Use cases, SSDs, and Operation Contracts that introduce or change persistence behavior.
- Logical View and Use Case Realization when they already exist.
- Supplementary Specification.
- Glossary.
- Existing master artifacts, if they already exist:
	- `openspec/artifacts/{domain}/03 Design/Data Model/data-model.plantuml`
	- `openspec/artifacts/{domain}/03 Design/Data Model/jpa-mapping.md`

## Source Baseline

Use these distilled rules as the working contract for this skill:

### UML Data Model Profile

- Use UML class-diagram notation as the base notation for physical data modeling.
- Indicate the model type explicitly as `<<Physical Data Model>>`.
- Indicate storage type explicitly as `<<Relational Database>>` when the target is relational.
- Model tables, associative tables, lookup tables, views, and indexes with class boxes when they matter to the design.
- Model columns with standard attribute notation.
- Model keys with the compact stereotypes `<<PK>>`, `<<FK>>`, and `<<AK>>`.
- Model nullability with `<<Not Null>>` or `<<Nullable>>` only when it adds signal.
- Use UML constraints or concise notes for relevant integrity rules.
- Use dependencies from views or indexes to the tables they depend on only when the dependency matters and the diagram remains readable.
- Keep replication, sizing, archival, access-control, and other operational detail out of the diagram unless it is architecturally significant.

### Relationship Notation (PlantUML)

Model every persistent relationship between tables using the correct UML symbol, explicit cardinality on both ends, and a short directional label.

| Semantic | PlantUML symbol | Example                   |
|----------|-----------------|---------------------------|
| Composition | `*--` (filled diamond) | `WorkDay "1" *-- "0..*" CorrectionRequest : owns` |
| Aggregation | `o--` (hollow diamond) | `Department "1" o-- "0..*" Employee : groups` |
| Association  | `--`  (plain line)      | `Employee "0..1" -- "0..*" WorkDay : records` |

- The diamond (filled or hollow) must be placed on the owner/whole/aggregate side.
- Cardinality (e.g. `"1"`, `"0..1"`, `"0..*"`, `"*"`, `"1..*"`) must be explicit on both ends.
- Every relationship line must carry a short label describing the navigability or domain role (e.g. `: owns`, `: references`, `: groups`).
- Associative tables (aggregation N:M) must use two aggregation lines from the associative table to each side.

### Persistence Mapping Heuristics

- Standalone object with no relationship: prefer one table per persisted concept, one row per object.
- Composition `1:1`: prefer embedded columns in the owner table when lifecycle is shared and access locality matters; split into a dependent table only when sparsity, governance, or schema reuse justifies it.
- Composition `1:N`: do not serialize child collections into blobs for the default design; prefer explicit child storage. If the source object model is intentionally unidirectional, prefer a design that preserves an acyclic software model and document the trade-off.
- Aggregation `N:1`: store the foreign key on the `N` side.
- Aggregation `N:N`: represent the relationship with an associative table.
- Inheritance: make the chosen relational strategy explicit and explain why.
- Document-style embedding is a trade-off reference only; mention it in rationale when it competes with a relational option, but do not let it blur the relational physical model.

## Mandatory Pair Programming Workflow

This skill must always run in driver/navigator mode.

1. Identify the persisted concepts and persistence-affecting deltas in the current iteration.
2. Decide which concepts require new tables, changed tables, lookup tables, or associative tables.
3. For each relevant relationship, decide ownership, key placement, nullability, and lifecycle semantics.
4. Draft or refine the master physical data model in PlantUML.
5. Summarize the current iteration delta in plain language for handoff to the JPA mapping skill.
6. Review the diagram with the user for naming, readability, and consistency with the domain language.

## Modeling Rules (MUST / MUST NOT)

- MUST start from the template `../storage/openspec/schemas/default/templates/plantuml.plantuml`.
- MUST maintain a single master diagram named `data-model.plantuml`.
- MUST evolve that master file incrementally across elaboration iterations; do not create one PlantUML file per iteration.
- MUST use PlantUML syntax.
- MUST add an explicit title or note identifying the diagram as `<<Physical Data Model>>` and `<<Relational Database>>`.
- MUST make every persisted table key explicit.
- MUST keep composite keys unambiguous; use tagged-value style notes such as `{key = PK, order = 1}` only when the order of columns matters.
- MUST prefer concise diagrams: keep clutter out of the drawing and move bulky rationale into notes handed to the JPA mapping artifact.
- MUST align table and column names with domain language unless there is a concrete technical reason not to.
- MUST mark deprecated or replacement structures only when they are part of an active refactor delta.
- MUST NOT include JPA annotations, Java collection types, repository names, service names, or package names.
- MUST NOT keep two competing physical realizations in the same master diagram; choose one and explain the decision.
- MUST render every persistent relationship with the correct PlantUML symbol (`*--` composition, `o--` aggregation, `--` association), explicit cardinality on both ends, and a short directional label.
- MUST NOT over-model indexes, triggers, views, or access-control rules when they are not needed for the current iteration.

## Translation Guide

### Simple persisted concept

- Model one table.
- Add the candidate columns required by the use cases and constraints.
- Mark the primary key explicitly.

### Composition

- `1:1`: choose embedded columns in the owner table by default.
- `1:N`: prefer explicit child storage and show the ownership structure clearly.
- When lifecycle is fully dependent, capture the dependency in the relationship choice and in the rationale.

### Aggregation

- `N:1`: use a foreign key column on the many side.
- `N:N`: create an associative table and make the foreign keys explicit.

### Inheritance

- Decide whether the hierarchy should collapse into one table or split across joined tables.
- Record the trade-off explicitly for downstream JPA mapping.

## Output Contract

Produce:

1. One updated PlantUML master diagram for `data-model.plantuml`.
2. A concise delta summary for the current iteration:
	 - added structures,
	 - changed structures,
	 - deprecated structures,
	 - unresolved data decisions.
3. A handoff note for JPA mapping describing ownership, lifecycle, key strategy, and non-obvious trade-offs.

If information is missing, mark it as `TBD` and continue.

## Validation Checklist

1. Does every persisted concept map to a table or an explicit rationale for not persisting it?
2. Does every table have a clearly identified primary key?
3. Are composite keys and foreign keys unambiguous?
4. Do composition and aggregation choices reflect lifecycle semantics?
5. Are associative tables explicit where required?
6. Does every relationship use the correct PlantUML symbol (`*--` for composition, `o--` for aggregation, `--` for association) with explicit cardinality on both ends and a label?
7. Is the diagram readable without JPA or Java implementation noise?
8. Does the delta preserve a master-model evolution instead of creating per-iteration fragments?
