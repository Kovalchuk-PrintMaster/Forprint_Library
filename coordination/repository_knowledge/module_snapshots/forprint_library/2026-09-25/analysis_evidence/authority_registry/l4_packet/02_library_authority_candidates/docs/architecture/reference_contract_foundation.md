# Library Reference Contract Foundation v0.2

## Purpose

This document defines the local ForPrint Library reference contract foundation.

The goal is to make Library-owned semantic/catalog references safe for downstream
modules without turning downstream modules into owners of Library truth.

This checkpoint is intentionally small.

It is not a production catalog implementation.

## Scope

The reference contract describes how downstream modules may store and exchange
references to Library-owned entities.

The contract covers:

```text
canonical Library reference id format
reference type / entity type
display label
optional alias input
reference resolution status
source module
schema/version marker
deprecation handling
ambiguous/manual-review handling
unknown/unresolved references
example downstream payloads
Library ownership

Library owns:

semantic/catalog IDs
product/service meaning
material meaning
operation meaning
unit meaning
template references
technical card references
aliases
deprecation rules
reference resolution semantics
Downstream ownership boundaries

Downstream modules may store Library references.

Downstream modules must not become owners of Library semantic/catalog truth.

Library must not own:

order state
client database
pricing logic
warehouse stock truth
payment/accounting truth
CRM workflow state
Telegram runtime behavior
Integration Gateway delivery ledger
production runtime state
Canonical reference id format

A canonical Library reference id should be stable, lowercase, namespaced and
dot-separated.

Recommended pattern:

<reference_type>.<domain>.<stable_name>[.<variant_or_version>]

Examples:

product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
operation.print.digital_color
unit.piece
template.business_card.90x50
technical_card.business_card.standard_v1

Reference ids are owned by Library.

Downstream modules should not invent new canonical Library ids locally.

If a downstream module receives user input that does not resolve to a known
Library id, it should store the user input as alias_input and mark the
reference with a non-confirmed resolution status.

Required payload shape

A downstream payload should carry a library_reference object.

Minimal fields:

library_reference:
  schema_version: library_reference_v0_2
  reference_type: product_service
  reference_id: product_service.business_card.standard
  display_label: Business card / standard
  resolution_status: library_reference_confirmed
  source_module: calculator_engine
  alias_input: "візитки стандарт"
Reference types

The v0.2 foundation covers these reference types:

product_service
material
operation
unit
template
technical_card
Resolution statuses

The v0.2 foundation uses these statuses:

library_reference_confirmed
library_reference_pending
ambiguous_manual_review_required
deprecated_reference
unknown
library_reference_confirmed

The reference is known and safe to use as a Library-owned canonical reference.

library_reference_pending

The reference has a plausible alias or provisional input, but Library has not
confirmed it yet.

ambiguous_manual_review_required

The input may match more than one Library-owned entity or needs human review.

deprecated_reference

The reference points to an older Library-owned id that should be migrated or
replaced when safe.

unknown

The input cannot currently be resolved to a known Library-owned entity.

Alias input

alias_input is optional.

It should preserve the original user-facing or downstream-provided wording.

Examples:

візитки стандарт
папір 300
кольоровий друк

Alias input is not a canonical id.

Alias input should not be used as a substitute for a confirmed Library reference.

Deprecation handling

Deprecated references should keep the original reference_id.

They may also provide a replacement candidate:

deprecation:
  is_deprecated: true
  replaced_by: product_service.business_card.standard
  message: Use the current standard business card reference.

Deprecation does not mean the downstream module owns migration truth.

It only means the Library reference contract can communicate the migration
direction.

Manual review handling

Ambiguous references should include a manual review marker:

manual_review:
  required: true
  reason: Multiple Library references may match the alias input.

Manual review should happen before treating the reference as confirmed.

Unknown references

Unknown references should preserve source context and alias input when available.

They should not silently become new Library ids.

A downstream module may keep the unresolved payload for intake, support or
operator review.

Safe downstream pattern

Downstream modules should store:

schema_version
reference_type
reference_id when known
display_label
resolution_status
source_module
alias_input when available
deprecation metadata when relevant
manual_review metadata when relevant

Downstream modules should not store copied Library catalog definitions as their
own source of truth.

Current checkpoint limitations

This checkpoint does not implement:

production catalog database
live API
CRM integration
Telegram integration
Operational Registry write
Calculator pricing logic
warehouse stock logic
accounting/payment logic
1C sync/write
automatic posting
production runtime service

Allowed in this checkpoint:

local docs
local YAML examples
schema files
tests for examples/schema
check-report visibility
small local validation helper
Related local files
examples/reference_contract/library_reference_examples.yaml
schemas/reference_contract/library_reference.schema.yaml
scripts/reference_contract/validate_library_reference_contract.py
tests/content/test_library_reference_contract.py

---
