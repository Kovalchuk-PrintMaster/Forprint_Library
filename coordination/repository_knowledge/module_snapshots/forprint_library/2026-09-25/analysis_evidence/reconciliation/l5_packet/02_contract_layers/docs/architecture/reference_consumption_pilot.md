# Library Reference Consumption Pilot v0.3

## Purpose

This document describes a small, local and read-only reference consumption pilot
for ForPrint Library.

The pilot demonstrates how downstream ForPrint modules may consume
Library-owned reference IDs without making Library responsible for downstream
runtime behavior.

This is not a production integration.

This does not start Configurable Product Workbench.

## Active prompt

```text
library_reference_consumption_pilot_v0_3
```
Source contract

The pilot consumes the existing Library Reference Contract Foundation v0.2
example references from:

examples/reference_contract/library_reference_examples.yaml

These references are controlled contract examples. They are not a final
production catalog database.

Library-owned reference IDs

Library-owned reference IDs represent stable semantic references owned by
ForPrint Library.

Examples used by the pilot:

product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
template.business_card.90x50

Library owns the semantic meaning of these reference identifiers.

Library may define and validate reference semantics.

## consumer-owned runtime fields

Consumer-owned runtime fields belong to downstream modules.

Examples:

calculator_engine requested quantity
telegram_bot channel hint
forprint_operational_registry local task reference

These fields may travel next to Library references in consumer payloads, but
they do not become Library-owned fields.

Foreign module references

A consumer payload may include foreign module references.

Examples:

calculator_engine.demo.pricing_context_001
telegram_bot.demo.message_001
forprint_operational_registry.demo.material_ref_001

These foreign module references are owned by the downstream module that created
them.

Library stores no runtime state for these examples.

Boundary rule

Consumer payloads must not redefine Library-owned semantics.

Consumer payloads must not include fields that try to rename, override or mutate
Library references.

Forbidden examples include:

canonical_name_override
semantic_definition_override
library_alias_write
library_reference_write

Consumer payloads must also avoid runtime ownership fields that would imply
Library is performing downstream work.

Forbidden examples include:

final_price
price_formula
stock_mutation
material_write_off
order_creation
client_creation
payment_posting
production_runtime_write
telegram_runtime_behavior
calculator_runtime_integration
operational_registry_write
one_c_sync
one_c_import
What the pilot does

The pilot provides:

local consumer fixture examples
schema documentation
validation that referenced Library IDs exist in the reference contract examples
validation that consumer payloads do not redefine Library-owned semantics
validation that consumer payloads do not place downstream runtime ownership in Library
human-readable preview output
tests for valid and invalid payloads
What the pilot does not do

The pilot does not implement Calculator formulas.

The pilot does not implement Telegram runtime behavior.

The pilot does not implement Operational Registry storage.

The pilot does not implement Accounting Registry behavior.

The pilot does not implement Prepress Hub behavior.

The pilot does not import 1C data.

The pilot does not synchronize with 1C.

The pilot does not create clients.

The pilot does not create orders.

The pilot does not mutate stock.

The pilot does not calculate final price.

The pilot does not expose a live API.

The pilot does not start production runtime.

The pilot does not start Configurable Product Workbench.

Example preview

A valid consumer payload may be rendered as:

Consumer: calculator_engine
Uses Library reference: product_service::product_service.business_card.standard
Boundary: no semantic redefinition, no downstream runtime write

This means Calculator Engine may use the Library reference as a stable semantic
identifier, but Library does not calculate price and does not own Calculator
runtime behavior.

Readiness

This pilot proves that Library reference contracts can be consumed locally by
example downstream payloads while preserving module boundaries.

It prepares the ground for future module integration contracts, but does not
perform real integration.