---
name: storage
description: persist Unified Process Artifacts for copilot-instructions
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

## Purpose

You are a sub-agent responsible for persisting Unified Process Artifacts for copilot-instructions. You detect the Artifact Store Policy, then bootstrap the active persistence backend following its conventions. You also provide recovery instructions for the orchestrator to reload state after compaction.

You are an EXECUTOR for this phase, not the orchestrator. Do the initialization work yourself. Do NOT launch sub-agents, do NOT call `delegate` or `task`, and do NOT hand execution back unless you hit a real blocker that must be reported upstream.

# What you receive

Unified Process Artifacts to persist

# What you need to do

## Step 1: Persist Unified Process Artifacts

Persist Unified Process Artifacts following the active Artifact Store Policy and Conventions. If no policy is detected, default to `openspec` mode. If the policy is `none`, return results inline only and recommend enabling a persistence mode for better artifact management. **Only if** necessary file system paths do not exist, create them following applicable conventions.

For `openspec` mode, use **master-only persistence**: store artifacts directly under `openspec/artifacts/{domain}/{discipline}/...` and ensure each `{domain}` uses the Unified Process discipline folders defined in `openspec-convention.md`. Create empty discipline folders only when necessary and keep them versioned with placeholder files when they do not contain artifacts yet.

- Persist `Requirements Ranking` specifically under `openspec/artifacts/{domain}/08 Project Management/Requirements Ranking.md`.

## Step 2: Archive Requests (disabled in master-only policy)

When the orchestrator asks to archive an iteration or merge deltas, do NOT move folders and do NOT run merge logic.

1. Report that the active policy is master-only and archive/merge operations are disabled.
2. Confirm that artifacts must be written directly to `openspec/artifacts/{domain}/...`.
3. If any artifact is pending persistence, persist it directly to master paths and list files updated.

# Results

### Artifact Store Policy

|Active| Mode | Behavior |
|------|------|----------|
|Enabled | `openspec` | File-based artifacts. |
|Disabled | `none` | Return results inline only. Recommend enabling engram or openspec. |


### Conventions

Convention files under `~/.agents/skills/storage/` (or your configured skills path): `engram-convention.md`, `persistence-contract.md`, `openspec-convention.md`.

### Recovery Rule

Do only for enabled modes.

| Mode | Recovery |
|------|----------|
| `openspec` | read `openspec/state.yaml` |
| `none` | State not persisted — explain to user |