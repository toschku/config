#!/usr/bin/env bash
set -euo pipefail
umask 077
export SSH_AUTH_SOCK="${XDG_RUNTIME_DIR:-/run/user/$UID}/ssh-agent.socket"
key="$HOME/.ssh/id_ed25519_github"

if [[ ! -f "$key" ]]; then
  echo 'Erstelle einen SSH-Schlüssel für diesen Rechner.'
  echo 'Wähle im folgenden Dialog eine Passphrase; die Eingabe bleibt unsichtbar.'
  ssh-keygen -t ed25519 -a 100 -f "$key" -C "Toschku@$(hostname) GitHub"
fi
if [[ ! -f "$key.pub" ]]; then
  ssh-keygen -y -f "$key" > "$key.pub"
fi
fingerprint="$(ssh-keygen -lf "$key.pub" | awk '{print $2}')"
if ! ssh-add -l 2>/dev/null | grep -Fq "$fingerprint"; then
  ssh-add "$key"
fi

if ! /usr/bin/gh auth status --hostname github.com >/dev/null 2>&1; then
  echo 'Melde dich im Browser mit deinem GitHub-Konto Toschku an.'
  /usr/bin/gh auth login --hostname github.com --git-protocol ssh --web --skip-ssh-key --scopes admin:public_key
fi
login="$(/usr/bin/gh api user --jq .login)"
if [[ "${login,,}" != toschku ]]; then
  echo "Angemeldet als $login statt Toschku. Bitte zuerst das richtige GitHub-Konto auswählen." >&2
  exit 1
fi
/usr/bin/gh config set git_protocol ssh --host github.com
public_key="$(awk '{print $1 " " $2}' "$key.pub")"
registered="$(/usr/bin/gh api --paginate user/keys --jq '.[].key')"
if ! grep -Fxq "$public_key" <<< "$registered"; then
  /usr/bin/gh ssh-key add "$key.pub" --title "Omarchy $(hostname) $(date +%Y-%m-%d)"
fi

set +e
result="$(LC_ALL=C ssh -T -o BatchMode=yes -o ConnectTimeout=15 git@github.com 2>&1)"
status=$?
set -e
printf '%s\n' "$result"
if [[ "$status" -ne 1 || "${result,,}" != *"hi toschku! you've successfully authenticated"* ]]; then
  echo 'SSH-Verbindung konnte noch nicht bestätigt werden.' >&2
  exit 1
fi
state="${XDG_STATE_HOME:-$HOME/.local/state}/omarchy-setup"
mkdir -p "$state"
date --iso-8601=seconds > "$state/github-connected"
echo 'Fertig: GitHub-Anmeldung und SSH-Zugriff auf Toschku erfolgreich geprüft.'
echo 'Repository klonen: gh repo clone Toschku/REPOSITORY'
