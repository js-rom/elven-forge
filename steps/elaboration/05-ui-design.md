# Step 5 — UI Design

## Inputs
- Use cases in scope, `System Sequence Diagrams`, `Operation Contracts`, `Supplementary Specification`, `Glossary`.
- For each significant state: screenshot or image, HTML mock with styles, and the design tokens used by that mock.
- Skill `ui-design` and its four-phase workflow.

## Output contract
- `Design System`: project-level tokens (color, typography, spacing, radius, elevation), component rules, breakpoints, accessibility.
- `Visual Specs`: one bundle per significant state (base, editing, loading, validation_error, server_error, success, empty, loaded) with mock, component states, layout and accessibility notes.
- `Interaction Spec`: interactive elements, transitions with from/to states, validations, success/error/loading paths, traceability to SSDs and Operation Contracts.
- `UI Technology Mapping`: structure, state-to-UI mapping, transitions, validation/Binder strategy, theming, accessibility and recommended class structure.

## Preconditions
- `OK 4` approved.
- Every UI state has an input asset; if an asset is missing, stop and ask.

## Rubric
- Every state in scope has a bundle; every transition has an id and a trace to SSD or contract.
- Accessibility constraints are explicit per state.
- The technology mapping does not invent components absent from the Design System.

## Evidence required
- Four gates in order: `OK 5.SYSTEM`, `OK 5.VISUAL`, `OK 5.INTERACTION`, `OK 5.VAADIN`.
- Final `OK 5` after all four.
- Asset paths per state.

## Anti-patterns
- Designing UI before the Design System is approved.
- Skipping error, empty or loading states.
- Writing Vaadin code in this step.
