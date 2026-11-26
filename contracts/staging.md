# Staging contract

Drafts and multi-batch plans are written under `.atl/staging/`, never directly to `openspec/`.

## Layout

```text
.atl/staging/{domain}/{iteration}/{step}/{artifact-or-batch}.md
```

Example: `.atl/staging/registro-horario/E21/14B/Test Plan.batch-03.md`.

## Lifecycle

1. The worker drafts in staging.
2. The orchestrator presents the draft or a diff in chat.
3. The gate is requested.
4. After approval, storage writes the artifact; the staging copy is deleted.
5. If rejected, the worker edits the staging copy; no artifact was touched.

## Ownership

| Role | Responsibility |
|---|---|
| Worker | Writes staging |
| Orchestrator | Presents and requests the gate |
| Storage | Only writer of `openspec/` |
| Reviewer | Reads staging or the persisted artifact |

## Rules

- `.atl` is gitignored; staging is never committed.
- One folder per step and batch; include the batch number in the file name.
- Code and tests in 14B are written in place only after `OK 14B.IMPL`; staging does not apply to them.
- A staging file is not an artifact: it has no schema path and no state lifecycle.
