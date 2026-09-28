#!/usr/bin/env python3
"""Enable natural mouse scrolling without changing touchpad settings."""
import datetime
import os
from pathlib import Path
import re
import shutil

root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
target = root / 'hypr/input.lua'
old = target.read_text()
begin = '-- BEGIN personal-omarchy-setup: mouse-scroll'
end = '-- END personal-omarchy-setup: mouse-scroll'
block = f'{begin}\nhl.config({{ input = {{ natural_scroll = true }} }})\n{end}\n'
if begin in old or end in old:
    if old.count(begin) != 1 or old.count(end) != 1:
        raise SystemExit('Uneindeutige Maus-Setup-Markierungen.')
    new, count = re.subn(re.escape(begin) + r'.*?' + re.escape(end) + r'\n?', lambda _: block, old, flags=re.S)
    if count != 1:
        raise SystemExit('Beschädigter Maus-Setup-Block.')
else:
    new = old.rstrip() + '\n\n' + block
if new != old:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    shutil.copy2(target, target.with_name(target.name + '.bak.' + stamp))
    target.write_text(new)
print('Maus: natürliche Scrollrichtung aktiviert.')
