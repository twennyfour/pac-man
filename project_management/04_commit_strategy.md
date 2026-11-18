# Commit strategy

- **One logical change per commit**, made once it works and `make lint` passes.
- **Messages:** short, imperative and capitalized, with no prefix (e.g. `Add .gitignore`).
- **Project management files** are updated in the same commit as the work they describe, so
  the git history doubles as evidence.
- **Generated files** (`uv.lock`, `requirements.txt`) are committed together with the
  `pyproject.toml` change that produced them.
