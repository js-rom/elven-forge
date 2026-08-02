# Elven-Forge

An agent system built on **Unified Process (UP)** for iterative, incremental, specification-driven development. Agents work in **pair programming** mode (driver/navigator) and persist artifacts in `openspec/artifacts/` as the single source of truth.

---

## Getting Started

### 1. Prerequisites

- A project with a detectable stack (Spring Boot + Vaadin, Node.js, Python, etc.).
- The agent system lives in `.agents/`. No external installation required.

### 2. Initialize the Project

Run the initialization command from the project root:

```
/up-init
```

This launches the `init` skill, which in order:

1. **Detects the tech stack** (language, frameworks, testing, CI).
2. **Copies the OpenSpec seed** from `.agents/skills/storage/openspec/` to `openspec/`, creating the schema, template, and instruction structure.
3. **Builds the skill registry** at `.atl/skill-registry.md`, scanning all available skills and project conventions.
4. **Returns a summary** with the detected stack and the recommended next step.

If `openspec/` already exists, the seed is not overwritten.

### 3. Launch the First Phase

Once the project is initialized, launch the inception phase:

```
/up-inception <idea to develop>
```

This starts the full UP flow in pair programming mode. From here, the agent (driver) guides you step by step while you (navigator) validate every decision.

---

## The Complete Flow

### Unified Process Phases

The system follows the four UP phases in order:

```
inception → elaboration → construction → transition
```

| Phase | Purpose | Typical Duration |
|---|---|---|
| **Inception** | Establish a common vision, scope, and viability. ~10% of use cases in detail. | 1 iteration |
| **Elaboration** | Build the core architecture, define most requirements, reduce risks. Programming from day one. | Multiple iterations (E1..En) |
| **Construction** | Implement the rest of the system on the stabilized architecture. | Multiple iterations |
| **Transition** | Delivery, migration, training, and stabilization. | 1-2 iterations |

The system currently implements **inception** and **elaboration** in full.

### Inside Each Phase: Steps with Approval Gates

Each phase is divided into numbered steps. The agent does not advance without explicit approval:

```
Driver (agent)   →  proposes a step
Navigator (you)  →  review, ask questions, correct
Navigator (you)  →  OK PASO N
Driver (agent)   →  persist artifacts, move to the next step
```

Example of the elaboration phase (18 steps):

```
✅ Step 1  — Iteration Plan
✅ Step 2  — Domain Model
✅ Step 3  — System Sequence Diagrams
✅ Step 4  — Operation Contracts
⬜ Step 5  — UI Design
⬜ Step 6  — Reports Design (TBD)
⬜ Step 7  — Architectural Analysis
⬜ Step 8  — Logical View (packages)
⬜ Step 9A — Domain-to-Design Transition
⬜ Step 9B — Scenario Design (sequence + class)
⬜ Step 10 — Use Case Realization
⬜ Step 11 — Reviewer pass
⬜ Step 12 — Data Model + JPA Mapping
⬜ Step 13 — SW Architecture Document
⬜ Step 14 — TDD (Code + Tests)
⬜ Step 15 — Refine Requirements Ranking
⬜ Step 16 — Use Case fully dressed (10%)
⬜ Step 17 — Cycle close
⬜ Step 18 — Phase close
```

Each step consumes artifacts from previous steps and produces its own artifacts, always with traceability between them.

### Artifacts and Disciplines

Artifacts are organized by UP disciplines under `openspec/artifacts/{domain}/`:

```
01 Business Modeling/     ← Domain Model
02 Requirements/          ← Vision, Use Cases, SSDs, Op. Contracts, Supplementary Spec, Glossary
03 Design/                ← Logical View, Data Model, UI, SW Architecture Document
04 Implementation/        ← Source code (tracked by git, not by artifacts)
05 Test/                  ← Test Plan, automated tests
06 Deployment/            ← Deployment configuration
07 Configuration & Change Management/
08 Project Management/    ← Iteration Plan, Requirements Ranking
09 Environment/           ← Tools, standards
```

Each artifact's state is tracked in `openspec/state.yaml` (in progress, approved, persisted).

### Persistence Mode: master-only

No iteration folders or deltas are created. All artifacts are persisted directly at their master paths under `openspec/artifacts/{domain}/`. When an artifact is refined in a later iteration, the same file is edited. Change history is recorded in the artifact's own Revision History.

### Day-to-Day Usage

**Starting a new project:**

```
/up-init
/up-inception <topic>
```

**Continuing an elaboration in progress:**

The system automatically detects state from `openspec/state.yaml`. Just resume the conversation with the agent. The step progress display shows you exactly where you left off.

**During a step:**

- The agent proposes a draft. Review it, ask questions, request changes.
- When satisfied: `OK PASO N`.
- The agent persists the artifacts and displays the next step.

**Write rules:**

- During analysis/design steps, the agent **does not write files** until approval is received.
- The exception is step 14 (TDD), where tests and code are written after `OK PASO 14 IMPLEMENTAR`.

### Available Skills

Each design discipline has its own skill loaded on demand by the orchestrator:

| Skill | Discipline |
|---|---|
| `up-inception` | Full inception phase |
| `up-elaboration` | Full elaboration phase |
| `architectural-analysis` | FURPS+ analysis, architectural factors |
| `architectural-design` | Architecture decisions, styles, tactics |
| `packages-logical-view` | Logical view: packages, subsystems, layers |
| `design-principles` | SOLID, GRASP, GoF, cohesion/coupling |
| `sequence-diagram` | UML sequence diagrams (SSD and DSD) |
| `class-diagram` | UML class diagrams |
| `data-model` | Physical data model (PlantUML, UML Data Model) |
| `jpa-mapping` | JPA mapping from physical model |
| `ui-design` | Design system, visual specs, Vaadin mapping |
| `tdd` | Test-Driven Development |
| `test-cases` | Test case selection |
| `unit-testing` | Unit test quality criteria |
| `mocks` | Test doubles (stub, mock, spy, dummy, fake) |
| `software-architecture-document` | Architecture document (4+1 views) |
| `create-spring-boot-java-project` | Spring Boot project skeleton |
| `create-spring-boot-vaadin-project` | Vaadin project skeleton |
| `java-junit` | JUnit 5 best practices |
| `java-springboot` | Spring Boot best practices |
| `storage` | Artifact persistence |
| `skill-registry` | Skill registration and scanning |
| `init` | SDD initialization |
| `vaadin-orchestrator` | Vaadin 25 component gateway |

### Quick Glossary

| Term | Meaning |
|---|---|
| **Driver** | The agent — proposes, drafts, executes. |
| **Navigator** | The user — reviews, corrects, approves. |
| **OK PASO N** | Approval token to advance to the next step. |
| **Artifact** | Document or diagram produced in a step (Domain Model, SSD, etc.). |
| **Discipline** | UP activity area (Business Modeling, Requirements, Design, etc.). |
| **Iteration** | Timeboxed cycle within a phase. In elaboration there are N iterations (E1..En). |
| **Cycle** | Synonym for iteration. Closing a cycle does NOT close the phase. |
| **Master-only** | Persistence mode without iteration folders. One file per artifact. |
| **state.yaml** | File tracking current phase progress (current step, approved steps, artifacts). |
