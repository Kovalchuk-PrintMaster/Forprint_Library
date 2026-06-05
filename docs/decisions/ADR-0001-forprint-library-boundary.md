# ADR-0001: forprint_library Boundary

## Status

Accepted

## Context

The ForPrint ecosystem will include calculator, prepress, warehouse, accounting, delivery, orchestrator and synchronization modules.

## Decision

`forprint_library` stores rules, contracts, schemas, dictionaries, semantic IDs, migration graph and change manifests.

It does not calculate prices, process files, manage stock, create accounting entries or route production work.

## Consequences

Other modules depend on `forprint_library` for standards, but keep their own business logic.
