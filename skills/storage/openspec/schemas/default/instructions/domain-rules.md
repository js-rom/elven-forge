# Domain Rules 

## Purpose

Captures long-living and spanning rules or policies, such as tax laws, that trascend one particular application.

---

## Instructions for the Agent

### Role in the Unified Process

The Domain Rules document is produced starting in **Inception** and refined throughout the project. It:

- Captures **business rules and policies** that span multiple use cases or applications.
- Separates long-lived domain rules (law, industry policy) from application-specific rules (captured in the Supplementary Specification).
- Provides traceability from rules to their authoritative source.

### Instructions

#### 1. Revision History

- Include a table with columns: `Version`, `Date`, `Description`, `Author`.
- Start with a single inception-draft entry.

#### 2. Rule List Table

- Include a note pointing to the Supplementary Specification for application-specific rules.
- Use a **table** with columns: `ID`, `Rule`, `Changeability`, `Source`.
- **ID:** assign sequential identifiers: `RULE1`, `RULE2`, etc.
- **Rule:** state the rule concisely. If official references exist (e.g., statutes, standards), note them inline.
- **Changeability:** describe how likely and how frequently the rule may change. Include a qualitative level (`Low`, `Medium`, `High`) and an explanatory sentence about the expected evolution or driving factors.
- **Source:** identify the authoritative source of the rule (e.g., law, regulation, industry association policy, company policy).

#### 3. What to include

- Include rules that:
  - Are dictated by external authorities (government law, industry regulation, standards bodies).
  - Apply across multiple use cases or systems.
  - Have a named, verifiable source.
- Do **not** include rules that are purely internal application logic or UI behavior — those belong in use cases or the Supplementary Specification.

---

## Domain Rules Example

### Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Inception draft | Jan 10, 2031 | First draft. To be refined primarily during elaboration. | Craig Larman |
| | | | |

---

## Rule List

*(See also the separate Application-specific Rules in the Supplementary Specification.)*

| ID | Rule | Changeability | Source |
| :--- | :--- | :--- | :--- |
| RULE1 | Signature required for credit payments. | Buyer "signature" will continue to be required, but within 2 years most of our customers want signature capture on a digital capture device, and within 5 years we expect there to be demand for support of the new unique digital code "signature" now supported by USA law. | The policy of virtually all credit authorization companies. |
| RULE2 | Tax rules. Sales require added taxes. See government statutes for current details. | High. Tax laws change annually, at all government levels. | law |
| RULE3 | Credit payment reversals may only be paid as a credit to the buyer's credit account, not as cash. | Low | credit authorization company policy |
