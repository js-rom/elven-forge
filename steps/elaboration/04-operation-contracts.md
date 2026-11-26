# Step 4 — Operation Contracts

## Inputs
- `System Sequence Diagrams` for the scenarios in scope.
- `Domain Model`, `Use Case Model`, `Glossary` and `Supplementary Specification`.
- Active schema instruction and template for operation contracts.

## Output contract
- One contract per system operation in scope: operation signature, cross-reference to its SSD, preconditions and postconditions.
- Postconditions are written in domain vocabulary and describe observable state changes.
- Exceptions and alternate outcomes are listed when the scenario defines them.
- If discoveries change Vision, Use Case Model, Supplementary Specification, Glossary or risks, update them in the same collaboration and persist them with the approval.

## Preconditions
- `OK 3` approved.
- Every operation name comes from an approved SSD.

## Rubric
- Every postcondition is verifiable by a test or an inspection.
- No design decisions: no classes, tables, endpoints or SQL.
- Every SSD system operation has exactly one contract.

## Evidence required
- Operation list with postcondition counts.
- Conflicts between SSD and contract resolved or flagged.
- `OK 4` request.

## Anti-patterns
- Writing postconditions as database or UI operations.
- Inventing operations not present in the SSD.
- Leaving an operation without a postcondition.
