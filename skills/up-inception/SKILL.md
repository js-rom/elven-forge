---
name: up-inception
description: Establish a common vision and basis scope for the project. Investigate to form a rational, justifiable opinion of the overall purpose and feasibility of the potential new system, and decide if it is worthwhile to invest in deeper exploration.
license: MIT
metadata:
  author: js-rom
  version: "2.0"
---

# Purpose

You are the driver for the INCEPTION phase of the Unified Process. Inception establishes a common vision, the initial scope, the first use cases and the business case, and prepares the environment so elaboration can start with production code.

This is not a requirements-complete phase. Most artifacts are partial by design and will be refined during elaboration.

# What you receive

- The project idea and the domain context provided by the user.
- The detected stack and project files.
- The domain config `openspec/artifacts/{domain}/config.yaml` (fallback: the seed template).

# Step Router (MANDATORY)

1. Read `openspec/artifacts/{domain}/state.yaml`. If it is missing, run step 0 (domain bootstrap) before anything else.
2. Resolve the current step: `current_step` if it is still in `pending_steps`; otherwise the first pending step. Steps 10-12 are automatic.
3. Load **only** `.agents/steps/inception/<contract>.md` for that step. Do not load other step contracts.
4. `.agents/flows/inception.flow.yaml` is the readable map; `.agents/flows/inception.checks.json` is the machine manifest.
5. Before requesting a gate, verify the token with `python .agents/scripts/gate.py --token "<token>"`. Proceed only on exit 0.
6. After approval, append the journal record, update `state.yaml`, and render the progress overview.

# Step contracts

| Step | Contract | Produces |
|---|---|---|
| 0 | `00-domain-bootstrap.md` | Infrastructure: config, state, journal, router |
| 1 | `01-vision-draft.md` | Vision and Business Case |
| 2 | `02-vision-scope.md` | Vision and Business Case |
| 3 | `03-actor-goal-table.md` | Use Case Model |
| 4 | `04-use-case-model.md` | Use Case Model |
| 5 | `05-use-case-briefs.md` | Use Case brief |
| 6 | `06-ranking-10pct.md` | Requirements Ranking, Use Case fully dressed |
| 7 | `07-deep-investigation.md` | No new artifact (refines) |
| 8 | `08-architectural-analysis.md` | Supplementary Specification, Technical Memo |
| 9 | `09-vision-final.md` | Vision and Business Case |
| 10 | `10-persist-batch.md` | Persistence batch (automatic) |
| 11 | `11-development-environment.md` | Environment setup (automatic) |
| 12 | `12-phase-close.md` | Phase close (automatic) |

# Schema Bootstrap Contract (MANDATORY)

1. Resolve the active schema from the domain config (`schema` key) and read `schema.yaml`. Map `artifact -> path -> instruction -> template`.
2. Resolve schema assets in this order: `openspec/schemas/{schema}/...`, then `.agents/skills/storage/openspec/schemas/{schema}/...`.
3. The `instruction` field may be a link expression (`INVOKE this link -> "./instructions/x.md"`). Extract the path inside the quotes and resolve it relative to the schema directory.
4. Before each step, load the instruction and template that the step contract names. Instruction wins for content rules; template wins for section names and order.
5. If an `instruction` is empty or its file is missing, do not stop: use the template and the skill named in the step contract, and record the fallback in the step's journal record.
6. A section that cannot be completed stays with `TBD` or `pendiente de refinar`; never omit it.
7. The schema is the authority for paths. Never hardcode an artifact path.

# Pair Programming Contract (MANDATORY)

- Driver/navigator for the whole phase; chat-first.
- Steps 1-9 are chat-only: no file writes, no artifact persistence.
- The user keeps typing `OK PASO N`; `gate.py` accepts the legacy forms and normalizes them.
- Do not advance without the explicit token. If it is missing, keep refining in the same step.
- If the user asks for file generation before the gates, confirm that the pair gates will be skipped.

# Batch Persistence Contract (MANDATORY)

- All approved artifacts are persisted in a single batch at step 10, by `artifact_id`; storage resolves the paths.
- No per-step persistence in steps 1-9.
- Domain config values refined during steps 1-9 are persisted in the same batch.
- After the batch, set every persisted artifact to `status: persisted` and write one journal record.

# State Tracking Contract (MANDATORY)

- Initialize at step 0: `phase: inception`, `iteration: I1`, `status: in_progress`, `pending_steps: [1, 2, 3, 4, 5, 6, 7, 8, 9]`, `summary`, `journal: journal/I1`, `approvals: []`.
- At step start: set `current_step` and mark the step artifacts `in_progress`.
- After a gate: move the step to `approved_steps`, update `last_approved_step`, append the approval (token + draft hash), mark artifacts `approved`.
- After the batch: mark them `persisted`.
- `summary` is at most five lines. History and evidence go to `journal/I1/` (append-only). Never write `notes` to `state.yaml`.
- Recovery: router -> state -> `journal/I1/index.json` -> last two records.

# Automatic Steps

- After `OK 9`, run steps 10, 11 and 12 in order, setting `current_step` to each one. They have no approval token.
- Step 10 persists the batch; step 11 sets up the environment (writes outside artifacts, requires confirmation); step 12 sets `status: completed` and hands off.
- They are not silent: report what was written, the commands run, and the journal record.
- Step 12 closes the phase only when every approved artifact is persisted, and hands off per `.agents/contracts/handoff-inception-elaboration.md`.

# Required Turn Template

For steps 1-9, always respond in this order:

1. Proposed draft for the current step only.
2. Open questions or assumptions.
3. Explicit gate request: `Escribe OK PASO N para continuar`.

Do not include content for later steps.

# Anti-Patterns

- Trying to define all requirements or produce a reliable project plan.
- Defining architecture before elaboration, or skipping the business case.
- Writing fully dressed use cases for everything, or for none.
- Skipping the ranking before selecting the 10%.
- Persisting per step instead of the single batch.
- Skipping gates, or writing several steps in one response.
- Persisting under `openspec/iterations/` or merging deltas.
- Writing history to `state.yaml` instead of `journal/I1/`.

# Results

Return the artifacts produced, the decisions taken and why, and the open questions and risks that elaboration must address. Hand off per `.agents/contracts/handoff-inception-elaboration.md`.
