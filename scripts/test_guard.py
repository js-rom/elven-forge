#!/usr/bin/env python3
"""Freeze and verify acceptance features and the test tree.

- 14A: --features --record   after OK 14A (test author wrote the features)
- 14B: --tests --record      after the test author's RED
- 14B.IMPL / 14C / 14D: --features --verify and --tests --verify
- Mutation re-open: --tests --record --reopen --reason "..." (test author only)

Baselines live under journal/{iteration}/feature-baseline.json and
test-baseline.json. Re-recording an existing baseline fails unless --reopen is
given with a reason; the reason is appended to the baseline history. The
implementer cannot edit tests by permission; this script makes any change
detectable even if it happens through another tool.

Stdlib only. Exit codes: 0 = ok, 1 = changed/missing baseline, 2 = usage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_state import read_state, read_state_fields  # noqa: E402
from _metrics import record_event  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"
SKIP_PARTS = {"target", ".git", "node_modules", "__pycache__", ".idea"}


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


def detect_source_root() -> Path:
    candidates = [REPO_ROOT]
    candidates.extend(sorted(item for item in REPO_ROOT.iterdir() if item.is_dir()))
    for candidate in candidates:
        if (candidate / "pom.xml").is_file() or (candidate / "build.gradle").is_file():
            return candidate
    raise SystemExit("source root not found; pass --source-root")


def read_field(lines: list[str], name: str) -> str:
    for line in lines:
        match = re.match(rf"^{re.escape(name)}:\s*(.*)$", line)
        if match:
            return match.group(1).split("#", 1)[0].strip().strip('"')
    return ""


def hash_tree(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        files[relative] = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def baseline_path(journal_dir: Path, kind: str) -> Path:
    name = "feature-baseline.json" if kind == "features" else "test-baseline.json"
    return journal_dir / name


def record_baseline(
    path: Path,
    kind: str,
    source_root: Path,
    files: dict[str, str],
    iteration: str,
    reopen_reason: str | None = None,
    step: str | None = None,
) -> dict:
    history: list[dict] = []
    if path.is_file():
        try:
            history = list(load_json(path).get("reopen", []))
        except (OSError, ValueError):
            history = []
    if reopen_reason:
        history.append(
            {
                "at": datetime.now().isoformat(timespec="seconds"),
                "step": step,
                "reason": reopen_reason,
            }
        )
    payload = {
        "iteration": iteration,
        "kind": kind,
        "source_root": str(source_root),
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "files": files,
    }
    if history:
        payload["reopen"] = history
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return payload


def verify_baseline(path: Path, files: dict[str, str]) -> dict:
    if not path.is_file():
        return {"ok": False, "errors": [f"baseline not found: {path}"], "added": [], "removed": [], "changed": []}
    baseline = load_json(path).get("files", {})
    current = files
    added = sorted(set(current) - set(baseline))
    removed = sorted(set(baseline) - set(current))
    changed = sorted(key for key in set(current) & set(baseline) if current[key] != baseline[key])
    errors = []
    if added:
        errors.append(f"added files: {added}")
    if removed:
        errors.append(f"removed files: {removed}")
    if changed:
        errors.append(f"changed files: {changed}")
    return {"ok": not errors, "errors": errors, "added": added, "removed": removed, "changed": changed}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze and verify features/tests.")
    parser.add_argument("--domain")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--iteration")
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--journal-dir", type=Path)
    parser.add_argument("--features", action="store_true")
    parser.add_argument("--tests", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--reopen", action="store_true", help="re-record an existing baseline deliberately")
    parser.add_argument("--reason", help="why the baseline is reopened")
    parser.add_argument("--phase", default="elaboration")
    parser.add_argument("--step")
    args = parser.parse_args(argv)

    if args.record == args.verify:
        parser.error("use exactly one of --record or --verify")
    if args.reopen and not args.record:
        parser.error("--reopen requires --record")
    if args.reopen and not (args.reason or "").strip():
        parser.error("--reopen requires a non-empty --reason")

    state_path = resolve_state(args.domain, args.state)
    if not state_path.is_file():
        print(json.dumps({"ok": False, "errors": [f"missing {state_path}"]}, indent=2))
        return 1

    state = read_state(state_path)
    fields = read_state_fields(state["lines"])
    iteration = args.iteration or read_field(state["lines"], "iteration")
    journal = read_field(state["lines"], "journal") or f"journal/{iteration}"
    journal_dir = args.journal_dir or (state_path.parent / journal)
    step = args.step or read_field(state["lines"], "current_step")
    source_root = (args.source_root or detect_source_root()).resolve()

    kinds = []
    if args.all or (not args.features and not args.tests):
        kinds = ["features", "tests"]
    else:
        if args.features:
            kinds.append("features")
        if args.tests:
            kinds.append("tests")

    reports = []
    ok = True
    for kind in kinds:
        if kind == "features":
            root = source_root / "src" / "test" / "resources" / "features"
        else:
            root = source_root / "src" / "test"
        if not root.is_dir():
            reports.append({"kind": kind, "ok": False, "errors": [f"tree not found: {root}"]})
            ok = False
            continue

        files = hash_tree(root)
        path = baseline_path(journal_dir, kind)
        if args.record:
            if path.is_file() and not args.reopen:
                reports.append(
                    {
                        "kind": kind,
                        "ok": False,
                        "baseline": str(path),
                        "errors": [f"baseline already exists: {path}; re-record with --reopen --reason"],
                    }
                )
                ok = False
                continue
            payload = record_baseline(
                path,
                kind,
                source_root,
                files,
                iteration,
                args.reason.strip() if args.reopen else None,
                step,
            )
            reports.append(
                {
                    "kind": kind,
                    "ok": True,
                    "recorded": str(path),
                    "files": len(files),
                    "reopened": bool(args.reopen),
                    "reopen_count": len(payload.get("reopen", [])),
                }
            )
            if args.reopen:
                record_event(
                    state_path,
                    {
                        "tool": "test_guard",
                        "phase": args.phase,
                        "step": step,
                        "iteration": iteration,
                        "kind": kind,
                        "ok": True,
                        "reopen": True,
                    },
                )
        else:
            result = verify_baseline(path, files)
            reports.append({"kind": kind, "baseline": str(path), **result})
            if not result["ok"]:
                ok = False
                record_event(
                    state_path,
                    {
                        "tool": "test_guard",
                        "phase": args.phase,
                        "step": step,
                        "iteration": iteration,
                        "kind": kind,
                        "ok": False,
                        "errors": len(result["errors"]),
                    },
                )

    print(json.dumps({"ok": ok, "iteration": iteration, "source_root": str(source_root), "reports": reports}, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
