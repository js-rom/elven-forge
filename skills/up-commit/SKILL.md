---
name: up-commit
description: >
  Creates commits with a Unified Process-aware convention. Reads the active UP
  phase (Inception, Elaboration, Construction, Transition), iteration id, current
  flow step, step description, and staged changes; then writes an English commit
  subject and body with phase, iteration, step, and change summary. Handles the
  .agents submodule first. Triggers: commit, comitear, haz commit.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

# Purpose

Create one commit from already staged changes using the project convention.
Keep token use low: run one script, read its compact output, write the summary,
and execute the returned command.

# Minimal Flow

1. Run:

```powershell
powershell -NoProfile -File ".agents\skills\up-commit\scripts\prepare-commit.ps1"
```

2. If `STAGED_COUNT=0` and `AGENTS_STAGED_COUNT=0`, stop and ask which files to stage. Do not stage automatically.
3. If `SAFETY=WARN`, show the warning and ask before committing.
4. Read only the script output. Do not inspect full diffs, artifacts, or other skills.
5. If `AGENTS_STAGED_COUNT>0`, commit `.agents` first with `AGENTS_COMMAND_TEMPLATE`, then run `AFTER_AGENTS`.
6. If `STAGED_COUNT>0`, run `COMMAND_TEMPLATE` after filling `<summary>` and the changes.
7. Run `git status --short` and `git log -1 --oneline`; report hashes. Do not push or amend.

# Commit Convention

Subject:

```text
[Elaboration][E19][Step 16] Short imperative summary
```

Body:

```text
UP phase: Elaboration
Iteration: E19
Flow step: Step 16 - Use case fully dressed
Changes:
- Change one.
- Change two.
```

Rules:

- Use the `SUBJECT_PREFIX` and `BODY_TEMPLATE` from the script verbatim.
- Write the summary and changes in English.
- Keep the subject at 72 characters or fewer, imperative, no trailing period.
- Describe the actual staged changes, not the branch or the whole iteration.
- If `.agents` is committed first, its subject/body describe the skill/tooling changes; the main commit describes project changes.
- Never `git add -A`, force-push, amend, or skip hooks.
- Do not commit unstaged or unrelated files.
- Do not commit secrets, credentials, conflict markers, or generated noise.

# Script Output

The script returns compact `key=value` lines:

- `PHASE`, `ITERATION`, `STEP`, `STEP_DESC`
- `SUBJECT_PREFIX`, `BODY_TEMPLATE`
- `STAGED_COUNT`, `AGENTS_STAGED_COUNT`, `AGENTS_DIRTY`
- `SAFETY`
- `STAGED` and `AGENTS_STAGED` file lists
- `COMMAND_TEMPLATE` and `AGENTS_COMMAND_TEMPLATE`
- `AFTER_AGENTS=git add .agents` when a submodule commit is required

Use this output directly. Do not perform extra discovery.
