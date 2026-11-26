#!/usr/bin/env python3
"""Migrate the monolithic state.yaml memory into a three-level layout.

Before: state.yaml carries a huge top-level `notes` scalar plus one `notes`
scalar per artifact (166 KB in the reference domain).

After:
  state.yaml                       working memory: position + short summary
  journal/{iteration}/notes/*.json episodic memory: one record per block
  journal/{iteration}/artifacts/*  episodic memory: one record per artifact

The migration is text-preserving: every line except the migrated `notes`
scalars is kept byte-identical, and a structural fingerprint is compared
before and after. Artifact ids, statuses and step tracking are not touched.

Modes:
  --analyze   report only, write nothing
  --dry-run   write the proposed result under --out
  --apply     backup state.yaml and write in place

Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "openspec" / "artifacts"

MARKER = re.compile(
    r"E(\d{1,2})\s+(PASO\s+\d+[A-D]?|TEST|on-demand|PHASE|CYCLE)\b", re.IGNORECASE
)
STEP_IN_ENTRY = re.compile(r"PASO\s+(\d+[A-D]?)", re.IGNORECASE)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
DISCIPLINE_RE = re.compile(r"^  (\S.*?):\s*(\[\])?\s*$")
ARTIFACT_ID_RE = re.compile(r"^    - id:\s*(.+?)\s*$")
ARTIFACT_KEY_RE = re.compile(r"^      ([A-Za-z_]+):\s*(.*)$")
TOP_KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")


# ---------------------------------------------------------------- YAML scalars


def parse_scalar(value: str) -> str:
    """Decode a single-line YAML scalar (double, single or plain).

    Some notes written by earlier agents contain unescaped inner quotes, so a
    double-quoted scalar is taken as everything between the first and the last
    quote on the line instead of stopping at the first closing quote.
    """
    text = value.strip()
    escapes = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}

    def decode(body: str) -> str:
        out: list[str] = []
        i = 0
        while i < len(body):
            char = body[i]
            if char == "\\" and i + 1 < len(body):
                nxt = body[i + 1]
                out.append(escapes.get(nxt, "\\" + nxt))
                i += 2
                continue
            out.append(char)
            i += 1
        return "".join(out)

    if text.startswith('"'):
        # Tolerate unterminated double-quoted scalars produced by earlier agents.
        body = text[1:-1] if text.endswith('"') and len(text) >= 2 else text[1:]
        return decode(body)
    if text.startswith("'"):
        body = text[1:-1] if text.endswith("'") and len(text) >= 2 else text[1:]
        return body.replace("''", "'")
    return text


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


# ------------------------------------------------------------------- reading


def read_state(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    bom = text.startswith("\ufeff")
    if bom:
        text = text[1:]
    newline = "\r\n" if "\r\n" in text[:4000] else "\n"
    return {
        "path": path,
        "text": text,
        "lines": text.splitlines(),
        "newline": newline,
        "bom": bom,
        "bytes": len(raw),
    }


def find_top_notes(lines: list[str]) -> tuple[int | None, str | None]:
    for index, line in enumerate(lines):
        match = re.match(r"^notes:\s*(.*)$", line)
        if match:
            value = match.group(1).strip()
            if value in ("|", ">", "|-", ">-"):
                raise SystemExit("block-scalar notes are not supported by this migration")
            return index, parse_scalar(value)
    return None, None


def parse_artifacts(lines: list[str]) -> list[dict]:
    artifacts: list[dict] = []
    in_artifacts = False
    discipline: str | None = None
    current: dict | None = None

    for index, line in enumerate(lines):
        if re.match(r"^artifacts:\s*$", line):
            in_artifacts = True
            continue
        if not in_artifacts:
            continue
        if line and not line.startswith(" "):
            break

        discipline_match = DISCIPLINE_RE.match(line)
        if discipline_match:
            discipline = discipline_match.group(1).strip()
            current = None
            continue

        id_match = ARTIFACT_ID_RE.match(line)
        if id_match:
            current = {
                "discipline": discipline,
                "id": parse_scalar(id_match.group(1)),
                "keys": {},
                "notes_index": None,
                "notes_raw": None,
            }
            artifacts.append(current)
            continue

        if current is None:
            continue

        key_match = ARTIFACT_KEY_RE.match(line)
        if key_match:
            key = key_match.group(1)
            raw_value = key_match.group(2).strip()
            current["keys"][key] = raw_value
            if key == "notes":
                current["notes_index"] = index
                current["notes_raw"] = parse_scalar(raw_value)

    return artifacts


# ----------------------------------------------------------------- migration


def split_notes(text: str) -> list[dict]:
    """Split the top-level notes into blocks at credible entry markers."""
    boundaries: list[int] = [0]
    for match in MARKER.finditer(text):
        start = match.start()
        if start == 0:
            continue
        probe = start - 1
        while probe >= 0 and text[probe] in " \t":
            probe -= 1
        if probe < 0 or text[probe] in ".;)]":
            boundaries.append(start)

    boundaries = sorted(set(boundaries))
    blocks: list[dict] = []
    for order, start in enumerate(boundaries):
        end = boundaries[order + 1] if order + 1 < len(boundaries) else len(text)
        raw = text[start:end]
        if not raw.strip():
            continue
        head = MARKER.search(raw)
        step = None
        if head:
            token = head.group(2).upper()
            step_match = STEP_IN_ENTRY.search(token)
            step = step_match.group(1) if step_match else token.lower()
        date_match = DATE_RE.search(raw)
        iteration_match = re.match(r"E(\d{1,2})", raw.lstrip())
        blocks.append(
            {
                "order": order,
                "raw": raw,
                "step": step,
                "date": date_match.group(1) if date_match else None,
                "iteration": f"E{iteration_match.group(1)}" if iteration_match else None,
            }
        )
    return blocks


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def fingerprint(lines: list[str]) -> str:
    kept: list[str] = []
    for line in lines:
        if re.match(r"^\s*notes(_ref)?\s*:", line):
            continue
        if re.match(r"^(summary|journal)\s*:", line):
            continue
        kept.append(line.rstrip())
    return hashlib.sha256("\n".join(kept).encode("utf-8")).hexdigest()


def artifact_signature(artifacts: list[dict]) -> list[str]:
    return sorted(f"{item['discipline']}|{item['id']}" for item in artifacts)


def read_state_fields(lines: list[str]) -> dict:
    fields: dict[str, str] = {}
    for line in lines:
        match = TOP_KEY_RE.match(line)
        if match and match.group(1) in {
            "phase",
            "iteration",
            "domain",
            "status",
            "date",
            "current_step",
            "last_approved_step",
            "approved_steps",
            "pending_steps",
            "scope",
        }:
            fields[match.group(1)] = match.group(2).split("#", 1)[0].strip()
    return fields


def build_summary(fields: dict) -> str:
    iteration = fields.get("iteration", "?").strip('"')
    phase = fields.get("phase", "?")
    current = fields.get("current_step", "?")
    last = fields.get("last_approved_step", "?")
    pending = fields.get("pending_steps", "[]").strip("[]").replace(" ", "")
    return (
        f"{iteration} {phase} in progress | current_step={current} | "
        f"last_approved={last} | pending={pending} | history: journal/{iteration}/"
    )


def unique_path(directory: Path, stem: str, used: set[str]) -> Path:
    """Deterministic name within a single run (idempotent across runs)."""
    candidate = f"{stem}.json"
    counter = 2
    while candidate in used:
        candidate = f"{stem}-{counter}.json"
        counter += 1
    used.add(candidate)
    return directory / candidate


def migrate(state: dict, domain_dir: Path, phase: str, iteration: str, domain: str) -> dict:
    lines = list(state["lines"])
    notes_index, notes_text = find_top_notes(lines)
    artifacts = parse_artifacts(lines)

    journal_root = domain_dir / "journal" / iteration
    notes_dir = journal_root / "notes"
    artifacts_dir = journal_root / "artifacts"

    written: list[dict] = []
    used_notes: set[str] = set()
    used_artifacts: set[str] = set()

    # --- top-level notes -> one record per block, chronological order
    blocks = split_notes(notes_text) if notes_text else []
    for sequence, block in enumerate(reversed(blocks), start=1):
        stem = f"{sequence:03d}-{slugify(block['step'] or 'note')}-{block['date'] or 'nodate'}"
        path = unique_path(notes_dir, stem, used_notes)
        payload = {
            "type": "step-note",
            "domain": domain,
            "phase": phase,
            "iteration": block["iteration"] or iteration,
            "step": block["step"],
            "date": block["date"],
            "order_newest_first": block["order"],
            "source": "state.yaml:notes",
            "chars": len(block["raw"]),
            "raw": block["raw"],
        }
        write_json(path, payload)
        written.append(
            {
                "file": path.relative_to(journal_root).as_posix(),
                "type": "step-note",
                "step": block["step"],
                "date": block["date"],
                "chars": len(block["raw"]),
            }
        )

    # --- artifact notes -> one record per artifact
    artifact_records: list[dict] = []
    replacements: dict[int, str] = {}
    for artifact in artifacts:
        if artifact["notes_index"] is None:
            continue
        stem = slugify(artifact["id"])
        path = unique_path(artifacts_dir, stem, used_artifacts)
        payload = {
            "type": "artifact-note",
            "domain": domain,
            "phase": phase,
            "iteration": iteration,
            "artifact_id": artifact["id"],
            "discipline": artifact["discipline"],
            "source": "state.yaml:artifacts[].notes",
            "chars": len(artifact["notes_raw"]),
            "raw": artifact["notes_raw"],
        }
        write_json(path, payload)
        reference = f"journal/{iteration}/artifacts/{path.name}"
        replacements[artifact["notes_index"]] = reference
        artifact_records.append(
            {
                "file": path.relative_to(journal_root).as_posix(),
                "type": "artifact-note",
                "artifact_id": artifact["id"],
                "chars": len(artifact["notes_raw"]),
            }
        )
        written.append(artifact_records[-1])

    # --- rewrite state.yaml
    new_lines = list(lines)
    for index, reference in replacements.items():
        original = new_lines[index]
        indent = original[: len(original) - len(original.lstrip())]
        new_lines[index] = f"{indent}notes_ref: {reference}"

    if notes_index is not None:
        summary = build_summary(read_state_fields(lines))
        new_lines[notes_index] = f"summary: {yaml_quote(summary)}"
        new_lines.insert(notes_index + 1, f"journal: journal/{iteration}")

    # --- journal index
    if written:
        write_json(
            journal_root / "index.json",
            {
                "domain": domain,
                "phase": phase,
                "iteration": iteration,
                "entries": sorted(written, key=lambda item: item["file"]),
            },
        )

    return {
        "lines": new_lines,
        "notes_index": notes_index,
        "notes_chars": len(notes_text) if notes_text else 0,
        "notes_blocks": len(blocks),
        "artifact_notes": len(artifact_records),
        "artifact_notes_chars": sum(item["chars"] for item in artifact_records),
        "journal_files": len(written) + (1 if written else 0),
        "fidelity_ok": sum(len(block["raw"]) for block in blocks)
        == (len(notes_text) if notes_text else 0),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate state.yaml memory into journal records.")
    parser.add_argument("--domain", help="domain under openspec/artifacts/ (default: single state)")
    parser.add_argument("--state", type=Path, help="explicit state.yaml path")
    parser.add_argument("--out", type=Path, help="output directory for --dry-run")
    parser.add_argument("--analyze", action="store_true", help="report only")
    parser.add_argument("--dry-run", action="store_true", help="write proposal under --out")
    parser.add_argument("--apply", action="store_true", help="backup and write in place")
    parser.add_argument("--force", action="store_true", help="allow --apply over an existing journal")
    args = parser.parse_args(argv)

    if not (args.analyze or args.dry_run or args.apply):
        args.analyze = True

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

    domain_dir = state_path.parent
    state = read_state(state_path)
    fields = read_state_fields(state["lines"])
    phase = fields.get("phase", "unknown").strip('"')
    iteration = fields.get("iteration", "unknown").strip('"')
    domain = fields.get("domain", domain_dir.name).strip('"')

    before_fingerprint = fingerprint(state["lines"])
    before_signature = artifact_signature(parse_artifacts(state["lines"]))

    # Analyze without writing: run the migration into a throwaway directory.
    staging_root = Path(args.out) if args.out else (
        REPO_ROOT / ".atl" / "staging" / "state-migration"
    )

    if args.analyze:
        scratch = REPO_ROOT / ".atl" / "staging" / "_analyze"
        shutil.rmtree(scratch, ignore_errors=True)
        result = migrate(state, scratch, phase, iteration, domain)
        report = {
            "mode": "analyze",
            "state": str(state_path),
            "before_bytes": state["bytes"],
            "after_bytes": len(state["newline"].join(result["lines"]).encode("utf-8")),
            "notes_chars": result["notes_chars"],
            "notes_blocks": result["notes_blocks"],
            "artifact_notes": result["artifact_notes"],
            "artifact_notes_chars": result["artifact_notes_chars"],
            "journal_files": result["journal_files"],
            "journal_chars": result["notes_chars"] + result["artifact_notes_chars"],
            "fidelity_ok": result["fidelity_ok"],
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    journal_root = domain_dir / "journal" / iteration
    if args.apply and journal_root.exists() and any(journal_root.iterdir()) and not args.force:
        print(
            json.dumps(
                {
                    "ok": False,
                    "errors": [f"journal already exists: {journal_root}; use --force to overwrite"],
                },
                indent=2,
            )
        )
        return 1

    out_root = staging_root if args.dry_run else domain_dir
    payload = migrate(state, out_root, phase, iteration, domain)

    after_fingerprint = fingerprint(payload["lines"])
    after_signature = artifact_signature(parse_artifacts(payload["lines"]))
    new_text = state["newline"].join(payload["lines"]) + state["newline"]
    if state["bom"]:
        new_text = "\ufeff" + new_text

    report = {
        "mode": "dry-run" if args.dry_run else "apply",
        "state": str(state_path),
        "out": str(out_root),
        "before_bytes": state["bytes"],
        "after_bytes": len(new_text.encode("utf-8")),
        "notes_chars": payload["notes_chars"],
        "notes_blocks": payload["notes_blocks"],
        "artifact_notes": payload["artifact_notes"],
        "artifact_notes_chars": payload["artifact_notes_chars"],
        "journal_files": payload["journal_files"],
        "fidelity_ok": payload["fidelity_ok"],
        "structural_fingerprint_match": before_fingerprint == after_fingerprint,
        "artifact_ids_match": before_signature == after_signature,
    }

    if not report["structural_fingerprint_match"] or not report["artifact_ids_match"]:
        print(json.dumps({**report, "ok": False, "errors": ["equivalence check failed"]}, indent=2))
        return 1

    if args.dry_run:
        staging_root.mkdir(parents=True, exist_ok=True)
        (staging_root / "state.yaml").write_text(new_text, encoding="utf-8", newline="")
        report["ok"] = True
        report["written"] = str(staging_root / "state.yaml")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    backup = state_path.with_suffix(".yaml.bak")
    if backup.exists():
        backup = state_path.with_name(f"state.yaml.bak.{datetime.now():%Y%m%d%H%M%S}")
    backup.write_bytes(state_path.read_bytes())
    state_path.write_text(new_text, encoding="utf-8", newline="")

    report["ok"] = True
    report["backup"] = str(backup)
    report["written"] = str(state_path)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
