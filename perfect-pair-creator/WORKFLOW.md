# Perfect Pair Workflow Guide

Your streamlined workflow for managing your Perfect Pair style across Cursor, Claude Code, Gemini CLI, and Codex CLI.

## Quick Start

### 1. Edit Your References

Edit `source/references.yaml` to add/remove shows:

```yaml
core:
  - name: "Your Favorite Show"
    type: "show"
    usage: "When to use these references"
    examples:
      - "Example quote or situation"

rotating_pool:
  - name: "Another Show"
    type: "show"
    usage: "Context for this reference"
    examples:
      - "Example usage"
```

### 2. Adjust Personality (Optional)

Edit `source/config.yaml` to tune the output tone:

```yaml
style_settings:
  roast_level: 3        # 1=minimal, 4=maximum roasting
  agile_intensity: 3    # 1=aware, 4=evangelist
  pushback_style: 3     # 1=trust, 4=devil's advocate
  formality: 2          # 1=professional, 4=best friend
```

### 3. Build & Deploy

```bash
./scripts/sync.sh
```

Changes are now live in all 4 tools:
- **Cursor** — Immediate (new projects)
- **Claude Code** — Restart to see changes
- **Gemini CLI** — New session or `/memory refresh`
- **Codex CLI** — New session

## File Structure

```
perfect-pair-creator/
├── source/
│   ├── references.yaml              # Your reference library (EDIT THIS)
│   ├── config.yaml                  # Personality settings (EDIT THIS)
│   └── perfect-pair-base.md         # Template (rarely edited)
├── generated/
│   ├── perfect-pair-current.md      # Generated output
│   └── rotation-state.json          # Tracks active refs
└── scripts/
    ├── sync.sh                      # Main command (venv + build + deploy)
    ├── build.py                     # Python build (primary)
    ├── deploy.sh                    # Deploy to all 4 tools
    └── build.sh                     # Legacy (not used)
```

## Daily Workflow

### Add a New Reference

```bash
# 1. Edit references
code source/references.yaml
# Add "Community" to rotating_pool

# 2. Sync everywhere
./scripts/sync.sh

# Done! Available in all 4 tools
```

### Change Personality

```bash
# 1. Edit config
code source/config.yaml
# Change roast_level from 3 to 2

# 2. Sync
./scripts/sync.sh

# Output tone changes across all tools
```

### Test Before Deploying

```bash
# Build only (no deploy)
.venv/bin/python scripts/build.py

# Review the generated output
cat generated/perfect-pair-current.md

# If it looks good, deploy
./scripts/deploy.sh
```

## Common Tasks

### Move a Reference to Core

1. Cut the entry from `rotating_pool:` in `source/references.yaml`
2. Paste it under `core:`
3. Run `./scripts/sync.sh`

### Adjust Roast Level

Edit `source/config.yaml`:
- **Level 1** — Gentle, encouraging feedback
- **Level 2** — Light teasing, mostly supportive
- **Level 3** — Solid roasting with love (default)
- **Level 4** — Maximum roast, comedy roast energy

### Preview Without Deploying

```bash
.venv/bin/python scripts/build.py
cat generated/perfect-pair-current.md
```

## Deploy Target Details

| Tool | Path | When Changes Apply |
|------|------|--------------------|
| Cursor | `~/.cursor/rules/perfect-pair.mdc` | New projects immediately |
| Claude Code | `~/.claude/plugins/user/perfect-pair-output-style/` | After restart |
| Gemini CLI | `~/.gemini/perfect-pair-style.md` | New session |
| Codex CLI | `~/.codex/AGENTS.md` | New session |

### dotfiles-ai Users

If your tool configs are managed by `~/.dotfiles-ai/` via GNU Stow, `deploy.sh` automatically detects the symlinks and writes to the repo paths instead. No extra steps needed.

## Tips

1. **Core vs Rotating**: Put your top 3-5 favorites in `core`, rest in `rotating_pool`
2. **Edit Once, Deploy Everywhere**: Change source files, run `sync.sh`
3. **Test First**: Run `build.py` to preview before deploying
4. **Version Control**: Commit your changes to track evolution
5. **Config Matters**: `config.yaml` settings actually change the output — experiment with different levels

## Sharing with Team

```bash
git add source/references.yaml source/config.yaml
git commit -m "Updated references and personality settings"
git push

# Team members pull and sync
git pull
./scripts/sync.sh
```

## Reference Rotation (Coming Soon)

As your library grows beyond 15-20 entries:
- Core references stay always active
- 5 rotating refs cycle weekly from the pool
- Tracked in `generated/rotation-state.json`
- Smart rotation based on usage patterns

---

**Questions?** Check the main [README.md](README.md) or open an issue!
