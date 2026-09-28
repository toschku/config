#!/usr/bin/env python3
"""Create a dedicated iCloud profile once, without storing credentials."""
import json
import os
from pathlib import Path

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
