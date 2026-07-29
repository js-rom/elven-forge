---
name: init
description: >
  Initialize Spec-Driven Development context in any project. Detects stack, conventions, and bootstraps the active persistence backend.
  Trigger: When user wants to initialize SDD in a project, or says "sdd init", "iniciar sdd", "openspec init".
license: MIT
metadata:
  author: js-rom
  version: "2.0"
---

## Purpose

You are a sub-agent responsible for initializing the Spec-Driven Development (SDD) context in a project. You detect the project stack and conventions, then bootstrap the active persistence backend.

You are an EXECUTOR for this phase, not the orchestrator. Do the initialization work yourself. Do NOT launch sub-agents, do NOT call `delegate` or `task`, and do NOT hand execution back unless you hit a real blocker that must be reported upstream.

## Execution and Persistence Contract

- Read and follow `skills/storage/openspec-convention.md`. Run full bootstrap.


## What to Do


### Step 1: Detect Project Context

Read the project to understand:
- Tech stack (check package.json, go.mod, pyproject.toml, etc.)
- Existing conventions (linters, test frameworks, CI)
- Architecture patterns in use

### Step 2: Copy OpenSpec Seed to Project Root

When this skill is launched, run the following terminal command from the project root to copy the full `openspec` seed and all contents:

```powershell
New-Item -ItemType Directory -Path "./openspec" -Force | Out-Null
Copy-Item -Path "./.agents/skills/storage/openspec/*" -Destination "./openspec" -Recurse -Force
```

Notes:
- This command MUST run before generating/updating config files.
- If `openspec/` already exists, this command **DO NOT** update/overwrite files with the seed content.

### Step 3: Build Skill Registry

Follow the same logic as the `skill-registry` skill (`skills/skill-registry/SKILL.md`):

1. Scan user skills: glob `*/SKILL.md` across ALL known skill directories. **User-level**: `~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.gemini/skills/`, `~/.cursor/skills/`, `~/.copilot/skills/`, parent of this skill file. **Project-level**: `.claude/skills/`, `.gemini/skills/`, `.agent/skills/`, `skills/`. Skip `sdd-*`, `_shared`, `skill-registry`. Deduplicate by name (project-level wins). Read frontmatter triggers.
2. Scan project conventions: check for `agents.md`, `AGENTS.md`, `CLAUDE.md` (project-level), `.cursorrules`, `GEMINI.md`, `copilot-instructions.md` in the project root. If an index file is found (e.g., `agents.md`), READ it and extract all referenced file paths — include both the index and its referenced files in the registry.
3. **ALWAYS write `.atl/skill-registry.md`** in the project root (create `.atl/` if needed). This file is mode-independent — it's infrastructure, not an SDD artifact.

See `skills/skill-registry/SKILL.md` for the full registry format and scanning details.

### Step 7: Return Summary

Return a structured summary for `openspec`:
```
## SDD Initialized

**Project**: {project name}
**Stack**: {detected stack}
**Persistence**: openspec

### Next Steps
Ready for /up-inception <topic>.
```

## Rules

- ALWAYS detect the real tech stack, don't guess
- NEVER behave like the orchestrator from this phase - execute directly and return results
- If the project already has an `openspec/` directory, report what exists and ask the orchestrator if it should be updated
- Keep config.yaml context CONCISE - no more than 10 lines
- Return a structured envelope with: `status`, `executive_summary`, `detailed_report` (optional), `artifacts`, `next_recommended`, and `risks`