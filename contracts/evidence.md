# Evidence contract

What a gate must show before `OK <STEP>` is accepted. Evidence is concrete: a command, a path, or a quoted line from the artifact. "It looks fine" is not evidence.

## Content steps (analysis, design, documentation)

Applies to: elaboration 1-4, 5, 7, 8, 9A, 9B, 10, 11, 12, 13, 15, 16; inception 1-9.

| Evidence | Required | Form |
|---|---|---|
| Draft presented in chat | Yes | The content itself, not a summary of it |
| Artifact contract loaded | Yes | Path to the step contract + schema template used |
| Validator output | When a validator exists for the step | `validate_step.py` output with 0 errors |
| Traceability | When the step consumes upstream artifacts | Explicit reference per row or item |
| Open questions / assumptions | Yes | Short list, or "none" |
| Gate request | Yes | `OK <STEP>` (legacy forms accepted) |

## Implementation steps (ATDD/TDD)

Applies to: elaboration 14A, 14B, 14C, 14D.

| Evidence | Required |
|---|---|
| Scope slice | The iteration items and scenarios in scope, quoted from the Iteration Plan |
| Test items | Identifier per item (`T-01`, `A-01`, ...) with its traceability row |
| RED | Failing command and output, or a documented reason why RED materializes later |
| GREEN | Command and result (`N tests, 0 failures`) |
| Coverage of contracts | Mapping item -> Operation Contract postcondition |
| Test status and evidence (14B) | Every Test Plan item has `Status` (`implemented`/`deferred`) and non-empty `Evidence`; deferred items are listed |
| Test author RED (14B) | Command and output produced by the test author before implementation starts |
| Feature baseline (14A) | `test_guard.py --features --record` at 14A; verify at 14C and 14D |
| Test baseline (14B) | `test_guard.py --tests --record` after the test author's RED; verify at 14B.IMPL, 14C and 14D |
| Scenario reconciliation (14C) | Every `A-xx` appears with feature file, `Executed=yes`, `Result=GREEN` and evidence |
| Iteration Verification (14D) | Design conformance + plan coverage (`COVERED`/`DEFERRED`) + exit criteria (`MET`) + `Overall: READY` |
| Gate request | `OK <STEP>` or `OK <STEP>.<SUBGATE>` |

A gate cannot pass with an unreconciled `Scope ID`, a `planned` test item, a skipped acceptance scenario, or a `NOT MET` exit criterion. The implementer cannot edit `src/test/**`; a test or feature change after approval is a gate failure.

## Review gates

Applies to: elaboration 11, 14D; inception 9 (Vision).

| Evidence | Required |
|---|---|
| Validator output | 0 errors; warnings with written rationale |
| Reviewer verdict | `YES`, `CONDITIONAL` or `NO`, with blocking items |
| Blocking citation | Every blocking item quotes the artifact text or the script line |
| Readiness | Explicit statement (`ready for step N: YES/NO`) |

A `NO` verdict cannot be overridden by the driver. It is either fixed and re-evaluated, or the step is routed back per `on_fail`.

## Automatic steps

Applies to: inception 0, 10, 11, 12; elaboration 17, 18.

| Evidence | Required |
|---|---|
| What was written / executed | File list or command output |
| Journal entry | One `journal/{iteration}/*.json` record with the outcome |
| Failure handling | If it fails: stop, report, do not advance |

## Gate tokens

Canonical: `OK <STEP>[.<SUBGATE>]`, resolved against the active phase from `state.yaml`.

Legacy forms are accepted and normalized by `scripts/gate.py`; the user is never required to change what they type.

## Approval binding

An approval is bound to the draft content hash. If the draft changes after `OK <STEP>` and before persistence, the gate must be requested again.
