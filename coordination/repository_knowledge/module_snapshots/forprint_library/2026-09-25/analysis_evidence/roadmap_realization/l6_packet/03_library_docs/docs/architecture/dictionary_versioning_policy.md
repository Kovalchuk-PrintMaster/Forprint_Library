# Dictionary Versioning Policy

Status

Draft policy for dictionary versioning.

Current version

Shared Operational Dictionary v0.1 uses:

version: "0.1"
dictionary_status: draft_shared_operational_dictionary_v0_1
schema_status: unstable_v0_1
usage: allowed_for_projection_use
contract_status: not_final_contract
owner_module: forprint_library
Stability

Dictionary IDs should be treated as stable once used by dependent modules.

Labels and descriptions may change more freely than IDs.

Deprecation

Deprecated values must remain readable for historical records and migrations.

New values should be added rather than silently changing the meaning of existing IDs.

Compatibility

Dependent modules should keep dictionary projections rebuildable from Library sources.
