.RECIPEPREFIX := >

PYTHON ?= .venv_forprint_library/bin/python
PIP := $(PYTHON) -m pip

BLUEPRINT_ROOT ?= /srv/software_development/forprint-project/forprint_system_blueprint
MODULE_ID := forprint_library

ACTIVE_BLUEPRINT_PROMPT ?= $(BLUEPRINT_ROOT)/coordination/outgoing_prompts/forprint_library/approved/2026-06-23__library__make_first_semantic_reference_readiness_v0_1.md
LOCAL_ACTIVE_PROMPT_DIR := coordination/prompts/active
LOCAL_ACTIVE_PROMPT := $(LOCAL_ACTIVE_PROMPT_DIR)/$(notdir $(ACTIVE_BLUEPRINT_PROMPT))

BLUEPRINT_STANDARDS_DIR := $(BLUEPRINT_ROOT)/coordination/standards
LOCAL_STANDARDS_DIR := coordination/standards
LOCAL_STANDARDS_SNAPSHOT := $(LOCAL_STANDARDS_DIR)/blueprint_standards_available_snapshot.txt

BLUEPRINT_OUTGOING_PROMPTS_DIR := $(BLUEPRINT_ROOT)/coordination/outgoing_prompts/forprint_library
BLUEPRINT_MODULE_POLICY := $(BLUEPRINT_ROOT)/coordination/module_policy/forprint_library/module_policy.md
BLUEPRINT_COORDINATION_CHECKER := $(BLUEPRINT_ROOT)/scripts/check_coordination_metadata.py
BLUEPRINT_COORDINATION_FIXER := $(BLUEPRINT_ROOT)/scripts/fix_coordination_metadata.py
BLUEPRINT_PYTHON := $(BLUEPRINT_ROOT)/.venv_blueprint/bin/python

.PHONY: install run lint lint-fix format test check check-report clean dictionary-preview status-report blueprint-pull blueprint-check blueprint-sync-directives blueprint-instruction-list blueprint-instruction-check blueprint-instruction-sync blueprint-instruction blueprint-standards-list blueprint-standards-check blueprint-standards-sync blueprint-standards blueprint-prompts-list blueprint-prompts-check blueprint-prompts-sync blueprint-prompts prompt-read blueprint-sync coordination-check coordination-fix module-policy-check governance-check module-start module-sync module-validate module-finish report-clean completion-packet-validate completion-packet-apply completion-packet-check

install:
>$(PIP) install -e ".[dev]"

run:
>PYTHONPATH=app $(PYTHON) -m uvicorn forprint_library.api.main:app --host 127.0.0.1 --port 8010 --reload

lint:
>PYTHONPATH=app $(PYTHON) -m ruff check app scripts tests

lint-fix:
>PYTHONPATH=app $(PYTHON) -m ruff check app scripts tests --fix

format:
>PYTHONPATH=app $(PYTHON) -m ruff format app scripts tests

test:
>PYTHONPATH=app $(PYTHON) -m pytest

check:
>$(MAKE) lint-fix
>$(MAKE) lint
>$(MAKE) test
>$(MAKE) check-report

check-report:
>PYTHONPATH=app $(PYTHON) scripts/run_library_checks.py

clean: report-clean

dictionary-preview:
>PYTHONPATH=app $(PYTHON) scripts/preview_shared_operational_dictionaries.py

status-report:
>$(MAKE) check-report

blueprint-pull:
>git -C $(BLUEPRINT_ROOT) pull --ff-only

blueprint-check:
>PYTHONPATH=app $(PYTHON) scripts/check_blueprint_instructions.py

blueprint-sync-directives:
>PYTHONPATH=app $(PYTHON) scripts/sync_blueprint_directives.py

blueprint-instruction-list:
>@echo "== Blueprint instruction list for $(MODULE_ID) =="
>@echo "Blueprint root: $(BLUEPRINT_ROOT)"
>@echo "Active prompt: $(ACTIVE_BLUEPRINT_PROMPT)"
>@if [ -d "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" ]; then find "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" -type f -name "*.md" | sort; else echo "WARN: no outgoing prompt directory for $(MODULE_ID)"; fi

blueprint-instruction-check:
>@echo "== Blueprint instruction check for $(MODULE_ID) =="
>@[ -d "$(BLUEPRINT_ROOT)" ] && echo "OK: Blueprint root is readable: $(BLUEPRINT_ROOT)" || { echo "FAILED: Blueprint root is missing: $(BLUEPRINT_ROOT)"; exit 1; }
>@[ -r "$(ACTIVE_BLUEPRINT_PROMPT)" ] && echo "OK: active Blueprint prompt is readable: $(ACTIVE_BLUEPRINT_PROMPT)" || { echo "FAILED: active Blueprint prompt is missing or unreadable: $(ACTIVE_BLUEPRINT_PROMPT)"; exit 1; }
>@[ -s "$(ACTIVE_BLUEPRINT_PROMPT)" ] && echo "OK: active Blueprint prompt is not empty" || { echo "FAILED: active Blueprint prompt is empty"; exit 1; }
>@grep -Eiq "library|semantic|reference|readiness|canonical" "$(ACTIVE_BLUEPRINT_PROMPT)" && echo "OK: active Blueprint prompt appears relevant to Library semantic/reference readiness" || echo "WARN: active prompt is readable, but expected semantic/readiness keywords were not detected"

blueprint-instruction-sync: blueprint-instruction-check
>@echo "== Blueprint instruction sync for $(MODULE_ID) =="
>@mkdir -p "$(LOCAL_ACTIVE_PROMPT_DIR)"
>@cp "$(ACTIVE_BLUEPRINT_PROMPT)" "$(LOCAL_ACTIVE_PROMPT)"
>@echo "OK: synced active prompt to $(LOCAL_ACTIVE_PROMPT)"

blueprint-instruction: blueprint-instruction-list blueprint-instruction-check blueprint-instruction-sync

blueprint-standards-list:
>@echo "== Blueprint standards list =="
>@[ -d "$(BLUEPRINT_STANDARDS_DIR)" ] && find "$(BLUEPRINT_STANDARDS_DIR)" -type f | sort || { echo "FAILED: Blueprint standards directory is missing: $(BLUEPRINT_STANDARDS_DIR)"; exit 1; }

blueprint-standards-check:
>@echo "== Blueprint standards check =="
>@[ -d "$(BLUEPRINT_STANDARDS_DIR)" ] && echo "OK: Blueprint standards directory is readable: $(BLUEPRINT_STANDARDS_DIR)" || { echo "FAILED: Blueprint standards directory is missing: $(BLUEPRINT_STANDARDS_DIR)"; exit 1; }
>@[ "$$(find "$(BLUEPRINT_STANDARDS_DIR)" -type f | wc -l)" -gt 0 ] && echo "OK: Blueprint standards files are available" || { echo "FAILED: Blueprint standards directory has no files"; exit 1; }

blueprint-standards-sync: blueprint-standards-check
>@echo "== Blueprint standards sync =="
>@mkdir -p "$(LOCAL_STANDARDS_DIR)"
>@printf '%s\n' "module_id: $(MODULE_ID)" > "$(LOCAL_STANDARDS_SNAPSHOT)"
>@printf '%s\n' "snapshot_type: blueprint_standards_available_snapshot" >> "$(LOCAL_STANDARDS_SNAPSHOT)"
>@printf '%s\n' "blueprint_root: $(BLUEPRINT_ROOT)" >> "$(LOCAL_STANDARDS_SNAPSHOT)"
>@printf '%s\n' "standards_files:" >> "$(LOCAL_STANDARDS_SNAPSHOT)"
>@find "$(BLUEPRINT_STANDARDS_DIR)" -type f | sort | sed 's#^#  - #' >> "$(LOCAL_STANDARDS_SNAPSHOT)"
>@echo "OK: wrote $(LOCAL_STANDARDS_SNAPSHOT)"

blueprint-standards: blueprint-standards-list blueprint-standards-check blueprint-standards-sync

blueprint-prompts-list:
>@echo "== Blueprint prompts list for $(MODULE_ID) =="
>@if [ -d "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" ]; then find "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" -type f -name "*.md" | sort; else echo "WARN: no outgoing prompt directory for $(MODULE_ID)"; fi

blueprint-prompts-check: blueprint-instruction-check

blueprint-prompts-sync: blueprint-instruction-sync

blueprint-prompts: blueprint-prompts-list blueprint-prompts-check blueprint-prompts-sync

prompt-read: blueprint-instruction-check
>@echo "== Active Blueprint prompt for $(MODULE_ID) =="
>@echo "Path: $(ACTIVE_BLUEPRINT_PROMPT)"
>@echo
>@sed -n '1,260p' "$(ACTIVE_BLUEPRINT_PROMPT)"

blueprint-sync: blueprint-pull blueprint-instruction blueprint-standards blueprint-prompts blueprint-sync-directives coordination-check

coordination-check:
>@if [ -x "$(BLUEPRINT_PYTHON)" ] && [ -f "$(BLUEPRINT_COORDINATION_CHECKER)" ]; then "$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_COORDINATION_CHECKER)" --module-root .; else echo "WARN: Blueprint coordination metadata checker is not available yet."; fi

coordination-fix:
>@if [ -x "$(BLUEPRINT_PYTHON)" ] && [ -f "$(BLUEPRINT_COORDINATION_FIXER)" ]; then "$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_COORDINATION_FIXER)" --module-root .; else echo "WARN: Blueprint coordination metadata fixer is not available yet."; fi

module-policy-check:
>@[ -r "$(BLUEPRINT_MODULE_POLICY)" ] && echo "OK: Blueprint module policy is readable." || { echo "FAILED: Blueprint module policy is missing or unreadable."; exit 1; }

governance-check:
>@echo "== ForPrint Library governance check =="
>$(MAKE) blueprint-pull
>$(MAKE) blueprint-check
>$(MAKE) blueprint-sync-directives
>$(MAKE) module-policy-check
>$(MAKE) coordination-check
>$(MAKE) status-report

module-start: blueprint-sync module-policy-check coordination-check prompt-read

module-sync: blueprint-sync coordination-fix coordination-check

module-validate: check-report check governance-check report-clean status-report

module-finish: module-validate completion-packet-check

report-clean:
>@echo "== Report clean =="
>@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
>@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name ".pytest_cache" -prune -exec rm -rf {} +
>@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name ".ruff_cache" -prune -exec rm -rf {} +
>@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name "*.egg-info" -prune -exec rm -rf {} +
>@echo "OK: report clean completed"

completion-packet-validate:
>@echo "== Completion packet validate =="
>@if [ -d "coordination/completion_packet" ] || [ -d "coordination/completion_packets" ]; then echo "OK: completion packet directory exists"; else echo "DEFERRED: completion packet automation is not configured in Library yet."; echo "Missing: coordination/completion_packet or coordination/completion_packets"; fi

completion-packet-apply:
>@echo "== Completion packet apply =="
>@if [ -d "coordination/completion_packet" ] || [ -d "coordination/completion_packets" ]; then echo "DEFERRED: apply logic requires an approved Blueprint completion packet contract."; echo "No files were changed."; else echo "DEFERRED: no completion packet automation exists, nothing to apply."; echo "No files were changed."; fi

completion-packet-check: completion-packet-validate completion-packet-apply
>@echo "OK: completion packet check completed with current deferred-safe behavior"