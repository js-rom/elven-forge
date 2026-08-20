# Release Planning Purpose

The Unified Process organizes delivery into releases, each grouping one or more completed iterations into a coherent, shippable increment. The Release Plan states what will ship, when, and with what traceability to completed use cases.

## Instructions for the Agent

- Produce one Release Plan per planned release.
- Persist the approved artifact under `06 Deployment/release-plan.md`.
- Scope must trace to use cases and iterations already completed (or explicitly committed for this release).

### 1. Context and Objective

- Record the release version, phase, target date, and release manager.
- State the release objective in one or two sentences.

### 2. Scope

- List use cases, scenarios, or features in scope with their completion status and originating iteration.

### 3. Build Artifact

- Identify the concrete build artifact, its version, and the build command that produces it.

### 4. Release Contents

- Enumerate deliverables: binaries, configuration, documentation, and database migrations.

### 5. Dependencies

- List external dependencies, approvals, and prior releases this release depends on.

### 6. Readiness Checklist

- Confirm the in-scope work is complete and tested, and that the deployment, migration, and rollback plans are approved.

### 7. Risks and Approval

- Record risks with owner and status, and capture the approval decision per stakeholder role.
