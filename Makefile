UV				?= uv
UV_PROJECT_ENV	:= .venv
CACHE_DIR		:= .cache
UV_CACHE_DIR	:= $(CACHE_DIR)/uv
UV_ENV			:= UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_PROJECT_ENV)

ARGS			?= config.json

.PHONY: install run debug lint lint-strict clean fclean

install:
	$(UV_ENV) $(UV) sync

run:
	$(UV_ENV) $(UV) run python -B pac-man.py $(ARGS)

debug:
	$(UV_ENV) $(UV) run python -B -m pdb pac-man.py $(ARGS)

lint: clean
	$(UV_ENV) $(UV) run flake8 .
	$(UV_ENV) $(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: clean
	$(UV_ENV) $(UV) run flake8 .
	$(UV_ENV) $(UV) run mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build

fclean: clean
	rm -rf $(UV_PROJECT_ENV)
	rm -rf $(CACHE_DIR)
	rm -rf dist
