#!/usr/bin/env python3
"""Parity check for the elaboration split.

Compares the previous monolithic SKILL.md (from git) with the new step
contracts and the machine manifest, so no artifact or rule is lost in the
split.

Checks:
  1. step ids in the old mapping table == step ids in elaboration.checks.json
  2. artifacts per step match (with an alias table for renamed artifacts)
  3. every contract exists and has the six required sections
  4. every gate in the manifest is valid for the elaboration phase
  5. step ids in elaboration.flow.yaml == step ids in the manifest

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
SKILL_REL = "skills/up-elaboration/SKILL.md"
CHECKS_PATH = AGENTS_DIR / "flows" / "elaboration.checks.json"
FLOW_PATH = AGENTS_DIR / "flows" / "elaboration.flow.yaml"
GATES_PATH = AGENTS_DIR / "flows" / "gates.json"
STEPS_DIR = AGENTS_DIR / "steps" / "elaboration"
BASELINE = AGENTS_DIR / "flows" / "baseline" / "up-elaboration.SKILL.pre-split.md"

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


def normalize(name: str) -> str:
    key = re.sub(r"\s+", " ", name.strip()).lower()
    return ALIASES.get(key, name.strip())


def load_old_skill(repo: Path, rel_path: str, rev: str, base_file: Path | None) -> str:
    if base_file is None and BASELINE.is_file():
        base_file = BASELINE
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


def parse_old_mapping(text: str) -> dict[str, set[str]]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if "Artifact-Step Mapping for Elaboration" in line:
            start = index
            break
    if start is None:
        raise SystemExit("old SKILL.md has no 'Artifact-Step Mapping for Elaboration' section")

    mapping: dict[str, set[str]] = {}
    for line in lines[start:]:
        match = re.match(r"^\|\s*([0-9]{1,2}[A-D]?)\s*\|(.*?)\|", line)
        if not match:
            if mapping and line.startswith("|"):
                continue
            if mapping and not line.startswith("|") and line.strip() == "":
                break
            continue
        step, cell = match.group(1), match.group(2)
        artifacts = {normalize(item) for item in re.findall(r"`([^`]+)`", cell)}
        mapping[step] = artifacts
    return mapping


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_gate(token: str, phase_cfg: dict) -> str | None:
    match = re.fullmatch(r"OK\s+(\d{1,2}[A-D]?)(?:\.([A-Z][A-Z0-9_]*))?", token)
    if not match:
        return f"gate '{token}' is not canonical"
    step, subgate = match.group(1), match.group(2)
    if step not in phase_cfg.get("steps", []):
        return f"gate '{token}': step {step} is not in the elaboration phase"
    if subgate and subgate not in phase_cfg.get("subgates", {}).get(step, []):
        return f"gate '{token}': subgate {subgate} is not declared for step {step}"
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check parity between the old SKILL.md and the split.")
    parser.add_argument("--repo", type=Path, default=AGENTS_DIR, help="git repo containing the old skill")
    parser.add_argument("--rel-path", default=SKILL_REL, help="skill path inside --repo")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--base-file", type=Path, help="read the old skill from a file instead of git")
    args = parser.parse_args(argv)

    old_text = load_old_skill(args.repo, args.rel_path, args.rev, args.base_file)
    old_mapping = parse_old_mapping(old_text)
    manifest = load_json(CHECKS_PATH)
    new_steps = manifest["steps"]
    gates_cfg = load_json(GATES_PATH)["phases"]["elaboration"]

    errors: list[str] = []
    warnings: list[str] = []

    old_ids = set(old_mapping)
    new_ids = set(new_steps)
    if old_ids != new_ids:
        errors.append(
            f"step ids differ: missing in new {sorted(old_ids - new_ids)}, "
            f"extra in new {sorted(new_ids - old_ids)}"
        )

    for step in sorted(old_ids & new_ids):
        old_artifacts = old_mapping[step]
        new_artifacts = {normalize(item) for item in new_steps[step].get("produces", [])}
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
            problem = check_gate(token, gates_cfg)
            if problem:
                errors.append(f"step {step}: {problem}")

    flow_ids = set(
        re.findall(r"(?m)^\s{2}- id:\s*\"?([0-9]{1,2}[A-D]?)\"?\s*$", FLOW_PATH.read_text(encoding="utf-8"))
    )
    if flow_ids != new_ids:
        errors.append(
            f"flow.yaml ids differ from manifest: missing {sorted(new_ids - flow_ids)}, "
            f"extra {sorted(flow_ids - new_ids)}"
        )

    report = {
        "ok": not errors,
        "old_steps": len(old_ids),
        "new_steps": len(new_ids),
        "contracts": len(list(STEPS_DIR.glob("*.md"))),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
