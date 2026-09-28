#!/usr/bin/env bash
set -euo pipefail
git_setup_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
omarchy pkg add git openssh github-cli
pacman -Q git openssh github-cli >/dev/null
python3 "$git_setup_dir/setup-git.py"
systemctl --user daemon-reload
systemctl --user enable --now ssh-agent.service
echo "Git eingerichtet. GitHub verbinden: bash $git_setup_dir/connect-github.sh"
