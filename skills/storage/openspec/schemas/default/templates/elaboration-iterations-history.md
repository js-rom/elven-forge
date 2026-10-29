# Histórico de Iteraciones de Elaboración

<!-- BEGIN GENERATED:iteration-history -->

## Metodología

- **Fuente de verdad:** `Elaboration Iterations Ledger.json`.
- **Días transcurridos:** días naturales inclusivos entre inicio y fin reales.
- **Días efectivos:** fechas únicas con al menos un commit dentro de `start_ref..end_ref`, usando fecha de autor.
- **Rango de commits:** solo commits alcanzables desde `end_ref`; no se usa `git log --all`.
- **Media por UC:** solo iteraciones de confianza alta y UCs `full` o `slice`; se excluyen refactors y soporte.
- **Zona horaria:** {{timezone}}.

## Iteraciones

| Iteración | Inicio | Fin | Días | Días efectivos | Casos de uso | Estado | Confianza | ¿Computa media? |
| :--- | :--- | :--- | ---: | ---: | :--- | :--- | :--- | :--- |
| {{iteration}} | {{start}} | {{end}} | {{calendar_days}} | {{effective_days}} | {{use_cases}} | {{status}} | {{confidence}} | {{include_in_average}} |

## Planificado frente a real

| Iteración | Fin planificado | Fin real | Desviación |
| :--- | :--- | :--- | :--- |
| {{iteration}} | {{planned_end}} | {{end}} | {{deviation}} |

## Evidencia git

| Iteración | start_ref | end_ref | Commits | Días efectivos | Fechas con commit |
| :--- | :--- | :--- | ---: | ---: | :--- |
| {{iteration}} | {{start_ref}} | {{end_ref}} | {{commit_count}} | {{effective_days}} | {{commit_days}} |

## Media de días efectivos por caso de uso

| Iteración | Días efectivos | UCs computados | Días efectivos / UC |
| :--- | ---: | :--- | ---: |
| {{iteration}} | {{effective_days}} | {{use_cases}} | {{days_per_uc}} |
| **Total** | **{{total_days}}** | **{{total_ucs}}** | **{{average}}** |

**Media: {{average}} días efectivos por caso de uso** (`{{total_days}} / {{total_ucs}}`).

## Datos excluidos de la media

| Iteración | Confianza | Motivo |
| :--- | :--- | :--- |
| {{iteration}} | {{confidence}} | {{excluded_reason}} |

## Notas

- {{note}}

<!-- END GENERATED:iteration-history -->

_Actualizado: {{last_updated}}._
