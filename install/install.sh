#!/bin/sh
set -eu

REPO="arch2kx/aronasay"
BRANCH="${ARONASAY_BRANCH:-main}"

BASE_RAW_URL="https://raw.githubusercontent.com/$REPO/$BRANCH"
MAIN_URL="$BASE_RAW_URL/src/aronasay.py"
ART_URL="$BASE_RAW_URL/src/art/arona_art.py"
VERSION_URL="$BASE_RAW_URL/VERSION.txt"

APP_NAME="aronasay"

echo "Aronasay Installation Script"
echo

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Choose install directory
if [ "$(id -u)" -eq 0 ]; then
    INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
elif [ -n "${INSTALL_DIR:-}" ]; then
    mkdir -p "$INSTALL_DIR"
elif [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

TARGET="$INSTALL_DIR/$APP_NAME"

echo "Installing to $TARGET"

# Downloader
download() {
    url="$1"
    out="$2"

    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$url" -o "$out"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$out" "$url"
    else
        echo "Error: curl or wget is required."
        exit 1
    fi
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT INT TERM

MAIN_FILE="$TMP_DIR/aronasay.py"
ART_FILE="$TMP_DIR/arona_art.py"
VERSION_FILE="$TMP_DIR/VERSION.txt"
TEMP_SCRIPT="$TMP_DIR/aronasay"

echo "Downloading program files..."
download "$MAIN_URL" "$MAIN_FILE"
download "$ART_URL" "$ART_FILE"

if download "$VERSION_URL" "$VERSION_FILE" 2>/dev/null; then
    VERSION="$(tr -d '\n' < "$VERSION_FILE")"
else
    VERSION="0.0.0"
fi

echo "Using version: $VERSION"

# Build bundled script
cat > "$TEMP_SCRIPT" <<EOF
#!/usr/bin/env python3
EOF

printf '\n' >> "$TEMP_SCRIPT"

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

printf '\n' >> "$TEMP_SCRIPT"

cat "$ART_FILE" >> "$TEMP_SCRIPT"

cat >> "$TEMP_SCRIPT" <<EOF

VERSION = "$VERSION"

if "--version" in sys.argv or "-V" in sys.argv:
    print(f"aronasay version {VERSION}")
    sys.exit(0)

EOF

# Skip shebang and optional encoding comment
awk '
NR == 1 && /^#!/ { next }
NR == 2 && /coding[:=]/ { next }
{ print }
' "$MAIN_FILE" >> "$TEMP_SCRIPT"

chmod 755 "$TEMP_SCRIPT"
mv "$TEMP_SCRIPT" "$TARGET"

echo
echo "✓ Installation complete!"
echo

case ":$PATH:" in
    *":$INSTALL_DIR:"*)
        echo "Run:"
        echo "  aronasay 'Hello, Sensei!'"
        ;;
    *)
        echo "Installed to: $TARGET"
        echo
        echo "Note: $INSTALL_DIR is not in your PATH."
        echo "Add this to your shell profile:"
        echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
        ;;
esac

echo
echo "Examples:"
echo "  aronasay 'Hello, Sensei!'"
echo "  aronasay -a"
echo "  aronasay -a hello"
echo "  aronasay -l"
echo "  aronasay --version"
echo
echo "No external Python packages required."
