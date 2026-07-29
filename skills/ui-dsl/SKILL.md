---
name: ui-dsl
description: >
  UI Design skill for the Unified Process elaboration phase. Transforms a sketch/screenshot into
  an abstract YAML DSL (technology-independent), defines a project-level Design System, and maps
  both to a concrete UI technology (e.g. Vaadin 25). The DSL models components, layout regions,
  and state transitions traceable to SSDs and Operation Contracts.
  Triggers: ui design, ui dsl, abstract ui, design system, technology mapping, vaadin ui.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

# Purpose

You are a sub-agent responsible for UI Design in the Elaboration phase. This skill produces three artifacts through a mandatory pair-programming workflow:

1. **Abstract UI DSL** — YAML document describing UI components, layout regions, and state transitions. Technology-independent.
2. **Design System** — Project-level document defining design tokens, component rules, responsive breakpoints, and accessibility constraints.
3. **Technology Mapping** — Document mapping the abstract DSL and Design System to a concrete UI technology (Vaadin 25 by default).

The DSL is structured around **state transitions**, not just static layout. Each transition maps to a system operation (SSD) and an Operation Contract, ensuring full traceability from requirements to UI.

# Required Inputs

- Use Cases (brief or fully dressed) in scope for the iteration.
- System Sequence Diagrams (SSDs) from step 3 of up-elaboration.
- Operation Contracts from step 4 of up-elaboration.
- Supplementary Specification (for accessibility, branding, and UI constraints).
- Glossary (for domain terminology used in labels and messages).
- A sketch, screenshot, or textual description of the intended UI.

# Scope

**In scope:**
- Produce a technology-independent YAML DSL describing components, layout, and state transitions.
- Define a project-level Design System with design tokens, spacing, typography, and responsive rules.
- Produce a documented mapping from DSL + Design System → Vaadin 25 components and behavior.
- Validate traceability: each transition ↔ system operation ↔ operation contract.

**Out of scope:**
- Generating executable code. The actual implementation happens in step 14 (TDD).
- Reports design (step 6, separate skill).
- Interactive UI prototyping. This phase produces specifications and mappings.

# Mandatory Pair Programming Workflow

This skill must always run in pair-programming mode:
- **Agent role:** Driver.
- **User role:** Navigator.
- **Cadence:** The agent proposes one step, asks for confirmation/feedback, then proceeds.
- **Rule:** Do not skip directly to final recommendations without step-by-step checkpoints.

## Write Gating Rules (MANDATORY)

- During Fases A, B, and C exploration: no create/update file operations; chat content only (YAML drafts, tables, mapping documents).
- After each gate approval, persist the corresponding artifact.
- If user requests file generation before approval, ask to confirm skipping the gate.

## Approval Gates

| Gate | Authorizes |
|------|-----------|
| `OK FASE A` | Persist `UI DSL.yaml` |
| `OK FASE B` | Persist `Design System.md` |
| `OK FASE C` | Persist `Vaadin Mapping.md` |

## Required Turn Template

For each step, always respond in this order:
1. Proposed draft for the current step (short and reviewable).
2. Open questions or assumptions.
3. Explicit approval request: `Escribe OK FASE X para continuar`.

Do not include content for later steps until approval is received.

# FASE A: Abstract UI DSL

## Purpose

Transform a sketch, screenshot, or textual UI description into a technology-independent YAML document that describes:
- **Structure**: layout regions and components with their intent, validation, and hierarchy.
- **Transitions**: state changes triggered by user actions, mapped to system operations and operation contracts.

## A.1 Load Required Inputs

Before drafting:
- Read the Use Cases in scope (brief or fully dressed) for the current iteration.
- Read the SSDs produced in step 3 of up-elaboration for each use case.
- Read the Operation Contracts produced in step 4 of up-elaboration for each use case.
- Read the Glossary for domain terminology.

## A.2 Analyze the UI Sketch/Screenshot with the User

- Ask the user to describe or share the UI (sketch, screenshot, or textual description).
- Collaboratively identify:
  - **Regions**: header, body, footer, sidebar, etc.
  - **Components per region**: inputs, buttons, tables, navigation, feedback.
  - **Intent** of each component (search, filter, submit-form, navigation-back, etc.).
  - **User actions**: what triggers each transition (click, submit, cancel, selection change).

## A.3 Identify State Transitions from SSDs and OCs

For each scenario in scope:
1. Identify the system operations from the SSD.
2. For each system operation, find the corresponding Operation Contract.
3. Define transitions:
   - **Happy path**: trigger → pre-conditions → ui_during → on_success.
   - **Validation error path**: trigger → pre-conditions (invalid) → ui_on_execute.
   - **Server error path**: trigger → pre-conditions → ui_during → on_error.
4. Verify that every post-condition from the OC has a corresponding `on_success` or `on_error` block.

## A.4 Draft the YAML DSL

Using the vocabulary defined below, draft the complete YAML for the current view.

### Controlled Vocabulary

| Category | Allowed Values |
|----------|---------------|
| **Layout** | `horizontal`, `vertical`, `grid`, `tabs`, `split` |
| **Input** | `text-field`, `password-field`, `text-area`, `select`, `checkbox`, `radio-group`, `date-picker`, `file-upload`, `combo-box` |
| **Display** | `title`, `text`, `image`, `icon`, `badge`, `card`, `table`, `list` |
| **Action** | `button`, `link`, `icon-button`, `menu-item` |
| **Navigation** | `breadcrumb`, `sidebar`, `tab-item`, `drawer` |
| **Feedback** | `notification`, `dialog`, `tooltip`, `spinner`, `progress-bar`, `snackbar` |
| **Intent** | `submit-form`, `navigation-back`, `navigation-forward`, `unique-identifier`, `contact-info`, `credential`, `authorization`, `search`, `filter`, `sort`, `delete`, `edit`, `create`, `cancel`, `confirm` |
| **State** | `visible`, `hidden`, `enabled`, `disabled`, `loading`, `valid`, `invalid`, `default`, `error`, `success`, `warning`, `info`, `focused`, `selected`, `reset` |
| **Variant** | `primary`, `secondary`, `tertiary`, `danger`, `small`, `large`, `outlined`, `text` |

### YAML Schema

```yaml
view:
  id: <unique-view-id>                # e.g. user-registration
  title: "<human-readable title>"
  use_case: <UC# - UC Name>          # traceable to use case
  scenarios: [S1, S2]                # scenarios covered by this view

  structure:
    regions:
      - id: <region-id>
        layout: horizontal|vertical|grid|tabs|split
        alignment: [start|center|end|space-between|space-around]
        spacing: xs|small|medium|large|xl
        children:
          - component: <component-type>   # from controlled vocabulary
            id: <unique-component-id>
            label: "<label>"
            text: "<display-text>"
            required: true|false
            intent: <intent-token>
            visible: true|false
            enabled: true|false
            variant: primary|secondary|tertiary|danger
            validation:                    # for input components
              pattern: alphanumeric|email|numeric|url|regex
              min_length: <int>
              max_length: <int>
              requirements: [upper, lower, digit, special]
            options_source: <data-reference>   # e.g. domain.roles
            children: [ ... ]                   # recursive for groups/regions

  transitions:
    - id: <transition-id>                  # unique within the view
      description: "<what this transition does>"
      maps_to_operation: <system-operation-name>   # from SSD
      maps_to_contract: OC-<operation-name>        # from Operation Contracts
      trigger:
        component: <component-id>          # must exist in structure
        event: click|change|submit|focus|blur|key-enter
      pre_conditions:                      # from OC pre-conditions
        - field: <component-id>
          state: valid|invalid|enabled|selected|checked
        - field: <component-id>
          state: valid
      ui_during:                           # loading/processing state
        - target: <component-or-region-id>
          state: [disabled, loading]
        - target: <component-id>
          state: loading
      on_success:                          # OC post-conditions (happy path)
        - target: <component-or-region-id>
          state: [visible, success]
          message: "<success-message>"
        - target: <component-or-region-id>
          state: reset
        - target: view
          action: navigate|refresh|close-dialog
          destination: "<path-or-view-id>"
          delay_ms: <int>
      on_error:                            # OC post-conditions (error path)
        - target: <component-or-region-id>
          state: [enabled, default]
        - target: <component-id>
          state: [visible, error]
          message_source: server_response   # or "server_response"
          message: "<fallback-message>"
      ui_on_execute:                       # immediate UI response (no server)
        - target: <component-id>
          state: [invalid, focused]
          error_message: "<validation-message>"
        - target: <component-id>
          state: enabled
```

### Naming and Formatting Rules

- All `id` values MUST be `snake_case` and unique within the view.
- `maps_to_operation` MUST match exactly the system operation name from the SSD.
- `maps_to_contract` MUST use the convention `OC-<operation-name>`.
- `message_source: server_response` indicates the message comes from the back-end response.
- `delay_ms` on navigation/actions is optional; use only when a deliberate pause is needed for UX.

## A.5 Validate Traceability

Before requesting approval, verify:
- Every transition has a `maps_to_operation` that exists in the SSDs.
- Every `maps_to_contract` reference corresponds to an existing Operation Contract.
- Every post-condition from the OC is addressed in either `on_success` or `on_error`.
- Every `trigger.component` exists in the `structure` tree.
- All `pre_conditions.field` values reference an existing component `id`.

## A.6 Gate

- Stop and request `OK FASE A` before continuing.
- After approval, persist the artifact using the storage skill:
  - Path: `openspec/artifacts/{domain}/03 Design/UI/Abstract DSL/UC{{#}} {{use-case.name}} - UI DSL.yaml`

# FASE B: Design System

## Purpose

Define or refine a project-level Design System document that establishes the visual and interaction rules for all UI views. This document is referenced during FASE C to guide the concrete technology mapping.

## B.1 Load Constraints

- Read the Supplementary Specification for accessibility requirements (contrast ratios, keyboard navigation, screen-reader compatibility), branding guidelines, and any UI-related non-functional requirements.
- Review the Vision for high-level user-experience goals.

## B.2 Define Design Tokens

Collaboratively define the following with the user:

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `color-primary` | Hex or CSS color | Primary actions, active states, brand |
| `color-primary-contrast` | Hex or CSS color | Text/icons on primary backgrounds |
| `color-secondary` | Hex or CSS color | Secondary surfaces, hover states |
| `color-error` | Hex or CSS color | Errors, destructive actions |
| `color-success` | Hex or CSS color | Success feedback |
| `color-warning` | Hex or CSS color | Warnings |
| `color-info` | Hex or CSS color | Informational states |
| `color-surface` | Hex or CSS color | Cards, dialogs, elevated surfaces |
| `color-background` | Hex or CSS color | Page background |
| `color-text-primary` | Hex or CSS color | Body text, headings |
| `color-text-secondary` | Hex or CSS color | Labels, hints, placeholders |
| `color-border` | Hex or CSS color | Dividers, borders |

### Typography

| Token | Attributes | Usage |
|-------|-----------|-------|
| `font-family-base` | Font name, fallback stack | All text |
| `font-family-mono` | Font name, fallback stack | Code, data |
| `font-size-h1` | Size, weight, line-height | Page titles |
| `font-size-h2` | Size, weight, line-height | Section headers |
| `font-size-h3` | Size, weight, line-height | Sub-section headers |
| `font-size-body` | Size, weight, line-height | Body text |
| `font-size-small` | Size, weight, line-height | Captions, hints |

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `space-xs` | px value | Tight spacing |
| `space-s` | px value | Compact spacing |
| `space-m` | px value | Default spacing |
| `space-l` | px value | Relaxed spacing |
| `space-xl` | px value | Section separation |
| `space-2xl` | px value | Page-level separation |

### Border & Elevation

| Token | Value | Usage |
|-------|-------|-------|
| `radius-s` | px value | Inputs, chips |
| `radius-m` | px value | Cards, dialogs |
| `radius-l` | px value | Modals |
| `radius-full` | value | Pills, avatars |
| `shadow-card` | CSS shadow | Cards, elevated surfaces |
| `shadow-dialog` | CSS shadow | Dialogs, overlays |

## B.3 Define Component Tokens

For each component type that will appear in the DSL, define which design tokens apply:

| Component | Attribute | Design Token |
|-----------|-----------|-------------|
| Button (primary) | background | `color-primary` |
| Button (secondary) | background | `color-secondary` |
| Button (primary) | text color | `color-primary-contrast` |
| TextField | border-radius | `radius-s` |
| TextField (focused) | border-color | `color-primary` |
| Notification (error) | background | `color-error` |
| Card | background | `color-surface` |
| Card | shadow | `shadow-card` |

## B.4 Define Responsive Breakpoints

| Breakpoint | Min Width | Layout Behavior |
|------------|-----------|----------------|
| `mobile` | — | Single column, stacked layouts |
| `tablet` | 600px | Two columns, condensed sidebar |
| `desktop` | 1024px | Full multi-column layouts |

## B.5 Define Accessibility Rules

- Minimum contrast ratio: 4.5:1 for normal text (WCAG AA).
- Focus indicators: visible on all interactive elements.
- Labels: required on all form inputs.
- Keyboard: all interactive elements reachable via Tab.
- Error messages: associated with their fields via accessible descriptions.

## B.6 Gate

- Stop and request `OK FASE B` before continuing.
- After approval, persist the artifact using the storage skill:
  - Path: `openspec/artifacts/{domain}/03 Design/UI/Design System.md`

# FASE C: Technology Mapping (Vaadin 25)

## Purpose

Map the abstract UI DSL and Design System to a concrete UI technology. By default this maps to Vaadin 25 (Java/Flow). The output is a documented mapping — not executable code. Implementation happens in step 14 (TDD).

## C.1 Load Inputs

- Read the UI DSL YAML produced in Fase A.
- Read the Design System produced in Fase B.
- Load the Vaadin 25 primer via `vaadin_get_vaadin_primer` with `vaadin_version: "25.2"`.
- Use `vaadin_search_vaadin_docs` to confirm any uncertain API details.

## C.2 Produce Structure Mapping

For every component and layout in the DSL `structure`, map it to its Vaadin equivalent:

| DSL Concept | Vaadin Component | Mapping Notes |
|-------------|-----------------|---------------|
| `layout: vertical` | `VerticalLayout` | `setPadding(true)`, `setSpacing(true)` |
| `layout: horizontal` | `HorizontalLayout` | `setSpacing(true)` |
| `layout: grid` | `Dashboard` or CSS Grid | Card-based layouts |
| `layout: tabs` | `Tabs` + content area | Selected tab switches content |
| `alignment: space-between` | `setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN)` | |
| `alignment: center` | `setAlignItems(FlexComponent.Alignment.CENTER)` | |
| `component: title` | `H1`, `H2`, `H3` | Based on typography token |
| `component: text` | `Span`, `Paragraph` | |
| `component: text-field` | `TextField` | See Binder integration below |
| `component: password-field` | `PasswordField` | |
| `component: text-area` | `TextArea` | |
| `component: select` | `Select<T>` | `setItems()`, `setItemLabelGenerator()` |
| `component: checkbox` | `Checkbox` | |
| `component: date-picker` | `DatePicker` | |
| `component: combo-box` | `ComboBox<T>` | With lazy loading via `DataProvider` |
| `component: button (primary)` | `Button` | `addThemeVariants(ButtonVariant.LUMO_PRIMARY)` |
| `component: button (secondary)` | `Button` | Default variant |
| `component: table` | `Grid<T>` | With columns, sorting, filtering |
| `component: notification` | `Notification` | `Notification.show(text, duration, position)` |
| `component: dialog` | `Dialog` | |
| `component: badge` | `Badge` | |
| `component: icon` | `Icon` | Vaadin icon set |
| `component: card` | Custom `Div` with card styling or `Card` | |
| `component: image` | `Image` | |
| `component: spinner` | `ProgressBar` (indeterminate) | |
| `component: group` | `Section` or nested `Div` | |

### Design Token Mapping to Vaadin

| Design Token | Vaadin Application |
|--------------|-------------------|
| `color-primary` | `--lumo-primary-color` or `--aura-primary` |
| `color-secondary` | `--lumo-contrast-10pct` or `--aura-secondary` |
| `color-error` | `--lumo-error-color` or `--aura-error` |
| `font-family-base` | `--lumo-font-family` or `--aura-font-family` |
| `font-size-h1` | `--lumo-font-size-xxxl` or `--aura-font-size-xxxl` |
| `space-m` | `--lumo-space-m` or `--aura-space-m` |
| `radius-s` | `--lumo-border-radius-s` or `--aura-border-radius-s` |
| `shadow-card` | `--lumo-box-shadow-s` or `--aura-box-shadow-s` |

## C.3 Produce Transition Mapping

For every transition in the DSL, map to the Vaadin implementation mechanism:

| DSL Concept | Vaadin Mechanism |
|-------------|-----------------|
| `trigger: [component, event: click]` | `button.addClickListener(e -> { ... })` |
| `pre_conditions: [field, state: valid]` | `binder.validate().isOk() && binder.writeBeanIfValid(bean)` |
| `ui_during: [state: disabled]` | `component.setEnabled(false)` |
| `ui_during: [state: loading]` | Set `Button` icon to spinner; or `ProgressBar.setVisible(true)` |
| `on_success: [action: navigate]` | `UI.getCurrent().navigate(TargetView.class)` |
| `on_success: [state: reset]` | `binder.readBean(null)` |
| `on_success/on_error: [state: visible, success/error]` | `Notification.show(msg, 5000, Notification.Position.MIDDLE)` |
| `on_error: [state: enabled]` | `component.setEnabled(true)` |
| `ui_on_execute: [state: invalid, focused]` | `field.setInvalid(true); field.setErrorMessage(msg); field.focus()` |
| `state: hidden/visible` | `component.setVisible(boolean)` |
| `delay_ms` | Use `UI.getCurrent().access(() -> ..., Duration.ofMillis(ms))` or `CompletableFuture` |

### Binder Integration Mapping

| DSL Field | Vaadin Binder Setup |
|-----------|-------------------|
| `text-field` (required) | `binder.forField(field).asRequired("message").bind(Bean::get, Bean::set)` |
| `text-field` (with validation) | `binder.forField(field).asRequired().withValidator(v -> condition, "message").bind(...)` |
| `select` (required) | `binder.forField(select).asRequired("message").bind(...)` |
| `checkbox` | `binder.forField(checkbox).bind(Bean::isX, Bean::setX)` |

## C.4 Validate Mapping Completeness

Before requesting approval, verify:
- Every `component` in the DSL has a corresponding entry in the structure mapping table.
- Every `transition` has a corresponding entry in the transition mapping table.
- Every `pre_condition.field` has a Binder setup documented.
- Every design token used in the DSL is mapped to a Vaadin CSS custom property.
- All layout directives (`alignment`, `spacing`, `justify`, `wrap`) have a mapping.

## C.5 Gate

- Stop and request `OK FASE C` before continuing.
- After approval, persist the artifact using the storage skill:
  - Path: `openspec/artifacts/{domain}/03 Design/UI/Technology Mapping/UC{{#}} {{use-case.name}} - Vaadin Mapping.md`

# Design Concern Routing

- For Vaadin component API details and best practices during FASE C, use the `vaadin-orchestrator` skill and its playbooks (`vaadin-layouts`, `forms-and-validation`, `theming`, `frontend-design`, `views-and-navigation`).
- For accessibility and non-functional UI constraints, refer to the Supplementary Specification.
- For domain terminology used in labels and messages, refer to the Glossary.
- For design-level object interactions and class assignment, step 9 of up-elaboration consumes this skill's output.

# Output Contract (MUST)

After this skill completes, the following artifacts MUST be persisted:

| Artifact | Path |
|----------|------|
| Abstract UI DSL | `openspec/artifacts/{domain}/03 Design/UI/Abstract DSL/UC{{#}} {{use-case.name}} - UI DSL.yaml` |
| Design System | `openspec/artifacts/{domain}/03 Design/UI/Design System.md` |
| Technology Mapping (Vaadin) | `openspec/artifacts/{domain}/03 Design/UI/Technology Mapping/UC{{#}} {{use-case.name}} - Vaadin Mapping.md` |

Additionally, ensure:
- The DSL YAML is valid YAML syntax and follows the controlled vocabulary.
- The Design System includes color, typography, spacing, border/elevation, component tokens, responsive breakpoints, and accessibility rules.
- The Technology Mapping covers both structure and transition mappings, plus Binder integration.
- Every transition is traceable to a system operation (SSD) and an operation contract.
- Every post-condition from the OC is addressed in `on_success` or `on_error`.

# Validation Checklist

Before considering this skill complete, verify:

- [ ] FASE A: YAML DSL is syntactically valid.
- [ ] FASE A: Every `id` is `snake_case` and unique within the view.
- [ ] FASE A: Every `trigger.component` exists in the `structure` tree.
- [ ] FASE A: Every `pre_conditions.field` references an existing component `id`.
- [ ] FASE A: Every transition maps to a valid system operation from the SSD.
- [ ] FASE A: Every `maps_to_contract` references an existing Operation Contract.
- [ ] FASE A: Every OC post-condition is covered by `on_success` or `on_error`.
- [ ] FASE B: Design System includes color palette, typography, spacing, border/elevation, and component tokens.
- [ ] FASE B: Responsive breakpoints are defined.
- [ ] FASE B: Accessibility rules are documented (contrast ratios, focus, keyboard, labels, errors).
- [ ] FASE C: Every DSL component has a structure mapping entry.
- [ ] FASE C: Every DSL transition has a transition mapping entry.
- [ ] FASE C: Every `pre_condition.field` has a Binder setup in the mapping.
- [ ] FASE C: Every design token used in the DSL is mapped to a Vaadin CSS property.
- [ ] FASE C: All layout directives (`alignment`, `spacing`, `justify`, `wrap`) have a mapping.
- [ ] Artifacts are persisted to the correct `openspec/artifacts/{domain}/03 Design/UI/` paths via storage skill.
- [ ] All three approval gates (`OK FASE A`, `OK FASE B`, `OK FASE C`) were received.

# Anti-Patterns

- Writing executable Vaadin code in FASE C — this phase produces a mapping document, not production code.
- Skipping state transitions and only documenting static layout — the DSL must capture user actions and system responses.
- Defining the Design System without consulting the Supplementary Specification.
- Creating one DSL per technology — the DSL is technology-independent; only FASE C is technology-specific.
- Using vocabulary outside the controlled set without discussing it with the user first.
- Persisting artifacts before receiving the corresponding gate approval.
- Designing a view without tracing its transitions back to SSDs and Operation Contracts.
- Including technology-specific details (component class names, API calls) in the DSL — those belong in FASE C.
