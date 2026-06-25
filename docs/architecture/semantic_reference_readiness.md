# Semantic Reference Readiness v0.1

## Status

Draft readiness checkpoint for `forprint_library`.

## Purpose

This document defines a minimal semantic/reference readiness layer for early downstream module usage.

The goal is not to build the full production catalog database.

The goal is to show how downstream modules can safely refer to canonical Library IDs for product/service, material, operation and template meanings.

## Canonical reference examples

Current local examples are stored in:

```text
examples/semantic_reference_preview.yaml

The example file includes canonical IDs such as:

product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
operation.print.digital_color
template.business_card.90x50

These IDs are stable sample references for early integration discussions.

They are not a final production catalog.

Alias readiness

Aliases are allowed as lookup helpers.

Aliases must not become canonical IDs.

If an alias maps clearly to one reference, the expected resolution status is:

confirmed_with_alias

If an alias is unknown, the expected resolution status is:

unresolved_manual_review_required

If an alias could match more than one canonical reference, the expected resolution status is:

ambiguous_manual_review_required
Boundary

Library owns semantic/catalog meaning.

Library does not own:

pricing formulas
warehouse stock truth
operational order state
client database
payment or accounting truth
production runtime state
Telegram runtime
CRM workflow
1C synchronization or posting
Downstream usage

Calculator Engine may reference canonical IDs for pricing input context, but pricing logic remains in Calculator.

Operational Registry may store canonical reference IDs as projections, but operational truth remains in Operational Registry.

Telegram Bot and CRM may display labels and route unresolved values for review, but they must not invent canonical semantic IDs.

Readiness conclusion

This checkpoint makes Library ready for early semantic/reference handoff.

It does not make Library a production catalog database.


---
