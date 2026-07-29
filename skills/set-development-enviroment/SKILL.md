---
name: set-development-enviroment
description: Set up the development environment for the current project. Asks the user which kind of project they would like to set up (e.g. Python, Node.js, Java), then delegates to the appropriate skill for that project type. If the user is unsure, provide recommendations based on the project's existing files and conventions.triggered by set up development environment
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

## Purpose
You set up the development environment for the current project. This is a high-level orchestration skill that asks the user which kind of project they want to set up (e.g. Python, Node.js, Java), then delegates to the appropriate skill for that project type (e.g. `setup-python-env`, `setup-nodejs-env`, `setup-java-env`). If the user is unsure, you analyze the project's existing files and conventions to provide recommendations.

## When to Run
- When the user explicitly asks to set up the development environment
- When the user is starting work on a new project and needs to configure their environment
- As part of up-inception when the project type is being determined and initial setup is needed

## What to Do
1. Greet the user and confirm that they want to set up the development environment for the current project.
2. Ask the user which type of project they would like to set up. Provide options if possible from available skills.
3. If the user selects a project type, delegate to the corresponding setup skill (e.g. `setup-python-env` for Python projects, `setup-nodejs-env` for Node.js projects, `setup-java-env` for Java projects).


