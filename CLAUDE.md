# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Perfect Pair** is a personalized AI pair programming output style system that brings witty cultural references (TV shows, comedians, etc.) into code conversations. It includes a build pipeline that generates and deploys output styles from structured YAML sources to both Cursor IDE and Claude Code.

This repository is currently in **active development** — the core build system works, with planned enhancements for smart rotation, config-driven generation, and multi-platform support.

## Document Inventory

### Canonical Documents

| File | Role |
|------|------|
| `perfect-pair.md` | Standalone, hand-written reference version of the complete output style |
| `perfect-pair-creator/CLAUDE.md` | Detailed build system architecture and developer guide |
| `perfect-pair-creator/WORKFLOW.md` | Daily workflow guide for managing styles |
| `perfect-pair-creator/README.md` | Project overview and quick start |

### Source Files (Single Source of Truth)

| File | Role |
|------|------|
| `perfect-pair-creator/source/references.yaml` | All cultural references — core + rotating pool |
| `perfect-pair-creator/source/config.yaml` | Personality settings (roast level, agile intensity, etc.) |
| `perfect-pair-creator/source/perfect-pair-base.md` | Template structure (currently embedded in build.sh) |

## Architecture

### Build Pipeline

```
source/references.yaml  ──┐
source/config.yaml      ──┼──> scripts/build.sh ──> generated/perfect-pair-current.md
source/perfect-pair-base.md ┘
                              ↓
                        scripts/deploy.sh
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
        ~/.cursor/rules/          ~/.claude/plugins/
        perfect-pair.mdc          perfect-pair-output-style/
```

### Two Build Paths

- `scripts/build.sh` — Shell script with the template as a heredoc. **Active build path** used by `sync.sh`.
- `scripts/build.py` — Python script using `source/perfect-pair-base.md` as a template with `{{PLACEHOLDER}}` substitution. **Not currently wired into the sync pipeline.**

### Reference Library System

- **Core** (4 entries) — always included in output
- **Rotating pool** (up to 5 active at a time) — tracked in `generated/rotation-state.json`

### Deploy Targets

- **Cursor**: `~/.cursor/rules/perfect-pair.mdc` (auto-applies to all projects)
- **Claude Code**: `~/.claude/plugins/user/perfect-pair-output-style/hooks-handlers/session-start.sh`

## Key Commands

```bash
cd perfect-pair-creator

# Full build + deploy cycle
./scripts/sync.sh

# Build only (generates generated/perfect-pair-current.md)
./scripts/build.sh

# Deploy only (pushes to ~/.cursor/rules/ and ~/.claude/plugins/)
./scripts/deploy.sh
```

## Key Design Principles

1. **Single Source of Truth** — All references live in `source/references.yaml`. Edit there, rebuild, done.
2. **Idempotent Deployment** — `deploy.sh` can be run multiple times safely. Overwrites existing files, creates dirs if missing, never deletes user data.
3. **Context Management** — Core + rotating pool architecture prevents context bloat as the reference library grows.
4. **Platform Agnostic Generation** — Build step produces platform-neutral markdown; deploy step transforms for each target.

## Don't Edit Directly

- `generated/perfect-pair-current.md` — build output, overwritten by build.sh
- `cursor-versions/modern/.cursor/rules/perfect-pair.mdc` — overwritten by deploy.sh

## Config.yaml Is Not Yet Wired

`source/config.yaml` defines personality settings (roast level, agile intensity, pushback style, formality) but `build.sh` does not read it. These settings are documented-only for now.

## Custom Agents (`.claude/agents/`)

| Agent | Purpose |
|-------|---------|
| `spec-checker.md` | Validates generated output against source references and config. |
| `build-engineer.md` | Works on the build/deploy pipeline scripts. |
| `style-designer.md` | Designs and refines reference content, templates, and output style. |
| `test-engineer.md` | Tests the build pipeline and validates deployments. |

## Multi-Tool Setup

This project uses three AI coding assistants in parallel:

| Tool | Config File | Agents | Role |
|------|------------|--------|------|
| **Codex CLI** | `AGENTS.md` | Embedded role sections | Primary implementation |
| **Claude Code** | `CLAUDE.md` | `.claude/agents/` | Spec compliance, architecture, review |
| **Gemini CLI** | `GEMINI.md` | `.gemini/agents/` | Rapid exploration, second opinions |

See `AGENTS.md` for the full cross-referencing workflow and example commands.
