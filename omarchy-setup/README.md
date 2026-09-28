# Persönliches Omarchy-Setup

Dieses Verzeichnis enthält das fortlaufende Protokoll und das Einrichtungsskript für die gewünschten Anpassungen. Für spätere Installationen das gesamte Repository einschließlich `config.ghostty` klonen.

Nach einer frischen Omarchy-Installation im Terminal als Desktop-Benutzer ausführen:

```bash
bash setup.sh
```

Voraussetzungen: Omarchy mit Hyprland-Lua-Konfiguration und Python 3. Das Skript ergänzt gezielt einen eigenen Block in `~/.config/hypr/input.lua`, sichert die Datei bei Änderungen mit Zeitstempel und prüft in einer laufenden Hyprland-Sitzung das Ergebnis. Wiederholtes Ausführen erzeugt keine doppelten Einträge.

Bei anderer interner Tastatur den Gerätenamen aus `hyprctl devices` übergeben:

```bash
INTERNAL_KEYBOARD=anderer-geraetename bash setup.sh
```

## Konfigurationsprotokoll

### 2026-09-28 – Externe Tastatur US-Mac, interne Deutsch-Mac

- Externes Apple Magic Keyboard mit Touch ID (`apple-inc.-magic-keyboard-with-touch-id`): eigener Geräteblock mit `kb_layout = "us"`, `kb_variant = "mac"` in `~/.config/hypr/input.lua`.
- Interne Tastatur (`apple-spi-keyboard`) bleibt bei `de`/`mac`. Beide Layouts nach Hyprland-Reload geprüft; keine Konfigurationsfehler.
- `setup-external-keyboard.py` ist in `setup.sh` eingebunden und sichert die Datei vor Änderungen. Anderes externes Gerät bei einer späteren Installation mit `EXTERNAL_KEYBOARD=geraetename bash setup.sh` angeben.

### 2026-09-28 – Maus-Scrollrichtung umgekehrt

- `input.natural_scroll` von `false` auf `true` gesetzt, in `~/.config/hypr/input.lua`. Verbundene Maus: `logi-pop-mouse`.
- Die bereits natürliche Scrollrichtung des Trackpads bleibt erhalten.
- Automatisiert mit `setup-mouse.py`, eingebunden in `setup.sh`; sichert die Eingabekonfiguration vor Änderungen.
- Hyprland neu geladen, Konfigurationsfehler und aktive Scrollwerte geprüft.

### 2026-09-28 – Thunderbird öffnete ein leeres Profil

- Ursache: Das eingerichtete iCloud-Profil wurde nur vom Starter „iCloud Mail“ explizit gewählt. Beim normalen Thunderbird-Start entstand ein separates, leeres Standardprofil; das iCloud-Konto war weiterhin in `omarchy-icloud/prefs.js` vorhanden.
- Reparatur: `omarchy-icloud` in `profiles.ini` registriert und als Standard gesetzt; vorhandene Installationszuordnungen in `profiles.ini` und `installs.ini` ebenfalls darauf umgestellt. Vorherige INI-Dateien werden mit Zeitstempel gesichert, andere Profile bleiben erhalten.
- `setup-mail.py` führt diese Zuordnung nun auch bei späteren Installationen aus. Thunderbird muss dabei geschlossen sein. Bestehende Kontoeinstellungen und gespeicherte Zugangsdaten werden nicht verändert oder ins Repository übernommen.

### 2026-09-28 – Bildschirmschoner auf eine Minute verkürzt

- Aktueller Sollwert: `idle.screensaver = 60` (1 Minute); automatische Sperre weiterhin `idle.lock = 28800` (8 Stunden), jeweils ab Beginn der Inaktivität.
- Die lokale `~/.config/omarchy/shell.json` enthielt bereits diese Werte. Mit `omarchy-shell idle status` bestätigt: Dienst aktiviert, `stayAwake: false`, Bildschirmschoner `60`, Sperre `28800` Sekunden. Keine weitere lokale Änderung nötig.
- `setup.sh` auf 60 Sekunden angepasst; ersetzt den früheren Bildschirmschonerwert von 600 Sekunden in den folgenden historischen Einträgen.

### 2026-09-28 – Defekte Menüübersetzung zurückgenommen

- Ursache: `setup-language-user.py` erzeugte Overrides mit ausschließlich `label`/`title`. Die installierte `MenuModel.js` normalisiert diese vor dem Zusammenführen mit den Originaleinträgen und setzt fehlende Felder auf leere Werte. Dadurch gingen 98 Aktionen, 2 dynamische Menüquellen und 141 Symbole verloren; Einträge wurden zu leeren Untermenüs.
- Reparatur: `~/.config/omarchy/extensions/omarchy-menu.jsonc` aus `omarchy-menu.jsonc.bak.20260928T103525925961Z` wiederhergestellt. Die defekte Übersetzung liegt lokal in `omarchy-menu.jsonc.broken-translation.20260928T112729Z` im selben Verzeichnis.
- Geprüft mit dem tatsächlich installierten Menümodell: Die Sicherung ergibt exakt das unveränderte Standardmenü. `omarchy menu refresh`, `omarchy menu ping` und das Öffnen des Hauptmenüs meldeten anschließend `ok`.
- Dauerhafte Änderung: Übersetzungsgenerator und `menu-de.json` entfernt. Auch erneutes Ausführen des Setups lässt die Menüdatei unverändert; Systemsprache, Anwendungssprachen und deutsches Uhrformat bleiben bestehen.
- Auf anderen bereits eingerichteten Rechnern repariert das Sprachskript alte Menü-Overrides nicht automatisch. Dort die passende Sicherung von vor der Übersetzung zurückspielen und `omarchy menu refresh` ausführen; eigene Menüanpassungen vorher sichern.
- Keine Neuinstallation erforderlich. Keine Änderung an paketverwalteten Omarchy-Dateien.

### 2026-09-28 – Interne Tastatur: Deutsch (Mac)

- Hardware: Apple SPI Keyboard, Hyprland-Name `apple-spi-keyboard`.
- Vorher: Layout `us`, keine Variante.
- Gewünscht: Deutsch (Macintosh), XKB-Layout `de`, Variante `mac`.
- Umsetzung: gerätespezifischer `hl.device`-Block in `~/.config/hypr/input.lua`.
- Bestehende Omarchy-Tastaturoptionen bleiben erhalten, darunter `compose:caps,shift:both_capslock_cancel`.
- Geltungsbereich: interne Tastatur in Hyprland; externe Tastaturen und Textkonsole erhalten keine globale Layoutänderung.
- Zusätzliche Pakete/Downloads: keine; das Layout ist bereits installiert.
- Durchgeführt und geprüft: `hyprctl reload` erfolgreich, `hyprctl configerrors` leer, aktives Layout der internen Tastatur `German (Macintosh)`.
- Sicherung dieser ersten Änderung: `~/.config/hypr/input.lua.bak.20260928T102023676244Z`.
- Wiederherstellung: den markierten Block entfernen oder die passende `input.lua.bak.*`-Sicherung zurückkopieren, anschließend `hyprctl reload` ausführen.

### 2026-09-28 – Bildschirmschoner und automatische Sperre

- Datei: `~/.config/omarchy/shell.json`.
- Vorher: `idle.screensaver = 150` (2,5 Minuten), `idle.lock = 300` (5 Minuten).
- Neu: `idle.screensaver = 600` (10 Minuten), `idle.lock = 28800` (8 Stunden).
- Beide Fristen zählen ab Beginn der Inaktivität. Nach Start des Bildschirmschoners bleiben somit 7 Stunden und 50 Minuten bis zur automatischen Sperre mit Passwortabfrage.
- Omarchy übernimmt die Einstellungen automatisch beim Speichern.
- Geprüft mit `omarchy-shell idle status`: Dienst aktiv (`enabled: true`), Bildschirmschoner `600`, Sperre `28800` Sekunden.
- Sicherung: `~/.config/omarchy/shell.json.bak.20260928T102241061133Z`.
- Das Skript sichert vorhandene Dateien mit Zeitstempel und erhält die übrigen JSON-Einstellungen.
- Manuelles Sperren und Sperren bei Suspend werden durch diese Inaktivitätsfristen nicht geändert.
- Zusätzliche Pakete/Downloads: keine.

Weitere gewünschte Einstellungen, Programme und Downloads werden hier und im Skript ergänzt.

### 2026-09-28 – Pianoteq nach Neustart geprüft und Startabsturz behoben

- Nach dem Neustart sind Echtzeitrechte aktiv: rtprio 90 und memlock 500000 KiB, sowohl in der Sitzung als auch im laufenden Pianoteq-Prozess. Audiothreads mit Echtzeitprioritäten 83/65 und MIDI-Thread mit 90 beobachtet.
- Pianoteq stürzte dennoch erneut mit SIGSEGV ab, an denselben Programmoffsets wie zuvor. Kein Hinweis auf Speichermangel. Der lokale Backtrace hat keine Modartt-Funktionssymbole; eine genaue interne Fehlerursache ist damit nicht belegt.
- Vergleichstest mit temporären Einstellungen: ohne `PIPEWIRE_NODE` startet Pianoteq; mit der zuvor eingerichteten Ausgangsfilterung trat der Absturz auf. Diese eigene Konfiguration wurde entfernt. Der Neustart allein konnte den Fehler nicht beheben.
- Neuer Startmechanismus: `~/.local/libexec/pianoteq-launch.py`, über `~/.local/bin/pianoteq` und den App-Menüeintrag. Keine Portfilterung. `jack.self-connect-mode = ignore-external` verhindert die falsche automatische Kopfhörerverbindung; ein separater `pw-link`-Aufruf verbindet ausschließlich die beiden Stereoausgänge des gestarteten Prozesses mit dem Desktop-Standardausgang.
- Der Installer verteilt den Helfer künftig mit. Die Auswahl in Pianoteq steht auf JACK / Auto-connect OFF; zusätzliche JACK-Selbstverbindungen werden ausdrücklich unterbunden.
- Geprüft: Programmstart und separater erneuter Start mit temporären Einstellungen erfolgreich; beide Stereokanäle ausschließlich über `audio_effect.j316-convolver` mit dem Asahi-Lautsprecher-DSP verbunden. 256 Samples bei 48 kHz, keine PipeWire-Fehler im kurzen Leerlauftest.
- Nutzer-Hörtest auf der Bildschirmklaviatur erfolgreich: **Ton ohne Knackser**. Physisches MIDI-Keyboard und langfristiger Lasttest sind damit noch nicht geprüft.
- Laufende Anwendung bleibt geöffnet. Vorheriger Launcher und persönliche Einstellungen wurden vor der Korrektur mit Zeitstempel gesichert; keine Aktivierungsdaten verändert.

### 2026-09-28 – Optik auf Omarchy-Standard zurückgesetzt

- Ersetzt die unten dokumentierten persönlichen Theme-, Schrift- und Transparenzanpassungen.
- Theme Tokyo Night; mitgelieferte Terminal- und Hyprland-Look-and-Feel-Konfigurationen wiederhergestellt.
- Persönliche Fontconfig-Overrides entfernt, GTK-Schriftwerte auf Schema-Standard zurückgesetzt. Monospace nutzt wieder JetBrainsMono Nerd Font.
- Ghostty bleibt Standardterminal, verwendet unter Linux jetzt die Omarchy-Standardkonfiguration samt dynamischer Theme-Anbindung.
- `setup-appearance.sh` stellt diese Standards wieder her; `setup-ghostty.sh` spielt die persönliche `config.ghostty` nicht mehr ein.
- Vorherige Benutzerkonfigurationen und GTK-Schriftwerte werden mit Zeitstempel gesichert.

### 2026-09-28 – Pianoteq 9.2.5 und Audio

- Grundlage: `README_LINUX.txt` aus dem selbst heruntergeladenen `pianoteq_setup_v925.tar.xz`; vollständig gelesen. Archiv-SHA256: `0ea69ca7a202dcc3a5a7d847688bb19bf6497e156c04f4f579fae82a73e36623`.
- ARM64-Standalone unter `~/.local/share/pianoteq/Pianoteq 9/arm-64bit/`; Menüeintrag **Pianoteq 9** und Startbefehl `pianoteq`. Deutsche Dokumentation und Linux-README im Installationsordner.
- VST3/LV2 über Links in `~/.vst3/` und `~/.lv2/` installiert. Archive, Binärdateien, Aktivierungsdaten und persönliche Presets werden nicht im Repository veröffentlicht.
- `pipewire-jack` ersetzt `jack2`; die JACK-Bibliotheksschnittstelle für andere Anwendungen bleibt vorhanden. Asahi-Audio, WirePlumber und speakersafetyd bleiben aktiv.
- Pianoteq-Audiosystem: JACK über PipeWire, zunächst **256 Samples bei 48 kHz**, also ein 64er-Vielfaches gemäß README. Das entspricht 5,33 ms pro Puffer, nicht der gesamten gemessenen Ein-/Ausgabelatenz.
- Startskript setzt `PIPEWIRE_LATENCY=256/48000` und verbindet nach dem Start per `pw-link` mit dem gewählten Desktop-Ausgang. Die ursprünglich verwendete Variable `PIPEWIRE_NODE` wurde wegen des reproduzierten Startabsturzes entfernt (siehe Nachprüfung oben). Bei Wechsel des Ausgabegeräts Pianoteq neu starten.
- Neue Echtzeitrechte nur für den Desktop-Benutzer: `/etc/security/limits.d/90-pianoteq-<Benutzer>.conf`, `rtprio 90`, `nice -10`, `memlock 500000` KiB. Entsprechend auch `/etc/systemd/system/user@<UID>.service.d/90-pianoteq.conf` für vom Desktop gestartete Anwendungen.
- **Einmal abmelden und wieder anmelden**, damit die laufende Desktop-Sitzung und der systemd-Benutzermanager diese Limits übernehmen. Frische PAM-Sitzung geprüft: rtprio 90, memlock 500000, Echtzeit-Scheduling-Test erfolgreich.
- CPU: `cpupower` installiert, `GOVERNOR='performance'` in `/etc/default/cpupower-service.conf`, `cpupower.service` aktiviert. Alle drei CPU-Cluster laufen im Performance-Modus. Diese Einstellung ist systemweit und dauerhaft, auch ohne Pianoteq; sie kann den Akkuverbrauch erhöhen. Thermische Schutzmechanismen bleiben aktiv.
- Zurück zum vorherigen dynamischen CPU-Modus: `sudo systemctl disable --now cpupower.service` und `sudo cpupower frequency-set -g schedutil`.
- Die Raspberry-Pi-spezifischen Taktwerte und die dort empfohlene Absenkung der Synthese-Samplerate werden auf diesem Apple-Silicon-Mac nicht übernommen.
- Erster Prüfstand: Desktopdatei, ARM64-Abhängigkeiten und JACK-Client geprüft; der Start um 13:12 Uhr scheiterte noch mit SIGSEGV. **Inzwischen behoben und nach dem Neustart einschließlich Nutzer-Hörtest erfolgreich geprüft**, siehe Nachprüfung oben.
- Erneute Installation: Archiv aus dem eigenen [Modartt-Konto](https://www.modartt.com/) herunterladen, dann `bash omarchy-setup/setup-pianoteq.sh /pfad/pianoteq_setup_v925.tar.xz`. Das Gesamtskript erkennt dieses Archiv im Downloads-Ordner oder über `PIANOTEQ_ARCHIVE`. Kein automatisierter Download mit Zugangsdaten.
- Technische Referenzen: [PipeWire-JACK-Konfiguration](https://docs.pipewire.org/page_man_pipewire-jack_conf_5.html), [Asahi-Audiostack](https://asahilinux.org/docs/sw/audio-userspace/).

### 2026-09-28 – Einheitliches Erscheinungsbild, weniger Transparenz

- Systemdesign: Omarchy `Catppuccin` (Mocha, dunkel), passend zu Ghosttys dunkler Variante; zuvor Tokyo Night.
- Schrift: `IBM Plex Mono` über `omarchy font set` für Terminals, Leiste und Monospace-Anwendungen; zusätzlich Fontconfig-Sans-Serif-Zuordnung sowie GTK-Oberflächen-, Dokument- und Titelschrift. Oberfläche 11 pt, Ghostty weiterhin 14 pt.
- Ghostty-Hintergrunddeckkraft von 0,2 auf 0,95 erhöht (5 % Transparenz), inaktive Splits ebenfalls 0,95 statt 0,5. Quelle `config.ghostty` angepasst.
- Hyprland: zusätzliche Omarchy-Fenstertransparenz für `default-opacity` auf `1.0 1.0` gesetzt. So bleiben Texte scharf und Ghosttys eigene Transparenz wird nicht nochmals verstärkt.
- Automatisierung: `setup-appearance.sh` und `setup-appearance.py`, im Gesamtskript eingebunden. Vorherige Benutzerdateien und GTK-Schriftwerte werden gesichert.
- Omarchys Theme-Unterstützung bestimmt die Reichweite: unterstützte Anwendungen erhalten Catppuccin, GTK-Anwendungen den passenden dunklen Modus. Programme mit eigenen Design-/Schriftvorgaben können davon abweichen.
- Geprüft: aktives Theme `Catppuccin`, Fontconfig für Monospace und Sans-Serif `IBM Plex Mono`, Ghostty-Deckkraft 0,95, Ghostty-Validierung und Hyprland-Konfiguration ohne Fehler.

### 2026-09-28 – Ghostty und gemeinsames Konfigurationsrepository

- Repository: https://github.com/toschku/config, bestehender Hauptbranch `haupt`.
- Lokaler Checkout: `~/Work/config`; Einrichtungsskripte unter `omarchy-setup/`.
- Pakete: `ghostty` 1.3.1-1, `ttf-ibm-plex`; Ghostty-Shell-Integration und Terminfo werden als Abhängigkeiten installiert.
- Quelle: vorhandene `config.ghostty` im Repository. Diese bleibt auch für macOS nutzbar.
- Linux-Version wird durch `setup-ghostty.py` erzeugt und nach Validierung in `~/.config/ghostty/config` installiert.
- Übernommen: Deutsch, IBM Plex Mono 14, Catppuccin Latte/Mocha, Hintergrunddeckkraft 0,2, Split-Deckkraft 0,5, Innenabstände 28, Zwischenablageschutz und weitere plattformunabhängige Einstellungen.
- Anpassungen: macOS-Optionen und macOS-Schrittgrößen beim Skalieren entfallen; `background-blur = true`, `window-decoration = none`. Die tatsächliche Hintergrundunschärfe hängt vom Compositor ab.
- Omarchy-Terminalintegration: SSH-Terminfo, Shift+Enter/Alt+Shift+Enter und Zwischenablage-Tastenkürzel; `async-backend = epoll`.
- Standardterminal: `omarchy default terminal ghostty` (Datei `~/.config/xdg-terminals.list`).
- Frühere Dateien werden mit Zeitstempel gesichert. Für Änderungen an der Ghostty-Quelle `bash omarchy-setup/setup-ghostty.sh` erneut ausführen.
- Sämtliche bisherigen Setup-Skripte und das Protokoll werden gemeinsam versioniert; keine privaten Schlüssel, Tokens oder Thunderbird-Profildaten übernommen.
- Geprüft: Ghostty-Konfiguration ohne Validierungsfehler, Schrift `IBM Plex Mono` verfügbar, Standardterminal `ghostty`, Syntax aller Python- und Shell-Skripte korrekt.

### 2026-09-28 – Git, SSH und GitHub

- GitHub-Konto: `Toschku` (API-Login `toschku`).
- Git-Identität: `Toschku <maxim.boeckelmann@hey.com>`, ausdrücklich gewünschte HEY-Adresse. Sie sollte bei GitHub bestätigt sein, damit Commits korrekt zugeordnet werden.
- Git-Vorgaben: neuer Branch `main`, automatisches Upstream beim ersten Push; vorhandene Omarchy-Einstellungen wie Rebase beim Pull bleiben erhalten.
- Pakete: `git`, `openssh`, `github-cli`. Git und OpenSSH waren bereits installiert; GitHub-CLI 2.101.0-1 ergänzt.
- Der vorhandene `~/.local/bin/gh`-Wrapper wurde gesichert und auf `/usr/bin/gh` umgestellt, damit das Systempaket verwendet wird.
- SSH-Schlüssel für diesen Rechner: `~/.ssh/id_ed25519_github`, Typ Ed25519. Die Passphrase wird direkt im Terminal eingegeben. Private Schlüssel und Passwörter gehören nicht in diesen Setup-Ordner.
- GitHub-SSH-Konfiguration in `~/.ssh/config`: Benutzer `git`, eigener Schlüssel, `IdentitiesOnly yes`, `AddKeysToAgent yes`, strikte Hostschlüsselprüfung.
- GitHubs öffentliche Hostschlüssel werden über die HTTPS-API `https://api.github.com/meta` abgerufen und in `~/.ssh/github_known_hosts` hinterlegt.
- SSH-Agent als systemd-Benutzerdienst: `~/.config/systemd/user/ssh-agent.service`, Socket `/run/user/<UID>/ssh-agent.socket`. Startet automatisch bei der Anmeldung.
- Nach einer neuen Desktop-Anmeldung wird die Schlüssel-Passphrase beim ersten Git-SSH-Zugriff im Terminal abgefragt und anschließend im Agent für die Sitzung gehalten. Vorab entsperren: `SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket" ssh-add ~/.ssh/id_ed25519_github`.
- `setup.sh` ruft `setup-git.sh` auf und startet am Ende bei interaktiver Ausführung `connect-github.sh`: Schlüssel erzeugen/entsperren, Browser-Anmeldung, Kontoprüfung, öffentlichen Schlüssel bei GitHub registrieren und SSH-Verbindung prüfen. Separat wiederholbar mit `bash connect-github.sh`.
- Geprüft: SSH-Konfiguration, aktiver SSH-Agent und erfolgreicher Test-Commit mit der gewünschten Git-Identität. GitHub-Anmeldung als `toschku` und SSH-Authentifizierung am 2026-09-28 um 12:43 Uhr (Europe/Berlin) erfolgreich abgeschlossen; GitHub-CLI bestätigt Speicherung im System-Schlüsselbund und Git-Protokoll SSH.
- Die GitHub-CLI verwendet den System-Schlüsselbund für die Anmeldung, sofern verfügbar. Im Einrichtungsskript werden keine Tokens gespeichert.
- Status einer erfolgreichen Verbindung: `~/.local/state/omarchy-setup/github-connected`. Das Skript schreibt diese Datei erst nach erfolgreicher GitHub-SSH-Authentifizierung.
- Es werden keine Repositories veröffentlicht und keine Commits zu GitHub übertragen.

Alltägliche Verwendung:

```bash
gh repo clone Toschku/REPOSITORY
cd REPOSITORY
# Änderungen bearbeiten
git add DATEI
git commit -m "Beschreibung der Änderung"
git push
# Änderungen von GitHub holen:
git pull
```

### 2026-09-28 – Deutsche Systemsprache und Anwendungen

- Systemsprache und regionale Formate: `de_DE.UTF-8`; Übersetzungsreihenfolge `de_DE:de:en_US:en`.
- `/etc/locale.gen`: deutsche UTF-8-Locale aktiviert und mit `locale-gen` erzeugt; englische Locale bleibt verfügbar.
- `/etc/locale.conf`: `LANG=de_DE.UTF-8`, `LANGUAGE=de_DE:de:en_US:en`.
- Desktop-Umgebung: gleiche Vorgaben in `~/.config/environment.d/60-personal-language.conf`, `~/.config/uwsm/env` und als `hl.env`-Einträge in `~/.config/hypr/hyprland.lua`.
- Chromium: `--lang=de` in `~/.config/chromium-flags.conf`; wird nach vollständigem Beenden und erneutem Öffnen aktiv, auch für Chromium-Webapp-Fenster. Die Sprache der Webseiten selbst hängt vom jeweiligen Dienst ab.
- Sprachpakete/Wörterbücher installiert: `libreoffice-fresh-de`, `hunspell-de`, `hyphen-de`, `mythes-de`, `tesseract-data-deu`. Thunderbird war bereits Deutsch; GTK-/KDE-Anwendungen wie Dateien, Evince, Xournal++ und Kdenlive enthalten deutsche Übersetzungen und verwenden die Systemsprache.
- Omarchy-Menü: bleibt im englischen Original. Die ursprünglich eingerichteten deutschen Benutzer-Overrides wurden wegen des unten dokumentierten Fehlers zurückgenommen; das Sprachskript verändert die Menüdefinitionen nicht mehr.
- Uhr: deutsche Wochentage/Monate durch die Sitzungssprache; alternatives Datumsformat `d. MMMM yyyy 'KW' ww`.
- Sicherungen: geänderte bestehende Dateien werden vor dem Schreiben als `*.bak.<UTC-Zeitstempel>` gesichert.
- Automatisierung: `setup.sh` ruft `setup-language.sh` auf. Dieses führt die System- und Benutzerkonfiguration aus und installiert Sprachpakete für vorhandene Anwendungen. Gesamten Setup-Ordner aufbewahren; als normaler Benutzer ausführen, Root-Rechte werden über `sudo` angefordert.
- Geprüft: Syntax, wiederholte Ausführung der Benutzerkonfiguration ohne weitere Änderungen, Erhalt vorhandener Einstellungen, deutsche Locale-Ausgabe, installierte Pakete, Hyprland ohne Konfigurationsfehler, Omarchy-Shell erreichbar. Bildschirmschoner/Sperre weiterhin 600/28800 Sekunden.
- Für alle laufenden Programme einmal abmelden und wieder anmelden. Keine automatische Abmeldung durchgeführt.
- Grenzen: Omarchy enthält fest englisch programmierte Dialoge, Hilfetexte und dynamische Menüeinträge. Diese werden durch eine Locale-Einstellung nicht übersetzt. Anwendungsinterne Sprachvorgaben und Webdienste können ebenfalls eigene Einstellungen benötigen. Keine Änderungen an paketverwalteten Omarchy-Dateien.

### 2026-09-28 – Thunderbird für iCloud Mail

- Installiert: `thunderbird`, `thunderbird-i18n-de` (156.0-1); Abhängigkeiten werden durch den Paketmanager installiert.
- Konto: `maxim.boeckelmann@mac.com`, Anzeigename: Maxim Boeckelmann.
- Eigenes Profil: `~/.thunderbird/omarchy-icloud`; App-Menü: **iCloud Mail** (`~/.local/share/applications/omarchy-icloud.desktop`).
- IMAP: `imap.mail.me.com:993`, SSL/TLS, Benutzername `maxim.boeckelmann`.
- SMTP: `smtp.mail.me.com:587`, STARTTLS, Benutzername `maxim.boeckelmann@mac.com`.
- Authentifizierung: Passwort über die verschlüsselte Verbindung; App-spezifisches Apple-Passwort erforderlich.
- `setup.sh` installiert die Pakete und ruft `setup-mail.py` auf. Dieses initialisiert das Profil nur einmal; spätere Kontoeinstellungen werden bei erneutem Aufruf erhalten.
- HEY bleibt separat verfügbar; das Skript setzt keinen Standard-Mailclient.
- Noch manuell erforderlich: Unter [Apple Account](https://account.apple.com/) → Anmelden und Sicherheit → App-spezifische Passwörter ein Passwort für Thunderbird erstellen und direkt in Thunderbird eingeben. Keine Passwörter im Skript oder Protokoll.
- Bei abgelehntem IMAP-Benutzernamen laut Apple alternativ die vollständige Mailadresse in den Kontoeinstellungen verwenden.
- Quellen: [Apple-Servereinstellungen](https://support.apple.com/de-de/102525), [App-spezifische Passwörter](https://support.apple.com/de-de/102654).
- Die Anmeldung sowie Empfang und Versand können erst nach Eingabe des Passworts geprüft werden.

### 2026-09-28 – Codex ohne einzelne Befehlsfreigaben

- Auf ausdrücklichen Wunsch: `approval_policy = "never"` und `sandbox_mode = "danger-full-access"` in `~/.codex/config.toml`. Damit darf Codex mit den Rechten des angemeldeten Benutzers ohne Sandbox und ohne Befehlsfreigaben arbeiten. Betriebssystemrechte und sudo bleiben separat.
- `setup.sh` ruft `setup-codex.py` auf; bestehende Einstellungen bleiben erhalten und werden vor einer Änderung gesichert. Keine Zugangsdaten im Repository.
- Die untersuchte Sitzung wurde mit `codex resume` gestartet; bisher waren keine dauerhaften Berechtigungsdefaults gesetzt. Ghostty setzt diese Berechtigungen nicht.
- Für die aktuelle Sitzung Codex beenden und mit `codex --dangerously-bypass-approvals-and-sandbox resume --last` fortsetzen. Für neue direkte Starts reicht anschließend `codex`.
- Omarchys Agent-Starter übergibt derzeit `--approve-for-me` und kann dadurch die Defaults überschreiben. Für Vollzugriff Codex direkt im Terminal starten; keine paketverwalteten Starter verändert.
- Einstellungen nach der [offiziellen OpenAI-Konfigurationsreferenz](https://learn.chatgpt.com/docs/config-file/config-reference).
