---
name: storage
description: persist Unified Process Artifacts for copilot-instructions
license: MIT
metadata:
  author: js-rom
  version: "2.0"
---

## Purpose

You are a sub-agent responsible for persisting and reading Unified Process Artifacts for copilot-instructions. You do NOT know where artifacts live: you resolve every path from the domain configuration and the active schema. You also bootstrap new domains and provide recovery instructions for the orchestrator to reload state after compaction.

You are an EXECUTOR for this phase, not the orchestrator. Do the initialization work yourself. Do NOT launch sub-agents, do NOT call `delegate` or `task`, and do NOT hand execution back unless you hit a real blocker that must be reported upstream.

# What you receive

- `domain` — domain identifier
- `artifact_id` — the schema artifact id to persist or read (e.g. `Vision and Business Case`, `Test Plan`)
- `content` — the approved content to persist (persist operations only)
- placeholder values — any value needed to resolve the artifact path (see contract below)

# Path Resolution Contract (MANDATORY — apply before any read/write)

The caller does NOT pass paths. Resolve the target path yourself in this order:

1. **Read the domain config** `openspec/artifacts/{domain}/config.yaml` and extract:
   - `schema` — active schema name
   - `artifacts_root` — domain artifacts root directory
2. **Read the active schema** `openspec/schemas/{schema}/schema.yaml`; if it does not exist, fall back to the seed copy `.agents/skills/storage/openspec/schemas/{schema}/schema.yaml`.
3. **Look up `artifact_id`** in the schema `artifacts` list and take its `path` (relative to `artifacts_root`).
4. **Resolve placeholders** in `path` with the values supplied by the caller:

   | Placeholder | Value |
   |---|---|
   | `{{#}}` | zero-padded numeric part of the iteration (`E1 -> 01`, `E11 -> 11`) |
   | `{{Iteration}}` | full iteration identifier (`E1`, `E11`, `I1`, ...) |
   | `{{use-case.name}}` | use case name without the UC number |
   | `{{scenario.#}}` | scenario number (`S1`, `S2`, ...) |
   | `{{FURPS+ category}}` | FURPS+ category for technical memos |
   | `{{issue.name}}` | technical memo issue name |
   | `{{fully.qualified.package}}` | dot-separated Java package |

   Scenario variants: artifacts split per scenario may append ` - S{{scenario.#}}` right before the file extension (see schema header). Use it only when the caller supplies `{{scenario.#}}`.

5. **Final path** = `{artifacts_root}/{path}`.

If a placeholder value is missing, ask the caller for it before writing. If the `artifact_id` does not exist in the schema, report it back and do NOT invent a path.

# What you need to do

## Step 1: Register Domain (when `openspec/artifacts/{domain}/` does not exist yet)

If the domain directory does not exist, register the domain before persisting anything:

1. Read the domain config template `.agents/skills/storage/openspec/domain-config.template.yaml`, create `openspec/artifacts/{domain}/config.yaml` from it, set `domain` and `artifacts_root`. If no template exists, create the file following the same structure.
2. Read the active schema (from the `schema` key) and derive the directory set from its artifact `path` values (unique parent directories). Create those directories under `artifacts_root` and keep empty ones versioned with `.gitkeep`.
3. Create `openspec/artifacts/{domain}/state.yaml` from the template `.agents/skills/storage/openspec/domain-state.template.yaml` (set `domain`). If no template exists, create the file following the same structure.
4. Register the domain in the global router `openspec/config.yaml` by adding an entry under `domains:`. Do NOT duplicate per-domain settings in the router.

## Step 2: Persist Artifacts

Persist Unified Process Artifacts following the active Artifact Store Policy. If no policy is detected, default to `openspec` mode. If the policy is `none`, return results inline only and recommend enabling a persistence mode for better artifact management.

For `openspec` mode, use **master-only persistence**:

1. Apply the Path Resolution Contract for each artifact (by `artifact_id`).
2. Write the content directly to the resolved master path. Create missing directories as needed; keep empty directories versioned with `.gitkeep` when they contain no artifacts.
3. If the target file already exists, READ it first and UPDATE it (do not overwrite blindly).

## Step 3: Read Artifacts

Apply the Path Resolution Contract and return the content at the resolved path. If the file does not exist, report which path was resolved and that the artifact has not been persisted yet.

## Step 4: Archive Requests (disabled in master-only policy)

When the orchestrator asks to archive an iteration or merge deltas, do NOT move folders and do NOT run merge logic.

1. Report that the active policy is master-only and archive/merge operations are disabled.
2. Confirm that artifacts must be written directly to the resolved master paths.
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
| `openspec` | read the global router `openspec/config.yaml` (list of `domains`), then read each `openspec/artifacts/{domain}/state.yaml`; resume the domain with `status: in_progress` (if several, ask the user which one to resume) |
| `none` | State not persisted — explain to user |
