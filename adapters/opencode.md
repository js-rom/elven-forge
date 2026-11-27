# OpenCode adapter

Maps the abstract roles of `contracts/roles.yaml` to OpenCode V2 mechanisms.

| Role | Mechanism | Path |
|---|---|---|
| Orchestrator | Current session (primary agent) | `AGENTS.md` -> `.agents/agent.md` |
| Worker | Subagent, writes only to `.atl/staging` | `.opencode/agents/up-worker.md` |
| Test author | Subagent, writes `.atl/staging` and `src/test` | `.opencode/agents/up-test-author.md` |
| Implementer | Subagent, writes only `src/main` | `.opencode/agents/up-implementer.md` |
| Runner | Scripts and commands, no edits | `mvn test`, `test_guard.py` |
| Reviewer | Subagent, read-only | `.opencode/agents/up-reviewer.md` |
| Validator | Scripts | `.agents/scripts/validate_step.py`, `.agents/scripts/gate.py` |

## Commands

| Command | File |
|---|---|
| `/up-inception` | `.opencode/commands/up-inception.md` |
| `/up-elaboration` | `.opencode/commands/up-elaboration.md` |

## Invocation

- The reviewer is launched with the `subagent` tool and the agent id `up-reviewer`.
- The reviewer receives only: the artifact (or its staging path), the rubric path, and the cited source paths.
- The orchestrator never passes its own reasoning to the reviewer.

## Portability

Only this file and `.opencode/agents/*` are OpenCode-specific. The flows, step contracts, rubrics and scripts are runtime-agnostic.
