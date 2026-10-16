# Acceptance Test Plan

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Acceptance plan draft | {{date}} | Initial ATDD acceptance plan for the iteration slice (Gherkin scenarios over the real stack). | {{author}} |
| | | | |

---

## Planning Context

- **Phase:** elaboration
- **Domain:** <domain>
- **Iteration:** <iteration>
- **Use Cases in scope:** <UC ids>
- **Approach:** ATDD — escenarios Gherkin como especificación ejecutable contra la pila real (UI + presentador + controlador + servicio + repositorios).
- **Source Artifacts:** <use cases, domain model, domain rules, interaction specs>
- **Execution:** `mvn test -Pacceptance`

---

## Technology Stack

<Describe the acceptance harness: Cucumber + Spring glue, Vaadin browserless, Testcontainers, fixed clock, security bootstrap, fault injection seams.>

---

## Scenario List (Agreed Acceptance List — 14A Output)

| Scenario ID | Gherkin | UC Step / Extension | Domain Invariant | Interaction Spec | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | <scenario name> | <step/ext> | <I#> | <state/transition id> | <High/Medium/Low> |

Feature file(s): <path(s) under src/test/resources/features>

---

## Invariant Coverage Matrix

Criterio de promoción a aceptación (puerta de decisión): (1) traza a regla legal, (2) riesgo de integración entre capas, (3) efecto visible al actor, (4) contrato nuclear del dominio. Si ninguna aplica, la invariante permanece en unitario con justificación registrada.

| Invariant | Legal Rule | TDD Coverage | Acceptance Coverage | Decision |
| :--- | :--- | :--- | :--- | :--- |
| <I#> | <RULE# or —> | <TDD test ids> | <scenario ids or unit-only> | <criteria numbers and rationale> |

---

## Domain Rules Compliance Matrix

| Rule | Status | Evidence |
| :--- | :--- | :--- |
| <RULE#> | Cubierto / Pendiente / N-A | <invariant, UC, test, or justification> |

---

## Defects Found by Acceptance (14C Evidence)

| Defect | Evidence | Resolution |
| :--- | :--- | :--- |
| <D-01 description> | <RED evidence> | <GREEN fix> |

---

## Execution Evidence (14C)

| Run | Result |
| :--- | :--- |
| `mvn test -Pacceptance` | <n scenarios passed> |
| `mvn test` | <TDD suite green, Cucumber filtered out> |

---

## Traceability to Use Case Steps

| Scenario ID | UC Step | UCR Scenario | Domain Rule / Constraint | Notes |
| :--- | :--- | :--- | :--- | :--- |
| A-01 | <steps> | <main/extension> | <constraint> | <notes> |

---

## Execution Policy

- **Modo:** `mvn test -Pacceptance` o filtros `-Dcucumber.filter.tags=@tag`.
- **Requisito:** Docker Desktop en ejecución (Testcontainers PostgreSQL).
- El build por defecto (`mvn test`) excluye los escenarios Cucumber.
