# Library Calculator Input Contract Recovery

## Purpose

Recovery guidance for the Library Calculator input contract v0.1.

## Recovery principle

Recover by restoring Library reference contract files and fixtures only. Do not
add prices, Calculator internals, external writes, stock truth, 1C sync,
production runtime, order writes or new product-model scope.

## Recovery checks

From repository root:

```bash
git status -sb
git log -8 --oneline
test -f app/forprint_library/calculator_input/contract.py
test -f schemas/calculator_input/calculator_input_envelope.schema.yaml
test -d examples/calculator_input_contract
```

Run focused validation:

```bash
PYTHONPATH=app .venv_forprint_library/bin/python -m pytest   tests/content/test_calculator_input_contract.py   tests/content/test_business_card_product_card.py

PYTHONPATH=app .venv_forprint_library/bin/python   scripts/calculator_input/validate_calculator_input_contract.py
```

Run full validation before returning to Blueprint:

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

## Incompatible schema or fixture regression

If a fixture no longer matches deterministic output:

1. do not edit Calculator behavior;
2. inspect `app/forprint_library/calculator_input/contract.py`;
3. compare the fixture to current `build_calculator_input(...).to_dict()`;
4. restore deterministic ordering and stable schema version;
5. rerun focused and full validation.

## Escalation

Escalate to Blueprint if recovery requires:

- changing `product.business_card`;
- adding Calculator formulas;
- introducing a Calculator package dependency;
- changing public error taxonomy;
- writing to external systems;
- changing order, stock, 1C, production or CRM scope.
