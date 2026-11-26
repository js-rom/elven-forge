---
name: up-elaboration
description: builds the project's core architecture, define most requirements, and estimates the overall schedule and resources.
license: MIT
metadata:
  author: js-rom
  version: "2.0"
---

# Purpose

You are the driver for the ELABORATION phase of the Unified Process. Elaboration builds the core architecture, defines most requirements, and produces production-quality slices through short, risk-driven iterations.

Key ideas: short timeboxed iterations; program early; test early and realistically; adapt from feedback; refine requirements once per iteration.

## What you receive

- The inception handoff: `.agents/contracts/handoff-inception-elaboration.md` and the inherited artifacts.
- The project files, to detect stack and code patterns.
- The domain config `openspec/artifacts/{domain}/config.yaml` (fallback: the seed template).

# Step Router (MANDATORY)

1. Read `openspec/artifacts/{domain}/state.yaml`. If it is missing, initialize it from the active schema's `state.template.yaml` and register the domain per the storage skill.
2. If `phase: inception` and `status: completed`, apply `.agents/contracts/handoff-inception-elaboration.md`: switch to `phase: elaboration`, `iteration: E1`, `status: in_progress`, and keep the inherited artifacts and their statuses.
3. Resolve the current step: `current_step` if it is still in `pending_steps`; otherwise the first pending step.
4. Load **only** `.agents/steps/elaboration/<contract>.md` for that step. Do not load other step contracts.
5. `.agents/flows/elaboration.flow.yaml` is the readable map; `.agents/flows/elaboration.checks.json` is the machine manifest. Use them to route, not as content.
6. Before requesting a gate, verify the token with `python .agents/scripts/gate.py --token "<token>"`. Proceed only on exit 0.
7. After approval and persistence, append the journal record, update `state.yaml`, and render the progress overview.

# Step contracts

| Step | Contract | Produces |
|---|---|---|
| 0 | `00-glossary.md` | Glossary |
| 1 | `01-iteration-plan.md` | Requirements Ranking, Iteration Plan, Ledger entry |
| 2 | `02-domain-model.md` | Domain Model |
| 3 | `03-ssd.md` | System Sequence Diagrams |
| 4 | `04-operation-contracts.md` | Operation Contracts |
| 5 | `05-ui-design.md` | Design System, Visual Specs, Interaction Spec, UI Technology Mapping |
| 6 | `06-reports-design.md` | TBD (no artifact) |
| 7 | `07-architectural-analysis.md` | Architectural Analysis, Technical Memos, Supplementary Spec |
| 8 | `08-logical-view-packages.md` | Logical View Package Diagram |
| 9A | `09a-domain-to-design.md` | Domain-to-Design Transition Map |
| 9B | `09b-scenario-design.md` | Design Sequence Diagram, Logical View Class Diagram |
| 10 | `10-use-case-realization.md` | Use Case Realization |
| 11 | `11-reviewer-pass.md` | Reviewed 8/9A/9B/10 artifacts |
| 12 | `12-data-model-jpa.md` | Data Model, JPA Mapping |
| 13 | `13-sw-architecture-document.md` | SW Architecture Document |
| 14A | `14a-acceptance-atdd.md` | Acceptance Test Plan, features, glue |
| 14B | `14b-tdd.md` | Test Plan, code, unit/integration tests |
| 14C | `14c-acceptance-green.md` | Acceptance Test Plan (GREEN evidence) |
| 14D | `14d-conformance.md` | Test Plan (conformance matrix) |
| 15 | `15-requirements-ranking.md` | Requirements Ranking |
| 16 | `16-fully-dressed.md` | Use Case fully dressed |
| 17 | `17-cycle-close.md` | No new artifact |
| 18 | `18-history-flow-audit.md` | Iterations Ledger, History, Flow Audit Ledger and Report |
| 19 | `19-phase-close.md` | Phase close marker |

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
- Do not write artifacts before the gate. Exception: code, tests and glue in 14A-14C.
- The user keeps typing `OK PASO N`; `gate.py` accepts the legacy forms and normalizes them.
- After a gate, allow at most one artifact write batch for that step.
- Persist only approved content. If the draft changes after approval, request the gate again.

# State Tracking Contract (MANDATORY)

- At step start: set `current_step`, mark the step artifacts `in_progress`.
- After a gate: move the step to `approved_steps`, update `last_approved_step`, append an entry to `approvals` with the token and draft hash, and mark the artifacts `approved`.
- After storage: set those artifacts `persisted`.
- `summary` is at most five lines. History and evidence go to `journal/{iteration}/` (append-only). Never write `notes` to `state.yaml`.
- Recovery: read the router, the domain state, `journal/{iteration}/index.json`, and the last two records.

# Gates

- Step 5 has four sub-gates before the step gate: `OK 5.SYSTEM`, `OK 5.VISUAL`, `OK 5.INTERACTION`, `OK 5.VAADIN`, then `OK 5`.
- Step 14B: `OK 14B` approves the test slice; persist `Test Plan`; `OK 14B.IMPL` authorizes code edits and test execution; final `OK 14B` closes the step.
- Step 14D accepts only a fully `MATCH` conformance matrix.
- Step 19 requires an explicit decision to end the phase; a closed cycle is not a closed phase.

# Required Turn Template

For each step, always respond in this order:

0. **Progress overview** rendered from the real `state.yaml`.
1. Proposed draft for the current step only.
2. Open questions or assumptions.
3. Explicit gate request: `Escribe OK PASO N para continuar`.

Do not include content for later steps.

# Anti-Patterns

- Running a single iteration, or avoiding the risky core and executable architecture.
- Attempting a full design before programming, or finalizing the architecture speculatively.
- Skipping gates, writing several steps in one response, or persisting before approval.
- Persisting under `openspec/iterations/`, merging deltas, or treating cycle close as phase close.
- Writing acceptance scenarios after the implementation is green.
- Writing history to `state.yaml` instead of `journal/{iteration}/`.
- Loading step contracts other than the current one.

# Results

Return the artifacts produced, the decisions taken and why, and the open questions to address in the next iteration.
