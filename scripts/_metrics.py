#!/usr/bin/env python3
"""Append-only agent telemetry for gate and validation runs.

Events are written only when the state file belongs to a real domain under
openspec/artifacts/, so tests with temporary states do not pollute the log.
The log lives under .atl/ (gitignored); Agent Metrics.json is the versioned
aggregate.

Stdlib only.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"
METRICS_DIR = REPO_ROOT / ".atl" / "metrics"
EVENTS_PATH = METRICS_DIR / "agent-events.jsonl"


def is_real_domain(state_path: Path) -> bool:
    try:
        resolved = state_path.resolve()
        return ARTIFACTS_DIR.resolve() in resolved.parents
    except OSError:
        return False


def record_event(state_path: Path, event: dict) -> None:
    if not is_real_domain(state_path):
        return
    payload = {"ts": datetime.now().isoformat(timespec="seconds"), **event}
    try:
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        with EVENTS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    except OSError:
        return
