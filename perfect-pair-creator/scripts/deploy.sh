#!/bin/bash
# Deploy script - syncs generated style to Claude Code and Cursor

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
GENERATED_DIR="$ROOT_DIR/generated"
SOURCE_FILE="$GENERATED_DIR/perfect-pair-current.md"
DOTFILES_AI_DIR="$HOME/.dotfiles-ai"

echo "Deploying Perfect Pair style..."

# Check if source exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: $SOURCE_FILE not found. Run ./build.sh first!"
    exit 1
fi

# Check if a path (file or within a directory) is a stow symlink into dotfiles-ai.
# For files: checks the file itself.
# For directories: checks any file within (up to 2 levels deep).
is_stow_managed() {
    local path="$1"
    if [ -L "$path" ] && [[ "$(readlink "$path")" == *".dotfiles-ai"* ]]; then
        return 0
    fi
    if [ -d "$path" ]; then
        for f in "$path"/* "$path"/*/*; do
            if [ -L "$f" ] && [[ "$(readlink "$f")" == *".dotfiles-ai"* ]]; then
                return 0
            fi
        done
    fi
    return 1
}

# ─── Deploy to Claude Code ─────────────────────────────────────────

CLAUDE_PLUGIN_BASE="$HOME/.claude/plugins/user/perfect-pair-output-style"
CLAUDE_DOTFILES_BASE="$DOTFILES_AI_DIR/claude-code/.claude/plugins/user/perfect-pair-output-style"

echo "Deploying to Claude Code..."

# Detect dotfiles-ai stow management
CLAUDE_DEPLOY_BASE="$CLAUDE_PLUGIN_BASE"
if is_stow_managed "$CLAUDE_PLUGIN_BASE" && [ -d "$CLAUDE_DOTFILES_BASE" ]; then
    echo "  Detected dotfiles-ai stow management, writing to ~/.dotfiles-ai/claude-code/..."
    CLAUDE_DEPLOY_BASE="$CLAUDE_DOTFILES_BASE"
else
    # Create directory structure only when not stow-managed
    mkdir -p "$CLAUDE_DEPLOY_BASE/.claude-plugin"
    mkdir -p "$CLAUDE_DEPLOY_BASE/hooks"
    mkdir -p "$CLAUDE_DEPLOY_BASE/hooks-handlers"
fi

# Write plugin manifest
cat > "$CLAUDE_DEPLOY_BASE/.claude-plugin/plugin.json" << 'PLUGIN_JSON'
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
cat > "$CLAUDE_DEPLOY_BASE/hooks/hooks.json" << 'HOOKS_JSON'
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

# Generate session-start.sh with python3 JSON wrapper
# Claude Code SessionStart hooks REQUIRE JSON output:
# {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}
{
    cat << 'SCRIPT_HEADER'
#!/usr/bin/env bash

# Output the Perfect Pair style instructions as JSON additionalContext
# Format must match Claude Code's SessionStart hook spec

cat << 'CONTENT_EOF' | python3 -c "
import json, sys
content = sys.stdin.read()
result = {
    'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': content
    }
}
print(json.dumps(result))
"
SCRIPT_HEADER
    # Append content (skip header line and blank line after it)
    tail -n +3 "$SOURCE_FILE"
    echo "CONTENT_EOF"
    echo ""
    echo "exit 0"
} > "$CLAUDE_DEPLOY_BASE/hooks-handlers/session-start.sh"

chmod +x "$CLAUDE_DEPLOY_BASE/hooks-handlers/session-start.sh"
echo "  Claude Code plugin updated"

# ─── Deploy to Cursor ───────────────────────────────────────────────

CURSOR_GLOBAL_DIR="$HOME/.cursor/rules"
CURSOR_DOTFILES_DIR="$DOTFILES_AI_DIR/cursor/.cursor/rules"
CURSOR_MDC="$CURSOR_GLOBAL_DIR/perfect-pair.mdc"

echo "Deploying to Cursor (global)..."

# Detect dotfiles-ai stow management for Cursor
CURSOR_DEPLOY_DIR="$CURSOR_GLOBAL_DIR"
if is_stow_managed "$CURSOR_MDC" && [ -d "$CURSOR_DOTFILES_DIR" ]; then
    echo "  Detected dotfiles-ai stow management, writing to ~/.dotfiles-ai/cursor/..."
    CURSOR_DEPLOY_DIR="$CURSOR_DOTFILES_DIR"
else
    mkdir -p "$CURSOR_DEPLOY_DIR"
fi

# Create .mdc file with YAML frontmatter
{
    cat << 'CURSOR_HEADER'
---
description: Perfect pair programming partner with witty references and agile mindset
alwaysApply: true
---

CURSOR_HEADER
    cat "$SOURCE_FILE"
} > "$CURSOR_DEPLOY_DIR/perfect-pair.mdc"

echo "  Cursor global rules updated"

# Also update repo version for reference/sharing
CURSOR_REPO_DIR="$ROOT_DIR/cursor-versions/modern/.cursor/rules"
if [ -d "$CURSOR_REPO_DIR" ]; then
    cp "$CURSOR_DEPLOY_DIR/perfect-pair.mdc" "$CURSOR_REPO_DIR/perfect-pair.mdc"
    echo "  Repo version updated (for sharing)"
fi

echo ""
echo "Deployment complete!"
echo ""
echo "Deployed to:"
if [ "$CLAUDE_DEPLOY_BASE" = "$CLAUDE_DOTFILES_BASE" ]; then
    echo "  - Claude Code: ~/.dotfiles-ai/claude-code/...perfect-pair-output-style/"
else
    echo "  - Claude Code: ~/.claude/plugins/user/perfect-pair-output-style/"
fi
if [ "$CURSOR_DEPLOY_DIR" = "$CURSOR_DOTFILES_DIR" ]; then
    echo "  - Cursor: ~/.dotfiles-ai/cursor/.cursor/rules/perfect-pair.mdc"
else
    echo "  - Cursor: ~/.cursor/rules/perfect-pair.mdc (global)"
fi
echo ""
echo "Next steps:"
echo "  - Restart Claude Code to see changes"
echo "  - Cursor will automatically use the global rules in all projects"
