#!/usr/bin/env python3
"""Start Pianoteq without JACK port filtering, then connect stereo output."""
import json
import os
import re
import signal
import subprocess
import sys
import time


def stereo_links(objects, pid, sink_id):
    def props(obj):
        return obj.get('info', {}).get('props', {})
    clients = {str(o['id']) for o in objects if o['type'].endswith(':Client')
               and str(props(o).get('application.process.id')) == str(pid)}
    nodes = {str(o['id']) for o in objects if o['type'].endswith(':Node')
             and (str(props(o).get('client.id')) in clients
                  or str(props(o).get('application.process.id')) == str(pid))}
    ports = [o for o in objects if o['type'].endswith(':Port')]
    links = []
    for number, channel in ((1, 'FL'), (2, 'FR')):
        source = next((o['id'] for o in ports if str(props(o).get('node.id')) in nodes
                       and props(o).get('port.direction') == 'out'
                       and props(o).get('port.name') == f'out_{number}'), None)
        target = next((o['id'] for o in ports if str(props(o).get('node.id')) == str(sink_id)
                       and props(o).get('port.direction') == 'in'
                       and props(o).get('audio.channel') == channel), None)
        if source is None or target is None:
            return []
        links.append((source, target))
    return links


def main():
    env = dict(os.environ)
    env.pop('PIPEWIRE_NODE', None)  # Crashes Pianoteq 9.2.5 on this ARM64 system.
    env.setdefault('PIPEWIRE_LATENCY', '256/48000')
    # Pianoteq may still auto-connect despite its saved device selection.
    # Let the separate pw-link client choose the output instead.
    env['PIPEWIRE_PROPS'] = '{ jack.self-connect-mode = ignore-external }'
    process = subprocess.Popen(['pw-jack', *sys.argv[1:]], env=env)
    def stop(signum, _frame):
        if process.poll() is None:
            process.send_signal(signum)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        for _ in range(100):
            if process.poll() is not None:
                return process.returncode
            info = subprocess.check_output(['wpctl', 'inspect', '@DEFAULT_AUDIO_SINK@'], text=True, timeout=5)
            match = re.search(r'^id (\d+),', info)
            objects = json.loads(subprocess.check_output(['pw-dump'], text=True, timeout=5))
            links = stereo_links(objects, process.pid, int(match[1])) if match else []
            if links:
                for source, target in links:
                    subprocess.run(['pw-link', str(source), str(target)], check=True, timeout=5)
                print(f'Pianoteq: Stereo mit Desktop-Ausgang {match[1]} verbunden.', flush=True)
                break
            time.sleep(0.2)
        else:
            print('Pianoteq: automatische Audioverbindung nicht verfügbar; Ausgang manuell verbinden.', file=sys.stderr)
    except (subprocess.SubprocessError, ValueError, OSError) as error:
        print(f'Pianoteq-Audioverbindung: {error}', file=sys.stderr)
    return process.wait()


if __name__ == '__main__':
    sys.exit(main())
