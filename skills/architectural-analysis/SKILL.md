---
name: architectural-analysis
description: Analyze architectural factors from Vision, Use Case Model, and Supplementary Specification; produce FURPS+ factor tables and technical memo recommendations through a mandatory pair-programming workflow.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

## Purpose

Use architectural analysis to identify and prioritize the factors that most influence the architecture, then resolve them through explicit design decisions and rationale.

## Motivation

- Reduce the risk of missing architecturally significant concerns.
- Avoid spending excessive effort on low-priority issues.
- Align architecture with business goals and constraints.

## Required Inputs

- Vision
- Use Case Model
- Supplementary Specification

## Design Concern Routing (MUST)

- When the discussion moves from analysis to architecture design decisions, use [../architectural-design/SKILL.md](../architectural-design/SKILL.md) as the governing skill.
- Route concerns such as style selection, modularity/package rules, dependency governance, MVC variants, quality tactics, and architecture trade-offs to [../architectural-design/SKILL.md](../architectural-design/SKILL.md).
- Do not document 4+1 views in this skill; route 4+1 documentation concerns to [../software-architecture-document/SKILL.md](../software-architecture-document/SKILL.md).

## Core Concepts

- Variation point: Existing variability in requirements, integrations, or deployment contexts.
- Evolution point: Likely future variability not yet required now.

Both must be identified, prioritized, and addressed with proportionate architectural decisions.

## Mandatory Pair Programming Workflow

This skill must always run in pair-programming mode.

- Agent role: Driver.
- User role: Navigator.
- Cadence: The agent proposes one step, asks for confirmation/feedback, then proceeds.
- Rule: Do not skip directly to final recommendations without step-by-step checkpoints.

### Step-by-Step Execution

1. Confirm scope and objectives with the user.
2. Extract candidate architectural factors from input artifacts.
3. Classify factors by FURPS+ categories.
4. Define measurable quality scenarios for each relevant factor.
5. Build and review the factor table with the user.
6. Prioritize factors using the decision hierarchy.
7. Propose architectural decisions and alternatives, referencing [../architectural-design/SKILL.md](../architectural-design/SKILL.md) for design concerns.
8. Record rationale, trade-offs, and rejected alternatives.
9. Identify over-engineering and under-engineering risks.
10. Produce final outputs and request user sign-off.

## Typical Questions to Drive Analysis

- How do reliability and fault-tolerance requirements influence architecture?
- How do licensing and third-party component costs impact feasibility and profitability?
- How do adaptability and configurability requirements affect design boundaries?
- Which branding, market, or compliance constraints influence architectural choices?

## Factor Identification and Analysis Rules

- Analyze both functional and non-functional requirements with architectural impact.
- Use FURPS+ categories to ensure complete coverage.
- Focus especially on functionality, reliability, performance, supportability, implementation constraints, and interfaces.
- Ensure quality scenarios are testable and measurable.
- Select critical make-or-break scenarios first.
- Trace each factor to concrete source artifacts.

## Required Factor Table Format

Use this structure for each FURPS+ category:

| Factor | Measures and Quality Scenarios | Variability | Impact on Stakeholders and Other Factors | Priority for Success | Difficulty / Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <factor> | <measure + scenario> | <variation/evolution notes> | <stakeholder + cross-factor impact> | <critical/high/medium/low> | <high/medium/low + reason> |

## Decision Prioritization Hierarchy

1. Inflexible constraints (safety, legal, compliance).
2. Business goals (profitability, market impact, competitive advantage).
3. Other indirect business goals.

## Resolution Guidance

- Favor decisions that balance trade-offs and interdependencies explicitly.
- For architecture design concerns, follow [../architectural-design/SKILL.md](../architectural-design/SKILL.md).
- Apply foundational design principles:
  - Low coupling and high cohesion.
  - Protected variation (interfaces, indirection, service lookup).
  - Separation of concerns and localization of impact.
- Consider techniques such as modularization, decorators/interceptors, and AOP for cross-cutting concerns.
- Evaluate styles/patterns that fit prioritized factors (for example layered architecture, microservices).

## Technical Memo Rules

- Record notable alternatives, decisions, and motivations as Technical Memos.
- Include rationale for both accepted and rejected alternatives.
- A single Technical Memo may resolve multiple related factors.

## Under- vs Over-Engineering Checks

- Avoid over-engineering low-priority evolution points.
- Avoid under-engineering high-priority evolution points.
- Match solution effort to priority and risk.

## Outputs

- Architectural factor tables (grouped by FURPS+).
- Prioritized list of architecturally significant factors.
- Proposed decisions with trade-offs and rationale, including design-concern references to [../architectural-design/SKILL.md](../architectural-design/SKILL.md).
- Technical Memo recommendations (or drafts) for significant decisions.
