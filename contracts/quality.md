# Code Quality Contract

How the UP flow runs, reads and acts on static code quality. The gate is a
measurement over the iteration slice, not a grade for the repository.

## Scope

- Applies to the Elaboration phase, steps 14B and 14D.
- Opt-in per iteration through the `Code Quality` block of the Iteration Plan.
- The unit of analysis is the **new code of the slice**, not the whole legacy
  repository.
- SonarQube is the aggregator; ArchUnit covers architecture and Trivy covers
  dependencies. Mutation (F7) remains the test-strength signal.

## Roles

| Role | Responsibility |
|---|---|
| `runner` | Runs the Sonar analysis, ArchUnit and Trivy. Does not edit. |
| `implementer` | Fixes bugs, vulnerabilities and smells in `src/main`. |
| `test-author` | Closes coverage gaps in `src/test`. |
| `orchestrator` | Owns the gate, the baseline, the allowlist and the reading. |
| `reviewer` | Judges the triage with `rubrics/code-quality.md`. |

## Where it runs

```text
14B  tests + code GREEN
     ├─ Sonar quality gate + ArchUnit + Trivy (slice / new code)
     ├─ triage → fixes → re-run (the gate must turn green)
     ├─ mutation (F7)
     └─ OK 14B
14C  acceptance
14D  Iteration Verification → Code Quality
```

No new gate: the quality loop closes inside 14B, before the final `OK 14B`.
If the Sonar server is down, the step is `SKIPPED` with a warning; an
infrastructure outage never blocks an iteration.

## Signals

| Signal | Source | Target | Blocks |
|---|---|---|---|
| New bugs | Sonar `new_bugs` / issues `type=BUG` | 0 `blocker`/`critical` | yes |
| New vulnerabilities | Sonar `new_vulnerabilities` / `type=VULNERABILITY` | 0 `blocker`/`critical` | yes |
| New coverage | JaCoCo + Sonar `new_coverage` | >= 80% | yes |
| New duplicated lines | Sonar `new_duplicated_lines_density` | <= 3% | no |
| New code smells | Sonar `new_code_smells` | 0 `blocker`/`critical`; `major` advisory | partial |
| Security hotspots | Sonar `new_security_hotspots_reviewed` | 100% reviewed | yes |
| Architecture violations | ArchUnit | 0 new | yes |
| Dependency CVEs | Trivy | 0 `critical` with a fix | yes |
| New technical debt | Sonar `new_technical_debt` | trend only | no |

## Taxonomy

Every finding gets exactly one class. `UNCLASSIFIED` blocks the triage.

| Class | Recognition | Owner | Measure |
|---|---|---|---|
| `BUG` | Sonar issue `type=BUG` | `implementer` | fix the defect, keep the tests green |
| `VULNERABILITY` | issue `type=VULNERABILITY` | `implementer` | fix or mitigate; allowlist only if false positive |
| `SECURITY_HOTSPOT` | issue `type=SECURITY_HOTSPOT` | `implementer` | review and mark safe, or fix |
| `CODE_SMELL` | issue `type=CODE_SMELL` | `implementer` | refactor, or defer with a debt ID |
| `ARCHITECTURE` | ArchUnit violation | `orchestrator` | route to 8/11 and fix the dependency |
| `COVERAGE_GAP` | new coverage below the floor | `test-author` | add a test for the new lines |
| `DEPENDENCY_RISK` | Trivy CVE | `implementer` | upgrade or mitigate |
| `FALSE_POSITIVE` | confirmed on the allowlist | `orchestrator` | allowlist with rationale and evidence |

Severity uses Sonar's `severity` (`BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`,
`INFO`) and the new `impacts` model (`softwareQuality`, `severity`). A finding
is critical when it is a `BUG`/`VULNERABILITY` with `BLOCKER`/`CRITICAL`
severity, or a `HIGH` impact on `SECURITY`/`RELIABILITY`.

## Verdicts

| Signal | Verdict | Measure | Closes 14B? |
|---|---|---|---|
| Gate OK, 0 new critical, coverage >= 80%, duplication <= 3% | `PASS` | record baseline | yes |
| New smells or duplication above target, coverage below 80% | `IMPROVE` | fix the top offenders | yes, when no critical remains |
| New critical bug/vulnerability, ArchUnit violation, critical CVE | `BLOCK` | fix before closing 14B | no |
| Coverage or duplication worsens more than 5 / 2 points vs baseline | `REGRESSION` | explain and correct | no |
| All remaining findings are allowlisted | `ACCEPT` | allowlist with evidence | yes |

Under `advisory`, a `BLOCK` is reported but does not fail the step; under
`blocking`, `BLOCK` and `REGRESSION` fail the gate. The absolute scores
(bugs, smells, debt) are never a gate by themselves.

## Measures and evidence of effect

| Measure | Owner | Evidence of effect |
|---|---|---|
| Fix a bug or vulnerability | `implementer` | the issue disappears from the next analysis; tests green |
| Refactor a smell | `implementer` | the issue disappears; complexity/duplication drop |
| Add a coverage test | `test-author` | `new_coverage` rises above the floor |
| Review a hotspot | `implementer` | hotspot marked safe in Sonar |
| Upgrade a dependency | `implementer` | the CVE disappears from Trivy |
| Route an architecture violation | `orchestrator` | the dependency is fixed in 8/11 |
| Allowlist a false positive | `orchestrator` | entry approved with rationale and evidence |

## Baseline and new code

- Each iteration publishes `sonar.projectVersion=<Iteration>` (for example
  `E22`). The project uses **new code: previous version**, so the gate only
  sees the iteration's changes.
- The first analysis is a baseline: it records existing debt and is not a pass.
- `journal/{iteration}/quality-baseline.json` stores the gate, the measures and
  the issue counts. The next iteration compares against it.
- Legacy debt is never blocked; it is reported and paid down deliberately.

## Allowlist

Project-scoped, at `openspec/artifacts/{domain}/quality-allowlist.json`.

```json
{
  "version": 1,
  "entries": [
    {
      "id": "QUA-001",
      "rule": "java:S2077",
      "component": "src/main/java/com/example/Legacy.java",
      "line": 84,
      "reason": "False positive: the query is a constant, not user input.",
      "approved_by": "user",
      "date": "2026-12-01"
    }
  ]
}
```

The key is `rule#component:line`. If the line moves, the entry stops matching
and the finding returns to triage.

## Presentation contract

```text
Quality gate: OK | new code: 0 bugs, 0 vulnerabilities, 2 smells, coverage 84%, duplication 1.2%
Diagnosis: 2 maintainability smells in the new adapter; no critical findings.
Measures: 1) extract the duplicated mapping (implementer) 2) add a boundary test (test-author).
Expected effect: gate OK, smells 0, coverage 86%.
```

## Anti-patterns

- Blocking the iteration on legacy debt from the whole repository.
- Using a single "quality score" as the gate.
- Treating the first baseline analysis as a pass.
- Ignoring a false positive instead of allowlisting it with evidence.
- Running Sonar as the only quality gate, without ArchUnit or Trivy.
- Analyzing generated code (`target`, `node_modules`, Vaadin generated frontend).
- Letting a Sonar outage block a step.
- Weakening tests or suppressing rules to make the gate green.
