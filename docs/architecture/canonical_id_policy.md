# Canonical ID Policy

## Status

Draft policy for ForPrint Library canonical IDs.

## Core rule

Canonical IDs are stable internal truth.

Human-readable names may change, but canonical IDs should remain stable unless a
formal migration is created.

## Names are not truth

Names such as:

- `Візитка`;
- `Business card`;
- `карточка`;

may all point to one canonical ID:

```yaml
product_family_id: business_card

Dependent modules must reference canonical IDs, not uncontrolled free text.

Alias relationship

Aliases help users and modules find the correct canonical ID, but aliases are
not canonical truth.

Aliases may be added, deprecated or reviewed without changing the canonical ID.

Dependent module rule

Dependent modules should store and exchange Library IDs where possible.

Examples:

material_id: paper_350g_gloss
product_family_id: business_card
operation_id: digital_print
print_mode_id: color_4_4
finishing_option_id: matte_lamination
Ambiguous input

If a name or alias can point to more than one entity, the system must not
silently choose a random ID.

Ambiguous input should be reported as unresolved or routed to a future approval
workflow.

Current seed limitation

Canonical Catalog Seed v0.1 is:

catalog_status: draft_canonical_seed
schema_status: unstable_v0_1
usage: allowed_for_projection_use
contract_status: not_final_contract

It is safe for projection use, but it is not a final production contract.


---