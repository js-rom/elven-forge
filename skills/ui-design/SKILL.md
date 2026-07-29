---
name: ui-design
description: >
  UI Design skill for the Unified Process elaboration phase. Produces a project-level
  Design System in YAML, state-based Visual Specs per use case view, an Interaction
  Spec focused on behavior and traceability, and a Vaadin 25 mapping document.
  Optimized for high visual fidelity, functional fidelity, and reduced iterations
  from design to correct implementation. Triggers: ui design, visual spec,
  interaction spec, state-based ui, design system, vaadin mapping.
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

## Purpose

You are a sub-agent responsible for UI Design in the Elaboration phase.

This skill produces four complementary artifacts through a mandatory pair-programming workflow:

1. **Design System** -- project-level YAML artifact defining tokens, component rules, responsive rules, and accessibility constraints.
2. **State Visual Specs** -- per-use-case, per-state visual artifacts based on screenshot/image + HTML mock + semantic state description.
3. **Interaction Spec** -- YAML artifact describing events, validations, transitions, success/error/loading states, and traceability to SSDs and Operation Contracts.
4. **Vaadin Mapping** -- document mapping the Design System + State Visual Specs + Interaction Spec to Vaadin 25 Flow implementation decisions.

This skill separates concerns explicitly:

- **Visual truth** lives in the State Visual Specs.
- **Functional truth** lives in the Interaction Spec.
- **Technical implementation truth** lives in the Vaadin Mapping.
- **Cross-application visual consistency** lives in the Design System.
- **Rendering anchors** live in the approved screen assets (`screens/...`) referenced by each State Visual Spec.

## Scope

**In scope:**
- Define or refine the project-level Design System.
- Create visual specifications for each significant UI state of a use case view.
- Create an Interaction Spec that captures transitions, validations, feedback, and navigation.
- Map visual and functional artifacts to Vaadin 25 Flow.
- Validate traceability: transition <-> SSD operation <-> Operation Contract.
- Optimize for minimal iteration count between design and correct Vaadin implementation.

**Out of scope:**
- Generating executable Vaadin code.
- Interactive prototyping beyond the approved visual artifacts.
- Replacing SSDs or Operation Contracts.
- Replacing TDD or implementation work.

## Required Inputs

- Use Cases (brief or fully dressed) in scope for the iteration.
- System Sequence Diagrams (SSDs) from step 3 of up-elaboration.
- Operation Contracts from step 4 of up-elaboration.
- Supplementary Specification for accessibility, branding, and UI-related constraints.
- Glossary for consistent domain terminology.
- Project-level Design System input, if it already exists.
- For each significant UI state of the target view:
  - a screenshot or image,
  - an HTML mock with styles,
  - design system variables or tokens used by that HTML.
- Target implementation technology: Vaadin 25 Flow by default.

## Design Principles

- Use one **master Design System** for the whole app unless the user explicitly wants isolated systems.
- Use one **State Visual Spec bundle per significant UI state**, not one giant static screen definition.
- Use one **Interaction Spec per use case view**.
- Use one **Vaadin Mapping per use case view**.
- Do not duplicate layout detail in the Interaction Spec when it is already captured by the visual artifacts.
- Do not rely on image or HTML alone to infer behavior; behavior must be captured in the Interaction Spec.
- Do not rely on the Interaction Spec alone to infer precise visual layout; visual fidelity must come from the State Visual Specs.
- Do not treat screenshot, HTML mock, and YAML as optional alternatives; when available, they are complementary and must be kept aligned.

## Implementation Anchors (MANDATORY)

- For every approved State Visual Spec, `assets.html_mock` is required unless the user explicitly approves image-only design.
- For every approved State Visual Spec, `assets.screenshot` is required unless the HTML mock fully expresses the state and the user agrees to omit the screenshot.
- The approved HTML mock becomes a mandatory implementation anchor for PASO 14 and any implementation skill consuming the UI artifacts.
- The approved screenshot/image becomes supporting implementation evidence for spacing, emphasis, hierarchy, and responsive intent when the HTML mock does not fully express them.
- If the HTML mock, screenshot/image, State Visual Spec, and Vaadin Mapping disagree, the driver must resolve the conflict in the UI artifacts before implementation proceeds.

## Artifact Model

### 1. Design System

Project-level artifact containing:
- color tokens
- typography tokens
- spacing scale
- radius and elevation
- component token rules
- responsive breakpoints
- accessibility rules

Recommended persistence path:
- `openspec/artifacts/{domain}/03 Design/UI/Design System.yaml`

### 2. State Visual Spec

One artifact per significant UI state of a view.

Recommended contents:
- `view_id`
- `use_case`
- `state_id`
- `state_type`
- `intent`
- `source_transitions`
- `assets.screenshot`
- `assets.html_mock`
- `component_states`
- `layout_notes`
- `token_expectations`
- `accessibility_notes`
- `delta_from_base` for all non-base states

A significant state is one that changes one or more of:
- component visibility
- enabled/disabled status
- loading state
- validation state
- success/error feedback
- focus behavior
- important responsive arrangement
- action availability

### 3. Interaction Spec

One YAML artifact per use case view.

Recommended contents:
- `view_id`
- `use_case`
- `states`
- `interactive_elements`
- `transitions`

Each transition should include:
- `id`
- `from_states`
- `trigger`
- `conditions` or `failed_conditions`
- `server_call` when applicable
- `ui_during` when applicable
- `on_success`
- `on_error`
- `ui_immediate` when there is no server call

### 4. Vaadin Mapping

One mapping document per use case view.

It must cover:
- top-level layout
- component mapping
- state-to-UI mapping
- transition mapping
- validation strategy
- backend delegation points
- theming/token strategy
- accessibility mapping
- recommended class structure
- implementation non-negotiables derived from the approved screen assets

## Mandatory Pair Programming Workflow

This skill must always run in pair-programming mode:

- **Agent role:** Driver
- **User role:** Navigator
- **Cadence:** propose one step, ask for feedback/approval, then continue
- **Rule:** do not skip directly to the final artifacts without checkpoint review

## Write Gating Rules (MANDATORY)

- During exploration and draft phases: no file creation/update operations; chat content only.
- After each approval gate, persist only the authorized artifact(s).
- If the user asks to persist earlier, explicitly ask whether to skip the gate.

## Approval Gates

| Gate | Authorizes |
|------|------------|
| `OK DESIGN SYSTEM` | Persist master Design System |
| `OK VISUAL` | Persist State Visual Specs for the current use case/view |
| `OK INTERACTION` | Persist Interaction Spec |
| `OK VAADIN` | Persist Vaadin Mapping |

## Required Turn Template

For each step, always respond in this order:

1. Proposed draft for the current step, short and reviewable.
2. Open questions or assumptions.
3. Explicit approval request: `Escribe OK ... para continuar`.

Do not include later-step content until approval is received.

## Phase A: Design System

### Purpose

Define or refine the master, cross-application Design System used by all use cases and views.

### A.1 Load Constraints

Read:
- Supplementary Specification
- Vision, if available
- existing project design system
- branding constraints
- accessibility constraints

### A.2 Define or Refine Tokens

Collaboratively define or confirm:
- color tokens
- typography tokens
- spacing tokens
- radius/elevation tokens

### A.3 Define Component Rules

For components expected in the project, define:
- variants
- token usage
- interaction states
- minimum accessibility expectations

### A.4 Define Responsive Rules

Document:
- breakpoints
- stacking rules
- content priority rules
- density differences if needed

### A.5 Define Accessibility Rules

Document at least:
- contrast targets
- focus visibility
- keyboard reachability
- field labeling
- error association
- status announcement expectations

### A.6 Gate

Stop and request:
- `OK DESIGN SYSTEM`

After approval, persist:
- `openspec/artifacts/{domain}/03 Design/UI/Design System.yaml`

## Phase B: State Visual Specs

### Purpose

Create one visual bundle per significant state of the target view, using screenshot/image + HTML mock + semantic UI state description.

### B.1 Load Inputs

Before drafting:
- read the use case
- read SSDs
- read Operation Contracts
- read glossary
- read Design System
- inspect all provided state screenshots/images
- inspect all provided HTML mocks and token usage

### B.2 Identify Significant States

For the target view:
1. identify the base state
2. identify all significant states that materially change what the user sees or can do
3. avoid creating separate states for trivial textual differences

Recommended state types:
- `base`
- `editing`
- `loading`
- `validation_error`
- `server_error`
- `success`
- `empty`
- `loaded`
- `other`

### B.3 Draft State Visual Specs

For each significant state, produce a bundle that includes:
- `view_id`
- `use_case`
- `state_id`
- `state_type`
- `intent`
- `source_transitions`
- assets
- `component_states`
- `layout_notes`
- `token_expectations`
- `accessibility_notes`
- `delta_from_base` if not the base state
- Ensure `assets.html_mock` points to the approved HTML mock under `openspec/artifacts/{domain}/03 Design/UI/screens/...` when applicable.
- Ensure `assets.screenshot` points to the approved screenshot/image under `openspec/artifacts/{domain}/03 Design/UI/screens/...` when applicable.

### B.4 Validate Visual Coverage

Before requesting approval, verify:
- there is exactly one base state
- every significant visible state has a visual bundle
- every bundle includes screenshot and HTML mock references
- component states reflect meaningful visible differences
- accessibility-relevant focus/error/status details are captured
- tokens referenced are consistent with the Design System
- linked screen assets actually exist and can serve as implementation anchors

### B.5 Gate

Stop and request:
- `OK VISUAL`

After approval, persist each artifact under:
- `openspec/artifacts/{domain}/03 Design/UI/Visual Specs/UC{{#}} {{use-case.name}}/`

Suggested naming:
- `UC{{#}} {{use-case.name}} - State {{state_id}}.yaml`

## Phase C: Interaction Spec

### Purpose

Capture behavior, transitions, validations, and traceability for the target view, without duplicating visual layout detail.

### C.1 Load Inputs

Read:
- use case in scope
- SSDs
- Operation Contracts
- glossary
- approved State Visual Specs

### C.2 Identify Interactive Elements

List all meaningful interactive elements for the view:
- inputs
- actions
- selectors
- navigational controls
- dismiss/retry controls

### C.3 Define Transitions

For each scenario in scope:
1. identify trigger
2. identify from-state(s)
3. identify local validation rules
4. identify system operation and corresponding Operation Contract when applicable
5. define state entered during processing if applicable
6. define success path
7. define error path
8. define local immediate UI response if no server call occurs

### C.4 Draft the YAML

Use a compact schema centered on:
- `states`
- `interactive_elements`
- `transitions`

Allow:
- `from_states` instead of single `from_state`
- aggregated working states such as `sale_in_progress` when repeated microstates do not justify separate visual bundles

### C.5 Validate Traceability

Before requesting approval, verify:
- every transition maps to a valid trigger
- every `enter_state` exists as an approved visual state
- every system operation exists in the SSDs
- every Operation Contract reference exists
- every important success/error/loading effect is represented by a visual state when visible to the user

### C.6 Gate

Stop and request:
- `OK INTERACTION`

After approval, persist:
- `openspec/artifacts/{domain}/03 Design/UI/Interaction Specs/UC{{#}} {{use-case.name}} - Interaction Spec.yaml`

## Phase D: Vaadin Mapping

### Purpose

Map the approved Design System, State Visual Specs, and Interaction Spec to Vaadin 25 Flow implementation decisions.

### D.1 Load Inputs

Read:
- Design System
- State Visual Specs
- Interaction Spec
- Vaadin primer using `vaadin_get_vaadin_primer` with `vaadin_version: "25.2"`
- Vaadin docs as needed to confirm uncertain API or theming details

### D.2 Define Structure Mapping

Map:
- top-level layout regions
- visual regions to Vaadin layouts
- display elements to Vaadin components
- interaction elements to Vaadin components
- implementation non-negotiables derived from the approved HTML mocks and screenshots

### D.3 Define State Rendering Mapping

For each visual state:
- explain what `setVisible`, `setEnabled`, `setInvalid`, data refresh, feedback, focus, and navigation behaviors are required

### D.4 Define Transition Mapping

For each interaction transition:
- identify listener mechanism
- validation strategy
- service/facade delegation
- UI during processing
- success mapping
- error mapping

### D.4a Define Implementation Non-Negotiables

For the target view, document at least:
- top-level composition that must not be substituted,
- forbidden substitutions (for example modal vs inline, card list vs generic grid),
- feedback placement,
- action hierarchy,
- minimum CSS hooks / theme hooks,
- minimum state assertions the implementation must validate.

### D.5 Define Validation and Binder Strategy

For each meaningful input set:
- recommend whether to use no Binder, a small Binder, or a full Binder
- document why

### D.6 Define Theming Mapping

Map design tokens to Vaadin theme application strategy.

Rules:
- do not assume Lumo
- distinguish Aura vs Lumo variables
- keep token-level mapping if theme selection is still undecided

### D.7 Validate Mapping Completeness

Before requesting approval, verify:
- every interactive element has a Vaadin component mapping
- every visual state has a rendering strategy
- every transition has a listener and behavior mapping
- every validation rule has a documented mechanism
- every visible error/success/loading effect is mapped
- design tokens are mapped to a plausible theme strategy
- accessibility rules are reflected

### D.8 Gate

Stop and request:
- `OK VAADIN`

After approval, persist:
- `openspec/artifacts/{domain}/03 Design/UI/Technology Mapping/UC{{#}} {{use-case.name}} - Vaadin Mapping.md`

## Reusable Schemas

### Design System Schema

```yaml
design_system:
  metadata:
    name: <design-system-name>
    version: <version>
    owners:
      - <owner>

  color:
    primary: <color>
    primary_contrast: <color>
    secondary: <color>
    error: <color>
    success: <color>
    warning: <color>
    info: <color>
    surface: <color>
    background: <color>
    text_primary: <color>
    text_secondary: <color>
    border: <color>

  typography:
    font_family_base: <font-stack>
    font_family_mono: <font-stack>
    h1:
      size: <value>
      weight: <value>
      line_height: <value>
    h2:
      size: <value>
      weight: <value>
      line_height: <value>
    h3:
      size: <value>
      weight: <value>
      line_height: <value>
    body:
      size: <value>
      weight: <value>
      line_height: <value>
    small:
      size: <value>
      weight: <value>
      line_height: <value>

  spacing:
    xs: <value>
    s: <value>
    m: <value>
    l: <value>
    xl: <value>
    xxl: <value>

  radius:
    s: <value>
    m: <value>
    l: <value>
    full: <value>

  elevation:
    card: <shadow>
    dialog: <shadow>

  breakpoints:
    mobile: <value>
    tablet: <value>
    desktop: <value>

  accessibility:
    contrast_ratio_min: "4.5:1"
    focus_visible: true
    keyboard_navigation: true
    labels_required: true
    error_association_required: true
    status_announcements_required: true

  components:
    button:
      primary:
        background: color.primary
        text_color: color.primary_contrast
      secondary:
        background: color.secondary
    text_field:
      border_radius: radius.s
      focus_border_color: color.primary
      error_border_color: color.error
```

### State Visual Spec Schema

```yaml
state_visual_spec:
  view_id: <view-id>
  use_case: <UC# - UC Name>

  state_id: <unique-state-id>
  state_type: base|editing|loading|validation_error|server_error|success|empty|loaded|other
  intent: <short human description>

  source_transitions:
    - <transition-id>

  assets:
    screenshot: <path>
    html_mock: <path>

  component_states:
    - id: <component-id>
      role: input|action|display|feedback|navigation
      visible: true|false
      enabled: true|false
      status: default|disabled|loading|invalid|error|success|hidden|empty|selected
      message: <optional text>
      focused: true|false

  layout_notes:
    - <note>

  token_expectations:
    - <token expectation>

  accessibility_notes:
    - <a11y note>

  delta_from_base:
    - <difference>
```

### Interaction Spec Schema

```yaml
interaction_spec:
  view_id: <view-id>
  use_case: <UC# - UC Name>

  states:
    - <state-id>

  interactive_elements:
    - id: <component-id>
      type: <component-type>

  transitions:
    - id: <transition-id>

      from_states:
        - <state-id>

      trigger:
        component: <component-id>
        event: click|change|submit|focus|blur|key-enter

      conditions:
        - field: <component-id>
          rule: <rule-name>

      failed_conditions:
        - field: <component-id>
          rule: <rule-name>

      server_call:
        operation: <system-operation-name>
        contract: OC-<operation-name>

      ui_during:
        enter_state: <state-id>

      on_success:
        enter_state: <state-id>
        effects:
          - <effect>

      on_error:
        enter_state: <state-id>
        effects:
          - <effect>

      ui_immediate:
        enter_state: <state-id>
        effects:
          - <effect>
```

### Vaadin Mapping Template

```md
# UC{{#}} {{use_case_name}} - Vaadin Mapping

## Scope

This document maps the visual state bundles and interaction spec of `{{use_case_id}}: {{use_case_name}}`
to Vaadin 25 Flow components, layouts, validation, interaction handling, and theming.

View id: `{{view_id}}`
Use case: `{{use_case_id}}: {{use_case_name}}`
Target framework: `Vaadin 25 Flow (Java)`

## 1. Inputs

### Design Inputs
- Design System: `{{design_system_path}}`
- Visual state bundles: `{{visual_spec_folder}}`
- Interaction spec: `{{interaction_spec_path}}`

### Analysis Inputs
- Use case: `{{use_case_artifact_path}}`
- System Sequence Diagrams (SSDs): `{{ssd_paths}}`
- Operation Contracts: `{{operation_contract_paths}}`
- Supplementary Specification: `{{supplementary_spec_path}}`
- Glossary: `{{glossary_path}}`

## 2. View Composition

### Route and Main Class

- Vaadin view class: `{{view_class_name}}`
- Route: `@Route("{{route_path}}")`
- Main container: `{{main_layout_component}}`

### Top-Level Layout

| Visual Region | Vaadin Component | Notes |
|---|---|---|
| Header | `{{header_component}}` | {{header_notes}} |
| Main content | `{{main_content_component}}` | {{main_content_notes}} |
| Summary / sidebar | `{{summary_component}}` | {{summary_notes}} |
| Feedback area | `{{feedback_component}}` | {{feedback_notes}} |
| Actions area | `{{actions_component}}` | {{actions_notes}} |

### Layout Mapping Rules

| Visual Spec Concept | Vaadin Mapping |
|---|---|
| Main vertical stacking | `VerticalLayout` |
| Inline horizontal grouping | `HorizontalLayout` |
| Structured form area | `FormLayout` |
| Data table/list | `Grid` or `VirtualList` |
| Overlay / modal state | `Dialog` |
| State-driven sections | `setVisible(true/false)` |
| Disabled interactions | `setEnabled(false)` |

## 3. Component Mapping

### Interactive Elements

| Interaction Element | Vaadin Component | Notes |
|---|---|---|
| `{{element_id_1}}` | `{{vaadin_component_1}}` | {{notes_1}} |
| `{{element_id_2}}` | `{{vaadin_component_2}}` | {{notes_2}} |
| `{{element_id_3}}` | `{{vaadin_component_3}}` | {{notes_3}} |

### Display Elements

| Visual Element | Vaadin Component | Notes |
|---|---|---|
| `{{display_id_1}}` | `{{display_component_1}}` | {{display_notes_1}} |
| `{{display_id_2}}` | `{{display_component_2}}` | {{display_notes_2}} |

## 4. State-To-UI Mapping

Repeat this subsection for each `state_id` from the visual state bundles.

### `{{state_id}}`

| Expected Visual State | Vaadin Mechanism |
|---|---|
| {{visual_behavior_1}} | `{{vaadin_mechanism_1}}` |
| {{visual_behavior_2}} | `{{vaadin_mechanism_2}}` |
| {{visual_behavior_3}} | `{{vaadin_mechanism_3}}` |

## 5. Transition Mapping

Repeat this subsection for each transition from the interaction spec.

### `{{transition_id}}`

**Interaction Spec**
- Trigger: `{{trigger_component}}`, `{{trigger_event}}`
- From states: `{{from_states}}`
- Operation: `{{operation_name_or_none}}`
- Contract: `{{operation_contract_or_none}}`

**Vaadin Mapping**
- Listener: `{{listener_strategy}}`
- Preconditions / failed conditions: `{{precondition_strategy}}`
- UI during: `{{ui_during_strategy}}`
- On success: `{{success_strategy}}`
- On error: `{{error_strategy}}`

Suggested implementation shape:
- `{{handler_method_name}}()`
- delegates to `{{application_service_or_facade}}`

## 6. Validation Mapping

### Field-Level Rules

| Rule | Vaadin Mechanism |
|---|---|
| `{{rule_1}}` | `{{mechanism_1}}` |
| `{{rule_2}}` | `{{mechanism_2}}` |

### Binder Recommendation

Use one of these and justify it:

- No `Binder`
- Small local `Binder`
- Full view `Binder`

Rationale:
{{binder_rationale}}

## 7. Backend Interaction Mapping

| System Operation | Suggested UI Delegation |
|---|---|
| `{{operation_1}}` | `{{delegation_1}}` |
| `{{operation_2}}` | `{{delegation_2}}` |

### UI Boundary Recommendation

The Vaadin view should:
- collect user input
- render states
- delegate business operations

The Vaadin view should not:
- implement business rules
- calculate domain results that belong to the application/domain layer
- hide operation contract effects inside UI-only logic

## 8. View State Management

Recommended approach:
- Maintain a lightweight UI state enum or equivalent state holder:
  - `{{ui_state_1}}`
  - `{{ui_state_2}}`
  - `{{ui_state_3}}`

Central rendering entrypoint:
- `render(UiState state, {{view_data_type}} data)`

This method should update:
- visibility
- enabled state
- invalid/error messages
- displayed values
- focus targets
- loading indicators

## 9. Theming Mapping

### Design Token Application Strategy

| Design Token | Vaadin CSS Variable Strategy |
|---|---|
| `{{token_1}}` | `{{css_var_mapping_1}}` |
| `{{token_2}}` | `{{css_var_mapping_2}}` |
| `{{token_3}}` | `{{css_var_mapping_3}}` |

### Theme Rule

Do not assume Lumo variables.
Check whether the app uses `Aura` or `Lumo`.

If `Lumo`:
- use `--lumo-*`

If `Aura`:
- use `--aura-*`

If theme is undecided:
- keep mapping at token level and defer exact CSS variable assignment.

### Component-Level Styling

| UI Need | Vaadin Strategy |
|---|---|
| Primary action emphasis | `{{primary_action_strategy}}` |
| Error state | `{{error_state_strategy}}` |
| Loading state | `{{loading_state_strategy}}` |
| Card / surface styling | `{{surface_strategy}}` |

## 10. Accessibility Mapping

| Requirement | Vaadin Mapping |
|---|---|
| Initial focus | `{{initial_focus_mapping}}` |
| Error association | `{{error_association_mapping}}` |
| Keyboard flow | `{{keyboard_mapping}}` |
| Loading / status announcement | `{{status_announcement_mapping}}` |
| Contrast / token compliance | `{{contrast_mapping}}` |

## 11. Recommended Class Structure

- `{{view_class_name}}`
- `{{application_service_name}}`
- `{{view_data_type}}`
- `{{dto_or_row_type_1}}`
- `{{dto_or_row_type_2}}`

Keep everything in the view unless complexity justifies extraction.

## 12. Validation Checklist

- Every interaction transition maps to a Vaadin listener.
- Every visual state maps to concrete `setVisible`, `setEnabled`, `setInvalid`, data refresh, or navigation behavior.
- Required validations are explicitly mapped.
- Success, error, and loading states are represented.
- Theme token usage stays aligned with the design system.
- Business logic remains outside the view.
- Every `enter_state` from the interaction spec has a corresponding state rendering strategy.
```

## Validation Checklist

Before considering this skill complete, verify:

- [ ] The project has one master Design System or an explicit reason not to.
- [ ] The Design System is persisted as YAML.
- [ ] There is exactly one base state per target view.
- [ ] Every significant visible state has a State Visual Spec bundle.
- [ ] Every State Visual Spec references screenshot and HTML mock assets.
- [ ] Every `enter_state` in the Interaction Spec exists in the approved visual states.
- [ ] Every non-base visual state is referenced by at least one transition, unless explicitly justified.
- [ ] Every transition is traceable to an SSD system operation and Operation Contract when applicable.
- [ ] Success, error, validation, and loading states are represented when visible to the user.
- [ ] The Vaadin Mapping covers structure, state rendering, transitions, validation, theming, and accessibility.
- [ ] Approved artifacts are persisted only after the corresponding approval gate.

## Design Concern Routing

- For Vaadin component API details and best practices in Phase D, use `vaadin-orchestrator` and Vaadin documentation tools.
- For accessibility and non-functional constraints, refer to the Supplementary Specification.
- For consistent domain naming, refer to the Glossary.
- For design-level interaction responsibility and class assignment, downstream design steps may consume the Interaction Spec and Vaadin Mapping outputs.

## Anti-Patterns

- Using a single static screen description when the use case clearly has multiple significant UI states.
- Treating HTML/Tailwind as the implementation contract for Vaadin instead of as the visual truth.
- Duplicating full layout structure inside the Interaction Spec.
- Inferring behavior only from screenshots or HTML without explicit transitions.
- Creating one Design System per use case without a concrete reason.
- Writing executable Vaadin code in this phase.
- Persisting artifacts before the corresponding approval gate.
- Ignoring loading, validation, error, or success states because the base screen looks correct.
