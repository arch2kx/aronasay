#!/bin/bash
# Aronasay Installation Script

set -e

echo "Aronasay Installation Script"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)."
    exit 1
fi

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required but not installed."
  exit 1
fi

# Determine installation directory
INSTALL_DIR="/usr/local/bin"
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)/src"

echo "Installing aronasay to $INSTALL_DIR..."

# Create temporary combined script
TEMP_SCRIPT=$(mktemp)

# Write shebang
echo "#!/usr/bin/env python3" > "$TEMP_SCRIPT"
echo "" >> "$TEMP_SCRIPT"

# Add essential imports first
echo "import sys, os" >> "$TEMP_SCRIPT"
echo "" >> "$TEMP_SCRIPT"

# Add the art module inline
cat "$SRC_DIR/art/arona_art.py" >> "$TEMP_SCRIPT"

# Add separator comment
echo "" >> "$TEMP_SCRIPT"
echo "# Version handling" >> "$TEMP_SCRIPT"
echo "" >> "$TEMP_SCRIPT"

# Read version from VERSION.txt
VERSION_FILE="$SRC_DIR/../VERSION.txt"
if [ -f "$VERSION_FILE" ]; then
    VERSION=$(<"$VERSION_FILE")
else
    echo "VERSION.txt not found. Defaulting to 0.0.0"
    VERSION="0.0.0"
fi

echo "Using version: $VERSION"

# Inject version and check
cat << EOF >> "$TEMP_SCRIPT"
VERSION = "$VERSION"

# Check for --version flag before main
import sys
if "--version" in sys.argv or "-V" in sys.argv:
    print(f"aronasay version {VERSION}")
    sys.exit(0)
EOF

echo "" >> "$TEMP_SCRIPT"
echo "# Main Program" >> "$TEMP_SCRIPT"
echo "" >> "$TEMP_SCRIPT"

# Add main script (skip the imports)
tail -n +9 "$SRC_DIR/aronasay.py" >> "$TEMP_SCRIPT"

# Install to system
install -m 755 "$TEMP_SCRIPT" "$INSTALL_DIR/aronasay"

# Clean up
rm "$TEMP_SCRIPT"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Try it out:"
echo "  aronasay 'Hello, Sensei!'"
echo "  aronasay -a"
echo "  aronasay -l"
echo "  aronasay --version"
echo ""
