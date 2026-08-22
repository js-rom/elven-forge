# OpenSpec File Convention (shared across all SDD skills)

## Directory Structure

```
openspec/
├── config.yaml              <- Global domain router (list of domains only: no defaults, no state)
├── schemas/
│   └── default/
│       ├── templates/       <- Default templates for creating artifacts
│       ├── instructions/    <- Default instructions for creating artifacts
│       └── schema.yaml      <- Artifact layout (paths, templates, instructions, requires)
├── artifacts/               <- Source of truth (main specs)
│   └── {domain}/
│       ├── config.yaml      <- Domain config (schema, artifacts_root, rules, tdd)
│       ├── state.yaml       <- Domain state tracking (phase, steps, artifact lifecycle)
│       ├── 01 Business Modeling/
│       ├── 02 Requirements/
│       ├── 03 Design/
│       ├── 04 Implementation/
│       ├── 05 Test/
│       ├── 06 Deployment/
│       ├── 07 Configuration & CM/
│       ├── 08 Project Management/
│       └── 09 Enviroment/
```

The concrete layout inside each discipline directory is **derived from the active schema**, not from this file. Each artifact declares its `path` in `openspec/schemas/{schema}/schema.yaml`.

## Discipline Directories

| Directory | Purpose |
|-----------|---------|
| `01 Business Modeling` | Domain-level business concepts and relationships |
| `02 Requirements` | Vision, use cases, supplementary requirements, glossary, domain rules, architectural analysis, and technical memos |
| `03 Design` | Logical design and architecture artifacts (logical view, data model, UI, SW architecture document) |
| `04 Implementation` | Implementation-level artifacts (reserved) |
| `05 Test` | Test artifacts |
| `06 Deployment` | Deployment artifacts |
| `07 Configuration & CM` | Configuration and change-management artifacts |
| `08 Project Management` | Project planning and tracking artifacts |
| `09 Enviroment` | Environment setup and support artifacts |

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
- Do NOT create or use `openspec/iterations/` folders for artifact persistence.
- Within each `{domain}`, always place artifacts in the correct Unified Process discipline directory (resolved from the schema).
- Keep empty discipline directories versioned with a placeholder such as `.gitkeep`.
- Use `openspec/artifacts/{domain}/config.yaml` `rules` section for domain-specific constraints per phase.

## Configuration and State (per domain)

- The global `openspec/config.yaml` is ONLY a domain router: it lists `domains` (each with its `config_path`). It holds no defaults, no rules and no state.
- Each domain owns its configuration at `openspec/artifacts/{domain}/config.yaml` (schema, `artifacts_root`, context, rules, tdd, persistence mode).
- Each domain owns its state at `openspec/artifacts/{domain}/state.yaml` (phase, iteration, steps, artifact lifecycle).
- There is no global state file. Recovery: read the router, then each domain state; resume the domain with `status: in_progress` (if several, ask the user).

## Archive Policy (Master-Only)

- Do NOT create or move `openspec/iterations/{iteration}/` folders.
- Do NOT run archive or delta-merge operations.
- Use version control history (for example, Git commits) as the audit trail for specification changes.
