# Deployment Planning Purpose

The Unified Process Transition phase moves a completed, verified increment into production. The Deployment Plan turns the Release Plan into a concrete, repeatable, and reversible set of steps for publishing the system to a target environment.

## Instructions for the Agent

- Produce one Deployment Plan per release that reaches the Transition phase.
- Persist the approved artifact under `06 Deployment/deployment-plan.md`.
- Base the plan on the Release Plan, the Deployment View, and the Data Migration Plan.

### 1. Context and Scope

- Record the release version, target environment, deployment window, and owner.
- Enumerate exactly what is deployed: application artifact, configuration, data, and infrastructure.

### 2. Prerequisites

- List the conditions that must hold before deployment: green build, passing tests, backups, and approvals.

### 3. Deployment Steps

- Write numbered, reversible steps. Mark parallel vs sequential execution and assign an owner to each.
- For every step, state the corresponding rollback action.

### 4. Data Migration

- Summarize the migration steps or reference the Data Migration Plan instead of duplicating it.

### 5. Verification

- Define smoke tests that confirm the deployment succeeded, with expected results.

### 6. Rollback

- Describe how to revert the full deployment, naming the exact artifacts and versions to restore.

### 7. Go / No-Go

- State explicit go and no-go criteria. Never leave the decision implicit.

### 8. Risks

- Capture risks with likelihood, impact, and mitigation. Note post-deployment actions (monitoring, communication, cleanup).
