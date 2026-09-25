# ForPrint Library — Module Knowledge Stabilization Pilot
## L4 Document / Artifact Authority Analysis Report

**Module:** `forprint_library`  
**Stage:** `L4 — Document / Artifact Authority Registry`  
**Library branch:** `feature/library-calculator-input-contract-v01`  
**Library HEAD:** `bba52bf6001f256a5c13ea7dbe175336b431754c`  
**Blueprint branch:** `audit/blueprint-inventory-refresh-2026-07-29`  
**Blueprint HEAD:** `b6ab9b65a2c27b70a574468caa8e3de4c3b454c5`  
**Library authority candidates classified:** `73`  
**Blueprint authority/context surfaces classified:** `9`  
**Registry records:** `82`  
**Source mutation:** `false`  
**Document rewrite:** `false`  
**Coordination repair:** `false`  
**Artifact regeneration:** `false`  
**Implementation authority:** `false`  
**Cleanup authority:** `false`  

---

# 1. Executive conclusion

L4 resolves the central Stage 2 question:

> which Library documents/artifacts are allowed to define current truth, which are generated
> from stronger sources, which are merely supporting/provenance surfaces, and which must be
> blocked from current-state claims.

The result is not one universal source of truth.

ForPrint Library has several distinct authority planes:

1. **Blueprint governance authority** for module role, ownership and non-ownership;
2. **Library implementation/data authority** for what is actually implemented inside that boundary;
3. **generated projections/artifacts** that inherit authority from generators/sources;
4. **supporting schemas/docs/fixtures/runbooks** that constrain, explain or validate bounded surfaces;
5. **planning context** that defines intended direction but no execution/release authority;
6. **historical provenance** that records completed decisions/checkpoints;
7. **stale/superseded surfaces** that must not be used as current-state truth;
8. **three unresolved high-risk authority conflicts** that must move to L5.

The highest-value L4 result is that several generation questions are now mechanically resolved.

No source cleanup is needed to know that:

- `catalog_seed_v0_1.yaml` feeds component catalog projections;
- catalog schema exporter code generates catalog schemas and the seed example;
- shared-dictionary exporter code contains current dictionary values/metadata and generates dictionary YAML/schema artifacts;
- dictionary-policy exporter code contains and overwrites policy documents.

The last item remains semantically dangerous: generation direction is known, but it is not yet established that embedded policy strings should remain the normative policy source.

**Final L4 result:**

`PASS_FOR_DOCUMENT_ARTIFACT_AUTHORITY_REGISTRY_WITH_L5_DECISIONS_READY`

---

# 2. Authority precedence established by L4

## Rank 1 — Blueprint current policy

Current Blueprint global/module policy governs:

- Library strategic role;
- ownership;
- non-ownership;
- ecosystem module boundaries;
- current governance constraints.

The strongest Library-specific current policy is:

`forprint_system_blueprint/coordination/module_policy/forprint_library/module_policy.md`

It is strategic authority, not blanket implementation authorization.

## Rank 2 — Current Library implementation/data sources

Inside that approved boundary, actual implemented behavior/data is proven by current implementation sources.

Examples:

- `catalog/seeds/catalog_seed_v0_1.yaml`;
- `catalog/configurable_products/business_card.yaml`;
- `app/forprint_library/calculator_input/contract.py`;
- `schemas/configurable_product.schema.yaml`;
- `schemas/reference_contract/library_reference.schema.yaml`;
- `schemas/reference_consumption/library_reference_consumption.schema.yaml`;
- current generator source code.

This does not permit local implementation to redefine ecosystem ownership.

## Rank 3 — Current manually authored machine schemas

A current manually authored schema may be a machine constraint for its bounded contract/pilot.

Where runtime code and schema coexist, normative precedence must remain explicit.

The principal unresolved example is Calculator Input v0.1.

## Rank 4 — Generated projections/artifacts

Generated outputs never outrank their source/generator.

This includes:

- component catalog YAML files;
- generated catalog schemas;
- generated seed example;
- shared operational dictionary YAML;
- generated dictionary schemas;
- generated dictionary-policy docs.

## Rank 5 — Supporting documents, fixtures and runbooks

These may explain current behavior or support validation.

They cannot override:

- Blueprint policy;
- executable/data source;
- current machine constraints.

## Rank 6 — Completion reports and ADRs

These are evidence/provenance.

They do not constitute rolling current state.

## Rank 7 — Human Intent and roadmap

These are planning context.

They may describe agreed/recovered future direction.

They do not grant execution/release authority.

## Rank 8 — stale/superseded surfaces

These are blocked from current-state claims.

---

# 3. Authority-class totals

| Authority class | Records |
|---|---:|
| `CONFLICT_REQUIRES_DECISION` | 3 |
| `CURRENT_AUTHORITY` | 4 |
| `CURRENT_IMPLEMENTATION_SOURCE` | 11 |
| `GENERATED_ARTIFACT` | 14 |
| `GENERATED_PROJECTION` | 5 |
| `HISTORICAL_PROVENANCE` | 8 |
| `PLANNING_CONTEXT` | 5 |
| `STALE` | 5 |
| `SUPERSEDED_CANDIDATE` | 3 |
| `SUPPORTING` | 24 |

Total registry records:

`82`

---

# 4. Catalog authority decision

## 4.1 Canonical draft semantic source

`catalog/seeds/catalog_seed_v0_1.yaml`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

Lifecycle:

`CURRENT_DRAFT_CANONICAL_SEED`

It remains explicitly:

- draft;
- unstable v0.1;
- allowed for projection use;
- not final production contract.

Therefore “canonical seed” does not mean “production-final contract.”

## 4.2 Component catalogs

The following are:

`GENERATED_PROJECTION`

- `catalog/materials.yaml`
- `catalog/product_families.yaml`
- `catalog/operations.yaml`
- `catalog/print_modes.yaml`
- `catalog/finishing_options.yaml`

Generation direction:

`catalog seed -> export_component_catalogs.py -> component YAMLs`

They are not independent human-edit authorities.

## 4.3 Catalog schemas

Generated by:

`scripts/export_catalog_schema_artifacts.py`

Classification:

`GENERATED_ARTIFACT`

Affected schemas:

- catalog seed;
- material;
- product family;
- operation;
- print mode;
- finishing option.

The same generator also produces:

`examples/catalog_seed_v0_1.example.yaml`

Therefore manual edits to those generated outputs are not an authoritative workflow.

## 4.4 Configurable product schema

`schemas/configurable_product.schema.yaml`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

No generator in the L4 evidence establishes it as generated.

---

# 5. Shared dictionary authority decision

## 5.1 Dictionary exporter code

`scripts/export_shared_operational_dictionaries.py`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

More precisely:

`CURRENT_GENERATOR_AND_EMBEDDED_DATA_SOURCE`

It currently contains:

- `DICTIONARY_VALUES`;
- aliases;
- deprecated-value declarations;
- metadata;
- entry construction;
- schema construction.

It generates:

- `dictionaries/shared_operational_dictionary_v0_1.yaml`;
- group dictionary YAML files;
- `schemas/dictionary_entry.schema.yaml`;
- `schemas/shared_operational_dictionary.schema.yaml`.

## 5.2 Generated dictionary YAML/schema outputs

Classification:

`GENERATED_ARTIFACT`

They are valid current generated reference artifacts.

They are not independent edit authority.

## 5.3 Domain ownership caveat

This L4 classification determines **where current repository values are generated from**.

It does not decide whether Library should permanently own every foreign-domain operational status.

That remains L5 capability/ownership reconciliation.

---

# 6. Dictionary policy authority decision

`scripts/export_dictionary_policy_docs.py`

contains complete policy text and writes architecture policy files.

Therefore generation direction is resolved.

Generator:

`CONFLICT_REQUIRES_DECISION`

Generated policy docs:

`GENERATED_ARTIFACT`

This is intentionally asymmetric.

Why:

- the script is mechanically authoritative for overwriting those files;
- the evidence does not establish that embedded strings are the correct durable semantic-policy authority;
- future Blueprint/domain-owner reconciliation may change ownership/content;
- running the exporter now could erase manually improved policy text.

Therefore:

`DO_NOT_RUN_DICTIONARY_POLICY_EXPORTER_CASUALLY`

until L5 decides the durable authority model.

---

# 7. Business Card authority decision

`catalog/configurable_products/business_card.yaml`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

It is the current Library semantic/reference definition for:

`product.business_card`

Its role is bounded:

- product semantic identity;
- parameter definitions;
- Library references;
- allowed reference choices;
- consumer boundary metadata.

It is not:

- Calculator pricing truth;
- order truth;
- stock truth;
- production truth.

Business Card runbook:

`SUPPORTING`

Business Card recovery document:

`STALE`

because it contains an obsolete branch assumption.

Business Card completion report:

`HISTORICAL_PROVENANCE`

because it is checkpoint evidence, not rolling module state.

---

# 8. Calculator Input authority decision

## 8.1 Runtime implementation

`app/forprint_library/calculator_input/contract.py`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

It currently defines implemented runtime behavior for:

- supported product;
- schema version constant;
- normalization;
- error taxonomy;
- deterministic configuration ID;
- reference validation;
- no-monetary-field enforcement.

## 8.2 Machine schema

`schemas/calculator_input/calculator_input_envelope.schema.yaml`

Classification:

`SUPPORTING`

Lifecycle:

`CURRENT_MACHINE_CONTRACT_SCHEMA`

It is a current machine constraint, but L4 intentionally does not declare it superior to runtime code.

L5 must decide:

`runtime implementation vs machine schema normative precedence`

and define the drift gate.

## 8.3 Fixtures

Calculator fixtures are:

`SUPPORTING / CURRENT_DETERMINISTIC_FIXTURE`

They may lock deterministic behavior and validate compatibility.

They are not product semantic truth.

## 8.4 Completion evidence

Latest Calculator completion report:

`SUPPORTING / CURRENT_MODULE_SIDE_COMPLETION_EVIDENCE`

It proves:

`READY_FOR_BLUEPRINT_REVIEW`

It does not prove:

`BLUEPRINT_ACCEPTED`

---

# 9. Generic Reference Contract authority decision

`schemas/reference_contract/library_reference.schema.yaml`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

for the current generic reference-foundation payload shape.

`examples/reference_contract/library_reference_examples.yaml`

Classification:

`SUPPORTING`

and explicitly non-production.

`schemas/reference_consumption/library_reference_consumption.schema.yaml`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

for the bounded local consumption pilot only.

Consumption examples:

`SUPPORTING`

No L4 surface proves live downstream adoption.

The relationship among:

- generic Library Reference Contract;
- Reference Consumption Pilot;
- specialized Calculator Input;
- `ContractVersion`;
- Contract Registry

remains an L5 decision.

---

# 10. ContractVersion authority conflict

`app/forprint_library/contracts/models.py`

Classification:

`CONFLICT_REQUIRES_DECISION`

Reason:

It contains local:

- contract identity;
- lifecycle status;
- effective/deprecated/blocked dates;
- machine/human changelog;
- migration rules;
- historical compatibility.

Those concerns overlap the Blueprint direction for:

`forprint_contract_registry`

The file is real current code.

But current portfolio architecture does not establish Library as the cross-module contract lifecycle registry.

Therefore a future assistant must not infer:

`this code exists -> Library owns Contract Registry responsibilities`

L5 must map retained Library-local semantics vs Registry-owned lifecycle/adoption authority.

---

# 11. Coordination authority decision

## 11.1 Current prompt navigation

Current sequencing/navigation authority:

`Blueprint Prompt Queue`

Local:

`coordination/prompts/active/current_blueprint_prompt.md`

is:

`SUPPORTING / CURRENT_LOCAL_MIRROR`

It may be used for local prompt content after verifying queue/currentness.

## 11.2 Old prompts under active/

Older prompt copies under `active/` are:

`HISTORICAL_PROVENANCE`

Their directory name does not make them current.

## 11.3 Local prompt index

`coordination/prompts/index.yaml`

Classification:

`STALE`

It contains an old empty received-prompts state despite later prompt work.

It must not be used for current sequencing.

---

# 12. Current-status authority decision

The following are:

`STALE`

- `coordination/status/current_status.md`
- `coordination/status/current_status.yaml`
- `coordination/status/next_questions_for_blueprint.md`

They stop at Business Card or contain still older mixed state while the repository is already on the Calculator Input branch/front.

Assistant visibility:

`BLOCK_CURRENT_STATE_CLAIMS`

Current truth should instead be reconstructed from:

- Git;
- current Prompt Queue/mirror;
- latest completion evidence;
- authoritative Blueprint lifecycle evidence.

L5 should define one deterministic current-status derivation rather than another manual patch.

---

# 13. Reports-index authority decision

`coordination/reports/index.yaml`

Classification:

`CONFLICT_REQUIRES_DECISION`

Reason:

It contains multiple index generations in one file.

It mixes:

- older `completion_reports`;
- older `commit_reports`;
- later `schema_version`;
- later `reports`.

It does not represent a normalized current lifecycle index.

Assistant visibility:

`BLOCK_CURRENT_STATE_CLAIMS`

Historical entries remain useful.

---

# 14. Blueprint awareness and standards snapshots

`document_review_ledger.yaml`

Classification:

`SUPPORTING`

Role:

provenance of acknowledged/applied documents at recorded hashes.

It cannot prove those Blueprint documents remain unchanged/current.

`blueprint_standards_available_snapshot.txt`

Classification:

`SUPPORTING`

Role:

point-in-time standards awareness snapshot.

Live Blueprint standards remain authoritative.

---

# 15. Documentation authority decision

## Root README

Classification:

`SUPERSEDED_CANDIDATE`

Blocked for current architecture claims.

It describes an old standalone FastAPI/ChangeManifest/MigrationGraph architecture not established at current HEAD.

## Architecture README

Classification:

`SUPERSEDED_CANDIDATE`

Same reason at architecture level.

## Alias / canonical ID / catalog-seed / Library-boundary docs

Classification:

`SUPPORTING`

They remain useful and broadly aligned.

They do not outrank current Blueprint policy or implementation/data sources.

## ADRs

Classification:

`HISTORICAL_PROVENANCE`

Their local Accepted status is preserved as historical decision evidence.

Current applicability must be mapped to current Blueprint architecture.

## Semantic readiness doc

Classification:

`HISTORICAL_PROVENANCE`

Later reference/contract layers are stronger current evidence.

## Calculator architecture/runbook/recovery

Classification:

`SUPPORTING`

Current and useful, subject to executable/schema/test freshness.

---

# 16. Semantic preview decision

`examples/semantic_reference_preview.yaml`

Classification:

`SUPERSEDED_CANDIDATE`

It is an early demo/reference surface and must not become canonical semantic truth.

This classification does not authorize deletion.

L8 may later decide its disposition after L5 reconciliation.

---

# 17. Makefile authority decision

`Makefile`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

but only for its operator/workflow scope.

It is:

- the current operator-facing functional map;
- a supported command surface.

It is not:

- semantic/catalog truth;
- business-state truth;
- Blueprint authority.

Some targets/composites mutate reports or coordination state.

Therefore L5/quality reconciliation should distinguish:

- read-only checks;
- synchronization;
- publishing/report mutation;
- cleanup.

---

# 18. Project/tool configuration

`pyproject.toml`

Classification:

`CURRENT_IMPLEMENTATION_SOURCE`

for current package/tool configuration.

It is the relevant current configuration surface for tools configured there.

It does not prove those tools were freshly executed at current HEAD.

---

# 19. Blueprint authority surfaces

## Module Policy

`CURRENT_AUTHORITY`

for Library strategic role, ownership and non-ownership.

## Project doctrine

`CURRENT_AUTHORITY`

for ecosystem-wide architectural doctrine.

## Ecosystem module map

`CURRENT_AUTHORITY`

for module-role/topology context.

## Current execution focus

`CURRENT_AUTHORITY`

for Blueprint execution scheduling/focus only.

It is not proof of Library semantic implementation.

## Human Intent

`PLANNING_CONTEXT`

Explicitly not release authority.

## Portfolio roadmaps

`PLANNING_CONTEXT`

They are planning-only and grant no execution authority.

## Deterministic Worker Promotion policy

`PLANNING_CONTEXT`

It is canonical planning policy with `execution_authority=false`.

---

# 20. Assistant visibility restrictions

The following surfaces are explicitly blocked from current-state claims:

- `README.md`
- `coordination/prompts/index.yaml`
- `coordination/reports/index.yaml`
- `coordination/status/current_status.md`
- `coordination/status/current_status.yaml`
- `coordination/status/next_questions_for_blueprint.md`
- `docs/architecture/README.md`
- `docs/operations/business_card_skeleton_recovery.md`
- `examples/semantic_reference_preview.yaml`

In addition, these require higher-authority verification before use:

- local current prompt mirror;
- standards snapshot;
- generated dictionary policy documents;
- dictionary policy exporter;
- old/current mixed contract lifecycle models where Contract Registry ownership matters.

---

# 21. L5 required decisions

L4 has intentionally **not** collapsed architecture questions into document classification.

L5 must decide:

1. Calculator runtime vs schema normative precedence.
2. Calculator Input vs generic Library Reference Contract relationship.
3. Local `ContractVersion` vs Contract Registry ownership boundary.
4. Dictionary-policy generator semantic authority.
5. Foreign-domain status dictionary ownership/mapping.
6. Resolution-status vocabulary mapping.
7. Generic reference example IDs vs current catalog IDs.
8. Prompt Queue/current mirror/local archive lifecycle.
9. Deterministic derivation of current status.
10. Normalized reports-index model.
11. Blueprint acceptance event representation.
12. Generated-artifact drift gates.
13. Human-edit workflow for catalog/dictionary sources.

---

# 22. What L4 resolved vs did not resolve

## Resolved

- source/projection direction for component catalogs;
- source/generation direction for catalog schemas/example;
- source/generation direction for shared dictionaries/schemas;
- generated nature of dictionary policy documents;
- current role of product.business_card source;
- current runtime role of Calculator contract.py;
- local prompt mirror vs Prompt Queue hierarchy;
- stale status surfaces;
- stale/mixed reports index;
- old README/architecture generation;
- supporting/provenance role of completion reports and ADRs;
- planning-only nature of Human Intent/roadmap.

## Not resolved by design

- cross-contract unification;
- domain status ownership;
- Contract Registry adoption;
- schema-vs-code canonical precedence;
- policy-source redesign;
- current-status implementation;
- cleanup/deletion/migration;
- roadmap distribution;
- new feature implementation.

Those belong to later stages.

---

# 23. L4 disposition

```text
MODULE=forprint_library
STAGE=L4_DOCUMENT_ARTIFACT_AUTHORITY

LIBRARY_CANDIDATES_CLASSIFIED=73
BLUEPRINT_CONTEXT_SURFACES_CLASSIFIED=9
REGISTRY_RECORDS=82

CURRENT_AUTHORITY=4
CURRENT_IMPLEMENTATION_SOURCE=11
GENERATED_PROJECTION=5
GENERATED_ARTIFACT=14
SUPPORTING=24
PLANNING_CONTEXT=5
HISTORICAL_PROVENANCE=8
STALE=5
SUPERSEDED_CANDIDATE=3
CONFLICT_REQUIRES_DECISION=3

SOURCE_MUTATION=false
DOCUMENT_REWRITE=false
COORDINATION_REPAIR=false
ARTIFACT_REGENERATION=false
CLEANUP_AUTHORITY=false
IMPLEMENTATION_AUTHORITY=false

RESULT=PASS_FOR_DOCUMENT_ARTIFACT_AUTHORITY_REGISTRY_WITH_L5_DECISIONS_READY
NEXT=L5_CAPABILITY_RECONCILIATION
```

---

# 24. Final statement

L4 converts Library from a repository containing many apparently competing files into an explicit authority model.

The most important rule for future work is now:

> **never infer authority from file existence, directory name, “Accepted” wording, or a green historical report alone.**

Use:

- current Blueprint policy for role/ownership;
- current implementation/data sources for actual implemented behavior;
- generator/source relationships for generated artifacts;
- supporting docs/fixtures only within their bounded role;
- provenance surfaces only for history/evidence;
- planning surfaces only for intended direction;
- stale/superseded surfaces never for current-state truth.

The module is now ready for L5 capability reconciliation without guessing which artifact is normative.

**Final L4 status:**

`PASS_FOR_DOCUMENT_ARTIFACT_AUTHORITY_REGISTRY_WITH_L5_DECISIONS_READY`
