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

Ghostty separat installieren oder nach Änderungen an `config.ghostty` neu konfigurieren:

```bash
bash omarchy-setup/setup-ghostty.sh
```

Unter Linux werden die macOS-spezifischen Optionen weggelassen, die Unschärfe auf `true` gesetzt und Fensterdekorationen ausgeblendet. Schrift, Größe, Farben, Transparenz und Abstände stammen aus `config.ghostty`. Vorhandene Konfigurationen werden vor Änderungen gesichert.

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
