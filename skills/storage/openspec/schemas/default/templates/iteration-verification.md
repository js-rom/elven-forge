# {{Iteration}} Iteration Verification

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| v1 | {{date}} | Initial verification for {{Iteration}}. | {{author}} |

---

## Scope and Inputs

- Iteration Plan: `08 Project Management/{{#}} {{Iteration}} Plan.md`
- Test Plan: `05 Test/{{#}} {{Iteration}} Test plan.md`
- Acceptance Test Plan: `05 Test/{{#}} {{Iteration}} Acceptance plan.md`
- Logical View: design sequence and class diagrams for the iteration slice
- Build layout: production source root and compile command

Scope IDs: {{list of Scope IDs from the Iteration Plan}}

---

## Design Conformance (14D)

| Element | Source | Implementation | Verdict | Action |
| :--- | :--- | :--- | :--- | :--- |
| <package / classifier / message> | <file + line> | <namespaced identifier#operation> | <MATCH \| MISSING \| EXTRA \| DIVERGENT> | <none / TDD item / route to 9B / route to 8> |
| ... | ... | ... | ... | ... |

- **Review scope (packages / scenarios):** {{review-scope}}
- **Out of scope (untouched packages validated in prior iterations):** {{out-of-scope}}
- **Build / compile evidence:** {{build-command + result}}

---

## Iteration Plan Coverage (14D)

| Scope ID | UC/Scenario | Design | Implementation | Test IDs | A-IDs | Evidence | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| <S1> | <UCxx Sx or n/a> | <DSD / DCD / UCR or n/a> | <classifier or operation, or n/a> | <T-xx or -> | <A-xx or -> | <test command, commit or inspection> | <COVERED \| DEFERRED \| MISSING \| PARTIAL> |
| ... | ... | ... | ... | ... | ... | ... | ... |

Rules:

- Every Scope ID from the Iteration Plan appears exactly once.
- `COVERED` requires implementation evidence and at least one Test ID or an explicit no-test rationale in `Evidence`.
- `DEFERRED` requires a row in Uncovered and Deferred with a reason and approval.
- `MISSING` and `PARTIAL` block the gate.

---

## Iteration Exit Criteria (14D)

| Criterion | Evidence | Verdict |
| :--- | :--- | :--- |
| <criterion from the Iteration Plan> | <command, report or inspection> | <MET \| NOT MET> |
| ... | ... | ... |

All criteria must be `MET` for the gate.

---

## Test Quality (Mutation)

Omit this section when the Iteration Plan sets mutation to `off`.

| Slice | Score | Target | Killed | Survived | No coverage | Trend | Verdict |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| <slice> | <0.0>% | <70> | <n> | <n> | <n> | <delta> | <PASS \| IMPROVE \| REINFORCE \| REGRESSION \| BLIND_SPOTS \| CRITICAL \| ACCEPT> |
| ... | ... | ... | ... | ... | ... | ... | ... |

| Mutant | Class | Line | Mutator | Status | Triaged as | Confirmed | Measure | Owner |
| :--- | :--- | ---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `<method>` | `<class>` | <line> | <mutator> | <SURVIVED \| NO_COVERAGE> | <class> | <yes \| no> | <measure> | <owner> |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

Rules:

- `PASS` requires zero survivors on protected invariants and a complete triage.
- `PASS` with a high `No coverage` is `BLIND_SPOTS`, not `PASS`.
- Every measure closes with evidence that the mutant died or was allowlisted.
- `CRITICAL` or `REGRESSION` blocks the gate under `blocking`; under `advisory` it is recorded as debt with a Scope ID.

---

## Code Quality

Omit this section when the Iteration Plan sets code quality to `off`.

| Gate | Coverage | Duplication | Issues | Critical | Verdict |
| :--- | ---: | ---: | ---: | ---: | :--- |
| <OK \| ERROR> | <0.0>% | <0.0>% | <n> | <n> | <PASS \| IMPROVE \| BLOCK \| REGRESSION \| ACCEPT \| BASELINE> |
| ... | ... | ... | ... | ... | ... |

| Issue | Type | Severity | File | Line | Triaged as | Confirmed | Measure | Owner |
| :--- | :--- | :--- | :--- | ---: | :--- | :--- | :--- | :--- |
| `<rule>` | <BUG \| VULNERABILITY \| CODE_SMELL \| SECURITY_HOTSPOT> | <BLOCKER \| CRITICAL \| MAJOR \| MINOR \| INFO> | `<path>` | <line> | <class> | <yes \| no> | <measure> | <owner> |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

Rules:

- `PASS` requires a green gate, zero new critical findings and new-code coverage at or above the floor.
- The first `BASELINE` is a debt record, not a pass.
- Every measure closes with evidence that the finding disappeared or was allowlisted.
- New critical bugs/vulnerabilities, ArchUnit violations and coverage below the floor block under `blocking`.

---

## Build Evidence

- **Compile command:** `<command>`
- **Result:** `<output summary>`

---

## Uncovered and Deferred

| Scope ID | Reason | Approved by |
| :--- | :--- | :--- |
| <Sx> | <why it is deferred or uncovered> | <user / date> |

---

## Verdict

| Check | Verdict |
| :--- | :--- |
| Design Conformance | <MATCH \| MISSING> |
| Iteration Plan Coverage | <COVERED \| MISSING> |
| Iteration Exit Criteria | <MET \| NOT MET> |
| Overall | <READY \| NOT READY> |
