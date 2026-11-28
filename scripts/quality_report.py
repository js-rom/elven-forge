#!/usr/bin/env python3
"""Read SonarQube (plus ArchUnit/Trivy) and turn it into a code-quality verdict.

The gate is read over the iteration's new code, never over the whole legacy
repository. The script emits a scorecard, a triage table and a baseline.

Contract: .agents/contracts/quality.md
Stdlib only. Exit codes: 0 = ok, 1 = policy violation, 2 = usage/parse error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_state import read_state  # noqa: E402
from _metrics import record_event  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"

METRICS = (
    "bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,"
    "sqale_index,ncloc,new_bugs,new_vulnerabilities,new_code_smells,new_coverage,"
    "new_duplicated_lines_density,new_technical_debt,new_lines,new_security_hotspots_reviewed"
)

MEASURES = {
    "BUG": ("implementer", "Fix the defect and keep the tests green"),
    "VULNERABILITY": ("implementer", "Fix or mitigate; allowlist only if false positive"),
    "SECURITY_HOTSPOT": ("implementer", "Review and mark safe, or fix"),
    "CODE_SMELL": ("implementer", "Refactor, or defer with a debt ID"),
    "ARCHITECTURE": ("orchestrator", "Route to 8/11 and fix the dependency"),
    "COVERAGE_GAP": ("test-author", "Add a test for the new lines"),
    "DEPENDENCY_RISK": ("implementer", "Upgrade or mitigate the dependency"),
    "FALSE_POSITIVE": ("orchestrator", "Allowlist with rationale and evidence"),
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


def http_json(url: str, token: str) -> dict:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as error:  # noqa: BLE001
        print(f"sonar request failed: {url}: {error}", file=sys.stderr)
        raise SystemExit(2)


def fetch_issues(host: str, token: str, project: str, scope: str) -> dict:
    issues: list[dict] = []
    page = 1
    total = 0
    while page <= 20:
        params = {
            "componentKeys": project,
            "resolved": "false",
            "ps": "500",
            "p": str(page),
        }
        if scope == "new":
            params["inNewCodePeriod"] = "true"
        query = urllib.parse.urlencode(params)
        payload = http_json(f"{host}/api/issues/search?{query}", token)
        total = int(payload.get("total", 0))
        batch = payload.get("issues", []) or []
        issues.extend(batch)
        if len(issues) >= total or not batch:
            break
        page += 1
    return {"total": total, "list": issues}


def fetch_snapshot(host: str, token: str, project: str, version: str, scope: str) -> dict:
    gate = http_json(f"{host}/api/qualitygates/project_status?projectKey={urllib.parse.quote(project)}", token)
    measures = http_json(
        f"{host}/api/measures/component?component={urllib.parse.quote(project)}&metricKeys={METRICS}", token
    )
    issues = fetch_issues(host, token, project, scope)
    return {
        "project": project,
        "version": version,
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "scope": scope,
        "gate": gate.get("projectStatus", {}),
        "measures": measures.get("component", {}).get("measures", []),
        "issues": issues,
    }


def load_allowlist(path: Path | None) -> dict[str, dict]:
    if not path or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"cannot read allowlist {path}: {error}", file=sys.stderr)
        raise SystemExit(2)
    return {
        f"{entry['rule']}#{entry['component']}:{entry['line']}": entry
        for entry in payload.get("entries", [])
        if entry.get("rule") and entry.get("component") and entry.get("line") is not None
    }


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


def issue_type(issue: dict) -> str:
    kind = (issue.get("type") or "").upper()
    if kind in ("BUG", "VULNERABILITY", "CODE_SMELL", "SECURITY_HOTSPOT"):
        return kind
    for impact in issue.get("impacts", []) or []:
        quality = (impact.get("softwareQuality") or "").upper()
        if quality == "RELIABILITY":
            return "BUG"
        if quality == "SECURITY":
            return "VULNERABILITY"
        if quality == "MAINTAINABILITY":
            return "CODE_SMELL"
    return "UNCLASSIFIED"


def is_critical(issue: dict) -> bool:
    kind = issue_type(issue)
    if kind not in ("BUG", "VULNERABILITY"):
        return False
    if (issue.get("severity") or "").upper() in ("BLOCKER", "CRITICAL"):
        return True
    for impact in issue.get("impacts", []) or []:
        if (impact.get("severity") or "").upper() == "HIGH" and (impact.get("softwareQuality") or "").upper() in (
            "SECURITY",
            "RELIABILITY",
        ):
            return True
    return False


def measure_value(measures: dict[str, str], key: str, fallback: str | None = None) -> float | None:
    value = measures.get(key)
    if value is None and fallback:
        value = measures.get(fallback)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def normalize_issue(issue: dict, project: str) -> dict:
    component = issue.get("component", "")
    prefix = f"{project}:"
    if component.startswith(prefix):
        component = component[len(prefix):]
    return {
        "key": issue.get("key", ""),
        "rule": issue.get("rule", ""),
        "type": issue_type(issue),
        "severity": (issue.get("severity") or "").upper(),
        "component": component,
        "line": int(issue.get("line") or 0),
        "message": issue.get("message", ""),
        "impacts": issue.get("impacts", []) or [],
    }


def verdict_for(signals: dict, target_coverage: float, max_duplication: float, policy: str) -> tuple[str, list[str]]:
    flags = []
    if signals["critical"] or signals["architecture"] or signals["dependencies"]:
        flags.append("BLOCK")
    if signals["regression"]:
        flags.append("REGRESSION")
    if signals["coverage"] is not None and signals["coverage"] < target_coverage:
        flags.append("BLOCK" if policy == "blocking" else "IMPROVE")
    if signals["duplication"] is not None and signals["duplication"] > max_duplication:
        flags.append("IMPROVE")
    if signals["critical_smells"]:
        flags.append("IMPROVE")
    if not flags:
        flags.append("ACCEPT" if signals["all_allowlisted"] and signals["issues"] else "PASS")
    priority = ["BLOCK", "REGRESSION", "IMPROVE", "PASS", "ACCEPT"]
    verdict = next(item for item in priority if item in flags)
    return verdict, flags


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize and triage a SonarQube analysis.")
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--save-snapshot", type=Path)
    parser.add_argument("--host", default="http://localhost:9000")
    parser.add_argument("--token", default=os.environ.get("SONAR_TOKEN", ""))
    parser.add_argument("--project-key")
    parser.add_argument("--version", default="")
    parser.add_argument("--scope", choices=["new", "all"], default="new")
    parser.add_argument("--mode", choices=["baseline", "iteration"], default="iteration")
    parser.add_argument("--domain")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--iteration")
    parser.add_argument("--policy", choices=["advisory", "blocking"], default="advisory")
    parser.add_argument("--target-coverage", type=float, default=80.0)
    parser.add_argument("--max-duplication", type=float, default=3.0)
    parser.add_argument("--max-coverage-drop", type=float, default=5.0)
    parser.add_argument("--max-duplication-rise", type=float, default=2.0)
    parser.add_argument("--allowlist", type=Path)
    parser.add_argument("--triage", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--journal-dir", type=Path)
    parser.add_argument("--baseline-out", type=Path)
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--architecture-violations", type=int, default=0)
    parser.add_argument("--critical-cves", type=int, default=0)
    parser.add_argument("--strict-triage", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

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

    if args.snapshot:
        try:
            snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            print(f"cannot read snapshot {args.snapshot}: {error}", file=sys.stderr)
            return 2
    else:
        project = args.project_key or args.domain
        if not project or not args.token:
            print("pass --project-key and SONAR_TOKEN (or --snapshot)", file=sys.stderr)
            return 2
        snapshot = fetch_snapshot(args.host, args.token, project, args.version or iteration, args.scope)
        if args.save_snapshot:
            args.save_snapshot.parent.mkdir(parents=True, exist_ok=True)
            args.save_snapshot.write_text(
                json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )

    project = snapshot.get("project", args.project_key or args.domain or "unknown")
    version = snapshot.get("version", args.version or iteration)
    gate = snapshot.get("gate", {}) or {}
    gate_status = (gate.get("status") or "UNKNOWN").upper()
    conditions = gate.get("conditions", []) or []
    measures = {item["metric"]: item.get("value") for item in snapshot.get("measures", []) if item.get("metric")}

    coverage = measure_value(measures, f"{'new_' if args.scope == 'new' else ''}coverage", "coverage")
    duplication = measure_value(
        measures, f"{'new_' if args.scope == 'new' else ''}duplicated_lines_density", "duplicated_lines_density"
    )
    new_lines = measure_value(measures, "new_lines") or 0
    new_code = args.scope == "new" and new_lines > 0

    allowlist = load_allowlist(args.allowlist)
    triage_map = load_triage(args.triage)
    issues = [normalize_issue(item, project) for item in snapshot.get("issues", {}).get("list", [])]

    survivors = []
    critical = 0
    critical_smells = 0
    allowlisted = 0
    for issue in issues:
        key = f"{issue['rule']}#{issue['component']}:{issue['line']}"
        entry = allowlist.get(key)
        suggested = "FALSE_POSITIVE" if entry else issue["type"]
        triaged = triage_map.get(key, suggested)
        confirmed = key in triage_map or entry is not None
        if triaged not in MEASURES:
            triaged = "UNCLASSIFIED"
        if triaged == "FALSE_POSITIVE":
            allowlisted += 1
        if triaged in ("BUG", "VULNERABILITY") and is_critical(issue):
            critical += 1
        if triaged == "CODE_SMELL" and issue["severity"] in ("BLOCKER", "CRITICAL"):
            critical_smells += 1
        owner, measure = MEASURES.get(triaged, MEASURES["UNCLASSIFIED"])
        survivors.append(
            {
                **issue,
                "key": key,
                "triaged_as": triaged,
                "confirmed": confirmed,
                "owner": owner,
                "measure": measure,
            }
        )

    baseline = None
    if args.baseline and args.baseline.is_file():
        try:
            baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            baseline = None
    regression = False
    delta = None
    if baseline:
        base_coverage = baseline.get("coverage")
        base_duplication = baseline.get("duplication")
        if base_coverage is not None and coverage is not None:
            delta = round(coverage - float(base_coverage), 1)
            if float(base_coverage) - coverage > args.max_coverage_drop:
                regression = True
        if base_duplication is not None and duplication is not None:
            if duplication - float(base_duplication) > args.max_duplication_rise:
                regression = True

    signals = {
        "critical": critical,
        "critical_smells": critical_smells,
        "architecture": args.architecture_violations,
        "dependencies": args.critical_cves,
        "coverage": coverage,
        "duplication": duplication,
        "regression": regression,
        "issues": len(survivors),
        "all_allowlisted": bool(survivors) and allowlisted == len(survivors),
    }
    verdict, flags = verdict_for(signals, args.target_coverage, args.max_duplication, args.policy)
    flags = list(dict.fromkeys(flags))
    if args.mode == "baseline":
        verdict = "BASELINE"

    unclassified = [
        item
        for item in survivors
        if item["triaged_as"] == "UNCLASSIFIED" or (args.strict_triage and not item["confirmed"])
    ]
    policy_failure = args.mode == "iteration" and args.policy == "blocking" and verdict in ("BLOCK", "REGRESSION")
    strict_failure = bool(args.strict_triage and unclassified)

    summary = {
        "ok": not (policy_failure or strict_failure),
        "iteration": iteration,
        "project": project,
        "version": version,
        "scope": args.scope,
        "mode": args.mode,
        "new_code": new_code,
        "gate": gate_status,
        "conditions": conditions,
        "verdict": verdict,
        "flags": flags,
        "coverage": round(coverage, 1) if coverage is not None else None,
        "duplication": round(duplication, 1) if duplication is not None else None,
        "target_coverage": args.target_coverage,
        "max_duplication": args.max_duplication,
        "issues": len(survivors),
        "critical": critical,
        "critical_smells": critical_smells,
        "allowlisted": allowlisted,
        "architecture_violations": args.architecture_violations,
        "critical_cves": args.critical_cves,
        "regression": regression,
        "coverage_delta": delta,
        "policy": args.policy,
        "unclassified": len(unclassified),
        "confirmed": sum(1 for item in survivors if item["confirmed"]),
    }

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "quality-summary.json").write_text(
            json.dumps({**summary, "findings": survivors}, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (args.out_dir / "triage.md").write_text(render_triage(summary, survivors), encoding="utf-8", newline="\n")

    if args.write_baseline or args.baseline_out:
        target = args.baseline_out or ((journal_dir or (REPO_ROOT / ".atl")) / "quality-baseline.json")
        write_baseline(target, summary)

    if args.state or args.domain:
        record_event(
            state_path,
            {
                "tool": "quality",
                "phase": "elaboration",
                "step": step,
                "iteration": iteration,
                "gate": gate_status,
                "verdict": verdict,
                "critical": critical,
                "coverage": summary["coverage"],
                "duplication": summary["duplication"],
                "ok": summary["ok"],
            },
        )

    if args.json:
        print(json.dumps({**summary, "findings": survivors}, indent=2, ensure_ascii=False))
    else:
        print(render_reading(summary))

    return 1 if (policy_failure or strict_failure) else 0


def write_baseline(path: Path, summary: dict) -> None:
    payload = {
        "iteration": summary["iteration"],
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "project": summary["project"],
        "version": summary["version"],
        "scope": summary["scope"],
        "mode": summary["mode"],
        "gate": summary["gate"],
        "coverage": summary["coverage"],
        "duplication": summary["duplication"],
        "issues": summary["issues"],
        "critical": summary["critical"],
        "verdict": summary["verdict"],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def render_triage(summary: dict, survivors: list[dict]) -> str:
    coverage = f"{summary['coverage']}%" if summary["coverage"] is not None else "-"
    duplication = f"{summary['duplication']}%" if summary["duplication"] is not None else "-"
    lines = [
        "## Code Quality",
        "",
        "| Gate | Coverage | Duplication | Issues | Critical | Verdict |",
        "| :--- | ---: | ---: | ---: | ---: | :--- |",
        f"| {summary['gate']} | {coverage} | {duplication} | {summary['issues']} | {summary['critical']} | {summary['verdict']} |",
        "",
        "| Issue | Type | Severity | File | Line | Triaged as | Confirmed | Measure | Owner |",
        "| :--- | :--- | :--- | :--- | ---: | :--- | :--- | :--- | :--- |",
    ]
    for item in survivors:
        lines.append(
            f"| `{item['rule']}` | {item['type']} | {item['severity']} | `{item['component']}` | {item['line']} | "
            f"{item['triaged_as']} | {'yes' if item['confirmed'] else 'no'} | {item['measure']} | {item['owner']} |"
        )
    if not survivors:
        lines.append("| - | - | - | - | - | - | - | - | - |")
    lines.append("")
    return "\n".join(lines)


def render_reading(summary: dict) -> str:
    coverage = f"{summary['coverage']}%" if summary["coverage"] is not None else "-"
    duplication = f"{summary['duplication']}%" if summary["duplication"] is not None else "-"
    trend = f"{summary['coverage_delta']:+.1f}" if summary["coverage_delta"] is not None else "first baseline"
    lines = [
        f"Quality gate: {summary['gate']} | mode: {summary['mode']} | scope: {summary['scope']} | "
        f"coverage {coverage} | duplication {duplication}",
        f"Verdict: {summary['verdict']} ({', '.join(summary['flags'])}) | policy: {summary['policy']} | trend: {trend}",
        f"Issues: {summary['issues']} | critical: {summary['critical']} | allowlisted: {summary['allowlisted']} | "
        f"architecture: {summary['architecture_violations']} | critical CVEs: {summary['critical_cves']}",
    ]
    if summary["unclassified"]:
        lines.append(f"Unclassified findings: {summary['unclassified']} (blocks triage)")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
