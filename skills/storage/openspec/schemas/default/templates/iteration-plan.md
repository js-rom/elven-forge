# Iteration Plan

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Iteration draft | {{date}} | First draft for the current iteration plan. To be refined during iteration planning. | {{author}} |
| | | | |

---

## Iteration Context

- **Iteration:** {{iteration-name}}
- **Phase:** {{phase}}
- **Time Box:** 2 weeks
- **Start Date:** {{start-date}}
- **End Date:** {{end-date}}
- **Iteration Goal:** <Short statement of the business or technical outcome expected from this iteration.>

> In the Unified Process, the normal planning unit is often a use case scenario or thin slice rather than a full use case. Use a full use case only when it is realistically deliverable within the iteration.

---

## Team Availability

| Member | Role | Available Hours | Notes |
| :--- | :--- | :--- | :--- |
| <Member 1> | <Role> | <hours in this 2-week period> | <Vacation, support load, part-time allocation, etc.> |
| <Member 2> | <Role> | <hours> | <Notes> |
| <Member 3> | <Role> | <hours> | <Notes> |
| **Total** |  | **{{total-available-hours}}** | |

---

## Selected Scope Summary

| Scope ID | Priority | Planning Unit | Scope Item | Why Selected | Planned Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <S1> | High | <Scenario \| Use Case \| Feature> | <Use case, scenario, or feature name> | <Risk, coverage, or criticality reason> | <What should be demonstrated or completed this iteration> |
| <S2> | High | <Scenario \| Use Case \| Feature> | <Name> | <Reason> | <Outcome> |
| <S3> | Medium | <Scenario \| Use Case \| Feature> | <Name> | <Reason> | <Outcome> |
| ... | ... | ... | ... | ... | ... |

The `Scope ID` is stable for the iteration. The Test Plan, the Acceptance Test Plan and the Iteration Verification use it as the traceability key.

---

## Test Quality

| Field | Value |
| :--- | :--- |
| Mutation testing | <on \| off> |
| Target classes | <packages or classes; the iteration slice only> |
| Target tests | <test classes that cover the slice> |
| Target score (`T`) | <70 default; 80 for domain-critical code> |
| Policy | <advisory \| blocking> |
| Protected invariants | <INV ids or `class#method`> |
| Runtime budget | <minutes> |

When `off`, 14B and 14D do not run mutation and the section does not appear in the Iteration Verification.

---

## Code Quality

| Field | Value |
| :--- | :--- |
| Code quality | <on \| off> |
| Project key | <sonar project key> |
| Sonar host | <http://localhost:9000> |
| Scope | <new \| all> (`all` only for the first baseline) |
| Target coverage | <80> |
| Max duplication | <3> |
| Policy | <advisory \| blocking> |
| Architecture | ArchUnit |
| Dependencies | Trivy |
| Runtime budget | <minutes> |

When `off`, 14B and 14D do not run Sonar and the section does not appear in the Iteration Verification. The first analysis with `scope=all` is a baseline: it records legacy debt and is not a pass.

---

## History Tracking

| Scope ID | Scope Item | UC ID | Delivery Type | Counts for average |
| :--- | :--- | :--- | :--- | :--- |
| <S1> | <Use case, scenario, slice, or feature> | <UCxx or empty> | <full \| slice \| refactor \| support \| retired> | <Yes \| No> |
| ... | ... | ... | ... | ... |

---

## Historical Calibration

| Item | Value |
| :--- | :--- |
| Source | `Elaboration Iterations History` + ledger, cutoff `<date>` |
| Sample iterations | `<E12, E13, E15>` |
| Sample UCs | `<n>` |
| Effective days per UC | `<values>` |
| Median days per UC | `<value>` |
| Weighted average days per UC | `<value>` |
| Range | `<min>-<max>` |
| Applied to | `<UCxx>` |
| Adjustment | `<complexity, risk, UI, persistence, uncertainty>` |
| Calibrated estimate | `<effective days>` |
| Reconciliation with task breakdown | `<estimate vs task-derived estimate>` |
| Confidence | `<High \| Medium \| Low>` and rationale |

---

## Selected Work Detail

### <Scope ID> — <Use Case, Scenario, or Feature>

- **Planning Unit:** <Scenario | Use Case | Feature>
- **Parent Use Case:** <Name of the parent use case when planning a scenario. Leave blank if not applicable.>
- **Scenario Slice:** <Short description of the selected scenario or slice.>

- **Description:** <Describe the scope to be covered in this iteration.>
- **Questions Resolved:** <List clarifications that were resolved during planning.>
- **Open Questions:** <List remaining uncertainties if any.>
- **Expected Result:** <Describe the concrete result expected by the end of the iteration.>

### <Use Case, Scenario, or Feature 2>

- **Planning Unit:** <Scenario | Use Case | Feature>
- **Parent Use Case:** <Name of the parent use case when planning a scenario. Leave blank if not applicable.>
- **Scenario Slice:** <Short description of the selected scenario or slice.>

- **Description:** <Describe the scope to be covered in this iteration.>
- **Questions Resolved:** <List clarifications that were resolved during planning.>
- **Open Questions:** <List remaining uncertainties if any.>
- **Expected Result:** <Describe the concrete result expected by the end of the iteration.>

---

## Work Breakdown and Estimates

| ID | Area | Task | Related Scope Item | Estimate (h) | Running Total (h) | Owner | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | UI | <Task description> | <Use case, scenario, or feature> | <hours> | <running total> | <Owner> | <Notes> |
| T2 | Database | <Task description> | <Use case, scenario, or feature> | <hours> | <running total> | <Owner> | <Notes> |
| T3 | Domain | <Task description> | <Use case, scenario, or feature> | <hours> | <running total> | <Owner> | <Notes> |
| T4 | Integration | <Task description> | <Use case, scenario, or feature> | <hours> | <running total> | <Owner> | <Notes> |
| T5 | Test | <Task description> | <Use case, scenario, or feature> | <hours> | <running total> | <Owner> | <Notes> |
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## Capacity Check

- **Total Available Hours:** {{total-available-hours}}
- **Total Estimated Hours:** {{total-estimated-hours}}
- **Planned Buffer:** {{buffer-hours}}
- **Remaining Capacity:** {{remaining-hours}}
- **Scope Cut Line:** <State which work is deferred first if estimates grow beyond available capacity.>

---

## Risks and Dependencies

| Item | Type | Impact | Mitigation / Follow-up |
| :--- | :--- | :--- | :--- |
| <Risk or dependency> | <Risk \| Dependency> | <Impact on the iteration> | <Mitigation or next action> |
| <Risk or dependency> | <Risk \| Dependency> | <Impact> | <Mitigation> |
| ... | ... | ... | ... |

---

## Iteration Exit Criteria

- <Outcome that must be true by the end of the iteration>
- <Outcome that must be true by the end of the iteration>
- <Outcome that must be true by the end of the iteration>

---

## Notes

<Additional planning notes, assumptions, coordination agreements, or deferred work.>
