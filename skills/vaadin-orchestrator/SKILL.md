---
name: vaadin-orchestrator
description: >
  Primary Vaadin 25 Java/Flow gateway skill. Classify the user request,
  orchestrate one or more domain skills, and return production-ready guidance
  with a consistent delivery contract.
version: 1.0.0
---

# Vaadin 25 Orchestrator

Use this as the primary entrypoint for Vaadin requests. Route to one primary domain skill and optional secondary skills, then produce one unified response.

Use the Vaadin MCP tools (`search_vaadin_docs`, `get_component_java_api`, `get_component_styling`) to confirm uncertain API details. Always set `vaadin_version` to `"25"` and `ui_language` to `"java"`.

## Technology Defaults

- Vaadin 25
- Java + Flow by default
- Spring Boot 4 and JUnit 6 compatible examples
- Switch to Hilla/React only when the user explicitly asks

## Routing Workflow

1. Determine user intent in one sentence.
2. Detect constraints: stack, scope, deadlines, and explicit user preferences.
3. Select one primary domain skill and up to two secondary domain skills.
4. Apply cross-cutting checks: security, responsive behavior, and testability.
5. Resolve conflicts by priority:
   - Security and correctness
   - Vaadin 25 compatibility
   - Maintainability and minimal-change approach
   - Visual polish and styling preferences
6. Return one merged answer with code and rationale.

## Domain Skill Map

Use the following playbook files:

- Layout and composition: `playbooks/vaadin-layouts.md`
- Responsive behavior: `playbooks/responsive-layouts.md`
- Theming and styling: `playbooks/theming.md`
- Visual polish and UX composition: `playbooks/frontend-design.md`
- Forms and validation: `playbooks/forms-and-validation.md`
- Reusable components: `playbooks/reusable-components.md`
- Grid and data loading: `playbooks/data-providers.md`
- Views and navigation: `playbooks/views-and-navigation.md`
- Reactive state: `playbooks/signals.md`
- Browser-free UI testing: `playbooks/ui-unit-testing.md`
- End-to-end testing: `playbooks/testbench-testing.md`
- Third-party component integration: `playbooks/third-party-components.md`
- Security hardening: `playbooks/security.md`
- Client-side views (React/Hilla): `playbooks/client-side-views.md`

## Intent Classification Guide

- If user asks about alignment, spacing, flex behavior, overflow, or layout sizing, use `vaadin-layouts`.
- If user asks about breakpoints, mobile behavior, or container/media queries, use `responsive-layouts`.
- If user asks about colors, tokens, dark mode, variants, or theme setup, use `theming`.
- If user asks for stronger visual identity, better hierarchy, or interaction polish, use `frontend-design`.
- If user asks about Binder, validators, converters, or save/cancel flow, use `forms-and-validation`.
- If user asks about custom component APIs and encapsulation, use `reusable-components`.
- If user asks about Grid lazy loading, filtering, sorting, or pageable integration, use `data-providers`.
- If user asks about routes, AppLayout, SideNav, route params, or navigation structure, use `views-and-navigation`.
- If user asks about reactive shared state and effects, use `signals`.
- If user asks for fast browser-free tests, use `ui-unit-testing`.
- If user asks for browser automation and page objects, use `testbench-testing`.
- If user asks about wrapping Web Components or React adapters, use `third-party-components`.
- If user asks about access control, secure defaults, or hardening, use `security`.
- If user explicitly asks for React/Hilla client-side views, use `client-side-views`.

## Multi-Skill Composition Rules

- Choose one primary skill that owns architecture decisions.
- Secondary skills may refine constraints but must not override primary decisions unless they fix correctness or security issues.
- For form-driven pages, pair `forms-and-validation` with `views-and-navigation` when route params or post-submit navigation is involved.
- For dashboard/grid pages, pair `data-providers` with `responsive-layouts` to avoid desktop-only designs.
- For new UI features, pair at least one testing skill (`ui-unit-testing` or `testbench-testing`) unless user explicitly declines tests.

## Clarification Policy

Ask clarifying questions only when missing information blocks a safe implementation. Keep to a maximum of two short questions per iteration.

If uncertainty is low, proceed with explicit assumptions rather than pausing.

## Output Contract

Structure responses in this order:

1. Decision summary (what was selected and why).
2. Implementation (code-level or step-by-step changes).
3. Validation (what was checked, what remains unverified).
4. Risks and limits (only concrete, actionable items).
5. Optional next steps (only when they are natural and useful).

## Guardrails

- Do not invent Vaadin APIs.
- Do not provide Vaadin 24-era advice as Vaadin 25 behavior.
- Keep code production-oriented and minimal-change by default.
- Prefer explicit bindings and explicit layout decisions over implicit behavior when maintainability is at risk.
- Include test recommendations for non-trivial changes.

## Review Mode Override

If user asks for a review, prioritize findings first:

1. Critical/major bugs and regressions.
2. Security and data-integrity issues.
3. Missing or weak tests.

Then provide assumptions and a short summary.