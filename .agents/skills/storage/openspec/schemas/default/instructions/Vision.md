# Vision Purpose

An executive summary of the project. It serves to tersely comunicate the big ideas. Summarizes some of the information in the Use Case Model ans Suplementary Specification.

---

# Instructions for the Agent

## Role in the Unified Process

The Vision is the **first artifact** produced in the Inception phase. It:

- Communicates the **big ideas** of the project in an executive summary.
- Establishes the business case and justifies the project's existence.
- Defines the scope, key stakeholder goals, and high-level features.
- Serves as input to the Use Case Model and Supplementary Specification, which elaborate its content.

## Instructions

### 1. Revision History

- Include a table with columns: `Version`, `Date`, `Description`, `Author`.
- Start with a single inception-draft entry.

### 2. Introduction

- Write **one short paragraph** summarizing the envisioned system.
- Mention the system's name, its primary purpose, and its two or three most distinctive qualities (e.g., fault tolerance, flexibility, integration).

### 3. Positioning

#### Business Opportunity
- Describe the **market gap or pain** that motivates the project.
- Explain what current solutions lack (inflexibility, poor scalability, limited integration, etc.).
- Keep it factual and concise; avoid marketing language.

#### Problem Statement
- Summarize the core problem in two or three sentences.
- Name the types of users or stakeholders who are affected.

#### Product Position Statement
- One terse sentence: *for whom*, *what the product is*, *its key differentiator*.

#### Alternatives and Competition
- Acknowledge existing alternatives and explain why they fall short.

### 4. Stakeholder Descriptions

#### Market Demographics
- Briefly describe the target market segment.

#### Stakeholder (Non-User) Summary
- List stakeholders who have an interest in the system but do not directly use it (e.g., corporate management, government bodies).

#### User Summary
- List the primary user types and their key characteristics.

#### Key High-Level Goals and Problems of the Stakeholders

- Present findings from requirements workshops or surveys in a **table** with columns: `High-Level Goal`, `Priority`, `Problems and Concerns`, `Current Solutions`.
- Merge rows when multiple problems share the same goal.
- Assign priorities: `high`, `medium`, or `low`.
- Keep Current Solutions brief; the point is to show they do **not** solve the problem.

#### User-Level Goals

- List goals per actor using bold actor names followed by a colon and a comma-separated list of goals.
- Include external systems as actors when relevant.

#### User Environment

- Describe the physical and technical context where users interact with the system (location, devices, connectivity, volume of users).

### 5. Product Overview

#### Product Perspective

- Describe where the system will physically or logically reside.
- Include a **context diagram** (or reference to one) showing the system and its external actors/systems.
- Use a blockquote to describe the diagram if it cannot be rendered inline.

#### Summary of Benefits

- Present a **table** with columns: `Supporting Feature`, `Stakeholder Benefit`.
- Each row maps one system capability to a concrete stakeholder benefit.
- Keep feature descriptions factual; keep benefit statements outcome-focused.

#### Assumptions and Dependencies
- List technical, organizational, or external assumptions the project relies on.

#### Cost and Pricing / Licensing and Installation
- Note high-level constraints or open questions; mark as *TBD* if not yet known.

### 6. Summary of System Features

- List features as a bullet list.
- Each feature should be a short noun phrase (3–10 words).
- Features should be traceable to use cases or supplementary specification sections.
- Do **not** describe implementation details here.

### 7. Other Requirements and Constraints

- Write one short paragraph noting that non-functional requirements, design constraints, usability, reliability, performance, supportability, documentation, and packaging are captured in the **Supplementary Specification** and use cases.
- Do not duplicate content from those artifacts here.

---

# Vision Example

## Revision History

| Version         | Date         | Description                                                                 | Author        |
|-----------------|--------------|-----------------------------------------------------------------------------|---------------|
| inception draft | Jan 10, 2031 | First draft. To be refined primarily during elaboration.                    | Craig Larman  |
|                 |              |                                                                             |               |

## Introduction

We envision a next generation fault-tolerant point-of-sale (POS) application, NextGen POS, with the flexibility to support varying customer business rules, multiple terminal and user interface mechanisms, and integration with multiple third-party supporting systems.

## Positioning

### Business Opportunity

Existing POS products are not adaptable to the customer’s business, in terms of varying business rules and varying network designs (for example, thin client or not; 2, 3, or 4-tier architectures). In addition, they do not scale well as terminals and business increase. And, none can work in either on-line or off-line mode, dynamically adapting depending on failures. None easily integrate with many third-party systems. None allow for new terminal technologies such as mobile PDAs. There is marketplace dissatisfaction with this inflexible state of affairs, and demand for a POS that rectifies this.

### Problem Statement

Traditional POS systems are inflexible, fault intolerant, and difficult to integrate with third-party systems. This leads to problems in timely sales processing, instituting improved processes that don’t match the software, and accurate and timely accounting and inventory data to support measurement and planning, among other concerns. This affects cashiers, store managers, system administrators, and corporate management.

### Product Position Statement

—Terse summary of who the system is for, its outstanding features, and what differentiates it from the competition.

### Alternatives and Competition...

## Stakeholder Descriptions

### Market Demographics...

### Stakeholder (Non-User) Summary...

### User Summary...

### Key High-Level Goals and Problems of the Stakeholders

A one-day requirements workshop with subject matter experts and other stakeholders, and surveys in
several retail outlets led to identification of the following key goals and problems:

| High-Level Goal | Priority | Problems and Concerns | Current Solutions |
| :--- | :--- | :--- | :--- |
| Fast, robust, integrated sales processing | high | Reduced speed as load increases. | Existing POS products provide basic sales processing, but do not address these problems. |
| | | Loss of sales processing capability if components fail. | |
| | | Lack of up-to-date and accurate information from accounting and other systems due to non-integration with existing accounting, inventory, and HR systems. Leads to difficulties in measuring and planning. | |
| | | Inability to customize business rules to unique business requirements. | |
| | | Difficulty in adding new terminal or user interface types (for example, mobile PDAs). | |
| ... | ... | | ... |

---

### User-Level Goals

The users (and external systems) need a system to fulfill these goals:

- **Cashier:** process sales, handle returns, cash in, cash out
- **System administrator:** manage users, manage security, manage system tables
- **Manager:** start up, shut down
- **Sales activity system:** analyze sales data
- ...

---

### User Environment...

---

## Product Overview

### Product Perspective

The NextGen POS will usually reside in stores; if mobile terminals are used, they will be in close proximity
to the store network, either inside or close outside. It will provide services to users, and collaborate with
other systems, as indicated in Figure Vision-1.

> **Figure Vision-1. NextGen POS system context diagram**
>
> Actors: Sales Activity System, Cashier, System Administrator, Store Manager  
> The **NextGen POS** calls upon services from and provides services to:
> - `«actor»` Payment Authorization Service
> - `«actor»` Tax Calculator
> - `«actor»` Accounting System
> - `«actor»` Human Resources System
> - `«actor»` Inventory System

### Summary of Benefits

| Supporting Feature | Stakeholder Benefit |
| :--- | :--- |
| Functionally, the system will provide all the common services a sales organization requires, including sales capture, payment authorization, return handling, and so forth. | Automated, fast point-of-sale services. |
| Automatic detection of failures, switching to local offline processing for unavailable services. | Continued sales processing when external components fail. |
| Pluggable business rules at various scenario points during sales processing. | Flexible business logic configuration. |
| Real-time transactions with third-party systems, using industry standard protocols. | Timely, accurate sales, accounting, and inventory information, to support measuring and planning. |
| ... | ... |

---

*Assumptions and Dependencies...*  
*Cost and Pricing...*  
*Licensing and Installation...*  

---

## Summary of System Features

- sales capture
- payment authorization (credit, debit, check)
- system administration for users, security, code and constants tables, and so forth.
- automatic offline sales processing when external components fail
- real-time transactions, based on industry standards, with third-party systems, including inventory, accounting, human resources, tax calculators, and payment authorization services
- definition and execution of customized "pluggable" business rules at fixed, common points in the processing scenarios
- ...

---

## Other Requirements and Constraints

Including design constraints, usability, reliability, performance, supportability, design constraints, documentation, packaging, and so forth: See the Supplementary Specification and use cases.