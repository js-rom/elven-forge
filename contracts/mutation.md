# Mutation Testing Contract

How the UP flow runs, reads and acts on mutation testing. The score is a
measurement, never a verdict on its own.

## Scope

- Applies to the Elaboration phase, steps 14B and 14D.
- Opt-in per iteration through the `Test Quality` block of the Iteration Plan.
- The unit of analysis is the **iteration slice**, never the whole repository.
- Acceptance tests (Cucumber) are out of scope. Mutation runs over unit and
  integration tests that cover the target classes.

## Roles

| Role | Responsibility |
|---|---|
| `runner` | Executes PIT with the `mutation` profile. Does not edit. |
| `test-author` | Triages weak tests and strengthens them under a recorded re-open. |
| `implementer` | Removes dead code or fixes unreachable branches. |
| `orchestrator` | Classifies equivalents, owns the allowlist, presents the reading. |
| `reviewer` | Judges the triage with `rubrics/mutation-quality.md`. |

## Where it runs

```text
14B  tests + code GREEN
     └─ mutation (slice) → triage → actions → re-test → re-mutation
     └─ OK 14B final (with the triage as evidence)
14C  acceptance (unchanged)
14D  Iteration Verification → Test Quality (Mutation)
```

No new gate: the mutation loop closes inside 14B, before the final `OK 14B`.
14D reports the result and applies the veto. There is no `OK 14B.MUT`.

## Score

```text
score = killed / (killed + survived)
```

- `NO_COVERAGE` is excluded from the denominator and reported separately.
- `TIMED_OUT`, `RUN_ERROR`, `NON_VIABLE` and `MEMORY_ERROR` are reported
  separately; they are not evidence of a weak test and not evidence of a kill.
- `no_coverage_ratio = no_coverage / generated`.
- The score is always reported with `killed`, `survived`, `no_coverage`,
  the target and the delta against the previous baseline.

## Five signals

The score is read with all five; reading only the first is a process error.

1. `score` over covered mutants.
2. `no_coverage_ratio` and the classes it concentrates in.
3. Survivor concentration by class, method and mutator.
4. Delta against `journal/{iteration}/mutation-baseline.json`.
5. Survivors on invariants declared as protected in the Iteration Plan.

## Survivor taxonomy

Every survivor gets exactly one class. `UNCLASSIFIED` blocks the triage.

| Class | Recognition | Owner | Measure |
|---|---|---|---|
| `WEAK_ASSERTION` | line covered; the method kills other mutants but not this one | `test-author` | strengthen the assertion on the observable effect |
| `MISSING_BEHAVIOR_TEST` | no test exercises that branch or condition | `test-author` | add an equivalence-class or boundary case |
| `NO_COVERAGE` | PIT reports `NO_COVERAGE` | `test-author` / `implementer` | if reachable from an approved Scope ID, test; if not, dead code |
| `SCOPE_GAP` | not covered by `targetTests`, but JaCoCo shows the line covered by the full suite | `orchestrator` | widen `targetTests` or record it as scope evidence; no test required |
| `DEAD_CODE` | no call site reachable from an approved Scope ID | `implementer` | delete, or justify and exclude |
| `EQUIVALENT` | the mutant does not change observable behavior | `orchestrator` | allowlist entry with rationale and evidence |
| `DESIGN_GAP` | exposes a rule that no contract states | `orchestrator` | route to 04/10/11; never hide behind a test |
| `ENVIRONMENT` | logging, `toString`, getters, config, generated code | `orchestrator` | documented exclusion pattern |

`NO_COVERAGE` is a finding, not an exclusion. A reachable uncovered branch is a
`MISSING_BEHAVIOR_TEST`; an unreachable one is `DEAD_CODE`.

`NO_COVERAGE` is relative to the configured `targetTests`. Before classifying it
as `DEAD_CODE` or adding a test, check whether a test outside the mutation scope
covers the method. If JaCoCo shows the line is covered by the full suite, the
class is `SCOPE_GAP`, not a blind spot.

## Verdicts

The score chooses the posture; the survivors choose the action; invariants veto.

| Signal | Verdict | Measure | Closes 14B? |
|---|---|---|---|
| `score >= T` and 0 invariant survivors | `PASS` | record baseline | yes |
| `T-10 <= score < T` | `IMPROVE` | kill by domain criticality; boundaries and conditionals with parameterized tests | yes, with no `WEAK_ASSERTION` or `MISSING_BEHAVIOR_TEST` left |
| `score < T-10` | `REINFORCE` | full triage; one behavior test per affected class; a concentration points to testability, not to tests | no (advisory: yes with recorded debt) |
| `score < baseline - 5` | `REGRESSION` | explain the delta before closing: removed test, weakened test or refactor without test | no |
| `no_coverage_ratio > 20%` | `BLIND_SPOTS` | separate unreachable (delete) from untested (add) | no |
| 1+ survivor on a protected invariant | `CRITICAL` | invariant with an executable assertion; if it is not in the contract, route to 04/10 | no (always vetoes) |
| most survivors are `EQUIVALENT` | `ACCEPT` | allowlist; above 10% of the total, the semantics are ambiguous: consider refactoring | yes |

`T` comes from the Iteration Plan. Defaults: `70` for a normal slice, `80` for
domain-critical code. The calibration replaces the default after two iterations:
`T = max(60, baseline)`.

## Measures and evidence of effect

A measure closes only with evidence that the survivor died. "I fixed it" is not
evidence.

| Measure | Owner | Evidence of effect |
|---|---|---|
| Strengthen an assertion | `test-author` | re-run the class; the mutant is `KILLED` |
| Add a boundary or equivalence case | `test-author` | re-run the class; the mutant is `KILLED` |
| Delete dead code | `implementer` | the mutant no longer exists; tests still green |
| Route a design gap | `orchestrator` | the contract is updated and the new assertion kills the mutant |
| Allowlist an equivalent | `orchestrator` | entry approved, with the argument and a test reference |
| Exclude infrastructure | `orchestrator` | exclusion pattern documented in the Iteration Plan |

## Allowlist

Project-scoped, at `openspec/artifacts/{domain}/mutation-allowlist.json`.

```json
{
  "version": 1,
  "entries": [
    {
      "id": "MUT-001",
      "class": "com.example.DomainPolicy",
      "method": "toString",
      "line": 42,
      "mutator": "NullReturnValsMutator",
      "reason": "Equivalent: no observable effect on any contract.",
      "approved_by": "user",
      "date": "2026-12-01"
    }
  ]
}
```

The key is `class#method:line:mutator`. If the line moves, the entry stops
matching and the mutant returns to triage: no zombie allowlists.

## Re-open protocol

Mutation runs after GREEN, so strengthening a test touches a frozen tree. The
only legitimate path is a recorded re-open by the `test-author`:

```bash
python .agents/scripts/test_guard.py --tests --record --reopen --reason "MUT: 3 weak assertions in EmployeeAbsenceLedger"
```

- `--record` on an existing baseline fails without `--reopen`.
- `--reopen` requires a non-empty reason and appends it to the baseline.
- The `implementer` never re-opens tests.
- A re-open **strengthens, never widens scope**: it may add assertions or cases
  for behavior already approved in the Test Plan. A new scenario returns to 14A
  and needs a new `OK 14A`; a new feature returns to 14A as well.

## Gate policy

| Policy | Behaviour |
|---|---|
| `advisory` | Reports the verdict; never blocks. Used for the pilot and calibration. |
| `blocking` | Blocks on `CRITICAL` (invariant survivor) and `REGRESSION`. The absolute score stays advisory. |

Under `advisory`, non-blocking debt is recorded with a Scope ID or a mutation
debt ID (`MUT-E21-01`) and reviewed in the next iteration. A debt ID is
traceable and owned; it is not a silent TODO.

`CRITICAL` always vetoes, regardless of policy, when the invariant is declared
as protected in the Iteration Plan.

## Presentation contract

The orchestrator presents the reading with this shape, not the raw report:

```text
Score 78% (target 70) | +6 vs baseline | 6 survivors, 2 without coverage
Diagnosis: 2 boundary assertion gaps, 1 missing business case, 2 dead-code, 1 equivalent.
Measures: 1) boundaries in OverlapValidator (test-author)
          2) weekend crossing (test-author)
          3) delete LegacyImport (implementer)
          4) allowlist toString.
Expected effect: 78% -> 91%, 0 without coverage.
```

## Anti-patterns

- Treating the score as a grade or a KPI for a person or an agent.
- Chasing 100% and allowlisting nothing.
- Reading the score without `no_coverage` and the baseline delta.
- Mutating the whole repository or the acceptance suite.
- Comparing scores across slices with different criticality.
- Weakening a test to make the suite pass.
- Silently re-baselining tests to hide a mutation finding.
- Marking `NO_COVERAGE` as "excluded" without classifying it.
- Reading a narrow `targetTests` run as whole-suite coverage.
