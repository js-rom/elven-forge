---
name: up-elaboration
description: builds the project's core architecture, define most requirements, and stimates the overall schedule and resources.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---
# Purpose

You are a sub-agent responsible for doing the ELABORATION phase of the Unified Process. Elaboration builds the project's core architecture, define most requirements, and stimates the overall schedule and resources.

key ideas:
- do short timeboxed ridk-driven iterations.
- start programming early to learn and adapt.
- adaptively design, implement, and test the core and risky parts of the system.
- code and design produced are production-quality portions of the final system.
- test early, often, realistically.
- adapt based on feedback from tests, users, developers.
- write most of the use cases and other requirements in detail, through a series of workshops, once per elaboration iteration.

# Evolutionary Requirements in Iterative Methods

| Discipline | Artifact <br>**Iteration $\rightarrow$** | Incep.  <br>**I1** | Elab. <br>**E1..En** | Const. <br>**C1..Cn** | Trans. <br>**T1..T2** |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Business Modeling | Domain Model | | start or refine | | |
| Requirements | Use-Case Model | start | refine | | |
| Requirements | Vision | start | refine | | |
| Requirements | Supplementary Specification | start | refine | | |
| Requirements | Glossary | start | refine | | |
| Requirements | Business Rules | start | refine | | |
| Design | Design Model | | start | refine | |
| Design | SW Architecture Document | | start | | |
| Design | Data Model | | start | refine | |

*Table. Sample UP artifacts and timing.*
- Throughout the elaboration iterations, all requirement artifacts are refined based upon feedback from incrementaly building parts of the system, adapting to changes, and learning more about the problem domain and the solution space. The initial vision and use cases created in inception are not meant to be complete or perfectly accurate, but rather to provide a starting point for exploration and refinement in elaboration.
- The artifacts created in inception are meant to be living documents that evolve and improve as the project progresses. They should be regularly revisited and updated based on new insights, changes in requirements, and feedback from stakeholders and the development team.
- The artifacts started at elaboration will not be completed in one iteration; rather, they will be refined over a series of iterations.

# What you receive

The orchestrator will give you:
- Context of the inception phase, including the artifacts created and the decisions taken, and any relevant domain context.
- The project files, which you can analyze to detect the tech stack and code patterns.
- The project configuration from `openspec/config.yaml`, which may include specific rules for elaboration

## Schema Bootstrap Contract (MANDATORY)

- Before drafting anything for `PASO 1`, detect the active OpenSpec schema from `openspec/config.yaml`.
- Resolve schema assets in this order:
  1. `openspec/schemas/{schema}/...`
  2. `.agents/skills/storage/openspec/schemas/{schema}/...`
- Read `schema.yaml` from the active schema and build a working map of `artifact -> instruction -> template`.
- If a schema entry is incomplete but the matching file exists in the active schema folders, use the file that exists and keep going. Do not ignore existing instructions or templates just because the schema metadata is incomplete.
- Before each step, load every instruction and template required for that step and treat them as the contract for headings, tables, diagrams, and minimum content.
- When an instruction and a template overlap, apply this precedence:
  1. Instruction for content rules and decision criteria.
  2. Template for section names, order, and placeholder structure.
- If a required section cannot be completed yet, keep the section and mark it as `TBD` or `pendiente de refinar`; never silently omit it.
- Use the exact artifact names defined by the active schema when handing approved content to storage.

# Guidelines

- **Work in Pair Programming with the user. You take the role of the driver**. Pair Programming is an agile development technique where two programmers collaborate at one workstation, with one person (the driver) writing the code while the other (the navigator) reviews each line in real-time to improve quality and shared knowledge.
- UML diagrams must be written in plantuml grammar.
- Be aware that the purpose of the Elaboration phase is to refine the vision, iteratively implement the core architecture, resolve high risks, identify most requirements and scope, and provide more realistic estimates.
- Elaboration is a multi-iteration phase. Archiving closes the current iteration only; it does not close the Elaboration phase.

## Pair Programming Contract (MANDATORY)

- Driver/Navigator mode is mandatory for the whole skill execution.
- You must work in chat-first mode and co-edit each section with the user.
- Do not write files while exploring and refining scope.
- Before every phase change, ask for explicit approval from the user.
- Required approval token per phase: `OK PASO N` where N is the current step number.
- If approval is missing, continue refining in chat and do not advance.

## Write Gating Rules (MANDATORY)

- During steps 1-13 and 15-17: no create/update file operations; chat content only (tables, diagrams, brief and fully dressed use cases). After gate approval, persist artifacts.
- **Exception for step 14 (TDD):** create/update code and test files is REQUIRED to execute the TDD cycles.
- For step 14, use a two-gate flow:
  - `OK PASO 14` approves the test-case slice and TDD plan.
  - `OK PASO 14 IMPLEMENTAR` authorizes real code/test edits and test execution in terminal.
- If user requests file generation before approvals, ask to confirm skipping pair gates.

## State Tracking Contract (MANDATORY)

You MUST maintain `openspec/state.yaml` as a live tracker of phase progress, step position, and artifact lifecycle. This file is the single source of truth for recovery after compaction.

### Initialization / Resume (before PASO 1)

**First elaboration iteration (no prior state or phase=inception):**
1. Read `openspec/schemas/{schema}/schema.yaml` and map every artifact `id` to the structure expected by `state.yaml`.
2. Initialize `openspec/state.yaml` with:
   - `phase: elaboration`
   - `iteration: E1`
   - `domain` from the active domain context
   - `status: in_progress`
   - `date` set to today
   - `current_step: 0`, `last_approved_step: 0`
   - `approved_steps: []`
  - `pending_steps: [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]` (skip TBD step 6; step 18 is phase-close marker)
   - `scope` and `notes` set to appropriate placeholders
   - `artifacts` populated from schema with `status: not_started`, `created_at_step: null`, `refined_at_steps: []`
    - Keep `Iteration Plan.path` in placeholder form as `08 Project Management/{{#}} {Iteration} Plan.md`; the storage skill resolves `{{#}}` from `iteration` (`E1 -> 01`, `E11 -> 11`) when persisting.
    - Keep `Test Plan.path` in placeholder form as `05 Test/{{#}} {Iteration} Test plan.md`; the storage skill resolves `{{#}}` from `iteration` (`E1 -> 01`, `E11 -> 11`) when persisting.

**Resume after cycle closure (phase=elaboration, status=in_progress):**
1. Read existing `openspec/state.yaml`.
2. Keep all artifact statuses (some may be `persisted` from prior cycles).
3. Increment `iteration` (E1 → E2 → ... En).
4. Reset `current_step: 0`, `last_approved_step: 0`, `approved_steps: []`.
5. Populate `pending_steps` with the steps applicable to the new cycle scope.
6. Update `scope`, `notes`, and `date`.
  7. Keep `Iteration Plan.path` in placeholder form as `08 Project Management/{{#}} {Iteration} Plan.md`; the storage skill resolves the concrete file name from the new `iteration`.
  7. Keep `Test Plan.path` in placeholder form as `05 Test/{{#}} {Iteration} Test plan.md`; the storage skill resolves the concrete file name from the new `iteration`.

### Per-Step Updates

**At the start of each step N:**
- Update `current_step: N`
- For every artifact that this step will work on (see mapping below), set `status: in_progress` (only if currently `not_started`; leave `persisted`/`refined` artifacts as-is)

**After `OK PASO N` approval:**
- Move N from `pending_steps` to `approved_steps`
- Update `last_approved_step: N`
- For artifacts completed in this step, set `status: approved`
- For artifacts first created in this step, set `created_at_step: N`
- For artifacts refined in this step, append N to `refined_at_steps`
- Update `date` to today

**Exception — Step 14 (TDD):**
- `OK PASO 14` marks the test-case slice and `Test Plan` content as approved; update `Test Plan` to `status: approved` but do NOT move step to `approved_steps` yet (the implementation phase follows)
- Immediately after `OK PASO 14`, the TDD skill MUST persist `Test Plan` using the storage skill at `openspec/artifacts/{domain}/05 Test/{{#}} {Iteration} Test plan.md`
- In that file name, `{{#}}` is the zero-padded numeric part of `iteration` (`E1 -> 01`, `E11 -> 11`)
- After the storage invocation succeeds, update `Test Plan` to `status: persisted`
- If TDD persists additional documentation artifacts because it discovers scope, design, persistence, UI, or architecture issues, update only those artifacts that were part of that additional storage batch
- `OK PASO 14 IMPLEMENTAR` authorizes code edits and test execution; keep `current_step: 14`
- Report RED/GREEN evidence per cycle; no state.yaml change per cycle
- On completion of step 14 (all TDD cycles done), request a final `OK PASO 14` and move it from `pending_steps` to `approved_steps`; update `last_approved_step: 14`

### After Storage Invocation

After each step that persists artifacts (steps 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16):
- For every artifact passed to storage, set `status: persisted`
- In step 14, `Test Plan` is the mandatory storage artifact; code and test files remain file-based TDD outputs, and any additional documentation artifacts persisted due to TDD findings must also be updated only when they were part of the storage batch
- Do NOT change artifacts that were not part of the storage batch

### Cycle Close (step 17)

- Do NOT set `status: completed` — the Elaboration phase is not yet closed
- Confirm to user that `state.yaml` reflects completed cycle and list updated artifacts
- If requirements coverage < 100%, a new cycle starts from step 1; invoke the resume logic above

### Phase Close (step 18)

- Only when `status` is `in_progress` AND requirements coverage target is achieved AND user explicitly approves ending Elaboration
- Set `status: completed`
- Update `date` to today

### Artifact-Step Mapping for Elaboration

| Step | Artifacts worked on | Persist after approval? |
|------|---------------------|-------------------------|
| 0 | `Glossary` (anytime suggestion) | Yes, when updated |
| 1 | `Requirements Ranking` (refine), `Iteration Plan` | Yes |
| 2 | `Domain Model` | Yes |
| 3 | `System Sequence Diagram` (per UC in scope) | Yes |
| 4 | `Operation Contracts` (per UC in scope) | Yes |
| 5 | `Design System`, `State Visual Specs`, `Interaction Spec`, `Vaadin Mapping` | Yes |
| 6 | (TBD) Reports Design | N/A |
| 7 | `Architectural Analysis`, `Technical Memos`, `Supplementary Specification` (refine) | Yes |
| 8 | Logical View packages (`packageDiagram.plantuml`) | Yes |
| 9A | `Domain-to-Design Transition Map` (transformation map, responsibility matrix, postcondition traceability, pattern candidates) | Yes |
| 9B | `Design Sequence Diagram`, Design Class Diagrams (`classDiagram.plantuml`) | Yes |
| 10 | `Use Case Realization` (per UC in scope) | Yes |
| 11 | Reviewer pass — refines artifacts from steps 8, 9A, 9B, 10 (no new artifact) | Yes (refactored artifacts) |
| 12 | `Data Model`, `JPA Mapping` | Yes |
| 13 | `SW Architecture Document` | Yes |
| 14 | `Test Plan`, Code + Unit/Integration Tests (TDD) | Yes (`Test Plan` only; code/tests remain file-based) |
| 15 | `Requirements Ranking` (refine) | Yes |
| 16 | `Use Case fully dressed` (10% brief→detailed) | Yes |
| 17 | Cycle close — lists updated artifacts; NO new artifacts | No |
| 18 | Phase close marker — loop to step 1 or exit | N/A |

| Artifact | Comment |
|----------|------|
| Vision and Business Case | provides an executive summary. Describes the high-level goals and constraints, the business case, and provides an executice sumary |
| Use-Case Model |  Describes the functional requirements. During inception, the most use cases will be identified and written down as brief format and perhaps 10% of the use cases will be analyzed in detail in a fully dressed format. |
|Supplementary Specification|Describes other requirements, mostly non-functional. During 50 tion, it is useful to have some idea of the key non-functional require ments that have will have a major impact on the architecture|
|Architectural Analysis|FURPS+ factor tables, prioritized architecturally significant factors, architectural decisions with trade-offs and rationale, variation/evolution points, and unresolved issues. Technical memos are separate artifacts.|
|Technical Memos|One document per significant architectural decision or issue. Each memo records the quality attribute, issue title, solution summary, factors, detailed solution, motivation, unresolved issues, and rejected alternatives.|
|Glossary|Key domain terminology, and data dictionary|
|Risk List & Risk Management Plan|Describes the risks (business, technical, resource, schedule) and d for their mitigation or response.|
|Prototypes and proof-of-concepts|To clarify the vision, and validate technical ideas.|
|Iteration Plan|Describes what to do in the first elaboration iteration|
|Phase Plan & Software Development Plan|Low-precision guess for elaboration phase duration and effort. Tool people, education, and other resources.|
|Development Case|A description of the customized UP steps and artifacts for this project In the UP, one always customizes it for the project|
|Domain Model|This is a visualization of the domain concepts, it is similiar to a static information model of the domain entities|
|Design Model|This is the set of diagrams that describes the logical design. This includes software class diagrams, object interaction diagrams, package diagrams, and other design artifacts|
|Software Architecture Document|A learning aid that summarizes the key architecturl issues and their resolution in the design. It is a summary of the outstanding design ideas and their motivation in the system|
|Data Model|This includes the database schemas, and tha mapping strategy between objects and non-object representations|
|JPA Mapping|Technology-specific Spring Data JPA mapping rationale derived from the physical data model, including entity boundaries, ownership, identifiers, and persistence trade-offs|
|Use Case Realization|One document per use case that maps each scenario to object design using design sequence diagrams and design class diagrams|
|Use-Case Storyboards, UI Prototypes|A description of the user interface, paths of navigation, usability models, and so forth. Realized through `Design System` (tokens, rules), `State Visual Specs` (per-state visual bundles), `Interaction Spec` (transitions and traceability), and `Vaadin Mapping` (concrete Vaadin 25 mapping).|
|Requirements Ranking|A prioritized list of requirements based on risk, coverage, and criticality|
|Design System|Project-level YAML artifact defining design tokens (color, typography, spacing, radius, elevation), component token rules, responsive breakpoints, and accessibility constraints for the whole application.|
|State Visual Specs|Per-use-case, per-state visual bundles. Each bundle captures a significant UI state (base, editing, loading, validation_error, etc.) with screenshot, HTML mock, component states, layout notes, and delta-from-base.|
|Interaction Spec|YAML artifact per use case view describing interactive elements, transitions with from/to states, validations, success/error/loading paths, and full traceability to SSDs and Operation Contracts.|
|Vaadin Mapping|Document mapping the approved Design System + State Visual Specs + Interaction Spec to Vaadin 25 Flow implementation decisions: structure, state rendering, transitions, validation/Binder strategy, theming, accessibility, and recommended class structure.|
# What you need to do (Pair Programming workflow)

0. At any step, suggest to add relevant domain concepts to the Glossary.
 - Before starting step 1, load the active schema instruction for glossary and the active schema template `glossary.md` to check if there are any specific rules or structure to follow.
 - if new additions are made, update the Glossary artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/01 Business Modeling/Glossary.md`.
1. Plan the iteration based on the Requirements Ranking, selecting the most risky, valuable and least covered use cases, use case scenarios or features (10% chosen in previous iterations from inception or elaboration). Refine it in collaboration with the user.
  - early iterations focus on programing and testing architecturally significat concerns (such as security), and using, proving, devoloping ans stabilizing the key architectural elements (subsystems, interfaces, frameworks, wiring, and so on).
  - Artifacts in progress: `Requirements Ranking` and `Iteration Plan`
  - Before planning, load the active schema instruction Iteration Plan and the active schema template `Iteration Plan.md`.
  - Stop and request `OK PASO 1` before continuing.
  - After approval, store the `Iteration Plan` artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/08 Project Management/{{#}} {Iteration} Plan.md`.
  - In that file name, `{{#}}` is the zero-padded numeric part of `{Iteration}` (`E1 -> 01`, `E11 -> 11`).
2. Elaborate Domain Model for the current iteration.
  - Artifacts in progress: `Domain Model`
  - Before elaborating, load the active schema instruction for domain models and the active schema template `domain-model.md`.
  - Stop and request `OK PASO 2` before continuing.
  - After approval, store the `Domain Model` artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/01 Business Modeling/Domain Model.md`.
3. Elaborate System Sequence Diagrams for the use cases in scope for the iteration.
  - Artifacts in progress: `System Sequence Diagrams`
  - Before elaborating, load the active schema instruction for sequence diagrams and the active schema template `sequence-diagram.md`.
  - Stop and request `OK PASO 3` before continuing.
  - After approval, store the `System Sequence Diagrams` artifacts using the storage skill, following the active Artifact Store Policy. They should be stored under `openspec/artifacts/{domain}/02 Requirements/SSDs/SSD UC{{#}} {{use-case.name}}.md`.
4. Elaborate Operation Contracts for the use cases in scope for the iteration.
  - Artifacts in progress: `Operation Contracts`
  - Before elaborating, load the active schema instruction for operation contracts and the active schema template `operation-contract.md`.
  - If new discoveries during elaboration require changes to the vision, use-case model, supplementary specification, glossary, or risk list, update them in collaboration with the user and load the updated artifacts to storage before proceeding.
  - Stop and request `OK PASO 4` before continuing.
  - After approval, store the `Operation Contracts` artifacts using the storage skill, following the active Artifact Store Policy. They should be stored under `openspec/artifacts/{domain}/02 Requirements/Operation Contracts/UC{{#}} {{use-case.name}} - Operation Contracts.md`.

5. UI Design if there is UI scope in the iteration.
   - Artifacts in progress: `Design System`, `State Visual Specs`, `Interaction Spec`, `Vaadin Mapping`.
   - Load the skill `/ui-design/SKILL.md` and follow its 4-phase (Phase A, Phase B, Phase C, Phase D) pair-programming workflow.
   - Required inputs: Use Cases in scope, SSDs from step 3, Operation Contracts from step 4, Supplementary Specification, Glossary, and for each significant UI state: a screenshot/image, an HTML mock with styles, and design system variables or tokens used by that HTML.
   - For each use case with UI scope:
     a. Phase A: Define or refine the project-level Design System YAML (color tokens, typography, spacing, component rules, responsive breakpoints, accessibility). Gate: `OK DESIGN SYSTEM`.
     b. Phase B: Create State Visual Specs — one bundle per significant UI state (base, editing, loading, validation_error, server_error, success, empty, loaded) with screenshot, HTML mock, component states, layout notes, and accessibility notes. Gate: `OK VISUAL`.
     c. Phase C: Create the Interaction Spec YAML — interactive elements, transitions with from/to states, validations, success/error/loading paths, and traceability to SSDs and Operation Contracts. Gate: `OK INTERACTION`.
     d. Phase D: Create the Vaadin Mapping document — structure mapping, state-to-UI mapping, transition mapping, validation/Binder strategy, theming, accessibility, and recommended class structure. Gate: `OK VAADIN`.
   - Stop and request `OK PASO 5` before continuing.
   - After approval, store artifacts using the storage skill:
     - Design System: `openspec/artifacts/{domain}/03 Design/UI/Design System.yaml`
     - Visual Specs: `openspec/artifacts/{domain}/03 Design/UI/Visual Specs/UC{{#}} {{use-case.name}}/`
     - Interaction Spec: `openspec/artifacts/{domain}/03 Design/UI/Interaction Specs/UC{{#}} {{use-case.name}} - Interaction Spec.yaml`
     - Vaadin Mapping: `openspec/artifacts/{domain}/03 Design/UI/Technology Mapping/UC{{#}} {{use-case.name}} - Vaadin Mapping.md`

6. (TBD) Reports design if there is report scope in the iteration.

7. Elaborate or refine the Architectural Analysis for the current iteration.
   - Artifacts in progress: `Architectural Analysis`, `Technical Memos`.
   - Before elaborating, load the skill `/architectural-analysis/SKILL.md`, the active schema template `architectural-analysis.md`, and the active schema template `technical-memo.md`.
   - Required inputs: Vision, Use Case Model, Supplementary Specification.
   - The `/architectural-analysis/SKILL.md` produces FURPS+ factor tables, prioritized factors, architectural decisions with trade-offs and rationale, and technical memo recommendations.
   - Separate the output into two artifact types:
     a. `Architectural Analysis` — FURPS+ factor tables, prioritized factors, architectural decisions, variation/evolution points, and unresolved issues. Use the `architectural-analysis.md` template (this template does NOT include technical memos).
     b. `Technical Memos` — One file per significant architectural decision or issue. Use the `technical-memo.md` template.
   - Stop and request `OK PASO 7` before continuing.
   - After approval, store artifacts using the storage skill:
     - Architectural Analysis: `openspec/artifacts/{domain}/02 Requirements/architectural-analysis.md`
     - Technical Memos: `openspec/artifacts/{domain}/02 Requirements/Technical memos/Issue - {{FURPS+ category}} - {{issue.name}}.md`
   - If new discoveries during architectural analysis require changes to the Supplementary Specification, update it in collaboration with the user. Store under `openspec/artifacts/{domain}/02 Requirements/supplementary-specification.md`.

8. Refine if needed or elaborate if not exist the logical view for packages, subsystems, and layers using `/packages-logical-view/SKILL.md` to add to the master files the incremental changes for the current iteration.
  - Artifacts in progress: `Logical View` (packages, subsystems, and layers).
  - Before elaborating, load the skill `/packages-logical-view/SKILL.md`.
  - This step is the package-level design gate. Its purpose is to freeze the structural canvas that later scenario design must use.
  - Required inputs: iteration plan, Domain Model from step 2, Architectural Analysis from step 7, Supplementary Specification, and Glossary.
  - Define package structure, subsystem boundaries, layer definitions, dependency direction rules, and allowed responsibilities per package.
  - Produce an explicit package catalog for the iteration scope:
    a. package or subsystem name,
    b. responsibility summary,
    c. inbound and outbound dependency rules,
    d. use cases or scenarios that are expected to touch that package.
  - Create or refine UML package diagrams per package/subsystem using PlantUML.
  - Create an explicit package-to-scenario traceability list so step 9A can process scenarios without redesigning boundaries.
  - MUST stay at package, subsystem, and layer level only.
  - MUST NOT include class-level design detail, method design, or sequence design in this step.
  - If a scenario cannot be placed cleanly into the current package boundaries, resolve that now in step 8 before moving to step 9A.
  - Stop and request `OK PASO 8` before continuing.
  - After approval,
   - update the `Logical View` artifact in the master files with the incremental changes for the current iteration, using the storage skill and following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/03 Design/Logical View/{{fully.qualified.package}}.packageDiagram.plantuml`.
   - if new discoveries during logical view design require changes to supplementary specification or technical memos, update them in collaboration with the user. They should be stored under `openspec/artifacts/{domain}/02 Requirements/supplementary-specification.md` and `openspec/artifacts/{domain}/02 Requirements/Technical memos/Issue - {{FURPS+ category}} - {{issue.name}}.md` respectively, using the storage skill and following the active Artifact Store Policy.

9A. Elaborate the Domain-to-Design Transition: bridge the conceptual Domain Model to the software Design Model with an explicit mapping that makes every design decision traceable to domain concepts and operation contracts.
  - Artifacts in progress: `Logical View` (domain-to-design transition map and responsibility assignments).
  - Before elaborating, load the skills `/design-principles/SKILL.md`, the active schema instruction `domain-to-design-transition.md`, and the active schema template `domain-to-design-transition.md`.
  - Required inputs: Domain Model from step 2 (conceptual classes, attributes, associations, invariants), SSDs from step 3 (system operations per scenario), Operation Contracts from step 4 (postconditions in domain vocabulary), Logical View packages from step 8 (package boundaries and dependency rules), Supplementary Specification, and Glossary.
  - This step produces the transformation contract that step 9B will use as fixed input. It does NOT produce sequence or class diagrams yet.
  - Build an explicit scenario queue from the approved iteration plan and process all scenarios together in this step:
    a. Domain-to-Software Transformation Map: for every domain concept referenced by the scenarios in scope, produce a table mapping DomainModelConcept → SoftwareClass/Interface. Note where the software model diverges from the domain model and why.
    b. Responsibility Assignment Matrix: assign knowing/doing responsibilities to each software class using Information Expert, using the Operation Contract postconditions as the primary driver. Walk through each postcondition and identify which software class(es) must collaborate to satisfy it.
    c. Postcondition Traceability Matrix: map every Operation Contract postcondition to the software design element(s) that will satisfy it. If a postcondition cannot yet be assigned, mark it as TBD with a rationale.
    d. Pattern Candidate List: identify hotspots (versioning, state machines, policy variation, etc.) and propose pattern candidates (Memento, State, Strategy, Composite, etc.) with problem evidence, intent fit, and participant mapping to domain concepts.
    e. Transformation Rationale: document decisions where the software model diverges from the domain model, with explicit justification aligned with `/design-principles/SKILL.md`.
  - MUST NOT design sequence diagrams, class diagram deltas, or method-level collaborations in this step.
  - MUST keep the transformation map at the class-and-responsibility level; do not descend into method signatures or algorithmic design.
  - If the transformation reveals a mismatch that requires changing package boundaries, stop and route the issue back to step 8.
  - Stop and request `OK PASO 9A` before continuing.
  - After approval, persist the transition artifacts using the storage skill, following the active Artifact Store Policy:
    - Domain-to-Design Transition Map under: `openspec/artifacts/{domain}/03 Design/Logical View/domain-to-design-transition.md`

9B. Design sequence diagrams and class diagrams for the Logical View, mapping each approved scenario in scope to object design using the transition map from step 9A as a fixed contract.
  - Artifacts in progress: `Logical View` (design sequence diagrams and design class diagrams).
  - Before designing, load the skills `/sequence-diagram/SKILL.md` and `/class-diagram/SKILL.md`, and re-load the approved `domain-to-design-transition.md` from step 9A.
  - Required inputs: approved iteration plan, SSDs from step 3, Operation Contracts from step 4, approved Domain-to-Design Transition Map from step 9A, Logical View packages from step 8, Supplementary Specification, and Glossary.
  - Use the scenario queue already built in step 9A; do NOT rebuild it.
  - This step is the scenario-level design step. Use the package boundaries from step 8 and the transition map from step 9A as fixed constraints.
  - For each scenario in scope, execute these phases in order:
    a. Design Sequence Diagram (DSD): design one DSD for that scenario starting from the SSD system operations, the Operation Contract events and postconditions, and the responsibility assignments from step 9A.
    b. Design Class Diagram Delta (DCD Delta): update only the class diagrams of the packages touched by that scenario, adding or refining classes, associations, responsibilities, and interfaces needed by the DSD. Use the Domain-to-Software Transformation Map from step 9A as the naming and structure contract.
    c. Validation: verify that every Operation Contract postcondition is satisfied in the proposed design, using the Postcondition Traceability Matrix from step 9A as the checklist.
    d. Rationale: document concise design rationale aligned with the transformation decisions from step 9A, including cohesion/coupling checks, controller/view separation, and pattern realization details.
    e. Constraint alignment: reflect Supplementary Specification constraints and Glossary terminology in the scenario mapping.
  - Use the Domain-to-Software Transformation Map from step 9A as the authoritative source for software class names.
  - MUST keep one scenario per DSD.
  - MUST update only the package class diagrams touched by the current scenario.
  - MUST NOT redesign package boundaries, subsystem boundaries, or layer rules in this step.
  - MUST NOT override transformation decisions from step 9A; if a transformation issue is discovered, stop and route it back to step 9A.
  - If a package or layer problem is discovered, stop scenario design and route the issue back to step 8.
  - Stop and request `OK PASO 9B` before continuing.
  - After approval, persist class and sequence diagrams using the storage skill, following the active Artifact Store Policy:
    - Design Sequence Diagrams under: `openspec/artifacts/{domain}/03 Design/Logical View/DSD UC{{#}} {{use-case.name}} - S{{scenario.#}}.sequenceDiagram.plantuml`
    - Design Class Diagrams under: `openspec/artifacts/{domain}/03 Design/Logical View/{{fully.qualified.package}}.classDiagram.plantuml`

10. Assemble Use Case Realization documents for each use case in scope, referencing and validating the designs already produced in steps 9A and 9B.
  - Artifacts in progress: `Use Case Realization`
  - Before assembling, load the active schema instruction `use-case-realization.md`, the active schema template `use-case-realization.md`, and the skill `/design-principles/SKILL.md`.
  - This step is assembly and validation only. It does not introduce new design elements.
  - Required inputs (already designed in steps 9A and 9B; reference only):
    - Domain-to-Design Transition Map from step 9A
    - Design Sequence Diagrams and Design Class Diagrams from Logical View (step 9B)
    - SSDs from step 3
    - Operation Contracts from step 4
  - For each use case:
    a. Build the scenario mapping table (UC steps → SSD → OC → Design reference from steps 9A/9B).
    b. Reference, and do not recreate, the design diagrams and transition map from Logical View.
    c. Fill the operation contract postcondition satisfaction checklist, cross-referencing the Postcondition Traceability Matrix from step 9A.
    d. Verify and document alignment with Supplementary Specification and Glossary.
    e. Add design rationale notes drawing from `/design-principles/SKILL.md` validation already produced in step 9B.
  - MUST NOT introduce new classes, new responsibilities, new package decisions, or new interactions in this step.
  - If documentation is incomplete but the design already exists, complete it here.
  - If a missing design element is discovered, route the issue back to step 9A or 9B instead of solving it inside step 10.
  - Stop and request `OK PASO 10` before continuing.
  - After approval, store each `Use Case Realization` artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/03 Design/Use Case Realization/UCR UC{{#}} {{use-case.name}}.md`.

11. Reviewer pass for Logical View quality gate (steps 8, 9A, 9B, and 10).
  - Artifacts in progress: `Logical View` and `Use Case Realization`.
  - Before reviewing, load the skills `/design-principles/SKILL.md` and `/architectural-design/SKILL.md`, and re-load `use-case-realization.md` to validate both design quality and artifact structure.
  - This step is a readiness gate before persistence design. Do not continue to PASO 12 until the logical design is explicitly accepted.
  - Required inputs: approved Logical View outputs from steps 8, 9A, and 9B, approved Use Case Realization outputs from step 10, Domain Model from step 2, SSDs from step 3, Operation Contracts from step 4, Supplementary Specification, Glossary, and Architectural Analysis from step 7.
  - Run these review passes in order:
    a. Structural review of step 8: verify package catalog, package-to-scenario traceability, layer rules, dependency direction rules, and absence of boundary violations.
    b. Transition review of step 9A: verify Domain-to-Software Transformation Map completeness, Responsibility Assignment Matrix coverage and Information Expert justification, Postcondition Traceability Matrix coverage (no missing postconditions), pattern candidate evidence and rationale, and transformation divergence justifications.
    c. Scenario design review of step 9B: verify one DSD per scenario, DCD deltas only in touched packages, object collaborations consistent with 9A responsibility assignments, controller/view separation, cohesion/coupling rationale, pattern realization aligned with 9A candidates, persistence touchpoints, and explicit fulfillment of every Operation Contract postcondition against the 9A traceability matrix.
    d. Documentation review of step 10: verify complete scenario mapping (UC steps → SSD → OC → design references from 9A/9B), correct references to design diagrams and transition map from Logical View, alignment with Supplementary Specification and Glossary, and confirmation that PASO 10 did not introduce new design elements.
  - If any package, layer, or dependency issue is found, route the issue back to step 8.
  - If any transformation, responsibility mapping, or traceability issue is found, route the issue back to step 9A.
  - If any scenario design, collaboration, or diagram issue is found, route the issue back to step 9B.
  - If any traceability or UCR assembly issue is found, route the issue back to step 10.
  - For each use case in scope, produce a concise review summary including:
    - principles applied,
    - blocking issues found,
    - refactor actions taken,
    - remaining risks/TBDs,
    - readiness status for PASO 12: `YES`, `CONDITIONAL`, or `NO`.
  - MUST NOT allow PASO 12 to start while any use case is marked `NO`.
  - Stop and request `OK PASO 11` before continuing.
  - After approval, persist each reviewed or refactored artifact using the storage skill, following the active Artifact Store Policy:
    - Domain-to-Design Transition Map under: `openspec/artifacts/{domain}/03 Design/Logical View/domain-to-design-transition.md`
    - Package diagrams under: `openspec/artifacts/{domain}/03 Design/Logical View/{{fully.qualified.package}}.packageDiagram.plantuml`
    - Design Sequence Diagrams under: `openspec/artifacts/{domain}/03 Design/Logical View/DSD UC{{#}} {{use-case.name}} - S{{scenario.#}}.sequenceDiagram.plantuml`
    - Design Class Diagrams under: `openspec/artifacts/{domain}/03 Design/Logical View/{{fully.qualified.package}}.classDiagram.plantuml`
    - Use Case Realization under: `openspec/artifacts/{domain}/03 Design/Use Case Realization/UCR UC{{#}} {{use-case.name}}.md`

12. Elaborate or refine the Data Model if there is data scope in the iteration.
  - Artifacts in progress: `Data Model` and `JPA Mapping`.
  - Before elaborating, load the skills `/data-model/SKILL.md` and `/jpa-mapping/SKILL.md`, the template `../storage/openspec/schemas/default/templates/plantuml.plantuml`, and the template `/jpa-mapping/templates/jpa-mapping.md`.
  - Required inputs: Domain Model from step 2, SSDs from step 3, Operation Contracts from step 4, reviewed Logical View and Use Case Realization outputs from steps 8 to 11, Supplementary Specification, Glossary, and the existing master data-model artifacts if they already exist.
  - Reload the persisted artifacts refined in PASO 11 before drafting the physical model or the JPA mapping.
  - First, use `/data-model/SKILL.md` to draft or refine the framework-agnostic physical data model in PlantUML.
  - Then, use `/jpa-mapping/SKILL.md` to translate that model into an implementable Spring Data JPA design and rationale document.
  - Keep both artifacts in master-only mode: apply the current iteration delta to the same files instead of creating iteration-specific copies.
  - If PASO 12 discovers a mismatch that requires changing the logical design, stop and route the issue back to steps 8, 9A, 9B, or 10 through the PASO 11 review gate before finalizing persistence design.
  - If the iteration has no data scope, document the skip rationale and still request approval for the step.
  - Stop and request `OK PASO 12` before continuing.
  - After approval, store the `Data Model` and `JPA Mapping` artifacts using the storage skill, following the active Artifact Store Policy:
    - `openspec/artifacts/{domain}/03 Design/Data Model/data-model.plantuml`
    - `openspec/artifacts/{domain}/03 Design/Data Model/jpa-mapping.md`
  - If new discoveries during data-model design require changes to the Domain Model, Glossary, Supplementary Specification, or Technical Memos, update them in collaboration with the user before persisting.

13. Elaborate the SW Architecture Document using the `/software-architecture-document/SKILL.md`, describing the key architectural decisions, patterns, and rationale for the current iteration.
  - Artifacts in progress: `SW Architecture Document`
  - Stop and request `OK PASO 13` before continuing.
  - After approval, store the `SW Architecture Document` artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/03 Design/SW Architecture Document.md`.

14. Start Skill Test-Driven Development (TDD) cycles to implement the design for the selected scenarios in the iteration scope, producing working code and automated tests as part of elaboration.
  - Artifacts in progress: `Test Plan`, `Code`, `Unit and Integration Tests`
  - Before starting TDD, load the skill `/tdd/SKILL.md` and the approved artifacts that define the selected implementation slice:
    - `Iteration Plan` from step 1, as the scope and sequencing contract for the iteration.
    - `Use Case Realization` from step 10 together with the referenced reviewed `Logical View` artifacts from steps 8 to 11, as the primary design-to-code contract for the selected scenario.
    - `System Sequence Diagrams` from step 3 and `Operation Contracts` from step 4, as the behavior and postcondition contract.
    - `SW Architecture Document` from step 13, as the architecture constraint and significant-decision contract.
    - `Supplementary Specification` and `Glossary`, as the constraint and terminology contract.
  - If the selected scenario touches persistence, also load `Data Model` and `JPA Mapping` from step 12.
  - If the selected scenario has UI scope, also load `Design System`, `State Visual Specs`, `Interaction Spec`, and `Vaadin Mapping` from step 5.
  - If the selected scenario has UI scope, also load the linked approved screen assets referenced by the `State Visual Specs` under `openspec/artifacts/{domain}/03 Design/UI/screens/...`.
  - If the selected scenario implements an architecturally significant or risky concern, also load the relevant `Architectural Analysis` and `Technical Memos` from step 7.
  - Use the `Iteration Plan` as a hard scope gate: implement only the use cases, scenarios, or slices explicitly selected for the current iteration. If implementation reveals out-of-scope work, stop and route the change back to PASO 1 before coding it.
  - Use the `Use Case Realization` as the primary scenario contract: derive the active test slice from the scenario mapping, referenced DSD/DCD, and postcondition satisfaction checklist. Do not invent behavior outside the approved scenario slice.
  - If the selected scenario has UI scope, before requesting `OK PASO 14`, present a UI implementation baseline that includes:
    - target view(s),
    - approved visual state ids in scope,
    - linked HTML mock and screenshot/image assets loaded,
    - `Interaction Spec` transitions in scope,
    - `Vaadin Mapping` sections used,
    - visual non-negotiables and any deferred UI states.
  - Before requesting `OK PASO 14`, confirm that the selected scenario passed the Logical View review gate and has no unresolved blocking design issues.
  - For each selected scenario, follow the TDD loop to incrementally implement the approved design, starting from the scenario's SSD system operations, operation contract events/postconditions, and the responsibilities defined in the referenced design artifacts.
  - Ensure that every implemented scenario has corresponding automated tests that validate expected behavior, edge cases, and the scenario result promised in the `Iteration Plan`.
  - Ensure that every `Test Plan` item is traceable at least to: `Iteration Plan` item, use case/scenario, `Use Case Realization` section, SSD reference, and Operation Contract postcondition. Add architecture, persistence, or UI references when applicable.
  - If the selected scenario has UI scope, the initial `Test Plan` MUST include at least one UI fidelity item per target view and trace it to:
    - `State Visual Spec.state_id`,
    - `Interaction Spec.transition.id`,
    - the relevant `Vaadin Mapping` section,
    - the linked HTML mock path under `openspec/artifacts/{domain}/03 Design/UI/screens/...` when applicable.
  - If issues are discovered during TDD, update and persist the owning artifacts before proceeding:
    - scope or cut-line issue -> `Iteration Plan`
    - package, layer, collaboration, or scenario-design issue -> `Logical View` and `Use Case Realization`
    - persistence-model or JPA-mapping issue -> `Data Model` and `JPA Mapping`
    - UI state, interaction, or rendering issue -> `Design System`, `State Visual Specs`, `Interaction Spec`, and `Vaadin Mapping`
    - architecture decision or cross-cutting concern issue -> `SW Architecture Document` and `Technical Memos`
  - Request `OK PASO 14` to approve the test-case slice and TDD plan.
  - Immediately after `OK PASO 14`, the TDD skill persists `Test Plan` through the storage skill under `openspec/artifacts/{domain}/05 Test/{{#}} {Iteration} Test plan.md`, with `{{#}}` resolved from the numeric part of `{Iteration}`.
  - After `Test Plan` is persisted, request `OK PASO 14 IMPLEMENTAR` before executing real file edits and test commands.
  - During execution, report RED/GREEN evidence per cycle (failing test, minimal change, green suite evidence, updated Test List).
  - When the selected scenario has UI scope, the final PASO 14 review MUST summarize:
    - implemented UI states,
    - deferred UI states,
    - remaining mismatches versus approved UI artifacts,
    - executable validation evidence for view structure and state rendering.
  - When implementation for this step is complete and reviewed, request `OK PASO 14` to continue to PASO 15.

15. Refine Requirements Ranking based on iteration feedback if any (new features or use cases, defects, changes in priorities). Refine it in collaboration with the user.
  - Artifacts in progress: `Requirements Ranking`
  - Before refining, load the active schema instruction for use cases and the active schema template `requirements-ranking.md`.
  - Stop and request `OK PASO 15` before continuing.
  - After approval, persist the updated `Requirements Ranking` artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/08 Project Management/Requirements Ranking.md`.

16. Based on the Requirements Ranking, choose 10% (at least one) of the use cases that are still in brief format (not yet converted to fully dressed). prioritize the pending candidates with the highest architectural significance, risk, and business value, explain the selection reasons, and then analyze each selected use case in fully dressed format. refine each in collaboration with the user before proceeding to the next one.
  - Artifacts in progress: `Requirements Ranking` and `Use Case fully dressed`.
  - Before choosing the 10%, load the active schema instruction/template for `Requirements Ranking` and produce an explicit ranking based on risk, coverage, and criticality.
  - Build the candidate pool only from use cases that remain in brief format; exclude any use case already documented in fully dressed format.
  - The 10% selection must come from that pending brief-format pool and be justified from the ranking; do not choose deep-dive use cases ad hoc.
  - Before drafting each detailed case, load the active schema instruction for use cases and the active schema template `use-case-fully-dressed.md`.
  - Stop and request `OK PASO 16` before continuing.
    - After approval, persist each `Use Case fully dressed` artifact using the storage skill, following the active Artifact Store Policy. It should be stored under `openspec/artifacts/{domain}/02 Requirements/use-cases/UC{{#}} {{use-case.name}}.md`.

17. Close the current elaboration cycle in master-only persistence mode (NOT the Elaboration phase).
  - Stop and request `OK PASO 17` before closing the cycle.
  - Treat this as an automatic step, not a user-driven action.
  - Do NOT create, move, or archive folders under `openspec/iterations/`.
  - Do NOT run delta-merge operations.
  - Confirm to the user that approved artifacts are already persisted directly under `openspec/artifacts/{domain}/...` and list the files updated in this cycle.
  - After cycle closure, if requirements coverage is < 100%, start a new elaboration cycle and continue from step 1.

18. Repeat steps 1 to 17 for each elaboration iteration until 100% of requirements are addressed.
  - Do not exit Elaboration only because one cycle was closed.
  - Transition out of Elaboration only when requirements coverage target is achieved and explicitly approved.

## Step Progress Display

Map `state.yaml` fields to visual indicators:

| Símbolo | Estado | Fuente en `state.yaml` |
|---------|--------|------------------------|
| `✅` | Completado | Paso presente en `approved_steps` |
| `🔄` | En progreso | Paso igual a `current_step` |
| `⬜` | Pendiente | Paso presente en `pending_steps` |
| `⏭️` | TBD / fuera de scope | Paso no aplicable en esta iteración |

### Paso 0 — Glossary (on-demand)
### ✅ Paso 1 — Iteration Plan
### ✅ Paso 2 — Domain Model
### 🔄 Paso 3 — System Sequence Diagrams ← ACTUAL
### ⬜ Paso 4 — Operation Contracts
### ⬜ Paso 5 — UI Design
### ⬜ Paso 6 — Reports Design (TBD)
### ⬜ Paso 7 — Architectural Analysis
### ⬜ Paso 8 — Logical View (packages)
### ⬜ Paso 9A — Domain-to-Design Transition
### ⬜ Paso 9B — Scenario Design (sequence + class)
### ⬜ Paso 10 — Use Case Realization
### ⬜ Paso 11 — Reviewer pass
### ⬜ Paso 12 — Data Model + JPA Mapping
### ⬜ Paso 13 — SW Architecture Document
### ⬜ Paso 14 — TDD (Code + Tests)
### ⬜ Paso 15 — Refine Requirements Ranking
### ⬜ Paso 16 — Use Case fully dressed (10%)
### ⬜ Paso 17 — Cycle close
### ⬜ Paso 18 — Phase close

La lista anterior es la plantilla — el driver la renderiza dinámicamente, sustituyendo los marcadores `✅`/`🔄`/`⬜`/`⏭️` según los datos reales de `state.yaml` en tiempo de ejecución.

## Required Turn Template

For each step, always respond in this order:

0. **Progress overview** — Render the step checklist above with current `state.yaml` data (completed, in-progress, pending), mark the current step and iteration label (e.g. `E1`, `E2`).
1. Proposed draft for the current step (short and reviewable).
2. Open questions or assumptions.
3. Explicit approval request: `Escribe OK PASO N para continuar`.

Do not include content for later steps until approval is received.

## Elaboration Anti-Patterns
- it only has one iteration.
- The risky elements and core architecture are no being tackled.
- it does not result in executable architecture, there is not production-code programming.
- it is considered primarily a requirement or design phase, preceding an implementation phase in construction.
- There is an attempt to do a full and careful design before programming.
- There is minimal feedback and adaptation; users are not continually engaged in evaluation and feedback.
- There is not early and realistic testing.
- The architecture is especulatively finalized before programming.
- skipping explicit approval checkpoints between steps.
- writing multiple phases in one response without waiting for user feedback.
- persisting approved artifacts under `openspec/iterations/{iteration}/...` instead of direct master paths.
- attempting archive or delta-merge operations in master-only persistence mode.
- treating elaboration cycle closure as if it were phase completion.
- starting a new UP phase immediately after cycle closure while Elaboration coverage is still below target.
define the architecture

# Results

Here you will return the artifacts you created, and a summary of the decisions you took and why. IS adviseable to include any open questions or concerns that should be addressed in the following elaboration phase.
