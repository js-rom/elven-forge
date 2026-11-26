# Step 8 — Architectural Analysis

## Inputs
- `Vision and Business Case` and `Use Case Model`.
- The key non-functional requirements that will have a major architectural impact.
- Skill `architectural-analysis`; schema instruction and template for the analysis and for technical memos.

## Output contract
- `Architectural Analysis`: FURPS+ factor tables, prioritized factors, architectural decisions with trade-offs, variation and evolution points, risks, unresolved issues.
- `Technical Memo`: one file per significant decision or issue, using the memo template. Do not embed memos in the analysis document.
- Refine `Supplementary Specification` with the key non-functional requirements identified here.

## Preconditions
- `OK 7` approved.
- The selected 10% and its risks are known.

## Rubric
- Every prioritized factor has scenario, response and measure.
- Every decision states alternatives and why they were rejected.
- Only architecturally significant factors are prioritized.

## Evidence required
- Factor summary and top drivers.
- List of memos created.
- Supplementary Specification delta.
- `OK 8` request.

## Anti-patterns
- Writing decisions without alternatives.
- Duplicating memo content inside the analysis.
- Prioritizing every factor as critical.
