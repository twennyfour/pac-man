UV_VENV			:= .venv
UV				?= uv
CACHE_DIR		:= .cache
UV_CACHE_DIR	:= $(CACHE_DIR)/uv
UV_ENV			:= UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_VENV)


PIP_VENV			:= .pip_venv
VENV_PY			:= $(PIP_VENV)/bin/python
VENV_PIP		:= $(PIP_VENV)/bin/pip
REQ_FILE		:= requirements.txt

ARGS			?= config.json

.PHONY: install run debug lint lint-strict uv-install uv-run uv-debug uv-lint uv-lint-strict py-install py-run py-debug py-lint py-lint-strict clean fclean

run: uv-run
install: uv-install
debug: uv-debug
lint: uv-lint
lint-strict: uv-lint-strict

uv-install:
	$(UV_ENV) $(UV) sync

uv-run:
	$(UV_ENV) $(UV) run python -B pac-man.py $(ARGS)

uv-debug:
	$(UV_ENV) $(UV) run python -B -m pdb pac-man.py $(ARGS)

uv-lint: clean
	$(UV_ENV) $(UV) run flake8 .
	$(UV_ENV) $(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

uv-lint-strict: clean
	$(UV_ENV) $(UV) run flake8 .
	$(UV_ENV) $(UV) run mypy . --strict

py-install: $(PIP_VENV)/.installed

$(PIP_VENV)/.installed: $(REQ_FILE)
	python3 -m venv $(PIP_VENV)
	$(VENV_PIP) install -r $(REQ_FILE)
	touch $@

py-run: py-install
	$(VENV_PY) -B pac-man.py $(ARGS)

py-debug: py-install
	$(VENV_PY) -B -m pdb pac-man.py $(ARGS)

py-lint: clean py-install
	$(VENV_PY) -B -m flake8 .
	$(VENV_PY) -B -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

py-lint-strict: clean py-install
	$(VENV_PY) -B -m flake8 .
	$(VENV_PY) -B -m mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(UV_VENV)
	rm -rf $(PIP_VENV)
	rm -rf $(CACHE_DIR)
	rm -rf build
	rm -rf dist
