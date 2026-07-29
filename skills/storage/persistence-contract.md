# Persistence Contract (shared across all SDD skills)

## Behavior Per Mode

| Mode | Read from | Write to | Project files |
|------|-----------|----------|---------------|
| `openspec` | Filesystem | Filesystem | Yes |
| `none` | Orchestrator prompt context | Nowhere | Never |

## State Persistence (Orchestrator)

The orchestrator persists DAG state after each phase transition to enable SDD recovery after compaction.

| Mode | Persist State | Recover State |
|------|--------------|---------------|
| `openspec` | Write `openspec/state.yaml` | Read `openspec/state.yaml` |
| `none` | Not possible — warn user | Not possible |

## Common Rules

- `none` → do NOT create or modify any project files; return results inline only
- `openspec` → write files ONLY to paths defined in [openspec-convention](./openspec-convention.md)
- `openspec` → use master-only persistence under `openspec/artifacts/{domain}/...` (no iteration delta folders, no archive merge)
- If unsure which mode to use, default to `none`

## Sub-Agent Context Rules

Sub-agents launch with a fresh context and NO access to the orchestrator's instructions or memory protocol.

Who reads, who writes:
- UP (phase with dependencies): sub-agent reads artifacts directly from backend; sub-agent saves its artifact
- UP (phase without dependencies, e.g. inception): nobody reads; sub-agent saves its artifact

## Skill Registry

The orchestrator pre-resolves compact rules from the skill registry and injects them as `## Project Standards (auto-resolved)` in your launch prompt. Sub-agents do NOT read the registry or individual SKILL.md files — rules arrive pre-digested.

To generate/update: run the `skill-registry` skill, or run `sdd-init`.

Sub-agent skill loading: check for a `## Project Standards (auto-resolved)` block in your prompt — if present, follow those rules. If not present, check for `SKILL: Load` instructions as a fallback. If neither exists, proceed without — this is not an error.

## Detail Level

The orchestrator may pass `detail_level`: `concise | standard | deep`. This controls output verbosity but does NOT affect what gets persisted — always persist the full artifact.
