#!/usr/bin/env bash
# Modified-by: FreeANDIY (Free Andy Agency), 2026. New file.
#
# Start a FreeANDIY app: fork its upstream on GitHub, clone it next to this repository, set up
# the upstream mirror branch and the freeandiy/ skeleton.
#
#   scripts/fork-app.sh APP
#
# 1. gh repo fork <upstream> as <owner>/<repo> (default branch only), set the description
#    ("FreeANDIY – <App>: …"), homepage and the `freeandiy` topic
# 2. clone to ../<repo>, add the `upstream` remote, create `upstream-main` (pristine upstream)
# 3. freeandiy/app.toml from templates/app/, then scripts/sync-common.sh APP
# Writing the app's rules.toml, patches and templates is the manual part (docs/new-app.md).
# Only touches the new repository; never other repositories of the account.
set -euo pipefail
META="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
app="${1:?usage: scripts/fork-app.sh APP}"
get() { "$META/scripts/apps.py" get "$app" "$1"; }
owner="$(get brand.github_owner)"
repo="$(get repo)"
upstream="$(get upstream)"
up_name="$(get upstream_name)"
label="$(get name | sed 's/^FreeANDIY //')"
desc="FreeANDIY – $label: free open-source $(get tagline) (based on $up_name, MIT/Apache-2.0)"
dest="$META/../$repo"

# Licence gate: upstream must ship both licence files and declare MIT OR Apache-2.0.
for f in LICENSE-MIT LICENSE-APACHE; do
  gh api "repos/$upstream/contents/$f" --silent || { echo "error: $upstream has no $f; stop and check its licence" >&2; exit 1; }
done
gh api "repos/$upstream/contents/Cargo.toml" --jq .content | base64 -d | grep -q '^license = "MIT OR Apache-2.0"' \
  || { echo "error: $upstream's Cargo.toml does not declare MIT OR Apache-2.0; stop and check" >&2; exit 1; }

if gh repo view "$owner/$repo" >/dev/null 2>&1; then
  echo "$owner/$repo exists; not forking again"
else
  gh repo fork "$upstream" --fork-name "$repo" --default-branch-only --clone=false
  for _ in 1 2 3 4 5 6; do gh repo view "$owner/$repo" >/dev/null 2>&1 && break; sleep 5; done
fi
# A fresh fork finishes copying asynchronously and can reset the description: retry until it sticks.
for _ in 1 2 3 4 5 6; do
  gh repo edit "$owner/$repo" --description "$desc" --homepage "$(get brand.website)" --add-topic freeandiy
  sleep 5
  [ "$(gh repo view "$owner/$repo" --json description -q .description)" = "$desc" ] && break
done
gh api -X PUT "repos/$owner/$repo/actions/permissions" -F enabled=true -f allowed_actions=all --silent || true

if [ ! -d "$dest/.git" ]; then
  git clone "https://github.com/$owner/$repo.git" "$dest"
fi
cd "$dest"
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "https://github.com/$upstream.git"
git fetch --quiet upstream
default="$(git remote show upstream | sed -n 's/.*HEAD branch: //p')"
git branch --force upstream-main "upstream/$default"
git push --quiet origin upstream-main

mkdir -p freeandiy
if [ ! -f freeandiy/app.toml ]; then
  sed -e "s/@APP@/$app/g" -e "s/@UPSTREAM_NAME@/$up_name/g" "$META/templates/app/app.toml" > freeandiy/app.toml
fi
"$META/scripts/sync-common.sh" "$app"
echo "ready: $dest (upstream-main = $upstream $default). Next: docs/new-app.md"
