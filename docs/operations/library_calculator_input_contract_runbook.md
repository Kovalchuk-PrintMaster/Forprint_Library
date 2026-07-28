# Library Calculator Input Contract Runbook

## Purpose

Runbook for verifying the read-only Library Calculator input contract v0.1.

## Scope

This runbook applies only to:

`forprint_library_calculator_input_contract_v0_1`

It covers `product.business_card` projection into Calculator-ready reference
input. It does not authorize pricing, Calculator runtime integration, stock,
1C, order, CRM, Telegram, Logistics, Gateway or production writes.

## Key artifacts

- `app/forprint_library/calculator_input/contract.py`
- `schemas/calculator_input/calculator_input_envelope.schema.yaml`
- `examples/calculator_input_contract/`
- `scripts/calculator_input/validate_calculator_input_contract.py`
- `tests/content/test_calculator_input_contract.py`
- `docs/architecture/library_calculator_input_contract.md`

## Focused verification

```bash
PYTHONPATH=app .venv_forprint_library/bin/python -m pytest   tests/content/test_calculator_input_contract.py   tests/content/test_business_card_product_card.py

PYTHONPATH=app .venv_forprint_library/bin/python   scripts/calculator_input/validate_calculator_input_contract.py
```

## Full validation

```bash
make lint
make format-check
make check
make governance-check
make module-validate
make check-report
make check-report-full
git diff --check
git status -sb
```

## Generated report noise

`make check-report` and `make check-report-full` may update:

- `reports/library_check_report.json`
- `reports/library_check_report.md`

If those contain only generated timing/status noise, restore before commit:

```bash
git restore reports/library_check_report.json reports/library_check_report.md
```

## Expected healthy state

- focused tests pass;
- full Library test suite passes;
- fixture validator passes;
- `git diff --check` passes;
- no product model changes are required;
- no Calculator dependency is imported;
- no external writes are performed.
