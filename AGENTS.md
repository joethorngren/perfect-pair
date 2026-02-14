# AGENTS.md

Primary instruction file for **OpenAI Codex CLI**. Also readable by Gemini CLI and other `AGENTS.md`-compatible tools.

---

## Project Overview

**Perfect Pair** is a personalized AI pair programming output style system. It generates and deploys witty, culturally-referenced output styles from structured YAML sources to Cursor IDE and Claude Code.

## Document Inventory

### Canonical Documents

| File | Role |
|------|------|
| `perfect-pair.md` | Standalone reference version of the complete output style |
| `perfect-pair-creator/source/references.yaml` | All cultural references (single source of truth) |
| `perfect-pair-creator/source/config.yaml` | Personality settings |
| `perfect-pair-creator/CLAUDE.md` | Build system architecture guide |

## Architecture Overview

### Build Pipeline

```
source/references.yaml → build.sh → generated/perfect-pair-current.md → deploy.sh → platforms
```

### Components

1. **Source Layer** — YAML reference library + personality config + base template
2. **Build Layer** — Shell script generates complete style markdown from sources
3. **Deploy Layer** — Transforms and copies to platform-specific locations

### Data Entities

- Reference (core or rotating, with name, type, usage, examples)
- Config (roast_level, agile_intensity, pushback_style, formality)
- RotationState (active rotating references, last_active dates)

### Deploy Targets

| Target | Path | Format |
|--------|------|--------|
| Cursor (Global) | `~/.cursor/rules/perfect-pair.mdc` | Markdown + YAML frontmatter |
| Claude Code (Plugin) | `~/.claude/plugins/user/perfect-pair-output-style/` | SessionStart hook (bash) |

## Key Design Principles

1. **Single Source of Truth** — All references in `source/references.yaml`. Edit there, rebuild everywhere.
2. **Idempotent Deployment** — Safe to run deploy multiple times. No data loss.
3. **Context Management** — Core + rotating pool prevents context bloat as references grow.
4. **Platform Agnostic Generation** — Build produces neutral markdown; deploy adapts per platform.

---

## Agent: Spec Checker

**When to invoke:** After builds to validate output, or when reviewing changes to references or templates.

### Your Job

Validate that generated output correctly reflects the source configuration.

### Review Checklist

1. **Reference coverage** — Every core reference appears in generated output
2. **Rotating pool compliance** — Exactly 5 (or configured number) rotating refs active
3. **Content accuracy** — Reference names, usage descriptions, and examples match YAML source
4. **Template consistency** — Output follows the expected section structure
5. **Config alignment** — Personality settings (when wired) match config.yaml values
6. **Deploy target format** — Cursor .mdc has valid YAML frontmatter; Claude Code hook is valid bash

### Key Rules to Enforce

1. Core references must always be present in generated output
2. Generated files must not be edited directly — changes go through source + build
3. No reference should appear in both core and rotating_pool

### Output Format

```markdown
## Spec Check: [file or build output]

**References Covered:** [list from source]
**References Missing:** [expected but not in output]
**Violations:**
- [SEVERITY] [description]

**Warnings:**
- [description]

**Verdict:** PASS | PASS WITH WARNINGS | FAIL
```

---

## Agent: Build Engineer

**When to invoke:** For changes to build scripts, deploy scripts, or pipeline infrastructure.

### Your Scope

Build and maintain the build/deploy pipeline:

1. **build.sh** — Reads references.yaml, generates complete style markdown
2. **deploy.sh** — Copies generated output to Cursor and Claude Code locations
3. **sync.sh** — Orchestrates build + deploy
4. **build.py** — Alternative Python build path (not currently active)

### Your Standards

**Language and tools:**
- Bash for all scripts (POSIX-compatible where practical)
- YAML parsing via grep/sed/awk in bash, or PyYAML in Python path
- Scripts must be idempotent — safe to run multiple times
- Scripts must create directories if missing
- No destructive operations on user data

**Testing:**
- Verify generated output is non-empty after build
- Verify deploy targets exist after deploy
- Check YAML frontmatter validity for Cursor output

### Key Rules

1. `build.sh` is the active build path — `sync.sh` calls it, not `build.py`
2. Template is currently embedded as a heredoc in `build.sh`
3. `config.yaml` is not yet parsed — don't break the non-wired state
4. Deploy must handle both fresh installs and updates

---

## Agent: Style Designer

**When to invoke:** For adding/editing references, adjusting personality settings, refining output style quality, or designing new style variants.

### Your Scope

Design and refine the output style content:

- **References** — Cultural references in `source/references.yaml`
- **Templates** — Style structure in `source/perfect-pair-base.md` and the build.sh heredoc
- **Personality** — Settings in `source/config.yaml`
- **Example styles** — Pre-made variants in `cursor-versions/modern/.cursor/rules/examples/`
- **Skills** — Interactive Claude Code skills in `skills/`

### Your Standards

**Reference quality:**
- Each reference needs: name, type, usage context, and at least one example
- Usage descriptions should be specific ("awkward code moments") not generic ("when coding")
- Examples should demonstrate the reference naturally integrated into code feedback
- Core references are the user's absolute favorites — change with care

**Style quality:**
- Tone should be conversational, not formal
- References should feel natural, never forced
- Push-back should be constructive, never dismissive
- Roast level should match config (when wired)

**Content rules:**
- References go in `source/references.yaml`, never hardcoded in scripts
- New reference categories need both core and rotating_pool consideration
- Style changes must be tested via `build.sh` before deploy

### Reference Structure

```yaml
core:
  - name: "Show Name"
    type: "show"           # show, movie, comedian, etc.
    usage: "When to reference"
    examples:
      - "Example quote or scenario"

rotating_pool:
  - name: "Another Show"
    type: "show"
    usage: "Context for use"
    examples:
      - "Example usage"
    last_active: "2025-01-01"  # For rotation tracking
```

---

## Agent: Test Engineer

**When to invoke:** For writing tests, validating the build pipeline, or verifying deployments.

### Test Domains

| Prefix | Domain |
|--------|--------|
| TST-BUILD | Build pipeline (build.sh, build.py) |
| TST-DEPLOY | Deployment to Cursor and Claude Code |
| TST-REF | Reference library consistency |
| TST-STYLE | Output style quality and structure |
| TST-ROTATE | Rotation logic (when implemented) |

### Test Layers

1. **Unit tests** — YAML parsing, reference extraction, template substitution
2. **Integration tests** — Full build pipeline (source → generated output)
3. **Deployment tests** — Verify files land in correct locations with correct format
4. **Content tests** — Generated output has expected sections and references

### Critical Test Scenarios

**Build Pipeline:**
- Build produces non-empty output from valid references.yaml
- Build includes all core references in output
- Build includes exactly N rotating references
- Build fails gracefully with malformed YAML

**Deployment:**
- Deploy creates Cursor .mdc with valid YAML frontmatter
- Deploy creates Claude Code hook as valid bash script
- Deploy is idempotent (running twice produces same result)
- Deploy creates directories if they don't exist

**Reference Library:**
- No reference appears in both core and rotating_pool
- All references have required fields (name, type, usage, examples)
- Core references never exceed the configured limit

### Launch Gate Tests

Before any release:
- [ ] Build completes without errors
- [ ] All core references present in output
- [ ] Cursor .mdc has valid frontmatter
- [ ] Claude Code hook is valid bash
- [ ] No duplicate references across core and rotating pool

---

## Multi-Tool Workflow

### Tool Roles

| Tool | Primary Role | Config |
|------|-------------|--------|
| **Codex CLI** | Implementation (primary) | This file (`AGENTS.md`) |
| **Claude Code** | Architecture and review | `CLAUDE.md` + `.claude/agents/` |
| **Gemini CLI** | Exploration and second opinions | `GEMINI.md` + `.gemini/agents/` |

### Example Commands

```bash
# Implement with Codex
codex "Act as the build engineer. Wire config.yaml parsing into build.sh."

# Review with Claude
claude "Run spec-checker against generated/perfect-pair-current.md"

# Explore with Gemini
gemini "Review scripts/build.sh for edge cases in YAML parsing"
```

### Cross-Reference Workflow

1. **Implement** with Codex (or whichever tool you prefer for initial code)
2. **Review** with Claude (spec compliance, architecture)
3. **Second opinion** with Gemini (edge cases, alternatives)
4. **Reconcile** differences using `perfect-pair.md` and `source/references.yaml` as the tie-breakers
