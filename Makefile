PYTHON ?= .venv_forprint_library/bin/python
PIP := $(PYTHON) -m pip
BLUEPRINT_ROOT ?= /srv/software_development/forprint-project/forprint_system_blueprint

.PHONY: install run lint lint-fix test check check-report 
		blueprint-pull blueprint-check blueprint-sync-directives 
		coordination-check coordination-fix module-policy-check format clean
		dictionary-preview status-report governance-check

install:
	$(PIP) install -e ".[dev]"

run:
	PYTHONPATH=app $(PYTHON) -m uvicorn forprint_library.api.main:app --host 127.0.0.1 --port 8010 --reload

lint:
	PYTHONPATH=app $(PYTHON) -m ruff check app scripts tests

lint-fix:
	PYTHONPATH=app $(PYTHON) -m ruff check app scripts tests --fix

format:
	PYTHONPATH=app $(PYTHON) -m ruff format app scripts tests

test:
	PYTHONPATH=app $(PYTHON) -m pytest

check:
	$(MAKE) lint-fix
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) check-report

check-report:
	PYTHONPATH=app $(PYTHON) scripts/run_library_checks.py

blueprint-pull:
	git -C $(BLUEPRINT_ROOT) pull --ff-only

blueprint-check:
	PYTHONPATH=app $(PYTHON) scripts/check_blueprint_instructions.py

blueprint-sync-directives:
	PYTHONPATH=app $(PYTHON) scripts/sync_blueprint_directives.py

coordination-check:
	@if [ -x "$(BLUEPRINT_ROOT)/.venv_blueprint/bin/python" ] && [ -f "$(BLUEPRINT_ROOT)/scripts/check_coordination_metadata.py" ]; then \
		$(BLUEPRINT_ROOT)/.venv_blueprint/bin/python \
			$(BLUEPRINT_ROOT)/scripts/check_coordination_metadata.py \
			--module-root . ; \
	else \
		echo "WARN: Blueprint coordination metadata checker is not available yet."; \
	fi

coordination-fix:
	@if [ -x "$(BLUEPRINT_ROOT)/.venv_blueprint/bin/python" ] && [ -f "$(BLUEPRINT_ROOT)/scripts/fix_coordination_metadata.py" ]; then \
		$(BLUEPRINT_ROOT)/.venv_blueprint/bin/python \
			$(BLUEPRINT_ROOT)/scripts/fix_coordination_metadata.py \
			--module-root . ; \
	else \
		echo "WARN: Blueprint coordination metadata fixer is not available yet."; \
	fi

module-policy-check:
	@test -r "$(BLUEPRINT_ROOT)/coordination/module_policy/forprint_library/module_policy.md" \
		&& echo "OK: Blueprint module policy is readable." \
		|| (echo "FAILED: Blueprint module policy is missing or unreadable."; exit 1)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +

dictionary-preview:
	PYTHONPATH=app $(PYTHON) scripts/preview_shared_operational_dictionaries.py

status-report:
	$(MAKE) check-report

governance-check:
	@echo "== ForPrint Library governance check =="
	$(MAKE) blueprint-pull
	$(MAKE) blueprint-check
	$(MAKE) blueprint-sync-directives
	$(MAKE) module-policy-check
	$(MAKE) coordination-check
	$(MAKE) status-report
