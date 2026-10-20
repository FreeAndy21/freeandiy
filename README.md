# FreeANDIY

FreeANDIY is a family of free, open-source creative and office apps by [Free Andy Agency](https://freeandy.agency):
rebranded builds of the open-source *Craft apps by the ArtCraft team (MIT OR Apache-2.0).
FreeANDIY is not affiliated with the ArtCraft team.

This is the meta repository. It holds what every FreeANDIY app shares; the apps live in their
own repositories.

| App | Repository | Based on | Slovak UI | FreeANDIY CI |
|---|---|---|---|---|
| FreeANDIY Photo | [freeandiy-photo](https://github.com/FreeAndy21/freeandiy-photo) | PhotoCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-photo/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-photo/actions/workflows/freeandiy.yml) |
| FreeANDIY Vector | [freeandiy-vector](https://github.com/FreeAndy21/freeandiy-vector) | VectorCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-vector/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-vector/actions/workflows/freeandiy.yml) |
| FreeANDIY PDF | [freeandiy-pdf](https://github.com/FreeAndy21/freeandiy-pdf) | PdfCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-pdf/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-pdf/actions/workflows/freeandiy.yml) |
| FreeANDIY Light | [freeandiy-light](https://github.com/FreeAndy21/freeandiy-light) | LightCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-light/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-light/actions/workflows/freeandiy.yml) |
| FreeANDIY Write | [freeandiy-write](https://github.com/FreeAndy21/freeandiy-write) | WordCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-write/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-write/actions/workflows/freeandiy.yml) |
| FreeANDIY Sheets | [freeandiy-sheets](https://github.com/FreeAndy21/freeandiy-sheets) | GridCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-sheets/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-sheets/actions/workflows/freeandiy.yml) |
| FreeANDIY Slides | [freeandiy-slides](https://github.com/FreeAndy21/freeandiy-slides) | DeckCraft | — (upstream has no translations) | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-slides/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-slides/actions/workflows/freeandiy.yml) |
| FreeANDIY Layout | [freeandiy-layout](https://github.com/FreeAndy21/freeandiy-layout) | DesignCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-layout/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-layout/actions/workflows/freeandiy.yml) |
| FreeANDIY Film | [freeandiy-film](https://github.com/FreeAndy21/freeandiy-film) | FilmCraft | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-film/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-film/actions/workflows/freeandiy.yml) |
| FreeANDIY Effects | [freeandiy-effects](https://github.com/FreeAndy21/freeandiy-effects) | EffectCraft | not yet | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-effects/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-effects/actions/workflows/freeandiy.yml) |
| FreeANDIY Sound | [freeandiy-sound](https://github.com/FreeAndy21/freeandiy-sound) | SoundCraft | — (upstream has no translations) | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-sound/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-sound/actions/workflows/freeandiy.yml) |
| FreeANDIY Launcher | [freeandiy-launcher](https://github.com/FreeAndy21/freeandiy-launcher) | ArtCraft Launcher | yes | [![FreeANDIY](https://github.com/FreeAndy21/freeandiy-launcher/actions/workflows/freeandiy.yml/badge.svg)](https://github.com/FreeAndy21/freeandiy-launcher/actions/workflows/freeandiy.yml) |

The website, <https://freeandiy-web.vercel.app>, lives in
[freeandiy-web](https://github.com/FreeAndy21/freeandiy-web). CADCraft and FigCraft are not
FreeANDIY apps (yet).

## Layout

```
common/                  copied into every app as freeandiy/ (scripts/sync-common.sh)
  branding.toml          names, colours, fonts, app ids, MSI ids of every app
  scripts/               regenerate, sync-upstream, check-branding, settings (CI)
  tools/rebrand/         the Rust tool that applies rules.toml to a pristine upstream tree
  tools/make_icons.py    app icons (macOS, Windows, Linux, SVG) from branding.toml
  tools/make_dmg.py      the macOS DMG window background and layout
  assets/                brand marks, fonts (OFL), app icons
  overlay/.github/       the FreeANDIY CI and release workflows
  docs/upstream-sync.md  how an app follows its upstream
scripts/
  fork-app.sh APP        fork the upstream, clone it, set up upstream-main and freeandiy/
  sync-common.sh [APP]   copy common/ into the local app clones
templates/app/           the starting app.toml
docs/new-app.md          how to bring up a new app
```

## How an app repository works

`upstream-main` mirrors the upstream project. `main` is generated from it: upstream plus the
app's `freeandiy/` directory (`rules.toml`, `patches/`, `templates/`, `overlay/`), applied by
`freeandiy/scripts/regenerate.sh`. Nothing outside `freeandiy/` is edited by hand, so following
upstream never conflicts. CI checks that `main` is exactly upstream + `freeandiy/` and that no
upstream branding ships. See [docs/new-app.md](docs/new-app.md).

## Licence

Scripts and tools: MIT OR Apache-2.0 (LICENSE-MIT, LICENSE-APACHE). Fonts: SIL OFL 1.1. The
FreeANDIY and Free Andy Agency marks and the app icons are protected by copyright and are the
property of Free Andy Agency; they are not open source (common/assets/brand/LICENSE-brand.txt).
See NOTICE.
