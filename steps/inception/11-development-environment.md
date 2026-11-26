# Step 11 — Development Environment (automatic)

## Inputs
- The project context created in steps 1-9: stack, architecture, testing and style.
- Skill `set-development-environment`.
- The domain config `tdd` values, if refined.

## Output contract
- Invoke the development environment skill and pass the project context; do not ask the user to repeat it in chat.
- This step writes outside the UP artifacts: project files, tooling or configuration.
- Requires explicit confirmation before writing, because it breaks the chat-only rule of steps 1-9.
- Write a journal record with what was created and the commands executed.

## Preconditions
- Step 10 persisted the artifact batch successfully.
- The detected stack is confirmed, not guessed.

## Rubric
- The setup matches the detected stack; no invented toolchain.
- The build or test command is recorded in the domain config.
- Nothing is written before the confirmation.

## Evidence required
- Confirmation.
- File and command list.
- Journal record.

## Anti-patterns
- Skipping the step without recording why.
- Writing project files without confirmation.
- Guessing the stack instead of detecting it.
