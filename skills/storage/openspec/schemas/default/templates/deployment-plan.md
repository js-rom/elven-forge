# Deployment Plan

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Deployment draft | {{date}} | First draft for the current deployment plan. To be refined during construction and transition. | {{author}} |
| | | | |

---

## Deployment Context

- **Release:** {{release-version}}
- **Target Environment:** {{target-environment}}
- **Date / Window:** {{deployment-date}} — {{deployment-window}}
- **Deployment Owner:** {{owner}}
- **Related Artifacts:** Deployment View, Release Plan, Data Migration Plan

> In the Unified Process, a deployment plan becomes concrete during the Transition phase and is rehearsed against a staging environment before production.

---

## Scope

<Describe what is being deployed in this release: the build artifact, configuration changes, and any data changes.>

| Item | Type | Version | Notes |
| :--- | :--- | :--- | :--- |
| <Artifact / Service> | <Application \| Config \| Data \| Infrastructure> | {{version}} | <Notes> |

---

## Prerequisites

<Checklist of conditions that must be true before the deployment can start (build green, tests passed, backups taken, approvals obtained, etc.).>

- [ ] <Prerequisite 1>
- [ ] <Prerequisite 2>
- [ ] <Prerequisite 3>

---

## Deployment Steps

<Numbered, reversible steps. Mark the ones that can be run in parallel vs sequentially, and note who executes each.>

| # | Step | Command / Action | Owner | Rollback |
| :--- | :--- | :--- | :--- | :--- |
| 1 | <Step> | <Command or action> | <Owner> | <Rollback action> |
| 2 | <Step> | <Command or action> | <Owner> | <Rollback action> |
| ... | ... | ... | ... | ... |

---

## Data Migration

<Summarize the data migration steps or reference the Data Migration Plan.>

---

## Verification (Smoke Tests)

<List the checks that confirm the deployment succeeded.>

| Check | Expected Result | Pass / Fail |
| :--- | :--- | :--- |
| <Health / smoke check> | <Expected> | |
| <Feature check> | <Expected> | |

---

## Rollback Plan

<Describe how to revert the deployment if it fails. Reference the exact artifacts/versions to restore.>

---

## Go / No-Go Criteria

- **Go:** <Conditions that authorize the deployment.>
- **No-Go:** <Conditions that halt or abort the deployment.>

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| <Risk> | <Low \| Medium \| High> | <Low \| Medium \| High> | <Mitigation> |

---

## Post-Deployment Actions

<Monitoring, cleanup, communication, and follow-up tasks after the deployment.>
