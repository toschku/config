#!/usr/bin/env bash
set -euo pipefail
appearance_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python3 "$appearance_dir/setup-appearance.py"
omarchy refresh config hypr/looknfeel.lua
for config in alacritty/alacritty.toml kitty/kitty.conf foot/foot.ini ghostty/config; do
  if [[ -f "$HOME/.config/$config" ]]; then
    omarchy refresh config "$config"
  fi
done
omarchy theme set 'Tokyo Night'
omarchy restart shell
hyprctl reload
errors="$(hyprctl configerrors)"
if [[ -n "$errors" && "$errors" != ok ]]; then
  printf '%s\n' "$errors" >&2
  exit 1
fi
ghostty +validate-config
