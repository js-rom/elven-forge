#!/usr/bin/env python3
"""Parity check for the UP phase split.

For each phase, compares the previous monolithic SKILL.md (from a frozen
baseline or git) with the new step contracts and the machine manifest.

Checks per phase:
  1. step ids in the old mapping table == step ids in <phase>.checks.json
     (plus explicitly allowed bootstrap steps)
  2. artifacts per step match the schema artifact ids
  3. every contract exists and has the six required sections
  4. every gate in the manifest is valid for the phase
  5. step ids in <phase>.flow.yaml == step ids in the manifest

Stdlib only. Exit codes: 0 = parity, 1 = mismatch.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".agents"
GATES_PATH = AGENTS_DIR / "flows" / "gates.json"
SCHEMA_PATH = REPO_ROOT / "openspec" / "schemas" / "default" / "schema.yaml"
SCHEMA_FALLBACK = AGENTS_DIR / "skills" / "storage" / "openspec" / "schemas" / "default" / "schema.yaml"

REQUIRED_SECTIONS = [
    "## Inputs",
    "## Output contract",
    "## Preconditions",
    "## Rubric",
    "## Evidence required",
    "## Anti-patterns",
]

ALIASES = {
    "technical memos": "Technical Memo",
    "state visual specs": "Visual Specs",
    "vaadin mapping": "UI Technology Mapping",
    "logical view packages": "Logical View Package Diagram",
    "packagediagram.plantuml": "Logical View Package Diagram",
    "classdiagram.plantuml": "Logical View Class Diagram",
    "design class diagrams": "Logical View Class Diagram",
}

PHASES = {
    "elaboration": {
        "skill_rel": "skills/up-elaboration/SKILL.md",
        "section": "Artifact-Step Mapping for Elaboration",
        "checks": AGENTS_DIR / "flows" / "elaboration.checks.json",
        "flow": AGENTS_DIR / "flows" / "elaboration.flow.yaml",
        "steps": AGENTS_DIR / "steps" / "elaboration",
        "baseline": AGENTS_DIR / "flows" / "baseline" / "up-elaboration.SKILL.pre-split.md",
        "bootstrap_steps": [],
    },
    "inception": {
        "skill_rel": "skills/up-inception/SKILL.md",
        "section": "Artifact-Step Mapping for Inception",
        "checks": AGENTS_DIR / "flows" / "inception.checks.json",
        "flow": AGENTS_DIR / "flows" / "inception.flow.yaml",
        "steps": AGENTS_DIR / "steps" / "inception",
        "baseline": AGENTS_DIR / "flows" / "baseline" / "up-inception.SKILL.pre-split.md",
        "bootstrap_steps": ["0"],
    },
}

PARITY_OVERRIDES = {
    "elaboration": {
        "14D": {"drop": ["Test Plan"], "add": ["Iteration Verification"]},
    }
}


def normalize(name: str) -> str:
    key = re.sub(r"\s+", " ", name.strip()).lower()
    return ALIASES.get(key, name.strip())


def load_old_skill(repo: Path, rel_path: str, rev: str, base_file: Path | None) -> str:
    if base_file:
        return base_file.read_text(encoding="utf-8")
    attempts = [
        ["git", "-C", str(repo), "show", f"{rev}:{rel_path}"],
        ["git", "-C", str(REPO_ROOT), "show", f"{rev}:.agents/{rel_path}"],
    ]
    errors = []
    for command in attempts:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            return result.stdout
        errors.append(result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "unknown")
    raise SystemExit("cannot read previous SKILL.md: " + " | ".join(errors))


def parse_old_mapping(text: str, section: str) -> dict[str, str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if section in line:
            start = index
            break
    if start is None:
        raise SystemExit(f"old SKILL.md has no '{section}' section")

    mapping: dict[str, str] = {}
    for line in lines[start:]:
        match = re.match(r"^\|\s*([0-9]{1,2}[A-D]?)\s*\|(.*?)\|", line)
        if not match:
            if mapping and line.startswith("|"):
                continue
            if mapping and not line.startswith("|") and line.strip() == "":
                break
            continue
        mapping[match.group(1)] = match.group(2)
    return mapping


def load_schema_ids(path: Path) -> set[str]:
    if not path.is_file():
        path = SCHEMA_FALLBACK
    text = path.read_text(encoding="utf-8")
    return {m.group(1).strip().strip('"') for m in re.finditer(r"(?m)^\s*- id:\s*(.+?)\s*$", text)}


def artifacts_in_cell(cell: str, known: set[str], aliases: dict[str, str]) -> set[str]:
    found = {normalize(item) for item in re.findall(r"`([^`]+)`", cell)}
    lowered = cell.lower()
    for alias, target in aliases.items():
        if alias in lowered:
            found.add(target)
    allowed = known | set(aliases.values())
    return {item for item in found if item in allowed}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_gate(token: str, phase_cfg: dict) -> str | None:
    match = re.fullmatch(r"OK\s+(\d{1,2}[A-D]?)(?:\.([A-Z][A-Z0-9_]*))?", token)
    if not match:
        return f"gate '{token}' is not canonical"
    step, subgate = match.group(1), match.group(2)
    if step not in phase_cfg.get("steps", []):
        return f"gate '{token}': step {step} is not in the phase"
    if subgate and subgate not in phase_cfg.get("subgates", {}).get(step, []):
        return f"gate '{token}': subgate {subgate} is not declared for step {step}"
    return None


def check_phase(name: str, cfg: dict, schema_ids: set[str], gates: dict, args) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    phase_cfg = gates["phases"][name]

    old_text = load_old_skill(args.repo, cfg["skill_rel"], args.rev, args.base_file or (
        cfg["baseline"] if cfg["baseline"].is_file() else None
    ))
    old_mapping = parse_old_mapping(old_text, cfg["section"])
    manifest = load_json(cfg["checks"])
    new_steps = manifest["steps"]

    for step, spec in new_steps.items():
        for artifact in spec.get("produces", []):
            if normalize(artifact) not in schema_ids:
                errors.append(f"step {step}: produced artifact '{artifact}' is not a schema id")

    old_ids = set(old_mapping) | set(cfg["bootstrap_steps"])
    new_ids = set(new_steps)
    if old_ids != new_ids:
        errors.append(
            f"step ids differ: missing in new {sorted(old_ids - new_ids)}, "
            f"extra in new {sorted(new_ids - old_ids)}"
        )

    for step in sorted(old_ids & new_ids):
        old_artifacts = artifacts_in_cell(old_mapping.get(step, ""), schema_ids, ALIASES)
        new_artifacts = {normalize(item) for item in new_steps[step].get("produces", [])}
        override = PARITY_OVERRIDES.get(name, {}).get(step)
        if override:
            old_artifacts = set(old_artifacts)
            for item in override.get("drop", []):
                old_artifacts.discard(item)
            for item in override.get("add", []):
                old_artifacts.add(item)
            warnings.append(f"step {step}: parity override applied ({override})")
        if old_artifacts != new_artifacts:
            errors.append(
                f"step {step}: artifacts differ; missing {sorted(old_artifacts - new_artifacts)}, "
                f"extra {sorted(new_artifacts - old_artifacts)}"
            )

        contract = AGENTS_DIR / new_steps[step]["contract"]
        if not contract.is_file():
            errors.append(f"step {step}: missing contract {contract.relative_to(AGENTS_DIR)}")
            continue
        body = contract.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if not re.search(rf"(?m)^{re.escape(section)}\s*$", body):
                errors.append(f"step {step}: contract lacks section '{section}'")
        line_count = len(body.splitlines())
        if line_count > 80:
            warnings.append(f"step {step}: contract has {line_count} lines (target <= 80)")

        for token in new_steps[step].get("gates", []):
            problem = check_gate(token, phase_cfg)
            if problem:
                errors.append(f"step {step}: {problem}")

    flow_ids = set(
        re.findall(r"(?m)^\s{2}- id:\s*\"?([0-9]{1,2}[A-D]?)\"?\s*$", cfg["flow"].read_text(encoding="utf-8"))
    )
    if flow_ids != new_ids:
        errors.append(
            f"flow.yaml ids differ from manifest: missing {sorted(new_ids - flow_ids)}, "
            f"extra {sorted(flow_ids - new_ids)}"
        )

    return {
        "old_steps": len(old_ids),
        "new_steps": len(new_ids),
        "contracts": len(list(cfg["steps"].glob("*.md"))),
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check parity between the old SKILL.md and the split.")
    parser.add_argument("--repo", type=Path, default=AGENTS_DIR, help="git repo containing the old skills")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--phase", choices=["both", "elaboration", "inception"], default="both")
    parser.add_argument("--base-file", type=Path, help="read the old skill from a file (single phase only)")
    args = parser.parse_args(argv)

    selected = ["elaboration", "inception"] if args.phase == "both" else [args.phase]
    if args.base_file and len(selected) > 1:
        parser.error("--base-file requires a single --phase")

    schema_ids = load_schema_ids(SCHEMA_PATH)
    gates = load_json(GATES_PATH)

    results: dict[str, dict] = {}
    all_errors: list[str] = []
    all_warnings: list[str] = []
    for name in selected:
        phase_result = check_phase(name, PHASES[name], schema_ids, gates, args)
        results[name] = phase_result
        all_errors.extend(f"[{name}] {item}" for item in phase_result["errors"])
        all_warnings.extend(f"[{name}] {item}" for item in phase_result["warnings"])

    report = {
        "ok": not all_errors,
        "phases": results,
        "errors": all_errors,
        "warnings": all_warnings,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not all_errors else 1


if __name__ == "__main__":
    sys.exit(main())
