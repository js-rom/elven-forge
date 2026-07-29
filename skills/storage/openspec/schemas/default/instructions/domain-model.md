# Domain Model Instructions

## Purpose
Create or update a Domain Model for the current iteration.

The Domain Model is a conceptual model of real-world domain concepts, not software classes.

## Required Inputs
- Iteration requirements (vision, supplementary specification, use cases).
- Existing Domain Model artifact (if it exists).
- Existing glossary/domain rules (if available).

## Mandatory Workflow (Pair Programming)
The agent MUST execute this exact principal flow and MUST NOT reorder or skip steps unless the user explicitly requests it.

1. Find conceptual classes.
2. Draw conceptual classes in UML class diagram(s).
3. Add attributes and associations.

### Execution Mode (MANDATORY)
- Agent role: Driver.
- User role: Navigator.
- At each step, the agent proposes and applies concrete changes, then asks/records navigator feedback before moving to the next step.

## Modeling Rules (MUST / MUST NOT)

### Core Rules
- MUST model domain concepts, vocabulary, and information content.
- MUST NOT model software responsibilities, methods, APIs, or technical object links.
- MUST use domain language used by business stakeholders.
- MUST exclude out-of-scope concepts for the current iteration.
- MUST avoid inventing concepts not present in the source requirements.

### Class and Attribute Rules
- MUST prefer conceptual classes over attributes when the concept is meaningful on its own.
- SHOULD keep text/number values as attributes only when they are simple scalar values.
- MUST represent derived attributes with `/` prefix.
- MUST keep UML attributes with private visibility `-` unless otherwise justified.
- MUST use associations (not attributes) to relate conceptual classes.

### Description Class Rule
Use a description class when one or more are true:
- Information must exist independently of concrete instances.
- Deleting concrete instances would lose important information.
- It removes duplicated information.

## Sub-domain Decomposition Rules
- MUST use one package when the domain is small.
- MUST split into sub-domains when the domain is large.
- If the domain is large, MUST include a general model in the first section that contains all major concepts and cross-subdomain relationships.
- MUST create one UML class diagram per sub-domain.
- Sub-domain diagrams MUST appear in the following sections, after the general model.

For each sub-domain diagram:
- MUST keep local classes inside the sub-domain package.
- MUST place cross-sub-domain associations outside the local package.
- MUST reference external classes using this exact prefix format (line break before the dot):

```text
SubdomainName
.ClassName
```

- MUST NOT place cross-sub-domain target classes inside the local package.

## Association Rules
- SHOULD include only need-to-remember associations.
- SHOULD avoid excessive associations.
- MUST use meaningful association names with `ClassName-VerbPhrase-ClassName` intent.
- SHOULD use multiplicities to express domain constraints.

Allowed multiplicity examples:
- `0`
- `0..1`
- `1`
- `*`
- `0..*`
- `1..*`
- `3`
- `1..40`
- `3, 5, 8`

## Concept Discovery Techniques (MUST use both)
1. Category list analysis.
2. Noun phrase identification from requirements text.

### Category List (quick reference)
Consider concepts in categories such as:
- business transactions
- transaction line items
- products/services in transactions
- records/ledgers/manifests
- actor roles and organizations
- places
- noteworthy events
- physical/logical objects
- descriptions/catalogs
- containers and contained things
- collaborating external systems
- legal/contract/work records
- financial instruments
- schedules/manuals/documents

## Anti-Patterns (MUST avoid)
- Modeling software classes or architecture elements instead of domain concepts.
- Modeling implementation links (database FK, object references, data flow links) as domain associations.

## Output Contract (MUST)
The produced artifact MUST:
- Use PlantUML class diagram syntax.
- Contain no method signatures.
- Follow the 3-step workflow result (classes, then structure, then relationships).
- If large domain: include a global/general diagram first.
- Include sub-domain diagrams when applicable.
- If large domain: place sub-domain diagrams after the global/general diagram.
- Follow the external class prefix format exactly for cross-sub-domain links.

## Validation Checklist (MUST run before finish)
1. Did I use both concept discovery techniques?
2. Are all classes conceptual (non-software)?
3. Are methods absent from all classes?
4. Are out-of-scope concepts excluded?
5. If large domain: is there a global/general diagram in the first section?
6. If large domain: is there one diagram per sub-domain in later sections?
7. Are cross-sub-domain associations outside local packages?
8. Do all external class references use:

```text
SubdomainName
.ClassName
```

9. Are multiplicities and association names meaningful?
10. Are derived attributes marked with `/` when needed?
11. Is the model traceable to current iteration requirements?