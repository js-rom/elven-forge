# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

See `_shared/skill-resolver.md` for the full resolution protocol.

Only project-local skills were found during this scan. The checked user-level roots (`~/.claude/skills`, `~/.config/opencode/skills`, `~/.gemini/skills`, `~/.cursor/skills`, `~/.copilot/skills`) did not contain `SKILL.md` files.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| n/a | architectural-analysis | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\architectural-analysis\SKILL.md |
| n/a | architectural-design | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\architectural-design\SKILL.md |
| n/a | class-diagram | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\class-diagram\SKILL.md |
| n/a | create-spring-boot-java-project | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\create-spring-boot-java-project\SKILL.md |
| create spring boot vaadin project or similar | create-spring-boot-vaadin-project | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\create-spring-boot-vaadin-project\SKILL.md |
| n/a | data-model | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\data-model\SKILL.md |
| design principles, software design, architecture review, SOLID, GoF, unit testing, testability, TDD, pruebas unitarias, refactor | design-principles | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\design-principles\SKILL.md |
| when user wants to initialize SDD in a project, or says "sdd init", "iniciar sdd", "openspec init" | init | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\init\SKILL.md |
| junit, junit5, unit tests | java-junit | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\java-junit\SKILL.md |
| n/a | java-springboot | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\java-springboot\SKILL.md |
| n/a | jpa-mapping | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\jpa-mapping\SKILL.md |
| mocks, test doubles, DOC, stub, mock, spy, dummy, fake, behavior tests, state tests | mocks | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\mocks\SKILL.md |
| n/a | packages-logical-view | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\packages-logical-view\SKILL.md |
| n/a | sequence-diagram | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\sequence-diagram\SKILL.md |
| set up development environment | set-development-enviroment | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\set-development-enviroment\SKILL.md |
| n/a | software-architecture-document | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\software-architecture-document\SKILL.md |
| n/a | storage | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\storage\SKILL.md |
| tdd, test-driven development, red green refactor, write failing test, test list, unit tests first, pruebas unitarias, desarrollo guiado por pruebas | tdd | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\tdd\SKILL.md |
| casos de prueba unitarias, clases de equivalencia, valores limite, pairwise, vector ortogonal, caja negra, caja blanca, cobertura de caminos | test-cases | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\test-cases\SKILL.md |
| ui design, visual spec, interaction spec, state-based ui, design system, vaadin mapping | ui-design | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\ui-design\SKILL.md |
| ui design, ui dsl, abstract ui, design system, technology mapping, vaadin ui | ui-dsl | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\ui-dsl\SKILL.md |
| unit testing, pruebas unitarias, test quality, flaky tests, anti-patterns de pruebas, safety net tests | unit-testing | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\unit-testing\SKILL.md |
| n/a | up-elaboration | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\up-elaboration\SKILL.md |
| n/a | up-inception | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\up-inception\SKILL.md |
| n/a | vaadin-orchestrator | c:\Users\Jesus\Desktop\DEV\registro-horario\.agents\skills\vaadin-orchestrator\SKILL.md |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### architectural-analysis
- Run in driver/navigator mode and advance step by step with user feedback.
- Analyze architectural factors from Vision, Use Case Model, and Supplementary Specification using FURPS+.
- Define measurable quality scenarios and trace each factor back to source artifacts.
- Prioritize factors by inflexible constraints, business impact, and risk; capture variation and evolution points.
- Route design-decision work to `architectural-design` and 4+1 documentation to `software-architecture-document`.

### architectural-design
- Stay at architecture level only; do not drift into class-level or algorithmic design.
- Run in driver/navigator mode through drivers, style selection, package rules, quality tactics, risks, and evolution.
- Model processing elements, data elements, connectors, interfaces, collaborations, and layer-vs-tier separation explicitly.
- Apply ADP, SDP, SAP, CRP, CCP, and REP, and define allowed dependencies, forbidden dependencies, and cycle-breaking strategy.
- Evaluate styles and MVC-family variants against measurable quality scenarios and document rationale plus rejected alternatives.

### class-diagram
- Use PlantUML class-diagram syntax and represent Java records as `class X <<record>>`.
- Declare internal classifiers inside the `package {}` block and external classifiers outside with the external alias pattern.
- Keep internal-only relationships inside the package block and cross-package relationships outside after external declarations.
- Use the correct relationship semantics with multiplicities and roles; generalization and realization arrows must be `<|--` and `<|..`.
- Produce one diagram per package named `<fully.qualified.package>.classDiagram.plantuml` and avoid framework detail.

### create-spring-boot-java-project
- Verify Java 21, Docker, and Docker Compose before bootstrapping.
- Download the Spring Initializr Maven project with Boot 3.4.5 and the listed dependencies, then unzip it into the target folder.
- Add `springdoc-openapi-starter-webmvc-ui` and `archunit-junit5` to `pom.xml`.
- Configure SpringDoc, PostgreSQL, Redis, and MongoDB properties; create compose services and ignore the data folders.
- Validate with `./mvnw clean test`; optionally run with `docker-compose up -d` plus `./mvnw spring-boot:run`.

### create-spring-boot-vaadin-project
- Verify Java 21, Docker, and Docker Compose before bootstrapping.
- Download the Spring Initializr Maven project with Boot 4.0.5, Vaadin, JPA, PostgreSQL, and Testcontainers, then unzip it into the target folder.
- Add `archunit-junit5` to `pom.xml`.
- Configure PostgreSQL properties, create `docker-compose.yaml` for PostgreSQL, and ignore `postgres_data`.
- Validate with `./mvnw clean test`; optionally run compose and `./mvnw spring-boot:run`.

### data-model
- Maintain one master `data-model.plantuml`; refine it instead of creating per-iteration variants.
- Use PlantUML physical data model notation with explicit PK/FK/AK markers and concise integrity notes.
- Render persistent relationships with the correct symbol (`*--`, `o--`, `--`), explicit cardinality on both ends, and a short label.
- Keep the model technology-agnostic: no JPA annotations, Java types, repositories, or provider-specific detail.
- Start from the template and produce both an iteration delta summary and a JPA-mapping handoff.

### design-principles
- Assign responsibilities by Information Expert and scenario walkthroughs; split classes when cohesion drops.
- Prefer high cohesion, low coupling, explicit interfaces, and dependency inversion over concrete wiring.
- Keep views on UI concerns only; route system-event handling to controllers and business logic to domain/services.
- Prefer polymorphism, composition, delegation, and DI over type switches and inheritance that breaks substitutability.
- Refactor toward clearer contracts, readable naming, DRY/KISS/YAGNI, and testable seams.

### init
- Execute initialization directly; do not delegate or act like an orchestrator.
- Detect the real project stack and conventions before changing anything.
- Bootstrap `openspec` from the seed path, but do not silently overwrite an existing `openspec/` tree.
- Build `.atl/skill-registry.md` using the same scan rules as the skill-registry workflow.
- Return a structured summary with status, executive summary, artifacts, next recommended action, and risks.

### java-junit
- Use standard Maven or Gradle test layout with JUnit Jupiter API, Engine, and Params.
- Structure tests with AAA, descriptive names, and setup/teardown annotations only where needed.
- Keep one behavior per test and make tests independent and idempotent.
- Use parameterized tests when they improve coverage with controlled input sets.
- Prefer readable assertions, explicit exception testing, and Mockito-based doubles for isolation.

### java-springboot
- Organize code by feature or domain and prefer constructor injection with `private final` dependencies.
- Externalize config via `application.yml` and profiles; bind structured config with `@ConfigurationProperties`.
- Use DTOs plus Bean Validation at the web edge; do not expose JPA entities directly.
- Keep business logic in stateless services and apply `@Transactional` at the smallest useful service boundary.
- Use Spring Data JPA, parameterized SLF4J logging, focused test slices, and Spring Security for auth concerns.

### jpa-mapping
- Map from the physical data model first; call out mismatches instead of silently changing the model.
- Maintain one master `jpa-mapping.md` loaded from the template and refine it across iterations.
- Prefer standard `jakarta.persistence`, `EnumType.STRING`, and explicit association entities when a link carries behavior or attributes.
- Explain identifier strategy, cascade, orphan removal, inheritance choice, and naming overrides only where justified.
- Keep the output implementation-ready but vendor-neutral, and do not generate code unless explicitly asked.

### mocks
- Use doubles only when a collaborator is slow, nondeterministic, unavailable, UI-bound, infra-bound, or expensive to prepare.
- The double must implement the same interface as the real collaborator and define explicit simulated behavior or expectations.
- Choose `Stub` for state/output checks, `Mock` for interaction checks, `Spy` for both, `Dummy` for filler args, and `Fake` for simplified functional behavior.
- Document the contract per doubled method: inputs, outputs, and expected interactions.
- Call out fragility and false-green risks, and recommend complementary integration coverage when needed.

### packages-logical-view
- Run in driver/navigator mode and refine one modeling step at a time with the user.
- Use PlantUML package diagrams at package, subsystem, and layer level only; never include class-level detail or code.
- Use fully qualified package or subsystem names directly and do not use PlantUML aliases for them.
- Draw dependencies whenever any class in the source depends on any class in the target, and make allowed and forbidden directions explicit.
- Split diagrams by hierarchy level and keep traceability back to requirements, SSDs, operation contracts, and technical memos.

### sequence-diagram
- Start every design sequence diagram from the SSD system operation entering the controller.
- Show only software-object lifelines, activation bars, time-ordered messages, and structured frames like `loop`, `alt`, `opt`, and `ref`.
- Use Controller and Information Expert reasoning to cover every operation-contract postcondition explicitly.
- Reflect validation, audit, authorization, and similar supplementary constraints as explicit messages or notes.
- Keep one scenario per diagram, avoid framework or SQL detail, and use the required `DSD UC# ... - S#.sequenceDiagram.plantuml` naming.

### set-development-enviroment
- Confirm the user wants environment setup and identify the project type before acting.
- If the user is unsure, infer likely project types from existing files and conventions.
- Offer available setup options and route to the corresponding environment skill.
- Treat this as orchestration: choose the right setup path instead of configuring everything ad hoc.
- Keep the interaction focused on reaching the concrete environment task quickly.

### software-architecture-document
- Run in driver/navigator mode and assemble the document incrementally with approval checkpoints.
- Own final architecture documentation, especially Architecture Overview, 4+1 Views, traceability, and compliance checks.
- Keep the document at architecture level: elements, connectors, interfaces, constraints, rationale, and evolution, not class or algorithm detail.
- Include all five 4+1 views with intent, scope, diagrams, key rules, and rationale for each.
- Integrate style, MVC, dependency-governance, quality-scenario, risk, and validation results from architecture work.

### storage
- Execute persistence directly using the active Artifact Store Policy; default to `openspec` when no policy is detected.
- In `openspec` mode, use master-only persistence under `openspec/artifacts/{domain}/...` and do not archive or merge iteration folders.
- Create missing directories only when necessary and keep discipline folders aligned with `openspec-convention.md`.
- Persist `Requirements Ranking` specifically to `08 Project Management/Requirements Ranking.md`.
- Return recovery guidance keyed to the active mode, including `openspec/state.yaml` for `openspec`.

### tdd
- Treat TDD as a strict one-item-at-a-time `RED -> GREEN -> REFACTOR` loop with explicit evidence at each step.
- Load the approved implementation-slice artifacts first and do not code outside that scope.
- Build the Test List with `test-cases`, apply `unit-testing` quality rules, and persist the Test Plan before the first red cycle when required.
- In Guided mode require per-case approval; in Automatic mode still process exactly one agreed case per cycle.
- Do not implement before red evidence, do not batch pending tests, and do not move on until post-refactor green is proven.

### test-cases
- Stay in driver mode: propose a test slice, list assumptions or questions, and request `OK CASOS N` before implementation.
- Start from requirements and identify factors across inputs, SUT state, collaborators, environment, outputs, and exceptions.
- Build valid and invalid equivalence classes and add boundary values for ordered domains.
- Control explosion with pairwise or orthogonal reduction when full combinations are excessive; add white-box paths only when risk justifies it.
- Output a minimal sufficient catalog with objective, setup, input, expected result, and coverage rationale for every case.

### ui-design
- Use pair programming with explicit gates: no file writes during exploration, and persist only after the matching approval token.
- Keep visual truth in State Visual Specs, behavioral truth in Interaction Spec, technical truth in Vaadin Mapping, and cross-app consistency in the Design System.
- Produce a project-level Design System plus per-view state specs, per-view interaction YAML, and per-view Vaadin mapping.
- Model significant UI states explicitly when visibility, enablement, loading, validation, feedback, focus, responsiveness, or action availability changes.
- Maintain traceability from UI transitions to SSD operations and Operation Contracts, optimized for Vaadin 25 Flow delivery.

### ui-dsl
- Use pair programming with phased approval gates and do not write files before approval.
- Build a technology-independent YAML DSL for structure and state transitions, then a Design System, then a concrete technology mapping.
- Derive transitions from SSDs and Operation Contracts so each UI change maps to a system operation and postconditions.
- Use the controlled vocabulary for layout, components, intents, states, and variants to keep the DSL consistent.
- Treat code generation as out of scope; the artifact is a specification and mapping input for later implementation.

### unit-testing
- Keep unit tests automated, self-verifying, repeatable, independent, and fast.
- Treat test code as professional code: apply design principles, isolate external coupling, and reduce duplication with helpers or builders.
- Keep tests cohesive, simple, and expressive; one behavior per test, clear assertions, and no magic-number or conditional-noise tests.
- Detect and fix the listed anti-patterns, especially flaky, hidden-dependency, slow, obscure, or multi-personality tests.
- End with execution evidence, anti-pattern findings, safety-net confidence, and residual risks.

### up-elaboration
- Run the phase in driver/navigator mode with explicit `OK PASO N` gates and no file writes in steps 1-13 and 15-17.
- Bootstrap the active schema before work and treat instruction and template files as the contract for every step.
- Keep `openspec/state.yaml` as the live source of truth for phase, iteration, steps, and artifact lifecycle.
- Persist only the artifacts approved for each step, with the specific step-to-artifact mapping and TDD exception rules.
- Treat elaboration as iterative, risk-driven, architecture-first work; refine existing artifacts instead of trying to finalize everything in one cycle.

### up-inception
- Run the phase in driver/navigator mode with `OK PASO N` gates and no file writes during chat-first steps 1-9.
- Bootstrap the active schema before drafting and use its instructions and templates as the artifact contract.
- Maintain `openspec/state.yaml` as the authoritative tracker of phase progress and artifact status.
- Focus on partial, decision-oriented inception artifacts: Vision, Use-Case Model, selected detailed cases, ranking, supplementary spec, and early technical memos.
- After approvals, persist only approved inception artifacts and then hand off to storage and development-environment setup automatically.

### vaadin-orchestrator
- Treat this as the primary Vaadin 25 Flow entrypoint and always pin docs and API lookups to Vaadin 25 plus Java.
- Classify intent and constraints, then select one primary domain skill plus up to two secondary skills.
- Resolve conflicts in this order: security and correctness, Vaadin 25 compatibility, maintainability and minimal change, then visual polish.
- Ask at most two short clarifying questions only when needed for a safe implementation; otherwise proceed with explicit assumptions.
- Return one merged answer with decision summary, implementation, validation, risks or limits, and optional next steps; in review mode, findings come first.

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| None found | n/a | No `agents.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, or `copilot-instructions.md` file was found at the project root. |

Read the convention files listed above for project-specific patterns and rules. All referenced paths have been extracted when present; no convention index files were found in this project.