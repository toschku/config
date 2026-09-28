#!/usr/bin/env python3
"""Run as root: generate German locale and select system defaults."""
import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess

if os.geteuid() != 0:
    raise SystemExit('Dieses Skript benötigt Root-Rechte.')

def write(path, content):
    path = Path(path)
    if path.exists() and path.read_text() == content:
        return
    if path.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, str(path) + '.bak.' + stamp)
    path.write_text(content)
    print(f'Konfiguriert: {path}')

p = Path('/etc/locale.gen')
old = p.read_text()
new, count = re.subn(r'^\s*#?\s*de_DE\.UTF-8\s+UTF-8[^\n]*$', 'de_DE.UTF-8 UTF-8', old, flags=re.M)
if not count:
    new = old.rstrip() + '\nde_DE.UTF-8 UTF-8\n'
write(p, new)
locales = subprocess.check_output(['locale', '-a'], text=True)
if new != old or 'de_DE.utf8' not in locales:
    subprocess.run(['locale-gen'], check=True)
p = Path('/etc/locale.conf')
old = p.read_text() if p.exists() else ''
lines = [line for line in old.splitlines() if not re.match(r'^(LANG|LANGUAGE|LC_[A-Z_]+)=', line)]
write(p, '\n'.join(lines + ['LANG=de_DE.UTF-8', 'LANGUAGE=de_DE:de:en_US:en']) + '\n')
