#!/usr/bin/env python3
"""Normalize and validate Unified Process gate tokens.

Canonical form: OK <STEP>[.<SUBGATE>]
Legacy forms accepted (user never has to change what they type):
  OK PASO 14B                -> OK 14B
  OK PASO 14B IMPLEMENTAR    -> OK 14B.IMPL
  OK DESIGN SYSTEM           -> OK 5.SYSTEM
  OK VISUAL / INTERACTION / VAADIN -> OK 5.<SUB>
  OK CASOS 14B modo Automatic -> OK 14B.CASES

The phase is resolved from the domain state file unless --phase is given,
because the same step number can exist in more than one phase.

Stdlib only. Exit codes: 0 = valid, 1 = invalid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GATES_PATH = REPO_ROOT / ".agents" / "flows" / "gates.json"
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"

UI_SUBGATES = {"DESIGN SYSTEM": "SYSTEM"}


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_phase(state_path: Path) -> str | None:
    match = re.search(r"(?m)^phase:\s*(\S+)", state_path.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else None


def resolve_state(domain: str | None) -> Path | None:
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
    return {
        "ok": not errors,
        "phase": phase,
        "step": step,
        "subgate": subgate,
        "canonical": canonical,
        "via": via,
        "errors": errors,
    }


def normalize(token: str, gates: dict, phase: str | None) -> dict:
    text = collapse(token).upper()
    aliases = {collapse(key).upper(): value for key, value in gates.get("aliases", {}).items()}

    if text in aliases:
        return parse_canonical(aliases[text], gates, phase, via="alias")

    match = re.fullmatch(
        r"OK\s+(?:PASO\s+)?(\d{1,2}[A-D]?)(?:\s*[.\s]\s*([A-Z][A-Z0-9_]*))?", text
    )
    if match:
        step = match.group(1).rstrip(".")
        subgate = match.group(2)
        via = "canonical" if text.startswith("OK ") and "PASO" not in text else "legacy-paso"
        return build(step, subgate, gates, phase, via)

    ui = re.fullmatch(r"OK\s+(DESIGN\s+SYSTEM|VISUAL|INTERACTION|VAADIN)", text)
    if ui:
        label = collapse(ui.group(1))
        return build("5", UI_SUBGATES.get(label, label), gates, phase, via="legacy-ui")

    return {
        "ok": False,
        "phase": phase,
        "step": None,
        "subgate": None,
        "canonical": None,
        "via": "unmatched",
        "errors": [f"unrecognized token '{collapse(token)}'"],
    }


def parse_canonical(value: str, gates: dict, phase: str | None, via: str) -> dict:
    text = collapse(value).upper()
    match = re.fullmatch(r"OK\s+(\d{1,2}[A-D]?)(?:\s*[.\s]\s*([A-Z][A-Z0-9_]*))?", text)
    if not match:
        return {
            "ok": False,
            "phase": phase,
            "step": None,
            "subgate": None,
            "canonical": None,
            "via": via,
            "errors": [f"alias target '{value}' is not canonical"],
        }
    return build(match.group(1).rstrip("."), match.group(2), gates, phase, via)


def list_tokens(gates: dict, phase: str) -> list[str]:
    cfg = gates.get("phases", {}).get(phase, {})
    tokens: list[str] = []
    for step in cfg.get("steps", []):
        tokens.append(f"OK {step}")
        tokens.extend(f"OK {step}.{sub}" for sub in cfg.get("subgates", {}).get(step, []))
    return tokens


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize and validate UP gate tokens.")
    parser.add_argument("--token", help="token typed by the user, e.g. 'OK PASO 14B IMPLEMENTAR'")
    parser.add_argument("--state", type=Path, help="path to the domain state.yaml")
    parser.add_argument("--domain", help="domain name under openspec/artifacts/")
    parser.add_argument("--phase", help="override the phase resolved from state")
    parser.add_argument("--draft", type=Path, help="draft file to hash for the approval record")
    parser.add_argument("--expect-hash", help="expected sha256 of --draft (sha256:...)")
    parser.add_argument("--list", action="store_true", help="list valid tokens for the phase")
    args = parser.parse_args(argv)

    if not GATES_PATH.is_file():
        print(json.dumps({"ok": False, "errors": [f"missing {GATES_PATH}"]}, indent=2))
        return 1

    gates = load_json(GATES_PATH)

    state_path = args.state or resolve_state(args.domain)
    if state_path is None or not state_path.is_file():
        print(
            json.dumps(
                {"ok": False, "errors": ["cannot resolve state.yaml; pass --domain or --state"]},
                indent=2,
            )
        )
        return 1

    phase = args.phase or read_phase(state_path)
    phase_source = "arguments" if args.phase else "state"

    if args.list:
        print(json.dumps({"phase": phase, "tokens": list_tokens(gates, phase)}, indent=2))
        return 0

    if not args.token:
        parser.error("--token is required unless --list is used")

    result = normalize(args.token, gates, phase)
    result["input"] = collapse(args.token)
    result["phase_source"] = phase_source
    result["state"] = str(state_path)

    if args.draft:
        if not args.draft.is_file():
            result["ok"] = False
            result["errors"].append(f"draft not found: {args.draft}")
        else:
            actual = sha256_file(args.draft)
            result["draft"] = {"path": str(args.draft), "sha256": actual}
            if args.expect_hash and args.expect_hash != actual:
                result["ok"] = False
                result["errors"].append(
                    f"hash mismatch: expected {args.expect_hash}, got {actual}"
                )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
