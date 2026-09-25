# ForPrint Library — Module Knowledge Stabilization Pilot
## L2 Block Analysis Report — `02_dictionaries_resolution_profiles`

**Module:** `forprint_library`  
**Stage:** `L2 — Sequential Block Analysis`  
**Block:** `02_dictionaries_resolution_profiles`  
**Analysis status:** `ANALYZED_WITH_RECONCILIATION_CANDIDATES`  
**Block closeout recommendation:** `PASS_FOR_L2_WITH_CARRIED_SEMANTIC_RECONCILIATION`  
**Date:** 2026-09-24  
**Mutation performed:** false  
**Implementation authority:** none  
**Roadmap mutation authority:** none  
**Primary evidence packet:** `l2_block_02_analysis_packet.md`  
**Primary source population:** 36 files  
**Direct related-test population in this packet:** 0 files  
**Prior L2 supporting context:** Block 01 analysis  
**Blueprint/context evidence:** 8 files + 2 bounded roadmap subsets

---

# 1. Executive conclusion

Block `02_dictionaries_resolution_profiles` proves that ForPrint Library already contains a real current semantic dictionary and reference-resolution layer.

The strongest current implementation facts are:

1. A **Shared Operational Dictionary v0.1** exists and is Library-owned.

2. It currently contains **18 dictionary groups** and **158 dictionary entries**.

3. Entry lifecycle distribution in the captured evidence is:
   - 156 `active`;
   - 2 `deprecated`;
   - 0 `draft`.

4. The dictionary as a whole is nevertheless explicitly **draft / unstable / projection-only**:
   - `dictionary_status: draft_shared_operational_dictionary_v0_1`
   - `schema_status: unstable_v0_1`
   - `usage: allowed_for_projection_use`
   - `contract_status: not_final_contract`
   - `unit_dictionary_status: not_final_inventory_unit_system`

5. Current group dictionaries are exact per-group projections of the combined shared dictionary.

6. A generator script exists that currently defines the dictionary value lists, label overrides, aliases and deprecated values and writes:
   - the combined shared dictionary;
   - all group dictionary YAML files;
   - both dictionary schemas.

7. A real group-scoped resolver exists. It supports:
   - exact ID resolution;
   - alias resolution;
   - unresolved input;
   - ambiguous alias detection;
   - deprecated reference detection.

8. Dictionary identity is **group-scoped**, not globally ID-scoped:
   - IDs such as `unknown`, `cancelled`, `completed`, `in_progress` intentionally repeat across groups;
   - callers must preserve `dictionary_group` context.

9. `CatalogRegistry` source is present in this packet. This closes the Block 01 uncertainty where its behavior was test-visible but its implementation source was absent.

10. Naming profiles, profile-specific defaults, production tokens, device/equipment capability context and misspelling governance are **not implemented by the Block 02 primary source population**.

11. The packet contains **zero direct related test files** because L1 secondary test relationships did not associate tests with Block 02. Existing tests are referenced by prior Block 01 analysis, but their source is not direct evidence in this packet.

12. Several semantic and structural reconciliation candidates were discovered:
   - three overlapping resolution-status vocabularies;
   - three equivalent alias-normalization functions;
   - current dictionary generator/source-direction ambiguity at the authority/documentation level;
   - several scripts misclassified into Block 02;
   - a stale mutating coordination exporter that must not be treated as current operational authority;
   - partial Ukrainian localization;
   - no mature profile-aware naming layer despite roadmap intent.

The block is valid and useful current implementation, but it is not yet the mature target semantic-profile system.

---

# 2. Evidence boundary

This report distinguishes:

## 2.1 Current implementation evidence

The 36 files selected by the reviewed L1 Block 02 manifest.

Used to determine:

- dictionary data;
- resolver behavior;
- loader/validation implementation;
- generator direction;
- current schema/maturity;
- current semantic helper surfaces.

## 2.2 Direct test evidence

`RELATED_TEST_COUNT=0`.

Therefore this report does **not** independently claim a Block 02 pytest result from the packet.

The packet build itself passed; that is not equivalent to test execution.

## 2.3 Prior L2 supporting evidence

Block 01 analysis is present as supporting cross-block context.

It identifies existing adjacent tests for:

- dictionary policy docs;
- shared dictionary completion report;
- shared operational dictionary v0.1;
- dictionary resolver and preview.

Their presence is useful context, but their source bodies are not included as direct Block 02 test evidence.

## 2.4 Blueprint / Human Intent / roadmap context

Used for intended ownership and future direction.

Planning context does not prove implementation.

---

# 3. Block population review

The reviewed L1 manifest selected 36 primary files.

## 3.1 Strongly in-scope core implementation

### Dictionary Python layer

- `app/forprint_library/dictionaries/__init__.py`
- `app/forprint_library/dictionaries/loader.py`
- `app/forprint_library/dictionaries/models.py`
- `app/forprint_library/dictionaries/resolver.py`
- `app/forprint_library/dictionaries/validation.py`

### Semantic helpers

- `app/forprint_library/semantic/__init__.py`
- `app/forprint_library/semantic/aliases.py`
- `app/forprint_library/semantic/resolver.py`

### Dictionary data

- 18 group dictionary YAML files;
- `dictionaries/shared_operational_dictionary_v0_1.yaml`

### Schemas

- `schemas/dictionary_entry.schema.yaml`
- `schemas/shared_operational_dictionary.schema.yaml`

### Generator

- `scripts/export_shared_operational_dictionaries.py`

This generator is strongly relevant because it currently constructs and writes the dictionary population and schemas.

---

# 4. Block-boundary reclassification candidates

No file should be moved during L2.

These are reconciliation candidates only.

## RECLASS-CAND-LIB-B02-001 — Catalog registry

**Path:**
`app/forprint_library/catalog/registry.py`

**Observed responsibility:**

- loads the catalog seed;
- validates the catalog seed;
- indexes catalog entries by ID;
- builds global catalog alias index;
- resolves catalog aliases.

**Primary functional fit:**

`01_domain_semantics_catalog`

**Candidate disposition:**

`RECLASSIFY_PRIMARY_TO_01_DOMAIN_SEMANTICS_CATALOG`

This file closes Block 01 uncertainty `UNC-LIB-B01-001`.

---

## RECLASS-CAND-LIB-B02-002 — Dictionary policy document exporter

**Path:**
`scripts/export_dictionary_policy_docs.py`

**Observed responsibility:**

Writes architecture/policy documentation from embedded static strings.

**Primary functional fit:**

`07_documentation_architecture`

Potential secondary relation:

`02_dictionaries_resolution_profiles`

L1 already marked this file as a legacy candidate.

---

## RECLASS-CAND-LIB-B02-003 — Coordination artifact exporter

**Path:**
`scripts/export_shared_dictionary_coordination_artifacts.py`

**Observed responsibility:**

Mutates:

- `coordination/status/current_status.yaml`
- `coordination/status/current_status.md`
- `coordination/reports/index.yaml`
- a completion report.

**Primary functional fit:**

`06_coordination_governance_intake`

**Important safety note:**

The script embeds an earlier checkpoint state dated `2026-06-09` and writes status such as:

`shared_operational_dictionary_v0_1_ready_pending_blueprint_review`

It must not be treated as a current status authority or casually re-run during Stage 2.

Candidate disposition:

`LEGACY_OR_CHECKPOINT_SPECIFIC_MUTATING_COORDINATION_EXPORTER_RECONCILE_BEFORE_REUSE`

---

## RECLASS-CAND-LIB-B02-004 — Preview tool

**Path:**
`scripts/preview_shared_operational_dictionaries.py`

**Primary functional fit:**

`04_exports_previews_examples`

Secondary capability support:

Block 02 dictionary consumption.

---

## RECLASS-CAND-LIB-B02-005 — Reference Contract validator

**Path:**
`scripts/reference_contract/validate_library_reference_contract.py`

**Primary functional fit:**

`03_contracts_cross_module_consumption`
or
`05_validation_tests_quality`

It validates the Library Reference Contract, not the shared dictionary itself.

---

## RECLASS-CAND-LIB-B02-006 — Shared dictionary validation CLI

**Path:**
`scripts/validate_shared_operational_dictionaries.py`

**Primary functional fit:**

`05_validation_tests_quality`

It is an important validation surface for Block 02 but functionally belongs to quality/check tooling.

---

# 5. Current Shared Operational Dictionary population

The current dictionary model declares 18 groups.

| Dictionary group | Entries | Active | Deprecated | Aliases |
|---|---:|---:|---:|---:|
| `source_system` | 16 | 16 | 0 | 12 |
| `entity_type` | 23 | 23 | 0 | 1 |
| `order_status` | 10 | 10 | 0 | 8 |
| `order_line_status` | 8 | 8 | 0 | 7 |
| `payment_status` | 8 | 8 | 0 | 7 |
| `production_status` | 8 | 8 | 0 | 5 |
| `workflow_status` | 7 | 7 | 0 | 5 |
| `workflow_stage_status` | 10 | 10 | 0 | 8 |
| `material_requirement_status` | 8 | 8 | 0 | 4 |
| `reference_resolution_status` | 6 | 5 | 1 | 1 |
| `product_service_reference_status` | 6 | 5 | 1 | 1 |
| `contractor_reference_status` | 6 | 6 | 0 | 3 |
| `deadline_type` | 6 | 6 | 0 | 1 |
| `alert_rule_type` | 7 | 7 | 0 | 1 |
| `alert_severity` | 5 | 5 | 0 | 3 |
| `alert_event_status` | 6 | 6 | 0 | 1 |
| `notification_status` | 6 | 6 | 0 | 1 |
| `unit` | 12 | 12 | 0 | 8 |
| **Total** | **158** | **156** | **2** | **77** |

Every group currently includes an `unknown` entry.

No duplicate IDs within a group were observed in the captured data.

No duplicate normalized aliases within a group were observed in the captured data.

---

# 6. Critical maturity distinction

The entry field:

`status: active`

does **not** mean the dictionary contract is production-final.

Current global dictionary metadata remains:

- draft;
- schema unstable;
- projection-use only;
- not a final contract.

Therefore the correct interpretation is:

> Entries are active members of the current draft dictionary vocabulary.

Not:

> These values are final production contract values.

This distinction must be preserved in future knowledge projections.

---

# 7. Provisional capability map

Capability IDs below are L2 candidates only.

Do not finalize stable capability IDs before L3.

---

## CAP-CAND-LIB-B02-01 — Shared Operational Dictionary v0.1

**Implementation state:** `VERIFIED_CURRENT_DRAFT_PROJECTION`

**Confidence:** HIGH

### Purpose

Provide a Library-owned shared semantic vocabulary for cross-module operational/reference concepts without owning operational facts.

### Implementation

- `dictionaries/shared_operational_dictionary_v0_1.yaml`
- group YAML projections;
- dictionary schemas;
- dictionary Python loader/model/validation layer.

### Current maturity

`draft_shared_operational_dictionary_v0_1`

### Boundary

The dictionary defines language/reference semantics.

It does not create:

- real orders;
- clients;
- payments;
- stock;
- production runtime;
- Calculator pricing;
- CRM workflow;
- 1C accounting truth.

---

## CAP-CAND-LIB-B02-02 — Dictionary generator / projection builder

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Implementation

`scripts/export_shared_operational_dictionaries.py`

### Observed generation direction

The script defines:

- `DICTIONARY_VALUES`
- `UK_LABEL_OVERRIDES`
- `ALIASES`
- `DEPRECATED_VALUES`
- metadata

and generates:

1. combined shared dictionary;
2. 18 group dictionary files;
3. dictionary entry schema;
4. shared dictionary schema.

The captured generated group data is consistent with the combined shared dictionary.

### Important authority question

Behaviorally, the Python generator is an upstream generation surface.

However, L2 does not establish that the generator is the formally declared human-editing authority.

Carry to L4/L5:

`GENERATOR_VS_GENERATED_DICTIONARY_AUTHORITY_REQUIRES_EXPLICIT_DECLARATION`

---

## CAP-CAND-LIB-B02-03 — Group dictionary projections

**Implementation state:** `VERIFIED_CURRENT_GENERATED_PROJECTION`

**Confidence:** HIGH

### Evidence

18 individual group YAML files.

Their `entries` are consistent with the corresponding sections of the combined shared dictionary in the captured evidence.

### Interpretation

These should not be treated as 18 unrelated independent truth stores.

Observed current pattern:

`generator definitions -> shared dictionary -> group dictionary projections`

---

## CAP-CAND-LIB-B02-04 — Dictionary loading and enumeration

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Entry points

- `load_shared_dictionary(...)`
- `load_dictionary(group_name, ...)`
- `load_all_dictionaries(...)`
- `list_dictionary_groups()`

### Behavior

File-backed, read-only loading.

Unknown dictionary groups fail with `KeyError`.

---

## CAP-CAND-LIB-B02-05 — Dictionary structural validation

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Validates

- metadata structure;
- expected draft maturity values;
- required entry fields;
- Library ownership;
- version `0.1`;
- allowed lifecycle statuses;
- expected dictionary group;
- duplicate IDs within groups;
- duplicate aliases within groups.

### Current schema model

Entry fields include:

- `id`
- `label_uk`
- `label_en`
- `description`
- `status`
- `aliases`
- `owner_module`
- `dictionary_group`
- `version`
- `notes`

---

## CAP-CAND-LIB-B02-06 — Group-scoped dictionary resolver

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Entry point

`resolve_dictionary_value(group_name, value_or_alias, dictionary=None)`

### Resolution order

1. normalize input;
2. exact ID match;
3. alias matches;
4. detect multiple alias matches;
5. return one alias match;
6. otherwise unresolved.

### Runtime result states

- `confirmed`
- `confirmed_with_alias`
- `unresolved`
- `ambiguous_manual_review_required`
- `deprecated_reference`

### Important semantics

The resolver is group-scoped.

`group_name` is required.

This is correct for values that intentionally repeat across semantic domains.

---

## CAP-CAND-LIB-B02-07 — Ambiguity detection

**Implementation state:** `VERIFIED_CURRENT_DETECTION_ONLY`

**Confidence:** HIGH

### Entry point

`find_ambiguous_aliases(dictionary)`

### What exists

Detection of aliases that map to more than one ID within a dictionary group.

### What does not exist

No approval workflow, human-review queue, or ambiguity-resolution lifecycle is implemented in this block.

Therefore Blueprint goal:

`Define ambiguity routing and approval lifecycle`

is only partially implemented.

---

## CAP-CAND-LIB-B02-08 — Deprecated reference recognition

**Implementation state:** `VERIFIED_CURRENT_PRIMITIVE`

**Confidence:** HIGH

The dictionary resolver recognizes deprecated entries and returns:

`deprecated_reference`

The result property `is_resolved` treats deprecated references as technically resolved.

This means:

- semantic identity can be found;
- lifecycle state still warns that the reference is deprecated.

No migration/supersession graph is implemented here.

---

## CAP-CAND-LIB-B02-09 — Catalog registry / catalog alias lookup

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Source

`app/forprint_library/catalog/registry.py`

### Cross-block finding

This capability belongs primarily to Block 01.

The source now confirms the behavior previously established only by tests:

- validates catalog seed;
- indexes by ID;
- builds normalized global alias index;
- `get(item_id)`;
- `resolve_alias(alias)`.

### Block 01 uncertainty resolution

`UNC-LIB-B01-001 = RESOLVED_BY_BLOCK02_SOURCE_EVIDENCE`

Carry this resolution to L3 synthesis.

---

## CAP-CAND-LIB-B02-10 — Semantic alias normalization helper

**Implementation state:** `CURRENT_BUT_THIN`

**Confidence:** HIGH

### Source

`app/forprint_library/semantic/aliases.py`

### Entry point

`normalize_semantic_alias(value)`

### Behavior

- casefold;
- trim;
- collapse whitespace.

This is currently a very small primitive.

It does not implement:

- misspelling dictionaries;
- transliteration;
- punctuation normalization;
- naming profiles;
- token context;
- device context;
- profile defaults.

---

## CAP-CAND-LIB-B02-11 — Semantic catalog resolver facade

**Implementation state:** `CURRENT_THIN_FACADE`

**Confidence:** HIGH

### Source

`app/forprint_library/semantic/resolver.py`

### Behavior

`resolve_catalog_alias(...)`

delegates directly to:

`CatalogRegistry.resolve_alias(...)`

This is not yet a unified semantic resolver.

---

# 8. Identity model: dictionary group + ID

A critical semantic rule emerges from current implementation.

Dictionary IDs are not globally unique.

Examples such as:

- `unknown`
- `cancelled`
- `completed`
- `in_progress`
- `manual_review_required`

occur in multiple dictionary groups.

Therefore the stable semantic identity is effectively:

`(dictionary_group, id)`

not:

`id`

alone.

This is reinforced by:

- `DictionaryResolutionResult.group_name`;
- group-specific loading;
- group-prefixed duplicate-alias validation.

Future contracts must preserve group context when an ID is not otherwise field-scoped unambiguously.

---

# 9. Alias behavior and normalization

## 9.1 Dictionary alias normalization

Current function:

`normalize_dictionary_lookup_value`

performs:

- `casefold()`
- trim
- whitespace collapse.

## 9.2 Catalog alias normalization

Block 01 found equivalent behavior in catalog normalization.

## 9.3 Generic semantic alias normalization

`normalize_semantic_alias`

also performs the same normalization.

### Reconciliation candidate

Three equivalent normalization primitives currently exist:

- catalog normalization;
- dictionary normalization;
- generic semantic normalization.

Candidate:

`DUP-CAND-LIB-B02-01_ALIAS_NORMALIZATION`

Disposition:

`RECONCILE_BEFORE_IMPLEMENTATION`

Do not consolidate during L2.

A future decision should determine whether:

- one shared normalizer is correct;
- namespace-specific normalizers are intentional;
- future profile-aware normalization makes them diverge.

---

# 10. Generator model limitations

The current generator stores alias definitions as:

`ALIASES[value]`

rather than:

`ALIASES[(group, value)]`

This means entries with the same ID across groups inherit the same alias list.

The same pattern applies to many label overrides.

This is acceptable for the current draft population but cannot express group/profile-specific meaning where the same token or ID needs different aliases/defaults in different contexts.

This directly matters to future naming-profile work.

Candidate:

`MODEL_LIMITATION_GROUP_OR_PROFILE_SPECIFIC_ALIAS_CONTEXT_NOT_SUPPORTED`

---

# 11. Resolution-status semantic reconciliation

This is the strongest semantic reconciliation issue found in Block 02.

There are currently at least three related status vocabularies.

## 11.1 Dictionary resolver runtime statuses

Code constants:

- `confirmed`
- `confirmed_with_alias`
- `unresolved`
- `ambiguous_manual_review_required`
- `deprecated_reference`

## 11.2 Shared dictionary `reference_resolution_status`

Current dictionary values:

- `draft_display_only`
- `reference_pending`
- `reference_confirmed`
- `ambiguous_manual_review_required`
- `deprecated_reference`
- `unknown`

## 11.3 Library Reference Contract statuses

The current Reference Contract validator expects:

- `library_reference_confirmed`
- `library_reference_pending`
- `ambiguous_manual_review_required`
- `deprecated_reference`
- `unknown`

## Interpretation

These may represent three intentionally different layers:

1. internal resolver outcome;
2. shared operational reference state;
3. cross-module Library Reference Contract state.

But their semantic overlap is high and the naming is not self-evidently mapped.

No explicit mapping layer is proven in Block 02.

### Candidate

`SEMANTIC-RECON-LIB-B02-001_RESOLUTION_STATUS_LAYER_MAPPING`

Disposition:

`RECONCILE_BEFORE_NEW_CONSUMER_IMPLEMENTATION`

Do not collapse the vocabularies automatically.

---

# 12. Catalog resolver vs dictionary resolver

These are related but distinct mechanisms.

## Catalog registry

- global catalog seed;
- ID lookup;
- global alias lookup;
- current catalog validation prevents duplicate normalized aliases;
- unknown returns `None`;
- no rich ambiguity result at runtime.

## Dictionary resolver

- explicit group context;
- exact ID then alias;
- supports ambiguity;
- supports deprecated state;
- returns structured `DictionaryResolutionResult`.

### Conclusion

They are **not exact duplicates**.

Candidate relation:

`DISTINCT_RESOLUTION_DOMAINS_WITH_SHARED_NORMALIZATION_CONCERN`

A future unified semantic facade may wrap both, but L2 does not authorize such refactor.

---

# 13. Naming profiles / production tokens assessment

The L1 block title hypothesized:

- dictionaries;
- resolution;
- naming profiles.

Current source proves the first two.

It does **not** prove the third.

No primary implementation was found for:

- naming profile objects;
- profile IDs;
- equipment/device profiles;
- production-token dictionaries;
- profile-specific defaults;
- filename grammar;
- profile-aware token resolver;
- common misspelling registry;
- profile-scoped ambiguity;
- capability context.

The only `profile`-like primary data occurrence is an entity-type value such as `legal_entity_profile`, which is not naming-profile implementation.

Therefore:

`NAMING_PROFILE_IMPLEMENTATION_PROVEN=false`

`PRODUCTION_TOKEN_IMPLEMENTATION_PROVEN=false`

`PROFILE_SPECIFIC_DEFAULTS_IMPLEMENTATION_PROVEN=false`

These remain Human Intent / roadmap targets.

---

# 14. Human Intent relation

## HI-FP-LIBRARY-002 — aliases, alternate names, normalization, provenance/confidence

**Relation:** `PARTIAL_CURRENT`

Implemented:

- aliases;
- basic normalization.

Not proven:

- supplier part numbers;
- provider provenance;
- confidence;
- ambiguous external-merge workflow.

---

## HI-FP-LIBRARY-009 — aliases, misspellings, production tokens, naming profiles/defaults

**Relation:** `PARTIAL_CURRENT`

Implemented:

- canonical aliases;
- basic dictionary/catalog resolution.

Not proven:

- common misspelling model;
- short production-token model;
- naming profiles;
- device/equipment context;
- profile-specific defaults.

---

## HI-FP-LIBRARY-010 — filename omission via profile defaults

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

---

## HI-FP-LIBRARY-011 — same token meaning varies by profile

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

Current generator is not profile-aware.

---

## HI-FP-LIBRARY-012 — Contract Registry/adoption flow

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

Dependency remains roadmap-level.

---

## Semantic registry/discovery intents

Current local resolvers are useful primitives.

They do not constitute the planned shared semantic registration/discovery system.

Relation:

`EARLY_LOCAL_PRIMITIVES_ONLY`

---

# 15. Roadmap ↔ implementation relation

Roadmap and implementation states remain separate.

## FORPRINT_LIBRARY-H01
Reconcile catalog, alias, template, naming-profile and UI evidence.

**Block 02 implementation:** `PARTIAL_CURRENT`

Proven:

- aliases;
- dictionary resolution.

Not proven:

- naming profiles;
- templates;
- UI publication.

---

## FORPRINT_LIBRARY-H02
Confirm semantic ownership excluding business workflows.

**Block 02 implementation:** `CURRENT_ALIGNED`

Shared dictionary definitions remain semantic vocabulary and do not create business records.

---

## FORPRINT_LIBRARY-H03
Inventory IDs, aliases, misspellings, production tokens, templates and technical cards.

**Block 02 implementation:** `PARTIAL_CURRENT`

Proven:

- dictionary IDs;
- aliases.

Not proven:

- misspellings as a governed layer;
- production tokens;
- templates;
- technical cards.

---

## FORPRINT_LIBRARY-H04
Define versioned naming/profile/default semantics.

**Block 02 implementation:** `NOT_PROVEN`

---

## FORPRINT_LIBRARY-H08
Fast capability/semantic discovery.

**Block 02 implementation:** `LOCAL_LOOKUP_PRIMITIVES_ONLY`

---

## FORPRINT_LIBRARY-H09
Deprecation/migration for legacy aliases/profiles.

**Block 02 implementation:** `PARTIAL_PRIMITIVE`

Implemented:

- `deprecated` status;
- deprecated-reference resolver outcome.

Not implemented:

- supersession target;
- migration graph;
- adoption evidence;
- profile migration.

---

# 16. Localization assessment

The generator uses explicit Ukrainian overrides for a subset of IDs.

For values without an override, it falls back to title-casing the identifier.

As a result, many `label_uk` values are currently identical to `label_en`.

In the captured data, **68 of 158** entries have identical UK/EN label text.

Some of these are legitimate names/system identifiers.

Others are ordinary business terms and therefore indicate incomplete Ukrainian localization.

The current schema validates only non-empty strings; it does not validate language quality.

Candidate:

`QUALITY-CAND-LIB-B02-001_PARTIAL_UK_LOCALIZATION`

Do not change labels during L2.

---

# 17. Unit dictionary boundary

Current units include:

- `pcs`
- `set`
- `m`
- `m2`
- `kg`
- `g`
- `l`
- `ml`
- `hour`
- `minute`
- `service`
- `unknown`

Metadata explicitly says:

`unit_dictionary_status: not_final_inventory_unit_system`

Therefore the current unit dictionary must not be treated as:

- Warehouse inventory-unit authority;
- conversion engine;
- accounting unit system;
- measurement/calibration system.

It is a draft shared semantic vocabulary.

---

# 18. Operational-looking statuses do not create operational ownership

The dictionary includes semantic values for:

- order statuses;
- payment statuses;
- production statuses;
- workflow statuses;
- alerts;
- deadlines.

This does **not** mean Library owns:

- order state;
- payment truth;
- production runtime;
- workflow execution.

Current policy and Stage 1 reconciliation consistently preserve those boundaries.

Correct interpretation:

> Library owns shared vocabulary/reference semantics for these concepts; domain modules own the facts and transitions.

---

# 19. Validation assessment

Current Python validation verifies:

- expected dictionary metadata;
- required entry fields;
- group consistency;
- Library ownership;
- version;
- supported lifecycle status;
- duplicate IDs within groups;
- duplicate aliases within groups.

The validation CLI additionally checks:

- shared dictionary schema;
- group dictionaries;
- JSON Schemas;
- selected required IDs.

## Current-data inspection result

Within the captured dictionary population:

- no duplicate IDs within groups were observed;
- no duplicate normalized aliases within groups were observed;
- no alias-to-other-ID collision was observed.

## Validation gap candidate

Current duplicate-alias validation does not explicitly reject:

- a duplicate alias repeated twice on the same entry;
- an alias equal to another entry's ID.

No such collision was observed in current data.

Candidate:

`QUALITY-CAND-LIB-B02-002_ALIAS_ID_COLLISION_GUARD_NOT_EXPLICIT`

Low-to-medium priority; carry to L5/L8.

---

# 20. Direct test-evidence gap

The packet run report states:

`related_test_count: 0`

Yet prior Block 01 analysis identifies adjacent dictionary tests:

- `tests/contract/test_dictionary_policy_docs.py`
- `tests/contract/test_shared_dictionary_completion_report.py`
- `tests/contract/test_shared_operational_dictionary_v0_1.py`
- `tests/integration/test_dictionary_resolver_and_preview.py`

This means the issue is not necessarily absence of tests.

It is an L1 relationship/packet-selection gap.

Candidate:

`ANALYSIS-CAND-LIB-B02-001_TEST_RELATIONSHIP_UNDERLINKED`

Disposition:

- do not reopen L1;
- carry to L3/L5;
- when module-wide synthesis is created, treat these tests as likely Block 02 evidence only after their direct source is inspected in their own block or a bounded follow-up.

---

# 21. Stale mutating coordination exporter risk

`scripts/export_shared_dictionary_coordination_artifacts.py` is especially important.

It contains hard-coded checkpoint metadata from June 2026 and writes current coordination status surfaces.

If executed now, it could project an earlier module phase back into current status files.

Therefore:

`CURRENT_OPERATOR_SAFE_TO_RUN=false`

until reconciled.

Candidate:

`CLEANUP-CAND-LIB-B02-001_STALE_COORDINATION_EXPORTER`

Recommended later disposition options for L8, after authority review:

- archive;
- convert to immutable historical reproduction tool;
- guard against modern HEAD/state;
- replace with current generalized exporter;
- remove from operator surface if obsolete.

No action is authorized in L2.

---

# 22. Dictionary policy-doc generator risk

`scripts/export_dictionary_policy_docs.py` contains full policy documents as embedded static strings and overwrites architecture docs.

This creates a potential source-authority conflict between:

- script-embedded policy;
- generated docs;
- later manually maintained docs.

L1 already marked it as a legacy candidate.

Carry to L4:

`DOCUMENT_AUTHORITY_REQUIRES_RECONCILIATION`

Do not re-run casually.

---

# 23. Duplicate / overlap candidates

## DUP-CAND-LIB-B02-01 — alias normalization

Three equivalent normalization implementations.

Disposition:

`RECONCILE_BEFORE_IMPLEMENTATION`

---

## DUP-CAND-LIB-B02-02 — combined dictionary vs group YAML files

Observed generated parallel representation.

Disposition:

`INTENTIONAL_GENERATED_PROJECTION_LIKELY`

Authority direction still needs explicit documentation.

---

## DUP-CAND-LIB-B02-03 — resolver status vocabularies

Not exact duplicate data, but overlapping concepts across three layers.

Disposition:

`SEMANTIC_MAPPING_REQUIRED`

---

## DUP-CAND-LIB-B02-04 — semantic resolver wrapper

`semantic.resolver.resolve_catalog_alias` is a thin delegate to `CatalogRegistry`.

Disposition:

`POSSIBLE_COMPATIBILITY_OR_FACADE_SURFACE`

Do not remove until public-use evidence is analyzed.

---

# 24. Reuse candidates

## REUSE-CAND-LIB-B02-01 — group-scoped resolver

Potential canonical Library primitive for resolving shared dictionary values.

Consumers should consume it or its contract, rather than recreate independent vocabulary resolution.

## REUSE-CAND-LIB-B02-02 — DictionaryResolutionResult

Useful typed result pattern:

- group;
- input;
- status;
- matched ID;
- match mode;
- entry;
- candidate IDs.

## REUSE-CAND-LIB-B02-03 — dictionary metadata maturity pattern

The explicit draft/projection/not-final metadata is a useful model for preventing premature production authority.

## REUSE-CAND-LIB-B02-04 — generated group projections

Group-specific projections can serve consumers that do not need the full combined dictionary, provided source direction remains clear.

---

# 25. Migration candidates

## MIG-CAND-LIB-B02-01 — mature version/adoption lifecycle

Current `version: 0.1` and `deprecated` status are primitives only.

Future target requires:

- revision identity;
- effective dates;
- supersedes/replaced-by;
- consumer adoption state;
- migration evidence.

## MIG-CAND-LIB-B02-02 — naming/profile system

Future migration from flat aliases toward profile-aware naming may be needed.

Current implementation must not be silently retrofitted without explicit contract design.

## MIG-CAND-LIB-B02-03 — consumer shadow dictionaries

Blueprint intent says consumers should not become independent dictionary authorities.

Cross-module shadow vocabularies should be discovered later and migrated deliberately.

No external module migration is authorized by this report.

---

# 26. Wrong-owner assessment

No confirmed wrong-owner business capability was found.

The dictionary contains operational-looking terms, but only as semantic references.

No evidence in Block 02 shows Library executing:

- order transitions;
- payment posting;
- stock updates;
- production state changes;
- CRM workflows.

Therefore:

`AUTHORITY_LEAKAGE_CONFIRMED=false`

---

# 27. Architecture fit

**Architecture generation fit:**

`BLUEPRINT_ALIGNED_DRAFT_SEMANTIC_LAYER_WITH_PRE_MATURE_PROFILE_SYSTEM`

Why:

- semantic ownership aligns with Blueprint;
- operational truth remains excluded;
- dictionary maturity is explicitly draft;
- ambiguity/deprecation primitives exist;
- consumer vocabulary centralization is represented;
- profile-aware naming and mature adoption/versioning are still absent.

---

# 28. Key maturity warnings for future assistants

Do not say:

> Library has a final shared operational dictionary.

Correct:

> Library has Shared Operational Dictionary v0.1 marked draft, unstable, projection-use and not-final-contract.

Do not say:

> `active` dictionary entries are production-final.

Correct:

> `active` is entry lifecycle inside the current draft dictionary.

Do not say:

> Dictionary IDs are globally unique.

Correct:

> Dictionary identity is group-scoped; the same ID may appear in multiple groups.

Do not say:

> Library owns order/payment/production state because it defines those statuses.

Correct:

> Library owns canonical vocabulary; domain owners own operational facts.

Do not say:

> Naming profiles are implemented.

Correct:

> Naming profiles/tokens/profile defaults are current Human Intent/roadmap targets and are not proven by Block 02.

Do not say:

> There is one unified reference-resolution status model.

Correct:

> Several related status vocabularies currently coexist and require reconciliation/mapping.

---

# 29. Uncertainty / reconciliation register

## UNC-LIB-B02-001 — Formal source authority of dictionary generator

**Severity:** MEDIUM

Observed generation direction is clear.

Formal document/edit authority is not yet reconciled.

Carry to L4/L5.

## UNC-LIB-B02-002 — Direct test linkage absent

**Severity:** MEDIUM

Tests likely exist but direct Block 02 packet linkage is missing.

Carry to L3/L5.

## UNC-LIB-B02-003 — Resolution status mapping

**Severity:** HIGH for future consumer work

Three related vocabularies need explicit relationship mapping before broad new integration.

## UNC-LIB-B02-004 — Naming/profile target absent

**Severity:** EXPECTED ROADMAP GAP

No current implementation.

## UNC-LIB-B02-005 — Localization completeness

**Severity:** LOW-MEDIUM

Schema-valid but many Ukrainian labels are not actually localized.

## UNC-LIB-B02-006 — Generic semantic facade maturity

**Severity:** LOW-MEDIUM

Current semantic package is thin and not a unified resolver.

## UNC-LIB-B02-007 — stale coordination exporter

**Severity:** HIGH if executed casually

Tracked source exists but should not be treated as current operational workflow.

---

# 30. Cross-block updates

## Block 01

Resolved:

`UNC-LIB-B01-001 — CatalogRegistry implementation source absent`

New status:

`RESOLVED_BY_BLOCK02_EVIDENCE`

The source implementation is now directly visible.

## Block 03

Requires later reconciliation for:

- Library Reference Contract status vocabulary;
- Contract Registry/adoption relation;
- downstream reference-resolution mapping.

## Block 04

Requires later reconciliation for:

- preview tool;
- generated projections;
- generation/export direction.

## Block 05

Requires later reconciliation for:

- dictionary validation CLI;
- direct pytest coverage;
- schema/validation test authority.

## Block 06

Requires later reconciliation for:

- stale dictionary coordination exporter;
- checkpoint-specific completion/status mutation.

## Block 07

Requires later reconciliation for:

- generated dictionary policy documents;
- document authority vs embedded script text.

---

# 31. Evidence-to-capability matrix

| Capability candidate | Current evidence | State | Confidence |
|---|---|---|---|
| Shared Operational Dictionary v0.1 | combined YAML + model/schema | VERIFIED_CURRENT_DRAFT_PROJECTION | HIGH |
| 18 group dictionaries | group YAMLs | VERIFIED_CURRENT_GENERATED_PROJECTION | HIGH |
| dictionary generator | export script | VERIFIED_CURRENT | HIGH |
| dictionary loading | loader.py | VERIFIED_CURRENT | HIGH |
| dictionary validation | validation.py | VERIFIED_CURRENT | HIGH |
| group-scoped resolution | resolver.py | VERIFIED_CURRENT | HIGH |
| ambiguity detection | resolver.py | VERIFIED_CURRENT_DETECTION_ONLY | HIGH |
| deprecated-reference recognition | resolver/model | VERIFIED_CURRENT_PRIMITIVE | HIGH |
| CatalogRegistry implementation | catalog/registry.py | VERIFIED_CURRENT / PRIMARY FIT BLOCK01 | HIGH |
| generic semantic alias normalization | semantic/aliases.py | CURRENT_THIN_PRIMITIVE | HIGH |
| semantic catalog resolver facade | semantic/resolver.py | CURRENT_THIN_FACADE | HIGH |
| naming profiles | none | NOT_PROVEN | HIGH |
| production tokens | none | NOT_PROVEN | HIGH |
| profile-specific defaults | none | NOT_PROVEN | HIGH |
| misspelling governance | none beyond explicit aliases | NOT_PROVEN_AS_SEPARATE_LAYER | HIGH |
| mature adoption/migration lifecycle | none | NOT_PROVEN | HIGH |
| final inventory unit system | explicitly excluded | NOT_IMPLEMENTED | HIGH |

---

# 32. L2 Block 02 disposition

## Analysis result

`L2_BLOCK_02=PASS_FOR_ANALYSIS`

## Knowledge result

`CURRENT_SHARED_DICTIONARY_AND_GROUP_RESOLUTION_CORE_CONFIRMED`

## Maturity result

`DRAFT_PROJECTION_NOT_FINAL_CONTRACT`

## Naming-profile result

`NAMING_PROFILE_IMPLEMENTATION_PROVEN=false`

## Production-token result

`PRODUCTION_TOKEN_IMPLEMENTATION_PROVEN=false`

## Authority result

`SEMANTIC_VOCABULARY_OWNERSHIP_ALIGNED_NO_BUSINESS_TRUTH_LEAKAGE`

## Direct test packet result

`DIRECT_RELATED_TEST_EVIDENCE=ABSENT_DUE_TO_L1_RELATIONSHIP_GAP`

## Implementation action created

`NONE`

## Source mutation

`NONE`

## Roadmap mutation

`NONE`

---

# 33. Carry-forward to L3

Carry provisional capabilities:

- shared operational dictionary;
- dictionary generator;
- group projections;
- loader;
- validator;
- group-scoped resolver;
- ambiguity detector;
- deprecated reference handling;
- generic semantic-normalization primitive;
- thin semantic resolver facade.

Carry cross-block correction:

- CatalogRegistry belongs primarily with catalog semantics and closes Block 01 source gap.

Carry unresolved semantic reconciliation:

- resolver-status layer mapping;
- alias-normalization duplication;
- generator authority;
- profile-aware future model.

Do not finalize stable capability IDs until all L2 blocks are complete.

---

# 34. Carry-forward to L4

Document authority review must include:

- dictionary policy docs;
- dictionary versioning policy;
- dictionary consumption policy;
- generator-embedded policy strings;
- shared dictionary maturity metadata;
- stale coordination completion report/status exporter.

Key question:

> Which artifact is current authority, and which is generated/supporting/historical?

---

# 35. Carry-forward to L5

Capability reconciliation must explicitly decide:

1. catalog normalization vs dictionary normalization vs semantic normalization;
2. catalog resolver vs dictionary resolver vs Reference Contract resolution status;
3. generator source vs generated YAML authority;
4. generic semantic facade responsibility;
5. profile-aware naming architecture;
6. deprecation/migration lifecycle;
7. whether group-scoped dictionary identity needs a formal reference type.

---

# 36. Next sequential block

Per L1 closeout order:

`03_contracts_cross_module_consumption`

Before moving forward, preserve this report as:

`tmp/module_knowledge_analysis/forprint_library/02_dictionaries_resolution_profiles/analysis_report.md`

Do not commit/push the temporary pilot analysis workspace yet.

---

# 37. Final statement

Block 02 proves that ForPrint Library already has a substantial shared semantic vocabulary and deterministic group-scoped resolution implementation.

The accurate current description is:

> Library owns a draft Shared Operational Dictionary v0.1 with 18 groups, 158 current semantic entries, generated group projections, schemas, validation, aliases and deterministic group-scoped resolution including ambiguity and deprecation handling. This is a semantic/reference layer only. It is not a final contract, operational state engine, final inventory-unit system, or naming-profile system.

The most important reconciliation requirement discovered here is that several overlapping resolution-status vocabularies and normalization surfaces currently coexist. Future integrations should not invent another variant before these are mapped during L5.

**Final L2 Block 02 status: `PASS_FOR_ANALYSIS_WITH_SEMANTIC_RECONCILIATION_CANDIDATES`.**
