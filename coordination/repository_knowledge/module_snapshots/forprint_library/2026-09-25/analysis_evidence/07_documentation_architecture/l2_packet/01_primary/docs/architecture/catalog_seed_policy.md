# Canonical Catalog Seed Policy

## Status

Draft policy for Canonical Catalog Seed v0.1.

## Seed identity

The current seed is:

```yaml
id: canonical_catalog_seed_v0_1
catalog_status: draft_canonical_seed
schema_status: unstable_v0_1
usage: allowed_for_projection_use
contract_status: not_final_contract
owner_module: forprint_library

Meaning

Canonical Catalog Seed v0.1 is a draft canonical source that dependent modules
may consume as projection input.

It is not a final production contract.

Allowed use

Dependent modules may use the seed to build local read-only projections,
selection lists, lookup helpers and validation fixtures.

Allowed consumers include:

Calculator Engine;
Telegram Bot;
Operational Registry;
Accounting Registry;
Prepress Hub;
CRM;
Website;
future Mobile App.
Not allowed

Dependent modules must not treat this seed as their own permanent catalog
authority.

They must not fork the seed into independent permanent catalogs.

They must not overwrite Library canonical IDs with local free-text names.

Versioning

The seed version is intentionally unstable:

schema_status: unstable_v0_1

Breaking changes may happen before a final contract is approved.

Dependent modules should keep projections rebuildable from Library sources.


---