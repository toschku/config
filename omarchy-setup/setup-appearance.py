#!/usr/bin/env python3
"""Back up and remove the former personal font overrides."""
import datetime
import os
from pathlib import Path
import shutil
import subprocess

root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
for name in ('fontconfig/fonts.conf', 'fontconfig/conf.d/99-personal-interface-font.conf'):
    path = root / name
    if path.exists():
        shutil.copy2(path, str(path) + '.bak.' + stamp)
        path.unlink()

settings = [('org.gnome.desktop.interface', 'font-name'),
            ('org.gnome.desktop.interface', 'document-font-name'),
            ('org.gnome.desktop.interface', 'monospace-font-name'),
            ('org.gnome.desktop.wm.preferences', 'titlebar-font')]
backup = root / ('omarchy/appearance-gsettings.rollback.' + stamp + '.txt')
backup.parent.mkdir(parents=True, exist_ok=True)
backup.write_text(''.join(f'{schema} {key} = ' + subprocess.check_output(
    ['gsettings', 'get', schema, key], text=True) for schema, key in settings))
for schema, key in settings:
    subprocess.run(['gsettings', 'reset', schema, key], check=True)
