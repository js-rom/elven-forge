# Step 0 — Domain Bootstrap (automatic)

## Inputs
- Project idea and detected stack.
- Seed `domain-config.template.yaml` and the active schema's `state.template.yaml`.
- Global router `openspec/config.yaml`.
- Storage skill, Step 1 (Register Domain).

## Output contract
- Follow the storage skill Step 1 exactly. This step creates infrastructure, not artifacts.
- `openspec/artifacts/{domain}/config.yaml` from the template, with `domain` and `artifacts_root`.
- `openspec/artifacts/{domain}/journal/` with `.gitkeep`.
- `openspec/artifacts/{domain}/state.yaml` from the state template, initialized with:
  - `phase: inception`, `iteration: I1`, `status: in_progress`, today's date;
  - `current_step: 0`, `last_approved_step: 0`, `approved_steps: []`;
  - `pending_steps: [1, 2, 3, 4, 5, 6, 7, 8, 9]` (10-12 are automatic);
  - `scope` and `summary` placeholders; `journal: journal/I1`; `approvals: []`;
  - `artifacts` populated from the schema with `not_started`.
- Add the domain to `openspec/config.yaml` under `domains:`.

## Preconditions
- `openspec/artifacts/{domain}/` does not exist. If it exists, do not recreate it: report and continue.
- `openspec/` seed already copied by `/init`.

## Rubric
- No per-domain settings duplicated in the global router.
- No `artifact-index.json` is created (it is derived).
- Artifact directories follow the schema `path` parents, with `.gitkeep` for empty ones.

## Evidence required
- Files created and the router entry.
- Journal record for the bootstrap.
- No approval token: report and continue to step 1.

## Anti-patterns
- Registering the domain twice.
- Putting schema, rules or state in the global router.
- Creating artifacts or writing history in this step.
