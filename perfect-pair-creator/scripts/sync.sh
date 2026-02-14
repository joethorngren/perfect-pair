#!/bin/bash
# Main sync script - builds and deploys in one go

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 Syncing Perfect Pair..."
echo ""

# Build
"$SCRIPT_DIR/build.sh"

echo ""

# Deploy
"$SCRIPT_DIR/deploy.sh"
