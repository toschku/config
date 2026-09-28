#!/usr/bin/env python3
"""Persist the user's requested Codex full-access defaults."""
import datetime
import os
from pathlib import Path
import re
import shutil
import tomllib

target = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'config.toml'
old = target.read_text() if target.exists() else ''
parsed = tomllib.loads(old)
if 'default_permissions' in parsed:
    raise SystemExit('default_permissions ist bereits gesetzt; zuerst mit sandbox_mode abstimmen.')
# Only change root keys; preserve project, model and other table settings.
parts = re.split(r'(?m)^(?=[ \t]*\[)', old, maxsplit=1)
head = parts[0]
for key, value in [('approval_policy', 'never'), ('sandbox_mode', 'danger-full-access')]:
    pattern = rf'(?m)^[ \t]*{key}[ \t]*=.*$'
    line = f'{key} = "{value}"'
    if re.search(pattern, head):
        head = re.sub(pattern, line, head)
    else:
        head = line + '\n' + head
new = head + (parts[1] if len(parts) == 2 else '')
result = tomllib.loads(new)
assert result['approval_policy'] == 'never'
assert result['sandbox_mode'] == 'danger-full-access'
if new != old:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = target.with_name(target.name + '.bak.' + stamp)
        shutil.copy2(target, backup)
        print(f'Sicherung: {backup}')
    target.write_text(new)
    print(f'Konfiguriert: {target}')
else:
    print('Codex-Vollzugriff bereits konfiguriert.')
print('Neue Codex-Sitzungen: Vollzugriff ohne Befehlsfreigaben. Laufende Sitzung neu starten.')
