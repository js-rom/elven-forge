#!/usr/bin/env python3
"""Aggregate agent telemetry into per-step flow metrics.

Reads .atl/metrics/agent-events.jsonl (written by gate.py and validate_step.py),
the domain journal, and state.yaml, and writes:

  08 Project Management/Agent Metrics.json

Metrics per step:
  gate_rejections    gate runs with ok=false
  validator_errors   errors reported by validate_step.py
  routes_back        journal records that mention a route back or a reopen
  state_read_bytes   size of state.yaml at measurement time (iteration level)

Stdlib only. Exit codes: 0 = ok, 1 = --check mismatch or bad input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_state import read_state_fields  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"
EVENTS_PATH = REPO_ROOT / ".atl" / "metrics" / "agent-events.jsonl"
ROUTE_RE = re.compile(r"\b(routed?|route back|back to (paso|step)|reopen(ed)?)\b", re.IGNORECASE)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve_state(domain: str | None, state: Path | None) -> Path:
    if state:
        return state
    if domain:
        return ARTIFACTS_DIR / domain / "state.yaml"
    candidates = sorted(ARTIFACTS_DIR.glob("*/state.yaml"))
    if len(candidates) != 1:
        raise SystemExit("pass --domain or --state")
    return candidates[0]


def step_key(step: str):
    match = re.match(r"(\d+)([A-D]?)", str(step))
    if match:
        return (int(match.group(1)), match.group(2))
    return (999, str(step))


def read_events(iteration: str, events_path: Path) -> list[dict]:
    if not events_path.is_file():
        return []
    events = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(event.get("iteration", "")) == iteration:
            events.append(event)
    return events


def read_journal_routes(domain_dir: Path, journal: str) -> list[str]:
    root = domain_dir / journal
    index = root / "index.json"
    if not index.is_file():
        return []
    entries = load_json(index).get("entries", [])
    routes = []
    for entry in entries:
        path = root / entry["file"]
        if not path.is_file():
            continue
        payload = load_json(path)
        if payload.get("type") != "step-note":
            continue
        raw = payload.get("raw", "")
        step = payload.get("step")
        if step and ROUTE_RE.search(raw):
            routes.append(str(step))
    return routes


def build(state_path: Path, iteration: str | None, events_path: Path = EVENTS_PATH) -> dict:
    state = read_state_fields(state_path.read_text(encoding="utf-8").splitlines())
    domain = state.get("domain", state_path.parent.name).strip('"')
    iteration = iteration or state.get("iteration", "").strip('"')
    journal = state.get("journal", "").strip('"') or f"journal/{iteration}"

    events = read_events(iteration, events_path)
    steps: dict[str, dict] = {}

    def entry(step: str) -> dict:
        if step not in steps:
            steps[step] = {"step": str(step), "gate_rejections": 0, "validator_errors": 0, "routes_back": 0}
        return steps[step]

    for event in events:
        step = str(event.get("step", ""))
        if not step:
            continue
        target = entry(step)
        if event.get("tool") == "gate" and event.get("ok") is False:
            target["gate_rejections"] += 1
        if event.get("tool") == "validate":
            target["validator_errors"] += int(event.get("errors", 0) or 0)

    for step in read_journal_routes(state_path.parent, journal):
        entry(step)["routes_back"] += 1

    summary = {
        "gate_rejections": sum(item["gate_rejections"] for item in steps.values()),
        "validator_errors": sum(item["validator_errors"] for item in steps.values()),
        "routes_back": sum(item["routes_back"] for item in steps.values()),
        "state_read_bytes": state_path.stat().st_size,
    }

    timestamps = sorted(event["ts"] for event in events if event.get("ts"))
    return {
        "schema": 1,
        "domain": domain,
        "iteration": iteration,
        "summary": summary,
        "steps": sorted(steps.values(), key=lambda item: step_key(item["step"])),
        "events": {
            "total": len(events),
            "first": timestamps[0] if timestamps else None,
            "last": timestamps[-1] if timestamps else None,
        },
        "method": {
            "gate_rejections": "gate.py runs with ok=false",
            "validator_errors": "sum of errors reported by validate_step.py",
            "routes_back": "journal records matching route back / reopen wording",
            "state_read_bytes": "state.yaml size at measurement time",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Agent Metrics.json for the flow audit.")
    parser.add_argument("--domain")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--iteration")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--events", type=Path, default=EVENTS_PATH)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    state_path = resolve_state(args.domain, args.state)
    if not state_path.is_file():
        print(json.dumps({"ok": False, "errors": [f"missing {state_path}"]}, indent=2))
        return 1

    payload = build(state_path, args.iteration, args.events)
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    out_path = args.out or (state_path.parent / "08 Project Management" / "Agent Metrics.json")

    if args.check:
        if not out_path.is_file():
            print(json.dumps({"ok": False, "errors": [f"missing {out_path}"]}, indent=2))
            return 1
        same = out_path.read_text(encoding="utf-8") == text
        print(json.dumps({"ok": same, "check": True, "path": str(out_path), "iteration": payload["iteration"]}, indent=2))
        return 0 if same else 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"ok": True, "path": str(out_path), **payload["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
