---
name: elaboration-history
description: >
  Generates and maintains the Elaboration iterations history for the Unified
  Process. Produces a confidence-scored Markdown report and a machine-readable
  ledger with iteration dates, effective working days, use cases, git evidence,
  and a reliable average of effective days per use case. Triggers: elaboration
  history, iteration history, dias efectivos, cerrar iteracion, historical
  metrics, media por caso de uso.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

# Purpose

You are responsible for closing the documentary history of one Elaboration
iteration and maintaining the project-level history of all iterations.

You produce two artifacts:

1. `Elaboration Iterations Ledger` - JSON source of truth.
2. `Elaboration Iterations History` - Markdown report generated from the ledger.

The Markdown report MUST be generated from the ledger. Do not edit generated
tables manually; fix the ledger and regenerate.

# Required Inputs

- `openspec/artifacts/{domain}/state.yaml`.
- The approved `Iteration Plan` for the iteration being closed.
- `Requirements Ranking` and `Use Case Model`.
- The existing `Elaboration Iterations Ledger`, if it exists.
- The existing `Elaboration Iterations History`, if it exists.
- Git repository metadata.
- Project timezone from the ledger; default `Europe/Madrid`.
- Explicit user confirmation for any UC classification that is not obvious.
- `get-calibration-baseline.ps1` for PASO 1 planning calibration.

# Artifact Paths

Resolve paths through the active schema and the storage skill. The default
schema uses:

- `08 Project Management/Elaboration Iterations Ledger.json`
- `08 Project Management/Elaboration Iterations History.md`

# Reliability Contract

The history is only as reliable as its source data. Apply these rules:

- Capture `start_ref` when the iteration starts, after `OK PASO 1`.
- Capture `end_ref` when the iteration closes, before the history report.
- Compute commits with `git log <start_ref>..<end_ref>`; never use `git log --all`.
- Use author dates, not committer dates.
- Record both author and committer dates so timezone or rebase anomalies are visible.
- Record the commit hashes and commit days; never store only an inferred total.
- Do not infer use cases from commit messages.
- Classify each in-scope item as `full`, `slice`, `refactor`, `support`, or `retired`.
- Mark `counts_for_average` explicitly for each UC.
- Record `working_tree_clean_at_close`; do not silently count uncommitted work.
- If `start_ref` is not an ancestor of `end_ref`, mark the record `medium` and exclude it from the average.
- If the repository is unavailable, keep the record with `reliability: low` and no git metrics.
- Never rewrite historical records without an explicit migration note.

Reliability levels:

| Level | Criteria | Include in average |
| :--- | :--- | :--- |
| `high` | Closed iteration, valid refs and ancestry, clean tree, explicit scope, at least one commit day | Yes |
| `medium` | Closed but refs fall back to dates, dirty tree, ambiguous boundary, or mixed unclassified scope | No |
| `low` | Missing dates, missing scope, no git history, or retrospective reconstruction | No |
| `open` | Iteration not closed | No |

Average rule:

`average = sum(effective_days of high records) / sum(counts_for_average UCs of high records)`

Only UCs with `delivery_type` equal to `full` or `slice` may count. Refactors,
support work, and retired use cases never count.

# Workflow

## Phase 0 - Planning calibration

Run during PASO 1, before drafting the Iteration Plan. This phase is read-only.

1. Read the ledger and the existing history document.
2. Run `get-calibration-baseline.ps1` against the ledger.
3. Use only `high` iterations and UCs with `delivery_type` `full` or `slice`.
4. Treat the median days per UC as the primary reference, the weighted average as
   a secondary reference, and the min-max range as the uncertainty band.
5. Report the sample size and confidence. With three iterations and five UCs,
   confidence is `medium`; do not present the result as a precise prediction.
6. Do not apply the baseline to refactors, support work, retired UCs, or open
   iterations.
7. If there is no valid sample, report `no historical baseline` and continue with
   normal task-based estimation.
8. Require an explicit justification when the task-based estimate falls outside
   30% of the historical range.

## Phase A - Open the iteration record

Run after `OK PASO 1` and after the Iteration Plan is approved.

1. Read the ledger if it exists.
2. Add a record with `status: in_progress`.
3. Record:
   - `iteration`
   - `planned_start` and `planned_end` from the Iteration Plan
   - `start_ref` = current `HEAD`
   - `branch` = current branch
   - `scope[]` with the selected UCs and their provisional `delivery_type`
   - `counts_for_average` defaults: `true` for `full` and `slice`, `false` otherwise
   - `calibration` snapshot used for the Iteration Plan: source cutoff, sample
     iterations and UCs, median, weighted average, range, applied UCs,
     adjustment, and confidence
5. Capture the current git state. Do not require a clean tree at iteration start.
6. Persist the ledger with the storage skill.

Do not add a new approval gate for this phase; it is part of PASO 1 persistence.

## Phase B - Close the iteration record

Run after `OK PASO 17`.

1. Read `state.yaml`, the Iteration Plan, the ledger, and the existing history.
2. Verify that the iteration is closed and that the user approved PASO 17.
3. Resolve `end_ref` = current `HEAD`.
4. Validate that `start_ref` exists and is an ancestor of `end_ref`.
5. Run `collect-iteration-git.ps1` or the equivalent git commands.
6. Confirm the scope classification with the user when the plan mixes UCs,
   refactors, support work, or deferred items.
7. Set `status: closed`, `actual_start`, `actual_end`, `commit_count`,
   `effective_days`, `commit_days`, `working_tree_clean_at_close`, and `reliability`.
8. Set `include_in_average` from the reliability gate and UC classification.
9. Add `excluded_reason` when the record does not count.
10. Recompute the average from the ledger.
11. Render the Markdown report with `render-iteration-history.ps1`.
12. Present the generated report in chat.
13. Stop and request `OK PASO 18`.
14. After approval, persist both artifacts with the storage skill and update
    artifact statuses in `state.yaml`.

If the working tree is dirty, do not commit automatically. Record the condition,
mark the record `medium`, and ask the user whether the pending files belong to
the iteration.

# Required Git Commands

Use these commands as the minimum evidence set:

```powershell
git rev-parse --verify "<start-ref>^{commit}"
git rev-parse --verify "<end-ref>^{commit}"
git merge-base --is-ancestor "<start-ref>" "<end-ref>"
git log --format="%H%x09%aI%x09%cI" "<start-ref>..<end-ref>"
git status --porcelain
```

Derive effective days from the unique normalized author dates. Keep the raw
commit list in the ledger so the result can be audited.

# Ledger Schema

The ledger is a JSON object with this shape:

```json
{
  "schema_version": 1,
  "project_timezone": "Europe/Madrid",
  "method": "commit_range_author_date_v1",
  "last_updated": "YYYY-MM-DD",
  "document_notes": [],
  "iterations": [
    {
      "iteration": "E1",
      "phase": "elaboration",
      "status": "closed",
      "planned_start": "YYYY-MM-DD",
      "planned_end": "YYYY-MM-DD",
      "actual_start": "YYYY-MM-DD",
      "actual_end": "YYYY-MM-DD",
      "start_ref": null,
      "end_ref": null,
      "branch": null,
      "method": "retrospective",
      "commit_count": 0,
      "effective_days": 0,
      "commit_days": [],
      "commits": [],
      "working_tree_clean_at_close": null,
      "scope": [
        {
          "uc": "UC01",
          "name": "Registrar Fichaje",
          "delivery_type": "full",
          "counts_for_average": true
        }
      ],
      "shared_boundary_days": [],
      "reliability": "low",
      "include_in_average": false,
      "excluded_reason": "No dates or scope evidence",
      "calibration": {
        "source_cutoff": null,
        "sample_iterations": [],
        "sample_ucs": 0,
        "median_days_per_uc": null,
        "weighted_average_days_per_uc": null,
        "range": [],
        "applied_to": [],
        "adjustment": "",
        "confidence": "none"
      },
      "notes": ""
    }
  ]
}
```

# Markdown Report Contract

The generated report MUST include:

- Title and purpose.
- Methodology and reliability legend.
- Iterations table with: iteration, start, end, calendar days, effective days,
  use cases, status, confidence, and whether it counts for the average.
- Git evidence table with start ref, end ref, commit count, commit days, and
  whether ancestry was valid.
- Average section with the formula, included records, total days, total UCs,
  and result.
- Excluded records table with reasons.
- Notes and known limitations.

Generated content must be delimited by:

```markdown
<!-- BEGIN GENERATED:iteration-history -->
...
<!-- END GENERATED:iteration-history -->
```

# Validation

Run `validate-iteration-history.ps1` before requesting approval. It MUST verify:

- JSON parses and `schema_version` is supported.
- Iteration identifiers are unique.
- `effective_days` equals the number of unique `commit_days`.
- `commit_count` is not negative.
- `include_in_average` is only true for `high` records.
- Every averaged UC has `delivery_type` `full` or `slice` and `counts_for_average: true`.
- The reported average equals total effective days divided by total averaged UCs.
- Every closed high record has both refs and a valid commit range.
- `start_ref` and `end_ref` are present for every record with git metrics.

# Anti-Patterns

- Reconstructing dates only from prose when git evidence exists.
- Using `git log --all` and counting orphan or agent-session commits.
- Counting uncommitted work as an effective day.
- Mixing author and committer dates.
- Counting a refactor or support item as a delivered use case.
- Averaging over low, medium, or open iterations.
- Editing the generated Markdown instead of the ledger.
- Hiding an unreliable record instead of recording its exclusion reason.
- Auto-committing or rewriting history without user approval.
- Using the historical average as a precise prediction instead of a calibrated reference.
- Estimating with low, medium, open, refactor-only, or mixed-scope iterations.
- Ignoring sample size or hiding a deviation greater than 30% from the historical range.
- Applying a multi-UC baseline to one UC without adjusting for scope.

# Results

Return:

- Ledger record added or updated.
- History report path.
- Effective days and reliability for the closed iteration.
- Current average and which records support it.
- Excluded records and reasons.
- Any anomalies requiring user review.
