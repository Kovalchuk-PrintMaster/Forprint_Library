# Business Card Skeleton Runbook

## Purpose

This runbook documents the governance operation procedure for the accepted
ForPrint Library configurable product reference:

- Prompt ID: `library_configurable_product_workbench_business_card_skeleton_v0_1`
- Blueprint prompt ID: `2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1`
- Product ID: `product.business_card`
- Blueprint-accepted commit: `a87d62c`

This runbook is governance documentation only. It does not authorize product
model changes, Calculator integration, runtime integration, production writes,
1C writes, stock writes or order writes.

## Scope

Use this runbook when checking, reviewing or preparing the Library-side
business card skeleton for Blueprint governance acceptance.

The accepted implementation provides a Library reference object for business
cards / візитки. It is not a production runtime component and it is not a
pricing engine.

## Canonical artifacts

Product and schema artifacts:

- `catalog/configurable_products/business_card.yaml`
- `schemas/configurable_product.schema.yaml`
- `examples/product_cards/business_card_product_card.yaml`

Documentation artifacts:

- `docs/architecture/configurable_product_workbench.md`
- `docs/architecture/business_card_skeleton.md`
- `docs/operations/business_card_skeleton_runbook.md`
- `docs/operations/business_card_skeleton_recovery.md`

Validation and preview artifacts:

- `scripts/product_workbench/validate_business_card_product.py`
- `scripts/product_workbench/preview_business_card_product.py`
- `tests/content/test_business_card_product_card.py`

Completion metadata artifacts:

- `coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`
- `coordination/reports/index.yaml`
- `coordination/status/current_status.yaml`
- `coordination/status/current_status.md`
- `coordination/status/next_questions_for_blueprint.md`

## Standard verification commands

Run from the repository root:

`/srv/software_development/forprint-project/forprint_library`

Focused tests:

`PYTHONPATH=app .venv_forprint_library/bin/python -m pytest tests/coordination/test_business_card_skeleton_closure.py tests/coordination/test_reference_consumption_pilot_closure.py tests/coordination/test_coordination_foundation_alignment_closure.py tests/content/test_business_card_product_card.py tests/contract/test_completion_report.py`

Full check:

`make check`

Check report:

`make check-report`

Whitespace check:

`git diff --check`

## Generated report noise

`make check-report` may regenerate timing-only report files:

- `reports/library_check_report.json`
- `reports/library_check_report.md`

If those files contain only generated/timing changes, restore them before commit:

`git restore reports/library_check_report.json reports/library_check_report.md`

## Acceptance checklist

Before handing back to Blueprint, confirm:

- focused tests pass;
- `make check` passes;
- `make check-report` passes;
- `git diff --check` passes;
- no root-level duplicate completion report exists;
- generated report noise is not committed unless intentionally required;
- `git status -sb` is clean after commit/push;
- Blueprint repository was not written from the Library-side task;
- `product.business_card` model was not changed during governance closeout.

## Boundary reminders

This checkpoint must not add:

- product schema expansion;
- Calculator integration;
- price formulas;
- stock truth;
- material write-off logic;
- 1C import or synchronization;
- order writes;
- CRM writes;
- Website writes;
- production runtime;
- production task creation;
- real client or order data.

## Calculator dependency note

Calculator may later consume `product.business_card` and its constructor parameters as
reference input context.

This runbook does not define Calculator formulas, pricing ownership or
Calculator runtime integration.
