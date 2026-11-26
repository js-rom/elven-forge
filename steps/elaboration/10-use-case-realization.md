# Step 10 — Use Case Realization

## Inputs
- `Domain-to-Design Transition Map` from 9A.
- `Design Sequence Diagram` and `Logical View Class Diagram` from 9B.
- `System Sequence Diagrams`, `Operation Contracts`, `Supplementary Specification`, `Glossary`.
- Skill `design-principles`.

## Output contract
- One `Use Case Realization` per use case in scope, with:
  - scenario mapping table: UC step -> SSD -> Operation Contract -> design reference from 9A/9B;
  - references to the design diagrams and transition map, never recreated;
  - postcondition satisfaction checklist, cross-referenced with the 9A matrix;
  - alignment with Supplementary Specification and Glossary;
  - design rationale already produced in 9B.
- Diagram export is mandatory before assembling: run `export-plantuml-svg.ps1`.
- Every diagram reference is an embedded image `![](relative-path-to-out-svg)`.
  Exception: the "Inputs and References" lists keep plain text links to the `.plantuml` sources.
- Links to `.md` documents remain plain text links.

## Preconditions
- `OK 9B` approved.
- SVGs for every referenced diagram exist under `out/`.

## Rubric
- No new classes, responsibilities, packages or interactions.
- Every diagram link resolves to an existing exported SVG.
- Every in-scope postcondition appears in the checklist.

## Evidence required
- Export command output; missing SVGs = 0.
- Scenario mapping table per use case.
- `OK 10` request.

## Anti-patterns
- Recreating or editing diagrams in this step.
- Adding design elements that were not approved in 9A/9B.
- Linking `.plantuml` sources where an embedded SVG is required.
