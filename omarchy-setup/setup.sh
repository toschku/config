#!/usr/bin/env bash
set -euo pipefail

# Nach der Omarchy-Installation als normaler Desktop-Benutzer ausführen.
# Bei anderer Hardware: INTERNAL_KEYBOARD=name ./setup.sh
export INTERNAL_KEYBOARD="${INTERNAL_KEYBOARD:-apple-spi-keyboard}"
command -v python3 >/dev/null || { echo 'python3 fehlt.' >&2; exit 1; }
setup_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
omarchy pkg add thunderbird thunderbird-i18n-de
pacman -Q thunderbird thunderbird-i18n-de >/dev/null
python3 "$setup_dir/setup-mail.py"
bash "$setup_dir/setup-language.sh"
bash "$setup_dir/setup-git.sh"
python3 "$setup_dir/setup-codex.py"
bash "$setup_dir/setup-ghostty.sh"
bash "$setup_dir/setup-appearance.sh"
if [[ -f "${PIANOTEQ_ARCHIVE:-$HOME/Downloads/pianoteq_setup_v925.tar.xz}" ]]; then
  bash "$setup_dir/setup-pianoteq.sh"
else
  echo 'Pianoteq: Linux-Archiv bei Modartt herunterladen, danach setup-pianoteq.sh ARCHIV ausführen.'
fi

python3 - <<'PY'
import datetime
import json
import os
import pathlib
import re
import shutil

root = pathlib.Path(os.environ.get('XDG_CONFIG_HOME', str(pathlib.Path.home() / '.config')))
hypr = root / 'hypr'
main = hypr / 'hyprland.lua'
target = hypr / 'input.lua'
if not main.is_file() or not target.is_file():
    raise SystemExit('Erwartet eine Omarchy-Installation mit hyprland.lua und input.lua.')
if not re.search(r'require\s*\(?\s*[\'"]hypr\.input[\'"]', main.read_text()):
    raise SystemExit('hyprland.lua lädt hypr.input nicht; bitte Einbindung prüfen.')
name = os.environ['INTERNAL_KEYBOARD']
if not re.fullmatch(r'[a-z0-9_./:-]+', name):
    raise SystemExit('Ungültiger Hyprland-Gerätename.')
begin = '-- BEGIN personal-omarchy-setup: internal-keyboard'
end = '-- END personal-omarchy-setup: internal-keyboard'
block = f'''{begin}
hl.device({{
  name = "{name}",
  kb_layout = "de",
  kb_variant = "mac",
}})
{end}
'''
old = target.read_text()
if begin in old or end in old:
    if old.count(begin) != 1 or old.count(end) != 1:
        raise SystemExit('Uneindeutige Setup-Markierungen in input.lua.')
    new, count = re.subn(re.escape(begin) + r'.*?' + re.escape(end) + r'\n?', lambda _: block, old, flags=re.S)
    if count != 1:
        raise SystemExit('Beschädigter Setup-Block in input.lua.')
else:
    new = old.rstrip() + '\n\n' + block
if new != old:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = target.with_name(target.name + '.bak.' + stamp)
    shutil.copy2(target, backup)
    target.write_text(new)
    print(f'Konfiguriert: {target}\nSicherung: {backup}')
else:
    print('Tastatur bereits konfiguriert.')

target = root / 'omarchy' / 'shell.json'
old = target.read_text() if target.exists() else '{}'
config = json.loads(old)
idle = config.setdefault('idle', {})
if idle.get('screensaver') != 60 or idle.get('lock') != 28800:
    idle.update(screensaver=60, lock=28800)
    new = json.dumps(config, ensure_ascii=False, indent=2) + '\n'
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = target.with_name(target.name + '.bak.' + stamp)
        shutil.copy2(target, backup)
        print(f'Sicherung: {backup}')
    target.write_text(new)
    print(f'Konfiguriert: {target}')
else:
    print('Inaktivitätszeiten bereits konfiguriert.')
print('Bildschirmschoner: 1 Minute; automatische Sperre: 8 Stunden Inaktivität.')
PY

if [[ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]] && command -v hyprctl >/dev/null; then
  hyprctl reload
  errors="$(hyprctl configerrors)"
  if [[ -n "$errors" && "$errors" != 'ok' ]]; then
    printf 'Hyprland meldet Konfigurationsfehler:\n%s\n' "$errors" >&2
    exit 1
  fi
  hyprctl devices -j | python3 -c '
import json, os, sys
name = os.environ["INTERNAL_KEYBOARD"]
devices = [k for k in json.load(sys.stdin)["keyboards"] if k["name"] == name]
if not devices:
    raise SystemExit(f"Konfiguriert, aber Gerät {name} ist derzeit nicht verbunden.")
for k in devices:
    if k["layout"] != "de" or k["variant"] != "mac":
        raise SystemExit(f"Layoutprüfung fehlgeschlagen: {k}")
    keymap = k["active_keymap"]
    print(f"Aktiv: {name}: {keymap}")
'
else
  echo 'Gespeichert. Das Layout wird beim nächsten Hyprland-Start aktiv.'
fi

if [[ -t 0 && -t 1 ]]; then
  bash "$setup_dir/connect-github.sh"
else
  echo "GitHub-Anmeldung im Terminal abschließen: bash $setup_dir/connect-github.sh"
fi
