# ForPrint Library Makefile
#
# Purpose:
#   Standard operator command surface for ForPrint Library.
#
# Rules:
#   - Use standard Make recipe TAB indentation.
#   - Prefer Blueprint Make tooling over raw script calls where available.
#   - Keep Prompt Queue and Coordination Document Awareness visible during module start.
#   - Keep generated bundle/report writes explicit through *-write targets.

.DEFAULT_GOAL := help

# =============================================================================
# 00 Environment / constants START
# =============================================================================

# Purpose: define local Python runtime.
# Result: all local module commands use the project venv by default.
PYTHON ?= .venv_forprint_library/bin/python
PIP ?= $(PYTHON) -m pip

# Purpose: define Blueprint repository/runtime paths.
# Result: module can call Blueprint governance, prompt queue and awareness tools.
BLUEPRINT_ROOT ?= /srv/software_development/forprint-project/forprint_system_blueprint
BLUEPRINT_PYTHON ?= $(BLUEPRINT_ROOT)/.venv_blueprint/bin/python

# Purpose: define this module id.
# Result: Blueprint tools can filter module-specific prompts, policy and awareness docs.
MODULE_ID := forprint_library

# Purpose: define default awareness/bundle output controls.
# Result: operator can override scope/limit without editing the Makefile.
SCOPE ?= bootstrap
LIMIT ?= 40

# Purpose: define Blueprint standards paths.
# Result: standards list/snapshot targets can read Blueprint standards.
BLUEPRINT_STANDARDS_DIR := $(BLUEPRINT_ROOT)/coordination/standards
LOCAL_STANDARDS_DIR := coordination/standards
LOCAL_STANDARDS_SNAPSHOT := $(LOCAL_STANDARDS_DIR)/blueprint_standards_available_snapshot.txt

# Purpose: define Blueprint prompt and module policy paths.
# Result: prompt and governance targets use module-specific Blueprint sources.
BLUEPRINT_OUTGOING_PROMPTS_DIR := $(BLUEPRINT_ROOT)/coordination/outgoing_prompts/$(MODULE_ID)
BLUEPRINT_MODULE_POLICY := $(BLUEPRINT_ROOT)/coordination/module_policy/$(MODULE_ID)/module_policy.md

# Purpose: keep a legacy/static active prompt fallback during transition.
# Result: old prompt-read workflows still have a safe fallback, but Prompt Queue is preferred.
ACTIVE_BLUEPRINT_PROMPT ?= $(BLUEPRINT_OUTGOING_PROMPTS_DIR)/approved/2026-06-29__library__reference_contract_foundation_v0_2.md
LOCAL_ACTIVE_PROMPT_DIR := coordination/prompts/active
LOCAL_ACTIVE_PROMPT := $(LOCAL_ACTIVE_PROMPT_DIR)/$(notdir $(ACTIVE_BLUEPRINT_PROMPT))

# Purpose: define Blueprint coordination metadata scripts.
# Result: local coordination metadata can be checked/fixed through Blueprint tools.
BLUEPRINT_COORDINATION_CHECKER := $(BLUEPRINT_ROOT)/scripts/check_coordination_metadata.py
BLUEPRINT_COORDINATION_FIXER := $(BLUEPRINT_ROOT)/scripts/fix_coordination_metadata.py

# Purpose: define Blueprint Prompt Queue scripts.
# Result: module can discover and read the next prompt without hardcoded prompt paths.
BLUEPRINT_PROMPT_QUEUE_VALIDATOR := $(BLUEPRINT_ROOT)/scripts/coordination/validate_prompt_queue.py
BLUEPRINT_PROMPT_DASHBOARD_RENDERER := $(BLUEPRINT_ROOT)/scripts/coordination/render_prompt_dashboard.py
BLUEPRINT_NEXT_PROMPT_RESOLVER := $(BLUEPRINT_ROOT)/scripts/coordination/resolve_next_prompt.py

# Purpose: define Blueprint Coordination Document Awareness scripts.
# Result: module can see new/changed Blueprint documents and build context bundles.
BLUEPRINT_DOCUMENT_MANIFEST_BUILDER := $(BLUEPRINT_ROOT)/scripts/coordination/build_document_manifest.py
BLUEPRINT_DOCUMENT_AWARENESS_DASHBOARD := $(BLUEPRINT_ROOT)/scripts/coordination/render_document_awareness_dashboard.py
BLUEPRINT_CONTEXT_BUNDLE_BUILDER := $(BLUEPRINT_ROOT)/scripts/coordination/build_context_bundle.py

# Purpose: define module-local awareness ledger path.
# Result: this module owns its own review/adoption status for Blueprint documents.
MODULE_DOCUMENT_AWARENESS_LEDGER := $(CURDIR)/coordination/blueprint_awareness/document_review_ledger.yaml

# =============================================================================
# 00 Environment / constants FINISH
# =============================================================================


# =============================================================================
# 01 Help / navigation START
# =============================================================================

# Purpose: list public Make targets.
# Result: operator can quickly discover the standard command surface.
.PHONY: help
help:
	@echo "ForPrint Library Make targets"
	@echo ""
	@echo "Core:"
	@echo "  make install"
	@echo "  make run"
	@echo "  make lint"
	@echo "  make lint-fix"
	@echo "  make format"
	@echo "  make test"
	@echo "  make check"
	@echo "  make check-report"
	@echo "  make clean"
	@echo ""
	@echo "Blueprint sync:"
	@echo "  make blueprint-pull"
	@echo "  make blueprint-check"
	@echo "  make blueprint-sync-directives"
	@echo "  make blueprint-instruction"
	@echo "  make blueprint-standards"
	@echo "  make blueprint-prompts"
	@echo "  make blueprint-sync"
	@echo ""
	@echo "Prompt Queue:"
	@echo "  make prompt-queue-validate"
	@echo "  make prompt-dashboard NO_COLOR=1"
	@echo "  make prompt-next"
	@echo "  make prompt-read-next"
	@echo ""
	@echo "Coordination document awareness:"
	@echo "  make document-manifest"
	@echo "  make document-awareness NO_COLOR=1 LIMIT=20"
	@echo "  make context-bundle SCOPE=bootstrap LIMIT=10"
	@echo "  make context-bundle-print SCOPE=bootstrap LIMIT=10"
	@echo "  make context-bundle-write SCOPE=bootstrap LIMIT=10"
	@echo ""
	@echo "Governance / workflow:"
	@echo "  make coordination-check"
	@echo "  make coordination-fix"
	@echo "  make module-policy-check"
	@echo "  make governance-check"
	@echo "  make module-start"
	@echo "  make module-sync"
	@echo "  make module-validate"
	@echo "  make module-finish"

# =============================================================================
# 01 Help / navigation FINISH
# =============================================================================


# =============================================================================
# 02 Install / bootstrap START
# =============================================================================

# Purpose: install module development dependencies.
# Result: editable local package and dev dependencies are installed.
.PHONY: install
install:
	$(PIP) install -e ".[dev]"

# =============================================================================
# 02 Install / bootstrap FINISH
# =============================================================================


# =============================================================================
# 03 Project lifecycle START
# =============================================================================

# Purpose: run the local API service for development.
# Result: uvicorn starts ForPrint Library API on localhost.
.PHONY: run
run:
	PYTHONPATH=app $(PYTHON) -m uvicorn forprint_library.api.main:app --host 127.0.0.1 --port 8010 --reload

# =============================================================================
# 03 Project lifecycle FINISH
# =============================================================================


# =============================================================================
# 06 Syntax / formatting / lint START
# =============================================================================

# Purpose: run ruff checks without modifying files.
# Result: returns non-zero if lint issues are found.
.PHONY: lint
lint:
	PYTHONPATH=app $(PYTHON) -m ruff check app scripts tests

# Purpose: run safe automatic ruff fixes.
# Result: fixable lint issues are corrected.
.PHONY: lint-fix
lint-fix:
	PYTHONPATH=app $(PYTHON) -m ruff check app scripts tests --fix

# Purpose: format Python files with ruff formatter.
# Result: app, scripts and tests are formatted.
.PHONY: format
format:
	PYTHONPATH=app $(PYTHON) -m ruff format app scripts tests

# =============================================================================
# 06 Syntax / formatting / lint FINISH
# =============================================================================


# =============================================================================
# 07 Tests START
# =============================================================================

# Purpose: run the full Library test suite.
# Result: all tests pass or pytest returns non-zero.
.PHONY: test
test:
	PYTHONPATH=app $(PYTHON) -m pytest

# =============================================================================
# 07 Tests FINISH
# =============================================================================


# =============================================================================
# 08 Validation / check reports START
# =============================================================================

# Purpose: run the main local validation sequence before commit.
# Result: lint, tests, check report and Blueprint awareness smoke checks pass.
.PHONY: check
check:
	$(MAKE) lint-fix
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) check-report
	$(MAKE) prompt-queue-validate
	$(MAKE) document-manifest
	$(MAKE) context-bundle

# Purpose: run Library-specific validation report.
# Result: human/machine check reports are generated by Library check runner.
.PHONY: check-report
check-report:
	PYTHONPATH=app $(PYTHON) scripts/run_library_checks.py

# =============================================================================
# 08 Validation / check reports FINISH
# =============================================================================


# =============================================================================
# 09 Status / generated reports / cleanup START
# =============================================================================

# Purpose: clean generated runtime/cache artifacts.
# Result: caches and temporary generated Python metadata are removed.
.PHONY: clean
clean: report-clean

# Purpose: show current module status through the Library check report.
# Result: concise validation/status report is printed.
.PHONY: status-report
status-report:
	$(MAKE) check-report

# Purpose: remove local generated/cache files without touching source coordination reports.
# Result: working tree remains reviewable after checks.
.PHONY: report-clean
report-clean:
	@echo "== Report clean =="
	@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	@find . -path "./.git" -prune -o -path "./.venv_forprint_library" -prune -o -type d -name "*.egg-info" -prune -exec rm -rf {} +
	@echo "OK: report clean completed"

# =============================================================================
# 09 Status / generated reports / cleanup FINISH
# =============================================================================


# =============================================================================
# 10 Blueprint integration START
# =============================================================================

# Purpose: update local Blueprint repository.
# Result: Blueprint is pulled using ff-only.
.PHONY: blueprint-pull
blueprint-pull:
	git -C $(BLUEPRINT_ROOT) pull --ff-only

# Purpose: run Library-specific Blueprint instruction compatibility check.
# Result: local script confirms required Blueprint instruction sources are readable.
.PHONY: blueprint-check
blueprint-check:
	PYTHONPATH=app $(PYTHON) scripts/check_blueprint_instructions.py

# Purpose: import active Blueprint directives into Library coordination.
# Result: local directive sync runs according to Library script logic.
.PHONY: blueprint-sync-directives
blueprint-sync-directives:
	PYTHONPATH=app $(PYTHON) scripts/sync_blueprint_directives.py

# Purpose: run all Blueprint synchronization needed before module work starts.
# Result: Blueprint repo, instruction intake, standards, prompts and awareness manifest are refreshed/checked.
.PHONY: blueprint-sync
blueprint-sync:
	$(MAKE) blueprint-pull
	$(MAKE) blueprint-check
	$(MAKE) blueprint-instruction
	$(MAKE) blueprint-standards
	$(MAKE) blueprint-prompts
	$(MAKE) blueprint-sync-directives
	$(MAKE) coordination-check
	$(MAKE) document-manifest

# =============================================================================
# 10 Blueprint integration FINISH
# =============================================================================


# =============================================================================
# 11 Blueprint instruction intake START
# =============================================================================

# Purpose: list Blueprint instruction/prompt sources relevant to Library.
# Result: operator can inspect available Blueprint prompt files.
.PHONY: blueprint-instruction-list
blueprint-instruction-list:
	@echo "== Blueprint instruction list for $(MODULE_ID) =="
	@echo "Blueprint root: $(BLUEPRINT_ROOT)"
	@echo "Legacy active prompt fallback: $(ACTIVE_BLUEPRINT_PROMPT)"
	@if [ -d "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" ]; then find "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" -type f -name "*.md" | sort; else echo "WARN: no outgoing prompt directory for $(MODULE_ID)"; fi

# Purpose: verify Blueprint prompt queue and legacy prompt fallback readability.
# Result: prompt queue index is required; legacy fallback prompt is advisory.
.PHONY: blueprint-instruction-check
blueprint-instruction-check:
	@echo "== Blueprint instruction check for $(MODULE_ID) =="
	@[ -d "$(BLUEPRINT_ROOT)" ] && echo "OK: Blueprint root is readable: $(BLUEPRINT_ROOT)" || { echo "FAILED: Blueprint root is missing: $(BLUEPRINT_ROOT)"; exit 1; }
	@[ -r "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)/index.yaml" ] && echo "OK: Blueprint prompt queue index is readable." || { echo "FAILED: Blueprint prompt queue index is missing or unreadable."; exit 1; }
	@[ -r "$(ACTIVE_BLUEPRINT_PROMPT)" ] && echo "OK: legacy active Blueprint prompt fallback is readable." || echo "WARN: legacy active Blueprint prompt fallback is missing; prompt-read-next remains preferred."

# Purpose: sync legacy/static fallback prompt into local coordination.
# Result: local fallback prompt is copied if available.
.PHONY: blueprint-instruction-sync
blueprint-instruction-sync: blueprint-instruction-check
	@echo "== Blueprint instruction sync for $(MODULE_ID) =="
	@mkdir -p "$(LOCAL_ACTIVE_PROMPT_DIR)"
	@if [ -r "$(ACTIVE_BLUEPRINT_PROMPT)" ]; then cp "$(ACTIVE_BLUEPRINT_PROMPT)" "$(LOCAL_ACTIVE_PROMPT)"; echo "OK: synced legacy active prompt fallback to $(LOCAL_ACTIVE_PROMPT)"; else echo "WARN: legacy active prompt fallback was not synced."; fi

# Purpose: run complete Blueprint instruction intake workflow.
# Result: instruction sources are listed, checked and synced.
.PHONY: blueprint-instruction
blueprint-instruction: blueprint-instruction-list blueprint-instruction-check blueprint-instruction-sync

# =============================================================================
# 11 Blueprint instruction intake FINISH
# =============================================================================


# =============================================================================
# 12 Blueprint standards START
# =============================================================================

# Purpose: list Blueprint standard files.
# Result: operator can inspect available Blueprint standards.
.PHONY: blueprint-standards-list
blueprint-standards-list:
	@echo "== Blueprint standards list =="
	@[ -d "$(BLUEPRINT_STANDARDS_DIR)" ] && find "$(BLUEPRINT_STANDARDS_DIR)" -type f | sort || { echo "FAILED: Blueprint standards directory is missing: $(BLUEPRINT_STANDARDS_DIR)"; exit 1; }

# Purpose: verify Blueprint standards are readable.
# Result: standards directory exists and contains files.
.PHONY: blueprint-standards-check
blueprint-standards-check:
	@echo "== Blueprint standards check =="
	@[ -d "$(BLUEPRINT_STANDARDS_DIR)" ] && echo "OK: Blueprint standards directory is readable: $(BLUEPRINT_STANDARDS_DIR)" || { echo "FAILED: Blueprint standards directory is missing: $(BLUEPRINT_STANDARDS_DIR)"; exit 1; }
	@[ "$$(find "$(BLUEPRINT_STANDARDS_DIR)" -type f | wc -l)" -gt 0 ] && echo "OK: Blueprint standards files are available" || { echo "FAILED: Blueprint standards directory has no files"; exit 1; }

# Purpose: write local snapshot of available Blueprint standards.
# Result: coordination/standards/blueprint_standards_available_snapshot.txt is refreshed.
.PHONY: blueprint-standards-sync
blueprint-standards-sync: blueprint-standards-check
	@echo "== Blueprint standards sync =="
	@mkdir -p "$(LOCAL_STANDARDS_DIR)"
	@printf '%s\n' "module_id: $(MODULE_ID)" > "$(LOCAL_STANDARDS_SNAPSHOT)"
	@printf '%s\n' "snapshot_type: blueprint_standards_available_snapshot" >> "$(LOCAL_STANDARDS_SNAPSHOT)"
	@printf '%s\n' "blueprint_root: $(BLUEPRINT_ROOT)" >> "$(LOCAL_STANDARDS_SNAPSHOT)"
	@printf '%s\n' "standards_files:" >> "$(LOCAL_STANDARDS_SNAPSHOT)"
	@find "$(BLUEPRINT_STANDARDS_DIR)" -type f | sort | sed 's#^#  - #' >> "$(LOCAL_STANDARDS_SNAPSHOT)"
	@echo "OK: wrote $(LOCAL_STANDARDS_SNAPSHOT)"

# Purpose: run complete Blueprint standards workflow.
# Result: standards are listed, checked and local snapshot is refreshed.
.PHONY: blueprint-standards
blueprint-standards: blueprint-standards-list blueprint-standards-check blueprint-standards-sync

# =============================================================================
# 12 Blueprint standards FINISH
# =============================================================================


# =============================================================================
# 13 Blueprint outgoing prompts / Prompt Queue START
# =============================================================================

# Purpose: list Blueprint prompt files for Library.
# Result: operator can inspect prompt markdown files under module outgoing prompt directory.
.PHONY: blueprint-prompts-list
blueprint-prompts-list:
	@echo "== Blueprint prompts list for $(MODULE_ID) =="
	@if [ -d "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" ]; then find "$(BLUEPRINT_OUTGOING_PROMPTS_DIR)" -type f -name "*.md" | sort; else echo "WARN: no outgoing prompt directory for $(MODULE_ID)"; fi

# Purpose: verify Blueprint prompt sources.
# Result: prompt queue index is readable.
.PHONY: blueprint-prompts-check
blueprint-prompts-check: blueprint-instruction-check

# Purpose: sync legacy/static fallback prompt.
# Result: fallback prompt is synced if available.
.PHONY: blueprint-prompts-sync
blueprint-prompts-sync: blueprint-instruction-sync

# Purpose: run complete prompt workflow.
# Result: prompts are listed, checked, synced and Prompt Queue dashboard is shown.
.PHONY: blueprint-prompts
blueprint-prompts:
	$(MAKE) blueprint-prompts-list
	$(MAKE) blueprint-prompts-check
	$(MAKE) blueprint-prompts-sync
	$(MAKE) prompt-queue-validate
	$(MAKE) prompt-dashboard

# Purpose: legacy alias for reading the next prompt.
# Result: uses Prompt Queue v0.2 resolver instead of static prompt path.
.PHONY: prompt-read
prompt-read: prompt-read-next

# Purpose: validate Blueprint Prompt Queue indexes.
# Result: Prompt Queue v0.2 index validation passes or returns non-zero.
.PHONY: prompt-queue-validate
prompt-queue-validate:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_PROMPT_QUEUE_VALIDATOR)" --root "$(BLUEPRINT_ROOT)"

# Purpose: render Prompt Queue dashboard for Library.
# Result: operator can see prompt sequence, statuses and next prompt.
.PHONY: prompt-dashboard
prompt-dashboard:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_PROMPT_DASHBOARD_RENDERER)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)" $(if $(filter 1,$(NO_COLOR)),--no-color,)

# Purpose: resolve next ready Blueprint prompt for Library.
# Result: next prompt metadata/path is printed.
.PHONY: prompt-next
prompt-next:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_NEXT_PROMPT_RESOLVER)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)"

# Purpose: read next ready Blueprint prompt for Library.
# Result: next prompt metadata and prompt body are printed.
.PHONY: prompt-read-next
prompt-read-next:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_NEXT_PROMPT_RESOLVER)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)" --read

# =============================================================================
# 13 Blueprint outgoing prompts / Prompt Queue FINISH
# =============================================================================


# =============================================================================
# 14 Coordination document awareness START
# =============================================================================

# Purpose: build/validate Blueprint document manifest without writing reports.
# Result: manifest summary is printed; no generated manifest files are written.
.PHONY: document-manifest
document-manifest:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_DOCUMENT_MANIFEST_BUILDER)" --root "$(BLUEPRINT_ROOT)" --no-write

# Purpose: write Blueprint document manifest reports explicitly.
# Result: generated manifest reports are written under Blueprint reports directory.
.PHONY: document-manifest-write
document-manifest-write:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_DOCUMENT_MANIFEST_BUILDER)" --root "$(BLUEPRINT_ROOT)"

# Purpose: render Library coordination document awareness dashboard.
# Result: operator sees new/changed/unseen/applied Blueprint docs for Library.
.PHONY: document-awareness
document-awareness:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_DOCUMENT_AWARENESS_DASHBOARD)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)" --ledger "$(MODULE_DOCUMENT_AWARENESS_LEDGER)" --limit "$(LIMIT)" $(if $(filter 1,$(NO_COLOR)),--no-color,)

# Purpose: build Library context bundle without writing files.
# Result: bundle summary is printed; no generated bundle file is written.
.PHONY: context-bundle
context-bundle:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_CONTEXT_BUNDLE_BUILDER)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)" --ledger "$(MODULE_DOCUMENT_AWARENESS_LEDGER)" --scope "$(SCOPE)" --limit "$(LIMIT)" --no-write

# Purpose: write Library context bundle explicitly.
# Result: generated Markdown bundle is written under Blueprint reports directory.
.PHONY: context-bundle-write
context-bundle-write:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_CONTEXT_BUNDLE_BUILDER)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)" --ledger "$(MODULE_DOCUMENT_AWARENESS_LEDGER)" --scope "$(SCOPE)" --limit "$(LIMIT)"

# Purpose: print Library context bundle to stdout.
# Result: bundle content can be copied into an assistant chat.
.PHONY: context-bundle-print
context-bundle-print:
	"$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_CONTEXT_BUNDLE_BUILDER)" --root "$(BLUEPRINT_ROOT)" --module "$(MODULE_ID)" --ledger "$(MODULE_DOCUMENT_AWARENESS_LEDGER)" --scope "$(SCOPE)" --limit "$(LIMIT)" --print

# =============================================================================
# 14 Coordination document awareness FINISH
# =============================================================================


# =============================================================================
# 15 Coordination metadata / module policy / governance START
# =============================================================================

# Purpose: validate Library coordination metadata using Blueprint checker.
# Result: metadata check passes or reports warnings/errors.
.PHONY: coordination-check
coordination-check:
	@if [ -x "$(BLUEPRINT_PYTHON)" ] && [ -f "$(BLUEPRINT_COORDINATION_CHECKER)" ]; then "$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_COORDINATION_CHECKER)" --module-root .; else echo "WARN: Blueprint coordination metadata checker is not available yet."; fi

# Purpose: apply safe fixes to Library coordination metadata using Blueprint fixer.
# Result: fixable metadata issues are updated.
.PHONY: coordination-fix
coordination-fix:
	@if [ -x "$(BLUEPRINT_PYTHON)" ] && [ -f "$(BLUEPRINT_COORDINATION_FIXER)" ]; then "$(BLUEPRINT_PYTHON)" "$(BLUEPRINT_COORDINATION_FIXER)" --module-root .; else echo "WARN: Blueprint coordination metadata fixer is not available yet."; fi

# Purpose: verify Blueprint module policy for Library is readable.
# Result: module policy file exists and is readable.
.PHONY: module-policy-check
module-policy-check:
	@[ -r "$(BLUEPRINT_MODULE_POLICY)" ] && echo "OK: Blueprint module policy is readable." || { echo "FAILED: Blueprint module policy is missing or unreadable."; exit 1; }

# Purpose: run Library governance checks.
# Result: Blueprint sync, policy, prompt queue, awareness and coordination checks pass.
.PHONY: governance-check
governance-check:
	@echo "== ForPrint Library governance check =="
	$(MAKE) blueprint-pull
	$(MAKE) blueprint-check
	$(MAKE) blueprint-sync-directives
	$(MAKE) module-policy-check
	$(MAKE) prompt-queue-validate
	$(MAKE) document-manifest
	$(MAKE) document-awareness
	$(MAKE) coordination-check
	$(MAKE) status-report

# =============================================================================
# 15 Coordination metadata / module policy / governance FINISH
# =============================================================================


# =============================================================================
# 16 Completion packet / prompt finalization START
# =============================================================================

# Purpose: validate completion packet availability.
# Result: current deferred-safe behavior reports missing automation without faking implementation.
.PHONY: completion-packet-validate
completion-packet-validate:
	@echo "== Completion packet validate =="
	@if [ -d "coordination/completion_packet" ] || [ -d "coordination/completion_packets" ]; then echo "OK: completion packet directory exists"; else echo "DEFERRED: completion packet automation is not configured in Library yet."; echo "Missing: coordination/completion_packet or coordination/completion_packets"; fi

# Purpose: apply completion packet if automation exists.
# Result: current deferred-safe behavior makes no changes when automation is not configured.
.PHONY: completion-packet-apply
completion-packet-apply:
	@echo "== Completion packet apply =="
	@if [ -d "coordination/completion_packet" ] || [ -d "coordination/completion_packets" ]; then echo "DEFERRED: apply logic requires an approved Blueprint completion packet contract."; echo "No files were changed."; else echo "DEFERRED: no completion packet automation exists, nothing to apply."; echo "No files were changed."; fi

# Purpose: run completion packet validation/apply sequence.
# Result: deferred-safe completion packet check completes.
.PHONY: completion-packet-check
completion-packet-check:
	$(MAKE) completion-packet-validate
	$(MAKE) completion-packet-apply
	@echo "OK: completion packet check completed with current deferred-safe behavior"

# =============================================================================
# 16 Completion packet / prompt finalization FINISH
# =============================================================================


# =============================================================================
# 18 Local previews / operator workflows START
# =============================================================================

# Purpose: preview shared operational dictionary exports.
# Result: operator can inspect dictionary preview output.
.PHONY: dictionary-preview
dictionary-preview:
	PYTHONPATH=app $(PYTHON) scripts/preview_shared_operational_dictionaries.py

# =============================================================================
# 18 Local previews / operator workflows FINISH
# =============================================================================


# =============================================================================
# 90 Module workflow helpers START
# =============================================================================

# Purpose: prepare Library for prompt execution.
# Result: Blueprint sync, policy check, Prompt Queue dashboard, awareness dashboard and next prompt are shown.
.PHONY: module-start
module-start:
	$(MAKE) blueprint-sync
	$(MAKE) module-policy-check
	$(MAKE) coordination-check
	$(MAKE) prompt-dashboard
	$(MAKE) document-awareness
	$(MAKE) prompt-read-next

# Purpose: synchronize Library with Blueprint without executing a prompt.
# Result: Blueprint sync, coordination fix/check and awareness dashboard run.
.PHONY: module-sync
module-sync:
	$(MAKE) blueprint-sync
	$(MAKE) coordination-fix
	$(MAKE) coordination-check
	$(MAKE) document-awareness

# Purpose: run validation before completion or commit.
# Result: check report, check, governance check, cleanup and status report run.
.PHONY: module-validate
module-validate:
	$(MAKE) check-report
	$(MAKE) check
	$(MAKE) governance-check
	$(MAKE) report-clean
	$(MAKE) status-report

# Purpose: finalize current prompt work.
# Result: validation and deferred-safe completion packet check run.
.PHONY: module-finish
module-finish:
	$(MAKE) module-validate
	$(MAKE) completion-packet-check

# =============================================================================
# 90 Module workflow helpers FINISH
# =============================================================================