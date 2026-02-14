#!/bin/bash
# Deploy script - syncs generated style to Claude Code and Cursor

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
GENERATED_DIR="$ROOT_DIR/generated"
SOURCE_FILE="$GENERATED_DIR/perfect-pair-current.md"

echo "🚀 Deploying Perfect Pair style..."

# Check if source exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "❌ Error: $SOURCE_FILE not found. Run ./build.sh first!"
    exit 1
fi

# Deploy to Claude Code plugin
CLAUDE_PLUGIN_BASE="$HOME/.claude/plugins/user/perfect-pair-output-style"
echo "📦 Deploying to Claude Code..."

# Create plugin directory structure
mkdir -p "$CLAUDE_PLUGIN_BASE/.claude-plugin"
mkdir -p "$CLAUDE_PLUGIN_BASE/hooks"
mkdir -p "$CLAUDE_PLUGIN_BASE/hooks-handlers"

# Write plugin manifest
cat > "$CLAUDE_PLUGIN_BASE/.claude-plugin/plugin.json" << 'PLUGIN_JSON'
{
  "name": "perfect-pair-output-style",
  "description": "Your perfect pair programming partner with references to The Office, Parks & Rec, Arrested Development, Chappelle Show, Key & Peele, SNL, and more",
  "version": "1.0.0",
  "author": {
    "name": "oh_henry"
  },
  "hooks": "./hooks/hooks.json"
}
PLUGIN_JSON

# Write hooks config
cat > "$CLAUDE_PLUGIN_BASE/hooks/hooks.json" << 'HOOKS_JSON'
{
  "description": "Perfect Pair output style hook",
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks-handlers/session-start.sh"
      }
    ]
  }
}
HOOKS_JSON

# Update the session-start.sh script with new content
cat > "$CLAUDE_PLUGIN_BASE/hooks-handlers/session-start.sh" << 'SCRIPT_START'
#!/bin/bash

cat <<'EOF'
SCRIPT_START

# Append the content (skipping the first line "# Perfect Pair...")
tail -n +2 "$SOURCE_FILE" >> "$CLAUDE_PLUGIN_BASE/hooks-handlers/session-start.sh"

cat >> "$CLAUDE_PLUGIN_BASE/hooks-handlers/session-start.sh" << 'SCRIPT_END'
EOF
SCRIPT_END

chmod +x "$CLAUDE_PLUGIN_BASE/hooks-handlers/session-start.sh"
echo "   ✅ Claude Code plugin updated"

# Deploy to Cursor (global)
CURSOR_GLOBAL_DIR="$HOME/.cursor/rules"
mkdir -p "$CURSOR_GLOBAL_DIR"

echo "📦 Deploying to Cursor (global)..."

# Create .mdc file with frontmatter
cat > "$CURSOR_GLOBAL_DIR/perfect-pair.mdc" << 'CURSOR_START'
---
description: Perfect pair programming partner with witty references and agile mindset
alwaysApply: true
---

CURSOR_START

# Append the content
cat "$SOURCE_FILE" >> "$CURSOR_GLOBAL_DIR/perfect-pair.mdc"

echo "   ✅ Cursor global rules updated"

# Also update repo version for reference/sharing
CURSOR_REPO_DIR="$ROOT_DIR/cursor-versions/modern/.cursor/rules"
if [ -d "$CURSOR_REPO_DIR" ]; then
    cp "$CURSOR_GLOBAL_DIR/perfect-pair.mdc" "$CURSOR_REPO_DIR/perfect-pair.mdc"
    echo "   ✅ Repo version updated (for sharing)"
fi

echo ""
echo "✨ Deployment complete!"
echo ""
echo "📍 Deployed to:"
echo "   - Claude Code: ~/.claude/plugins/user/perfect-pair-output-style/"
echo "   - Cursor: ~/.cursor/rules/perfect-pair.mdc (global - applies to all projects)"
echo ""
echo "💡 Next steps:"
echo "   - Restart Claude Code to see changes"
echo "   - Cursor will automatically use the global rules in all projects"
echo "   - Override per-project: Create <project>/.cursor/rules/ with custom rules"
