#!/usr/bin/env python3
# Modified-by: FreeANDIY (Free Andy Agency), 2026. New file.
"""Write a starting freeandiy/rules.toml for a *Craft app (the parts every app shares).

  scripts/make_rules.py APP [--catalogs GLOB] [--guids G1,G2…] [--extra FILE] > rules.toml

Reads common/branding.toml and the clone at ../<repo> (crate names under crates/, the WiX
component GUIDs, the macOS window icon). App-specific rules (links in code, About text, settings
folders, catalogs) go in --extra, a TOML fragment inserted before the name rules. Review the
result and run freeandiy/scripts/regenerate.sh: every rule has a minimum match count, so a rule
that misses fails loudly. See docs/new-app.md.
"""
import argparse
import re
import sys
import tomllib
from pathlib import Path

META = Path(__file__).resolve().parents[1]
CFG = tomllib.loads((META / "common/branding.toml").read_text())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app")
    ap.add_argument("--catalogs", default="crates/ui-egui/src/i18n/*.tsv", help="translation catalog glob")
    ap.add_argument("--extra", help="TOML fragment with app-specific rules")
    a = ap.parse_args()
    app = CFG["apps"][a.app]
    repo = app["repo"]
    up = app["upstream_name"]
    slug = app["upstream"].split("/")[1]
    root = META.parent / repo
    crates = sorted(p.name for p in (root / "crates").iterdir() if p.is_dir()) + ["web"]
    wxs = sorted((root / "packaging/windows").glob("*.wxs"))
    guids = []
    for w in wxs:
        guids += re.findall(r'Guid="([0-9A-Fa-f-]{36})"', w.read_text())
    main_rs = (root / f"apps/{slug}/src/main.rs").read_text() if (root / f"apps/{slug}/src/main.rs").exists() else ""
    macos_icon = re.search(rf"app-icon/{slug}-macos-(\d+)\.png", main_rs)
    extra = Path(a.extra).read_text() if a.extra else ""
    cat = a.catalogs
    out = []
    w = out.append
    w(f'''# FreeANDIY rebrand rules for this repository (applied by freeandiy/tools/rebrand, after the
# patches in freeandiy/patches/). Modified-by: FreeANDIY (Free Andy Agency), 2026.
#
# Double-brace placeholders (e.g. this.name) come from branding.toml and app.toml (`rebrand vars`
# lists them). Every rule has a minimum match count: when upstream renames or moves something, the
# rule fails loudly instead of silently leaving the old brand in place.
#
# Protected text: rules first swap text that must keep the upstream name (cargo package names,
# file names we keep, upstream's copyright) for @@...@@ markers, and the last rules swap them
# back. The product name is replaced as a whole word in code: type names like `{up}App` stay.

templates = [
  "crates/ui-egui/src/freeandiy.rs",
]

delete = [
  "docs/brand",                                  # ArtCraft marks: forks must remove them
  "assets/app-icon",                             # upstream's identity; ours is copied in below
  "packaging/icons.sh",                          # icons come from the FreeANDIY meta repository
  "packaging/macos/dmg",                         # background and layout derived from upstream's icon; ours is copied in
]

# Translation catalogs: drop the Discord entries (the strings are gone from the UI); other
# ArtCraft mentions become FreeANDIY below, so complete catalogs stay complete.
[[drop_lines]]
include = ["{cat}"]
regex = '^[^#\\n]*Discord'
min = 0

# ---------------------------------------------------------------------------------------------
# Identifiers, maintainers, URLs.

[[replace]]
name = "app id"
include = ["**"]
exclude = ["**/*.md", "docs/**", "NOTICE", "ATTRIBUTION.md"]
find = "ai.storyteller.{slug}"
replace = "{{{{this.app_id}}}}"
min = 10

[[replace]]
name = "developer id"
include = ["packaging/**"]
find = "ai.storyteller"
replace = "{{{{brand.id_prefix}}}}"
min = 0

[[replace]]
name = "package maintainer"
include = ["packaging/**"]
find = "{up} maintainers <{slug}@storyteller.ai>"
replace = "{{{{brand.maintainer}}}}"
min = 0

[[replace]]
name = "links in code: this app's page"
include = ["**/*.rs"]
find = "https://getartcraft.com/apps/{slug}"
replace = "{{{{this.page}}}}"
min = 0

[[replace]]
name = "links in code: repository, releases, issues"
include = ["**/*.rs"]
exclude = ["vendor/**"]
find = "https://github.com/storytold/{slug}"
replace = "{{{{this.github}}}}"
skip_comments = ["//"]
min = 0

[[replace]]
name = "link labels: this app's page (code and catalogs)"
include = ["**/*.rs", "{cat}"]
find = "getartcraft.com/apps/{slug}"
replace = "freeandiy.freeandy.agency/{{{{this.key}}}}"
skip_comments = ["//"]
min = 0

[[replace]]
name = "link labels: source repository (code and catalogs)"
include = ["**/*.rs", "{cat}"]
find = "github.com/storytold/{slug}"
replace = "github.com/{{{{brand.github_owner}}}}/{{{{this.repo}}}}"
skip_comments = ["//"]
min = 0

[[replace]]
name = "links in code: website"
include = ["**/*.rs"]
find = "https://getartcraft.com"
replace = "{{{{brand.website}}}}"
skip_comments = ["//"]
min = 0

[[replace]]
name = "labels: the website's host (code and catalogs)"
include = ["**/*.rs", "{cat}"]
exclude = ["xtask/**"]
find = "getartcraft.com"
replace = "freeandiy.freeandy.agency"
skip_comments = ["//"]
min = 0

[[replace]]
name = "website label (code and catalogs)"
include = ["**/*.rs", "{cat}"]
regex = 'ArtCraft [Ww]ebsite'
replace = "{{{{brand.name}}}} website"
min = 0

[[replace]]
name = "Crafting Apps"
include = ["crates/**/*.rs", "apps/**/*.rs", "packaging/**", "{cat}"]
find = "Crafting Apps"
replace = "{{{{brand.name}}}} apps"
min = 0

[[replace]]
name = "upstream issues URL"
include = ["packaging/**", ".github/**"]
find = "https://github.com/storytold/{slug}/issues"
replace = "{{{{this.issues}}}}"
min = 0

[[replace]]
name = "upstream repository URL"
include = ["packaging/**", ".github/**"]
regex = 'https://github\\.com/storytold/{slug}(/|"|<|\\x27|$)'
replace = "{{{{this.github}}}}${{1}}"
min = 0

[[replace]]
name = "upstream repo slug (raw URLs, GITHUB_REPOSITORY defaults)"
include = ["packaging/**", ".github/**"]
regex = 'storytold/{slug}\\b'
replace = "{{{{brand.github_owner}}}}/{{{{this.repo}}}}"
min = 0

[[replace]]
name = "upstream product page"
include = ["packaging/**", ".github/**", "apps/{slug}-web/index.html"]
find = "https://getartcraft.com/apps/{slug}"
replace = "{{{{this.page}}}}"
min = 0

[[replace]]
name = "upstream Discord (packaging contact/help links)"
include = ["packaging/**"]
find = "https://discord.gg/artcraft"
replace = "{{{{this.issues}}}}"
min = 0

# ---------------------------------------------------------------------------------------------
# Protect text that keeps the upstream name.

[[replace]]
name = "protect: upstream's copyright holder and contributors"
include = ["**/*.rs", "{cat}", "packaging/**"]
regex = 'ArtCraft Team and the {up} (contributors|authors)'
replace = 'ArtCraft Team and the @@UPSTREAM@@ ${{1}}'
min = 0

[[replace]]
name = "protect: upstream's copyright lines in the catalogs (ArtCraft, twice per line)"
include = ["{cat}"]
regex = '(?m)^([^\\n]*Copyright[^\\n]*?)ArtCraft'
replace = '${{1}}@@AC@@'
min = 0

[[replace]]
name = "protect: upstream's copyright lines in the catalogs (ArtCraft, 2nd)"
include = ["{cat}"]
regex = '(?m)^([^\\n]*Copyright[^\\n]*?)ArtCraft'
replace = '${{1}}@@AC@@'
min = 0

[[replace]]
name = "catalogs: other ArtCraft mentions"
include = ["{cat}"]
find = "ArtCraft"
replace = "{{{{brand.name}}}}"
min = 0

[[replace]]
name = "protect: attribution 'the {up} authors'"
include = ["apps/*/build.rs", "packaging/**"]
find = "the {up} authors"
replace = "{{{{brand.owner}}}} and the @@UPSTREAM@@ authors"
min = 0

[[replace]]
name = "web release zip: {repo}-<version>-web-wasm32.zip (before the crate-name protect)"
include = ["packaging/web/package.sh", "packaging/web/README.md", "docs/releasing.md"]
regex = '{slug}-web-(<version>|<v>|\\$VERSION)'
replace = "{{{{this.repo}}}}-${{1}}-web-wasm32"
min = 0

[[replace]]
name = "protect: cargo -p / --package {slug}"
include = ["packaging/**", ".github/**", "Dockerfile"]
regex = '(-p|--package) {slug}'
replace = '$1 @@PKG@@'
min = 1

[[replace]]
name = "protect: crate names {slug}-<crate>"
include = ["packaging/**", ".github/**", "Dockerfile"]
regex = '{slug}-({"|".join(re.escape(c) for c in crates)})\\b'
replace = '@@PKG@@-$1'
min = 0

[[replace]]
name = "protect: cargo features {slug}/<feature>"
include = ["packaging/**", ".github/**"]
find = "'{slug}/"
replace = "'@@PKG@@/"
min = 0

[[replace]]
name = "protect: source paths apps/{slug}"
include = ["packaging/**", ".github/**", "Dockerfile"]
regex = '(apps[/\\\\]){slug}'
replace = '${{1}}@@PKG@@'
min = 0

[[replace]]
name = "protect: crate idents {slug}_"
include = ["packaging/**", ".github/**", "Dockerfile"]
find = "{slug}_"
replace = "@@PKG@@_"
min = 0

[[replace]]
name = "protect: WiX sources {slug}.wxs/.wxl"
include = ["packaging/**", ".github/**", "Dockerfile"]
regex = '{slug}(\\.wxs|\\.en-us\\.wxl)'
replace = '@@PKG@@${{1}}'
min = 0
''')
    if extra:
        w("\n# ---------------------------------------------------------------------------------------------\n# App-specific rules.\n\n" + extra.strip() + "\n")
    w(f'''
# ---------------------------------------------------------------------------------------------
# The product name in the UI, messages, translations, packaging and the web page.

[[replace]]
name = "Info.plist custom keys: {up}Version, {up}BuildCommit"
include = ["packaging/**"]
regex = '{up}(Version|BuildCommit)'
replace = 'FreeANDIY{app["name"].split()[-1]}${{1}}'
min = 0

[[replace]]
name = "product name after an escaped newline in strings (\\\\n{up})"
include = ["**/*.rs"]
exclude = ["xtask/**"]
find = '\\n{up}'
replace = '\\n{{{{this.name}}}}'
skip_comments = ["//"]
min = 0

[[replace]]
name = "product name {up} (Rust code, not comments; whole word)"
include = ["**/*.rs"]
exclude = ["xtask/**", "vendor/**"]
regex = '\\b{up}\\b'
replace = "{{{{this.name}}}}"
skip_comments = ["//"]
min = 20

[[replace]]
name = "product name {up} (catalogs: any script or inflection may follow it)"
include = ["{cat}"]
regex = '{up}[a-z]*'
replace = "{{{{this.name}}}}"
min = 0

[[replace]]
name = "product name {up} (packaging, web page, CI)"
include = ["packaging/**", "apps/{slug}-web/index.html", ".github/**", "Dockerfile"]
exclude = ["**/*.md"]
regex = '\\b{up}\\b'
replace = "{{{{this.name}}}}"
min = 10

# ---------------------------------------------------------------------------------------------
# Executables, packaging file names.

[[replace]]
name = "test binaries CARGO_BIN_EXE_{slug}"
include = ["apps/**/*.rs"]
find = "CARGO_BIN_EXE_{slug}"
replace = "CARGO_BIN_EXE_{{{{this.repo}}}}"
min = 0

[[replace]]
name = "cli executable name in code and catalogs"
include = ["apps/**/*.rs", "crates/**/*.rs", "{cat}"]
regex = '\\b{slug}-cli\\b'
replace = "{{{{this.repo}}}}-cli"
min = 0

[[replace]]
name = "icon file paths in code (assets/app-icon/{slug}*)"
include = ["apps/**/*.rs", "crates/**/*.rs", "apps/*/build.rs", "xtask/**"]
find = "app-icon/{slug}"
replace = "app-icon/{{{{this.repo}}}}"
min = 1
''')
    if macos_icon:
        w(f'''
[[replace]]
name = "macOS window icon: our 1024 px tile"
include = ["apps/{slug}/src/main.rs"]
find = "app-icon/{{{{this.repo}}}}-macos-{macos_icon.group(1)}.png"
replace = "app-icon/{{{{this.repo}}}}-1024.png"
min = 1
''')
    w(f'''
[[replace]]
name = "windows exe resources"
include = ["apps/*/build.rs"]
regex = '"{slug}(\\.exe)?"'
replace = '"{{{{this.repo}}}}${{1}}"'
min = 0

[[replace]]
name = "packaging/CI: executables, file names, paths"
include = ["packaging/**", ".github/**", "Dockerfile"]
regex = '{slug}'
replace = "{{{{this.repo}}}}"
min = 20

[[replace]]
name = "MSI UpgradeCode (new GUID)"
include = ["packaging/windows/*.wxs"]
regex = 'UpgradeCode="[0-9A-Fa-f-]{{36}}"'
replace = 'UpgradeCode="{{{{this.msi_upgrade_code}}}}"'
min = 1
''')
    for i, g in enumerate(guids):
        key = "this.msi_component_guid" if i == 0 else f"msi.guid{i + 1}"
        w(f'''
[[replace]]
name = "MSI component GUID {i + 1} (new GUID)"
include = ["packaging/windows/*.wxs"]
find = "{g}"
replace = "{{{{{key}}}}}"
min = 1
''')
    w(f'''
# ---------------------------------------------------------------------------------------------
# Restore protected text.

[[replace]]
name = "restore @@UPSTREAM@@"
include = ["**"]
find = "@@UPSTREAM@@"
replace = "{{{{this.upstream_name}}}}"
min = 0

[[replace]]
name = "restore @@AC@@ (upstream's copyright holder)"
include = ["**"]
find = "@@AC@@"
replace = "ArtCraft"
min = 0

[[replace]]
name = "restore @@PKG@@"
include = ["**"]
find = "@@PKG@@"
replace = "{slug}"
min = 1

# ---------------------------------------------------------------------------------------------

# Upstream's README stays available; ours replaces it at the root.
[[rename]]
include = ["README.md"]
find = "README.md"
replace = "docs/upstream-README.md"
min = 1

[[rename]]
include = ["packaging/**"]
find = "ai.storyteller.{slug}"
replace = "{{{{this.app_id}}}}"
min = 1

[[copy]]
from = "freeandiy/overlay"
to = "."

[[copy]]
from = "freeandiy/assets/dmg"
to = "packaging/macos/dmg"

[[copy]]
from = "freeandiy/templates/freeandiy.rs"
to = "crates/ui-egui/src/freeandiy.rs"
''')
    icons = [
        ("{{this.key}}.svg", "{{this.repo}}.svg"),
        ("{{this.key}}.svg", "{{this.repo}}-small.svg"),
        ("mark-128.png", "{{this.repo}}-mark.png"),
        ("macos-1024.png", "{{this.repo}}-1024.png"),
        ("{{this.key}}.icns", "{{this.repo}}.icns"),
        ("{{this.key}}.ico", "{{this.repo}}.ico"),
        ("{{this.key}}.svg", "hicolor/scalable/apps/{{this.app_id}}.svg"),
    ] + [(f"hicolor/{n}.png", f"hicolor/{n}x{n}/apps/{{{{this.app_id}}}}.png") for n in (16, 24, 32, 48, 64, 128, 256, 512)]
    for src, dst in icons:
        w(f'''
[[copy]]
from = "freeandiy/assets/icons/{{{{this.key}}}}/{src}"
to = "assets/app-icon/{dst}"
''')
    w((META / "common/rules-windows-notices.toml").read_text())
    sys.stdout.write("".join(out))
    if len(guids) > 1:
        print(f"# NOTE: add to app.toml [msi]: " + ", ".join(f"guid{i + 1}" for i in range(1, len(guids))), file=sys.stderr)


if __name__ == "__main__":
    main()
