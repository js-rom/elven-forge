# Environment Setup Purpose

The Environment Setup artifact allows a new developer to provision the local development environment from scratch. It documents the tools, versions, dependencies, local infrastructure, and run commands, while keeping secrets out of version control.

## Instructions for the Agent

- Produce one Environment Setup artifact per project, and update it when the toolchain or infrastructure changes.
- Persist the approved artifact under `09 Enviroment/environment-setup.md`.
- Derive the concrete values from the project's build files (`pom.xml` or `build.gradle`), wrapper scripts, and local infrastructure files (e.g., `docker-compose.yaml`). Never invent versions.

### 1. Prerequisites

- List the required tools with their exact versions as found in the project (JDK, build tool, container runtime, IDE, database).

### 2. Getting the Code

- Provide the clone command and the working branch.

### 3. Installing Dependencies

- Document how dependencies are resolved and built (e.g., the Maven/Gradle wrapper).

### 4. Infrastructure

- Document local services and how to start them (e.g., `docker compose up -d`), including ports and credentials used only for development.

### 5. Running the Application

- Document the development-mode run command (e.g., Spring Boot / Vaadin dev server).

### 6. Configuration and Secrets

- List environment variables and profiles. Never commit secrets; reference where they must be provided.

### 7. Verification and Troubleshooting

- Provide checks that confirm a correct setup, and a table of common symptoms, causes, and resolutions.
