# Progress

Progress compared with the [timeline](01_timeline.md).

**Last updated:** 18-11-2026

## Done

- [x] Tooling: uv project, exported `requirements.txt`, Makefile with uv and pip rules,
  `.flake8`, `.gitignore` (M1) — 17-11-2026
- [x] Baseline timeline — 17-11-2026
- [x] `pac-man.py` entry point, config loader, default `config.json` (M2) — 18-11-2026
  - Tested by hand:
    - wrong argument count, missing file, folder, invalid JSON, top level not an object, not
      UTF-8;
    - `#` and `//` comments;
    - wrong types, out-of-range values, missing and unknown keys, fewer than 10 levels.

    Every case gave a clear message, with no traceback.

## To do

- [ ] Maze adapter (M3)
- [ ] Highscore store (M4)
- [ ] Game logic: player, pacgums, collisions, scoring, lives, timer, levels (M5)
- [ ] Screens: main menu, instructions, highscores, game + HUD, pause, game over, victory (M6)
- [ ] Ghost AI and cheat mode (M7)
- [ ] Original sprites and game title
- [ ] Packaging and itch.io upload (M8)
- [ ] README and final test pass (M9)
