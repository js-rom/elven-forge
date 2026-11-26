#!/usr/bin/env python3
"""Build a regenerable inventory of the domain artifacts.

Reads state.yaml (position and artifact lifecycle) and the filesystem, and
writes artifact-index.json with one entry per artifact: path, status, resolved
files, size and sha256, plus a pointer to its journal history.

The index is derived data: it can always be rebuilt from state.yaml + files,
and it is byte-stable across runs while those inputs do not change.

Stdlib only. Exit codes: 0 = ok, 1 = --check found differences or bad input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_state import parse_artifacts, parse_scalar, read_state, read_state_fields  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}|\{[A-Za-z]+\}")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def parse_value(raw: str) -> str:
    if raw in ("", "null", "~"):
        return ""
    return parse_scalar(raw)


def parse_list(raw: str) -> list[str]:
    text = raw.strip()
    if not text or text in ("[]", "null"):
        return []
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [parse_value(item.strip()) for item in text.split(",") if item.strip()]


def to_number(value: str):
    text = parse_value(value)
    if text in ("", "null"):
        return None
    try:
        return int(text)
    except ValueError:
        return text


def resolve_path(domain_dir: Path, raw_path: str) -> dict:
    path = parse_value(raw_path)
    if not path:
        return {"kind": "missing", "exists": False, "pattern": None, "matches": []}

    has_placeholder = bool(PLACEHOLDER_RE.search(path))
    if path.endswith("/"):
        directory_pattern = PLACEHOLDER_RE.sub("*", path).rstrip("/")
        directories = sorted(item for item in domain_dir.glob(directory_pattern) if item.is_dir())
        matches_all = sorted(
            file.relative_to(domain_dir).as_posix()
            for directory in directories
            for file in directory.rglob("*")
            if file.is_file()
        )
        return {
            "kind": "pattern",
            "exists": bool(matches_all),
            "pattern": directory_pattern + "/**",
            "matches": matches_all[:25],
            "match_count": len(matches_all),
        }

    if has_placeholder:
        pattern = PLACEHOLDER_RE.sub("*", path)
        matches_all = sorted(
            item.relative_to(domain_dir).as_posix()
            for item in domain_dir.glob(pattern)
            if item.is_file()
        )
        return {
            "kind": "pattern",
            "exists": bool(matches_all),
            "pattern": pattern,
            "matches": matches_all[:25],
            "match_count": len(matches_all),
        }

    target = domain_dir / path
    if not target.is_file():
        return {"kind": "file", "exists": False, "pattern": None, "matches": []}

    data = target.read_bytes()
    return {
        "kind": "file",
        "exists": True,
        "pattern": None,
        "matches": [path],
        "size": len(data),
        "sha256": sha256_bytes(data),
    }


def history_info(domain_dir: Path, raw_ref: str) -> dict:
    reference = parse_value(raw_ref)
    if not reference:
        return {}
    target = domain_dir / reference
    if not target.is_file():
        return {"ref": reference, "exists": False}
    payload = json.loads(target.read_text(encoding="utf-8"))
    return {
        "ref": reference,
        "exists": True,
        "chars": payload.get("chars"),
        "type": payload.get("type"),
    }


def build(state_path: Path) -> dict:
    domain_dir = state_path.parent
    state = read_state(state_path)
    fields = read_state_fields(state["lines"])
    artifacts = parse_artifacts(state["lines"])

    entries: list[dict] = []
    for artifact in artifacts:
        keys = artifact["keys"]
        entries.append(
            {
                "discipline": artifact["discipline"],
                "id": artifact["id"],
                "path": parse_value(keys.get("path", "")),
                "status": parse_value(keys.get("status", "")),
                "created_at_step": to_number(keys.get("created_at_step", "")),
                "refined_at_steps": parse_list(keys.get("refined_at_steps", "")),
                "depends_on": parse_list(keys.get("depends_on", "")),
                "resolution": resolve_path(domain_dir, keys.get("path", "")),
                "history": history_info(domain_dir, keys.get("notes_ref", "")),
            }
        )

    by_status: dict[str, int] = {}
    for entry in entries:
        by_status[entry["status"] or "unknown"] = by_status.get(entry["status"] or "unknown", 0) + 1

    return {
        "schema": 1,
        "domain": parse_value(fields.get("domain", domain_dir.name)),
        "phase": parse_value(fields.get("phase", "")),
        "iteration": parse_value(fields.get("iteration", "")),
        "state": {
            "path": state_path.name,
            "bytes": state["bytes"],
            "sha256": sha256_bytes(state_path.read_bytes()),
        },
        "summary": {
            "total": len(entries),
            "by_status": dict(sorted(by_status.items())),
            "resolved_files": sum(1 for e in entries if e["resolution"]["kind"] == "file" and e["resolution"]["exists"]),
            "patterns": sum(1 for e in entries if e["resolution"]["kind"] == "pattern"),
            "missing": sum(1 for e in entries if not e["resolution"]["exists"]),
            "with_history": sum(1 for e in entries if e["history"].get("exists")),
        },
        "artifacts": entries,
    }


def dump(payload: dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build artifact-index.json from state.yaml.")
    parser.add_argument("--domain", help="domain under openspec/artifacts/")
    parser.add_argument("--state", type=Path, help="explicit state.yaml path")
    parser.add_argument("--out", type=Path, help="output path (default: <domain>/artifact-index.json)")
    parser.add_argument("--check", action="store_true", help="compare instead of writing")
    args = parser.parse_args(argv)

    if args.state:
        state_path = args.state
    elif args.domain:
        state_path = ARTIFACTS_DIR / args.domain / "state.yaml"
    else:
        candidates = sorted(ARTIFACTS_DIR.glob("*/state.yaml"))
        if len(candidates) != 1:
            print(json.dumps({"ok": False, "errors": ["pass --domain or --state"]}, indent=2))
            return 1
        state_path = candidates[0]

    if not state_path.is_file():
        print(json.dumps({"ok": False, "errors": [f"missing {state_path}"]}, indent=2))
        return 1

    payload = build(state_path)
    text = dump(payload)
    out_path = args.out or (state_path.parent / "artifact-index.json")

    if args.check:
        if not out_path.is_file():
            print(json.dumps({"ok": False, "errors": [f"missing {out_path}"]}, indent=2))
            return 1
        current = out_path.read_text(encoding="utf-8")
        same = current == text
        print(
            json.dumps(
                {"ok": same, "check": True, "path": str(out_path), "artifacts": payload["summary"]["total"]},
                indent=2,
            )
        )
        return 0 if same else 1

    out_path.write_text(text, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "ok": True,
                "path": str(out_path),
                "artifacts": payload["summary"]["total"],
                "by_status": payload["summary"]["by_status"],
                "resolved_files": payload["summary"]["resolved_files"],
                "patterns": payload["summary"]["patterns"],
                "missing": payload["summary"]["missing"],
                "with_history": payload["summary"]["with_history"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
