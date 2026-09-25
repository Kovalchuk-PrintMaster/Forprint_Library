# ForPrint Library Calculator Input Contract v0.1 Completion Report

## Prompt

- Prompt ID: `forprint_library_calculator_input_contract_v0_1`
- Prompt title: ForPrint Library Calculator Input Contract v0.1
- Module: `forprint_library`
- Repository: `/srv/software_development/forprint-project/forprint_library`
- Branch: `feature/library-calculator-input-contract-v01`
- Status: `completed_pending_blueprint_review`
- Scope class: `library_read_contract`
- Product covered first: `product.business_card`

## Commits

- Base Library commit: `01f78ea` (`01f78ea0687f8a9c9bee99d3f1042cda0fce2d55`)
- Final Library implementation commit: `0b8cbce` (`0b8cbce6b4c4dc0d37f9d9fcb4b58d20929dd4a7`)
- Blueprint commit consumed during validation: `3f18787` (`3f1878763c052afca9cdee28b5dfe45c6bb60f5f`)
- Blueprint branch observed during final validation: `main`

## Summary

Library now provides a stable, deterministic, versioned, read-only Calculator
input contract for `product.business_card`.

The contract converts a validated configurable product selection into a
Calculator-ready reference input envelope. It preserves Library ownership of
product identity, configurable parameter definitions, validation,
normalization, reference identifiers and schema metadata.

Calculator remains the owner of price formulas, pricing policy, numerical
calculation, costs, margins and quote totals.

## Public contract

Public package:

- `app/forprint_library/calculator_input/__init__.py`
- `app/forprint_library/calculator_input/contract.py`

Public entry point:

```python
build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope
```

Public envelope semantics:

```python
CalculatorInputEnvelope(
    schema_version: str,
    product_id: str,
    configuration_id: str,
    normalized_parameters: Mapping[str, object],
    reference_ids: CalculatorReferenceIds,
    validation_snapshot: ValidationSnapshot,
)
```

Schema version:

```text
calculator_input_envelope_v0_1
```

## Business-card projection

The `product.business_card` projection includes:

- `product_id`
- `size`
- `sides`
- `material_ref`
- `print_mode_ref`
- `quantity`
- `finishing_refs`
- `artwork_source` when supplied

## Error taxonomy

Stable public error types:

- `unknown_product`
- `invalid_configuration`
- `missing_required_parameter`
- `invalid_reference`
- `unsupported_projection_version`
- `internal_contract_error`

Errors are typed, structurally stable and safe for Calculator consumption.

## Determinism and safety

Confirmed behavior:

- deterministic field ordering in serialized artifacts;
- stable normalization;
- deterministic `finishing_refs` sorting by catalog and id;
- duplicate finishing references collapse deterministically;
- no locale-dependent values;
- no database-object leakage;
- no mutable internal-model leakage;
- no implicit defaults hidden from Calculator;
- explicit schema version;
- explicit validation snapshot;
- no network calls;
- no writes;
- no Calculator import dependency inside Library.

## Schema and fixtures

Schema:

- `schemas/calculator_input/calculator_input_envelope.schema.yaml`

Canonical machine-readable fixtures:

- `examples/calculator_input_contract/minimal_valid_business_card.yaml`
- `examples/calculator_input_contract/business_card_with_finishing.yaml`
- `examples/calculator_input_contract/business_card_with_artwork_source.yaml`
- `examples/calculator_input_contract/invalid_missing_material.yaml`
- `examples/calculator_input_contract/invalid_print_mode_reference.yaml`
- `examples/calculator_input_contract/invalid_quantity.yaml`

Validator:

- `scripts/calculator_input/validate_calculator_input_contract.py`

Tests:

- `tests/content/test_calculator_input_contract.py`
- `tests/content/test_business_card_product_card.py`

## Documentation and recovery

Architecture document:

- `docs/architecture/library_calculator_input_contract.md`

Operations runbook:

- `docs/operations/library_calculator_input_contract_runbook.md`

Recovery guide:

- `docs/operations/library_calculator_input_contract_recovery.md`

Completion report:

- `coordination/reports/completion/forprint_library_calculator_input_contract_v0_1_completion.md`

## Validation evidence

Focused validation:

```text
PYTHONPATH=app .venv_forprint_library/bin/python -m pytest \
  tests/content/test_calculator_input_contract.py \
  tests/content/test_business_card_product_card.py

Result: 25 passed
```

Fixture validator:

```text
PYTHONPATH=app .venv_forprint_library/bin/python \
  scripts/calculator_input/validate_calculator_input_contract.py

Result: OK: Library Calculator input contract validates
```

Required validation:

```text
make lint
Result: LINT_EXIT: 0

make format-check
Result: FORMAT_CHECK_EXIT: 0

make check
Result: CHECK_EXIT: 0
Full suite: 160 passed

make governance-check
Result: GOVERNANCE_CHECK_EXIT: 0

make module-validate
Result: MODULE_VALIDATE_EXIT: 0

make check-report
Result: CHECK_REPORT_EXIT: 0

make check-report-full
Result: CHECK_REPORT_FULL_EXIT: 0

git diff --check
Result: DIFF_CHECK_FINAL_EXIT: 0
```

## Changed files grouped by area

### Contract API

- `app/forprint_library/calculator_input/__init__.py`
- `app/forprint_library/calculator_input/contract.py`

### Schema and fixtures

- `schemas/calculator_input/calculator_input_envelope.schema.yaml`
- `examples/calculator_input_contract/minimal_valid_business_card.yaml`
- `examples/calculator_input_contract/business_card_with_finishing.yaml`
- `examples/calculator_input_contract/business_card_with_artwork_source.yaml`
- `examples/calculator_input_contract/invalid_missing_material.yaml`
- `examples/calculator_input_contract/invalid_print_mode_reference.yaml`
- `examples/calculator_input_contract/invalid_quantity.yaml`

### Validation and tests

- `scripts/calculator_input/validate_calculator_input_contract.py`
- `tests/content/test_calculator_input_contract.py`

### Documentation and recovery

- `docs/architecture/library_calculator_input_contract.md`
- `docs/operations/library_calculator_input_contract_runbook.md`
- `docs/operations/library_calculator_input_contract_recovery.md`

## Compatibility confirmation

Preserved:

- existing `product.business_card` behavior;
- current configurable-product workbench API;
- current validation behavior;
- current public imports outside the new `calculator_input` package;
- existing business-card tests and fixtures;
- module policy and reporting contracts.

## Forbidden-scope confirmation

Not implemented:

- price formulas;
- quote totals;
- cost, margin, discount, tax or currency calculations;
- Calculator internals;
- canonical-order creation;
- Telegram Bot changes;
- Logistics changes;
- CRM changes;
- Gateway changes;
- 1C changes;
- payment writes;
- stock writes;
- production writes;
- production deployment;
- Blueprint repository writes.

## Known warnings and deferred work

Blueprint module directives index remains missing/deferred for `forprint_library`.
This is an existing governance warning and not a blocker for this Library
contract completion.

Blueprint repository refactor is ongoing separately. This completion report
does not restore or modify Blueprint WIP.

Blueprint acceptance and merge to `main` remain deferred until Blueprint review.

## Final status

Ready for Blueprint review after this module-side completion report is committed
and pushed.

RESULT: READY_FOR_BLUEPRINT_REVIEW
