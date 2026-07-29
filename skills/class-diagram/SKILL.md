---
name: class-diagram
description: Create UML class diagrams in PlantUML to model static structure with classifiers, members, and relationships
metadata:
  author: js-rom
  version: "1.0"
---

## Purpose

Create UML class diagrams in PlantUML to model static structure: classifiers, members, and relationships. Keep the diagram aligned with domain language and readable for analysis/design.

## Required inputs

- Domain concepts to model (entities, roles, services, rules)
- Candidate attributes and operations per classifier
- Relationship semantics (inheritance, composition, dependency, multiplicities, roles)
- Collaboration context between objects (visibility, temporality, versatility)

## Design Concern Routing

- Use [../design-principles/SKILL.md](../design-principles/SKILL.md) for design decisions and rationale.
- Use this skill to realize those decisions into logical-view structure and diagrams.

## Mandatory workflow (Driver/Navigator)

1. List classifiers and choose the correct type (class, interface, enum, etc.)
2. **Separate classifiers into two groups:**
   - **Internal**: those belonging to the package being modeled — declare them INSIDE the `package { }` block.
   - **External**: those belonging to other packages — declare them OUTSIDE the `package { }` block using the `class OuterClass as "externalPackage\n.OuterClass"` pattern.
3. Define members (attributes/operations) and visibility when relevant
4. Add structural relationships in this order:
   - **Internal-only relationships** (both ends inside the same package): place them INSIDE the `package { }` block.
   - **Cross-package relationships** (one end internal, the other external): place them OUTSIDE the `package { }` block, right after the external class declarations, using qualified names for internal classes (e.g., `domain.JornadaDiaria`) and alias names for external classes.
5. Decorate relationships with multiplicities, roles, and direction
6. Run a final readability pass (remove noise, keep domain terminology)

## Execution rules (MUST / MUST NOT)

- MUST use PlantUML class diagram syntax
- MUST choose the correct classifier keyword for each concept
- MUST use `class ClassName <<record>>` for Java records — the `record` keyword is NOT valid in PlantUML
- MUST use relationship types that match meaning (inheritance is not dependency)
- MUST choose relationships using collaboration context: visibility, temporality, and versatility
- MUST keep names and labels in domain language
- MUST add multiplicities when cardinality is relevant
- MUST NOT force layout as the primary objective (PlantUML autolayout first)
- MUST NOT add implementation detail (SQL, internal framework concerns) at analysis level
- MUST NOT overload the diagram with unnecessary members or decorative relationships
- MUST NOT declare external classes (from other packages) inside the `package { }` block — they must be declared outside with the `class OuterClass as "externalPackage\n.OuterClass"` pattern
- MUST place cross-package relationships (between internal and external classes) OUTSIDE the `package { }` block, immediately after the external class declarations
- MUST use left-to-right direction for generalization/realization arrows: `<|--` and `<|..` (NOT `--|>` or `..|>`). The parent/interface always appears on the left side of the arrow, the child/implementation on the right.

## Per-Package Diagram Rule (MANDATORY)

- MUST create ONE class diagram PER package being modeled
- Each diagram file MUST be named: `<fully.qualified.package>.classDiagram.plantuml`
- Cross-references to external classes MUST use fully qualified class aliases (no package nesting), e.g: `class OuterClass as "externalPackage\n.OuterClass"`
- MUST show collaborations/dependencies to external classes used by classes in this package

## Package Cross-references syntax

Use package with alias to keep names concise. **Internal-only relationships stay inside the `package { }` block. Cross-package relationships go OUTSIDE, after the external class declarations:**

```plantuml
package currentPackageNotQualified as "currentPackageQualified" {
    class InnerClassA {
        - attribute
        + operation()
    }
    class InnerClassB {
        + anotherOperation()
    }

    currentPackageNotQualified.InnerClassA --> currentPackageNotQualified.InnerClassB
}

class OuterClass as "externalPackage\n.OuterClass"
currentPackageNotQualified.InnerClassA --> OuterClass
```

- Package member name: only the last node of the path (e.g., `domain`)
- Alias: use only relevant path, not full classpath (e.g.,  `as fichaje.domain`)

## Member syntax

Use class blocks for attributes and operations.

```plantuml
class ClassName {
	type attribute
	untypedAttribute
	{static} staticAttribute

	- privateAttribute
	# protectedAttribute
	~ packageAttribute
	+ publicAttribute

	returnType method(paramType parameter) Exception
	{static} staticMethod()
	{abstract} abstractMethod()

	- privateMethod()
	# protectedMethod()
	~ packageMethod()
	+ publicMethod()
}
```

Visibility markers:

- `+` public
- `-` private
- `#` protected
- `~` package

## Relationship syntax

Use connector semantics intentionally:

- Generalization: `Base <|- Derived`
- Realization: `Base <|. Implementation`
- Composition: `Whole *-- Part`
- Aggregation: `Whole o-- Part`
- Association: `ClassA -- ClassB`
- Dependency/usage: `ClassA ..> ClassB`

Direction hints to improve readability:

- `-up-`, `-down-`, `-left-`, `-right-`

Multiplicities and role:

```plantuml
Source "1..*" -right-> "7" Target : role >
```

Association-class style (when needed):

```plantuml
class Buyer
class Seller
class Purchase

Buyer "0..*" -- "1..*" Seller
(Buyer, Seller) .. Purchase
```

## Relationship selection guide

### 1) Decide relationship family first

- Collaboration relationships: composition/aggregation, association, dependency
- Transmission relationships: generalization/realization

Use transmission only when you truly model a type hierarchy (`is-a`) or a contract implementation.

### 2) Collaboration criteria

Evaluate these three criteria in the specific context:

- Visibility: is the collaboration private to one object, or public/shared with others?
- Temporality: is collaboration long-lived or momentary?
- Versatility: is collaborator interchangeable (many possible providers) or fixed/specific?

Context is decisive. There is no universal categorical choice for every domain.

### 3) Decision matrix for collaboration

| Relationship | Choose it when... | Typical signals | PlantUML |
| --- | --- | --- | --- |
| Composition | It is a strong whole-part ownership relation | Private visibility, high temporality, low versatility; part lifecycle tied to whole; parts not shared | `Whole *-- Part` |
| Aggregation | It is a weak whole-part relation | Public visibility, high/medium temporality, low versatility; part can outlive whole; parts can be shared | `Whole o-- Part` |
| Association | A client keeps a stable link to a specific server over time | Public visibility, high/medium temporality, low versatility; repeated use of same collaborator | `Client -- Server` |
| Dependency/Usage | A client uses any server momentarily | Public/private visibility, low temporality, high versatility; parameter/local-variable collaboration | `Client ..> Server` |

### 4) Decision matrix for transmission

| Relationship | Choose it when... | PlantUML |
| --- | --- | --- |
| Generalization | Subtype preserves and specializes base behavior (polymorphic substitution expected) | `Base <|- Derived` |
| Realization | A concrete type implements an interface/contract | `Contract <|. Implementation` |

Avoid these inheritance mistakes:

- Inheritance by limitation: subclass cannot support full base behavior
- Inheritance by construction: relation is actually composition, not inheritance

### 5) Practical selection order

1. Ask `is-a` or `implements` first. If yes, use generalization/realization
2. If not, ask `whole-part`
3. If whole-part: choose composition vs aggregation by lifecycle and sharing
4. If not whole-part: choose association vs dependency by duration and collaborator interchangeability

## Output contract

The generated output MUST include:

- One PlantUML block with `@startuml` and `@enduml`
- Correct classifier declarations
- Members only when they add modeling value
- Relationships with correct semantics
- Multiplicities/roles only when meaningful

## Minimal template

```plantuml
@startuml
allow_mixing

class Sale {
	+date
	+total()
}

class SaleLine {
	+quantity
}

interface SalesRepository

Sale "1" *-- "1..*" SaleLine : lines
Sale ..> SalesRepository : save()

@enduml
```

## Validation checklist

1. Are classifier types correctly chosen?
2. Are visibility/static/abstract markers used correctly?
3. **Are all external classes declared OUTSIDE the `package { }` block with the correct cross-reference alias pattern?**
4. Does each relationship express the intended meaning?
5. Are multiplicities and roles consistent with domain rules?
6. Was relationship choice justified by visibility, temporality, and versatility?
7. Are inheritance links real transmission (`is-a`/`implements`) and not disguised composition?
8. Is the diagram readable without layout micromanagement?
9. Was implementation noise avoided?