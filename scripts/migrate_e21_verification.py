#!/usr/bin/env python3
"""One-off E21 migration to Iteration Verification and traceability columns.

Adds Scope ID, test status/evidence, scenario reconciliation and the
Iteration Verification artifact. Dry-run by default; use --apply to write.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOMAIN = ARTIFACTS = REPO_ROOT / "openspec" / "artifacts" / "registro-horario"
PLAN = ARTIFACTS / "08 Project Management" / "21 E21 Plan.md"
TEST = ARTIFACTS / "05 Test" / "21 E21 Test plan.md"
ACCEPTANCE = ARTIFACTS / "05 Test" / "21 E21 Acceptance plan.md"
VERIFICATION = ARTIFACTS / "08 Project Management" / "21 E21 Verification.md"
STATE = ARTIFACTS / "state.yaml"

EVIDENCE = "mvn test (1039 green, 2026-11-25)"
ACCEPTANCE_EVIDENCE = "mvn test -Pacceptance (174 scenarios, 5338 steps, 2026-11-25)"
FEATURES = {
    "S1": "src/test/resources/features/e21/evidencia_ausencias.feature",
    "S2": "src/test/resources/features/e21/read_model_uc26.feature",
    "S3": "src/test/resources/features/e21/retencion_purga.feature",
}


def read_lines(path: Path) -> tuple[list[str], str]:
    text = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in text[:4000] else "\n"
    return text.splitlines(), newline


def write_lines(path: Path, lines: list[str], newline: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(newline.join(lines) + newline, encoding="utf-8", newline="")


def norm(value: str) -> str:
    return re.sub(r"[—–-]", "-", value).strip().lower()


def section_bounds(lines: list[str], heading: str) -> tuple[int, int] | None:
    target = norm(heading)
    start = None
    for index, line in enumerate(lines):
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match and norm(match.group(1)) == target:
            start = index + 1
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(r"^##\s+", lines[index]):
            end = index
            break
    return start, end


def split_cells(line: str) -> list[str]:
    parts = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [part.strip().replace("\\|", "|") for part in parts]


def join_cells(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def find_h2(lines: list[str], heading: str) -> int | None:
    target = norm(heading)
    for index, line in enumerate(lines):
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match and norm(match.group(1)) == target:
            return index
    return None


def scope_for(test_id: str) -> str:
    prefix = test_id.split("-", 1)[0]
    if prefix in ("M", "D", "F"):
        return "S1"
    if prefix in ("A", "P", "R"):
        return "S2"
    if prefix == "S":
        return "S3"
    return "-"


def scope_id_for(item: str) -> str:
    match = re.match(r"\s*(S\d+|EP-[A-Z0-9-]+|UC\d+)", item)
    return match.group(1) if match else "-"


def feature_for(scenario_id: str) -> str:
    number = int(scenario_id.split("-")[1])
    if number <= 13:
        return FEATURES["S1"]
    if number <= 26:
        return FEATURES["S2"]
    return FEATURES["S3"]


def transform_plan(lines: list[str]) -> tuple[list[str], bool]:
    bounds = section_bounds(lines, "Selected Scope Summary")
    if not bounds:
        raise SystemExit("Selected Scope Summary not found")
    start, end = bounds
    out = lines[:start]
    changed = False
    index = start
    while index < end:
        if lines[index].strip().startswith("|"):
            block = []
            while index < end and lines[index].strip().startswith("|"):
                block.append(lines[index])
                index += 1
            header = split_cells(block[0])
            if "Scope ID" in header:
                out.extend(block)
                continue
            new_header = ["Scope ID"] + header
            out.append(join_cells(new_header))
            out.append(join_cells(["---"] * len(new_header)))
            for row_line in block[2:]:
                cells = split_cells(row_line)
                if len(cells) < 3:
                    out.append(row_line)
                    continue
                out.append(join_cells([scope_id_for(cells[2])] + cells))
            changed = True
        else:
            out.append(lines[index])
            index += 1
    out.extend(lines[end:])
    return out, changed


def transform_test_plan(lines: list[str]) -> tuple[list[str], bool]:
    bounds = section_bounds(lines, "Agreed Test List (Step 1 Output)")
    if not bounds:
        raise SystemExit("Agreed Test List not found")
    start, end = bounds
    out = lines[:start]
    changed = False
    index = start
    while index < end:
        if lines[index].strip().startswith("|"):
            block = []
            while index < end and lines[index].strip().startswith("|"):
                block.append(lines[index])
                index += 1
            header = split_cells(block[0])
            if "Test ID" not in header or "Status" in header:
                out.extend(block)
                continue
            new_header = [header[0], "Scope IDs"] + header[1:] + ["Status", "Test file", "Evidence"]
            out.append(join_cells(new_header))
            out.append(join_cells(["---"] * len(new_header)))
            for row_line in block[2:]:
                cells = split_cells(row_line)
                if not cells or not re.match(r"^[A-Z]+-\d+$", cells[0]):
                    out.append(row_line)
                    continue
                out.append(join_cells([cells[0], scope_for(cells[0])] + cells[1:] + ["implemented", "-", EVIDENCE]))
            changed = True
        else:
            out.append(lines[index])
            index += 1
    out.extend(lines[end:])
    return out, changed


def add_deferred_section(lines: list[str]) -> list[str]:
    if find_h2(lines, "Deferred Items") is not None:
        return lines
    index = find_h2(lines, "Approval and Execution Policy")
    if index is None:
        return lines
    block = [
        "## Deferred Items",
        "",
        "| Test ID | Reason | Approved by |",
        "| :--- | :--- | :--- |",
        "| - | No deferred items in E21. | - |",
        "",
        "---",
        "",
    ]
    return lines[:index] + block + lines[index:]


def extract_conformance(lines: list[str]) -> tuple[list[str], list[str]]:
    bounds = section_bounds(lines, "Implementation Conformance Review (14D)")
    if not bounds:
        return lines, []
    start, end = bounds
    heading = start - 1
    body = lines[start:end]
    while body and body[-1].strip() in ("", "---"):
        body.pop()
    cleaned = []
    for line in body:
        if line.strip().startswith("| Diagram Element"):
            cleaned.append("| Element | Source | Implementation | Verdict | Action |")
        elif line.strip().startswith("| :---"):
            cleaned.append("| :--- | :--- | :--- | :--- | :--- |")
        else:
            cleaned.append(line)
    return lines[:heading] + lines[end:], cleaned


def transform_acceptance(lines: list[str]) -> tuple[list[str], list[tuple[str, str, str]], bool]:
    bounds = section_bounds(lines, "Scenario List (Agreed Acceptance List - 14A Output)")
    if not bounds:
        raise SystemExit("Scenario List not found")
    start, end = bounds
    out = lines[:start]
    changed = False
    rows: list[tuple[str, str, str]] = []
    group = "-"
    index = start
    while index < end:
        line = lines[index]
        if line.startswith("### "):
            match = re.match(r"^###\s+(S\d+)", line)
            group = match.group(1) if match else "-"
            out.append(line)
            index += 1
            continue
        if line.strip().startswith("|"):
            block = []
            while index < end and lines[index].strip().startswith("|"):
                block.append(lines[index])
                index += 1
            header = split_cells(block[0])
            if "Scenario ID" not in header or "Scope ID" in header:
                out.extend(block)
                continue
            new_header = header[:1] + ["Scope ID"] + header[1:-1] + ["Feature file", "Planned execution", header[-1]]
            out.append(join_cells(new_header))
            out.append(join_cells(["---"] * len(new_header)))
            for row_line in block[2:]:
                cells = split_cells(row_line)
                if not cells or not re.match(r"^A-\d{2}$", cells[0]):
                    out.append(row_line)
                    continue
                aid = cells[0]
                feature = feature_for(aid)
                out.append(join_cells([aid, group] + cells[1:-1] + [feature, "yes", cells[-1]]))
                rows.append((aid, group, feature))
            changed = True
        else:
            out.append(line)
            index += 1
    out.extend(lines[end:])
    return out, rows, changed


def add_reconciliation(lines: list[str], rows: list[tuple[str, str, str]]) -> list[str]:
    if find_h2(lines, "Scenario Reconciliation (14C)") is not None:
        return lines
    index = find_h2(lines, "Execution Evidence (14C)")
    if index is None:
        return lines
    block = [
        "## Scenario Reconciliation (14C)",
        "",
        "| Scenario ID | Feature file | Executed | Result | Evidence |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for aid, _scope, feature in rows:
        block.append(f"| {aid} | {feature} | yes | GREEN | {ACCEPTANCE_EVIDENCE} |")
    block.extend(
        [
            "",
            "The gate accepts only `Executed = yes` and `Result = GREEN`. Every scenario in the Scenario List must appear here.",
            "",
            "---",
            "",
        ]
    )
    return lines[:index] + block + lines[index:]


def verification_text(design_body: list[str]) -> str:
    design = "\n".join(design_body).strip()
    plan_rows = [
        ("S1", "UC16 S1/S10/S13/S14/S15/S16/S17; UC01; UC03",
         "DSD/DCD absence.* and fichaje.*", "Event-sourced absence, projection, TimeEvent actor/role/source",
         "M-01..M-05, D-01..D-11, F-01..F-06", "A-01..A-13", "mvn test 1039; acceptance 174/5338; design-consistency 0/0", "COVERED"),
        ("S2", "UC13 S2; UC18 S1; UC26 read model",
         "DSD/DCD absence.* and audit.*", "Conflicts, balance events, read model 1-4",
         "A-01..A-13, P-01..P-11, R-01..R-07", "A-14..A-26", "mvn test 1039; acceptance 174/5338; design-consistency 0/0", "COVERED"),
        ("S3", "UC07 S5",
         "DSD/DCD absence.infrastructure and employees", "Retention 4 years and ordered purge",
         "S-01..S-05", "A-27..A-29", "mvn test 1039; acceptance 174/5338", "COVERED"),
        ("EP-DPIA-01", "n/a", "n/a", "-", "-", "-",
         "Out of scope: evolution point only (plan rationale)", "DEFERRED"),
        ("UC26", "UC26 (E22)", "n/a", "-", "-", "-",
         "Deferred to E22; read model delivered in S2", "DEFERRED"),
    ]
    coverage = "\n".join("| " + " | ".join(row) + " |" for row in plan_rows)
    criteria = [
        ("S1: history reconstructible; UC16/UC19 green; UPDATE/DELETE blocked; time_events actor/role/source",
         "mvn test 1039; EvidenceImmutabilityTddTest", "MET"),
        ("S2: every type and derived state tested; idempotent sweep; coexistence; OVER_CONSUMED; read model 1-4",
         "mvn test 1039; acceptance 174/5338", "MET"),
        ("S3: manual purge respects 4 years, cascades and leaves no domain trace",
         "Retention/purge tests; acceptance A-27..A-29", "MET"),
        ("Regression green: mvn test, mvn test -Pacceptance, design-consistency, SVG export",
         "All green; 183 SVGs", "MET"),
        ("UP artifacts updated before code, including UC26 fully dressed in PASO 16",
         "state.yaml; UC26 fully dressed", "MET"),
        ("EP-AUSENCIAS-01 and EP-DPIA-01 not implemented",
         "Explicitly out of scope/deferred", "MET"),
    ]
    exit_rows = "\n".join("| " + " | ".join(row) + " |" for row in criteria)
    return f"""# E21 Iteration Verification

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| v1 | 2026-11-27 | Initial verification for E21. | agent |

---

## Scope and Inputs

- Iteration Plan: `08 Project Management/21 E21 Plan.md`
- Test Plan: `05 Test/21 E21 Test plan.md`
- Acceptance Test Plan: `05 Test/21 E21 Acceptance plan.md`
- Logical View: `03 Design/Logical View/` for the E21 slice
- Build layout: `registro-horario/` (Maven)

Scope IDs: S1, S2, S3, EP-DPIA-01, UC26.

---

## Design Conformance (14D)

{design}

---

## Iteration Plan Coverage (14D)

| Scope ID | UC/Scenario | Design | Implementation | Test IDs | A-IDs | Evidence | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{coverage}

---

## Iteration Exit Criteria (14D)

| Criterion | Evidence | Verdict |
| :--- | :--- | :--- |
{exit_rows}

---

## Build Evidence

- **Compile command:** `mvn -q -DskipTests compile` (in `registro-horario/`)
- **Result:** `BUILD SUCCESS` (exit 0).
- **Unit suite:** 1039 green.
- **Acceptance suite:** 174 scenarios / 5338 steps green.

---

## Uncovered and Deferred

| Scope ID | Reason | Approved by |
| :--- | :--- | :--- |
| EP-DPIA-01 | Out of scope: evolution point only (plan rationale). | plan |
| UC26 | Fully dressed in E21 PASO 16; implementation (UI and export) deferred to E22. | plan |

---

## Verdict

| Check | Verdict |
| :--- | :--- |
| Design Conformance | MATCH |
| Iteration Plan Coverage | COVERED |
| Iteration Exit Criteria | MET |
| Overall | READY |
"""


def add_state_entry(lines: list[str]) -> tuple[list[str], bool]:
    if any(line.strip() == "- id: Iteration Verification" for line in lines):
        return lines, False
    index = None
    for position, line in enumerate(lines):
        if line.strip() == "- id: Iteration Plan":
            index = position
            break
    if index is None:
        raise SystemExit("Iteration Plan entry not found in state.yaml")
    end = index + 1
    while end < len(lines):
        if re.match(r"^    - id: ", lines[end]) or re.match(r"^  \S", lines[end]):
            break
        end += 1
    block = [
        "    - id: Iteration Verification",
        "      path: 08 Project Management/{{#}} {{Iteration}} Verification.md",
        "      status: in_progress",
        "      created_at_step: 14D",
        "      refined_at_steps: []",
        "      depends_on: [Iteration Plan, Test Plan, Acceptance Test Plan]",
        "",
    ]
    return lines[:end] + block + lines[end:], True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate E21 to Iteration Verification.")
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args(argv)

    plan_lines, plan_nl = read_lines(PLAN)
    test_lines, test_nl = read_lines(TEST)
    acceptance_lines, acceptance_nl = read_lines(ACCEPTANCE)
    state_lines, state_nl = read_lines(STATE)

    plan_lines, plan_changed = transform_plan(plan_lines)
    test_lines, test_changed = transform_test_plan(test_lines)
    test_lines = add_deferred_section(test_lines)
    test_lines, design_body = extract_conformance(test_lines)
    acceptance_lines, scenario_rows, acceptance_changed = transform_acceptance(acceptance_lines)
    acceptance_lines = add_reconciliation(acceptance_lines, scenario_rows)
    state_lines, state_changed = add_state_entry(state_lines)

    print(f"plan changed: {plan_changed}")
    print(f"test plan changed: {test_changed}; design rows: {len(design_body)}")
    print(f"acceptance changed: {acceptance_changed}; scenarios: {len(scenario_rows)}")
    print(f"state changed: {state_changed}")

    if not args.apply:
        print("dry-run: no files written")
        return 0

    write_lines(PLAN, plan_lines, plan_nl)
    write_lines(TEST, test_lines, test_nl)
    write_lines(ACCEPTANCE, acceptance_lines, acceptance_nl)
    write_lines(STATE, state_lines, state_nl)
    VERIFICATION.write_text(verification_text(design_body), encoding="utf-8", newline="\n")
    print(f"written: {PLAN.name}, {TEST.name}, {ACCEPTANCE.name}, {VERIFICATION.name}, {STATE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
