#!/usr/bin/env python3
"""Negative and positive tests for validate_step.py and gate.py.

Covers the F3.6 acceptance:
  1. missing section      -> validate exits 1
  2. broken link          -> validate exits 1
  3. hash mismatch        -> gate exits 1
  4. out-of-order gate    -> gate exits 1
  5. valid gate           -> gate exits 0
  6. batch approval       -> no per-step hash, recorded with draft_hash null
  7. persist binding      -> gate exits 1 when the artifact differs from the approved draft
  8. approval binding ok  -> gate exits 0 when hashes match

Stdlib only. Exit codes: 0 = all cases pass, 1 = at least one failed.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".agents" / "scripts"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=REPO_ROOT,
    )


def state_elaboration(directory: Path, current: str) -> Path:
    text = f"""phase: elaboration
iteration: E99
domain: test
status: in_progress
date: 2026-11-26
current_step: {current}
last_approved_step: 1
approved_steps: [1, 2, 3, 4, 5, 7, 8, 9A, 9B, 10, 11, 12, 13, 14A, 14B, 14C]
pending_steps: [{current}]
scope: "test"
summary: "test"
journal: journal/E99
approvals: []

artifacts:
  08 Project Management:
    - id: Iteration Plan
      path: plan.md
      status: persisted
      created_at_step: 1
      refined_at_steps: []
      depends_on: []
  05 Test:
    - id: Test Plan
      path: 05 Test/99 E99 Test plan.md
      status: approved
      created_at_step: 14
      refined_at_steps: []
      depends_on: []
"""
    return write(directory / "state-elab.yaml", text)


def state_inception(directory: Path, current: str) -> Path:
    text = f"""phase: inception
iteration: I9
domain: test
status: in_progress
date: 2026-11-26
current_step: {current}
last_approved_step: 4
approved_steps: [1, 2, 3, 4]
pending_steps: [{current}]
scope: "test"
summary: "test"
journal: journal/I9
approvals: []

artifacts:
  02 Requirements:
    - id: Vision and Business Case
      path: 02 Requirements/vision.md
      status: approved
      created_at_step: 1
      refined_at_steps: []
      depends_on: []
"""
    return write(directory / "state-inc.yaml", text)


def main() -> int:
    base = Path(tempfile.mkdtemp(prefix="up-gates-"))
    cases: list[dict] = []

    def record(name: str, expected: int, result: subprocess.CompletedProcess, note: str = "") -> None:
        cases.append(
            {
                "case": name,
                "expected_exit": expected,
                "actual_exit": result.returncode,
                "ok": result.returncode == expected,
                "note": note,
            }
        )

    missing = write(base / "missing.md", "# Domain Model\n\nNo required headings.\n")
    record(
        "missing section",
        1,
        run("validate_step.py", "--phase", "elaboration", "--step", "3",
            "--file", str(missing), "--state", str(state_elaboration(base, "14D"))),
    )

    headings = "\n".join(
        [
            "# UCR", "", "## Revision History", "", "## Goal", "", "## Inputs and References", "",
            "## Scenario Mapping", "", "## Scenario Realizations", "",
            "## Consolidated Design Class View (Use Case Level)", "", "## Validation Checklist", "",
            "![broken](missing.svg)", "",
        ]
    )
    broken = write(base / "broken-link.md", headings)
    record(
        "broken link",
        1,
        run("validate_step.py", "--phase", "elaboration", "--step", "10",
            "--file", str(broken), "--state", str(state_elaboration(base, "14D"))),
    )

    draft = write(base / "draft.md", "approved content\n")
    gate_state = state_elaboration(base, "14D")
    record(
        "hash mismatch",
        1,
        run("gate.py", "--state", str(gate_state), "--token", "OK PASO 14D",
            "--draft", str(draft), "--expect-hash", "sha256:deadbeef"),
    )
    record(
        "out of order",
        1,
        run("gate.py", "--state", str(gate_state), "--token", "OK PASO 14B"),
    )
    record(
        "valid gate",
        0,
        run("gate.py", "--state", str(gate_state), "--token", "OK PASO 14D"),
    )

    batch_state = state_inception(base, "5")
    batch_result = run(
        "gate.py", "--state", str(batch_state), "--token", "OK PASO 5", "--record"
    )
    recorded_null = 'draft_hash: null' in batch_state.read_text(encoding="utf-8")
    record("batch approval", 0, batch_result, "draft_hash null" if recorded_null else "draft_hash bound")
    if not recorded_null:
        cases[-1]["ok"] = False

    approved = write(base / "approved.md", "approved content\n")
    changed = write(base / "changed.md", "different content\n")
    import hashlib

    approved_hash = "sha256:" + hashlib.sha256(approved.read_bytes()).hexdigest()
    persist_state = state_elaboration(base, "14D")
    text = persist_state.read_text(encoding="utf-8").replace(
        "approvals: []",
        "approvals:\n  - phase: elaboration\n    step: \"14D\"\n    token: \"OK PASO 14D\"\n"
        f"    draft_hash: {approved_hash}\n    persisted_hash: null\n    at: 2026-11-26T10:00:00",
    )
    persist_state.write_text(text, encoding="utf-8", newline="\n")
    record(
        "persist mismatch",
        1,
        run("gate.py", "--state", str(persist_state), "--token", "OK PASO 14D",
            "--draft", str(changed), "--persist"),
    )
    record(
        "persist match",
        0,
        run("gate.py", "--state", str(persist_state), "--token", "OK PASO 14D",
            "--draft", str(approved), "--persist"),
    )

    plan_fixture = write(
        base / "plan.md",
        """# Plan

## Selected Scope Summary

| Scope ID | Priority | Planning Unit | Scope Item | Why Selected | Planned Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | High | Refactor | S1 | reason | outcome |

UC01.
""",
    )

    test_plan_fixture = write(
        base / "test-plan-14b.md",
        """# Test Plan

## Agreed Test List (Step 1 Output)

| Test ID | Scope IDs | Scenario Slice | Preconditions | Input / Trigger | Expected Result | Selection Rationale | Priority | Status | Test file | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | S1 | UC01 slice | pre | in | out | why | High | planned | - | cmd |

## Deferred Items

| Test ID | Reason | Approved by |
| :--- | :--- | :--- |
| - | none | - |

## Traceability

UC01.
""",
    )
    record(
        "14B planned status",
        1,
        run("validate_step.py", "--phase", "elaboration", "--step", "14B",
            "--file", str(test_plan_fixture), "--state", str(state_elaboration(base, "14B")),
            "--from-file", str(plan_fixture), "--to-file", str(test_plan_fixture)),
    )

    acceptance_fixture = write(
        base / "acceptance-14c.md",
        """# Acceptance

## Scenario List (Agreed Acceptance List - 14A Output)

| Scenario ID | Scope ID | Gherkin | UC Step / Extension | Domain Invariant | Interaction Spec | Feature file | Planned execution | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | S1 | s | UC01 | I1 | N/A | f | yes | High |
| A-02 | S1 | s | UC01 | I1 | N/A | f | yes | High |

## Scenario Reconciliation (14C)

| Scenario ID | Feature file | Executed | Result | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| A-01 | f | skip | GREEN | cmd |

## Execution Evidence (14C)

| Run | Result |
| :--- | :--- |
| cmd | 1 |
""",
    )
    record(
        "14C skipped scenario",
        1,
        run("validate_step.py", "--phase", "elaboration", "--step", "14C",
            "--file", str(acceptance_fixture), "--state", str(state_elaboration(base, "14C"))),
    )

    verification_text = """# Verification

## Design Conformance (14D)

| Element | Source | Implementation | Verdict | Action |
| :--- | :--- | :--- | :--- | :--- |
| e | s | i | MISSING | fix |

## Iteration Plan Coverage (14D)

| Scope ID | UC/Scenario | Design | Implementation | Test IDs | A-IDs | Evidence | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | UC01 | d | i | T-01 | A-01 | cmd | MISSING |

## Iteration Exit Criteria (14D)

| Criterion | Evidence | Verdict |
| :--- | :--- | :--- |
| c | e | NOT MET |

## Build Evidence

- ok

## Verdict

| Check | Verdict |
| :--- | :--- |
| Design Conformance | MISSING |
| Iteration Plan Coverage | MISSING |
| Iteration Exit Criteria | NOT MET |
| Overall | NOT READY |
"""
    verification_negative = write(base / "verification-14d.md", verification_text)
    record(
        "14D missing coverage",
        1,
        run("validate_step.py", "--phase", "elaboration", "--step", "14D",
            "--file", str(verification_negative), "--state", str(state_elaboration(base, "14D"))),
    )

    verification_positive = write(
        base / "verification-14d-ok.md",
        verification_text.replace("| MISSING |", "| COVERED |")
        .replace("| NOT MET |", "| MET |")
        .replace("| Overall | NOT READY |", "| Overall | READY |"),
    )
    record(
        "14D ready",
        0,
        run("validate_step.py", "--phase", "elaboration", "--step", "14D",
            "--file", str(verification_positive), "--state", str(state_elaboration(base, "14D"))),
    )

    failed = [case for case in cases if not case["ok"]]
    print(json.dumps({"ok": not failed, "cases": cases}, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
