# OpenSpec File Convention (shared across all SDD skills)

This convention is schema-agnostic. Workflow-specific organization (such as the
Unified Process discipline directories) belongs to the active schema under
`openspec/schemas/{schema}/`, never to this file.

## Directory Structure

```
openspec/
├── config.yaml              <- Global domain router (list of domains only: no defaults, no state)
├── schemas/
│   └── {schema}/
│       ├── templates/       <- Templates for creating artifacts
│       ├── instructions/    <- Instructions for creating artifacts
│       ├── schema.yaml      <- Artifact layout (paths, templates, instructions, requires, disciplines)
│       └── state.template.yaml <- Domain state template for this schema
├── artifacts/               <- Source of truth (main specs)
│   └── {domain}/
│       ├── config.yaml      <- Domain config (schema, artifacts_root, rules, tdd)
│       ├── state.yaml       <- Domain state tracking (phase, steps, artifact lifecycle)
│       └── ...              <- Layout derived from the active schema `path` fields
```

The concrete layout inside each `{domain}` is **derived from the active schema**, not from this file. Each artifact declares its `path` in `openspec/schemas/{schema}/schema.yaml`. A schema may also declare its own domain state template at `openspec/schemas/{schema}/state.template.yaml` (grouping state entries however that workflow requires).

## Path Resolution

- Artifact paths are NOT hardcoded in any skill. They live in the active schema's `path` field per artifact.
- The storage skill resolves every read/write with its **Path Resolution Contract**:
  1. Read the domain config (`schema`, `artifacts_root`).
  2. Read `openspec/schemas/{schema}/schema.yaml` (fallback: seed copy under `.agents/skills/storage/openspec/schemas/{schema}/`).
  3. Look up the artifact by `id` → `path`.
  4. Resolve placeholders (`{{#}}`, `{{Iteration}}`, `{{use-case.name}}`, `{{scenario.#}}`, `{{FURPS+ category}}`, `{{issue.name}}`, `{{fully.qualified.package}}`) with caller-supplied values.
  5. Final path = `{artifacts_root}/{path}`.
- `{{#}}` resolves to the zero-padded numeric part of the iteration (`E1 -> 01`, `E11 -> 11`).
- Scenario variants may append ` - S{{scenario.#}}` before the file extension when the caller supplies `{{scenario.#}}`.
- Templates and instructions are declared per artifact in the same schema (`template` and `instruction` fields). Use them as the contract for headings, tables, diagrams, and minimum content.

## Writing Rules

- Always write directly to the resolved master path under `openspec/artifacts/{domain}/...`.
- If a file already exists, READ it first and UPDATE it (do not overwrite blindly).
- Artifacts whose schema `path` contains `{{#}}` or `{{Iteration}}` are iteration-scoped: each iteration resolves to a NEW file (e.g. `01 E1 domain-to-design-transition.md`). The read-then-update rule does not apply across iterations, only when re-persisting within the same iteration.
- Do NOT create or use `openspec/iterations/` folders for artifact persistence.
- Place each artifact in the path resolved from the active schema; never hardcode artifact paths in instructions.
- Keep empty directories versioned with a placeholder such as `.gitkeep`.
- Use `openspec/artifacts/{domain}/config.yaml` `rules` section for domain-specific constraints per phase.

## Configuration and State (per domain)

- The global `openspec/config.yaml` is ONLY a domain router: it lists `domains` (each with its `config_path`). It holds no defaults, no rules and no state.
- Each domain owns its configuration at `openspec/artifacts/{domain}/config.yaml` (schema, `artifacts_root`, context, rules, tdd, persistence mode).
- Each domain owns its state at `openspec/artifacts/{domain}/state.yaml`; the storage skill creates it from the active schema's `state.template.yaml` when the domain is registered.
- There is no global state file. Recovery: read the router, then each domain state; resume the domain with `status: in_progress` (if several, ask the user).

## Archive Policy (Master-Only)

- Do NOT create or move `openspec/iterations/{iteration}/` folders.
- Do NOT run archive or delta-merge operations.
- Use version control history (for example, Git commits) as the audit trail for specification changes.
