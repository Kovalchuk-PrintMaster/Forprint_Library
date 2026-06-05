# Architecture Notes

## Mission

`forprint_library` is the source of truth for contracts, semantic identifiers, schemas, change manifests and migration paths.

## Boundary

The module stores and validates rules. It does not execute operational business logic.

## Key concepts

- Contract
- ContractVersion
- ChangeManifest
- SemanticAttribute
- SemanticValue
- AliasMapping
- MigrationGraph
- LibraryResponse

## Future modules

- `forprint_sync_manager` will consume Change Manifest and bring internal modules to the desired state.
- `forprint_history_manager` or `forprint_migration_manager` will read legacy documents using Migration Graph.
- `forprint_orchestra` will route already valid and normalized work.
