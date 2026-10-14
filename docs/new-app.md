# Bringing up a new FreeANDIY app

FreeANDIY Photo (freeandiy-photo) is the reference: copy from its `freeandiy/` whatever fits.

## 1. Fork and skeleton

```
scripts/fork-app.sh vector
```

The script refuses to continue unless the upstream ships `LICENSE-MIT` and `LICENSE-APACHE` and
declares `MIT OR Apache-2.0`. Also read upstream's `ATTRIBUTION.md`/`NOTICE` and check every
bundled asset (fonts, icons, images, sounds): anything without a clear open licence stops the
work until it is cleared.

## 2. Find what must change

In the clone, on `upstream-main`:

```
git grep -n -i -E 'artcraft|storyteller|discord|getartcraft|crafting apps'
git grep -n -E 'https?://' -- '*.rs' | grep -v -E 'localhost|127\.0\.0\.1|w3\.org|schemas'
```

- every UI string with the upstream name (menus, About, title bar, start screen, translations),
- links and buttons to ArtCraft services (Discord, website, community feeds, update checks):
  remove them; nothing may contact ArtCraft infrastructure,
- app ids (`ai.storyteller.<app>`), MSI GUIDs, packaging names, settings directories,
- the theme (tokens) and UI fonts, the About dialog.

## 3. Write freeandiy/

- `app.toml`: cargo packages, tests, web page, check exceptions.
- `rules.toml`: start from freeandiy-photo's; rename PhotoCraft/photocraft to the upstream's
  names. Order matters: URL/id rules, then protect rules (crate names, cargo `-p`, source paths),
  then name rules, then restore rules. Give each rule a `min` so upstream drift fails loudly.
- `patches/`: code changes a text rule can't express (removing a Discord button, the About
  attribution, theme hooks). Author them in a worktree of `upstream-main` and save with
  `git diff`; one topic per patch.
- `templates/freeandiy.rs`: constants, colours, theme tokens, the About attribution
  (`{{key}}` placeholders from branding.toml).
- `overlay/`: README.md, CHANGELOG-FREEANDIY.md, assets/app-icon/{README.md,LICENSE.txt}, the Slovak
  catalogue `sk.tsv` (and the `sk` row patch in the language registry).
- `tools/make_dmg.py` writes `assets/dmg/`; icons come from the meta repository.

Then:

```
freeandiy/scripts/regenerate.sh          # main = upstream + freeandiy/
freeandiy/scripts/check-branding.sh
cargo build --release $(…build.bins)     # and the tests in build.tests
```

## 4. Must hold before the first release

- LICENSE-MIT, LICENSE-APACHE, NOTICE and ATTRIBUTION.md kept; NOTICE only appended to.
- The About shows the attribution: "<App> is based on the open-source project <Upstream>
  (© ArtCraft Team and contributors, MIT/Apache-2.0). FreeANDIY is not affiliated with the
  ArtCraft team." and keeps any trademark disclaimer upstream has (e.g. Adobe).
- App id `agency.freeandy.<app>`, MSI ids from branding.toml.
- No ArtCraft name, logo, link or network call in the UI, installers or metadata.
- Signing certificates only as GitHub secrets, never in the repository.
- Repository: name `freeandiy-<app>`, topic `freeandiy`, description starting "FreeANDIY –".

Tag `v<upstream version>-fa.<n>` to build a draft release.
