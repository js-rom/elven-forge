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

    failed = [case for case in cases if not case["ok"]]
    print(json.dumps({"ok": not failed, "cases": cases}, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
