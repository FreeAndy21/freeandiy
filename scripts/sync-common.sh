#!/usr/bin/env bash
# Modified-by: FreeANDIY (Free Andy Agency), 2026. New file.
#
# Copy the shared FreeANDIY files (common/) into the local clones of the app repositories.
#
#   scripts/sync-common.sh [APP ...]     (default: every app whose clone exists)
#
# Clones are expected next to this repository: ../freeandiy-<app>. Each gets, under freeandiy/:
# branding.toml, scripts/, tools/ (rebrand, icon and DMG generators), docs/, assets/brand,
# assets/fonts, assets/icons/<app>, and overlay/.github/workflows/. App-specific files
# (app.toml, rules.toml, patches/, templates/, the rest of overlay/) are left alone.
# Review and commit in each clone afterwards; nothing is committed or pushed here.
set -euo pipefail
META="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
C="$META/common"
apps=()
[ $# -gt 0 ] && apps=("$@")
if [ ${#apps[@]} -eq 0 ]; then
  while IFS= read -r a; do apps+=("$a"); done < <("$META/scripts/apps.py" list)
fi

for app in "${apps[@]}"; do
  repo="$("$META/scripts/apps.py" get "$app" repo)"
  dest="$META/../$repo"
  if [ ! -d "$dest/.git" ]; then
    [ $# -gt 0 ] && echo "skip $app: no clone at $dest" >&2
    continue
  fi
  F="$dest/freeandiy"
  mkdir -p "$F/assets/icons" "$F/overlay/.github/workflows"
  cp "$C/branding.toml" "$C/.gitignore" "$F/"
  rsync -a --delete "$C/scripts/" "$F/scripts/"
  rsync -a --delete "$C/docs/" "$F/docs/"
  rsync -a --delete --exclude target/ --exclude __pycache__/ "$C/tools/" "$F/tools/"
  rsync -a --delete "$C/assets/brand/" "$F/assets/brand/"
  rsync -a --delete "$C/assets/fonts/" "$F/assets/fonts/"
  rsync -a --delete "$C/assets/icons/$app/" "$F/assets/icons/$app/"
  rsync -a "$C/overlay/.github/workflows/" "$F/overlay/.github/workflows/"
  echo "synced $app -> $dest ($(git -C "$dest" status --porcelain -- freeandiy | wc -l | tr -d ' ') changed path(s))"
done
