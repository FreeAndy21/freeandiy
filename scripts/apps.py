#!/usr/bin/env python3
# Modified-by: FreeANDIY (Free Andy Agency), 2026. New file.
"""Read common/branding.toml for the shell scripts.

  scripts/apps.py list                 app ids (in branding.toml order)
  scripts/apps.py get <app> <key>      one value of [apps.<app>] (or brand.<key> with brand.)
"""
import sys
import tomllib
from pathlib import Path

CFG = tomllib.loads((Path(__file__).resolve().parents[1] / "common/branding.toml").read_text())

if sys.argv[1:2] == ["list"]:
    print("\n".join(CFG["apps"]))
elif sys.argv[1:2] == ["get"] and len(sys.argv) == 4:
    app, key = sys.argv[2], sys.argv[3]
    if key.startswith("brand."):
        print(CFG["brand"][key[6:]])
    else:
        print(CFG["apps"][app][key])
else:
    sys.exit(__doc__)
