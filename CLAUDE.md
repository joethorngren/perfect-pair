# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Perfect Pair** is a personalized AI pair programming output style system that brings witty cultural references (TV shows, comedians, etc.) into code conversations. It includes a build pipeline that generates and deploys output styles from structured YAML sources to four AI coding tools.

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
| `perfect-pair-creator/source/config.yaml` | Personality settings (roast level, agile intensity, pushback style, formality) |
| `perfect-pair-creator/source/perfect-pair-base.md` | Template with `{{PLACEHOLDER}}` substitution |

## Architecture

### Build Pipeline

```
source/references.yaml    ──┐
source/config.yaml        ──┼──> build.py ──> generated/perfect-pair-current.md
source/perfect-pair-base.md ┘         (via venv + PyYAML)
                                          ↓
                                    scripts/deploy.sh
                                          ↓
                    ┌──────────┬──────────┼──────────┐
                    ↓          ↓          ↓          ↓
             ~/.cursor/  ~/.claude/  ~/.gemini/  ~/.codex/
             rules/      plugins/   style.md    AGENTS.md
```

### Primary Build Path

`scripts/build.py` is the primary build script. It:
- Reads `references.yaml` for cultural references (core + active rotating)
- Reads `config.yaml` for personality settings that drive output tone
- Reads `rotation-state.json` for which rotating refs are active
- Uses `perfect-pair-base.md` as the template with `{{PLACEHOLDER}}` substitution
- Warns if any placeholders remain unreplaced

`scripts/sync.sh` orchestrates the full pipeline: creates a venv, installs PyYAML, runs build.py, then runs deploy.sh.

`scripts/build.sh` is the legacy build path (hardcoded heredoc, does not read sources). Kept for reference but not used by sync.sh.

### Config-Driven Personality

`source/config.yaml` settings actively drive the generated output:

| Setting | Range | Effect |
|---------|-------|--------|
| `roast_level` | 1-4 | Controls roast guidance text and number of examples |
| `agile_intensity` | 1-4 | Scales agile section from practical tips to evangelist |
| `pushback_style` | 1-4 | Ranges from trust-based to devil's advocate |
| `formality` | 1-4 | Adjusts tone from professional to best-friend casual |

### Reference Library System

- **Core** (4 entries) — always included in output
- **Rotating pool** (up to 5 active at a time) — tracked in `generated/rotation-state.json`

### Deploy Targets

| Target | Path | Format |
|--------|------|--------|
| **Cursor** | `~/.cursor/rules/perfect-pair.mdc` | Markdown + YAML frontmatter (`alwaysApply: true`) |
| **Claude Code** | `~/.claude/plugins/user/perfect-pair-output-style/` | SessionStart hook (JSON-wrapped bash) |
| **Gemini CLI** | `~/.gemini/perfect-pair-style.md` | `@import` in global GEMINI.md |
| **Codex CLI** | `~/.codex/AGENTS.md` | Global instructions file |

All targets are **dotfiles-ai stow-aware** — deploy.sh detects symlinks and writes to the `~/.dotfiles-ai/` repo paths when stow management is detected.

## Key Commands

```bash
cd perfect-pair-creator

# Full build + deploy cycle (all 4 tools)
./scripts/sync.sh

# Build only (generates generated/perfect-pair-current.md)
.venv/bin/python scripts/build.py

# Deploy only (pushes to all 4 tool locations)
./scripts/deploy.sh
```

## Key Design Principles

1. **Single Source of Truth** — All references live in `source/references.yaml`. Edit there, rebuild, done.
2. **Idempotent Deployment** — `deploy.sh` can be run multiple times safely. Never deletes user data.
3. **Context Management** — Core + rotating pool architecture prevents context bloat.
4. **Platform Agnostic Generation** — Build produces platform-neutral markdown; deploy adapts per target.
5. **dotfiles-ai Integration** — Deploy detects stow symlinks and writes to repo paths transparently.

## Don't Edit Directly

- `generated/perfect-pair-current.md` — build output, overwritten by build.py
- `cursor-versions/modern/.cursor/rules/perfect-pair.mdc` — overwritten by deploy.sh

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
