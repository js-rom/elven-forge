# Data Migration Plan

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Migration draft | {{date}} | First draft for the current data migration plan. | {{author}} |
| | | | |

---

## Migration Context

- **From Version:** {{from-version}}
- **To Version:** {{to-version}}
- **Database / Store:** {{database}}
- **Owner:** {{owner}}

> In the Unified Process, data migration is planned when a release changes the persistence schema, identity semantics, or data meaning.

---

## Objective

<Describe why the migration is needed and what it must achieve.>

---

## Source of Truth

<Reference the physical data model and JPA mapping that define the target schema.>

- **Data Model:** {{data-model-path}}
- **JPA Mapping:** {{jpa-mapping-path}}

---

## Affected Data

| Table / Collection | Change Type | Description |
| :--- | :--- | :--- |
| <Entity> | <New \| Renamed \| Dropped \| Transformed \| Backfilled> | <Description> |
| <Entity> | <New \| Renamed \| Dropped \| Transformed \| Backfilled> | <Description> |

---

## Migration Steps

<Numbered steps to transform the data. Distinguish pre-deployment, during-deployment, and post-deployment steps.>

| # | Phase | Step | Command / Script | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Pre-deployment | <Step> | <Script> | <Notes> |
| 2 | Deployment | <Step> | <Script> | <Notes> |
| 3 | Post-deployment | <Step> | <Script> | <Notes> |

---

## Validation

<List checks that confirm the migrated data is correct and complete.>

| Check | Expected Result | Actual Result |
| :--- | :--- | :--- |
| <Row counts / integrity check> | <Expected> | |
| <Referential integrity> | <Expected> | |

---

## Rollback

<Describe how to revert the data migration, including backup/restore points.>

---

## Risks

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| <Risk> | <Impact> | <Mitigation> |
