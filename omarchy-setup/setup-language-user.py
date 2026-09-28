#!/usr/bin/env python3
import datetime
import json
import os
from pathlib import Path
import re
import shutil

root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text() == text:
            return
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, str(path) + '.bak.' + stamp)
    path.write_text(text)
    print(f'Konfiguriert: {path}')

def block(path, name, body, comment='#'):
    old = path.read_text() if path.exists() else ''
    start, end = f'{comment} BEGIN personal-omarchy-setup: {name}', f'{comment} END personal-omarchy-setup: {name}'
    content = f'{start}\n{body}\n{end}\n'
    if start in old or end in old:
        if old.count(start) != 1 or old.count(end) != 1:
            raise SystemExit(f'Ungültige Markierungen: {path}')
        new, n = re.subn(re.escape(start) + r'.*?' + re.escape(end) + r'\n?', lambda _: content, old, flags=re.S)
        if n != 1:
            raise SystemExit(f'Ungültige Markierungen: {path}')
    else:
        new = old.rstrip() + '\n\n' + content if old.strip() else content
    write(path, new)

locale = 'LANG=de_DE.UTF-8\nLANGUAGE=de_DE:de:en_US:en'
write(root / 'environment.d/60-personal-language.conf', locale + '\n')
block(root / 'uwsm/env', 'language', 'export LANG=de_DE.UTF-8\nexport LANGUAGE=de_DE:de:en_US:en')
block(root / 'hypr/hyprland.lua', 'language', 'hl.env("LANG", "de_DE.UTF-8")\nhl.env("LANGUAGE", "de_DE:de:en_US:en")', '--')

flags = root / 'chromium-flags.conf'
old = flags.read_text() if flags.exists() else ''
lines = [l for l in old.splitlines() if not l.startswith('--lang=')]
write(flags, '\n'.join(lines + ['--lang=de']) + '\n')

# Keep Omarchy menu definitions untouched: label-only overrides also clear
# actions, providers and icons in the installed MenuModel.js implementation.

target = root / 'omarchy/shell.json'
if target.exists():
    config = json.loads(target.read_text())
    for entries in config.get('bar', {}).get('layout', {}).values():
        for entry in entries:
            if entry.get('id') == 'omarchy.clock':
                entry['format'] = 'dddd HH:mm'
                entry['formatAlt'] = "d. MMMM yyyy 'KW' ww"
    write(target, json.dumps(config, ensure_ascii=False, indent=2) + '\n')
