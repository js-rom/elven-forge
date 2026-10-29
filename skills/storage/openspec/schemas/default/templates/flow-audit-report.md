# Auditoria de Flujo de Elaboracion

<!-- BEGIN GENERATED:flow-audit -->

## Metodologia

- Fuente: `Flow Audit Ledger.json` y commits de git.
- Unidad: dias con al menos un commit asignado a un paso.
- Limite: en modo retrospectivo no hay timestamps de aprobacion.

## Cobertura

| Iteracion | Estado | Dias con commits | Pasos detectados | Dias con solape |
| :--- | :--- | ---: | ---: | ---: |
| {{iteration}} | {{status}} | {{commit_days}} | {{step_count}} | {{overlap_days}} |

## Resumen por iteracion

### {{iteration}}

- Dias con commits: {{commit_days}}.
- Pasos detectados: {{step_count}}.
- Dias con solape: {{overlap_days}}.
- Pasos con mas actividad: {{top_steps}}.

## Top pasos por actividad

| Iteracion | Paso | Nombre | Dias con commits | Commits | Span | Confianza |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- |
| {{iteration}} | {{step}} | {{step_name}} | {{commit_day_count}} | {{commit_count}} | {{span_days}} | {{confidence}} |

## Mapa de calor por fecha

| Iteracion | Paso | {{date}} |
| :--- | :--- | --- |
| {{iteration}} | {{step}} | {{cell}} |

## Hallazgos manuales

| Iteracion | Paso | Hallazgo | Impacto |
| :--- | :--- | :--- | :--- |
| {{iteration}} | {{step}} | {{finding}} | {{impact}} |

## Tooling y no clasificado

- Commits de tooling: {{tooling_count}}.
- Commits no clasificados: {{unclassified_count}}.

## Hipotesis de mejora

1. Reducir retrabajo tardio con validaciones automaticas antes de 14B/14D.
2. Congelar alcance tras PASO 15.
3. Reducir trabajo en paralelo y limitar WIP.
4. Automatizar state, schemas, espejos y diagramas.
5. Instrumentar timestamps por paso.

## Experimentos recomendados

| Experimento | Metrica | Esfuerzo |
| :--- | :--- | :--- |
| Preflight automatico antes de 14B/14D | Dias de 14D y defectos de conformidad | Medio |
| Congelacion de alcance tras PASO 15 | Dias de 16 y reaperturas | Bajo |
| Limite WIP: un paso activo | Dias con solape | Medio |
| Automatizar diagramas/estado/schemas | Dias de tooling | Bajo |
| Registrar timestamps por paso | Lead time y espera | Bajo |

<!-- END GENERATED:flow-audit -->
