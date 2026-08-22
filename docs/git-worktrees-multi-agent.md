# Strategy: Git Worktrees for Multi-Agent Development

Goal: run several AI agents in parallel, each implementing a different feature, without mixing their changes in the same files.

## Core Idea

One worktree + one branch per agent. Each worktree is an independent checkout of the same repository (same `.git`, separate working files). Each agent operates only inside its own folder, commits to its own branch, and integration happens centrally on `main`.

```
registro-horario/               ← main checkout (orchestrator)
├── .git/
└── ... (project files)

registro-horario-agente1/       ← worktree for agent 1 (branch feat/agente1)
registro-horario-agente2/       ← worktree for agent 2 (branch feat/agente2)
registro-horario-agente3/       ← worktree for agent 3 (branch feat/agente3)
```

## Key Rules

1. **Disjoint modules**: assign each agent a non-overlapping area (e.g. agent 1 → `policies/absence`, agent 2 → `policies/schedule`, agent 3 → UI). Worktrees prevent file mixing, but two agents editing the same file will still produce merge conflicts at integration time.
2. **Agents must commit**: each agent finishes by committing to its own branch. Worktrees do not inherit uncommitted changes.
3. **Integration is central**: only the orchestrator merges branches into `main`, where the full context lives, and resolves conflicts there.
4. **One opencode instance per worktree**: launch each agent session in its own worktree directory.
5. **Shared docs diverge too**: `.agents/` and `openspec/` are per-branch. If agents generate design artifacts, decide who integrates those folders to avoid overwriting each other.

## Alternatives (and why they are worse here)

| Approach | Problem |
|---|---|
| Branches without worktrees | Forcing commit/stash before every branch switch is fragile when agents leave uncommitted changes |
| Separate clones | Duplicate download/config; worktrees share the same `.git` |

## Project-Specific Notes

- This repo has a **submodule** (`.gitmodules`). Each worktree checks it out independently; an agent must run `git submodule update --init` if it touches that area.
- Worktrees are created from a commit: always commit (or stash) the current WIP on `main` first.

## Workflow State Management (openspec/) in Multi-Worktree Mode

### The Problem

Workflow state is **per-domain** (`openspec/artifacts/{domain}/state.yaml`) and the only shared workflow file is the global router `openspec/config.yaml` (list of domains). If every agent updated the same router or the same domain state in its own branch, merges would conflict and the merged state would be inconsistent (different `current_step`, `approved_steps`, artifact statuses).

### The Model: Per-Domain State + Per-Worktree Shadow State

1. **Global router, orchestrator-only**: `openspec/config.yaml` in `main` remains the only domain registry. Only the orchestrator updates it (adds/removes domains). It contains no rules and no state.

2. **Domain state and config are slice-owned**: `openspec/artifacts/{domain}/state.yaml` and `openspec/artifacts/{domain}/config.yaml` belong to the agent(s) working on that domain, exactly like its artifacts. They travel in the agent's branch and are reconciled at merge time like any other slice file.

3. **Shadow state per worktree**: when several agents share one domain (different UCs), each agent worktree keeps its own untracked file `openspec/artifacts/{domain}/state.worktree.<agent>.yaml`, initialized as a copy of the domain state at worktree creation. The agent's phase skill reads/writes this file instead of `openspec/artifacts/{domain}/state.yaml`. Because it is git-ignored:
   - It survives compaction inside the worktree (recovery works as usual).
   - It is never committed, so it can never conflict at merge time.
   - Each agent's view of the workflow is local and disposable.

4. **Skill adaptation** (two compatible options):
   - **Prompt-level (no skill changes)**: the agent session prompt says: "Maintain your progress in `openspec/artifacts/<domain>/state.worktree.<agent>.yaml` following the same format and rules as the domain state. NEVER modify `openspec/artifacts/<domain>/state.yaml` nor `openspec/config.yaml` in a worktree."
   - **Skill-level (recommended, permanent)**: add a resolution rule at the top of the state-tracking sections in `up-inception` and `up-elaboration` skills: "If `openspec/artifacts/{domain}/state.worktree.*.yaml` exists, use the one named in the session prompt as your state file; the domain `state.yaml` is read-only in worktree sessions."

5. **Commit contract per agent**: an agent commit contains only code and artifacts of its own slice (disjoint paths). Before committing, the agent verifies: `git status --short` must NOT list `openspec/config.yaml` (router), or files outside its assigned slice.

6. **Pre-merge guard (orchestrator)**: before merging a branch, verify the router is untouched:

   ```powershell
   git diff main...feat/agente1 -- openspec/config.yaml
   # output must be empty
   ```

7. **Post-merge reconciliation (orchestrator)**: after each merge into `main`, the orchestrator updates the merged domain's `openspec/artifacts/{domain}/state.yaml` (mark steps done, move artifacts to `persisted`, update `notes`), optionally reading the agent's shadow state as reference. Since only the orchestrator writes the router and reconciles domain states, inconsistency is impossible by construction.

### Work Partitioning Rules

- Parallelize only **disjoint slices/steps**. Example for E15: one agent per UC (UC12 → `policies/schedule`, UC13 → `policies/absence`), respecting the backend → UI dependency inside each UC.
- Shared single-file artifacts (e.g. `05 Test/15 E15 Test plan.md`, Design System, Data Model) are owned by the orchestrator or by exactly one designated agent; other agents must not touch them.
- The domain `config.yaml` and `state.yaml` under `openspec/artifacts/{domain}/` are slice files of that domain: agents working on the domain may update them, but only the orchestrator may touch the global router `openspec/config.yaml` or state files of other domains.
- `.agents/` and `openspec/` files diverge per branch by design; only the orchestrator integrates changes to shared workflow docs.

## Step by Step

### 1. Clean starting point

```powershell
git status                  # check current WIP on main
git add -A
git commit -m "wip: baseline before parallel agents"
git push origin main        # optional but recommended
```

### 2. Create one worktree per agent

```powershell
git worktree add ..\registro-horario-agente1 -b feat/agente1
git worktree add ..\registro-horario-agente2 -b feat/agente2
git worktree add ..\registro-horario-agente3 -b feat/agente3
```

Check they exist:

```powershell
git worktree list
```

### 3. Create the shadow state file in each worktree (workflow state isolation)

Each agent needs its own untracked copy of its domain's workflow state (never committed, never merged):

```powershell
cd ..\registro-horario-agente1
git show main:openspec/artifacts/registro-horario/state.yaml > openspec/artifacts/registro-horario/state.worktree.agente1.yaml
git submodule update --init   # only if the agent touches the submodule area
# repeat for each worktree with its agent name and domain
```

The pattern `openspec/artifacts/*/state.worktree.*.yaml` is already in `.gitignore`.

### 4. Launch one opencode instance per worktree

Run each session with the worktree as working directory and a prompt that delimits its scope:

```powershell
# session 1 → C:\Users\Jesus\Desktop\DEV\proyectos\registro-horario-agente1
# prompt: "Implementa <feature A>. No toques nada fuera de <module A>.
#          Haz TDD, ejecuta los tests y commitea al terminar.
#          Mantén tu progreso en
#          openspec/artifacts/registro-horario/state.worktree.agente1.yaml
#          (mismo formato que el state del dominio). NUNCA modifiques
#          openspec/artifacts/registro-horario/state.yaml ni
#          openspec/config.yaml."
```

### 5. Agent commits in its branch

Inside each worktree, at the end of its task:

```powershell
git status --short    # MUST NOT list openspec/config.yaml,
                      # or files outside the assigned slice
git add -A
git commit -m "feat: <description>"
```

### 6. Integrate centrally on main

```powershell
git checkout main
git pull                   # if the remote advanced meanwhile

# pre-merge guard: the domain router must be untouched in the branch
git diff main...feat/agente1 -- openspec/config.yaml
# output must be empty

git merge feat/agente1
git merge feat/agente2     # resolve conflicts here if any
git merge feat/agente3
```

Then reconcile the domain workflow state (orchestrator only):

```powershell
# edit openspec/artifacts/registro-horario/state.yaml: mark merged steps
# as done, move slice artifacts to persisted, update notes.
# Reference: the agent's shadow state
# openspec/artifacts/registro-horario/state.worktree.<agent>.yaml
# (still untracked; read it before removing the worktree)
git add openspec/artifacts/registro-horario/state.yaml
git commit -m "chore: reconcile domain state after agent merges"

# run the full test suite before pushing
git push origin main
```

### 7. Cleanup

```powershell
git worktree remove ..\registro-horario-agente1
git branch -d feat/agente1
# repeat for each agent
git worktree prune
```

## Benefits Summary

| Aspect | Behavior |
|---|---|
| **Isolation** | Each agent edits only its own checkout; no accidental file mixing |
| **Parallelism** | N agents work at the same time on the same repo |
| **Central integration** | Merges and conflict resolution happen in one place (`main`) |
| **Safety** | Work is preserved in branches until reviewed and merged |
