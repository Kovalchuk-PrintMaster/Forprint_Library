# ForPrint Library — L5 Capability Reconciliation Report

## Result

**L5_CAPABILITY_RECONCILIATION=CLOSED_WITH_LATER_IMPLEMENTATION_ITEMS**

This record resolves the 13 L5 questions using the evidence packet produced at Library HEAD `bba52bf6001f256a5c13ea7dbe175336b431754c` on branch `feature/library-calculator-input-contract-v01`.

L5 is architectural reconciliation only. No source implementation, cleanup, regeneration, roadmap mutation, or Blueprint write is authorized by this report.

## Executive reconciliation

- Library remains canonical semantic/reference/catalog authority, while operational/pricing/accounting/runtime truth stays with domain owners.
- Calculator Input is a specialized deterministic Library projection for Calculator, not a parallel semantic authority.
- Generic reference identity and resolution semantics belong to the Library reference layer; Reference Consumption is a validation/consumer-boundary profile.
- `reference_resolution_status` becomes the generic target vocabulary; older `library_reference_*` and product-specific resolution names require compatibility mapping, not silent replacement.
- Catalog seed is source for generated component catalogs; generated catalog schemas/examples and dictionary YAML are projections of their generator/source direction.
- Local `ContractVersion` is scaffolding, not an ecosystem Contract Registry. Cross-module adoption waits for the governed Contract Registry surface.
- Blueprint Prompt Queue is intake authority; local active prompt is a synchronized execution copy. Local prompt/status indexes that are stale are not current truth.
- Implementation truth (git + validated completion evidence) and Blueprint acceptance/release truth are distinct; `current_status.*` is a derived projection and is currently stale.
- Makefile remains the operator-facing functional map, but effect classes must later become explicit because aggregate targets mix read-only and mutating actions.

## Cluster A — Contract layers

### A01

**Decision:** Calculator Input is a specialized deterministic projection/composition over Library-owned product semantics and references; it is not an independent semantic contract authority parallel to the generic Library Reference Contract.

**Canonical authority:** Library canonical product/configuration semantics; Library Reference Contract for generic reference identity/resolution semantics; Calculator Input contract for Calculator-specific envelope shape.

**Compatibility boundary:** Calculator Input may embed/project Library reference IDs and validation snapshots, but must not redefine canonical reference identity, aliases, resolution semantics, pricing, or Calculator runtime behavior.

**Target relationship:** `generic_reference_contract -> specialized_calculator_input_projection`

**Implementation later:** `YES`

Later work: Remove/avoid duplicated reference-field semantics inside Calculator Input where a shared reference object or mapping can be reused without breaking current fixtures.

### A02

**Decision:** Canonical reference identity fields belong to Library semantic/reference authority. Consumer-specific contracts may carry them only as references/projections plus consumer-owned context.

**Canonical authority:** ForPrint Library canonical IDs, aliases, deprecation and reference semantics.

**Compatibility boundary:** Downstream modules may persist Library IDs and raw/alias input, but may not invent or rename canonical Library IDs.

**Target relationship:** `library_reference_identity_authority -> consumer_projection_only`

**Implementation later:** `NO`

### A03

**Decision:** Reference Consumption is a consumer-boundary validation/demo layer, not a producer-side contract authority. It consumes the generic Library Reference Contract and proves that foreign runtime context can coexist without semantic ownership leakage.

**Canonical authority:** Generic Library Reference Contract; consumer-owned runtime/domain fields in downstream modules.

**Compatibility boundary:** Reference Consumption must not define new canonical IDs, statuses, or Library-owned runtime state.

**Target relationship:** `reference_contract -> reference_consumption_validation_profile`

**Implementation later:** `NO`

### A04

**Decision:** The local Contract/ContractVersion models are currently Library implementation scaffolding for describing versioned contracts, not the ecosystem Contract Registry authority. Expansion of lifecycle/adoption semantics must wait for or align with the governed Contract Registry.

**Canonical authority:** Library may own contract definitions for Library semantics; Blueprint governs cross-module adoption direction.

**Compatibility boundary:** Existing ContractVersion can remain readable/usable locally, but must not become an implicit registry of ecosystem adoption, rollout, or release authority.

**Unresolved dependency:** No coordination/roadmaps/forprint_contract_registry.yaml was present in the L5 evidence packet; Human Intent nevertheless requires a versioned Contract Registry/adoption process.

**Target relationship:** `library_contract_definition -> future_contract_registry_registration/adoption`

**Implementation later:** `YES`

Later work: Create/consume the canonical Contract Registry contract when Blueprint exposes it; then map or adapt local ContractVersion without silently replacing historical models.

## Cluster B — Dictionary/status semantics

### B01

**Decision:** Library is the publication/reference authority for shared cross-module vocabulary IDs, labels, aliases and compatibility metadata, but domain modules remain owners of operational state meaning and factual lifecycle truth.

**Canonical authority:** Library shared dictionary publication; domain modules for operational facts/business lifecycle semantics.

**Compatibility boundary:** order/payment/production/etc. dictionary values may be published by Library as shared vocabulary, but Library must not thereby own orders, payments, production state, or domain transition rules.

**Unresolved dependency:** Some current policy text says Library 'owns canonical shared operational dictionary definitions'; this must be interpreted as vocabulary publication, not domain business-rule ownership.

**Target relationship:** `domain_semantics + cross_module_governance -> library_published_shared_vocabulary`

**Implementation later:** `YES`

Later work: Clarify metadata/ownership fields so vocabulary publication authority is distinguishable from domain semantic/state authority.

### B02

**Decision:** reference_resolution_status is the generic canonical resolution-state vocabulary. product_service_reference_status is a specialization/compatibility profile and the older library_reference_* values in Reference Contract v0.2 are legacy compatibility names that should converge through an explicit mapping rather than remain independent truth.

**Canonical authority:** reference_resolution_status for generic resolution states.

**Compatibility boundary:** Existing v0.2 fixtures and consumers must remain readable until migration; no silent value rewrite.

**Target relationship:** `reference_resolution_status -> specialized_compatibility_profiles`

**Implementation later:** `YES`

Later work: Define alias/migration table for library_reference_pending/library_reference_confirmed and product_service-specific names to generic resolution values.

### B03

**Decision:** For the current implementation, export_shared_operational_dictionaries.py constants/metadata are the implementation source; dictionary YAML and shared schema are generated projections; policy docs are explanatory/supporting. This direction must not be reversed by editing generated YAML as independent truth.

**Canonical authority:** export_shared_operational_dictionaries.py implementation definitions.

**Compatibility boundary:** Generated dictionary files remain committed/readable artifacts but are not independently editable semantic owners.

**Target relationship:** `current_generator_definition -> generated_dictionary_yaml/schema`

**Implementation later:** `YES`

Later work: Consider moving canonical dictionary definitions from Python constants into a dedicated declarative source, with the exporter becoming a pure renderer; this is a later implementation choice, not an L5 mutation.

## Cluster C — Generation authority

### C01

**Decision:** catalog/seeds/catalog_seed_v0_1.yaml is the canonical draft semantic input for the generated component catalogs. materials/product_families/operations/print_modes/finishing_options YAML files are projections. Configurable product cards such as business_card.yaml are separate hand-owned product-definition surfaces unless a future generator explicitly owns them.

**Canonical authority:** catalog_seed_v0_1.yaml for component catalog seed semantics; configurable product files for their own product definitions.

**Compatibility boundary:** Generated component catalog YAML must not be edited as a competing source of truth.

**Target relationship:** `catalog_seed -> component_catalog_projections; configurable_product_definition = separate_authority`

**Implementation later:** `NO`

### C02

**Decision:** Catalog component schemas and seed example produced by export_catalog_schema_artifacts.py are generated artifacts. Calculator Input, generic Reference Contract and Reference Consumption schemas are independent contract surfaces and must not be classified as catalog-generator outputs.

**Canonical authority:** generator code for generated catalog schemas/examples; individual contract definitions/schemas for contract-specific shapes.

**Compatibility boundary:** Do not generalize one generator authority across unrelated contract schemas.

**Target relationship:** `generator_scoped_outputs_only; independent_contract_schemas_remain_independent`

**Implementation later:** `NO`

### C03

**Decision:** Current drift evidence is provided by seed validation, catalog projection readiness tests, dictionary validation/tests and committed generated outputs. The canonical future gate should compare regenerated output with committed projection without granting generated files independent authority.

**Canonical authority:** source definitions + generator; validation/tests as proof.

**Compatibility boundary:** A passing generated-file test proves synchronization, not ownership.

**Target relationship:** `source + generator + reproducibility_gate -> generated_projection`

**Implementation later:** `YES`

Later work: Add explicit no-diff/dry-run regeneration gates where missing and expose them through Makefile as clearly mutating vs read-only workflows.

## Cluster D — Coordination lifecycle

### D01

**Decision:** Blueprint Prompt Queue is the authoritative intake/order source for governed work. coordination/prompts/active/current_blueprint_prompt.md is a synchronized local execution copy/fallback. coordination/prompts/index.yaml is stale and cannot be used as current queue truth.

**Canonical authority:** Blueprint Prompt Queue for task intake; local active prompt only for the currently synchronized execution copy.

**Compatibility boundary:** Historical local prompts remain provenance; they must not override a newer Blueprint queue item.

**Target relationship:** `blueprint_prompt_queue -> local_synced_prompt -> local_execution`

**Implementation later:** `YES`

Later work: Repair/redefine the local prompt index so its semantics match actual intake lifecycle or retire it from current-truth use.

### D02

**Decision:** Implementation truth and Blueprint acceptance truth are separate. Git/committed code plus validated completion evidence establish what the module implemented; Blueprint acceptance/release authority establishes governed adoption. reports/index.yaml is supporting registry. current_status.md/yaml and next_questions_for_blueprint.md are projections and are currently stale, so they must not override later git/completion evidence.

**Canonical authority:** git + validated implementation/completion evidence for implementation state; Blueprint acceptance/release surfaces for governed acceptance/adoption.

**Compatibility boundary:** A completed implementation is not automatically Blueprint-accepted; stale status projections do not erase later implementation.

**Target relationship:** `implementation_evidence || blueprint_acceptance -> derived_current_status_projection`

**Implementation later:** `YES`

Later work: Regenerate or replace current_status surfaces from authoritative evidence and make stale-state detection part of governance checks.

### D03

**Decision:** The Makefile already exposes many operator workflows, but read-only and mutating behavior is mixed inside aggregate targets. Targets such as checks/list/preview are read-only; sync/fix/write/update/pull/clean and some aggregate workflows mutate local or Blueprint-adjacent state. Operator safety requires this distinction to be explicit and machine-checkable.

**Canonical authority:** Makefile as operator-facing functional map.

**Compatibility boundary:** Aggregate targets like blueprint-sync, governance-check, module-start/module-sync/module-validate may invoke mutating subtargets even when their names sound observational.

**Target relationship:** `make_target -> declared_effect_class(read_only|local_mutation|external_repo_mutation|generated_output)`

**Implementation later:** `YES`

Later work: Add/standardize effect annotations or a target registry and validate Makefile coverage during closeout.

## L5 implementation candidates carried forward

- **A01** — Remove/avoid duplicated reference-field semantics inside Calculator Input where a shared reference object or mapping can be reused without breaking current fixtures.
- **A04** — Create/consume the canonical Contract Registry contract when Blueprint exposes it; then map or adapt local ContractVersion without silently replacing historical models.
- **B01** — Clarify metadata/ownership fields so vocabulary publication authority is distinguishable from domain semantic/state authority.
- **B02** — Define alias/migration table for library_reference_pending/library_reference_confirmed and product_service-specific names to generic resolution values.
- **B03** — Consider moving canonical dictionary definitions from Python constants into a dedicated declarative source, with the exporter becoming a pure renderer; this is a later implementation choice, not an L5 mutation.
- **C03** — Add explicit no-diff/dry-run regeneration gates where missing and expose them through Makefile as clearly mutating vs read-only workflows.
- **D01** — Repair/redefine the local prompt index so its semantics match actual intake lifecycle or retire it from current-truth use.
- **D02** — Regenerate or replace current_status surfaces from authoritative evidence and make stale-state detection part of governance checks.
- **D03** — Add/standardize effect annotations or a target registry and validate Makefile coverage during closeout.

These are not authorized implementation tasks yet. L6 must first map them against the current roadmap and realization state.

## Stage closeout

```text
L0  PRE-FLIGHT                         CLOSED
L1  INVENTORY + SEGMENTATION           CLOSED
L2  SEQUENTIAL BLOCK ANALYSIS          CLOSED
L3  CAPABILITY SYNTHESIS               CLOSED
L4  DOCUMENT / ARTIFACT AUTHORITY      CLOSED
L5  CAPABILITY RECONCILIATION          CLOSED

NEXT=L6_ROADMAP_REALIZATION
```

L6 should compare the reconciled capability/authority model against roadmap and Human Intent, classify realized/partial/roadmap-only/untracked capabilities, and produce the module-level canonical update package. Cleanup remains deferred.
