#!/usr/bin/env python3
"""Install the locally downloaded licensed archive; never publish it."""
import datetime
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET

archive = Path(sys.argv[1]).resolve()
arch = {'aarch64': 'arm-64bit', 'x86_64': 'x86-64bit'}.get(platform.machine())
if arch is None:
    raise SystemExit('Nicht unterstützte CPU-Architektur.')
home = Path.home()
data = Path(os.environ.get('XDG_DATA_HOME', str(home / '.local/share')))
config = Path(os.environ.get('XDG_CONFIG_HOME', str(home / '.config')))
dest = data / 'pianoteq/Pianoteq 9'
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
with tempfile.TemporaryDirectory() as scratch:
    with tarfile.open(archive, 'r:xz') as tar:
        tar.extractall(scratch, filter='data')
    src = Path(scratch) / 'Pianoteq 9'
    if not (src / arch / 'Pianoteq 9').is_file():
        raise SystemExit('Pianoteq-9-Binärdatei fehlt im Archiv.')
    if dest.exists():
        dest.rename(dest.with_name(dest.name + '.bak.' + stamp))
    dest.mkdir(parents=True)
    for name in ('README_LINUX.txt', 'Licence.rtf'):
        shutil.copy2(src / name, dest / name)
    shutil.copytree(src / 'Documentation', dest / 'Documentation')
    shutil.copytree(src / arch, dest / arch)

for extension in ('vst3', 'lv2'):
    plugin = home / ('.' + extension) / ('Pianoteq 9.' + extension)
    plugin.parent.mkdir(parents=True, exist_ok=True)
    if plugin.is_symlink() or plugin.exists():
        plugin.rename(plugin.with_name(plugin.name + '.bak.' + stamp))
    plugin.symlink_to(dest / arch / plugin.name, target_is_directory=True)

# Initial JACK configuration, preserving any unrelated preferences/licence data.
prefs = config / 'Modartt/Pianoteq90.prefs'
prefs.parent.mkdir(parents=True, exist_ok=True)
if prefs.exists():
    shutil.copy2(prefs, str(prefs) + '.bak.' + stamp)
    tree = ET.parse(prefs)
    root = tree.getroot()
else:
    root = ET.Element('PROPERTIES')
    tree = ET.ElementTree(root)
for item in list(root):
    if item.get('name') == 'audio-setup':
        root.remove(item)
value = ET.SubElement(root, 'VALUE', name='audio-setup')
ET.SubElement(value, 'DEVICESETUP', deviceType='JACK', audioOutputDeviceName='Auto-connect OFF',
              audioInputDeviceName='', audioDeviceRate='48000', audioDeviceBufferSize='256',
              audioDeviceInChans='0', audioDeviceOutChans='11')
tree.write(prefs, encoding='UTF-8', xml_declaration=True)
prefs.chmod(0o600)

binary = dest / arch / 'Pianoteq 9'
(data / 'Modartt').mkdir(parents=True, exist_ok=True)
(data / 'applications').mkdir(parents=True, exist_ok=True)
subprocess.run([str(binary), '--install-app-icon-and-quit'], check=True)
launcher = home / '.local/bin/pianoteq'
launcher.parent.mkdir(parents=True, exist_ok=True)
import shlex
helper = home / '.local/libexec/pianoteq-launch.py'
helper.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(Path(__file__).with_name('pianoteq-launch.py'), helper)
launcher.write_text('#!/bin/sh\nexec python3 ' + shlex.quote(str(helper)) + ' '
                   + shlex.quote(str(binary)) + ' "$@"\n')
launcher.chmod(0o755)
# Rewrite the vendor-generated launchers to use the low-latency wrapper.
for desktop in (data / 'applications').glob('*.desktop'):
    text = desktop.read_text()
    if str(binary) in text:
        import re
        text = re.sub(r'^Exec=.*$', 'Exec="' + str(launcher) + '" %F', text, flags=re.M)
        desktop.write_text(text)
desktop = data / 'applications/Pianoteq 9.desktop'
desktop.write_text('[Desktop Entry]\nType=Application\nName=Pianoteq 9\nComment=Pianoteq mit PipeWire-JACK\n'
                   + 'Exec="' + str(launcher) + '" %F\n'
                   + 'Icon=' + str(data / 'Modartt/Pianoteq 9.svg') + '\n'
                   + 'Terminal=false\nCategories=AudioVideo;Audio;Midi;\n')
print(f'Pianoteq installiert: {binary}')
