# Library Calculator Input Contract v0.1

## Purpose

This document defines the ForPrint Library read-only Calculator input contract
for `product.business_card`.

The contract converts a validated configurable product selection into a
deterministic, schema-versioned envelope that Calculator can consume as
reference input.

## Ownership boundary

Library owns:

- product identity;
- configurable parameter definitions;
- validation and normalization rules;
- Library reference identifiers;
- deterministic product-configuration projection;
- schema/version metadata.

Calculator owns:

- price formulas;
- pricing policy;
- numerical calculations;
- costs and margins;
- quote totals.

The Library contract must not contain prices, totals, margins, costs, taxes,
discounts, currency fields, vendor prices or hidden formulas.

## Schema versioning

Current envelope schema:

`calculator_input_envelope_v0_1`

Unsupported schema versions fail with the stable error type:

`unsupported_projection_version`

## Public entry point

```python
build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope
```

The entry point is read-only. It does not mutate input mappings, perform writes,
make network calls, import Calculator code or create runtime records.

## Business-card projection

For `product.business_card`, the projection includes:

- `product_id`;
- `size`;
- `sides`;
- `material_ref`;
- `print_mode_ref`;
- `quantity`;
- `finishing_refs`;
- `artwork_source` when supplied.

## Deterministic serialization

Serialized envelope field order is stable:

1. `schema_version`
2. `product_id`
3. `configuration_id`
4. `normalized_parameters`
5. `reference_ids`
6. `validation_snapshot`

`finishing_refs` are normalized by catalog and id. Duplicate finishing
references are collapsed.

## Error taxonomy

Stable public error types:

- `unknown_product`
- `invalid_configuration`
- `missing_required_parameter`
- `invalid_reference`
- `unsupported_projection_version`
- `internal_contract_error`

Errors are safe for Calculator consumption and do not expose stack traces or
persistence internals.

## Fixture paths

Machine-readable fixtures live in:

`examples/calculator_input_contract/`

Schema lives in:

`schemas/calculator_input/calculator_input_envelope.schema.yaml`

## Calculator consumption example

Calculator may consume the envelope as reference input context. Calculator must
still own all price formulas, pricing policy, totals, cost and margin logic.

## Forbidden scope

This contract does not implement:

- price formulas;
- quote totals;
- cost, margin, discount, tax or currency calculations;
- Calculator internals;
- canonical-order creation;
- Telegram behavior;
- Logistics behavior;
- CRM, Gateway, 1C, payment, stock or production writes;
- production deployment.
