#!/bin/bash
# Aronasay Uninstall Script

set -e

echo "Aronasay Uninstall Script"
echo ""

# Check root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)."
  exit 1
fi

INSTALL_PATH="/usr/local/bin/aronasay"

if [ -f "$INSTALL_PATH" ]; then
  # Ask for confirmation
  read -p "Are you sure you want to uninstall aronasay? [y/N]: " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

  echo "Removing $INSTALL_PATH..."
  rm "$INSTALL_PATH"

  # Check removal
  if [ ! -f "$INSTALL_PATH" ]; then
    echo "✓ Aronasay successfully uninstalled."
  else
    echo "Failed to remove $INSTALL_PATH. Check permissions."
  fi
else
  echo "Aronasay is not installed at $INSTALL_PATH"
fi

echo ""
