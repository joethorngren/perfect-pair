#!/bin/bash
# Main sync script - builds and deploys in one go

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$ROOT_DIR/.venv"

echo "Syncing Perfect Pair..."
echo ""

# Ensure virtual environment exists and has dependencies
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/pip" install -q -r "$ROOT_DIR/requirements.txt" 2>/dev/null

# Build (primary build path: Python)
"$VENV_DIR/bin/python3" "$SCRIPT_DIR/build.py"

echo ""

# Deploy
"$SCRIPT_DIR/deploy.sh"
