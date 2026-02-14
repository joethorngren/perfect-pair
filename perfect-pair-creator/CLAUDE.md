# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Perfect Pair Creator is a system for generating personalized AI pair programming styles that deploy to both Cursor IDE and Claude Code. It uses a reference library architecture with a build/deploy pipeline that transforms YAML configuration into platform-specific output styles.

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

The system has three phases:

1. **Source**: Reference library (YAML) + personality config + base template
2. **Build**: Generate complete style markdown from sources
3. **Deploy**: Transform and copy to platform-specific locations

### Single Source of Truth

- `source/references.yaml` - All cultural references (shows, movies, comedians)
- `source/config.yaml` - Personality settings (roast level, agile intensity, etc.)
- `source/perfect-pair-base.md` - Template structure (currently embedded in build.sh)

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

This design solves the context management problem: as users add more references, we can rotate which ones are active while keeping core favorites constant.

### Dual Deployment Targets

**Cursor (Global Rules)**
- Deploys to: `~/.cursor/rules/perfect-pair.mdc`
- Format: Markdown with YAML frontmatter
- Scope: All projects automatically
- Can be overridden per-project in `.cursor/rules/`

**Claude Code (Plugin Hook)**
- Deploys to: `~/.claude/plugins/user/perfect-pair-output-style/`
- Format: SessionStart hook (bash script that outputs markdown)
- Scope: All Claude Code sessions
- Requires restart to see changes

## Key Commands

### Build and Deploy

```bash
# Main workflow - build from sources and deploy everywhere
./scripts/sync.sh

# Or run separately:
./scripts/build.sh    # Generate from references.yaml
./scripts/deploy.sh   # Deploy to Cursor + Claude Code
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

### Interactive Skills

Two skills are available in `skills/`:

**`/update-perfect-pair`** - Comprehensive customization
- Add/remove references
- Adjust roast level (1-4)
- Adjust agile intensity (1-4)
- Adjust push-back style (1-4)
- Adjust formality (1-4)
- Interactive prompts for all changes

**`/create-perfect-pair`** - Generate completely new styles
- For creating variant styles from scratch
- Used to create the example styles

## Critical Files

### Source Files
- `source/references.yaml` - **EDIT THIS** to add/remove references
- `source/config.yaml` - Personality settings (future: will be read by build script)
- `source/perfect-pair-base.md` - Template (currently unused, embedded in build.sh)

### Build Scripts
- `scripts/build.sh` - Reads references.yaml, generates output
- `scripts/deploy.sh` - Copies to Cursor + Claude Code locations
- `scripts/sync.sh` - Wrapper: build + deploy

### Generated
- `generated/perfect-pair-current.md` - Build output (don't edit directly)
- `generated/rotation-state.json` - Tracks active rotating references

### Skills
- `skills/update-perfect-pair/SKILL.md` - Interactive customization
- `skills/create-perfect-pair/SKILL.md` - Generate new styles

## Important Patterns

### Build Script Embeds Content

`build.sh` currently has the template embedded as a heredoc. This means:
- Changes to style structure require editing `build.sh`
- The build script is the source of truth for output format
- Future: should read from `source/perfect-pair-base.md` template

### Deployment is Idempotent

`deploy.sh` can be run multiple times safely:
- Overwrites existing files
- Creates directories if missing
- Never deletes user data

### Config.yaml is Not Yet Read

`source/config.yaml` exists but isn't currently parsed by `build.sh`. Future enhancement would:
1. Parse config.yaml in build.sh
2. Adjust output based on settings (more/fewer roast examples, etc.)
3. Allow `./scripts/sync.sh` to apply personality changes

## Future Architecture

### Smart Rotation (Planned)

When the reference library grows beyond 15-20 entries:
1. Keep all core references active
2. Rotate 5 from rotating_pool weekly
3. Track usage in rotation-state.json
4. Prioritize frequently-used references

Script location: `scripts/rotate.sh` (to be created)

### Config-Driven Generation (Planned)

Currently personality settings in `config.yaml` are documented but not used. Future:
- Parse config.yaml in build.sh
- Generate more/fewer examples based on roast_level
- Adjust language based on agile_intensity
- Modify tone based on formality

### Multi-Platform Support (Planned)

Currently supports Cursor and Claude Code. Extensible to:
- Gemini CLI
- GitHub Copilot
- Other AI coding tools

Would require new deploy targets in `deploy.sh`.

## Working with This Codebase

### Adding a New Reference

1. Edit `source/references.yaml`
2. Add to `core:` or `rotating_pool:`
3. Run `./scripts/sync.sh`
4. Restart Claude Code to see changes (Cursor picks up automatically)

### Changing Build Output Format

1. Edit the heredoc in `scripts/build.sh` (lines 14-300+)
2. Modify template structure
3. Run `./scripts/build.sh` to test
4. Run `./scripts/deploy.sh` when ready

### Adding a New Personality Setting

1. Add to `source/config.yaml` under `style_settings:`
2. Update `scripts/build.sh` to parse the setting
3. Modify output generation based on the setting
4. Update `/update-perfect-pair` skill to prompt for it

### Testing Changes

```bash
# Build and check output
./scripts/build.sh
cat generated/perfect-pair-current.md

# Deploy to test locally
./scripts/deploy.sh

# For Cursor: Changes apply immediately in new projects
# For Claude Code: Restart to see changes
```

## Skills Usage

Skills are copied to `~/.claude/skills/` for Claude Code use.

When updating a skill:
1. Edit `skills/[skill-name]/SKILL.md`
2. Copy to `~/.claude/skills/`:
   ```bash
   cp -r skills/update-perfect-pair ~/.claude/skills/
   ```
3. Restart Claude Code or start new session

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

The repo contains both:
- **Source files** for the build system (this is the active development)
- **Example styles** in `cursor-versions/modern/.cursor/rules/examples/`

When making changes, edit source files and rebuild rather than editing examples directly.
