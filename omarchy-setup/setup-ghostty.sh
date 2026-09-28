#!/usr/bin/env bash
set -euo pipefail
ghostty_setup_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
omarchy pkg add ghostty ttf-ibm-plex
pacman -Q ghostty ttf-ibm-plex >/dev/null
python3 "$ghostty_setup_dir/setup-ghostty.py"
omarchy default terminal ghostty
omarchy restart terminal
ghostty +validate-config
