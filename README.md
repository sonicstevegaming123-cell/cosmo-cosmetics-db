# CosmoCosmetics online database

The mod downloads cosmetics from a website you host. They are saved on the player's computer, so they
keep working offline. The mod re-checks the index on startup, every 5 minutes, and whenever the Global
Cosmetics menu is opened (or "Check updates" is pressed): new cosmetics are installed, changed ones are
updated, and ones removed from the index are deleted.

## Layout on your web host

    index.txt                  <- generated, see below
    gold-crown/
        cosmetic.png
        cosmetic.txt
    shiny-crown/
        cosmetic.png
        cosmetic.txt

* Folder names: lowercase letters, digits, `.` `_` `-` only (max 64 characters).
* `cosmetic.png`: 64x64 or larger, square. Animated: frames stacked vertically (64x128 = 2 frames).
  Fully transparent pixels let the skin show through; the color `#ff00d4` makes a pixel completely invisible.
* `cosmetic.txt`: `key=value` lines (`#` starts a comment):

      name=Shiny Crown      display name (max 24 chars; defaults to the folder name)
      animated=true         true or false
      frames=3              number of stacked frames (animated only, 2-64)
      fps=6                 animation speed in frames per second (1-60)
      delay=1.5             seconds of rest between loops (0-30)

* `index.txt`: first line `cosmocosmetics-db 1`, then one `folder=hash` line per cosmetic.
  Don't write it by hand: run `python3 make_index.py` after every change. The hash changes when the png or
  txt changes, which is how the mod knows to re-download.

## Hosting (free option: GitHub)

1. Create a public GitHub repository and upload `index.txt` and all cosmetic folders to it.
2. The base URL is `https://raw.githubusercontent.com/<you>/<repo>/main/` (must be https and end with `/`).
3. Put that URL in `DEFAULT_URL` in `DatabaseSync.java` before building (so every player gets it), or in
   `config/cosmocosmetics/database.txt` as `url=...` for testing.

Any static web host works (GitHub Pages, Netlify, your own server). Caches can delay updates by a few minutes.

## What the mod does with it

* Downloaded cosmetics appear as Global Cosmetics (tag "Default"), off by default on every skin.
* Players can turn them on per skin, or use "Use on all" / "Disable all". They can't edit or delete them.
* If a download fails or the site is down, the saved cosmetics are kept. Nothing is removed unless the index
  loaded correctly and no longer lists a cosmetic.
