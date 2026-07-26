# Supplementary Specification

## Purpose

Captures and identifies all requirements that are **not** expressed in the use cases. This includes non-functional requirements, quality attributes, constraints, and other system-wide concerns. It is the primary artifact for recording FURPS+ requirements in the Unified Process.

## Role in the Unified Process

The Supplementary Specification complements the use cases. While use cases capture functional, actor-goal-driven behavior, the Supplementary Specification captures:

- **Cross-cutting functional requirements** that apply to many use cases (e.g., logging, security, error handling).
- **Quality attribute requirements** (reliability, performance, usability, supportability).
- **Constraints** on implementation, components, interfaces, and legal matters.
- **Domain rules** and business rules that do not fit naturally inside a single use case.

It is produced starting in the **Inception phase** and refined throughout **Elaboration**.

## FURPS+ Model

Organize requirements using the **FURPS+** model:

- **F — Functionality:** Cross-cutting functional requirements not captured in use cases (e.g., authentication, logging, auditing, pluggable rules).
- **U — Usability:** Human factors, aesthetics, consistency, documentation needs.
- **R — Reliability:** Frequency of failure, recoverability, predictability, data integrity.
- **P — Performance:** Response time, throughput, capacity, resource usage.
- **S — Supportability:** Testability, adaptability, maintainability, configurability, internationalization.
- **+ — Extensions:**
  - **Implementation Constraints:** Programming languages, platforms, tools, standards mandated.
  - **Purchased / Third-Party Components:** External libraries, services, or packages required.
  - **Free Open Source Components:** FOSS candidates to be used.
  - **Interfaces:** Hardware devices, external software systems, and communication protocols.
  - **Application-Specific Domain (Business) Rules:** Tabulated rules with ID, description, changeability, and source.
  - **Legal Issues:** Licensing, compliance, tax, and regulatory requirements.

## Instructions for the Agent

Follow these rules when producing a Supplementary Specification:

### 1. Header and Revision History

- Title the document **Supplementary Specification**.
- Include a **Revision History** table with columns: `Version`, `Date`, `Description`, `Author`.
- Start with an inception-phase draft entry.

### 2. Introduction

- Write a short paragraph stating that this document is the repository for all system requirements **not** captured in the use cases.
- Reference the system or project by name.

### 3. Functionality

- List **cross-cutting** functional requirements: things that appear in multiple use cases or apply system-wide.
- Use named sub-sections for each concern (e.g., *Logging and Error Handling*, *Security*, *Pluggable Rules*).
- Do **not** duplicate functional behavior already described inside a specific use case.

### 4. Usability

- Describe human-factor considerations: text legibility, accessibility, color choices, feedback mechanisms (audio vs. visual).
- Mention the target user's context (e.g., speed requirements, operator attention patterns).

### 5. Reliability

- Describe recoverability strategies when external services fail.
- State availability targets or mean-time-to-recovery expectations if known.
- Flag areas that need more analysis with a note: *"Much more analysis is needed here."*

### 6. Performance

- State measurable performance goals (e.g., response time percentiles, throughput targets).
- Tie performance goals to user experience concerns identified in Usability when relevant.

### 7. Supportability

- Use sub-sections for **Adaptability** and **Configurability** at minimum.
- Describe how the system must accommodate variation across customers, deployments, or regions.
- Flag areas requiring further analysis.

### 8. Implementation Constraints

- List technology mandates (languages, frameworks, platforms) with a brief justification.
- Keep this section factual and concise.

### 9. Purchased Components

- List third-party components that must be acquired.
- Note any pluggability or integration requirements.

### 10. Free Open Source Components

- List FOSS candidates as bullet points.
- Mark them as candidates (not final decisions) unless confirmed.

### 11. Interfaces

#### Hardware and Peripheral Interfaces
- List devices the system must interact with.
- Briefly describe how the OS/software perceives each device (e.g., keyboard events, mouse events).

#### Software Interfaces
- Describe external systems the application must integrate with.
- Emphasize the need for pluggable or adaptable interfaces when multiple vendors are possible.

### 12. Application-Specific Domain (Business) Rules

- Present rules in a **table** with columns: `ID`, `Rule`, `Changeability`, `Source`.
- Assign sequential IDs (RULE1, RULE2, ...).
- Describe changeability qualitatively (Low / Medium / High) with a reason.
- State the source of authority for each rule (e.g., government regulation, retailer policy).

### 13. Legal Issues

- Cover licensing constraints for any components used.
- List mandatory regulatory compliance items (e.g., tax law, data protection).

### 14. Information in Domains of Interest *(optional)*

- Include this section when there are non-trivial domain concepts that affect requirements (e.g., pricing models, payment settlement cycles, tax complexity, item identifier schemes).
- Write one sub-section per domain concept. Keep each focused on **requirements implications**, not a full domain model.