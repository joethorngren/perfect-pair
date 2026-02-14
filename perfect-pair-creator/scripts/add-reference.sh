#!/bin/bash
# Helper script to add a reference to references.yaml
# Called by the /add-reference skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
REFERENCES_FILE="$ROOT_DIR/source/references.yaml"

# Arguments
NAME="$1"
TYPE="$2"
USAGE="$3"
EXAMPLE="$4"
LOCATION="$5"  # "core" or "rotating"

if [ -z "$NAME" ] || [ -z "$TYPE" ] || [ -z "$USAGE" ] || [ -z "$EXAMPLE" ] || [ -z "$LOCATION" ]; then
    echo "Usage: $0 <name> <type> <usage> <example> <core|rotating>"
    exit 1
fi

echo "📝 Adding reference to $LOCATION..."
echo ""
echo "Name: $NAME"
echo "Type: $TYPE"
echo "Usage: $USAGE"
echo "Example: $EXAMPLE"
echo ""

# Create the YAML entry
YAML_ENTRY="
  - name: \"$NAME\"
    type: \"$TYPE\"
    usage: \"$USAGE\"
    examples:
      - \"$EXAMPLE\"
    last_active: null"

# Add to the appropriate section
if [ "$LOCATION" = "core" ]; then
    # Find the core: section and add after it
    # This is a simplified version - in production you'd want proper YAML parsing
    echo "⚠️  Adding to core requires manual editing for now."
    echo "Please add the following to the 'core:' section in $REFERENCES_FILE"
    echo "$YAML_ENTRY"
elif [ "$LOCATION" = "rotating" ]; then
    # Same for rotating_pool
    echo "⚠️  Adding to rotating_pool requires manual editing for now."
    echo "Please add the following to the 'rotating_pool:' section in $REFERENCES_FILE"
    echo "$YAML_ENTRY"
else
    echo "❌ Invalid location: $LOCATION"
    exit 1
fi

echo ""
echo "💡 Tip: Open the file and paste the above:"
echo "   open $REFERENCES_FILE"
echo ""
echo "Then run:"
echo "   ./scripts/sync.sh"
