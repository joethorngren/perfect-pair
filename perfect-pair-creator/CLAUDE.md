# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Perfect Pair Creator is a system for generating personalized AI pair programming styles that deploy to Cursor IDE, Claude Code, Gemini CLI, and Codex CLI. It uses a reference library architecture with a Python build pipeline that transforms YAML configuration into platform-specific output styles.

## Architecture

### Build Pipeline

```
source/references.yaml    ──┐
source/config.yaml        ──┼──> scripts/build.py ──> generated/perfect-pair-current.md
source/perfect-pair-base.md ┘    (via .venv + PyYAML)
                                          ↓
                                    scripts/deploy.sh
                                          ↓
              ┌──────────┬──────────┬──────────┐
              ↓          ↓          ↓          ↓
       ~/.cursor/  ~/.claude/  ~/.gemini/  ~/.codex/
       rules/      plugins/   style.md    AGENTS.md
```

The system has three phases:

1. **Source**: Reference library (YAML) + personality config + base template
2. **Build**: Python generates complete style markdown from sources via `{{PLACEHOLDER}}` substitution
3. **Deploy**: Adapts and copies to 4 platform-specific locations

### Single Source of Truth

- `source/references.yaml` - All cultural references (shows, movies, comedians)
- `source/config.yaml` - Personality settings that actively drive output tone
- `source/perfect-pair-base.md` - Template with `{{PLACEHOLDER}}` substitution points

### Reference Library System

References are divided into two categories:

**Core** - Always included (4 references currently)
- Reserved for absolute favorites
- Always present in generated output
- Located under `core:` in references.yaml

**Rotating Pool** - Rotate in/out to manage context
- Currently 5 active at a time
- Designed for future smart rotation (weekly/size-based)
- Located under `rotating_pool:` in references.yaml
- Tracks `last_active` date for rotation logic

### Config-Driven Personality

`source/config.yaml` settings actively drive the generated output:

| Setting | Range | Effect |
|---------|-------|--------|
| `roast_level` | 1-4 | Controls roast guidance text and number of examples |
| `agile_intensity` | 1-4 | Scales agile section from practical tips to evangelist |
| `pushback_style` | 1-4 | Ranges from trust-based to devil's advocate |
| `formality` | 1-4 | Adjusts tone from professional to best-friend casual |

### Deploy Targets

**Cursor (Global Rules)**
- Deploys to: `~/.cursor/rules/perfect-pair.mdc`
- Format: Markdown with YAML frontmatter (`alwaysApply: true`)
- Scope: All projects automatically

**Claude Code (Plugin Hook)**
- Deploys to: `~/.claude/plugins/user/perfect-pair-output-style/`
- Format: SessionStart hook (bash script outputting JSON with `hookSpecificOutput.additionalContext`)
- Scope: All Claude Code sessions

**Gemini CLI (Global Context)**
- Deploys to: `~/.gemini/perfect-pair-style.md` with `@import` in `~/.gemini/GEMINI.md`
- Format: Plain markdown (YAML frontmatter stripped)
- Scope: All Gemini sessions

**Codex CLI (Global Instructions)**
- Deploys to: `~/.codex/AGENTS.md`
- Format: Plain markdown (YAML frontmatter stripped)
- Scope: All Codex sessions

All targets are **dotfiles-ai stow-aware** — deploy.sh detects symlinks into `~/.dotfiles-ai/` and writes to the repo paths directly.

## Key Commands

### Build and Deploy

```bash
# Main workflow - build from sources and deploy everywhere
./scripts/sync.sh

# Or run separately:
.venv/bin/python scripts/build.py    # Generate from sources
./scripts/deploy.sh                   # Deploy to all 4 tools
```

### Editing References

Edit `source/references.yaml` directly:
```yaml
core:
  - name: "Show Name"
    type: "show"
    usage: "When to reference this"
    examples:
      - "Quote or situation"

rotating_pool:
  - name: "Another Show"
    # same structure
```

After editing, run `./scripts/sync.sh` to rebuild and deploy.

### Adjusting Personality

Edit `source/config.yaml`:
```yaml
style_settings:
  roast_level: 3        # 1=minimal, 4=maximum roasting
  agile_intensity: 3    # 1=aware, 4=evangelist
  pushback_style: 3     # 1=trust, 4=devil's advocate
  formality: 2          # 1=professional, 4=best friend
```

After editing, run `./scripts/sync.sh` to rebuild and deploy.

### Interactive Skills

Two skills are available in `skills/`:

**`/update-perfect-pair`** - Comprehensive customization
- Add/remove references
- Adjust personality settings
- Interactive prompts for all changes

**`/create-perfect-pair`** - Generate completely new styles
- For creating variant styles from scratch

## Critical Files

### Source Files
- `source/references.yaml` - **EDIT THIS** to add/remove references
- `source/config.yaml` - **EDIT THIS** to adjust personality
- `source/perfect-pair-base.md` - Template with `{{PLACEHOLDER}}` substitution

### Build Scripts
- `scripts/build.py` - **Primary build path**. Reads all sources, generates output.
- `scripts/deploy.sh` - Deploys to all 4 tool locations
- `scripts/sync.sh` - Wrapper: venv setup + build + deploy
- `scripts/build.sh` - Legacy (hardcoded heredoc, not used by sync)

### Generated
- `generated/perfect-pair-current.md` - Build output (don't edit directly)
- `generated/rotation-state.json` - Tracks active rotating references

### Skills
- `skills/update-perfect-pair/SKILL.md` - Interactive customization
- `skills/create-perfect-pair/SKILL.md` - Generate new styles

## Important Patterns

### Template-Based Generation

`build.py` reads `source/perfect-pair-base.md` as a template and replaces placeholders:
- `{{DESCRIPTION_REFS}}` — comma-separated list of active reference names
- `{{PHILOSOPHY_OPENING}}` — opening paragraph with active reference callbacks
- `{{REFERENCES_LIST}}` — bullet-point list of active references with usage
- `{{ROAST_GUIDANCE}}` — roast section guidance (driven by `roast_level`)
- `{{ROAST_EXAMPLES}}` — roast examples (count driven by `roast_level`)
- `{{PUSHBACK_GUIDANCE}}` — pushback section (driven by `pushback_style`)
- `{{AGILE_GUIDANCE}}` — agile section (driven by `agile_intensity`)
- `{{FORMALITY_NOTE}}` — formality note (driven by `formality`)

Unreplaced placeholders trigger a build warning.

### Deployment is Idempotent

`deploy.sh` can be run multiple times safely:
- Overwrites existing files
- Creates directories if missing
- Never deletes user data
- Gemini `@import` is added only once (idempotent check)

### dotfiles-ai Integration

Deploy targets at `~/.cursor/rules/`, `~/.claude/plugins/`, `~/.gemini/`, and `~/.codex/` are typically stow symlinks managed by `~/.dotfiles-ai/`. Deploy.sh detects this and writes to the repo paths directly, keeping dotfiles-ai clean.

## Future Architecture

### Smart Rotation (Planned)

When the reference library grows beyond 15-20 entries:
1. Keep all core references active
2. Rotate 5 from rotating_pool weekly
3. Track usage in rotation-state.json
4. Prioritize frequently-used references

Script location: `scripts/rotate.sh` (to be created)

## Working with This Codebase

### Adding a New Reference

1. Edit `source/references.yaml`
2. Add to `core:` or `rotating_pool:`
3. Run `./scripts/sync.sh`
4. All 4 tools pick up changes (Claude Code needs restart)

### Changing Personality

1. Edit `source/config.yaml` — adjust any setting (1-4 scale)
2. Run `./scripts/sync.sh`
3. Output tone changes across all 4 tools

### Changing Template Structure

1. Edit `source/perfect-pair-base.md`
2. If adding a new `{{PLACEHOLDER}}`, add the generator in `scripts/build.py`
3. Run `./scripts/sync.sh`

### Testing Changes

```bash
# Build and check output
.venv/bin/python scripts/build.py
cat generated/perfect-pair-current.md

# Deploy to test locally
./scripts/deploy.sh

# For Cursor: Changes apply immediately in new projects
# For Claude Code: Restart to see changes
# For Gemini: /memory refresh or new session
# For Codex: New session
```

## Repository Structure Context

```
source/          # Single source of truth - edit these
scripts/         # Build/deploy pipeline
generated/       # Build output - don't edit directly
skills/          # Claude Code interactive skills
cursor-versions/ # Cursor-specific files and examples
  modern/        # Cursor rules format
  skills/        # Cursor 2.4+ skills
```

When making changes, edit source files and rebuild rather than editing generated output directly.
