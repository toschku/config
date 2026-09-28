#!/usr/bin/env python3
import datetime
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys

if os.geteuid() != 0 or len(sys.argv) != 2:
    raise SystemExit('Als root mit Benutzername aufrufen.')
user = pwd.getpwnam(sys.argv[1])
if user.pw_uid == 0 or not re.fullmatch(r'[a-z_][a-z0-9_-]*', user.pw_name):
    raise SystemExit('Ungültiger Desktop-Benutzer.')

def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text() == text:
            return
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, str(path) + '.bak.' + stamp)
    path.write_text(text)

# User-specific limits: no direct raw-device access through the audio group.
write(f'/etc/security/limits.d/90-pianoteq-{user.pw_name}.conf',
      f'{user.pw_name} - rtprio 90\n{user.pw_name} - nice -10\n{user.pw_name} - memlock 500000\n')
write(f'/etc/systemd/system/user@{user.pw_uid}.service.d/90-pianoteq.conf',
      '[Service]\nLimitRTPRIO=90\nLimitNICE=-10\nLimitMEMLOCK=512000000\n')

path = Path('/etc/default/cpupower-service.conf')
old = path.read_text()
new, count = re.subn(r'^#?GOVERNOR=.*$', "GOVERNOR='performance'", old, flags=re.M)
if not count:
    new = old.rstrip() + "\nGOVERNOR='performance'\n"
write(path, new)
subprocess.run(['systemctl', 'daemon-reload'], check=True)
subprocess.run(['systemctl', 'enable', '--now', 'cpupower.service'], check=True)
subprocess.run(['systemctl', 'restart', 'cpupower.service'], check=True)
print('Echtzeitrechte vorbereitet; vollständig wirksam nach Ab-/Anmeldung. CPU-Modus: performance.')
