# Elaboration Iterations History Instructions

## Purpose

Maintain one project-level history of every Elaboration iteration and one
machine-readable ledger. The ledger is the source of truth; the Markdown report
is generated from it.

## Artifacts

- `Elaboration Iterations Ledger`: `08 Project Management/Elaboration Iterations Ledger.json`
- `Elaboration Iterations History`: `08 Project Management/Elaboration Iterations History.md`

## Data Collection Rules

- Capture the iteration `start_ref` after `OK PASO 1`, before the Iteration Plan is committed.
- Capture the iteration `end_ref` after `OK PASO 17`.
- Use `git log <start_ref>..<end_ref>`; never use `git log --all`.
- Use author dates normalized to the project timezone; record committer dates as evidence too.
- Record commit hashes and commit days. Do not store only an inferred total.
- Do not infer use cases from commit messages. Use the approved Iteration Plan and confirm ambiguous classifications with the user.
- Classify every scope item as `full`, `slice`, `refactor`, `support`, or `retired`.
- Set `counts_for_average` explicitly; only `full` and `slice` may count.
- Record `working_tree_clean_at_close`; never count uncommitted work as an effective day.
- If the working tree is dirty, do not commit automatically. Mark the record `medium`, exclude it from the average, and ask the user whether the pending files belong to the iteration.

## Reliability Levels

| Level | Criteria | Include in average |
| :--- | :--- | :--- |
| `high` | Closed, valid refs and ancestry, clean tree, explicit scope, at least one commit day | Yes |
| `medium` | Closed but dirty tree, fallback refs, ambiguous boundary, or mixed unclassified scope | No |
| `low` | Missing dates, missing scope, no git history, or retrospective reconstruction | No |
| `open` | Iteration not closed | No |

## Average Rule

`average = sum(effective_days of high records) / sum(counts_for_average UCs of high records)`

The report must show included records, total effective days, total computable
UCs, and the final result. Refactors, support work, and retired use cases never
count.

## Markdown Rules

- Generate tables from the ledger.
- Keep generated content inside `<!-- BEGIN GENERATED:iteration-history -->` and `<!-- END GENERATED:iteration-history -->`.
- Do not edit generated tables directly.
- Include methodology, iteration table, planned-vs-actual table, git evidence, average section, exclusions, and notes.
- Use Spanish in the generated document.

## Validation

Before requesting `OK PASO 18`, run the skill validation script. It must verify
unique iterations, effective-day totals, git ancestry, average eligibility,
UC delivery types, and the average formula.
