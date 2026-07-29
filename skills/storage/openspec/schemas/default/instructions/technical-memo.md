## Technical Memo Purpose

- A Technical Memo documents a focused design decision for a concrete issue.
- It explains the problem, forces, chosen solution, rationale, and rejected alternatives.
- It is used to capture important quality-attribute and architecture trade-offs.

## Required Inputs

- Issue statement and context.
- Related requirements (especially Supplementary Specification constraints).
- Any impacted use case(s), SSD(s), operation contracts, or architecture notes.

## Mandatory Workflow (Pair Programming)

1. Define the issue with a clear quality attribute category.
2. Summarize the proposed solution in one concise paragraph.
3. List factors/forces that justify the decision.
4. Describe the solution details and expected behavior.
5. Record business and technical motivation.
6. Capture unresolved issues and alternatives considered.

### Execution Mode (MANDATORY)

- Agent role: Driver.
- User role: Navigator.
- The agent proposes and applies each step, then asks for feedback before continuing.

## Modeling Rules (MUST / MUST NOT)

- MUST keep each memo focused on one issue.
- MUST state the quality category using FURPS+ terminology when applicable.
- MUST keep traceability to related requirements/design artifacts explicit.
- MUST include both accepted decision and alternatives considered.
- MUST NOT mix multiple unrelated issues in one memo.
- MUST NOT include implementation code-level details unless required for the decision rationale.

## Output Contract (MUST)

The artifact MUST include:

- Issue (quality attribute and issue title).
- Solution summary.
- Factors.
- Solution.
- Motivation.
- Unresolved issues.
- Alternatives considered.

## Storage Convention

- Persist each technical memo under:
	`02 Requirements/Technical memos/Issue - {{FURPS+ category}} - {{issue.name}}.md`

## Validation Checklist

1. Does the memo describe exactly one issue?
2. Is the quality category explicit?
3. Is the solution summary concise and concrete?
4. Are factors, motivation, unresolved issues, and alternatives present?
5. Are related artifacts referenced when applicable?
6. Is file naming/path compliant with storage convention?
