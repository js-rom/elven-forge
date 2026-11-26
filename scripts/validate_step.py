#!/usr/bin/env python3
"""Validate a step artifact against its declared checks.

Rules live in flows/step-checks.json, with artifact-level checks reused from
flows/shared.checks.json via {use: <artifact id>}.

Usage:
  python .agents/scripts/validate_step.py --step 2 --file draft.md
  python .agents/scripts/validate_step.py --phase inception --step 9 --file draft.md
  python .agents/scripts/validate_step.py --step 14B          # resolves the persisted Test Plan
  python .agents/scripts/validate_step.py --step 2 --list-checks

Stdlib only. Exit codes: 0 = pass (warnings allowed), 1 = errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_state import parse_artifacts, parse_scalar, read_state, read_state_fields  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".agents"
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"
STEP_CHECKS = AGENTS_DIR / "flows" / "step-checks.json"
SHARED_CHECKS = AGENTS_DIR / "flows" / "shared.checks.json"

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
UC_RE = re.compile(r"\bUC\d{2}\b")


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
        raise SystemExit("pass --domain or --state (multiple domains found)")
    return candidates[0]


def resolve_path(domain_dir: Path, raw_path: str, fields: dict) -> Path | None:
    path = parse_scalar(raw_path)
    iteration = parse_value(fields.get("iteration", ""))
    number = re.sub(r"^[A-Za-z]+", "", iteration)
    path = path.replace("{{#}}", number.zfill(2))
    path = path.replace("{{Iteration}}", iteration).replace("{Iteration}", iteration)
    if "{{" in path or "{" in path:
        return None
    return domain_dir / path


def parse_value(raw: str) -> str:
    return parse_scalar(raw).strip().strip('"')


def artifact_path(domain_dir: Path, lines: list[str], artifact_id: str, fields: dict) -> Path | None:
    for artifact in parse_artifacts(lines):
        if artifact["id"] == artifact_id:
            return resolve_path(domain_dir, artifact["keys"].get("path", ""), fields)
    return None


def expand_checks(step_spec: dict, shared: dict) -> tuple[list[dict], list[str]]:
    checks: list[dict] = []
    errors: list[str] = []
    for check in step_spec.get("checks", []):
        if "use" in check:
            artifact = check["use"]
            entry = shared.get("artifacts", {}).get(artifact)
            if not entry:
                errors.append(f"shared checks not found for artifact '{artifact}'")
                continue
            checks.extend(entry.get("checks", []))
        else:
            checks.append(check)
    return checks, errors


def check_headings(text: str, spec: dict) -> list[str]:
    levels = spec.get("levels") or [int(spec.get("level", 2))]
    optional = {heading.lower() for heading in spec.get("optional", [])}

    def present(name: str) -> bool:
        for level in levels:
            prefix = "#" * int(level)
            if re.search(rf"(?mi)^{re.escape(prefix)}\s+{re.escape(name)}\s*$", text):
                return True
        return False

    errors = []
    for heading in spec.get("require", []):
        if heading.lower() in optional:
            continue
        if not present(heading):
            errors.append(f"missing heading {levels} '{heading}'")
    for group in spec.get("any_of", []):
        if not any(present(heading) for heading in group):
            errors.append(f"missing one of the headings: {group}")
    return errors


def check_plantuml(text: str, spec: dict) -> list[str]:
    count = len(re.findall(r"```plantuml", text)) + len(re.findall(r"@startuml", text))
    minimum = int(spec.get("min", 1))
    if count < minimum:
        return [f"expected at least {minimum} PlantUML block(s), found {count}"]
    return []


def check_pattern(text: str, spec: dict) -> list[str]:
    regex = spec.get("regex", "")
    minimum = int(spec.get("min", 1))
    count = len(re.findall(regex, text))
    if count < minimum:
        return [f"pattern '{regex}' matched {count} times, expected at least {minimum}"]
    return []


def check_table_columns(text: str, spec: dict) -> list[str]:
    required = spec.get("require", [])
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(column in cells for column in required):
            return []
    return [f"no table contains all columns: {required}"]


def check_links(text: str, file: Path, spec: dict) -> list[str]:
    errors = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip().strip("<>").split(" ", 1)[0]
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        resolved = (file.parent / unquote(target)).resolve()
        if not resolved.exists():
            line = text[: match.start()].count("\n") + 1
            errors.append(f"line {line}: broken link '{target}'")
    return errors


def check_trace(text: str, from_text: str, spec: dict) -> tuple[list[str], list[str]]:
    source = set(UC_RE.findall(from_text))
    target = set(UC_RE.findall(text))
    missing = sorted(source - target)
    if not source:
        return [], ["trace source has no UC identifiers"]
    if not missing:
        return [], []
    message = f"missing trace for {missing}"
    if spec.get("strict"):
        return [message], []
    return [], [message]


def check_all_persisted(artifacts: list[dict], spec: dict) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []
    statuses = [(item["id"], parse_value(item["keys"].get("status", ""))) for item in artifacts]
    approved = [name for name, status in statuses if status == "approved"]
    if approved:
        errors.append(f"artifacts approved but not persisted: {approved}")
    if not any(status == "persisted" for _, status in statuses):
        warnings.append("no artifact is persisted")
    return errors, warnings


def check_evidence(domain_dir: Path, step: str, spec: dict, fields: dict) -> list[str]:
    journal = parse_value(fields.get("journal", "")) or f"journal/{parse_value(fields.get('iteration', ''))}"
    journal_root = domain_dir / journal
    index = journal_root / "index.json"
    if not index.is_file():
        return [f"journal index not found: {index.relative_to(domain_dir)}"]
    entries = json.loads(index.read_text(encoding="utf-8")).get("entries", [])
    selected = [entry for entry in entries if str(entry.get("step")) == str(step)]
    if not selected:
        selected = entries
    selected = sorted(selected, key=lambda item: item["file"])[-3:]
    text = ""
    for entry in selected:
        path = journal_root / entry["file"]
        if path.is_file():
            payload = json.loads(path.read_text(encoding="utf-8"))
            text += payload.get("raw", "") + "\n"
    regex = spec.get("regex", "")
    if not re.search(regex, text, re.IGNORECASE):
        return [f"journal evidence does not match '{regex}'"]
    return []


def check_state_field(lines: list[str], spec: dict) -> list[str]:
    field = spec.get("field", "")
    expected = spec.get("equals", "")
    for line in lines:
        match = re.match(rf"^{re.escape(field)}:\s*(.*)$", line)
        if match:
            value = match.group(1).split("#", 1)[0].strip().strip('"')
            if value != expected:
                return [f"state field '{field}' is '{value}', expected '{expected}'"]
            return []
    return [f"state field '{field}' not found"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a step artifact against its checks.")
    parser.add_argument("--step", required=True)
    parser.add_argument("--phase", choices=["elaboration", "inception"])
    parser.add_argument("--file", action="append", default=[], help="artifact file to validate (repeatable)")
    parser.add_argument("--from-file", type=Path, help="trace source override")
    parser.add_argument("--to-file", type=Path, help="trace target override")
    parser.add_argument("--domain")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--list-checks", action="store_true")
    args = parser.parse_args(argv)

    state_path = resolve_state(args.domain, args.state)
    if not state_path.is_file():
        print(json.dumps({"ok": False, "errors": [f"missing {state_path}"]}, indent=2))
        return 1

    state = read_state(state_path)
    fields = read_state_fields(state["lines"])
    phase = args.phase or parse_value(fields.get("phase", ""))
    domain_dir = state_path.parent

    rules = load_json(STEP_CHECKS)
    shared = load_json(SHARED_CHECKS)
    phase_rules = rules.get(phase, {})
    if args.step not in phase_rules:
        print(json.dumps({"ok": False, "errors": [f"no checks declared for {phase} step {args.step}"]}, indent=2))
        return 1

    step_spec = phase_rules[args.step]
    checks, errors = expand_checks(step_spec, shared)

    if args.list_checks:
        print(json.dumps({"phase": phase, "step": args.step, "checks": checks}, indent=2))
        return 0

    files: list[Path] = [Path(item) for item in args.file]
    if not files and step_spec.get("artifact"):
        resolved = artifact_path(domain_dir, state["lines"], step_spec["artifact"], fields)
        if resolved is None:
            errors.append(
                f"artifact '{step_spec['artifact']}' has unresolved placeholders; pass --file"
            )
        else:
            files = [resolved]

    results = []
    warnings: list[str] = []
    for check in checks:
        kind = check.get("kind")
        check_errors: list[str] = []
        check_warnings: list[str] = []

        if kind == "all_persisted":
            check_errors, check_warnings = check_all_persisted(parse_artifacts(state["lines"]), check)
        elif kind == "state_field":
            check_errors = check_state_field(state["lines"], check)
        elif kind == "evidence":
            check_errors = check_evidence(domain_dir, args.step, check, fields)
        elif kind == "trace":
            to_text = ""
            from_text = ""
            to_file = args.to_file or artifact_path(domain_dir, state["lines"], check.get("to", ""), fields)
            from_file = args.from_file or artifact_path(domain_dir, state["lines"], check.get("from", ""), fields)
            if to_file and Path(to_file).is_file():
                to_text = Path(to_file).read_text(encoding="utf-8")
            else:
                check_errors.append(f"trace target not found for '{check.get('to')}'; pass --to-file")
            if from_file and Path(from_file).is_file():
                from_text = Path(from_file).read_text(encoding="utf-8")
            else:
                check_errors.append(f"trace source not found for '{check.get('from')}'; pass --from-file")
            if to_text and from_text:
                check_errors_trace, check_warnings_trace = check_trace(to_text, from_text, check)
                check_errors.extend(check_errors_trace)
                check_warnings.extend(check_warnings_trace)
        elif not files:
            check_errors.append(f"check '{kind}' needs an artifact file; pass --file")
        else:
            for file in files:
                if not file.is_file():
                    check_errors.append(f"file not found: {file}")
                    continue
                text = file.read_text(encoding="utf-8")
                if kind == "headings":
                    check_errors.extend(f"{file.name}: {item}" for item in check_headings(text, check))
                elif kind == "plantuml":
                    check_errors.extend(f"{file.name}: {item}" for item in check_plantuml(text, check))
                elif kind == "pattern":
                    check_errors.extend(f"{file.name}: {item}" for item in check_pattern(text, check))
                elif kind == "table_columns":
                    check_errors.extend(f"{file.name}: {item}" for item in check_table_columns(text, check))
                elif kind == "links":
                    check_errors.extend(f"{file.name}: {item}" for item in check_links(text, file, check))
                else:
                    check_errors.append(f"unknown check kind '{kind}'")

        errors.extend(check_errors)
        warnings.extend(check_warnings)
        results.append({"kind": kind, "ok": not check_errors, "errors": check_errors, "warnings": check_warnings})

    if args.strict:
        errors.extend(warnings)
        warnings = []

    report = {
        "ok": not errors,
        "phase": phase,
        "step": args.step,
        "files": [str(item) for item in files],
        "checks": results,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
