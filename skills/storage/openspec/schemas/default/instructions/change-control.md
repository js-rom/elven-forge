# Change Control Purpose

The Change Control artifact defines how change requests are recorded, evaluated, approved, and traced to the artifacts they modify. It complements the Configuration Management Plan with the operational change-request lifecycle and log.

## Instructions for the Agent

- Produce one Change Control artifact per project (refined as changes are processed).
- Persist the approved artifact under `07 Configuration & CM/change-control.md`.

### 1. Purpose and Lifecycle

- Describe the change-request lifecycle and model its states as a PlantUML diagram.

### 2. Change Request Record

- Define the fields of a change request: ID, title, requester, date, priority, affected artifacts, status, decision, implementation, verification.

### 3. Change Log

- Maintain a running log of change requests with their current status and decision.

### 4. Traceability

- Explain how each change request links back to the requirements, use cases, and design artifacts it modifies.

### 5. Emergency Changes

- Define the accelerated hotfix process and the post-hoc documentation required.
