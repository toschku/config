#!/usr/bin/env python3
"""Create a dedicated iCloud profile once, without storing credentials."""
import json
import os
from pathlib import Path
import configparser
import datetime
import io
import shutil
import subprocess

if subprocess.run(['pgrep', '-x', 'thunderbird'], stdout=subprocess.DEVNULL).returncode == 0:
    raise SystemExit('Thunderbird vor Änderungen an der Profilzuordnung schließen.')

profile = Path.home() / '.thunderbird' / 'omarchy-icloud'
profile.mkdir(parents=True, exist_ok=True, mode=0o700)
prefs = {
    'intl.locale.requested': 'de',
    'mail.shell.checkDefaultClient': False,
    'mail.accountmanager.accounts': 'account1',
    'mail.accountmanager.defaultaccount': 'account1',
    'mail.account.account1.server': 'server1',
    'mail.account.account1.identities': 'id1',
    'mail.server.server1.type': 'imap',
    'mail.server.server1.hostname': 'imap.mail.me.com',
    'mail.server.server1.port': 993,
    'mail.server.server1.socketType': 3,
    'mail.server.server1.authMethod': 3,
    'mail.server.server1.userName': 'maxim.boeckelmann',
    'mail.server.server1.name': 'iCloud – maxim.boeckelmann@mac.com',
    'mail.server.server1.login_at_startup': True,
    'mail.server.server1.check_new_mail': True,
    'mail.server.server1.check_time': 10,
    'mail.server.server1.directory': str(profile / 'ImapMail' / 'imap.mail.me.com'),
    'mail.identity.id1.useremail': 'maxim.boeckelmann@mac.com',
    'mail.identity.id1.fullName': 'Maxim Boeckelmann',
    'mail.identity.id1.smtpServer': 'smtp1',
    'mail.identity.id1.valid': True,
    'mail.smtpservers': 'smtp1',
    'mail.smtp.defaultserver': 'smtp1',
    'mail.smtpserver.smtp1.hostname': 'smtp.mail.me.com',
    'mail.smtpserver.smtp1.port': 587,
    'mail.smtpserver.smtp1.try_ssl': 2,
    'mail.smtpserver.smtp1.authMethod': 3,
    'mail.smtpserver.smtp1.username': 'maxim.boeckelmann@mac.com',
    'mail.smtpserver.smtp1.description': 'iCloud',
}
target = profile / 'prefs.js'
if not target.exists():
    with target.open('x') as f:
        for key, value in prefs.items():
            f.write(f'user_pref({json.dumps(key)}, {json.dumps(value)});\n')
    target.chmod(0o600)
    print(f'iCloud-Konto vorbereitet: {profile}')
else:
    print(f'Vorhandenes Profil bleibt erhalten: {profile}')

# Register the same profile for normal Thunderbird starts, not only our launcher.
def read_ini(path):
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    if path.exists():
        config.read(path)
    return config

def save_ini(path, config):
    buffer = io.StringIO()
    config.write(buffer, space_around_delimiters=False)
    new = buffer.getvalue()
    if path.exists() and path.read_text() == new:
        return
    if path.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, path.with_name(path.name + '.bak.' + stamp))
    path.write_text(new)

registry = profile.parent / 'profiles.ini'
config = read_ini(registry)
section = None
for name in config.sections():
    if name.startswith('Profile'):
        config.remove_option(name, 'Default')
        entry = Path(config[name].get('Path', ''))
        if config[name].get('IsRelative', '1') == '1':
            entry = profile.parent / entry
        if entry.resolve() == profile.resolve():
            section = name
    elif name.startswith('Install'):
        config[name]['Default'] = profile.name
if section is None:
    index = 0
    while f'Profile{index}' in config:
        index += 1
    section = f'Profile{index}'
    config[section] = {'Name': 'omarchy-icloud', 'IsRelative': '1', 'Path': profile.name}
config[section]['Default'] = '1'
if 'General' not in config:
    config['General'] = {}
config['General'].update({'StartWithLastProfile': '1', 'Version': '2'})
save_ini(registry, config)
installs = profile.parent / 'installs.ini'
if installs.exists():
    config = read_ini(installs)
    for section in config.sections():
        config[section]['Default'] = profile.name
    save_ini(installs, config)
print('Thunderbird-Standardprofil: omarchy-icloud')

apps = Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'applications'
apps.mkdir(parents=True, exist_ok=True)
# Desktop Exec quoting: escape reserved characters and literal percent signs.
quoted = str(profile).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
desktop = f'''[Desktop Entry]
Type=Application
Name=iCloud Mail
Comment=iCloud in Thunderbird – maxim.boeckelmann@mac.com
Exec=thunderbird -no-remote -profile "{quoted}"
Icon=thunderbird
Terminal=false
Categories=Network;Email;
StartupNotify=true
'''
launcher = apps / 'omarchy-icloud.desktop'
if not launcher.exists() or launcher.read_text() != desktop:
    launcher.write_text(desktop)
print('App-Menü: iCloud Mail. App-spezifisches Apple-Passwort direkt in Thunderbird eingeben.')
