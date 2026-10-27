# Use Case Realization Purpose

- A Use Case Realization maps each scenario of one use case to object design artifacts.
- The realization must show how functional requirements are materialized as object collaborations.
- For each scenario, the artifact must include a design sequence diagram and a design class view.
- One realization document is produced per use case, and that document contains all mapped scenarios for that use case.

## Required Inputs

- Use Case text for the selected use case (main success and extensions).
- System Sequence Diagram artifacts for the selected scenarios.
- Operation Contracts derived from SSD system operations.
- Domain Model from Business Modeling.
- Supplementary Specification constraints (especially non-functional and cross-cutting constraints).
- Glossary terms and data definitions.
- Existing Use Case Realization document (if it exists).

## Mandatory Workflow (Pair Programming)

1. Select one use case and list all scenarios in scope.
2. Build a traceability map per scenario: Use Case steps -> SSD messages -> Operation Contracts.
3. For each scenario, design object collaboration with a design sequence diagram.
4. For each scenario, identify and refine the participating design classes and relationships.
5. Validate that operation contract postconditions are satisfied by the proposed design.
6. Validate terminology against Glossary and constraints against Supplementary Specification.

### Execution Mode (MANDATORY)

- Agent role: Driver.
- User role: Navigator.
- The agent proposes each scenario realization incrementally and asks for feedback before finalizing.

## Modeling Rules (MUST / MUST NOT)

- MUST produce exactly one realization artifact per use case.
- MUST include a mapping section for every scenario in scope of that use case.
- MUST start design from SSD system operations and operation contract events/postconditions.
- MUST treat system operations as the starting messages entering the Controllers for domain-layer sequence diagrams.
- MUST ensure every mapped operation contract postcondition is explicitly satisfied in the design.
- MUST use Business Modeling concepts as inspiration for software domain object naming.
- MUST keep names and meanings consistent with Glossary terminology.
- MUST include both:
	- a design sequence diagram for scenario interaction flow,
	- and a design class diagram (scenario slice and/or consolidated use-case-level view).
- MUST account for Supplementary Specification constraints that influence the design (security, auditing, performance, validation, etc.).
- MUST keep design traceability explicit from Use Case -> SSD -> Operation Contracts -> Design.
- MUST NOT invent behavior outside selected scenario scope.
- MUST NOT contradict operation contracts or omit required postconditions.
- MUST NOT replace domain language with framework-specific terminology.

## Output Contract (MUST)

The artifact MUST include:

- Use case identification (ID, name, and brief goal).
- Input references section (Use Case, SSDs, Operation Contracts, Domain Model, Supplementary Specification, Glossary).
- Scenario mapping table with at least:
	- Scenario,
	- Use case steps,
	- SSD reference,
	- Operation Contract reference,
	- Key postconditions,
	- Design sequence section,
	- Design class section,
	- Supplementary/Glossary notes,
	- Status.
- One realization subsection per scenario including:
	- requirement traceability,
	- design sequence diagram in PlantUML,
	- design class diagram in PlantUML (scenario slice or reference to consolidated view),
	- postcondition satisfaction checklist,
	- supplementary constraints and glossary alignment notes.
- A consolidated class view for the use case when multiple scenarios share or evolve the same classes.

## Storage Convention

- Persist one file per use case using the storage skill by artifact id (passing `{{use-case.name}}`; storage resolves the concrete path from the active schema). Do NOT hardcode artifact paths.
- The file must contain all mapped scenarios for that use case.

## Diagram Export & SVG Linking (MANDATORY)

Before assembling (and before the reviewer pass of step 11), every diagram referenced by the UCR must exist as an exported SVG:

1. Export command
   - Run the PlantUML VS Code extension command `PlantUML: Export Workspace Diagrams` (command id `plantuml.exportWorkspace`).
   - Terminal trigger (Windows): `Start-Process "vscode://command/plantuml.exportWorkspace"`.
   - If the command cannot be triggered or no SVG appears, stop and ask the user to run it manually from the VS Code Command Palette and confirm.
   - The export is asynchronous: poll `<workspace>/out/` for the required SVGs (timeout ~120 s) before writing the UCR.

2. Export layout
   - One folder per diagram: `<workspace>/out/{source dir relative to workspace}/{baseName}/{diagramName}.svg`
   - `{baseName}` is the original `.plantuml` file name WITHOUT the extension (e.g. `DSD UC18 Asignar Políticas al Empleado - S4.sequenceDiagram`).
   - `{diagramName}` is the identifier declared after `@startuml` in the source file (fallback: `{baseName}`). DSDs declare ids like `DSD_UC18_S4`; class/package diagrams declare the fully qualified name, which matches `{baseName}`.
   - Example: source `openspec/artifacts/registro-horario/03 Design/Logical View/DSD UC18 Asignar Políticas al Empleado - S4.sequenceDiagram.plantuml` with `@startuml DSD_UC18_S4` exports to `out/openspec/artifacts/registro-horario/03 Design/Logical View/DSD UC18 Asignar Políticas al Empleado - S4.sequenceDiagram/DSD_UC18_S4.svg`.

3. Linking rule
   - Every reference to a `.plantuml` diagram (DSD, DCD, package diagram) MUST be an embedded image with the relative path from the UCR document directory to its exported SVG: `![alt text](relative/path/to/svg.svg)`.
   - URL-encode the path: spaces as `%20` and non-ASCII characters percent-encoded (e.g. `í` → `%C3%AD`).
   - Links to `.md` documents (Use Case, SSD, Operation Contracts, transition map, Supplementary Specification, Glossary) stay as plain text links and are never converted.

4. Where the SVG rule applies inside the UCR
   - Inputs and References: the "Design Sequence Diagrams (9B)" and "Design Class Diagrams (9B)" lists keep plain text links to the original `.plantuml` files (`[label](relative/path/diagram.plantuml)`); they are NOT SVG images.
   - Scenario Mapping table: the Design Sequence and Design Class columns use embedded SVG images.
   - Per-scenario realization: the design sequence diagram reference uses an embedded SVG image.
   - Consolidated Design Class View: every diagram cross-reference uses an embedded SVG image.

5. Verification
   - Before requesting approval, verify that every `![](…svg)` path resolves to an existing file under `<workspace>/out/`. If any is missing, re-run the export (or ask the user to) and re-verify.

## Validation Checklist

1. Is there exactly one file per use case?
2. Are all in-scope scenarios mapped?
3. Does each scenario map Use Case -> SSD -> Operation Contracts -> Design?
4. Does each scenario include a design sequence diagram?
5. Are design classes explicit per scenario or in a consolidated view?
6. Are operation contract postconditions satisfied and traceable?
7. Are glossary terms used consistently?
8. Are supplementary constraints reflected where applicable?
9. Is the storage path and file name compliant?
