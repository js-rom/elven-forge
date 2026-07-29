# Test Plan

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Test plan draft | {{date}} | Initial test plan generated from Step 1 of the TDD loop. | {{author}} |
| | | | |

---

## Planning Context

- **Iteration:** {{iteration-name}}
- **Phase:** {{phase}}
- **Domain:** {{domain}}
- **Iteration Plan Item / Slice:** {{iteration-plan-item-reference}}
- **Use Case / Scenario Slice:** {{use-case-or-slice}}
- **Use Case Realization Reference:** {{use-case-realization-reference}}
- **Execution Mode:** {{Guided mode | Automatic mode}}

---

## Input Baseline and Design References

- **SSD References:** {{ssd-references}}
- **Operation Contract References:** {{operation-contract-references}}
- **SW Architecture References (if applicable):** {{architecture-references-or-NA}}
- **Persistence References (if applicable):** {{persistence-references-or-NA}}
- **UI References (if applicable):** {{ui-references-or-NA}}

---

## Scope and Intent

- **Objective:** <What behavior is validated by this plan?>
- **In Scope:** <Boundaries of this test planning cycle>
- **Out of Scope:** <Explicit exclusions to avoid ambiguity>
- **Assumptions:** <Assumptions agreed with the user>

---

## Factor Analysis

| Factor | Candidate Values | Risk / Note |
| :--- | :--- | :--- |
| <Factor 1> | <Value set> | <Why it matters> |
| <Factor 2> | <Value set> | <Why it matters> |
| ... | ... | ... |

---

## Equivalence Classes

| Factor | Class ID | Type (Valid/Invalid) | Representative Value | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| <Factor> | EC-01 | Valid | <value> | <reason> |
| <Factor> | EC-02 | Invalid | <value> | <reason> |
| ... | ... | ... | ... | ... |

---

## Boundary Value Analysis

| Variable | Boundary | Just Below | At Boundary | Just Above | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <Variable> | <value> | <case> | <case> | <case> | <reason> |
| ... | ... | ... | ... | ... | ... |

---

## Combinatorial Reduction

- **Strategy:** <Pairwise | Orthogonal Array | Explicit combinations>
- **Why this strategy:** <Reason to reduce combinations while keeping risk coverage>

| Combination ID | Inputs Combined | Covered Risk | Included in Test List (Yes/No) |
| :--- | :--- | :--- | :--- |
| C-01 | <input set> | <risk> | Yes |
| C-02 | <input set> | <risk> | No |
| ... | ... | ... | ... |

---

## Agreed Test List (Step 1 Output)

| Test ID | Scenario Slice | Preconditions | Input / Trigger | Expected Result | Selection Rationale | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | <slice> | <state> | <input> | <expected behavior> | <risk/boundary/class reason> | High |
| T-02 | <slice> | <state> | <input> | <expected behavior> | <reason> | Medium |
| ... | ... | ... | ... | ... | ... | ... |

---

## Approval and Execution Policy

- **Approval model:**
	- Guided mode: one-by-one implementation with explicit user approval before RED.
	- Automatic mode: one-by-one implementation of the agreed list without per-case approval; each item must complete `RED -> GREEN -> REFACTOR` before the next.
- **Selected model for this plan:** {{Guided mode | Automatic mode}}
- **Approval evidence:** {{chat confirmation / token / timestamp}}

---

## Traceability

| Test ID | Iteration Plan Item | Use Case / Scenario | UCR Section | SSD Operation / Extension | Operation Contract Postcondition | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | <item> | <scenario> | <section> | <operation or extension> | <postcondition> | <note> |
| T-02 | <item> | <scenario> | <section> | <operation or extension> | <postcondition> | <note> |
| ... | ... | ... | ... | ... | ... | ... |

### Architecture References (if applicable)

| Test ID | SW Architecture Reference | Architectural Analysis / Technical Memo Reference | Notes |
| :--- | :--- | :--- | :--- |
| T-01 | <reference or N/A> | <reference or N/A> | <note> |
| T-02 | <reference or N/A> | <reference or N/A> | <note> |
| ... | ... | ... | ... |

### Persistence References (if applicable)

| Test ID | Data Model Reference | JPA Mapping Reference | Notes |
| :--- | :--- | :--- | :--- |
| T-01 | <reference or N/A> | <reference or N/A> | <note> |
| T-02 | <reference or N/A> | <reference or N/A> | <note> |
| ... | ... | ... | ... |

### UI References (if applicable)

| Test ID | Design System / Visual Spec Reference | Interaction / Vaadin Reference | Notes |
| :--- | :--- | :--- | :--- |
| T-01 | <reference or N/A> | <reference or N/A> | <note> |
| T-02 | <reference or N/A> | <reference or N/A> | <note> |
| ... | ... | ... | ... |

---

## Risks and Follow-ups

| Risk / Pending Question | Impact | Mitigation / Next Action |
| :--- | :--- | :--- |
| <risk> | <impact> | <action> |
| ... | ... | ... |

---

## Notes

<Additional context for upcoming RED-GREEN-REFACTOR cycles.>
