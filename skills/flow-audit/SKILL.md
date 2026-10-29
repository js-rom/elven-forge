---
name: flow-audit
description: >
  Audits the up-elaboration development flow using commit days per step,
  artifact and code churn, rework evidence, and retrospective or instrumented
  flow data. Produces a flow audit ledger and a Markdown report with bottlenecks,
  hypotheses, and improvement experiments. Triggers: flow audit, process audit,
  cuellos de botella, tiempo de desarrollo, desarrollo lento, rework, iteration
  bottleneck, auditoria de flujo.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

# Purpose

You audit the Elaboration process to find where development time is lost and
which changes are most likely to reduce lead time without weakening quality.

You produce:

1. `Flow Audit Ledger` - JSON evidence and step-level metrics.
2. `Flow Audit Report` - Markdown analysis and improvement plan.

Default paths:

- `08 Project Management/Flow Audit Ledger.json`
- `08 Project Management/Flow Audit Report.md`

# Scope

The audit covers the process, not individual productivity. Use commit days,
artifact churn, rework, overlap, and batch size. Never rank people.

Retrospective mode is allowed when the required data exists. Instrumented mode
is preferred after PASO 18 starts recording step events.

# Data Sources

- Git history for the iteration range.
- `Iteration Plan`.
- `Elaboration Iterations Ledger` and `Elaboration Iterations History`.
- `state.yaml` notes and approved steps.
- Artifact revision histories for rework evidence.
- Test plans, acceptance plans, and test results when available.

# Metrics

| Metric | Definition |
| :--- | :--- |
| `commit_days` | Unique author dates with at least one commit assigned to the step |
| `span_days` | Calendar days between first and last commit of the step |
| `commit_count` | Commits assigned to the step |
| `overlap_days` | Dates where two or more steps have commits |
| `artifact_churn` | Commits touching an artifact after its step was closed |
| `rework_count` | Reopened steps or explicit correction loops |
| `tooling_days` | Dates spent only on generated, todo, submodule, or tooling files |
| `code_test_ratio` | Code/test commits vs documentation/artifact commits |

Do not report wait time or approval latency in retrospective mode unless the
source records contain reliable timestamps.

# Commit Classification

Use this order:

1. Explicit step marker in the commit message (`PASO 14B`, `14D`, etc.).
2. Primary changed path using the step-to-path rules.
3. Manual evidence from `state.yaml` or artifact revision history.
4. Otherwise classify as `unclassified` or `tooling`.

Rules:

- A commit may have one primary step and several secondary steps.
- A date counts once per step.
- Exclude generated frontend files, `out/`, `.agents` submodule internals, and
  `todo/` files from development metrics; report them as tooling.
- Mark confidence `high` when the message names the step, `medium` when a path
  mapping is clear, and `low` when the classification is ambiguous.
- Never use low-confidence records for a strong conclusion.

# Workflow

## Retrospective audit

1. Read the existing flow ledger. It must contain `sources` with iteration,
   `start_ref`, `end_ref`, and status.
2. Run `build-flow-audit.ps1` to rebuild step metrics from git.
3. Review `unclassified` commits and manual findings.
4. Run `render-flow-audit.ps1` to generate the Markdown report.
5. Run `validate-flow-audit.ps1`.
6. Present the top bottlenecks and proposed experiments to the user.

## Automatic PASO 18 audit

After `OK PASO 18`, after the elaboration history is persisted:

1. Add or update the closed iteration in `sources`.
2. Run `build-flow-audit.ps1`.
3. Run `render-flow-audit.ps1`.
4. Run `validate-flow-audit.ps1`.
5. Persist both artifacts through the storage skill.
6. Report a short summary: top steps, rework signals, and recommended experiments.
7. Do not add a new approval gate; the audit is automatic and non-blocking.

## Instrumented mode

When step timestamps are available, add:

- `step_started_at`
- `step_approved_at`
- `step_start_ref`
- `step_end_ref`
- `approval_attempts`
- `reopen_count`

Use them to calculate lead time, flow efficiency, wait time, and first-pass yield.
Do not fabricate these fields in retrospective records.

# Report Structure

The report MUST include:

1. Executive summary.
2. Coverage and limitations.
3. Per-iteration summary.
4. Step metrics table.
5. Commit-day heatmap.
6. Top bottlenecks by commit days and commit count.
7. Overlap and rework findings.
8. Tooling and unclassified work.
9. Manual findings.
10. Improvement hypotheses and experiments.
11. Confidence and next measurement date.

# Improvement Guardrails

- Prefer removing rework and waiting over removing quality gates.
- Validate every experiment with a before/after metric.
- Use median and range for small samples.
- Separate observations from hypotheses.
- Do not infer causality from commit dates alone.
- Report evidence paths and commit hashes for each strong finding.

# Anti-Patterns

- Ranking developers by commit count.
- Counting generated files as development work.
- Treating commit dates as hours worked.
- Mixing retrospective estimates with instrumented timestamps without labeling them.
- Concluding a step is slow only because it has more commits.
- Recommending fewer tests or weaker gates without measuring defect escape.
- Editing the generated report instead of the ledger and sources.

# Results

Return:

- Flow ledger path.
- Audit report path.
- Coverage and confidence.
- Top 3 bottlenecks with evidence.
- Top improvement experiments.
- Data gaps that require instrumentation.
