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
- Omarchy-Menü: deutsche Beschriftungen als Benutzer-Overrides in `~/.config/omarchy/extensions/omarchy-menu.jsonc`. Die Zuordnung steht in `menu-de.json`; Aktionen und Bedingungen kommen weiterhin aus Omarchys Originaldefinitionen.
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
