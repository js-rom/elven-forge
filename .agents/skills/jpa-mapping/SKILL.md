---
name: jpa-mapping
description: Map the technology-agnostic physical data model to an implementable Spring Data JPA design and rationale document.
license: MIT
metadata:
	author: js-rom
	version: "1.0"
---

## Purpose

Translate the current physical data model into a Spring Data JPA design that is implementable in a Spring Boot codebase.

This skill does not write Java code by default. Its output is the master markdown artifact that explains how the technology-agnostic physical model maps to JPA entities, embeddables, collections, identifiers, inheritance, and repository boundaries.

## Required Inputs

- The master physical data model `openspec/artifacts/{domain}/03 Design/Data Model/data-model.plantuml` or the draft produced in the current step.
- Domain Model.
- SSDs and Operation Contracts that impose persistence invariants.
- Logical View and Use Case Realization when they already exist.
- Existing Spring Boot conventions from the repository, when available.
- The template `templates/jpa-mapping.md`.
- The current master markdown artifact `openspec/artifacts/{domain}/03 Design/Data Model/jpa-mapping.md`, if it already exists.

## Source Baseline

Apply these distilled Spring Data JPA rules:

- Prefer the standard `jakarta.persistence` API, not provider-specific annotations, unless there is a justified exception.
- Every persisted entity needs `@Entity` and `@Id`.
- Use `@GeneratedValue` when the identifier strategy is surrogate and generated.
- Use `@Table` or `@Column` only when defaults are insufficient or when reserved words, nullability, length, uniqueness, or naming rules require control.
- Default enum mapping must be overridden to `@Enumerated(EnumType.STRING)` unless there is a very strong reason to accept ordinal persistence.
- Composition `1:1` chosen as embedded maps naturally to `@Embeddable` plus `@Embedded`.
- Composition `1:N` maps to `@OneToMany`; when lifecycle is owned by the parent, document `cascade = CascadeType.ALL` and `orphanRemoval = true`.
- Aggregation `N:1` maps to `@ManyToOne`.
- Aggregation `N:N` maps to `@ManyToMany` only for pure associations; if the relation has attributes, constraints, or behavior, prefer an explicit association entity.
- Collections of simple values map to `@ElementCollection`.
- Derived or non-persistent state maps to `@Transient`.
- Inheritance must explicitly choose between `@Inheritance(strategy = SINGLE_TABLE)` and `@Inheritance(strategy = JOINED)`, or use `@MappedSuperclass` when the base type should not have its own table.
- Repository design usually starts at aggregate roots with `JpaRepository<AggregateRoot, IdType>`.

## Mandatory Pair Programming Workflow

This skill must always run in driver/navigator mode.

1. Read the current physical model and identify every table, key, and relationship that must surface in JPA.
2. Propose entity boundaries, embeddables, association entities, and value collections.
3. Decide the annotation strategy for identifiers, relationships, inheritance, enums, and non-persistent fields.
4. Decide explicit naming overrides only where needed.
5. Record cascade, orphan-removal, and fetch decisions only when they are justified by lifecycle or use-case needs.
6. Update the master `jpa-mapping.md` artifact using the template structure.
7. Review with the user for consistency with the codebase and persistence intent.

## Execution Rules (MUST / MUST NOT)

- MUST load `templates/jpa-mapping.md` before drafting the artifact.
- MUST maintain a single master document named `jpa-mapping.md`.
- MUST append or refine iteration deltas in that master file; do not create one markdown file per iteration.
- MUST map from the physical data model; if a JPA decision requires changing the physical model, call out the mismatch explicitly.
- MUST explain every cascade choice.
- MUST explain every `@ManyToMany` choice and prefer an explicit association entity when the relation is more than a pure link.
- MUST default enums to `EnumType.STRING`.
- MUST call out column or table renames caused by reserved words or naming conventions.
- MUST distinguish clearly between entity, embeddable, element collection, association entity, and transient state.
- MUST keep the mapping vendor-neutral whenever JPA standard annotations are enough.
- MUST NOT generate code unless the caller explicitly asks for code.
- MUST NOT prescribe eager fetching as a default.
- MUST NOT use cascade remove in aggregation relationships.
- MUST NOT treat Lombok as a mandatory persistence rule; mention it only as a project convention if relevant.

## Output Contract

Produce one updated markdown artifact with:

1. Global mapping decisions.
2. A matrix that maps physical structures to JPA elements.
3. Relationship decisions, including ownership and lifecycle semantics.
4. Inheritance and value-object strategy.
5. Repository and query notes when they clarify the design.
6. An iteration delta log.
7. Open questions and pending risks.

If information is missing, mark it as `TBD` and continue.

## Validation Checklist

1. Does every physical table map to an entity, embeddable, collection table, join entity, or an explicit rationale?
2. Is identifier generation aligned with the physical key strategy?
3. Are composition and aggregation mapped with the correct JPA relationship type?
4. Are cascade and orphan-removal rules consistent with lifecycle semantics?
5. Are inheritance decisions explicit?
6. Are naming overrides limited to the cases that actually require them?
7. Does the artifact remain implementation-ready without becoming provider-specific code?
