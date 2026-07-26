# Glosary Purpose

Captures terms and definitions; it can also play the role of a data dictionary.

---

# Instructions for the Agent

## Role in the Unified Process

The Glossary is produced starting in **Inception** and refined continuously. It:

- Defines terms that are technical, domain-specific, or used inconsistently across stakeholders.
- Acts as a **data dictionary** by capturing format and validation rules for key data elements.
- Reduces communication ambiguity and prevents requirements defects caused by misunderstood terminology.

## Instructions

### 1. Revision History

- Include a table with columns: `Version`, `Date`, `Description`, `Author`.
- Start with a single inception-draft entry.

### 2. Definitions Table

- Use a **table** with columns: `Term`, `Definition and Information`, `Format`, `Validation Rules`, `Aliases`.
- List terms in **alphabetical order**.
- **Term:** use the singular form, lowercase unless it is a proper name or acronym.
- **Definition and Information:** write a precise, concise definition. Include domain context when the term is specific to the problem domain. Reference external standards or URLs when applicable (e.g., *See www.uc-council.org for details*).
- **Format:** only fill in when the term refers to a data element with a specific structure (e.g., *12-digit code of several subparts*). Leave blank otherwise.
- **Validation Rules:** only fill in when there are explicit constraints on valid values (e.g., *Digit 12 is a check digit*). Leave blank otherwise.
- **Aliases:** list common synonyms or alternate names used in the domain or by stakeholders. Leave blank if none.
- Add a final row `| ... | ... | | | |` to indicate the list is not exhaustive.

### 3. What to include

- Include terms that:
  - Are technical or domain-specific and not commonly known.
  - Are used inconsistently by different stakeholders.
  - Represent key data structures passed between system components.
  - Have format or validation constraints worth recording.
- Do **not** include terms that are self-evident or fully explained within a use case without ambiguity.

---

# Glosary Example

## Glossary

### Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Inception draft | Jan 10, 2031 | First draft. To be refined primarily during elaboration. | Craig Larman |
| | | | |

---

### Definitions

| Term | Definition and Information | Format | Validation Rules | Aliases |
| :--- | :--- | :--- | :--- | :--- |
| item | A product or service for sale. | | | |
| payment authorization | Validation by an external payment authorization service that they will make or guarantee the payment to the seller. | | | |
| payment authorization request | A composite of elements electronically sent to an authorization service, usually as a char array. Elements include: store ID, customer account number, amount, and timestamp. | | | |
| UPC | Numeric code that identifies a product. Usually symbolized with a bar code placed on products. See www.uc-council.org for details of format and validation. | 12-digit code of several subparts. | Digit 12 is a check digit. | Universal Product Code |
| ... | ... | | | |
