# Data Migration Planning Purpose

A release that changes the persistence schema, identity semantics, or data meaning requires a Data Migration Plan. It defines how data is transformed from the current state to the target schema defined by the physical data model and its JPA mapping.

## Instructions for the Agent

- Produce one Data Migration Plan when a release changes the database schema or data semantics.
- Persist the approved artifact under `06 Deployment/data-migration-plan.md`.
- Derive the target schema from the Data Model (`data-model.plantuml`) and the JPA Mapping (`jpa-mapping.md`).

### 1. Context and Objective

- Record the from/to versions, database, and owner. State why the migration is needed.

### 2. Source of Truth

- Reference the Data Model and JPA Mapping paths that define the target schema.

### 3. Affected Data

- Enumerate tables or collections and classify each change (new, renamed, dropped, transformed, backfilled).

### 4. Migration Steps

- Split steps into pre-deployment, deployment, and post-deployment phases. Name the script or command for each.

### 5. Validation

- Define checks that confirm data correctness and completeness (row counts, referential integrity).

### 6. Rollback and Risks

- Describe how to revert, including backup/restore points. Record risks with impact and mitigation.
