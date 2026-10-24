#!/usr/bin/env python3
"""Generates index.txt for the CosmoCosmetics online database.

Run it in the folder that contains your cosmetic folders (each with cosmetic.png + cosmetic.txt):
    python3 make_index.py
Then upload everything (index.txt + all folders) to your web host.
The hash changes whenever a cosmetic's png or txt changes, which tells the mod to re-download it.
"""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
lines = ["cosmocosmetics-db 1"]
for name in sorted(os.listdir(HERE)):
    d = os.path.join(HERE, name)
    png, txt = os.path.join(d, "cosmetic.png"), os.path.join(d, "cosmetic.txt")
    if not (os.path.isdir(d) and os.path.exists(png) and os.path.exists(txt)):
        continue
    if not FOLDER.match(name):
        print(f"skipping '{name}': folder names must be lowercase letters, digits, . _ -")
        continue
    h = hashlib.sha256()
    for p in (png, txt):
        with open(p, "rb") as f:
            h.update(f.read())
    lines.append(f"{name}={h.hexdigest()[:12]}")
with open(os.path.join(HERE, "index.txt"), "w", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
