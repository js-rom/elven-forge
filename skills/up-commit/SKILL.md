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
show it to the user, wait for confirmation, and execute the returned command.

# Hard Rules

- If `STAGED_COUNT > 0`, commit ONLY the files listed in `STAGED`. Never run `git add`.
- Extra unstaged or untracked files are out of scope. Report them as `EXTRA_CHANGES` and leave them uncommitted.
- If the user wants extra files included, stop and ask them to stage those files explicitly; use a separate commit.
- Never commit in the same turn in which the proposal is shown.
- Never `git add -A`, amend, force-push, or skip hooks.

# Minimal Flow

1. Run:

```powershell
powershell -NoProfile -File ".agents\skills\up-commit\scripts\prepare-commit.ps1"
```

2. If `STAGED_COUNT=0` and `AGENTS_STAGED_COUNT=0`, stop and ask which files to stage. Do not stage automatically.
2a. If `STAGED_COUNT>0`, do not stage anything. Use only the files listed in `STAGED`; `EXTRA_CHANGES=YES` means other files exist but must remain out of this commit.
3. If `SAFETY=WARN`, show the warning and ask before committing.
4. Read only the script output. Do not inspect full diffs, artifacts, or other skills.
5. Fill `SUBJECT` and `BODY` from `SUBJECT_PREFIX`, `BODY_TEMPLATE`, and the actual staged changes. Include `COMMIT_SCOPE=STAGED_ONLY` and `EXTRA_CHANGES` in the proposal.
6. Show the proposal and wait for explicit user confirmation:

```text
SUBJECT: [Phase][Iteration][Step N] Short imperative summary
BODY:
UP phase: ...
Iteration: ...
Flow step: ...
Changes:
- ...
STAGED: <file list>
COMMIT_SCOPE: STAGED_ONLY
EXTRA_CHANGES: YES|NO
```

7. Do not run the commit in the same turn in which the proposal is shown. Do not stage files on your own initiative; only commit what the user staged or approved. If the user asks to include extra files, stop and ask them to stage those files explicitly for a separate commit.
8. If `AGENTS_STAGED_COUNT>0`, commit `.agents` first with `AGENTS_COMMAND_TEMPLATE`, then run `AFTER_AGENTS`.
9. If `STAGED_COUNT>0`, run `COMMAND_TEMPLATE` after confirmation, with the same subject and body shown in step 6.
10. Run `git status --short` and `git log -1 --oneline`; report hashes. Do not push or amend.

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
- Always show `SUBJECT` and `BODY` and wait for explicit confirmation before committing, even when `SAFETY=OK`.
- Never stage files on your own initiative; only commit staged changes or files the user approved.
- When `STAGED_COUNT>0`, treat `STAGED` as a closed allowlist. Do not include `UNSTAGED` or `UNTRACKED` files.
- If `.agents` is committed first, its subject/body describe the skill/tooling changes; the main commit describes project changes.
- Never `git add -A`, force-push, amend, or skip hooks.
- Do not commit unstaged or unrelated files.
- Do not commit secrets, credentials, conflict markers, or generated noise.

# Script Output

The script returns compact `key=value` lines:

- `PHASE`, `ITERATION`, `STEP`, `STEP_DESC`
- `SUBJECT_PREFIX`, `BODY_TEMPLATE`
- `STAGED_COUNT`, `AGENTS_STAGED_COUNT`, `AGENTS_DIRTY`
- `UNSTAGED_COUNT`, `UNTRACKED_COUNT`, `EXTRA_CHANGES`
- `COMMIT_SCOPE`, `STAGE_POLICY`
- `SAFETY`
- `STAGED` and `AGENTS_STAGED` file lists
- `UNSTAGED` and `UNTRACKED` file lists
- `COMMAND_TEMPLATE` and `AGENTS_COMMAND_TEMPLATE`
- `AFTER_AGENTS=git add .agents` when a submodule commit is required

Use this output directly. Do not perform extra discovery.
