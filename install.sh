#!/usr/bin/env bash
set -euo pipefail

sudo install -m 0755 msi-cooler-toggle.py /usr/local/bin/msi-cooler-toggle

echo "Installed /usr/local/bin/msi-cooler-toggle"
echo
echo "To enable EC write support now, run:"
echo "  sudo modprobe -r ec_sys 2>/dev/null || true"
echo "  sudo modprobe ec_sys write_support=1"
echo
echo "Then test:"
echo "  sudo /usr/local/bin/msi-cooler-toggle"
