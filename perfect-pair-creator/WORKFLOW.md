# Perfect Pair Workflow Guide

Your streamlined workflow for managing your Perfect Pair style across Claude Code and Cursor.

## 🎯 Quick Start

### 1. Edit Your References

Edit `source/references.yaml` to add/remove shows:

```bash
# Edit in your favorite editor
code source/references.yaml

# Add to core (always included):
core:
  - name: "Your Favorite Show"
    type: "show"
    usage: "When to use these references"
    examples:
      - "Example quote or situation"

# Or add to rotating pool:
rotating_pool:
  - name: "Another Show"
    type: "show"
    usage: "Context for this reference"
    examples:
      - "Example usage"
```

### 2. Build & Deploy

```bash
# From the perfect-pair-creator directory
./scripts/sync.sh
```

That's it! Your changes are now in:
- Claude Code (restart to see changes)
- Cursor (copy to your project)

## 📂 File Structure

```
perfect-pair-creator/
├── source/
│   ├── references.yaml              # ✏️  EDIT THIS - Your reference library
│   ├── perfect-pair-base.md         # Template (rarely edited)
│   └── config.yaml                  # Rotation settings (future)
├── generated/
│   ├── perfect-pair-current.md      # 🤖 Generated output
│   └── rotation-state.json          # Tracks active refs
└── scripts/
    ├── sync.sh                       # 🚀 Main command (build + deploy)
    ├── build.sh                      # Build from sources
    └── deploy.sh                     # Deploy to platforms
```

## 🔄 Daily Workflow

### Option A: Manual Sync (Recommended)

```bash
# 1. Edit your references
code source/references.yaml

# 2. Sync everywhere
./scripts/sync.sh

# Done!
```

### Option B: Watch Mode (Future)

```bash
# Auto-sync on file changes
./scripts/watch.sh
```

## 📝 Common Tasks

### Add a New Reference

```bash
# Edit references.yaml
code source/references.yaml

# Add to core or rotating_pool, then sync
./scripts/sync.sh
```

### Test Your Changes

```bash
# Build and check output
./scripts/build.sh

# Review generated file
cat generated/perfect-pair-current.md

# Deploy when ready
./scripts/deploy.sh
```

### Use in Cursor

Good news - it's already deployed globally! The deploy script puts it at `~/.cursor/rules/` which applies to all your projects automatically.

**To override per-project:**
```bash
# Create project-specific rules that override global
mkdir -p <your-project>/.cursor/rules
code <your-project>/.cursor/rules/custom.mdc
```

**Cursor rule priority:**
1. Project rules (`.cursor/rules/` in project)
2. Global rules (`~/.cursor/rules/`)
3. Default behavior

## 🔄 Reference Rotation (Coming Soon)

### Current State
Right now, all core + first 5 rotating refs are included.

### Future: Smart Rotation

```bash
# Rotate to next set of references
./scripts/rotate.sh

# See what's active
./scripts/status.sh

# Set up weekly auto-rotation
./scripts/setup-cron.sh weekly
```

This will automatically:
- Keep core references always active
- Rotate 5 references from the pool weekly
- Keep context size manageable
- Track which refs you use most

## 💡 Tips

1. **Core vs Rotating**: Put your top 3-5 favorites in `core`, rest in `rotating_pool`
2. **Edit Once**: Change `references.yaml`, sync everywhere
3. **Test First**: Run `build.sh` to preview before deploying
4. **Version Control**: Commit your changes to track evolution
5. **Share**: Push to GitHub, others can use your references!

## 🎬 Example Session

```bash
# Morning: Add new show you discovered
code source/references.yaml
# Added "Community" to rotating_pool

# Sync it
./scripts/sync.sh

# Restart Claude Code
# Now "Community" references are available!

# Copy to Cursor project
cp cursor-versions/modern/.cursor/rules/perfect-pair.mdc ~/projects/my-app/.cursor/rules/

# Code all day with your updated Perfect Pair! 🎉
```

## 🚀 Advanced: CI/CD (Future)

```bash
# Auto-deploy on git push
./scripts/setup-githooks.sh

# Now every commit auto-syncs your style
```

## 🤝 Sharing with Team

```bash
# Share your reference library
git add source/references.yaml
git commit -m "Updated references with new shows"
git push

# Team members pull and sync
git pull
./scripts/sync.sh
```

---

**Questions?** Check the main [README.md](README.md) or open an issue!
