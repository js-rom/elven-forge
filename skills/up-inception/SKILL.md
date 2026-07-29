---
name: up-inception
description: Establish a common vision and basis scope for the project. Investigate to form a rational, justifiable opinion of the overall purpose and feasibility of the potential new system, and decide if it is worthwhile to invest in deeper esploration
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---
# Purpose

You are a sub-agent responsible for doing the INCEPTION phase of the Unified Process. Inception is the initial short step to stablish a common vision and basis scope for the project. It will include analysis of perhaps 10% of the use cases, analysis of the critical non-functional requirements, creation of a business case and preparation of the development enviroment so programing can start in the folowing elaboration phase. You will return variable number os artifacts, but the most important ones are the vision and business case and the initial use cases.

# Evolutionary Requirements in Iterative Methods

| Discipline | Artifact <br>**Iteration $\rightarrow$** | Incep.  <br>**I1** | Elab. <br>**E1..En** | Const. <br>**C1..Cn** | Trans. <br>**T1..T2** |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Business Modeling | Domain Model | | start | | |
| Requirements | Use-Case Model | start | refine | | |
| Requirements | Vision | start | refine | | |
| Requirements | Supplementary Specification | start | refine | | |
| Requirements | Glossary | start | refine | | |
| Requirements | Business Rules | start | refine | | |
| Design | Design Model | | start | refine | |
| Design | SW Architecture Document | | start | | |
| Design | Data Model | | start | refine | |

*Table. Sample UP artifacts and timing.*

- During inception, Vision summarizes the project idea in a form to help decision makers determine if it is worth continuing, and where to start.
- During inception, Supplementary Specification is a high-level description of the key non-functional requirements, especially those that will have a major impact on the architecture.

# What you receive

The orchestrator will give you:
- An idea of a project to explore
- Relevant domain context when available (for example: Spain labor context, and actors such as employee, admin and HR for a work-time registry project)

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
- Be awere that the purpose of the inception phase is not to define all the requirements, or genereate a believable estimate or project plan.
- as you are practising iterative development, be aware of that in this phase, the next artifacts list will be only partially completed, and they will be refined in the following phases. So you should not try to be very precise or complete, but just to have a first version of the vision, business case and use cases that can be refined later. Artifacts shoul be cosidered optional, choose to create only those that really add value to the project. 

## Pair Programming Contract (MANDATORY)

- Driver/Navigator mode is mandatory for the whole skill execution.
- You must work in chat-first mode and co-edit each section with the user.
- Do not write files while exploring and refining scope.
- Before every phase change, ask for explicit approval from the user.
- Required approval token per phase: `OK PASO N` where N is the current step number.
- If approval is missing, continue refining in chat and do not advance.
- Persist artifacts only after steps 1-9 are approved.

## Write Gating Rules (MANDATORY)

- During steps 1-9: no create/update file operations.
- Allowed output during steps 1-9: chat content only (tables, diagrams, brief and fully dressed use cases).
- After user approval of step 9 (`OK PASO 9`): persist artifacts using storage skill.
- If user requests file generation before approvals, ask to confirm skipping pair gates.

## State Tracking Contract (MANDATORY)

You MUST maintain `openspec/state.yaml` as a live tracker of phase progress, step position, and artifact lifecycle. This file is the single source of truth for recovery after compaction.

### Initialization (before PASO 1)

1. Read `openspec/schemas/{schema}/schema.yaml` and map every artifact `id` to the structure expected by `state.yaml`.
2. Initialize `openspec/state.yaml` with:
   - `phase: inception`
   - `iteration: I1`
   - `domain` from the active domain context
   - `status: in_progress`
   - `date` set to today
   - `current_step: 0`, `last_approved_step: 0`
   - `approved_steps: []`
   - `pending_steps: [1, 2, 3, 4, 5, 6, 7, 8, 9]` (chat-only steps; steps 10-12 are automatic/persistence)
   - `scope` and `notes` set to appropriate placeholders
   - `artifacts` populated from schema with `status: not_started`, `created_at_step: null`, `refined_at_steps: []`

### Per-Step Updates

**At the start of each step N:**
- Update `current_step: N`
- For every artifact that this step will work on, set `status: in_progress` (only if currently `not_started`)

**After `OK PASO N` approval:**
- Move N from `pending_steps` to `approved_steps`
- Update `last_approved_step: N`
- For artifacts completed in this step, set `status: approved`
- For artifacts first created in this step, set `created_at_step: N`
- For artifacts refined in this step, append N to `refined_at_steps`
- Update `date` to today

### After Storage Invocation (step 10)

- For every artifact passed to storage, set `status: persisted`
- Do NOT change artifacts that were not part of the storage batch

### Phase Close (step 12)

- Set `status: completed`
- Update `date` to today
- Confirm to user that `state.yaml` reflects completed inception phase

### Artifact-Step Mapping for Inception

| Step | Artifacts worked on |
|------|---------------------|
| 1 | `Vision and Business Case` (first draft) |
| 2 | `Vision and Business Case` (refine goals, scope) |
| 3 | `Use Case Model` (actor-goal table) |
| 4 | `Use Case Model` (diagram + list) |
| 5 | `Use Case brief` (one per use case) |
| 6 | `Requirements Ranking`, `Use Case fully dressed` (10% selected) |
| 7 | Deeper investigation on selected 10% (refines existing artifacts, no new artifact) |
| 8 | `Supplementary Specification` (architectural analysis), Technical Memos |
| 9 | `Vision and Business Case` (refined final version) |
| 10 | Storage — persist all approved artifacts |
| 11 | Development environment setup (no artifact tracked) |
| 12 | Close inception — `status: completed` |

| Artifact | Comment |
|----------|------|
| Vision and Business Case | provides an executive summary. Describes the high-level goals and constraints, the business case, and provides an executice sumary |
| Use-Case Model |  Describes the functional requirements. During inception, the most use cases will be identified and written down as brief format and perhaps 10% of the use cases will be analyzed in detail in a fully dressed format. |
|Supplementary Specification|Describes other requirements, mostly non-functional. During 50 tion, it is useful to have some idea of the key non-functional require ments that have will have a major impact on the architecture|
|Glossary|Key domain terminology, and data dictionary|
|Risk List & Risk Management Plan|Describes the risks (business, technical, resource, schedule) and d for their mitigation or response.|
|Prototypes and proof-of-concepts|To clarify the vision, and validate technical ideas.|
|Iteration Plan|Describes what to do in the first elaboration iteration|
|Phase Plan & Software Development Plan|Low-precision guess for elaboration phase duration and effort. Tool people, education, and other resources.|
|Development Case|A description of the customized UP steps and artifacts for this project In the UP, one always customizes it for the project|

# What you need to do (Pair Programming workflow)

1. Brief fisrt draft of the Vision.
  - Artifact in progress: `Vision and Business Case`.
  - Before drafting, load the active schema instruction for Vision and the active schema template `vision.md`.
  - Even though this is a brief first draft, structure the response using the Vision headings required by the loaded instruction/template. Leave unresolved parts as `TBD` or `pendiente de refinar`.
  - Stop and request `OK PASO 1` before continuing.
2. Identify goals and stakeholders, and speculate what it is in and out of scope for the project. refine it in collaboration with the user.
  - Continue the `Vision and Business Case` artifact using the same Vision instruction/template loaded in `PASO 1`.
  - Update stakeholder goals, user environment, scope boundaries, assumptions, and business framing using the structure required by the Vision artifact.
  - Stop and request `OK PASO 2` before continuing.
3. An actor-goal-use case table is written to the chat window. refine it in collaboration with the user.
  - Artifact in progress: `Use Case Model`.
  - Before drafting, load the active schema instruction for use cases and the active schema template `use-case-model.md`.
  - The actor-goal-use case table is a preparatory view for the Use Case Model and must stay consistent with the use case names that will appear later in the model.
  - Stop and request `OK PASO 3` before continuing.
4. write a use case context diagram and use case list to the chat window. refine it in collaboration with the user.
  - Continue the `Use Case Model` artifact using the same instruction/template loaded in `PASO 3`.
  - The diagram must be written in plantuml grammar, and the use case list must be compatible with the `use-case-model.md` template.
  - Stop and request `OK PASO 4` before continuing.
5. write each use case in brief format to tha chat window one by one and refine each in collaboration with the user before proceeding to the next one.
  - Artifact in progress: `Use Case brief`.
  - Before drafting each brief, load the active schema instruction for use cases and the active schema template `use-case-brief.md`.
  - Keep each brief aligned with the use case names agreed in `PASO 3` and `PASO 4`; do not improvise a different naming scheme or format.
  - Stop and request `OK PASO 5` before continuing.
6. After this, choose 10% of the use cases with a mix of the most architecturally significant, risky and of high business value, explain the reasons why you chose them, and then analyze them in a fully dressed format. refine each in collaboration with the user before proceeding to the next one.
  - Artifacts in progress: `Requirements Ranking` and `Use Case fully dressed`.
  - Before choosing the 10%, load the active schema instruction/template for `Requirements Ranking` and produce an explicit ranking based on risk, coverage, and criticality.
  - The 10% selection must be justified from that ranking; do not choose deep-dive use cases ad hoc.
  - Before drafting each detailed case, load the active schema instruction for use cases and the active schema template `use-case-fully-dressed.md`.
  - Stop and request `OK PASO 6` before continuing.
7. On the 10% selected, investigate a little deeper to better comprehend the magnitude, complexity and risks of the project. write it to the chat window and refine it in collaboration with the user.
  - Continue working from the selected `Requirements Ranking` and `Use Case fully dressed` artifacts.
  - Tie the deeper investigation back to the ranking criteria, the fully dressed special requirements, open issues, risks, and implementation uncertainty already surfaced.
  - Stop and request `OK PASO 7` before persisting artifacts.
8. Start architectural analysis using the `/architectural-analysis/SKILL.md` with the key non-functional requirements that will have a major impact on the architecture. refine it in collaboration with the user.
 - After approval, if new discoveries during architectural analysis require changes to supplementary specification or technical memos, update them in collaboration with the user. They should be stored under `openspec/artifacts/{domain}/02 Requirements/supplementary-specification.md` and `openspec/artifacts/{domain}/02 Requirements/Technical memos/Issue - {{FURPS+ category}} - {{issue.name}}.md` respectively, using the storage skill and following the active Artifact Store Policy.
  - Stop and request `OK PASO 8` before persisting artifacts.
9. Refine the Vision, summarizing information from previous steps, and write it to the chat window. refine it in collaboration with the user.
  - Return to the `Vision and Business Case` artifact and reload the active schema instruction/template for Vision before drafting the refined version.
  - The final Vision must conform to the same artifact structure used in `PASO 1` and `PASO 2`, enriched with validated information from the Use Case Model, Requirements Ranking, and Supplementary Specification.
  - Stop and request `OK PASO 9` before proceeding to storage.
10. **Immediately invoke the [storage](../storage/SKILL.md) skill to persist the artifacts approved in steps 1-9, following the active Artifact Store Policy.**
  - Treat this as an automatic step, not a user-driven action.
  - Pass only approved artifacts to storage.
  - Persist approved inception artifacts directly under the discipline directories defined in `openspec-convention.md`; most inception artifacts land in `openspec/artifacts/{domain}/02 Requirements/`, while `Requirements Ranking` must be stored as `openspec/artifacts/{domain}/08 Project Management/Requirements Ranking.md`.
  - If no policy is detected, storage must default to `openspec` and create the required folders.
11. **Immediately invoke the [set-development-environment](../set-development-enviroment/SKILL.md) skill to set up the development environment for the project.**
  - Treat this as an automatic step, not a user-driven action.
  - Pass the project context you just created to the skill without asking the user to do it in chat.
  - If no context is detected, the skill must default to a standard setup.
12. Close inception persistence in master-only mode.
  - Treat this as an automatic step, not a user-driven action.
  - Do NOT create, move, or archive folders under `openspec/iterations/`.
  - Do NOT run delta merge operations.
  - Confirm to the user that approved artifacts are already persisted directly under `openspec/artifacts/{domain}/...`.

## Required Turn Template

For each step, always respond in this order:
1. Proposed draft for the current step (short and reviewable).
2. Open questions or assumptions.
3. Explicit approval request: `Escribe OK PASO N para continuar`.

Do not include content for later steps until approval is received.

## Pre-Approval Validation (MANDATORY)

Before asking for `OK PASO N`, verify internally that:

- The step loaded the correct instruction and template files from the active schema or valid fallback.
- The response uses section names and order compatible with the artifact in progress.
- Mandatory tables are present when required by the instruction/template.
- Required PlantUML blocks are present when the artifact calls for a diagram.
- `PASO 6` explicitly applies risk, coverage, and criticality before selecting the 10% to deepen.
- Missing information is marked as `TBD` or `pendiente de refinar`, not omitted.
- The response does not leak content from later steps.

## Anti-Patterns
- skipping the schema bootstrap or drafting without loading the relevant instruction/template files first.
- ignoring available files in `openspec/schemas/...` or `.agents/skills/storage/openspec/schemas/...` and improvising the structure.
- using ad hoc headings that conflict with the active template for the current artifact.
- selecting the 10% deep-dive use cases without an explicit ranking by risk, coverage, and criticality.
- generating complete artifact files before user approvals in steps 1-9.
- skipping explicit approval checkpoints between steps.
- writing multiple phases in one response without waiting for user feedback.
- atempt to define all the requirements.
- expect reliable estimates or plans.
- persisting approved artifacts into `openspec/iterations/{iteration}/...` instead of direct master paths.
- attempting archive or delta-merge operations in master-only persistence mode.
define the architecture
- believe that the proper sequence of work should be:
  1. define all the requirements
  2. define the architecture
  3. do the implementation
- theres is no vision o business case.
- all use cases were written in detail.
- none of the ues cases were written in detail.

# Results

Here you will return the artifacts you created, and a summary of the decisions you took and why. IS adviseable to include any open questions or concerns that should be addressed in the following elaboration phase.
