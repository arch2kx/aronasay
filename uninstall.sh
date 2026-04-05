#!/bin/bash
# Aronasay Uninstall Script

set -e

echo "Aronasay Uninstall Script"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)."
    exit 1
fi

INSTALL_PATH="${INSTALL_PATH:-/usr/local/bin/aronasay}"

if [ ! -e "$INSTALL_PATH" ]; then
    echo "Aronasay is not installed at $INSTALL_PATH"
    echo ""
    exit 0
fi

read -r -p "Are you sure you want to uninstall aronasay from $INSTALL_PATH? [y/N]: " confirm
case "$confirm" in
    [Yy]|[Yy][Ee][Ss])
        echo "Removing $INSTALL_PATH..."
        rm -f "$INSTALL_PATH"
        echo "✓ Aronasay successfully uninstalled."
        ;;
    *)
        echo "Aborted."
        ;;
esac

echo ""
