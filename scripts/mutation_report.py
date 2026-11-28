#!/usr/bin/env python3
"""Read a PIT mutations.xml report and turn it into a triage decision.

The score alone is not a verdict. This script computes the five signals, applies
the project allowlist, pre-classifies survivors and emits a triage table plus a
baseline for the next iteration.

Contract: .agents/contracts/mutation.md
Stdlib only. Exit codes: 0 = ok, 1 = policy violation, 2 = usage/parse error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_state import read_state  # noqa: E402
from _metrics import record_event  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"

DETECTED = {"KILLED"}
EXCLUDED = {"NO_COVERAGE", "TIMED_OUT", "RUN_ERROR", "NON_VIABLE", "MEMORY_ERROR", "NOT_STARTED", "STARTED"}
ENVIRONMENT_METHODS = re.compile(r"^(get|set|is|toString|hashCode|equals)$")
ENVIRONMENT_CLASSES = re.compile(r"(Dto|DTO|Config|Application|Constants)$")

MEASURES = {
    "WEAK_ASSERTION": ("test-author", "Strengthen the assertion on the observable effect"),
    "MISSING_BEHAVIOR_TEST": ("test-author", "Add an equivalence-class or boundary case"),
    "NO_COVERAGE": ("test-author/implementer", "Add a test if reachable; otherwise remove dead code"),
    "SCOPE_GAP": ("orchestrator", "Covered by the full suite but outside targetTests; widen the scope or record it as evidence"),
    "DEAD_CODE": ("implementer", "Remove it, or justify and exclude it"),
    "EQUIVALENT": ("orchestrator", "Allowlist with rationale and evidence"),
    "DESIGN_GAP": ("orchestrator", "Route to 04/10/11; do not hide it behind a test"),
    "ENVIRONMENT": ("orchestrator", "Exclude with a documented pattern"),
    "UNCLASSIFIED": ("orchestrator", "Classify it before closing 14B"),
}


def read_field(lines: list[str], name: str) -> str:
    for line in lines:
        match = re.match(rf"^{re.escape(name)}:\s*(.*)$", line)
        if match:
            return match.group(1).split("#", 1)[0].strip().strip('"')
    return ""


def resolve_state(domain: str | None, state: Path | None) -> Path | None:
    if state:
        return state
    if domain:
        return ARTIFACTS_DIR / domain / "state.yaml"
    candidates = sorted(ARTIFACTS_DIR.glob("*/state.yaml"))
    return candidates[0] if len(candidates) == 1 else None


def short_mutator(value: str) -> str:
    return value.rsplit(".", 1)[-1]


def allowlist_key(entry: dict) -> str:
    return f"{entry['class']}#{entry['method']}:{entry['line']}:{entry['mutator']}"


def load_allowlist(path: Path | None) -> dict[str, dict]:
    if not path or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"cannot read allowlist {path}: {error}", file=sys.stderr)
        raise SystemExit(2)
    return {allowlist_key(entry): entry for entry in payload.get("entries", [])}


def load_triage(path: Path | None) -> dict[str, str]:
    if not path or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"cannot read triage {path}: {error}", file=sys.stderr)
        raise SystemExit(2)
    entries = payload.get("entries", payload)
    if isinstance(entries, list):
        return {entry["key"]: entry["class"] for entry in entries if entry.get("key") and entry.get("class")}
    return {str(key): str(value) for key, value in entries.items() if isinstance(value, str)}


def parse_report(path: Path) -> list[dict]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        print(f"cannot parse {path}: {error}", file=sys.stderr)
        raise SystemExit(2)
    mutants = []
    for node in root.findall("mutation"):
        mutants.append(
            {
                "status": (node.get("status") or "").upper(),
                "detected": node.get("detected") == "true",
                "tests_run": int(node.get("numberOfTestsRun") or 0),
                "source": node.findtext("sourceFile", ""),
                "class": node.findtext("mutatedClass", ""),
                "method": node.findtext("mutatedMethod", ""),
                "line": int(node.findtext("lineNumber", "0") or 0),
                "mutator": short_mutator(node.findtext("mutator", "")),
                "killing_test": node.findtext("killingTest", "") or "",
                "description": node.findtext("description", ""),
            }
        )
    return mutants


def classify(mutant: dict, allowlisted: bool) -> str:
    if mutant["status"] == "NO_COVERAGE":
        return "NO_COVERAGE"
    if allowlisted:
        return "EQUIVALENT"
    if ENVIRONMENT_METHODS.match(mutant["method"]) or ENVIRONMENT_CLASSES.search(mutant["class"]):
        return "ENVIRONMENT"
    if mutant["tests_run"] > 0:
        return "WEAK_ASSERTION"
    return "MISSING_BEHAVIOR_TEST"


def is_protected(mutant: dict, protected: set[str]) -> bool:
    return mutant["class"] in protected or f"{mutant['class']}#{mutant['method']}" in protected


def verdict_for(score: float, target: float, signals: dict) -> tuple[str, list[str]]:
    flags = []
    if signals["invariant_survivors"]:
        flags.append("CRITICAL")
    if signals["regression"]:
        flags.append("REGRESSION")
    if signals["no_coverage_ratio"] > 0.20:
        flags.append("BLIND_SPOTS")
    if not signals["actionable_survived"]:
        flags.append("ACCEPT" if signals["allowlisted"] else "PASS")
    elif score < target - 10:
        flags.append("REINFORCE")
    elif score < target:
        flags.append("IMPROVE")
    else:
        flags.append("PASS")
    priority = ["CRITICAL", "REGRESSION", "BLIND_SPOTS", "REINFORCE", "IMPROVE", "PASS", "ACCEPT"]
    verdict = next(item for item in priority if item in flags)
    return verdict, flags


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize and triage a PIT report.")
    parser.add_argument("--xml", type=Path, required=True)
    parser.add_argument("--domain")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--iteration")
    parser.add_argument("--target", type=float, default=70.0)
    parser.add_argument("--policy", choices=["advisory", "blocking"], default="advisory")
    parser.add_argument("--allowlist", type=Path)
    parser.add_argument("--triage", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--journal-dir", type=Path)
    parser.add_argument("--baseline-out", type=Path)
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--protected-invariants", default="")
    parser.add_argument("--strict-triage", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    mutants = parse_report(args.xml)
    if not mutants:
        print(json.dumps({"ok": False, "errors": ["no mutations in report"]}, indent=2))
        return 2

    counts = {status: 0 for status in ("KILLED", "SURVIVED", "NO_COVERAGE", "TIMED_OUT")}
    for mutant in mutants:
        counts[mutant["status"]] = counts.get(mutant["status"], 0) + 1
    killed = counts.get("KILLED", 0)
    survived = counts.get("SURVIVED", 0)
    no_coverage = counts.get("NO_COVERAGE", 0)
    generated = len(mutants)

    allowlist = load_allowlist(args.allowlist)
    triage_map = load_triage(args.triage)
    protected = {item.strip() for item in args.protected_invariants.split(",") if item.strip()}

    survivors = []
    allowlisted = 0
    invariant_survivors = []
    for mutant in mutants:
        if mutant["status"] not in ("SURVIVED", "NO_COVERAGE"):
            continue
        key = f"{mutant['class']}#{mutant['method']}:{mutant['line']}:{mutant['mutator']}"
        entry = allowlist.get(key)
        suggested = classify(mutant, entry is not None)
        triaged = triage_map.get(key, suggested)
        confirmed = key in triage_map or entry is not None
        if triaged not in MEASURES:
            triaged = "UNCLASSIFIED"
        if entry is not None and triaged == "EQUIVALENT":
            allowlisted += 1
        if triaged != "EQUIVALENT" and is_protected(mutant, protected):
            invariant_survivors.append(mutant)
        owner, measure = MEASURES.get(triaged, MEASURES["UNCLASSIFIED"])
        survivors.append(
            {
                **mutant,
                "key": key,
                "suggested_as": suggested,
                "triaged_as": triaged,
                "confirmed": confirmed,
                "owner": owner,
                "measure": measure,
            }
        )

    actionable_survived = survived - allowlisted
    denominator = killed + survived
    score = (killed / denominator * 100.0) if denominator else 0.0
    actionable_denominator = killed + actionable_survived
    score_actionable = (killed / actionable_denominator * 100.0) if actionable_denominator else 0.0
    no_coverage_ratio = (no_coverage / generated) if generated else 0.0

    baseline = None
    if args.baseline and args.baseline.is_file():
        try:
            baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            baseline = None
    delta = round(score - float(baseline["score"]), 1) if baseline and "score" in baseline else None

    signals = {
        "invariant_survivors": len(invariant_survivors),
        "regression": baseline is not None and delta is not None and delta < -5,
        "no_coverage_ratio": no_coverage_ratio,
        "actionable_survived": actionable_survived,
        "allowlisted": allowlisted,
    }
    verdict, flags = verdict_for(score_actionable, args.target, signals)

    unclassified = [
        item
        for item in survivors
        if item["triaged_as"] == "UNCLASSIFIED" or (args.strict_triage and not item["confirmed"])
    ]
    policy_failure = args.policy == "blocking" and verdict in ("CRITICAL", "REGRESSION")
    strict_failure = bool(args.strict_triage and unclassified)

    state_path = resolve_state(args.domain, args.state)
    iteration = args.iteration
    journal_dir = args.journal_dir
    step = ""
    if state_path and state_path.is_file():
        state = read_state(state_path)
        iteration = iteration or read_field(state["lines"], "iteration")
        step = read_field(state["lines"], "current_step")
        journal = read_field(state["lines"], "journal") or f"journal/{iteration}"
        journal_dir = journal_dir or (state_path.parent / journal)
    iteration = iteration or "unknown"

    summary = {
        "ok": not (policy_failure or strict_failure),
        "iteration": iteration,
        "score": round(score, 1),
        "score_actionable": round(score_actionable, 1),
        "target": args.target,
        "delta": delta,
        "generated": generated,
        "killed": killed,
        "survived": survived,
        "actionable_survived": actionable_survived,
        "allowlisted": allowlisted,
        "no_coverage": no_coverage,
        "no_coverage_ratio": round(no_coverage_ratio * 100.0, 1),
        "verdict": verdict,
        "flags": flags,
        "policy": args.policy,
        "protected_invariants": sorted(protected),
        "unclassified": len(unclassified),
        "confirmed": sum(1 for item in survivors if item["confirmed"]),
    }

    if args.state or args.domain:
        record_event(
            state_path,
            {
                "tool": "mutation",
                "phase": "elaboration",
                "step": step,
                "iteration": iteration,
                "score": summary["score"],
                "survived": survived,
                "no_coverage": no_coverage,
                "verdict": verdict,
                "ok": summary["ok"],
            },
        )

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "mutation-summary.json").write_text(
            json.dumps({**summary, "survivors": survivors}, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (args.out_dir / "triage.md").write_text(render_triage(summary, survivors), encoding="utf-8", newline="\n")

    if args.write_baseline or args.baseline_out:
        target = args.baseline_out or ((journal_dir or (REPO_ROOT / ".atl")) / "mutation-baseline.json")
        write_baseline(target, summary, survivors)

    if args.json:
        print(json.dumps({**summary, "survivors": survivors}, indent=2, ensure_ascii=False))
    else:
        print(render_reading(summary, survivors))

    return 1 if (policy_failure or strict_failure) else 0


def write_baseline(path: Path, summary: dict, survivors: list[dict]) -> None:
    payload = {
        "iteration": summary["iteration"],
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "score": summary["score"],
        "target": summary["target"],
        "generated": summary["generated"],
        "killed": summary["killed"],
        "survived": summary["survived"],
        "no_coverage": summary["no_coverage"],
        "allowlisted": summary["allowlisted"],
        "verdict": summary["verdict"],
        "survivors": [
            {key: item[key] for key in ("class", "method", "line", "mutator", "status", "triaged_as")}
            for item in survivors
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def render_triage(summary: dict, survivors: list[dict]) -> str:
    trend = "-" if summary["delta"] is None else f"{summary['delta']:+.1f}"
    lines = [
        "## Test Quality (Mutation)",
        "",
        "| Slice | Score | Target | Killed | Survived | No coverage | Trend | Verdict |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
        f"| {summary['iteration']} | {summary['score']}% | {summary['target']:.0f} | {summary['killed']} | "
        f"{summary['survived']} | {summary['no_coverage']} | {trend} | {summary['verdict']} |",
        "",
        "| Mutant | Class | Line | Mutator | Status | Triaged as | Confirmed | Measure | Owner |",
        "| :--- | :--- | ---: | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for item in survivors:
        lines.append(
            f"| `{item['method']}` | `{item['class']}` | {item['line']} | {item['mutator']} | "
            f"{item['status']} | {item['triaged_as']} | {'yes' if item['confirmed'] else 'no'} | "
            f"{item['measure']} | {item['owner']} |"
        )
    if not survivors:
        lines.append("| - | - | - | - | - | - | - | - | - |")
    lines.append("")
    return "\n".join(lines)


def render_reading(summary: dict, survivors: list[dict]) -> str:
    trend = "first baseline" if summary["delta"] is None else f"{summary['delta']:+.1f} vs baseline"
    lines = [
        f"Score {summary['score']}% (target {summary['target']:.0f}) | {trend} | "
        f"{summary['generated']} mutants, {summary['survived']} survived, {summary['no_coverage']} no coverage",
        f"Verdict: {summary['verdict']} ({', '.join(summary['flags'])}) | policy: {summary['policy']}",
    ]
    if summary["unclassified"]:
        lines.append(f"Unclassified survivors: {summary['unclassified']} (blocks triage)")
    for item in survivors:
        marker = "" if item["confirmed"] else " (suggested)"
        lines.append(
            f"- {item['triaged_as']:<22}{marker} {item['class']}#{item['method']}:{item['line']} "
            f"[{item['mutator']}] -> {item['owner']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
