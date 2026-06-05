# ADR-0002: Historical Compatibility

## Status

Accepted

## Context

The system must be able to read documents created many years ago under old contract versions.

## Decision

Old contracts are never physically deleted if historical documents depend on them.

A contract version may be blocked for new input but must remain readable for archive, audit and reporting.

## Consequences

Each document must preserve `contract_code` and `contract_version`.

Migration Graph and Semantic Registry are required from the early project stages.
