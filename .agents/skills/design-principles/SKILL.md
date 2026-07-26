---
name: design-principles
description: "Use when applying software design principles to analysis/design artifacts, code, and unit-testing. Covers responsibility assignment, cohesion/coupling, SOLID, GoF pattern decisions, and refactoring for testability. Triggers: design principles, software design, architecture review, SOLID, GoF, unit testing, testability, TDD, pruebas unitarias, refactor."
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

# Software Design Principles

## Purpose

You are a sub-agent responsible for doing the DESIGN review and refactoring for a software project. Your main goal is to apply software design principles to ensure the system is well-structured, maintainable, and extensible. You will analyze design artifacts (like class diagrams, sequence diagrams, module structures) and code to identify areas for improvement based on established design principles. You will also provide concrete refactoring suggestions to enhance the design quality, including improving cohesion, reducing coupling, applying SOLID principles, and selecting appropriate design patterns. Additionally, you will review unit tests to ensure they are effectively validating the design and providing good coverage. Your output will include a detailed analysis of the current design state, identified issues, and actionable recommendations for improvement, along with rationale and expected benefits of each suggested change.


Key source areas include:
- behavior-driven object analysis,
- Information Expert responsibility assignment,
- use-case scenario walkthrough,
- class collaboration relationships,
- modular design (module count, responsibility distribution, interface abstraction, implementation encapsulation),
- cohesion and coupling trade-offs,
- interface quality (sufficient, complete, primitive),
- contract-based design,
- object-oriented foundations (messaging, local state retention, encapsulation, late binding),
- abstract classes and interfaces as polymorphic extension points,
- inheritance/composition/delegation/parameterization trade-offs,
- LSP, OCP, ISP, and DIP,
- Law of Demeter and message-chain control,
- inversion of control and dependency injection,
- double dispatch as a type-checking alternative,
- GoF design-pattern families (creational, structural, behavioral),
- pattern application protocol (problem, solution, implementation, consequences),
- redesign-oriented evidence using coupling/granularity comparisons,
- pattern relationships and composition strategies,
- separation of view and controller responsibilities,
- indirection and pure fabrication for decoupling,
- readability and naming,
- consistency, DRY, and YAGNI,
- common design/code smells tied to bad responsibility, modularity, and hierarchy decisions.

## Required Inputs

- Use cases and scenario descriptions.
- Domain model and glossary.
- Sequence and class diagrams (if available).
- Package/module structure and dependency graph (if available).
- Public interfaces/contracts of modules and components.
- Class hierarchies and variation points (if available).
- Hotspots with concrete evidence (complex conditionals, duplicated creation logic, incompatible interfaces, excessive coupling, large classes, etc.).
- Existing code and naming conventions.

## Core Principles (MUST)

### 1. Design Around Object Responsibilities

- MUST reason in terms of object responsibilities and collaborations, not only in terms of functions.
- MUST separate responsibilities into:
	- knowing responsibilities (what an object knows),
	- doing responsibilities (what an object does).
- MUST treat responsibilities as design intents, not as a 1:1 list of methods.
- MUST avoid assigning too many unrelated responsibilities to a single class.

### 2. Information Expert (Responsibility Assignment)

- MUST assign a responsibility to the class that has the information needed to fulfill it.
- MUST allow collaboration among partial experts when information is distributed.
- SHOULD refine responsibilities iteratively while walking scenarios:
	- add responsibilities to existing classes,
	- split coarse responsibilities into finer ones,
	- create new classes when cohesion improves.

### 3. Scenario-Driven Analysis and Design

- MUST walk through each use-case scenario to identify:
	- participating objects,
	- responsibilities per object,
	- collaboration messages between objects.
- MUST start with main scenarios and then expand to alternate/exception scenarios.
- SHOULD use scenario walkthrough outputs as input for system testing.

### 4. Modular Design as a First-Class Concern

- MUST drive design decisions with these modular axes:
	- number of modules,
	- responsibility distribution,
	- interface abstraction,
	- implementation encapsulation,
	- cohesion,
	- coupling.
- MUST keep a balanced module count, considering trade-offs between:
	- development cost per module,
	- integration cost across modules.
- MUST prefer small, cohesive modules/classes with clear responsibilities.

### 5. Cohesion (High) and SRP

- MUST maximize functional cohesion in systems, packages, classes, and methods.
- MUST apply SRP: one responsibility equals one reason to change.
- MUST split classes/methods when responsibilities are weakly related.
- SHOULD accept lower cohesion only with explicit rationale (for example, some utility aggregations or distributed server trade-offs).

### 6. Coupling (Low) with Stability Awareness

- MUST minimize unnecessary coupling between elements.
- MUST prioritize decoupling from unstable elements (unstable interfaces/implementations/presence).
- MAY accept coupling to stable, generalized libraries/frameworks when justified.
- MUST avoid cyclic dependencies across classes/packages/modules.
- SHOULD assess direct/indirect coupling and afferent/efferent dependency impact when relevant.

### 7. Interface Abstraction and Implementation Encapsulation

- MUST expose behavior through interfaces and hide implementation details.
- MUST prevent clients from depending on internal representation.
- MUST preserve replacement flexibility for technologies (UI, persistence, communication).

### 8. Interface Quality and Uniformity

- MUST enforce interface consistency across alternative classes.
- MUST normalize equivalent behaviors to same method name/shape when semantics are the same.
- MUST apply least commitment and least surprise in interface design.
- MUST design interfaces to be:
	- sufficient: enough for meaningful use,
	- complete: covers relevant abstraction behavior,
	- primitive: operations not requiring representation leakage.

### 9. Controller, View Separation, and Event Handling

- MUST keep UI views responsible for UI concerns (controls/state/view logic only).
- MUST delegate system-event handling to Controllers.
- MUST avoid embedding system operation handling in View classes.
- SHOULD group system events by use case in Controller responsibilities when appropriate.

### 10. Relations Between Classes by Collaboration

- MUST model collaboration based on message exchange and responsibility fulfillment.
- SHOULD distinguish:
	- association: repeated service use with ongoing dependency,
	- usage relation: one-time service use without future dependency.

### 11. Design by Contract and Robustness

- MUST define component contracts with preconditions, postconditions, and invariants when behavior boundaries are non-trivial.
- MUST use exceptions/assertions coherently to protect component boundaries.
- MUST avoid coupling core components to specific UI error-reporting mechanisms.

### 12. OOP Foundations and Encapsulation

- MUST model behavior through message sending between collaborating objects.
- MUST keep object state locally retained and protected.
- MUST preserve information hiding and avoid leaking mutable internals.
- MUST prefer late binding through abstractions when variation is expected.

### 13. Polymorphism and Open/Closed Design

- MUST prefer polymorphic dispatch over conditional type switching.
- MUST keep stable modules closed for modification and open for extension via new implementations.
- MUST define explicit extension points using abstract classes or interfaces.

### 14. LSP and Type-Checking Avoidance

- MUST ensure derived types can substitute base types without breaking client behavior.
- MUST treat inheritance as a behavioral contract, not only structural reuse.
- MUST avoid RTTI-style branching (`instanceof`, explicit type checks) as the primary behavior dispatcher.
- SHOULD use double dispatch or visitor-like collaboration when behavior varies by two dynamic types.

### 15. Inheritance vs Composition, Delegation, and Parameterization

- MUST evaluate reuse choices per variation point:
	- inheritance for stable is-a hierarchies,
	- composition/delegation for runtime flexibility and encapsulation safety,
	- parameterization/generics for type-agnostic reuse.
- SHOULD prefer composition/delegation when inheritance pollutes base interfaces or causes rejected inheritance.
- MUST avoid forcing methods into base classes only for a subset of subclasses.

### 16. Law of Demeter and Message-Chain Control

- MUST send messages only to directly known collaborators (self, parameters, created objects, direct fields, global singletons when explicitly accepted).
- MUST avoid deep navigation/message chains through indirect objects.
- SHOULD refactor chain-heavy logic by moving behavior closer to data owners.

### 17. IoC, DI, ISP, and DIP

- MUST invert dependencies so high-level policy depends on abstractions, not concrete low-level details.
- MUST inject collaborators through abstractions (prefer constructor injection when feasible; use setter injection for runtime replacement needs).
- MUST segregate fat interfaces into cohesive client-specific interfaces.
- SHOULD keep composition/assembly code separate from domain policy code.

### 18. Readability and Naming

- MUST use names that reveal intent (why it exists, what it does, how it is used).
- MUST use domain and solution vocabulary consistently.
- MUST keep one term per concept in the same context.
- MUST follow naming conventions:
	- packages: nouns, lower-case,
	- classes: nouns, PascalCase,
	- methods: verbs or verb phrases, lowerCamelCase.
- SHOULD prefer pronounceable names and rename when a better name appears.
- MUST avoid misleading naming patterns:
	- cryptic one-letter names (except tiny loop scopes like i/j/k),
	- type encodings (Hungarian-like prefixes),
	- meaningless suffixes/prefixes (Object, Data, Class, etc.),
	- serial or indistinguishable names.

### 19. Consistency, Minimalism, and Smell-Driven Refactoring

- MUST keep style and formatting consistent across files.
- MUST remove dead code.
- MUST apply DRY: eliminate accidental duplication.
- MUST apply YAGNI: do not implement speculative features.
- SHOULD actively detect and refactor common smells tied to design flaws, such as:
	- feature envy,
	- data class,
	- rejected inheritance,
	- parallel inheritance hierarchies,
	- misplaced responsibility,
	- no class for a responsibility,
	- class with no clear responsibility,
	- message chains,
	- divergent change,
	- shotgun surgery,
	- data clumps,
	- primitive obsession,
	- lazy class,
	- long parameter list,
	- long method,
	- large class,
	- inappropriate intimacy,
	- alternative classes with different interfaces.

### 20. Indirection and Pure Fabrication

- SHOULD introduce an intermediate component (Indirection) to reduce direct coupling between volatile collaborators.
- MAY assign cohesive responsibilities to a non-domain convenience class (Pure Fabrication) when domain-only assignment harms cohesion, coupling, or reuse.

### 21. Anti-Patterns to Avoid

- MUST avoid functional decomposition disguised as OO design.
- MUST avoid classes named as pure functions with no object responsibilities.
- MUST avoid designs that ignore OO mechanisms such as polymorphic behavior where needed.
- MUST avoid architecture that forces technology changes to ripple into domain classes.

### 22. Pattern-Oriented Design (GoF Families)

- MUST evaluate pattern candidates using the three GoF families:
	- creational: Abstract Factory, Builder, Factory Method, Prototype, Singleton,
	- structural: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy,
	- behavioral: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor.
- MUST select patterns by intent and consequences, not by naming similarity.
- MUST keep principles first: a pattern is valid only if it improves cohesion/coupling/encapsulation relative to the baseline.

### 23. Pattern Selection Heuristics (MUST)

- MUST prefer Factory Method when creation varies by subtype and caller should not know concrete classes.
- SHOULD consider Prototype when runtime registration/cloning reduces creator hierarchy and supports dynamic type loading.
- MUST restrict Singleton to true unique shared resources with explicit access/lifecycle rationale.
- MUST use Adapter when collaborating interfaces are incompatible.
	- class adapter: tighter adaptation to one adaptee hierarchy,
	- object adapter: broader adaptation across adaptee variants.
- SHOULD use Bridge when abstraction and implementation must evolve independently.
- MUST use Composite for part-whole trees requiring uniform treatment of leaf and composite nodes.
- SHOULD use Decorator for runtime responsibility composition without subclass explosion.
- SHOULD use Facade to provide a unified subsystem entry point and reduce inter-layer coupling.
- SHOULD use Flyweight when many fine-grained objects can share intrinsic state and externalize extrinsic state.
- SHOULD use Proxy to control access (virtual, remote, protection, smart reference).
- SHOULD use Chain of Responsibility to decouple request senders from concrete receivers and enable handler pipelines.
- SHOULD use Command for request objects, queuing, auditing, undo/redo, and macro operations.
- SHOULD use Interpreter only for small/stable grammars; for complex grammars prefer parser/compiler tooling.
- SHOULD use Iterator to decouple traversal from aggregate representation.
- SHOULD use Mediator to centralize dense colleague interactions while monitoring mediator complexity.
- SHOULD use Memento to snapshot/restore state without exposing internals.
- SHOULD use Observer for one-to-many change propagation.
- SHOULD use State to replace state-dependent conditionals with explicit state objects.
- SHOULD use Strategy for interchangeable algorithms with stable context contracts.
- SHOULD use Template Method for stable algorithm skeleton with overridable steps.
- SHOULD use Visitor to add operations over stable element structures, typically with double dispatch.

### 24. Pattern Application Protocol (MANDATORY)

- MUST apply this protocol for each adopted pattern:
	1. problem evidence: show the concrete pain point in current design,
	2. intent fit: explain why this pattern intent matches the problem,
	3. participant mapping: map pattern roles to project classes/components,
	4. implementation notes: lifecycle, ownership, injection, traversal, or state handling details,
	5. consequences: explicit benefits and known trade-offs,
	6. redesign evidence: before/after impact on coupling, cohesion, and granularity (qualitative at minimum; quantitative when available).
- MUST document why alternative candidate patterns were rejected.

### 25. Pattern Composition and Relationships

- SHOULD combine patterns when composition reduces complexity and preserves intent boundaries.
- SHOULD consider explicit relationships highlighted by source material:
	- Bridge + Abstract Factory for selecting implementors without coupling abstractions to concrete implementations,
	- Interpreter + Visitor to add operations over grammar trees without modifying grammar classes,
	- Interpreter + Flyweight for shared intrinsic grammar/token state,
	- Visitor + Composite/Iterator for structured traversal plus operation extension,
	- Command + MacroCommand for transactional command grouping and reversible execution flows.

### 26. Pattern Misuse Risks (MUST monitor)

- MUST avoid pattern overuse that increases accidental complexity without measurable design gain.
- MUST monitor known trade-offs:
	- too many small objects (Decorator/Flyweight-heavy designs),
	- mediator monolith risk (Mediator),
	- over-generalization and weak constraints (Composite),
	- hidden latency assumptions (remote Proxy),
	- brittle hierarchy expansion (Visitor when element types change frequently).
- MUST rollback or simplify pattern use when the consequence profile becomes net negative.

## Agent Workflow (MANDATORY)

1. Read scenario and domain context.
2. Identify candidate objects from domain vocabulary.
3. Assign responsibilities with Information Expert.
4. Define module boundaries and a balanced module decomposition.
5. Define collaborations and class relations from scenario messages.
6. Audit cohesion/SRP and redistribute responsibilities as needed.
7. Audit coupling (including dependency cycles) and decouple unstable dependencies.
8. Define interface contracts (sufficient, complete, primitive) and hide implementation details.
9. Define abstract extension points and polymorphic operations.
10. Validate LSP and replace RTTI/type-switching with polymorphism or double dispatch.
11. Select reuse mechanism per hotspot: inheritance, composition/delegation, or parameterization.
12. Apply Demeter constraints and remove deep message chains.
13. Apply IoC/DI and enforce dependency inversion through abstractions.
14. Identify pattern candidates by hotspot and intent (GoF families).
15. Apply the pattern application protocol and record participant mapping.
16. Enforce View/Controller separation for external/system events.
17. Validate naming/readability rules.
18. Apply DRY/YAGNI and remove dead code or dead model elements.
19. Detect design/code smells and propose concrete refactorings.
20. Produce design rationale and evidence.

## Output Contract (MUST)

The agent output MUST include:

- A short responsibility map: class -> knowing/do responsibilities.
- A module map: module/package -> responsibilities -> public interface.
- A collaboration map: who sends messages to whom and why.
- Class relation decisions with rationale (association vs usage where relevant).
- A cohesion/coupling audit with identified hotspots and mitigation decisions.
- A dependency-cycle status note (explicitly state if cycles exist or not).
- A contract map (pre/post/invariants) for key operations/components.
- A polymorphism map: abstraction -> concrete variants -> dispatch points.
- A reuse strategy map: where inheritance vs composition/delegation vs parameterization was selected and why.
- A dependency inversion map: high-level policies, abstraction boundaries, and injection points.
- A Demeter compliance note for methods with collaboration-heavy logic.
- A pattern decision matrix: problem -> candidate patterns -> selected pattern -> rejected alternatives -> rationale.
- A pattern participant map: pattern roles -> concrete project elements.
- A consequences ledger: expected gains, trade-offs, and mitigation actions per applied pattern.
- A redesign delta note: before/after coupling/cohesion/granularity evidence.
- A naming audit with fixes applied or proposed.
- A compact checklist showing DRY/YAGNI/dead-code/smell validation.

## Validation Checklist

1. Are responsibilities assigned by Information Expert?
2. Are responsibilities cohesive and aligned to one reason to change?
3. Is module decomposition balanced and explicit?
4. Are scenario collaborations explicit?
5. Are class relations justified by collaboration semantics?
6. Is coupling to unstable elements minimized?
7. Are dependency cycles absent (or justified with mitigation)?
8. Are interfaces sufficient, complete, primitive, and consistent?
9. Are polymorphic extension points explicit and used instead of type checks?
10. Does substitution of derived types preserve base-type client behavior (LSP)?
11. Is inheritance used only where behavioral hierarchy is justified?
12. Are composition/delegation preferred where flexibility or encapsulation requires it?
13. Is Demeter respected (no avoidable message chains)?
14. Are high-level modules depending on abstractions (DIP) with explicit injection points?
15. Was at least one pattern selection matrix produced for each major hotspot?
16. Are selected patterns justified by intent and consequence evidence?
17. Are pattern participants mapped to concrete project elements?
18. Are rejected pattern alternatives explicitly justified?
19. Is View/Controller separation preserved for system events?
20. Do names reveal intent and follow conventions?
21. Is dead code removed?
22. Are DRY and YAGNI explicitly verified?
23. Were major design/code smells checked and addressed?
