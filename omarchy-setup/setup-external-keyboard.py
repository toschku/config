#!/usr/bin/env python3
"""Set the external Apple keyboard to US Mac, preserving internal layout."""
import datetime
import json
import os
from pathlib import Path
import re
import shutil

root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
target = root / 'hypr/input.lua'
name = os.environ.get('EXTERNAL_KEYBOARD', 'apple-inc.-magic-keyboard-with-touch-id')
if not re.fullmatch(r'[a-z0-9_./:-]+', name):
    raise SystemExit('Ungültiger Hyprland-Gerätename.')
old = target.read_text()
begin = '-- BEGIN personal-omarchy-setup: external-keyboard'
end = '-- END personal-omarchy-setup: external-keyboard'
block = f'''{begin}
hl.device({{
  name = {json.dumps(name)},
  kb_layout = "us",
  kb_variant = "mac",
}})
{end}
'''
if begin in old or end in old:
    if old.count(begin) != 1 or old.count(end) != 1:
        raise SystemExit('Uneindeutige Setup-Markierungen für externe Tastatur.')
    new, count = re.subn(re.escape(begin) + r'.*?' + re.escape(end) + r'\n?', lambda _: block, old, flags=re.S)
    if count != 1:
        raise SystemExit('Beschädigter Setup-Block für externe Tastatur.')
else:
    new = old.rstrip() + '\n\n' + block
if new != old:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    shutil.copy2(target, target.with_name(target.name + '.bak.' + stamp))
    target.write_text(new)
print(f'Externe Tastatur: {name}: US (Macintosh).')
