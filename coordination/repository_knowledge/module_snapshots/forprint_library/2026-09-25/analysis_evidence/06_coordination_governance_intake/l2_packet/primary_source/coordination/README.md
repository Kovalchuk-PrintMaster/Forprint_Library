# ForPrint Library Coordination

This directory stores coordination metadata for the ForPrint Library module.

ForPrint Library is the canonical catalog, semantic naming, alias and contract-definition
authority for the ForPrint ecosystem.

It must stay aligned with ForPrint System Blueprint and must not become an operational
database for clients, orders, payments, warehouse stock, production runtime, CRM workflow,
Telegram runtime, Calculator logic, or 1C synchronization.

## Structure

- `blueprint_source.yaml` — location of Blueprint policies, standards and directives.
- `prompts/index.yaml` — received prompt/directive index.
- `prompts/received/` — imported Blueprint directives or owner prompts.
- `reports/index.yaml` — completion and commit report index.
- `reports/completion/` — completion reports.
- `reports/commits/` — commit/checkpoint reports.
- `status/current_status.yaml` — machine-readable current status.
- `status/current_status.md` — human-readable current status.
- `status/next_questions_for_blueprint.md` — open questions for Blueprint.