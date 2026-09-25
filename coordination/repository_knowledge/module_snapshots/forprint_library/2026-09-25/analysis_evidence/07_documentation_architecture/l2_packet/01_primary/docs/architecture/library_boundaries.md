# ForPrint Library Boundaries

## Status

Draft architecture policy for ForPrint Library.

## Purpose

ForPrint Library is the canonical semantic, catalog, naming, alias and
contract-definition authority for the ForPrint ecosystem.

It provides stable IDs, canonical names, aliases, semantic definitions and
versioned catalog seeds for dependent modules.

## Library owns

ForPrint Library owns semantic and catalog truth for:

- materials;
- product families;
- products and services;
- operations;
- print modes;
- finishing options;
- aliases;
- canonical IDs;
- contract definitions;
- template references;
- technical-card references.

## Library does not own

ForPrint Library must not become an operational database or runtime owner for:

- clients;
- orders;
- payments;
- warehouse stock truth;
- production runtime;
- 1C synchronization;
- CRM workflow;
- Telegram runtime;
- Calculator logic;
- external customer communication.

## Design rule

Library may define references and canonical IDs that other modules store or
consume, but Library must not store operational records.

For example, Operational Registry may store an order that references
`product_family_id: business_card`, but Library must not store that order.

## Ambiguity routing

If a module receives ambiguous free text, the ambiguity should be routed back to
Library resolution logic or a future human approval workflow.

Library should never silently invent permanent catalog truth from unclear input.