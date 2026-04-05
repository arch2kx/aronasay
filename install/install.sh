#!/bin/bash
# Aronasay Installation Script

set -e

echo "Aronasay Installation Script"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)."
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required but not installed."
    exit 1
fi

INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)/src"
MAIN_FILE="$SRC_DIR/aronasay.py"
ART_FILE="$SRC_DIR/art/arona_art.py"
VERSION_FILE="$SRC_DIR/../VERSION.txt"

[ -f "$MAIN_FILE" ] || { echo "Missing $MAIN_FILE"; exit 1; }
[ -f "$ART_FILE" ] || { echo "Missing $ART_FILE"; exit 1; }

echo "Installing aronasay to $INSTALL_DIR..."

TEMP_SCRIPT=$(mktemp)
trap 'rm -f "$TEMP_SCRIPT"' EXIT

# Shebang
cat > "$TEMP_SCRIPT" <<'EOF'
#!/usr/bin/env python3
EOF

echo "" >> "$TEMP_SCRIPT"

# Standard-library imports
cat >> "$TEMP_SCRIPT" <<'EOF'
import sys
import os
import io
import re
import time
import shutil
import textwrap
import argparse
EOF

echo "" >> "$TEMP_SCRIPT"

# Embed art module first
cat "$ART_FILE" >> "$TEMP_SCRIPT"

echo "" >> "$TEMP_SCRIPT"
echo "# Version handling" >> "$TEMP_SCRIPT"
echo "" >> "$TEMP_SCRIPT"

if [ -f "$VERSION_FILE" ]; then
    VERSION=$(tr -d '\n' < "$VERSION_FILE")
else
    echo "VERSION.txt not found. Defaulting to 0.0.0"
    VERSION="0.0.0"
fi

echo "Using version: $VERSION"

cat <<EOF >> "$TEMP_SCRIPT"
VERSION = "$VERSION"

if "--version" in sys.argv or "-V" in sys.argv:
    print(f"aronasay version {VERSION}")
    sys.exit(0)
EOF

echo "" >> "$TEMP_SCRIPT"
echo "# Main Program" >> "$TEMP_SCRIPT"
echo "" >> "$TEMP_SCRIPT"

# Append main script, skipping only shebang and encoding comment
tail -n +3 "$MAIN_FILE" >> "$TEMP_SCRIPT"

install -m 755 "$TEMP_SCRIPT" "$INSTALL_DIR/aronasay"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Try it out:"
echo "  aronasay 'Hello, Sensei!'"
echo "  aronasay -a"
echo "  aronasay -a hello"
echo "  aronasay -l"
echo "  aronasay --version"
echo ""
echo "No external Python packages required."
echo ""
