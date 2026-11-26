# Step 0 — Glossary (on demand)

## Inputs
- Active schema instruction and template for the glossary.
- Existing master `Glossary`.
- The current draft or conversation where new domain terms appear.

## Output contract
- Add or refine terms in the master `Glossary`; never create a per-iteration glossary.
- Each term: name, definition, format (only for data elements), validation rules, aliases.
- Keep vocabulary aligned with the Use Case Model and the Domain Model.

## Preconditions
- `state.phase: elaboration`.
- Domain config and active schema resolved.

## Rubric
- Every new concept introduced by the iteration has a definition.
- Definitions are domain-level, not implementation-level.
- No synonyms without an alias entry; no duplicate terms.

## Evidence required
- Terms added or changed, with their definitions.
- Storage call by artifact id when the glossary is updated.

## Anti-patterns
- Creating a separate glossary per iteration.
- Defining software classes, tables or endpoints here.
- Leaving a term used by the iteration undefined.
