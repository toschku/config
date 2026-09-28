#!/usr/bin/env bash
set -euo pipefail
audio_setup_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
archive="${1:-${PIANOTEQ_ARCHIVE:-$HOME/Downloads/pianoteq_setup_v925.tar.xz}}"
[[ -f "$archive" ]] || { echo "Pianoteq-Archiv fehlt: $archive" >&2; exit 1; }
# Explicitly replace legacy JACK if present; PipeWire supplies its libraries.
if pacman -Q jack2 >/dev/null 2>&1; then
  sudo pacman -S --needed --noconfirm --ask=4 pipewire-jack cpupower
else
  omarchy pkg add pipewire-jack cpupower
fi
pacman -Q pipewire-jack cpupower >/dev/null
sudo python3 "$audio_setup_dir/setup-audio-system.py" "$(id -un)"
python3 "$audio_setup_dir/install-pianoteq.py" "$archive"
echo 'Pianoteq installiert. Für die Echtzeitrechte einmal abmelden und wieder anmelden.'
