# Downstream Reference Contract Notes v0.1

## Status

Draft downstream handoff notes for early ForPrint modules.

## Purpose

These notes explain how downstream modules should consume Library semantic references without violating ownership boundaries.

## General rule

Downstream modules should store or pass Library canonical IDs when they need to reference product/service, material, operation or template meaning.

They should not copy Library semantic ownership into their own local databases.

## Calculator Engine

Calculator Engine may consume Library IDs as context:

```text
product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
operation.print.digital_color
template.business_card.90x50

Allowed:

use canonical IDs as pricing input context
use aliases for input normalization
flag unresolved references
flag ambiguous references

Forbidden:

write pricing formulas into Library
treat demo references as final production catalog
make Library responsible for price calculation
Operational Registry

Operational Registry may store Library IDs as operational projections.

Allowed:

store product_service_reference_id
store material_reference_id
store operation_reference_id
store template_reference_id
record reference_resolution_status
surface unresolved references for review

Forbidden:

make Library the order database
write operational lifecycle state into Library
make Library own payment status
make Library own warehouse stock
Ambiguity handling

If a value is unknown, downstream modules should keep the raw input and mark the reference as unresolved.

If a value is ambiguous, downstream modules should keep candidate IDs and require manual review.

No downstream module should silently invent a new canonical Library ID.

Versioning

Local fixtures are versioned as 0.1.

They are safe for examples, tests and downstream handoff discussions.

They are not a final production catalog contract.


---