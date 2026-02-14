# GEMINI.md

Project context for **Gemini CLI**. For the full architecture and agent role definitions, see `AGENTS.md` and `CLAUDE.md`.

## Project Overview

**Perfect Pair** is a personalized AI pair programming output style system. It generates and deploys witty, culturally-referenced output styles from structured YAML sources to Cursor IDE, Claude Code, Gemini CLI, and Codex CLI.

## Document Inventory

### Canonical Documents

| File | Role |
|------|------|
| `perfect-pair.md` | Standalone reference version of the output style |
| `perfect-pair-creator/source/references.yaml` | All cultural references (single source of truth) |
| `perfect-pair-creator/source/config.yaml` | Personality settings (drives output tone) |
| `perfect-pair-creator/CLAUDE.md` | Build system architecture guide |

## Architecture Summary

### Build Pipeline

```
source/references.yaml + config.yaml → build.py (venv) → generated/perfect-pair-current.md → deploy.sh → 4 tools
```

### Components

1. **Source Layer** — YAML reference library + personality config + markdown template
2. **Build Layer** — Python script generates style markdown via template substitution
3. **Deploy Layer** — Adapts and copies to Cursor, Claude Code, Gemini CLI, and Codex CLI

### Deploy Targets

- **Cursor** — `~/.cursor/rules/perfect-pair.mdc` (global rule, alwaysApply)
- **Claude Code** — `~/.claude/plugins/user/perfect-pair-output-style/` (SessionStart hook)
- **Gemini CLI** — `~/.gemini/perfect-pair-style.md` (`@import` in GEMINI.md)
- **Codex CLI** — `~/.codex/AGENTS.md` (global instructions)

## Key Design Principles

1. **Single Source of Truth** — All references in `source/references.yaml`
2. **Idempotent Deployment** — Safe to run deploy multiple times
3. **Context Management** — Core + rotating pool prevents context bloat
4. **Platform Agnostic Generation** — Build produces neutral markdown; deploy adapts
5. **Config-Driven Personality** — config.yaml settings actively shape output

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
