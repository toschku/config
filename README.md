# Persönliche Konfiguration

Meine Ghostty-Konfiguration und ein reproduzierbares Einrichtungsskript für Omarchy.

- [`config.ghostty`](config.ghostty): ursprüngliche Ghostty-Konfiguration, einschließlich macOS-Einstellungen.
- [`omarchy-setup/`](omarchy-setup/README.md): Einrichtungsskripte und ausführliches Änderungsprotokoll für Omarchy.

## Neue Omarchy-Installation einrichten

Im Terminal als normaler Desktop-Benutzer ausführen:

```bash
git clone https://github.com/toschku/config.git ~/Work/config
cd ~/Work/config
bash omarchy-setup/setup.sh
```

Das Skript installiert die benötigten Pakete und richtet Tastatur, Bildschirmschoner/Sperre, deutsche Sprache, Thunderbird für iCloud, Git/SSH und Ghostty ein. Für Systemänderungen wird `sudo` verwendet. Am Ende führt es durch die GitHub-Anmeldung und die Erstellung eines SSH-Schlüssels für den jeweiligen Rechner. Das iCloud-App-Passwort wird direkt in Thunderbird eingegeben.

Das Omarchy-Menü bleibt im englischen Original. Die fehlerhafte eigene Menüübersetzung wurde entfernt; das Sprachsetup verändert Menüdefinitionen nicht mehr.

Das Erscheinungsbild verwendet die Omarchy-Standardwerte: Tokyo Night, Standardfonts und Standardtransparenz. Ghostty bleibt Standardterminal und nutzt Omarchys mitgelieferte Konfiguration. Optik separat zurücksetzen: `bash omarchy-setup/setup-appearance.sh`.

Pianoteq wird mit eingerichtet, wenn das selbst heruntergeladene Linux-Archiv `~/Downloads/pianoteq_setup_v925.tar.xz` vorhanden ist (alternativer Pfad: `PIANOTEQ_ARCHIVE`). Separat: `bash omarchy-setup/setup-pianoteq.sh /pfad/zum/archiv.tar.xz`. Das richtet auch Echtzeitrechte, PipeWire-JACK und einen dauerhaften Performance-CPU-Modus ein; Details und Rückstellung stehen im Protokoll. Lizenz und Download verbleiben lokal.

Ghostty separat mit Omarchy-Standardkonfiguration installieren:

```bash
bash omarchy-setup/setup-ghostty.sh
```

Unter Linux wird die mitgelieferte Omarchy-Konfiguration für Ghostty verwendet; `config.ghostty` wird dort nicht eingespielt. Vorhandene Konfigurationen werden vor Änderungen gesichert.

## Mit GitHub synchronisieren

Nach erfolgreicher GitHub-Anmeldung kann der Checkout auf SSH umgestellt werden:

```bash
git remote set-url origin git@github.com:toschku/config.git
git pull --rebase
# Konfigurationen bearbeiten und gezielt hinzufügen:
git add README.md config.ghostty omarchy-setup
git commit -m "Konfiguration aktualisieren"
git push
```

Das Repository enthält keine privaten SSH-Schlüssel, Passwörter, Tokens oder Maildaten. Diese werden auf jedem Rechner separat erzeugt bzw. eingegeben. Commit-Name und E-Mail-Adressen stehen als persönliche Einstellungen im Skript.
