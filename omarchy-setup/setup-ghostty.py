#!/usr/bin/env python3
"""Install a Linux-adapted copy of the repository's Ghostty configuration."""
import datetime
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

source = Path(__file__).resolve().parent.parent / 'config.ghostty'
root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
target = root / 'ghostty/config'
lines = []
for line in source.read_text().splitlines():
    setting = line.strip().split('=', 1)[0].strip()
    if setting.startswith('macos-') or setting == 'window-step-resize':
        continue
    if setting == 'background-blur':
        line = 'background-blur = true'
    lines.append(line)
content = '# Aus config.ghostty im Repository erzeugt; Linux-Anpassungen durch setup-ghostty.py.\n'
content += '\n'.join(lines).rstrip() + '''

# Linux/Omarchy: Titelleiste ausblenden und bestehende Terminal-Integration erhalten.
window-decoration = none
shell-integration-features = no-cursor,ssh-env
keybind = shift+insert=paste_from_clipboard
keybind = control+insert=copy_to_clipboard
keybind = shift+enter=csi:13;2u
keybind = alt+shift+enter=csi:13;4u
async-backend = epoll
'''
with tempfile.NamedTemporaryFile(mode='w', suffix='.ghostty', delete=True) as check:
    check.write(content)
    check.flush()
    subprocess.run(['ghostty', '+validate-config', '--config-file=' + check.name], check=True)
target.parent.mkdir(parents=True, exist_ok=True)
if not target.exists() or target.read_text() != content:
    if target.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(target, str(target) + '.bak.' + stamp)
    target.write_text(content)
    print(f'Ghostty-Konfiguration installiert: {target}')
else:
    print('Ghostty-Konfiguration bereits aktuell.')

preference = root / 'xdg-terminals.list'
desired = '# Terminal emulator preference order for xdg-terminal-exec\n# The first found and valid terminal will be used\ncom.mitchellh.ghostty.desktop\n'
if preference.exists() and preference.read_text() != desired:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    shutil.copy2(preference, str(preference) + '.bak.' + stamp)
