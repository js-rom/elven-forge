# Requirements Ranking Purpose

Organize requirements and iterations by risk, coverage, and criticality.

**Risk** includes both tecnical complexity and other factors, such as uncertainty of effort or usability.
**Coverage** implies that all major parts of the system are at least touched on in early iterations (perhaps a "wide and shallow" implementation across many components)
**Criticality** refers to functions the client considers of high business value.

- These criteria are used to rank work across iterations
- Use cases or use case scenarios are ranked for implementation
- early iterations implements high ranking scenarios

## Instructions for the Agent

### 1. Revision History

- Include a table with columns: `Version`, `Date`, `Description`, `Author`.
- Start with a single inception-draft entry.

### 2. Ranking Criteria

- Evaluate each candidate using all three lenses:
	- `Risk`: technical complexity, uncertainty, integration or organizational difficulty.
	- `Coverage`: how much of the system or architecture the candidate helps explore early.
	- `Criticality`: business value, compliance exposure, operational urgency, or stakeholder impact.
- Do not rank only by business value. The purpose is to balance architectural learning with delivery value.

### 3. Ranked Candidates Table

- Use a table with columns: `Rank`, `Requirement (Use Case or Feature)`, `Risk`, `Coverage`, `Criticality`, `Comment`.
- Use the rank values `High`, `Medium`, or `Low`.
- Keep comments concise but explicit enough to justify the rank.

### 4. Selection for Detailed Analysis

- After ranking, choose approximately 10% of the use cases for deeper analysis.
- Explain each selected item in terms of risk, coverage, and criticality.
- The detailed use cases chosen for inception must come from this ranked list rather than from ad hoc preference.