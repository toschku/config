#!/usr/bin/env bash
set -euo pipefail
appearance_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
omarchy pkg add ttf-ibm-plex
python3 "$appearance_dir/setup-appearance.py"
python3 "$appearance_dir/setup-ghostty.py"
omarchy font set 'IBM Plex Mono'
omarchy theme set Catppuccin
hyprctl reload
errors="$(hyprctl configerrors)"
if [[ -n "$errors" && "$errors" != ok ]]; then
  printf '%s\n' "$errors" >&2
  exit 1
fi
ghostty +validate-config
