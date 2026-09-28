#!/usr/bin/env bash
set -euo pipefail
setup_language_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
sudo python3 "$setup_language_dir/setup-language-system.py"
language_packages=(hunspell-de hyphen-de mythes-de)
pacman -Q libreoffice-fresh >/dev/null 2>&1 && language_packages+=(libreoffice-fresh-de)
pacman -Q thunderbird >/dev/null 2>&1 && language_packages+=(thunderbird-i18n-de)
pacman -Q tesseract >/dev/null 2>&1 && language_packages+=(tesseract-data-deu)
omarchy pkg add "${language_packages[@]}"
pacman -Q "${language_packages[@]}" >/dev/null
python3 "$setup_language_dir/setup-language-user.py"
if [[ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]]; then
  hyprctl reload
  errors="$(hyprctl configerrors)"
  if [[ -n "$errors" && "$errors" != ok ]]; then
    printf '%s\n' "$errors" >&2
    exit 1
  fi
  dbus-update-activation-environment --systemd LANG=de_DE.UTF-8 LANGUAGE=de_DE:de:en_US:en
  omarchy restart shell
fi
echo 'Deutsch eingerichtet. Für alle Anwendungen einmal abmelden und wieder anmelden.'
