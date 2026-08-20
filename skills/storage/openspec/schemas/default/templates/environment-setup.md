# Environment Setup

## Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| Environment draft | {{date}} | First draft for the development environment setup. | {{author}} |
| | | | |

---

## Purpose

<Describe how a new developer provisions the local development environment from scratch.>

---

## Prerequisites

| Tool | Version | Notes |
| :--- | :--- | :--- |
| <JDK> | {{version}} | <Notes> |
| <Build tool (Maven / Gradle)> | {{version}} | <Notes> |
| <Container runtime (Docker)> | {{version}} | <Notes> |
| <IDE> | {{version}} | <Notes> |
| <Database> | {{version}} | <Notes> |

---

## Getting the Code

<Describe how to clone the repository and check out the working branch.>

```powershell
# <Clone command>
```

---

## Installing Dependencies

<Describe how dependencies are resolved and built.>

```powershell
# <Dependency / build command>
```

---

## Infrastructure (Local Services)

<Describe the local services (database, cache, message broker) and how to start them.>

```powershell
# <docker compose or equivalent>
```

---

## Running the Application

<Describe how to run the application in development mode.>

```powershell
# <Run command>
```

---

## Configuration

<Describe environment variables, profiles, and local configuration files, and where secrets must never be committed.>

| Setting | Default | Description |
| :--- | :--- | :--- |
| <KEY> | {{value}} | <Description> |

---

## Verification

<List checks that confirm the environment is correctly provisioned.>

- [ ] <Check 1>
- [ ] <Check 2>

---

## Troubleshooting

| Symptom | Cause | Resolution |
| :--- | :--- | :--- |
| <Symptom> | <Cause> | <Resolution> |
