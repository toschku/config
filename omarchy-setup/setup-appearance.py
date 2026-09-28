#!/usr/bin/env python3
"""Back up appearance settings and install personal opacity/font overrides."""
import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess

root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
for name in ('hypr/looknfeel.lua', 'fontconfig/fonts.conf', 'alacritty/alacritty.toml',
             'kitty/kitty.conf', 'foot/foot.ini', 'ghostty/config'):
    path = root / name
    if path.exists():
        shutil.copy2(path, str(path) + '.bak.' + stamp)

target = root / 'hypr/looknfeel.lua'
old = target.read_text()
begin = '-- BEGIN personal-omarchy-setup: opacity'
end = '-- END personal-omarchy-setup: opacity'
block = f'''{begin}
-- App backgrounds control transparency; do not fade text or multiply alpha.
o.window({{ tag = "default-opacity" }}, {{ opacity = "1.0 1.0" }})
{end}
'''
if begin in old or end in old:
    if old.count(begin) != 1 or old.count(end) != 1:
        raise SystemExit('Ungültige Transparenz-Markierungen.')
    new, count = re.subn(re.escape(begin) + r'.*?' + re.escape(end) + r'\n?', lambda _: block, old, flags=re.S)
    if count != 1:
        raise SystemExit('Ungültiger Transparenz-Block.')
else:
    new = old.rstrip() + '\n\n' + block
if old != new:
    target.write_text(new)

target = root / 'fontconfig/conf.d/99-personal-interface-font.conf'
content = '''<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="pattern">
    <test name="family" qual="any"><string>sans-serif</string></test>
    <edit name="family" mode="prepend_first" binding="strong"><string>IBM Plex Mono</string></edit>
  </match>
</fontconfig>
'''
target.parent.mkdir(parents=True, exist_ok=True)
if not target.exists() or target.read_text() != content:
    if target.exists():
        shutil.copy2(target, str(target) + '.bak.' + stamp)
    target.write_text(content)

settings = [('org.gnome.desktop.interface', 'font-name', 'IBM Plex Mono 11'),
            ('org.gnome.desktop.interface', 'document-font-name', 'IBM Plex Mono 11'),
            ('org.gnome.desktop.interface', 'monospace-font-name', 'IBM Plex Mono 11'),
            ('org.gnome.desktop.wm.preferences', 'titlebar-font', 'IBM Plex Mono Bold 11')]
backup = root / 'omarchy/appearance-gsettings.before.txt'
if not backup.exists():
    backup.parent.mkdir(parents=True, exist_ok=True)
    backup.write_text(''.join(f'{schema} {key} = ' + subprocess.check_output(['gsettings', 'get', schema, key], text=True) for schema, key, _ in settings))
for schema, key, value in settings:
    subprocess.run(['gsettings', 'set', schema, key, value], check=True)
