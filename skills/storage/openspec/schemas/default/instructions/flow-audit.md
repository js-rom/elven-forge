# Flow Audit Instructions

## Purpose

Audit the Elaboration flow using commit days per step and produce a report with
bottlenecks and improvement experiments. The audit is non-blocking and must run
automatically after PASO 18.

## Artifacts

- `Flow Audit Ledger`: `08 Project Management/Flow Audit Ledger.json`
- `Flow Audit Report`: `08 Project Management/Flow Audit Report.md`

## Rules

- Measure process flow, never individual productivity.
- Prefer instrumented step timestamps when available.
- In retrospective mode, use commit days per step and label the limitation.
- Classify commits by explicit message marker, then changed path, then manual evidence.
- Exclude generated files, `out/`, `todo/`, schemas, and `.agents` internals from development metrics; record them as tooling.
- Mark confidence `high`, `medium`, or `low`; do not base strong conclusions on low confidence.
- Keep `sources` and `manual_findings` in the ledger.
- Generate the Markdown report from the ledger; do not edit generated tables manually.
- Run the validation script before reporting.

## Automatic PASO 18

After `OK PASO 18` and after the elaboration history is persisted:

1. Add or update the closed iteration in `sources`.
2. Run `build-flow-audit.ps1`.
3. Run `render-flow-audit.ps1`.
4. Run `validate-flow-audit.ps1`.
5. Persist both artifacts with storage.
6. Report a short summary; do not request a new approval.

## Report Requirements

Include coverage, limitations, per-iteration summary, top steps, heatmap, manual
findings, tooling, hypotheses, experiments, confidence, and next measurement.
