# Strategy: Git Submodules for Code + Agents

## Target Structure

```
prueba-multi-repo/           ← git repo for the Java project
├── .git/
├── src/                     ← Java code
├── pom.xml / build.gradle
├── .gitignore
└── .agents/                 ← git submodule (agents repository)
    ├── .git (points to the agents repository)
    └── ... (agents files)
```

## Step by Step

### 1. Agents Repository (already exists or create it)

Create a repository (GitHub/GitLab/etc.) for agents. Example: `github.com/your-user/agents`.

It contains all AI logic, prompts, configurations, etc. It evolves independently, with its own commits, tags, and releases.

### 2. Initialize the Java Project

```powershell
git init
echo "target/" > .gitignore
echo ".agents/" >> .gitignore      # important: ignore the submodule folder
# ... create Java project structure (src/, pom.xml, etc.)
git add -A
git commit -m "init java project"
```

### 3. Link the Agents Submodule

```powershell
git submodule add https://github.com/your-user/agents.git .agents
git commit -m "add agents submodule"
```

This creates:
- `.gitmodules` - registers the submodule URL and path
- `.agents/` - checks out the agents repository at the current commit

### 4. Clone on Another Machine (or for Other Projects)

```powershell
git clone --recurse-submodules <url-java-project>
```

If you already cloned without submodules:

```powershell
git submodule update --init --recursive
```

### 5. Update Agents to the Latest Version

```powershell
cd .agents
git pull origin main
cd ..
git add .agents
git commit -m "update agents submodule"
```

Or in one step:

```powershell
git submodule update --remote .agents
```

### 6. Reuse in Another Java Project

Repeat steps 2 and 3 in the new project. Each Java project can point to a different commit in the agents repository. This lets one project stay on a stable version while another tests the latest one.

## Benefits Summary

| Aspect | Behavior |
|---|---|
| **Independent evolution** | Commit to the agents repository without touching any Java project |
| **Explicit versioning** | Each Java project pins a specific agents commit |
| **Reuse** | N Java projects -> 1 single agents repository |
| **Traceability** | Java project `git log` shows when the submodule was updated |
