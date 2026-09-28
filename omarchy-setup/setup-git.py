#!/usr/bin/env python3
"""Configure Git and GitHub SSH; never read private keys or tokens."""
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request

home = Path.home()
config_root = Path(os.environ.get('XDG_CONFIG_HOME', str(home / '.config')))

def backup(path):
    if path.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, str(path) + '.bak.' + stamp)

def write(path, content, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != content:
        backup(path)
        path.write_text(content)
    path.chmod(mode)

settings = {
    'user.name': 'Toschku',
    'user.email': 'maxim.boeckelmann@hey.com',
    'init.defaultBranch': 'main',
    'push.autoSetupRemote': 'true',
}
changes = {}
for key, value in settings.items():
    result = subprocess.run(['git', 'config', '--global', '--get', key], text=True, capture_output=True)
    if result.returncode != 0 or result.stdout.strip() != value:
        changes[key] = value
if changes:
    for path in (home / '.gitconfig', config_root / 'git/config'):
        backup(path)
    for key, value in changes.items():
        subprocess.run(['git', 'config', '--global', key, value], check=True)

ssh = home / '.ssh'
ssh.mkdir(exist_ok=True, mode=0o700)
ssh.chmod(0o700)

# Obtain host keys through verified HTTPS, not an unauthenticated ssh-keyscan.
request = urllib.request.Request('https://api.github.com/meta', headers={'User-Agent': 'personal-omarchy-setup'})
with urllib.request.urlopen(request, timeout=30) as response:
    keys = json.load(response)['ssh_keys']
if not keys or any(not re.fullmatch(r'(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp256) [A-Za-z0-9+/=]+', key) for key in keys):
    raise SystemExit('Unerwartetes GitHub-Hostschlüsselformat.')
write(ssh / 'github_known_hosts', ''.join(f'github.com {key}\n' for key in keys))

begin = '# BEGIN personal-omarchy-setup: github'
end = '# END personal-omarchy-setup: github'
content = f'''{begin}
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes
    AddKeysToAgent yes
    IdentityAgent /run/user/{os.getuid()}/ssh-agent.socket
    UserKnownHostsFile ~/.ssh/github_known_hosts ~/.ssh/known_hosts
    StrictHostKeyChecking yes
Host *
{end}
'''
target = ssh / 'config'
old = target.read_text() if target.exists() else ''
if begin in old or end in old:
    if old.count(begin) != 1 or old.count(end) != 1:
        raise SystemExit('Ungültige Setup-Markierungen in SSH-Konfiguration.')
    new, count = re.subn(re.escape(begin) + r'.*?' + re.escape(end) + r'\n?', lambda _: content, old, flags=re.S)
    if count != 1:
        raise SystemExit('Ungültiger SSH-Konfigurationsblock.')
else:
    new = content + '\n' + old
write(target, new)

write(config_root / 'systemd/user/ssh-agent.service', '''[Unit]
Description=Personal SSH authentication agent

[Service]
Type=simple
ExecStart=/usr/bin/ssh-agent -D -a %t/ssh-agent.socket
Restart=on-failure

[Install]
WantedBy=default.target
''', 0o644)

# Prefer the installed package over Omarchy's download-on-first-use wrapper.
wrapper = home / '.local/bin/gh'
if wrapper.exists() and not wrapper.is_symlink():
    original = wrapper.read_text()
    if 'mise use -g --quiet "gh"' in original:
        write(wrapper, '#!/bin/sh\nexec /usr/bin/gh "$@"\n', 0o755)
print('Git: Toschku <maxim.boeckelmann@hey.com>')
print('SSH-Konfiguration, GitHub-Hostschlüssel und SSH-Agent vorbereitet.')
