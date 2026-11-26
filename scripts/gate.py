#!/usr/bin/env python3
"""Normalize and validate UP gate tokens, with order, hash and approvals.

Canonical form: OK <STEP>[.<SUBGATE>]
Legacy forms are accepted; the user never changes what they type.

Additions over the token parser:
  --check-order   the token must match current_step and satisfy the step preconditions
  --draft         hash the draft and bind the approval to that content
  --record        append or update the approval in state.yaml
  --persist       verify (or record) the persisted hash against the approval

Batch phases (inception) do not bind a hash per step: the batch is persisted at
step 10 and the per-step approvals carry draft_hash: null.

Stdlib only. Exit codes: 0 = valid, 1 = invalid.
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
from migrate_state import parse_artifacts, parse_scalar, read_state, read_state_fields  # noqa: E402
from _metrics import record_event  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
GATES_PATH = REPO_ROOT / ".agents" / "flows" / "gates.json"
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"
UI_SUBGATES = {"DESIGN SYSTEM": "SYSTEM"}


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve_state(domain: str | None, state: Path | None) -> Path | None:
    if state:
        return state
    if domain:
        candidate = ARTIFACTS_DIR / domain / "state.yaml"
        return candidate if candidate.is_file() else None
    candidates = sorted(ARTIFACTS_DIR.glob("*/state.yaml"))
    return candidates[0] if len(candidates) == 1 else None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def build(step: str, subgate: str | None, gates: dict, phase: str | None, via: str) -> dict:
    errors: list[str] = []
    cfg = gates.get("phases", {}).get(phase) if phase else None
    if cfg is None:
        errors.append(f"unknown phase '{phase}'; expected one of {sorted(gates.get('phases', {}))}")
    else:
        if step not in cfg.get("steps", []):
            same_prefix = [s for s in cfg["steps"] if s.rstrip("ABCD") == step.rstrip("ABCD")]
            hint = f"; did you mean {same_prefix}?" if same_prefix else ""
            errors.append(f"step '{step}' is not valid in phase '{phase}'{hint}")
        if subgate and subgate not in cfg.get("subgates", {}).get(step, []):
            allowed = cfg.get("subgates", {}).get(step, [])
            hint = f"; allowed subgates: {allowed}" if allowed else "; this step takes no subgate"
            errors.append(f"subgate '{subgate}' is not valid for step {step} in phase '{phase}'{hint}")
    canonical = f"OK {step}" + (f".{subgate}" if subgate else "")
    return {"ok": not errors, "phase": phase, "step": step, "subgate": subgate,
            "canonical": canonical, "via": via, "errors": errors}


def parse_canonical(value: str, gates: dict, phase: str | None, via: str) -> dict:
    text = collapse(value).upper()
    match = re.fullmatch(r"OK\s+(\d{1,2}[A-D]?)(?:\s*[.\s]\s*([A-Z][A-Z0-9_]*))?", text)
    if not match:
        return {"ok": False, "phase": phase, "step": None, "subgate": None,
                "canonical": None, "via": via, "errors": [f"alias target '{value}' is not canonical"]}
    return build(match.group(1).rstrip("."), match.group(2), gates, phase, via)


def normalize(token: str, gates: dict, phase: str | None) -> dict:
    text = collapse(token).upper()
    aliases = {collapse(key).upper(): value for key, value in gates.get("aliases", {}).items()}
    if text in aliases:
        return parse_canonical(aliases[text], gates, phase, via="alias")
    match = re.fullmatch(r"OK\s+(?:PASO\s+)?(\d{1,2}[A-D]?)(?:\s*[.\s]\s*([A-Z][A-Z0-9_]*))?", text)
    if match:
        step = match.group(1).rstrip(".")
        via = "canonical" if "PASO" not in text else "legacy-paso"
        return build(step, match.group(2), gates, phase, via)
    ui = re.fullmatch(r"OK\s+(DESIGN\s+SYSTEM|VISUAL|INTERACTION|VAADIN)", text)
    if ui:
        label = collapse(ui.group(1))
        return build("5", UI_SUBGATES.get(label, label), gates, phase, via="legacy-ui")
    return {"ok": False, "phase": phase, "step": None, "subgate": None,
            "canonical": None, "via": "unmatched", "errors": [f"unrecognized token '{collapse(token)}'"]}


def parse_list(raw: str) -> list[str]:
    text = raw.strip().strip("[]")
    return [item.strip().strip('"').strip("'") for item in text.split(",") if item.strip()]


def check_pre(item: str, fields: dict, artifacts: list[dict]) -> tuple[str | None, str | None]:
    if item.startswith("state.phase=="):
        expected = item.split("==", 1)[1]
        actual = fields.get("phase", "").strip('"')
        if actual != expected:
            return f"precondition failed: phase is '{actual}', expected '{expected}'", None
        return None, None
    if item.startswith("approved."):
        step = item.split(".", 1)[1]
        if step not in parse_list(fields.get("approved_steps", "[]")):
            return f"precondition failed: step {step} is not approved", None
        return None, None
    if item == "all_persisted":
        approved = [a["id"] for a in artifacts if parse_scalar(a["keys"].get("status", "")).strip('"') == "approved"]
        if approved:
            return f"precondition failed: artifacts still approved: {approved}", None
        return None, None
    if item == "design_consistency":
        return None, "design_consistency is evidence-based; validate_step.py enforces it"
    return None, f"unknown precondition '{item}' ignored"


def approvals_block_bounds(lines: list[str]) -> tuple[int | None, int]:
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^approvals:\s*(\[\])?\s*$", line):
            start = index
            break
    if start is None:
        return None, 0
    end = start + 1
    while end < len(lines) and (lines[end].startswith(" ") or lines[end].strip() == ""):
        if lines[end].strip() == "" and end + 1 < len(lines) and not lines[end + 1].startswith(" "):
            break
        end += 1
    return start, end


def append_or_update_approval(state_path: Path, entry: dict, persist: bool) -> dict:
    state = read_state(state_path)
    lines = list(state["lines"])
    block_start, block_end = approvals_block_bounds(lines)

    if block_start is not None and not lines[block_start].strip().endswith("[]"):
        for index in range(block_start + 1, block_end):
            if re.match(rf"\s*-\s*phase:\s*{re.escape(entry['phase'])}\s*$", lines[index]) and index + 1 < block_end:
                for offset in range(index, min(index + 6, block_end)):
                    if re.match(rf'\s+step:\s*"?{re.escape(str(entry["step"]))}"?\s*$', lines[offset]):
                        for target in range(index, min(index + 8, block_end)):
                            if persist and entry.get("persisted_hash") and re.match(r"\s+persisted_hash:\s*", lines[target]):
                                lines[target] = f"    persisted_hash: {entry['persisted_hash']}"
                            elif not persist and entry.get("draft_hash") and re.match(r"\s+draft_hash:\s*", lines[target]):
                                lines[target] = f"    draft_hash: {entry['draft_hash']}"
                        state_path.write_text(
                            state["newline"].join(lines) + state["newline"], encoding="utf-8", newline=""
                        )
                        return {"action": "updated", "entry": entry}
                break

    block = [
        "approvals:" if block_start is None or lines[block_start].strip().endswith("[]") else None,
        f"  - phase: {entry['phase']}",
        f"    step: \"{entry['step']}\"",
        f"    token: \"{entry['token']}\"",
        f"    draft_hash: {entry.get('draft_hash') or 'null'}",
        f"    persisted_hash: {entry.get('persisted_hash') or 'null'}",
        f"    at: {entry['at']}",
    ]
    block = [line for line in block if line is not None]

    if block_start is not None:
        if lines[block_start].strip().endswith("[]"):
            lines[block_start:block_start + 1] = block
        else:
            lines[block_end:block_end] = block[1:]
    else:
        insert_at = None
        for index, line in enumerate(lines):
            if re.match(r"^pending_steps:", line):
                insert_at = index + 1
                break
        if insert_at is None:
            raise SystemExit("cannot locate pending_steps to insert approvals")
        lines[insert_at:insert_at] = [""] + block

    state_path.write_text(state["newline"].join(lines) + state["newline"], encoding="utf-8", newline="")
    return {"action": "created", "entry": entry}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize and validate UP gate tokens.")
    parser.add_argument("--token")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--domain")
    parser.add_argument("--phase", choices=["elaboration", "inception"])
    parser.add_argument("--draft", type=Path)
    parser.add_argument("--expect-hash")
    parser.add_argument("--check-order", action="store_true", default=True)
    parser.add_argument("--allow-any", action="store_true", help="skip order and gate-declaration checks")
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--persist", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)

    gates = load_json(GATES_PATH)
    state_path = resolve_state(args.domain, args.state)
    if state_path is None or not state_path.is_file():
        print(json.dumps({"ok": False, "errors": ["cannot resolve state.yaml; pass --domain or --state"]}, indent=2))
        return 1

    state = read_state(state_path)
    fields = read_state_fields(state["lines"])
    phase = args.phase or fields.get("phase", "").strip('"')
    artifacts = parse_artifacts(state["lines"])

    if args.list:
        cfg = gates.get("phases", {}).get(phase, {})
        tokens = []
        for step in cfg.get("steps", []):
            tokens.append(f"OK {step}")
            tokens.extend(f"OK {step}.{sub}" for sub in cfg.get("subgates", {}).get(step, []))
        print(json.dumps({"phase": phase, "tokens": tokens}, indent=2))
        return 0

    if not args.token:
        parser.error("--token is required unless --list is used")

    result = normalize(args.token, gates, phase)
    result.update({"input": collapse(args.token), "phase_source": "arguments" if args.phase else "state",
                   "state": str(state_path)})
    warnings: list[str] = []

    manifest_path = REPO_ROOT / ".agents" / "flows" / f"{phase}.checks.json"
    manifest = load_json(manifest_path) if manifest_path.is_file() else {"steps": {}, "persist": {}}
    step_spec = manifest.get("steps", {}).get(str(result["step"]))

    if not args.allow_any:
        if step_spec is None:
            result["ok"] = False
            result["errors"].append(f"step {result['step']} is not in the {phase} manifest")
        else:
            declared = step_spec.get("gates", [])
            if not declared:
                result["ok"] = False
                result["errors"].append(f"step {result['step']} is automatic and takes no token")
            elif result["canonical"] not in declared:
                result["ok"] = False
                result["errors"].append(
                    f"token '{result['canonical']}' is not a declared gate for step {result['step']}: {declared}"
                )
            current = fields.get("current_step", "").strip('"')
            if args.check_order and str(result["step"]) != current:
                result["ok"] = False
                result["errors"].append(f"out of order: current_step is {current}, token is for {result['step']}")
            for item in step_spec.get("pre", []):
                error, warning = check_pre(item, fields, artifacts)
                if error:
                    result["ok"] = False
                    result["errors"].append(error)
                if warning:
                    warnings.append(warning)

    draft_hash = None
    if args.draft:
        if not args.draft.is_file():
            result["ok"] = False
            result["errors"].append(f"draft not found: {args.draft}")
        else:
            draft_hash = sha256_file(args.draft)
            result["draft"] = {"path": str(args.draft), "sha256": draft_hash}

    batch_mode = manifest.get("persist", {}).get("mode") == "batch"
    step_number = int(re.sub(r"\D", "", str(result["step"])) or 0)
    batch_step = int(str(manifest.get("persist", {}).get("at", "10")) or 10)
    if batch_mode and step_spec is not None and step_number < batch_step:
        if draft_hash:
            warnings.append("batch phase: per-step approval does not bind a hash")
        draft_hash = None

    if args.expect_hash and args.expect_hash != draft_hash:
        result["ok"] = False
        result["errors"].append(f"hash mismatch: expected {args.expect_hash}, got {draft_hash}")

    if args.persist and not batch_mode:
        if not draft_hash:
            result["ok"] = False
            result["errors"].append("--persist requires --draft to verify the approval binding")
        else:
            approved_hash = None
            block_start, block_end = approvals_block_bounds(state["lines"])
            if block_start is not None:
                for index in range(block_start + 1, block_end):
                    if re.match(rf'\s+step:\s*"?{re.escape(str(result["step"]))}"?\s*$', state["lines"][index]):
                        for offset in range(index, min(index + 6, block_end)):
                            match = re.match(r"\s+draft_hash:\s*(\S+)", state["lines"][offset])
                            if match:
                                approved_hash = match.group(1).strip('"')
                                break
                        break
            if approved_hash is None:
                result["ok"] = False
                result["errors"].append("no recorded approval for this step; record it before persisting")
            elif approved_hash != draft_hash:
                result["ok"] = False
                result["errors"].append(f"persisted content differs from the approved draft ({approved_hash})")

    if args.record:
        if not result["ok"]:
            result["errors"].append("refusing to record an invalid gate")
        else:
            entry = {
                "phase": phase,
                "step": str(result["step"]),
                "token": collapse(args.token),
                "draft_hash": draft_hash,
                "persisted_hash": draft_hash if (args.persist and not batch_mode) else None,
                "at": datetime.now().isoformat(timespec="seconds"),
            }
            result["recorded"] = append_or_update_approval(state_path, entry, persist=args.persist)

    record_event(
        state_path,
        {
            "tool": "gate",
            "phase": phase,
            "step": str(result["step"]),
            "iteration": fields.get("iteration", "").strip('"'),
            "domain": fields.get("domain", "").strip('"'),
            "ok": result["ok"],
            "errors": len(result["errors"]),
            "warnings": len(warnings),
            "canonical": result.get("canonical"),
        },
    )

    result["warnings"] = warnings
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
