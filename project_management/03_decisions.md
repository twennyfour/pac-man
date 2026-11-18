# Technical decisions

Choices that shape the code, oldest first.

## D1. uv, with pip as a fallback (17-11-2026)

uv manages dependencies (`pyproject.toml` + committed `uv.lock`). `requirements.txt` is
exported from the lockfile. \
**Why:** exact versions everywhere, and the local maze wheel installs as-is.

## D2. pygame-ce for graphics (17-11-2026)

Only calls with an MLX equivalent: window, images, blit, pixels, text, events, clock. No
audio. \
**Why:** TODO.

## D3. PyInstaller one-folder build (17-11-2026)

`pac-man.spec` at the root. The zipped `dist/` folder goes on itch.io as a Linux download. \
**Why:** it keeps a normal game loop, real files and the one-argument launch.

## D4. Maze package behind one adapter (17-11-2026)

The assigned wheel is committed unmodified, and one module imports it and handles its quirks. \
**Why:** it is reinstalled at review, and our code must adapt to its interface.

## D5. Config: fatal file errors, forgiving values (18-11-2026)

- A missing or unreadable file, or invalid JSON, gives a clear error and exit status 1.
- A bad value falls back to its default; an out-of-range value is clamped. Unknown keys are
  ignored.
- Fewer than 10 levels are completed with default levels.

**Why:** subject, and the config is edited live at the defense.

## Pending

- [ ] Game title
- [ ] Highscore storage (JSON or SQLite)
- [ ] What happens when the level timer runs out
- [ ] Movement model (smooth or cell by cell)
- [ ] Ghost chase strategy
- [ ] Meaning of `pacgum`: a count per level, or "most corridors"
