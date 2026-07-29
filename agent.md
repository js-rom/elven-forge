## Unified Process Orchestrator

## Global Priority Rules

Apply these rules in every task in this repository, even if the prompt does not mention OpenSpec.

1. Always apply and follow:
	- [abstract-orchestrator](./skills/utils/abstract-orchestrator.md)
	- [storage backend skill](./skills/storage/SKILL.md)
	- [OpenSpec convention](./skills/storage/openspec-convention.md)
2. Treat OpenSpec artifacts as source of truth:
	- Main specs and active work: openspec/artifacts/
3. Never overwrite existing artifacts blindly:
	- If a target file exists, read it first and update it.
4. Use master-only persistence for OpenSpec artifacts (no iteration delta folders and no archive merge workflow).
5. Code language policy:
	- All source code, tests, identifiers, and code comments MUST be written in English.
	- User-facing product text may follow explicit artifact or business language requirements.

## Workflow

This workflow is the planning layer for iterative and incremental Unified Process development.

### Commands

- /up-init -> run up-init
- /up-inception <topic> -> run up-inception

### Dependency Graph

inception -> elaboration -> construction -> transition

### Result Contract

Each phase returns: status, executive_summary, artifacts, next_recommended, risks.

### Sub-Agent Launch Pattern

All sub-agent prompts that read, write, or review code must include pre-resolved compact rules from the skill registry.

Orchestrator skill resolution (once per session):
1. Read .copilot/skills/skill-registry.md
2. Cache the Compact Rules section and User Skills trigger table
3. If no registry exists, warn and continue without project-specific standards

For each sub-agent launch:
1. Match relevant skills by task and code context
2. Copy matching compact rule blocks into prompt section: Project Standards (auto-resolved)
3. Inject those standards before task-specific instructions

### OpenSpec Storage Contract

When creating or updating OpenSpec artifacts:
1. Ensure openspec/config.yaml exists and use its rules section for project constraints.
2. Ensure the master path `openspec/artifacts/{domain}/` exists before writing artifacts.
3. Use schema templates and instructions from openspec/schemas/default/.
4. Write artifacts directly under `openspec/artifacts/{domain}/{discipline}/...`.
5. Organize each `{domain}` by the Unified Process discipline directories `01 Business Modeling` through `09 Enviroment`.
6. Do not create or use `openspec/iterations/` for persistence; do not run archive/merge flows.

### Sub-Agent Context Protocol

Sub-agents start with fresh context and no memory. The orchestrator controls references and artifact paths.

For UP phases with required dependencies, pass artifact references (paths or keys), not copied content.

### Recovery Rule

To recover previous session context, apply storage backend rules from [storage backend skill](./skills/storage/SKILL.md).


## Pair programming

### Pair-First Workflow Policy

- If a skill explicitly requires pair programming, that requirement has priority over automation.
- Operate in driver/navigator mode with the user for every phase.
- Work chat-first while refining analysis artifacts.
- Do not write or update project artifacts until the current phase is approved.

### Approval Gates

- Use explicit checkpoints between phases.
- Expected approval token format: `OK PASO N`.
- Do not proceed to the next phase until the approval token for the current phase is received.
- If approval is missing, ask focused clarification questions and keep working in the same phase.

### Write Safety Rules

- For pair-programming skills, allow at most one artifact write batch after approval gates are completed.
- If the user asks to skip gates, request explicit confirmation of skip behavior before writing.
- Persist only approved content.

### Response Contract for Pair Programming

For each phase response, always include:
1. Draft proposal for the current phase only.
2. Open questions and assumptions.
3. Explicit checkpoint request to continue.

### Anti-Patterns

- Generating full artifacts in one pass without review checkpoints.
- Advancing to later phases without user validation.
- Treating pair-programming instructions as optional guidance.