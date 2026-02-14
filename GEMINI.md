# GEMINI.md

Project context for **Gemini CLI**. For the full architecture and agent role definitions, see `AGENTS.md` and `CLAUDE.md`.

## Project Overview

**Perfect Pair** is a personalized AI pair programming output style system. It generates and deploys witty, culturally-referenced output styles from structured YAML sources to Cursor IDE and Claude Code.

## Document Inventory

### Canonical Documents

| File | Role |
|------|------|
| `perfect-pair.md` | Standalone reference version of the output style |
| `perfect-pair-creator/source/references.yaml` | All cultural references (single source of truth) |
| `perfect-pair-creator/CLAUDE.md` | Build system architecture guide |

## Architecture Summary

### Build Pipeline

```
source/references.yaml → build.sh → generated/perfect-pair-current.md → deploy.sh → platforms
```

### Components

1. **Source Layer** — YAML reference library + personality config + base template
2. **Build Layer** — Shell script generates style markdown from sources
3. **Deploy Layer** — Transforms and copies to Cursor and Claude Code

### Deploy Targets

- **Cursor** — `~/.cursor/rules/perfect-pair.mdc`
- **Claude Code** — `~/.claude/plugins/user/perfect-pair-output-style/`

## Key Design Principles

1. **Single Source of Truth** — All references in `source/references.yaml`
2. **Idempotent Deployment** — Safe to run deploy multiple times
3. **Context Management** — Core + rotating pool prevents context bloat
4. **Platform Agnostic Generation** — Build produces neutral markdown; deploy adapts

## Sub-Agents

Gemini agents live in `.gemini/agents/`. Each has YAML frontmatter declaring available tools.

| Agent | Purpose |
|-------|---------|
| `spec-checker.md` | Validates generated output against source references |
| `build-engineer.md` | Works on build/deploy pipeline scripts |
| `style-designer.md` | Designs and refines reference content and templates |
| `test-engineer.md` | Tests the build pipeline and validates deployments |

## Multi-Tool Workflow

Gemini is optimized for **rapid exploration and second opinions**. For the full cross-referencing workflow, see the "Multi-Tool Workflow" section in `AGENTS.md`.

| Tool | Config File | Role |
|------|------------|------|
| **Codex CLI** | `AGENTS.md` | Primary implementation |
| **Claude Code** | `CLAUDE.md` | Spec compliance, architecture, review |
| **Gemini CLI** | `GEMINI.md` | Rapid exploration, second opinions |
