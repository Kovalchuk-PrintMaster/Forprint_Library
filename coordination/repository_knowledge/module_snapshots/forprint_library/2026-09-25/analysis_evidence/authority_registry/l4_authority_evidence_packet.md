# ForPrint Library — Module Knowledge Stabilization Pilot
## L4 Document / Artifact Authority Evidence Packet

- Library branch: `feature/library-calculator-input-contract-v01`
- Library HEAD: `bba52bf6001f256a5c13ea7dbe175336b431754c`
- Library upstream: `bba52bf6001f256a5c13ea7dbe175336b431754c`
- Blueprint branch: `audit/blueprint-inventory-refresh-2026-07-29`
- Blueprint HEAD: `b6ab9b65a2c27b70a574468caa8e3de4c3b454c5`
- Library authority candidate files: **73**

## Boundary

This packet authorizes classification/reconciliation analysis only.

It does not authorize source edits, document rewrites, prompt/status repairs,
artifact regeneration, cleanup, migrations, roadmap changes, Blueprint writes,
or new capability implementation.

## L4 objective

For every important document/artifact surface, determine what it is allowed
to mean and how much authority a future assistant/operator may assign to it.

Required authority classes include:

- `CURRENT_AUTHORITY`
- `CURRENT_IMPLEMENTATION_SOURCE`
- `GENERATED_PROJECTION`
- `GENERATED_ARTIFACT`
- `SUPPORTING`
- `PLANNING_CONTEXT`
- `HISTORICAL_PROVENANCE`
- `STALE`
- `SUPERSEDED_CANDIDATE`
- `CONFLICT_REQUIRES_DECISION`

L4 must not silently delete, rewrite or repair any candidate.

---

# A. L3 synthesis basis

### `tmp/module_knowledge_analysis/forprint_library/synthesis/l3_capability_synthesis_report.md`

- SHA256: `8bf95e7343852259d7af2df4d41b0f3ddd7372cf5eb2b9bdf381178907223cba`
- Bytes: `41304`

```markdown
# ForPrint Library — Module Knowledge Stabilization Pilot
## L3 Capability Synthesis Report

**Module:** `forprint_library`  
**Stage:** `L3 — Capability Synthesis`  
**Library branch:** `feature/library-calculator-input-contract-v01`  
**Library HEAD:** `bba52bf6001f256a5c13ea7dbe175336b431754c`  
**Blueprint branch:** `audit/blueprint-inventory-refresh-2026-07-29`  
**Blueprint HEAD:** `b6ab9b65a2c27b70a574468caa8e3de4c3b454c5`  
**L2 block reports synthesized:** `8`  
**Source mutation:** `false`  
**Tests executed by L3:** `false`  
**Make executed by L3:** `false`  
**Roadmap mutation:** `false`  
**Implementation authority:** `false`  
**Cleanup authority:** `false`  

---

# 1. Executive synthesis

ForPrint Library already contains a meaningful current implementation core.

The strongest current module capabilities are:

1. a Library-owned draft canonical catalog/reference layer;
2. a Shared Operational Dictionary v0.1 with deterministic group-scoped resolution;
3. a controlled configurable-product reference for Business Cards;
4. a deterministic, typed, versioned, read-only Library → Calculator Input Contract v0.1;
5. a generic Library Reference Contract foundation and bounded Reference Consumption Pilot;
6. generated projection/schema/example tooling;
7. substantial automated validation and test coverage;
8. a modern Blueprint-aware operator/governance layer built around Prompt Queue, standards/document awareness and completion validation.

The module is therefore **not** merely a documentation repository or early empty scaffold.

At the same time, the current implementation is narrower than the full Blueprint target state.

The dominant unfinished work is not “build everything that the roadmap mentions.”
The dominant work is:

> reconcile authority, generation direction, lifecycle semantics and current-state projections before broadening implementation.

Across L2, the same pattern appears repeatedly:

- strong current local implementation;
- explicit draft/bounded maturity;
- good ownership boundaries;
- parallel or historical surfaces accumulated around it;
- no single normalized authority model across all surfaces.

The most important L3 conclusion is:

> Library has a viable semantic/reference/contract core. Its highest-risk debt is knowledge/governance normalization, not missing foundational implementation.

Therefore no broad rewrite, cleanup, migration or new cross-module contract expansion should start from L3.

---

# 2. Module role synthesized from current evidence

Current Blueprint and implementation evidence support the following module role:

> `forprint_library` is the ForPrint semantic/catalog/reference authority and shared-definition publication owner. It defines stable semantic identities, aliases, reference vocabularies, bounded shared contract definitions and selected shared publication surfaces. It does not own domain operational facts or foreign-domain runtime business logic.

## 2.1 Current confirmed ownership

Current implementation strongly supports Library ownership of:

- product-family semantics;
- material semantics;
- operation semantics;
- print-mode semantics;
- finishing-option semantics;
- canonical/reference IDs;
- aliases;
- shared operational vocabulary/reference semantics;
- semantic lookup/resolution primitives;
- configurable-product semantic/reference structure;
- Library → Calculator reference-input contract definition;
- generic Library-reference contract definitions;
- semantic boundary rules for downstream consumers.

## 2.2 Explicit non-ownership

Current evidence consistently excludes Library ownership of:

- Calculator pricing/calculation truth;
- operational orders;
- client/customer database truth;
- accounting/payment truth;
- warehouse stock truth;
- production runtime;
- CRM workflow;
- Telegram runtime behavior;
- 1C posting/synchronization truth;
- downstream module business rules.

## 2.3 Blueprint-owned future scope not yet proven current

Blueprint/Human Intent also assigns or proposes Library responsibility for:

- service catalog semantics;
- naming profiles;
- common misspelling governance;
- production tokens and profile-specific defaults;
- calibration profiles;
- SOP/instruction/media knowledge;
- shared UI design-system publication;
- reusable UI component catalog;
- semantic/capability discovery registry;
- external catalog ingestion provenance;
- historical/reference asset semantics;
- mature version/adoption/deprecation lifecycle.

These are not automatically current capabilities merely because they are in policy, Human Intent or roadmap.

---

# 3. L3 capability families

L3 consolidates numerous L2 capability candidates into nine substantive capability families plus one non-capability structural class.

Stable IDs below are **L3 synthesis IDs**, not yet final public Module Knowledge Base IDs.

---

## CAP-LIB-L3-01 — Canonical semantic catalog/reference core

**Maturity:** `CURRENT_IMPLEMENTED_DRAFT_REFERENCE`  
**Confidence:** HIGH  
**Primary L2 sources:** B01, B02, B04, B05  
**Current architecture fit:** Blueprint-aligned

### Includes

- combined catalog seed v0.1;
- five semantic domains:
  - materials;
  - product families;
  - operations;
  - print modes;
  - finishing options;
- current catalog loaders;
- catalog structural/semantic validation;
- `CatalogRegistry`;
- ID lookup;
- alias lookup;
- current catalog schemas;
- generated component projections.

### Current maturity

The catalog remains explicitly:

- draft canonical seed;
- unstable v0.1;
- projection-use;
- not final contract.

Current seed population:

`28` draft entries.

### Important synthesis resolution

L2 B04 resolves the generation direction:

`catalog seed -> component catalog projections`

Therefore the five component catalog YAMLs should not be synthesized as five independent authorities.

### Open authority question

Formal human-edit/source authority of:

- seed;
- exporter;
- committed generated component files

remains an L4 question.

---

## CAP-LIB-L3-02 — Shared dictionary and deterministic resolution core

**Maturity:** `CURRENT_IMPLEMENTED_DRAFT_REFERENCE`  
**Confidence:** HIGH  
**Primary L2 sources:** B02, B05  
**Current architecture fit:** Blueprint-aligned semantic layer

### Includes

- Shared Operational Dictionary v0.1;
- 18 group dictionaries;
- dictionary generator;
- loader/enumeration;
- structural validation;
- group-scoped resolver;
- ambiguity detection;
- deprecated-reference recognition;
- generic alias-normalization helper;
- thin semantic resolver facade.

### Current population

- 18 dictionary groups;
- 158 entries;
- 156 active entries;
- 2 deprecated entries.

Important:

`active` is entry lifecycle inside a draft dictionary.

It does not mean the overall dictionary contract is production-final.

### Identity rule

Stable dictionary identity is effectively:

`(dictionary_group, id)`

not globally:

`id`

### Current maturity gap

The module does not yet prove:

- naming profiles;
- device/equipment profiles;
- production-token grammar;
- profile-specific defaults;
- governed misspelling layer;
- profile-aware ambiguity;
- mature migration/supersession.

---

## CAP-LIB-L3-03 — Configurable product reference model

**Maturity:** `CURRENT_IMPLEMENTED_DRAFT_REFERENCE`  
**Confidence:** HIGH  
**Primary L2 sources:** B01, B03, B04, B05

### Current implementation

Controlled configurable product:

`product.business_card`

with:

- product identity;
- bilingual names;
- aliases;
- typed/structured parameters;
- Library-owned semantic references;
- consumer-owned selected values/context;
- explicit no-pricing/no-stock/no-order/no-runtime boundaries.

### Role

This is a semantic/reference product-card pattern.

It is not:

- full production catalog;
- product authoring UI;
- pricing engine;
- order object;
- stock object;
- production runtime.

### Reuse candidate

The Business Card pattern is a useful future configurable-product reference pattern, but mass expansion should wait for L5 reconciliation of:

- contract relationships;
- schema authority;
- consumer adoption model;
- catalog lifecycle.

---

## CAP-LIB-L3-04 — Deterministic Calculator input projection

**Maturity:** `CURRENT_IMPLEMENTED_EXECUTABLE_SPECIALIZED_CONTRACT`  
**Confidence:** HIGH  
**Primary L2 sources:** B03, B04, B05, B06, B07

### Current contract

`forprint_library_calculator_input_contract_v0_1`

Current product support:

`product.business_card`

Current envelope:

`calculator_input_envelope_v0_1`

### Proven characteristics

- deterministic;
- typed;
- schema-versioned;
- read-only;
- side-effect constrained;
- stable normalization;
- stable configuration identity;
- typed error taxonomy;
- no monetary fields;
- no Calculator pricing logic;
- no filesystem/network dependency during projection.

### Lifecycle status

Current evidence proves:

`IMPLEMENTED_AND_MODULE_COMPLETED_READY_FOR_BLUEPRINT_REVIEW`

Current Blueprint acceptance:

`NOT_PROVEN`

### Important architectural issue

This specialized contract does not currently use the generic `library_reference_v0_2` envelope as its substrate.

It is a parallel specialized contract layer.

---

## CAP-LIB-L3-05 — Generic Library reference-contract foundation

**Maturity:** `CURRENT_FOUNDATIONAL_AND_PILOT`  
**Confidence:** HIGH for artifacts; MEDIUM-HIGH for adoption  
**Primary L2 sources:** B03, B04, B05, B07

### Includes

- Library Reference Contract v0.2 schema;
- reference examples;
- Reference Consumption Pilot v0.3;
- consumer-boundary validation;
- deprecation/manual-review semantics;
- generic `Contract` / `ContractVersion` source model.

### Current strengths

- semantic/reference-only boundary;
- explicit downstream ownership preservation;
- positive and negative consumer examples;
- deprecation/manual-review concepts;
- version/lifecycle primitives.

### Current limitations

Not proven:

- Contract Registry runtime;
- cross-module adoption registry;
- subscriber freshness;
- rollout modes;
- actual migration graph;
- production consumer adoption;
- full binding to current catalog IDs.

### Namespace issue

Older/foundation examples use IDs different from the current catalog/configurable-product namespace.

This remains a high-priority L5 reconciliation problem.

---

## CAP-LIB-L3-06 — Generated projection, schema and fixture layer

**Maturity:** `CURRENT_SUPPORTING_GENERATED_LAYER`  
**Confidence:** HIGH  
**Primary L2 sources:** B04, B05, B07

### Includes

- component catalog exporter;
- catalog schema exporter;
- generated component catalogs;
- generated schema artifacts;
- generated catalog example;
- Calculator deterministic fixtures;
- dictionary demo fixtures;
- Reference Contract examples;
- Reference Consumption fixtures;
- illustrative Business Card consumer examples;
- semantic reference demo/preview.

### Important authority distinction

These artifact roles are not equivalent.

L3 preserves:

- `DETERMINISTIC_FIXTURE`;
- `VALIDATION_FIXTURE`;
- `GENERATED_EXAMPLE`;
- `ILLUSTRATIVE_USAGE_EXAMPLE`;
- `DEMO_PREVIEW`;
- `GENERATED_PROJECTION`.

Generated/supporting artifacts do not become canonical truth merely because they are committed.

### Current quality gap

Generated-artifact drift protection is not proven as one canonical generate-and-diff gate.

---

## CAP-LIB-L3-07 — Validation and quality surface

**Maturity:** `CURRENT_SUBSTANTIAL_WITH_FRESHNESS_AND_MUTATION_DEBT`  
**Confidence:** HIGH  
**Primary L2 source:** B05, supported by B01–B04/B06

### Includes

- pytest configuration;
- Ruff;
- strict mypy configuration;
- `run_library_checks.py`;
- catalog validation CLI;
- Blueprint visibility checks;
- content tests;
- contract tests;
- integration tests;
- coordination/closure tests;
- boundary tests;
- Make/operator surface tests.

### Strong behavioral coverage

Current test source provides strong proof for:

- catalog validation;
- stable IDs;
- aliases;
- dictionary semantics;
- ambiguity/deprecation;
- Business Card semantics;
- generic reference contracts;
- consumer boundaries;
- Calculator input determinism;
- no-write/no-network/no-monetary boundary;
- completion validation.

### Important limitations

L3 does not claim fresh current-HEAD test execution.

The checked-in Library check report is stale point-in-time evidence.

The report runner mutates tracked reports.

Nested warning propagation is incomplete.

Generated-artifact drift protection is not proven.

Therefore:

`TEST_SURFACE_STRONG`

but:

`ONE_CLEAN_CURRENT_HEAD_READ_ONLY_QUALITY_TRUTH = false`

---

## CAP-LIB-L3-08 — Blueprint-aware governance and operator surface

**Maturity:** `CURRENT_IMPLEMENTED_WITH_TRANSITIONAL_COORDINATION_STATE`  
**Confidence:** HIGH  
**Primary L2 source:** B06, supported by B03/B05/B07

### Current capabilities

- Blueprint Prompt Queue navigation;
- prompt dashboard;
- next-prompt resolution;
- current prompt local mirroring;
- directive sync;
- standards awareness;
- document awareness;
- context bundles;
- coordination metadata check/fix;
- governance composite workflows;
- module lifecycle workflows;
- completion packet validation;
- module-side completion reporting;
- document-awareness ledger;
- Makefile as operator-facing functional map.

### Current authority hierarchy

`Blueprint Prompt Queue`

is the current prompt sequencing/navigation authority.

Local `current_blueprint_prompt.md` is a synchronized mirror/provenance surface.

Local `prompts/index.yaml` is transitional directive-import metadata, not Prompt Queue authority.

### Current debt

- `active/` contains multi-era prompt files;
- `current_status.*` is stale;
- `next_questions_for_blueprint.md` is stale;
- reports index is mixed-schema and stale;
- completion packet contains older internal workflow metadata;
- some Makefile composites mutate state;
- redundant prompt/sync paths exist;
- document-awareness freshness is not fully proven;
- module manifest lifecycle metadata is stale/mixed.

### Synthesis

The governance layer is best described as:

`STRONG_OPERATOR_WORKFLOW + STRONG_PROVENANCE + WEAK_CURRENT_STATE_NORMALIZATION`

---

## CAP-LIB-L3-09 — Documentation and architecture knowledge layer

**Maturity:** `MULTI_GENERATIONAL_SUPPORTING_WITH_AUTHORITY_DEBT`  
**Confidence:** HIGH  
**Primary L2 source:** B07

### Current positive state

Library has substantial useful documentation for:

- semantic boundaries;
- canonical IDs;
- aliases;
- catalog maturity;
- dictionary usage;
- reference contracts;
- Business Card;
- Calculator input;
- runbooks/recovery.

### Architecture generations

At least four generations coexist.

### Strongest current concern

Root `README.md` and `docs/architecture/README.md` represent an older broader architecture generation and should not be assumed current.

Dictionary-policy docs have generator/source-authority ambiguity.

Local ADR acceptance must be mapped to current Blueprint architecture.

Runbooks contain freshness gaps.

### Synthesis

Documentation debt is primarily:

- authority;
- freshness;
- supersession;
- generation provenance;
- current-vs-historical role classification.

It is not evidence that the working semantic core is invalid.

---

## STRUCT-LIB-L3-01 — Python package scaffolding

**Capability:** false  
**Currentness:** current structural file  
**Primary source:** B10

`app/forprint_library/__init__.py`

is:

`TECHNICAL_SCAFFOLDING`

It must be excluded from substantive capability counts.

Disposition:

`KEEP`

---

# 4. Capability maturity summary

| L3 ID | Capability family | Maturity | Current implementation | Main blocker/debt |
|---|---|---|---|---|
| CAP-LIB-L3-01 | semantic catalog/reference core | draft/current | yes | lifecycle + formal generated authority |
| CAP-LIB-L3-02 | shared dictionary/resolution | draft/current | yes | status mapping + naming/profile gap |
| CAP-LIB-L3-03 | configurable product reference | draft/current | yes | scale/adoption model |
| CAP-LIB-L3-04 | Calculator input projection | executable/current | yes | Blueprint acceptance + contract unification |
| CAP-LIB-L3-05 | generic reference contracts | foundation/pilot | partial | namespace + Registry/adoption |
| CAP-LIB-L3-06 | generated artifacts/fixtures | supporting/current | yes | drift/source authority |
| CAP-LIB-L3-07 | quality/validation | substantial/current | yes | current-head read-only truth |
| CAP-LIB-L3-08 | governance/operator | substantial/current | yes | stale/transitional coordination projections |
| CAP-LIB-L3-09 | docs/architecture knowledge | supporting/multi-era | yes | authority/freshness |
| STRUCT-LIB-L3-01 | package scaffolding | structural | yes | none |

---

# 5. Cross-capability dependency map

## 5.1 Current semantic path

```text
catalog seed
    |
    +--> catalog loader / validator
    |
    +--> CatalogRegistry / alias lookup
    |
    +--> generated component catalog projections
    |
    +--> configurable product.business_card
             |
             +--> Calculator Input Contract v0.1
                     |
                     +--> deterministic Calculator fixtures
```

## 5.2 Current dictionary path

```text
dictionary generator definitions
    |
    +--> Shared Operational Dictionary v0.1
            |
            +--> group dictionary projections
            |
            +--> dictionary loader / validator
            |
            +--> group-scoped resolver
                    |
                    +--> ambiguity detection
                    +--> deprecated reference recognition
```

## 5.3 Generic reference-contract path

```text
Library Reference Contract v0.2
    |
    +--> controlled reference examples
    |
    +--> Reference Consumption Pilot v0.3
            |
            +--> consumer-boundary validation fixtures
```

This path is currently parallel to, not formally composed with, Calculator Input v0.1.

## 5.4 Cross-cutting quality path

```text
catalog / dictionary / contracts / fixtures / governance surfaces
    |
    +--> validators
    +--> pytest
    +--> integration tests
    +--> boundary tests
    +--> run_library_checks.py
```

## 5.5 Governance lifecycle path

```text
Blueprint Prompt Queue / module policy / Human Intent
    |
    +--> local prompt mirror / standards / document awareness
    |
    +--> module implementation
    |
    +--> module-side completion report / completion packet validation
    |
    +--> Blueprint acceptance
```

Important:

`module-side completion != Blueprint acceptance`

---

# 6. External dependency/consumer synthesis

## 6.1 Contract Registry

The most important architecture dependency.

Current state:

`DEPENDENCY_PRESENT_IN_BLUEPRINT`

Current Library integration:

`NOT_PROVEN`

Role to reconcile:

- Library owns semantic/contract definitions;
- Contract Registry is expected to govern interface/version/adoption lifecycle across modules.

Exact boundary remains L5 work.

## 6.2 Calculator Engine

Strongest current concrete Library consumer contract.

Current:

- deterministic input envelope implemented;
- pricing remains Calculator-owned;
- live runtime integration not implied.

## 6.3 Telegram Bot

Current evidence supports semantic/reference usage/hints only.

Live integration/adoption not proven.

## 6.4 Operational Registry

May persist Library IDs as foreign semantic metadata.

Library does not own operational state.

## 6.5 Accounting Registry

May map/reference semantic definitions.

Library does not own accounting/payment truth.

## 6.6 Prepress Hub

May consume semantic/reference definitions.

Library does not own prepress runtime/execution truth.

## 6.7 Warehouse

Blueprint target requires stable lookup contracts, but current Warehouse-specific adoption is not proven.

## 6.8 Website / shared UI consumers

Blueprint/Human Intent assigns Library shared UI publication responsibility.

Current implementation of a shared UI package/catalog is not proven.

---

# 7. Authority and conflict register

## AUTH-LIB-L3-001 — Catalog seed vs component catalogs

**Status:** `TRANSFORMATION_DIRECTION_RESOLVED / FORMAL_EDIT_AUTHORITY_OPEN`

Resolved:

`seed -> generated component projections`

Open:

Which file/process is the declared human-edit authority?

L4.

---

## AUTH-LIB-L3-002 — Schema exporter code vs committed schema YAML

**Status:** `OPEN_HIGH`

Exporter code generates schema YAML.

Need one explicit normative source/edit workflow.

L4/L5.

---

## AUTH-LIB-L3-003 — Dictionary generator vs generated dictionaries

**Status:** `OPEN_MEDIUM_HIGH`

Observed generation direction is clear.

Formal canonical edit authority remains undeclared.

L4/L5.

---

## AUTH-LIB-L3-004 — Dictionary policy docs vs embedded generator strings

**Status:** `OPEN_HIGH`

`export_dictionary_policy_docs.py` contains complete policy text and overwrites docs.

Do not run casually.

L4 decision required.

---

## AUTH-LIB-L3-005 — Multiple alias normalization primitives

**Status:** `OPEN_MEDIUM`

Equivalent basic normalization appears in:

- catalog;
- dictionary;
- generic semantic helper.

Do not merge until profile-aware future behavior is designed.

L5.

---

## AUTH-LIB-L3-006 — Resolution status vocabularies

**Status:** `OPEN_HIGH`

At least these layers coexist:

1. dictionary resolver runtime statuses;
2. shared dictionary reference-resolution statuses;
3. Library Reference Contract statuses;
4. specialized Calculator validation/error semantics;
5. historical/demo preview variants.

Do not create another status vocabulary before mapping these.

L5 priority.

---

## AUTH-LIB-L3-007 — Calculator Input vs Library Reference Contract

**Status:** `OPEN_HIGH`

Both are valid current layers.

Relationship/composition is not defined.

L5 priority.

---

## AUTH-LIB-L3-008 — Reference example IDs vs current canonical catalog IDs

**Status:** `OPEN_HIGH`

Foundation/example namespace differs from current catalog namespace.

Examples are explicitly non-production, but future adoption requires mapping or isolation.

L5.

---

## AUTH-LIB-L3-009 — ContractVersion model vs Contract Registry

**Status:** `OPEN_HIGH`

Local lifecycle model exists.

Current Contract Registry implementation/adoption is not proven.

Do not infer Library should become Contract Registry.

L5.

---

## AUTH-LIB-L3-010 — Current status projections vs Git/completion truth

**Status:** `CONFLICT_CONFIRMED`

`current_status.*`, `next_questions`, and reports index are stale/multi-era.

Do not use them as current-state authority until reconciled.

L4 visibility restriction + L5 derivation decision.

---

## AUTH-LIB-L3-011 — Prompt Queue vs local prompt lifecycle

**Status:** `CURRENT_AUTHORITY_RESOLVED / LOCAL_MODEL_TRANSITIONAL`

Current authority:

Blueprint Prompt Queue.

Local active/index surfaces are supporting/transitional and multi-era.

L4/L5 should normalize role.

---

## AUTH-LIB-L3-012 — Checked-in quality report vs current health

**Status:** `CONFLICT_CONFIRMED`

Tracked report is point-in-time evidence, not current HEAD truth.

Current-head test pass is not asserted by L3.

---

## AUTH-LIB-L3-013 — Root/architecture README vs current Blueprint architecture

**Status:** `CONFLICT_CONFIRMED`

Older READMEs describe a broader old standalone architecture.

Current Blueprint policy and current implementation are stronger current evidence.

L4.

---

## AUTH-LIB-L3-014 — Local ADR acceptance vs current Blueprint policy

**Status:** `OPEN_MEDIUM`

Historical/local accepted decisions remain provenance.

Current applicability must be mapped to current portfolio architecture.

L4/L5.

---

## AUTH-LIB-L3-015 — Module priority p1 vs portfolio P0

**Status:** `OPEN_METADATA/TAXONOMY`

Do not resolve in L3.

Blueprint reconciliation required.

---

# 8. Duplicate / overlap register

No item below authorizes deletion.

## DUP-LIB-L3-001 — Seed and component catalogs

Resolved as intentional source/projection relationship.

`NOT_DUPLICATE_CAPABILITIES`

## DUP-LIB-L3-002 — Combined dictionary and group dictionary files

Likely intentional generated projections.

`NOT_INDEPENDENT_AUTHORITIES`

## DUP-LIB-L3-003 — Catalog resolver vs dictionary resolver

Distinct domains.

Shared normalization concern only.

`DISTINCT_CAPABILITIES_WITH_COMMON_PRIMITIVE_CANDIDATE`

## DUP-LIB-L3-004 — Three alias normalizers

Potential implementation duplication.

`RECONCILE_BEFORE_CONSOLIDATION`

## DUP-LIB-L3-005 — Generic Reference Contract vs specialized Calculator references

Not duplicates.

`PARALLEL_CONTRACT_LAYERS_RELATIONSHIP_UNDEFINED`

## DUP-LIB-L3-006 — Reference Contract examples vs semantic preview

Foundational lineage overlap.

`DOCUMENT/ARTIFACT_AUTHORITY_REVIEW_REQUIRED`

## DUP-LIB-L3-007 — Historical checkpoint exporters

Multiple scripts write similar current status/report surfaces for old checkpoints.

`COORDINATION_DUPLICATION_AND_STALENESS_CANDIDATE`

## DUP-LIB-L3-008 — Repeated operator commands in runbooks

Useful now but drift-prone.

`DOCUMENTATION_DRIFT_CANDIDATE`

## DUP-LIB-L3-009 — Redundant Make prompt-sync paths

Current Makefile contains overlapping sync invocations.

`OPERATOR_WORKFLOW_RECONCILIATION_CANDIDATE`

---

# 9. Implementation gap register

These are gaps relative to current policy/intent/roadmap.

They are not all immediate tasks.

## GAP-LIB-L3-001 — Service catalog semantics

Blueprint-owned target.

Current implementation not proven.

## GAP-LIB-L3-002 — Naming profiles and production-token semantics

Not implemented/proven.

Includes:

- profile IDs;
- device/equipment context;
- short production tokens;
- profile-specific defaults;
- filename grammar;
- profile-aware ambiguity.

## GAP-LIB-L3-003 — Governed misspelling/supplier alias layer

Current aliases exist.

Mature misspelling/provenance/confidence model not proven.

## GAP-LIB-L3-004 — External catalog ingestion provenance

Human Intent target.

No current ingestion/review pipeline proven.

## GAP-LIB-L3-005 — Calibration profiles

Human Intent target.

Not proven current.

## GAP-LIB-L3-006 — SOP/instruction/media knowledge

Human Intent target.

Not proven current.

## GAP-LIB-L3-007 — Shared UI design-system publication

Blueprint/Human Intent target.

No current shared UI package/component catalog implementation proven.

## GAP-LIB-L3-008 — Shared semantic/capability discovery registry

Local lookup primitives exist.

Cross-module semantic registration/discovery system not proven.

## GAP-LIB-L3-009 — Mature version/adoption/migration lifecycle

Current primitives:

- versions;
- deprecated state;
- deprecation metadata;
- ContractVersion fields.

Missing mature system:

- effective-from lifecycle;
- supersedes/replaced-by governance;
- consumer adoption state;
- rollout mode;
- migration evidence;
- freshness.

## GAP-LIB-L3-010 — Contract Registry integration

Dependency exists.

Implementation/adoption not proven.

## GAP-LIB-L3-011 — Consumer adoption/live integrations

Examples/pilots exist.

Broad live consumer adoption is not proven.

## GAP-LIB-L3-012 — Historical/reference asset semantics implementation

Planning direction exists.

Current implementation not proven.

## GAP-LIB-L3-013 — Generated-artifact drift gate

Generation chains exist.

A single clean generate-and-diff conformance gate is not proven.

## GAP-LIB-L3-014 — Read-only current-head quality truth

Current quality surface is strong but report publication mutates tracked files and checked-in report is stale.

## GAP-LIB-L3-015 — Normalized current coordination truth

Current prompt navigation is strong.

Current status/report/index lifecycle normalization is incomplete.

## GAP-LIB-L3-016 — Blueprint acceptance proof for Calculator Input v0.1

Module-side completion exists.

Current direct authoritative acceptance evidence is not proven in this synthesis packet.

---

# 10. Roadmap realization synthesis

The roadmap is planning-only and grants no execution authority.

## H01 — reconcile catalog/alias/template/naming/UI evidence

**State:** `PARTIAL_CURRENT`

Implemented/proven:

- catalog;
- aliases;
- dictionary vocabulary;
- Business Card reference.

Not proven:

- templates as mature surface;
- naming profiles;
- UI publication.

## H02 — confirm semantic ownership boundary

**State:** `STRONGLY_ALIGNED`

Current implementation and policy consistently preserve domain boundaries.

## H03 — complete capability/self-inventory

**State:** `STAGE2_SUBSTANTIALLY_ADVANCED`

L0–L3 now provides strong module inventory.

Future target items still absent:

- production tokens;
- templates/technical cards as mature system;
- broader semantic registry.

## H04 — naming/profile/default semantics

**State:** `NOT_IMPLEMENTED / CONTRACT_PRIMITIVES_ONLY`

Calculator has a versioned contract, but profile semantics do not exist.

## H05 — stable identifiers and lookup contracts

**State:** `PARTIAL_CURRENT`

Product/material references and lookup primitives exist.

Service semantics, Warehouse-specific adoption and mature lifecycle are not proven.

## H06 — UI design-system package lifecycle

**State:** `NOT_PROVEN`

## H07 — UI version/adoption metadata

**State:** `NOT_PROVEN`

## H08 — fast capability/semantic discovery

**State:** `EARLY_LOCAL_PRIMITIVES_ONLY`

Local registries/resolvers and governance document awareness are useful precedents, not the target shared discovery system.

## H09 — deprecation/migration paths

**State:** `FOUNDATIONAL_PRIMITIVES_ONLY`

Deprecated state exists.

Mature migration/adoption lifecycle does not.

## H10 — hold broader implementation pending Contract Registry/readiness

**State:** `STILL_VALID`

L3 provides strong evidence that the hold remains appropriate.

## H11/H12 — historical/reference asset semantics/boundary

**State:** `PLANNING_ONLY_NOT_PROVEN_IMPLEMENTED`

---

# 11. L4 Document Authority Registry inputs

L4 should not re-analyze capability behavior from scratch.

It should consume L3 and classify authority/lifecycle per artifact.

## Highest-priority L4 surfaces

1. Blueprint module policy and Human Intent;
2. root `README.md`;
3. `docs/architecture/README.md`;
4. local ADRs;
5. catalog seed;
6. generated component catalogs;
7. catalog schema exporter vs generated schemas;
8. Shared Operational Dictionary;
9. dictionary generator;
10. dictionary policy generator/docs;
11. Calculator Input Python contract;
12. Calculator schema;
13. Calculator fixtures;
14. Library Reference Contract schema;
15. Reference Contract examples;
16. Reference Consumption Pilot fixtures;
17. semantic preview;
18. Makefile;
19. current prompt mirror;
20. local prompt index;
21. current status YAML/MD;
22. next questions;
23. reports index;
24. completion reports;
25. completion packet;
26. checked-in quality reports;
27. runbooks/recovery docs;
28. module manifest;
29. awareness ledger;
30. standards snapshot.

## Minimum L4 fields

- path/surface;
- role;
- architecture generation;
- current authority;
- lifecycle;
- source/manual/generated;
- generator;
- governing higher authority;
- freshness evidence;
- supersession relation;
- mutation risk;
- consumer scope;
- assistant visibility status.

## Immediate visibility restrictions recommended for L4

Until reconciled, assistants should not use as current-state truth:

- stale `current_status.*`;
- stale `next_questions_for_blueprint.md`;
- mixed reports index;
- historical prompts merely because they sit under `active/`;
- old root/architecture README claims that contradict current implementation/Blueprint;
- semantic demo preview as canonical semantics;
- checked-in quality report as current HEAD health.

---

# 12. L5 Capability Reconciliation inputs

L5 should prioritize decisions that unblock safe future implementation.

## Priority A — semantic/contract normalization

1. Map all resolution/status vocabularies.
2. Decide relationship between Calculator Input and Library Reference Contract.
3. Decide current catalog ID binding for generic Reference Contract.
4. Decide ContractVersion ownership vs Contract Registry.
5. Define formal contract adoption/freshness lifecycle.
6. Decide static Business Card allowlist vs catalog-registry validation.
7. Decide schema-vs-runtime authority for Calculator contract.

## Priority B — source/generation authority

8. Declare catalog seed edit authority.
9. Declare catalog schema source authority.
10. Declare dictionary generator/data source authority.
11. Resolve dictionary policy generator/docs authority.
12. Define generated-artifact drift checks.

## Priority C — semantic primitive consolidation

13. Decide whether basic alias normalizers should share one primitive.
14. Preserve resolver-domain differences.
15. Define future profile-aware naming architecture.
16. Define formal dictionary reference type if `(group,id)` must travel cross-module.

## Priority D — coordination/current-state normalization

17. Normalize Prompt Queue vs local prompt lifecycle.
18. Define exactly-one-current prompt representation.
19. Define archival model.
20. Define current-status derivation.
21. Normalize reports index schema/derivation.
22. Define Blueprint acceptance event representation.
23. Define completion-packet version/freshness model.
24. Separate read-only Make targets from mutating/publishing targets.
25. Reconcile redundant sync paths and `status-report` semantics.

## Priority E — quality normalization

26. Define canonical current-head quality gate.
27. Separate validation from tracked-report publishing.
28. Define nested warning propagation.
29. Define generated-artifact drift gate.
30. Separate checkpoint-history tests from current-state freshness tests.
31. Decide mypy execution policy.

No new broad implementation should precede these decisions where they affect the same surface.

---

# 13. L8 cleanup candidates

These are **candidates only**.

No cleanup is authorized by L3.

## High-value candidates after L4/L5

1. stale checkpoint-specific coordination exporters;
2. `make_first_workflow.py` superseded helper;
3. historical prompt files under misleading `active/`;
4. stale/multi-era current-status surfaces;
5. mixed reports index;
6. redundant Make prompt-sync paths;
7. misnamed `status-report`;
8. stale module manifest lifecycle metadata;
9. dictionary policy-doc generator if superseded/unsafe;
10. old semantic preview if classified superseded/historical;
11. root README currentness repair;
12. architecture README currentness repair;
13. runbook stale branch assumptions;
14. duplicated runbook command lists;
15. generated report currentness/provenance model;
16. duplicated alias normalizers if L5 approves consolidation.

## Explicit non-cleanup

Do not treat as cleanup candidates solely from L3:

- catalog seed;
- component catalogs;
- Shared Operational Dictionary;
- group dictionaries;
- Business Card semantic card;
- Calculator input contract;
- Reference Contract foundation;
- `app/forprint_library/__init__.py`.

---

# 14. Explicit uncertainty register

## UNC-LIB-L3-001 — Calculator Blueprint acceptance

Module completion is proven.

Direct current authoritative Blueprint acceptance is not.

Severity: HIGH for lifecycle truth.

## UNC-LIB-L3-002 — Contract Registry implementation/adoption

Dependency and planning are clear.

Runtime/adoption implementation is not proven.

Severity: HIGH.

## UNC-LIB-L3-003 — Formal source authority for generated semantic artifacts

Generation direction is often known.

Human-edit authority is not uniformly declared.

Severity: HIGH.

## UNC-LIB-L3-004 — Contract-layer relationship

Calculator Input, generic Reference Contract, Consumption Pilot and ContractVersion models coexist.

Formal hierarchy/composition is undefined.

Severity: HIGH.

## UNC-LIB-L3-005 — Resolution status mapping

Multiple overlapping vocabularies.

Severity: HIGH.

## UNC-LIB-L3-006 — Current-head quality pass

L3 did not execute tests.

Tracked report is stale.

Severity: MEDIUM for analysis, HIGH if someone attempts to claim current green status.

## UNC-LIB-L3-007 — Current status projection authority

Local status/report indexes are stale/transitional.

Severity: HIGH for assistant context.

## UNC-LIB-L3-008 — Naming/profile architecture

Target direction exists; current implementation absent.

Severity: expected roadmap gap.

## UNC-LIB-L3-009 — UI design-system implementation

Ownership direction exists; implementation not proven.

Severity: expected roadmap gap.

## UNC-LIB-L3-010 — SOP/media knowledge implementation

Intent exists; implementation not proven.

Severity: expected roadmap gap.

## UNC-LIB-L3-011 — Historical/reference asset implementation

Planning direction exists; implementation not proven.

Severity: expected roadmap gap.

## UNC-LIB-L3-012 — P0 vs p1 Library priority metadata

Current Blueprint surfaces differ.

Severity: low-to-medium metadata/governance.

---

# 15. Current implementation vs target-state summary

## Implemented now

- draft catalog/reference core;
- catalog registry/alias lookup;
- Shared Operational Dictionary;
- group-scoped dictionary resolution;
- ambiguity/deprecation primitives;
- Business Card reference model;
- deterministic Calculator Input v0.1;
- generic Reference Contract foundation;
- Reference Consumption Pilot;
- generated artifact/fixture layer;
- substantial automated validation/test surface;
- Blueprint-aware Prompt Queue/operator/governance tooling;
- completion packet validation.

## Current but transitional/debt-heavy

- current status/report/index coordination projections;
- checked-in quality reporting;
- multi-era docs;
- historical checkpoint exporters;
- ContractVersion foundation;
- generic semantic facade;
- generated policy-doc authority.

## Planned / intended but not proven current

- service semantic catalog;
- naming profiles;
- production tokens;
- profile defaults;
- external catalog ingestion;
- calibration profiles;
- SOP/media knowledge;
- UI design system publication;
- cross-module semantic/capability registry;
- mature Contract Registry adoption;
- mature migration/deprecation lifecycle;
- historical/reference asset index;
- broad live consumer adoption.

---

# 16. L3 module-level disposition

```text
MODULE=forprint_library
STAGE=L3_CAPABILITY_SYNTHESIS

L2_BLOCKS_SYNTHESIZED=8
SUBSTANTIVE_CAPABILITY_FAMILIES=9
NON_CAPABILITY_STRUCTURAL_CLASSES=1

CURRENT_SEMANTIC_CATALOG_CORE=true
CURRENT_SHARED_DICTIONARY_CORE=true
CURRENT_CONFIGURABLE_PRODUCT_REFERENCE=true
CURRENT_CALCULATOR_INPUT_CONTRACT=true
CURRENT_GENERIC_REFERENCE_FOUNDATION=true
CURRENT_GENERATED_ARTIFACT_LAYER=true
CURRENT_QUALITY_LAYER=true
CURRENT_BLUEPRINT_OPERATOR_LAYER=true
CURRENT_DOCUMENTATION_LAYER=true

FINAL_PRODUCTION_CATALOG=false
NAMING_PROFILES_IMPLEMENTED=false
UI_DESIGN_SYSTEM_IMPLEMENTED=false
SOP_MEDIA_KNOWLEDGE_IMPLEMENTED=false
CONTRACT_REGISTRY_ADOPTION_IMPLEMENTED=false
MATURE_MIGRATION_LIFECYCLE_IMPLEMENTED=false
HISTORICAL_ASSET_INDEX_IMPLEMENTED=false

BUSINESS_TRUTH_AUTHORITY_LEAKAGE=false

DOMINANT_DEBT=AUTHORITY_GENERATION_LIFECYCLE_AND_FRESHNESS_NORMALIZATION
BROAD_REWRITE_REQUIRED=false
BROAD_NEW_IMPLEMENTATION_AUTHORIZED=false

NEXT=L4_DOCUMENT_AUTHORITY_REGISTRY
THEN=L5_CAPABILITY_RECONCILIATION
```

---

# 17. Recommended stage transition

L3 has enough evidence to close.

Recommended next stage:

`L4 — Document / Artifact Authority Registry`

Why L4 before L5:

The highest-risk current questions depend on knowing which artifact is authoritative:

- seed vs projection;
- generator vs generated schema;
- generator vs dictionary data;
- script-embedded policy vs policy document;
- executable contract vs schema vs fixture;
- current Blueprint policy vs old README/ADR;
- Prompt Queue vs local prompt files;
- Git/completion truth vs stale current-status projections.

Once L4 explicitly classifies authority, L5 can reconcile capability overlaps without guessing which surface is normative.

No source cleanup or new domain implementation should occur between L3 and L4.

---

# 18. Final statement

The Stage 2 Library pilot has now moved from file inventory to a coherent module-level model.

The most accurate current description is:

> ForPrint Library already has a real semantic/reference platform core: a draft canonical catalog, shared operational dictionary and deterministic resolution, a configurable Business Card reference, a deterministic Library → Calculator input contract, generic reference-contract foundations, generated projection/fixture tooling, strong automated quality coverage and a modern Blueprint-aware operator layer.

The equally important maturity statement is:

> These capabilities are surrounded by multiple historical and transitional authority surfaces. Contract layers are not yet unified, generated sources are not uniformly declared, coordination current-state projections are stale, and several future Library responsibilities remain roadmap/intent only.

Therefore the next correct move is not expansion.

The next correct move is:

> **establish explicit document/artifact authority in L4, then reconcile capability relationships in L5.**

**Final L3 status:**

`PASS_FOR_CAPABILITY_SYNTHESIS_WITH_AUTHORITY_AND_RECONCILIATION_INPUTS_READY`
```

### `tmp/module_knowledge_analysis/forprint_library/synthesis/library_l3_capability_map_v0_1.yaml`

- SHA256: `6de32f0aef9774c7bd786766de7fbf525feb8cb2d6253f5d0a75c6b9f713e55b`
- Bytes: `4163`

```yaml
schema_version: forprint_library_l3_capability_map_v0_1
module_id: forprint_library
stage: L3_CAPABILITY_SYNTHESIS
source_state:
  library_branch: feature/library-calculator-input-contract-v01
  library_head: bba52bf6001f256a5c13ea7dbe175336b431754c
  blueprint_branch: audit/blueprint-inventory-refresh-2026-07-29
  blueprint_head: b6ab9b65a2c27b70a574468caa8e3de4c3b454c5
  l2_blocks_synthesized: 8
authority:
  source_mutation: false
  roadmap_mutation: false
  implementation_authority: false
  cleanup_authority: false
module_role:
  current: semantic_catalog_reference_and_shared_definition_authority
  must_not_own:
  - calculator_pricing_truth
  - operational_orders
  - client_database_truth
  - accounting_truth
  - warehouse_stock_truth
  - production_runtime
  - crm_workflow
  - telegram_runtime
  - foreign_domain_business_rules
capability_families:
- id: CAP-LIB-L3-01
  name: canonical_semantic_catalog_reference_core
  maturity: CURRENT_IMPLEMENTED_DRAFT_REFERENCE
  confidence: HIGH
  implemented: true
  main_debt:
  - lifecycle_maturity
  - formal_generated_authority
- id: CAP-LIB-L3-02
  name: shared_dictionary_and_resolution_core
  maturity: CURRENT_IMPLEMENTED_DRAFT_REFERENCE
  confidence: HIGH
  implemented: true
  main_debt:
  - resolution_status_mapping
  - naming_profile_gap
- id: CAP-LIB-L3-03
  name: configurable_product_reference_model
  maturity: CURRENT_IMPLEMENTED_DRAFT_REFERENCE
  confidence: HIGH
  implemented: true
  current_products:
  - product.business_card
- id: CAP-LIB-L3-04
  name: deterministic_calculator_input_projection
  maturity: CURRENT_IMPLEMENTED_EXECUTABLE_SPECIALIZED_CONTRACT
  confidence: HIGH
  implemented: true
  blueprint_acceptance: NOT_PROVEN
- id: CAP-LIB-L3-05
  name: generic_library_reference_contract_foundation
  maturity: CURRENT_FOUNDATIONAL_AND_PILOT
  confidence: HIGH_ARTIFACTS_MEDIUM_HIGH_ADOPTION
  implemented: true
  contract_registry_adoption: NOT_PROVEN
- id: CAP-LIB-L3-06
  name: generated_projection_schema_fixture_layer
  maturity: CURRENT_SUPPORTING_GENERATED_LAYER
  confidence: HIGH
  implemented: true
  generated_drift_gate: NOT_PROVEN
- id: CAP-LIB-L3-07
  name: validation_and_quality_surface
  maturity: CURRENT_SUBSTANTIAL_WITH_FRESHNESS_AND_MUTATION_DEBT
  confidence: HIGH
  implemented: true
  fresh_current_head_pass_asserted_by_l3: false
- id: CAP-LIB-L3-08
  name: blueprint_aware_governance_operator_surface
  maturity: CURRENT_IMPLEMENTED_WITH_TRANSITIONAL_COORDINATION_STATE
  confidence: HIGH
  implemented: true
  prompt_authority: BLUEPRINT_PROMPT_QUEUE
- id: CAP-LIB-L3-09
  name: documentation_and_architecture_knowledge_layer
  maturity: MULTI_GENERATIONAL_SUPPORTING_WITH_AUTHORITY_DEBT
  confidence: HIGH
  implemented: true
  architecture_generations: 4+
non_capability_structures:
- id: STRUCT-LIB-L3-01
  path: app/forprint_library/__init__.py
  classification: TECHNICAL_SCAFFOLDING
  disposition: KEEP
high_priority_reconciliation:
- resolution_status_vocabularies
- calculator_input_vs_library_reference_contract
- reference_example_ids_vs_current_catalog_ids
- contract_version_model_vs_contract_registry
- catalog_and_schema_source_authority
- dictionary_generator_and_policy_authority
- generated_artifact_drift_protection
- prompt_queue_vs_local_prompt_lifecycle
- current_status_and_report_index_derivation
- blueprint_acceptance_event_model
- quality_gate_read_only_vs_report_publishing
major_not_proven_current:
- service_catalog_semantics
- naming_profiles
- production_tokens
- profile_specific_defaults
- external_catalog_ingestion
- calibration_profiles
- sop_instruction_media_knowledge
- ui_design_system_publication
- shared_semantic_capability_registry
- mature_contract_registry_adoption
- mature_migration_lifecycle
- historical_reference_asset_index
- broad_live_consumer_adoption
stage_disposition:
  result: PASS_FOR_CAPABILITY_SYNTHESIS_WITH_AUTHORITY_AND_RECONCILIATION_INPUTS_READY
  dominant_debt: AUTHORITY_GENERATION_LIFECYCLE_AND_FRESHNESS_NORMALIZATION
  broad_rewrite_required: false
  broad_new_implementation_authorized: false
  next_stage: L4_DOCUMENT_AUTHORITY_REGISTRY
  then: L5_CAPABILITY_RECONCILIATION
```

### `tmp/module_knowledge_analysis/forprint_library/synthesis/l3_packet_run_report.yaml`

- SHA256: `e52f941e26975ba37af6351a3662585a69688fcbd45b75b7447e7eb4a711e651`
- Bytes: `1308`

```yaml
schema_version: forprint_library_l3_packet_run_report_v0_1
result: PASS
module_id: forprint_library
stage: L3_CAPABILITY_SYNTHESIS
branch: feature/library-calculator-input-contract-v01
head: bba52bf6001f256a5c13ea7dbe175336b431754c
upstream: bba52bf6001f256a5c13ea7dbe175336b431754c
blueprint_branch: audit/blueprint-inventory-refresh-2026-07-29
blueprint_head: b6ab9b65a2c27b70a574468caa8e3de4c3b454c5
l2_block_count: 8
l2_report_count: 8
non_tmp_git_status_unchanged: true
mutation_performed_outside_tmp: false
tests_run: false
make_run: false
exporters_run: false
generators_run: false
outputs:
  packet_dir: tmp/module_knowledge_analysis/forprint_library/synthesis/l3_packet
  packet_markdown: tmp/module_knowledge_analysis/forprint_library/synthesis/l3_capability_synthesis_packet.md
  packet_tar_gz: tmp/module_knowledge_analysis/forprint_library/synthesis/l3_capability_synthesis_packet.tar.gz
  run_report: tmp/module_knowledge_analysis/forprint_library/synthesis/l3_packet_run_report.yaml
sha256:
  packet_markdown: ff0f2082ec9c9c2ed03950463dbefe2b43a3e8e3c28406b04b14eff0fd7f8c77
  packet_tar_gz: c041db0f3df1aa5bf5eec479c9946e8eb2b8191fef79aeda8d7307a7b72ef86a
  packet_manifest: 62e6963453371a65062a1312aaec4a040e57f15f10f568569d1cb0e1d81602ab
next_action: produce L3 capability synthesis report
```

---

# B. Library authority candidates

### `Makefile`

- SHA256: `1dbb9d37aada8b97fc82bdead4205a9eec877d08d62939b47e518329591faa22`
- Bytes: `35129`

_Binary/non-text artifact; content not inlined._

### `README.md`

- SHA256: `9e071dc15b5ee6860fd84afa3ab9c5610fc9e4b460c8d9af971f2f0b686f70f8`
- Bytes: `3963`

```markdown
# forprint_library

`forprint_library` — центральний регламентно-документальний модуль екосистеми ForPrint.

## Призначення

Модуль зберігає, версіонує, описує і перевіряє:

- технічні контракти між модулями;
- JSON-схеми документів і запитів;
- людську документацію до контрактів;
- Change Manifest для змін між версіями;
- Semantic Registry для стабільних смислових ID;
- Migration Graph для переходів між версіями;
- правила історичної сумісності;
- базові довідники і політики валідації.

## Що модуль НЕ робить

`forprint_library` не виконує бізнес-логіку:

- не рахує ціни;
- не виконує препрес;
- не веде склад;
- не створює бухгалтерські проводки;
- не керує доставкою;
- не ремонтує обладнання;
- не маршрутизує живі замовлення.

## Архітектурний закон

`forprint_library` описує, що є правильним.  
`forprint_sync_manager` приводить внутрішні модулі до актуальних правил.  
`forprint_orchestra` маршрутизує вже валідні й узгоджені процеси.  
Робочі модулі виконують бізнес-логіку.

## Базові принципи

1. Стара версія може бути заборонена для нових запитів, але має лишатися читабельною для архіву.
2. Жодна фундаментальна сутність не повинна втрачати свій смисл через перейменування поля, зміну мови або зміну ID.
3. Автоматична міграція дозволена тільки тоді, коли нове значення можна отримати зі старого без здогадок.
4. Кожна зміна контракту має мати людський і машинний опис.
5. Жодна зміна не повинна ставати production-active без перевірки критичних залежностей.
6. Невідомий запит — це контрольований стан, а не аварія сервісу.

## Швидкий старт

```bash
cd forprint_library

python3.12 -m venv .venv_forprint_library
source .venv_forprint_library/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

make test
make run
```

Після запуску API:

```bash
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/api/v1/contracts/prepress.job_request/latest
```

## Структура

```text
app/forprint_library/
├── api/                 # FastAPI-шар
├── changes/             # Change Manifest
├── contracts/           # Контракти і версії контрактів
├── core/                # Статуси, відповіді, загальні типи
├── migration/           # Migration Graph
├── registry/            # In-memory registry на старті
├── semantic/            # Semantic Registry, attributes, values, aliases
├── services/            # Сервісний шар
└── validation/          # JSON Schema validation
```

## Поточний статус

Це стартовий каркас. Тут навмисно немає конкретних накладних, реальних товарів, відвантажень або бухгалтерських документів. Спочатку закладаємо основу.
```

### `app/forprint_library/calculator_input/contract.py`

- SHA256: `c3467f38d1747ce17cfeab77f3b32faf7cecf4a031eb14c692ca1c73b3adedd8`
- Bytes: `20193`

```python
"""Read-only Calculator input projection contract.

The contract converts a validated Library configurable product selection into a
deterministic, schema-versioned envelope that Calculator can consume as reference
input. It intentionally contains no prices, formulas, costs, margins, taxes,
discounts, totals, stock truth, order writes or external integration calls.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

SUPPORTED_PRODUCT_ID = "product.business_card"
CALCULATOR_INPUT_SCHEMA_VERSION = "calculator_input_envelope_v0_1"
VALIDATION_SNAPSHOT_SCHEMA_VERSION = "calculator_input_validation_snapshot_v0_1"
ERROR_SCHEMA_VERSION = "calculator_input_error_v0_1"

ROOT = Path(__file__).resolve().parents[3]
BUSINESS_CARD_PATH = ROOT / "catalog" / "configurable_products" / "business_card.yaml"

REQUIRED_PARAMETERS = (
    "size",
    "sides",
    "material_ref",
    "print_mode_ref",
    "quantity",
)

FORBIDDEN_MONETARY_KEYS = {
    "amount",
    "calculator_formula",
    "coefficient",
    "cost",
    "currency",
    "discount",
    "final_price",
    "formula",
    "margin",
    "price",
    "price_formula",
    "quote_total",
    "subtotal",
    "tax",
    "total",
    "vendor_price",
}


class CalculatorInputErrorType(StrEnum):
    """Stable public error taxonomy for Calculator input projection."""

    UNKNOWN_PRODUCT = "unknown_product"
    INVALID_CONFIGURATION = "invalid_configuration"
    MISSING_REQUIRED_PARAMETER = "missing_required_parameter"
    INVALID_REFERENCE = "invalid_reference"
    UNSUPPORTED_PROJECTION_VERSION = "unsupported_projection_version"
    INTERNAL_CONTRACT_ERROR = "internal_contract_error"


class CalculatorInputContractError(ValueError):
    """Safe typed error for Calculator input contract consumers."""

    def __init__(
        self,
        error_type: CalculatorInputErrorType,
        message: str,
        *,
        field_path: str | None = None,
        details: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.field_path = field_path
        self.details = dict(details or {})

    def to_public_error(self) -> dict[str, object]:
        """Return a stable, stack-trace-free public error payload."""

        return {
            "schema_version": ERROR_SCHEMA_VERSION,
            "error_type": self.error_type.value,
            "message": self.message,
            "field_path": self.field_path,
            "details": copy.deepcopy(self.details),
        }


@dataclass(frozen=True)
class CalculatorReferenceIds:
    """Reference identifiers projected for Calculator input context."""

    product_id: str
    size_id: str
    sides_id: str
    material_ref: Mapping[str, object]
    print_mode_ref: Mapping[str, object]
    finishing_refs: tuple[Mapping[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "product_id": self.product_id,
            "size_id": self.size_id,
            "sides_id": self.sides_id,
            "material_ref": _unfreeze(self.material_ref),
            "print_mode_ref": _unfreeze(self.print_mode_ref),
            "finishing_refs": [_unfreeze(ref) for ref in self.finishing_refs],
        }


@dataclass(frozen=True)
class ValidationSnapshot:
    """Explicit validation result included in successful envelopes."""

    schema_version: str
    valid: bool
    errors: tuple[Mapping[str, object], ...]
    warnings: tuple[Mapping[str, object], ...]
    required_parameters: tuple[str, ...]
    normalization_notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "valid": self.valid,
            "errors": [_unfreeze(error) for error in self.errors],
            "warnings": [_unfreeze(warning) for warning in self.warnings],
            "required_parameters": list(self.required_parameters),
            "normalization_notes": list(self.normalization_notes),
        }


@dataclass(frozen=True)
class CalculatorInputEnvelope:
    """Versioned deterministic envelope for Calculator-ready Library input."""

    schema_version: str
    product_id: str
    configuration_id: str
    normalized_parameters: Mapping[str, object]
    reference_ids: CalculatorReferenceIds
    validation_snapshot: ValidationSnapshot

    def to_dict(self) -> dict[str, object]:
        """Serialize with stable field ordering."""

        return {
            "schema_version": self.schema_version,
            "product_id": self.product_id,
            "configuration_id": self.configuration_id,
            "normalized_parameters": _unfreeze(self.normalized_parameters),
            "reference_ids": self.reference_ids.to_dict(),
            "validation_snapshot": self.validation_snapshot.to_dict(),
        }


def build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope:
    """Build a read-only Calculator input envelope from Library references.

    The function is deterministic, does not mutate input mappings, performs no
    writes, imports no Calculator code, and makes no network calls.
    """

    requested_schema_version = schema_version or CALCULATOR_INPUT_SCHEMA_VERSION

    if requested_schema_version != CALCULATOR_INPUT_SCHEMA_VERSION:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.UNSUPPORTED_PROJECTION_VERSION,
            "Unsupported Calculator input projection schema version.",
            field_path="schema_version",
            details={
                "requested_schema_version": requested_schema_version,
                "supported_schema_version": CALCULATOR_INPUT_SCHEMA_VERSION,
            },
        )

    if product_id != SUPPORTED_PRODUCT_ID:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.UNKNOWN_PRODUCT,
            "Unsupported product for Calculator input projection.",
            field_path="product_id",
            details={"product_id": product_id},
        )

    source_configuration = copy.deepcopy(dict(configuration))
    card = _load_business_card()

    normalized = _normalize_business_card_configuration(card, source_configuration)
    reference_ids = CalculatorReferenceIds(
        product_id=product_id,
        size_id=str(normalized["size"]),
        sides_id=str(normalized["sides"]),
        material_ref=_freeze(normalized["material_ref"]),
        print_mode_ref=_freeze(normalized["print_mode_ref"]),
        finishing_refs=tuple(_freeze(ref) for ref in normalized["finishing_refs"]),
    )

    validation_snapshot = ValidationSnapshot(
        schema_version=VALIDATION_SNAPSHOT_SCHEMA_VERSION,
        valid=True,
        errors=(),
        warnings=(),
        required_parameters=REQUIRED_PARAMETERS,
        normalization_notes=(
            "Output field order is stable.",
            "finishing_refs are sorted by catalog and id.",
            "Optional artwork_source is included only when supplied.",
            "No monetary, pricing, stock, production or runtime fields are projected.",
        ),
    )

    configuration_id = _build_configuration_id(
        product_id=product_id,
        schema_version=requested_schema_version,
        normalized_parameters=normalized,
        reference_ids=reference_ids,
    )

    envelope = CalculatorInputEnvelope(
        schema_version=requested_schema_version,
        product_id=product_id,
        configuration_id=configuration_id,
        normalized_parameters=_freeze(normalized),
        reference_ids=reference_ids,
        validation_snapshot=validation_snapshot,
    )

    _assert_no_forbidden_monetary_keys(envelope.to_dict())
    return envelope


def _load_business_card() -> dict[str, Any]:
    data = yaml.safe_load(BUSINESS_CARD_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Business card product card must be a mapping.",
            field_path="catalog/configurable_products/business_card.yaml",
        )

    if data.get("product_id") != SUPPORTED_PRODUCT_ID:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Business card product card has unexpected product_id.",
            field_path="product_id",
            details={"product_id": data.get("product_id")},
        )

    return data


def _normalize_business_card_configuration(
    card: Mapping[str, object],
    configuration: Mapping[str, object],
) -> dict[str, object]:
    missing = [key for key in REQUIRED_PARAMETERS if key not in configuration]
    if missing:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.MISSING_REQUIRED_PARAMETER,
            "Missing required Calculator input parameter.",
            field_path=missing[0],
            details={"missing_parameters": missing},
        )

    size = _normalize_choice(card, "size", configuration["size"])
    sides = _normalize_choice(card, "sides", configuration["sides"])
    material_ref = _normalize_reference(card, "material_ref", configuration["material_ref"])
    print_mode_ref = _normalize_reference(card, "print_mode_ref", configuration["print_mode_ref"])
    quantity = _normalize_quantity(configuration["quantity"])
    finishing_refs = _normalize_finishing_refs(card, configuration.get("finishing_refs", []))
    artwork_source = _normalize_optional_artwork_source(card, configuration.get("artwork_source"))

    _validate_sides_and_print_mode_match(card, sides, print_mode_ref)

    normalized: dict[str, object] = {
        "size": size,
        "sides": sides,
        "material_ref": material_ref,
        "print_mode_ref": print_mode_ref,
        "quantity": quantity,
        "finishing_refs": finishing_refs,
    }

    if artwork_source is not None:
        normalized["artwork_source"] = artwork_source

    return normalized


def _parameter(card: Mapping[str, object], key: str) -> Mapping[str, object]:
    parameters = card.get("constructor_parameters")
    if not isinstance(parameters, list):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Product card constructor_parameters must be a list.",
            field_path="constructor_parameters",
        )

    for parameter in parameters:
        if isinstance(parameter, dict) and parameter.get("key") == key:
            return parameter

    raise CalculatorInputContractError(
        CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
        "Product card parameter definition is missing.",
        field_path=f"constructor_parameters.{key}",
        details={"parameter_key": key},
    )


def _normalize_choice(card: Mapping[str, object], parameter_key: str, value: object) -> str:
    if not isinstance(value, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Choice parameter must be a string identifier.",
            field_path=parameter_key,
        )

    parameter = _parameter(card, parameter_key)
    allowed = {
        item["id"]
        for item in parameter.get("allowed_values", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    if value not in allowed:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Unsupported choice parameter value.",
            field_path=parameter_key,
            details={"value": value, "allowed_values": sorted(allowed)},
        )

    return value


def _normalize_reference(
    card: Mapping[str, object],
    parameter_key: str,
    value: object,
) -> dict[str, str]:
    parameter = _parameter(card, parameter_key)
    expected_catalog = parameter.get("reference_catalog")

    if not isinstance(expected_catalog, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Reference parameter definition is missing reference_catalog.",
            field_path=f"constructor_parameters.{parameter_key}.reference_catalog",
        )

    if not isinstance(value, Mapping):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference parameter must be a mapping with catalog and id.",
            field_path=parameter_key,
        )

    catalog = value.get("catalog")
    ref_id = value.get("id")

    if catalog != expected_catalog or not isinstance(ref_id, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference parameter has invalid catalog or id.",
            field_path=parameter_key,
            details={"expected_catalog": expected_catalog, "value": dict(value)},
        )

    allowed = _allowed_reference_ids(parameter)

    if ref_id not in allowed:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference parameter id is not allowed for this product.",
            field_path=parameter_key,
            details={"reference_id": ref_id, "allowed_refs": sorted(allowed)},
        )

    return {"catalog": expected_catalog, "id": ref_id}


def _normalize_quantity(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Quantity must be an integer.",
            field_path="quantity",
        )

    if value < 1:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Quantity must be greater than or equal to 1.",
            field_path="quantity",
            details={"minimum": 1, "value": value},
        )

    return value


def _normalize_finishing_refs(
    card: Mapping[str, object],
    value: object,
) -> list[dict[str, str]]:
    if value is None:
        value = []

    if not isinstance(value, list):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "finishing_refs must be a list of references.",
            field_path="finishing_refs",
        )

    normalized = [
        _normalize_reference_value_against_parameter(card, "finishing_refs", item)
        for item in value
    ]

    unique = {(ref["catalog"], ref["id"]): ref for ref in normalized}

    return [unique[key] for key in sorted(unique)]


def _normalize_reference_value_against_parameter(
    card: Mapping[str, object],
    parameter_key: str,
    value: object,
) -> dict[str, str]:
    parameter = _parameter(card, parameter_key)
    expected_catalog = parameter.get("reference_catalog")

    if not isinstance(expected_catalog, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Reference list parameter definition is missing reference_catalog.",
            field_path=f"constructor_parameters.{parameter_key}.reference_catalog",
        )

    if not isinstance(value, Mapping):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference list item must be a mapping with catalog and id.",
            field_path=parameter_key,
        )

    catalog = value.get("catalog")
    ref_id = value.get("id")

    if catalog != expected_catalog or not isinstance(ref_id, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference list item has invalid catalog or id.",
            field_path=parameter_key,
            details={"expected_catalog": expected_catalog, "value": dict(value)},
        )

    allowed = _allowed_reference_ids(parameter)

    if ref_id not in allowed:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference list item is not allowed for this product.",
            field_path=parameter_key,
            details={"reference_id": ref_id, "allowed_refs": sorted(allowed)},
        )

    return {"catalog": expected_catalog, "id": ref_id}


def _normalize_optional_artwork_source(card: Mapping[str, object], value: object) -> str | None:
    if value is None:
        return None

    return _normalize_choice(card, "artwork_source", value)


def _validate_sides_and_print_mode_match(
    card: Mapping[str, object],
    sides: str,
    print_mode_ref: Mapping[str, str],
) -> None:
    parameter = _parameter(card, "sides")

    for allowed_value in parameter.get("allowed_values", []):
        if not isinstance(allowed_value, Mapping):
            continue
        if allowed_value.get("id") != sides:
            continue

        expected_print_mode = allowed_value.get("print_mode_ref")
        if not isinstance(expected_print_mode, Mapping):
            return

        expected_id = expected_print_mode.get("id")
        if print_mode_ref.get("id") != expected_id:
            raise CalculatorInputContractError(
                CalculatorInputErrorType.INVALID_CONFIGURATION,
                "Selected sides and print_mode_ref are inconsistent.",
                field_path="print_mode_ref",
                details={
                    "sides": sides,
                    "expected_print_mode_ref": dict(expected_print_mode),
                    "actual_print_mode_ref": dict(print_mode_ref),
                },
            )
        return


def _allowed_reference_ids(parameter: Mapping[str, object]) -> set[str]:
    return {
        item["id"]
        for item in parameter.get("allowed_refs", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _build_configuration_id(
    *,
    product_id: str,
    schema_version: str,
    normalized_parameters: Mapping[str, object],
    reference_ids: CalculatorReferenceIds,
) -> str:
    canonical = {
        "schema_version": schema_version,
        "product_id": product_id,
        "normalized_parameters": normalized_parameters,
        "reference_ids": reference_ids.to_dict(),
    }

    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"calc_input_{digest}"


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(nested) for key, nested in value.items()})

    if isinstance(value, list | tuple):
        return tuple(_freeze(item) for item in value)

    return copy.deepcopy(value)


def _unfreeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _unfreeze(nested) for key, nested in value.items()}

    if isinstance(value, tuple):
        return [_unfreeze(item) for item in value]

    if isinstance(value, list):
        return [_unfreeze(item) for item in value]

    return copy.deepcopy(value)


def _assert_no_forbidden_monetary_keys(value: object) -> None:
    found = sorted(FORBIDDEN_MONETARY_KEYS.intersection(_iter_keys(value)))
    if found:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Calculator input envelope contains forbidden monetary keys.",
            details={"forbidden_keys": found},
        )


def _iter_keys(value: object) -> list[str]:
    if isinstance(value, Mapping):
        keys = list(value)
        for nested in value.values():
            keys.extend(_iter_keys(nested))
        return [str(key) for key in keys]

    if isinstance(value, list | tuple):
        keys: list[str] = []
        for item in value:
            keys.extend(_iter_keys(item))
        return keys

    return []
```

### `app/forprint_library/contracts/models.py`

- SHA256: `e0c46c169100c7216028668291abb5db8862021a81e9629a8a66a5a021cf518a`
- Bytes: `2295`

```python
"""Моделі контрактів forprint_library.

Контракт описує форму взаємодії між модулями, а ContractVersion описує
конкретну версію цього контракту.
"""

from datetime import date
from typing import Any

from forprint_library.core.enums import ChangeLevel, ContractStatus
from pydantic import BaseModel, Field


class Contract(BaseModel):
    """Логічний контракт без прив'язки до конкретної версії."""

    code: str = Field(..., examples=["prepress.job_request"])
    name: str
    domain: str = Field(..., examples=["prepress"])
    description: str = ""
    owner_module: str | None = None


class ContractVersion(BaseModel):
    """Окрема версія контракту."""

    contract_code: str
    version: str = Field(..., examples=["1.0.0"])
    status: ContractStatus = ContractStatus.DRAFT

    # Дати життєвого циклу.
    effective_from: date | None = None
    deprecated_from: date | None = None
    blocked_from: date | None = None

    # Машинна JSON Schema.
    json_schema: dict[str, Any]

    # Людинозрозуміла документація.
    human_description: str = ""
    human_changelog: str = ""

    # Машинний опис змін, який потім читатиме sync_manager.
    machine_changelog: dict[str, Any] = Field(default_factory=dict)
    change_level: ChangeLevel = ChangeLevel.COSMETIC

    # Політики міграції.
    auto_migration_allowed: bool = False
    migration_strategy: str | None = None
    migration_rules: list[dict[str, Any]] = Field(default_factory=list)

    # Історична сумісність.
    archive_read_allowed: bool = True

    def allows_new_input(self) -> bool:
        """Чи можна приймати нові документи по цій версії."""

        return self.status not in {
            ContractStatus.BLOCKED_FOR_INPUT,
            ContractStatus.READ_ONLY,
            ContractStatus.ARCHIVED,
        }

    def allows_archive_read(self) -> bool:
        """Чи можна читати архівні документи по цій версії."""

        return self.archive_read_allowed
```

### `catalog/configurable_products/business_card.yaml`

- SHA256: `461ec437136b09218c3c9e1dfce9ca7a8bb4582600736a5fabae128d5e0de912`
- Bytes: `4635`

```yaml
schema_version: configurable_product_card_v0_1
product_id: product.business_card
kind: configurable_product
status: draft_reference
version: "0.1"
owner_module: forprint_library
names:
  uk: Візитки
  en: Business cards
aliases:
  - візитки
  - візитка
  - business cards
  - business card
compatibility_aliases:
  - product:business_cards
product_family_ref:
  catalog: product_families
  id: business_card
  label: Візитка
description:
  uk: Контрольна configurable product card для друкованих візиток.
  en: Controlled configurable product card for printed business cards.
constructor_parameters:
  - key: size
    label:
      uk: Розмір
      en: Size
    type: choice
    required: true
    library_owned: true
    allowed_values:
      - id: size_90x50_mm
        label: 90x50 mm
        width_mm: 90
        height_mm: 50
      - id: size_85x55_mm
        label: 85x55 mm
        width_mm: 85
        height_mm: 55
  - key: sides
    label:
      uk: Сторони друку
      en: Printed sides
    type: choice
    required: true
    library_owned: true
    allowed_values:
      - id: one_sided
        label: 4+0
        print_mode_ref:
          catalog: print_modes
          id: color_4_0
      - id: two_sided
        label: 4+4
        print_mode_ref:
          catalog: print_modes
          id: color_4_4
  - key: material_ref
    label:
      uk: Матеріал
      en: Material
    type: reference_choice
    required: true
    library_owned: true
    reference_catalog: materials
    allowed_refs:
      - catalog: materials
        id: paper_300g_matte
      - catalog: materials
        id: paper_350g_gloss
  - key: print_mode_ref
    label:
      uk: Режим друку
      en: Print mode
    type: reference_choice
    required: true
    library_owned: true
    reference_catalog: print_modes
    allowed_refs:
      - catalog: print_modes
        id: color_4_0
      - catalog: print_modes
        id: color_4_4
  - key: quantity
    label:
      uk: Кількість
      en: Quantity
    type: numeric_input_context
    required: true
    consumer_owned_value: true
    minimum: 1
    example_values:
      - 100
      - 500
      - 1000
    notes: Quantity is input context only. Library does not calculate price.
  - key: finishing_refs
    label:
      uk: Постобробка
      en: Finishing
    type: reference_list
    required: false
    library_owned: true
    reference_catalog: finishing_options
    allowed_refs:
      - catalog: finishing_options
        id: none
      - catalog: finishing_options
        id: matte_lamination
      - catalog: finishing_options
        id: gloss_lamination
      - catalog: finishing_options
        id: corner_rounding
  - key: artwork_source
    label:
      uk: Джерело макета
      en: Artwork source
    type: choice
    required: false
    consumer_owned_value: true
    allowed_values:
      - id: customer_print_ready_file
        label: Customer provides print-ready file
      - id: customer_needs_design
        label: Customer needs design
      - id: customer_needs_prepress_check
        label: Customer needs prepress check
consumer_usage_notes:
  telegram_bot:
    allowed_use: May use product.business_card and aliases as route hints only.
    forbidden_use: Must not treat this card as Telegram runtime behavior.
  calculator_engine:
    allowed_use: May later use constructor parameters as pricing input context.
    forbidden_use: No formula or final price is implemented in Library.
  forprint_operational_registry:
    allowed_use: May store product.business_card as foreign-domain metadata.
    forbidden_use: Library does not create orders or operational records.
boundary_notes:
  library_owned:
    - product_id
    - names
    - aliases
    - product_family_ref
    - constructor parameter definitions
    - references to Library catalog IDs
  consumer_owned:
    - selected parameter values
    - channel routing context
    - pricing input context
    - operational foreign metadata
  explicit_non_goals:
    - No full product catalog
    - No product modeling UI
    - No production catalog database
    - No live API
    - No 1C import
    - No 1C synchronization
    - No Calculator integration
    - No Telegram Bot integration
    - No Operational Registry write
    - No CRM write
    - No Website write
    - No price calculation
    - No final price formula
    - No material write-off logic
    - No warehouse stock truth
    - No production task creation
    - No real client or order data
    - No production runtime
```

### `catalog/finishing_options.yaml`

- SHA256: `85b6dd494d15f87bd7271204eddcb15d21211c0c0cdc83723f19749985f13736`
- Bytes: `2160`

```yaml
catalog_type: finishing_options
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: none
  name_uk: Без постобробки
  name_en: No finishing
  aliases:
  - без постобробки
  - no finishing
  - без додаткової обробки
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: matte_lamination
  name_uk: Матова ламінація
  name_en: Matte lamination
  aliases:
  - матова ламінація
  - matte lamination
  - матове ламінування
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: gloss_lamination
  name_uk: Глянцева ламінація
  name_en: Gloss lamination
  aliases:
  - глянцева ламінація
  - gloss lamination
  - глянцеве ламінування
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: corner_rounding
  name_uk: Заокруглення кутів як опція
  name_en: Corner rounding finish
  aliases:
  - заокруглені кути
  - corner rounding finish
  - круглі кути
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: finishing_folding
  name_uk: Фальцювання як опція
  name_en: Folding finish
  aliases:
  - фальцювання як опція
  - folding finish
  - згин як постобробка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
```

### `catalog/materials.yaml`

- SHA256: `8d113c1b375965bfbb2efef3de9c4dce45b867d31cb1d8cf33d56feb903215ad`
- Bytes: `2381`

```yaml
catalog_type: materials
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: paper_300g_matte
  name_uk: Папір 300 г матовий
  name_en: 300 gsm matte paper
  aliases:
  - папір 300 мат
  - 300gsm matte
  - матовий папір 300 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: paper_350g_gloss
  name_uk: Папір 350 г глянцевий
  name_en: 350 gsm gloss paper
  aliases:
  - папір 350 глянц
  - 350gsm gloss
  - мелований 350 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: paper_130g_matte
  name_uk: Папір 130 г матовий
  name_en: 130 gsm matte paper
  aliases:
  - папір 130 мат
  - 130gsm matte
  - матовий папір 130 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: banner_440g
  name_uk: Банер 440 г
  name_en: 440 gsm banner material
  aliases:
  - банер 440
  - 440gsm banner
  - банерна тканина 440 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: pvc_3mm
  name_uk: ПВХ 3 мм
  name_en: 3 mm PVC sheet
  aliases:
  - пвх 3мм
  - pvc 3mm
  - пластик пвх 3 мм
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: self_adhesive_vinyl
  name_uk: Самоклеюча вінілова плівка
  name_en: Self-adhesive vinyl
  aliases:
  - самоклейка вініл
  - self adhesive vinyl
  - вінілова плівка з клеєм
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
```

### `catalog/operations.yaml`

- SHA256: `8fdeccc5de0742ce02d5191eab27f4b855628b8c5a50a5794c5e8c213d843cd5`
- Bytes: `2508`

```yaml
catalog_type: operations
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: digital_print
  name_uk: Цифровий друк
  name_en: Digital print
  aliases:
  - цифровий друк
  - digital print
  - друк цифровий
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: large_format_print
  name_uk: Широкоформатний друк
  name_en: Large-format print
  aliases:
  - широкоформатний друк
  - large format print
  - друк на банері
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: cutting
  name_uk: Різання
  name_en: Cutting
  aliases:
  - різання
  - cutting
  - порізка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: lamination
  name_uk: Ламінування
  name_en: Lamination
  aliases:
  - ламінування
  - lamination
  - покриття плівкою
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: rounding
  name_uk: Заокруглення кутів
  name_en: Corner rounding
  aliases:
  - заокруглення кутів
  - corner rounding
  - округлення кутів
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: folding
  name_uk: Фальцювання
  name_en: Folding
  aliases:
  - фальцювання
  - folding operation
  - згинання продукції
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: scoring
  name_uk: Бігування
  name_en: Scoring
  aliases:
  - бігування
  - scoring
  - лінія згину
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
```

### `catalog/print_modes.yaml`

- SHA256: `4a0e5466a206a117ab0d094eb8fbb719302a6955410d4536066d25fc271f757e`
- Bytes: `1586`

```yaml
catalog_type: print_modes
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: color_4_0
  name_uk: 4+0
  name_en: Full color one side
  aliases:
  - 4+0
  - односторонній повноколір
  - full color one side
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
- id: color_4_4
  name_uk: 4+4
  name_en: Full color both sides
  aliases:
  - 4+4
  - двосторонній повноколір
  - full color both sides
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
- id: color_1_0
  name_uk: 1+0
  name_en: One color one side
  aliases:
  - 1+0
  - односторонній один колір
  - one color one side
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
- id: color_1_1
  name_uk: 1+1
  name_en: One color both sides
  aliases:
  - 1+1
  - двосторонній один колір
  - one color both sides
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
```

### `catalog/product_families.yaml`

- SHA256: `525b3c1ab5b7446dce72484078970b27e737ad533cb1a9c55eb681a78bd6a85e`
- Bytes: `2152`

```yaml
catalog_type: product_families
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: business_card
  name_uk: Візитка
  name_en: Business card
  aliases:
  - візитка
  - business card
  - карточка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for small-format contact cards.
- id: flyer
  name_uk: Флаєр
  name_en: Flyer
  aliases:
  - флаєр
  - flyer
  - рекламна листівка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for simple promotional leaflets.
- id: leaflet
  name_uk: Буклет
  name_en: Leaflet
  aliases:
  - буклет
  - leaflet
  - складна листівка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for folded informational products.
- id: poster
  name_uk: Плакат
  name_en: Poster
  aliases:
  - плакат
  - poster
  - афіша
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for posters and display prints.
- id: banner
  name_uk: Банер
  name_en: Banner
  aliases:
  - банер
  - banner
  - банерна продукція
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for large-format banners.
- id: sticker
  name_uk: Наліпка
  name_en: Sticker
  aliases:
  - наліпка
  - sticker
  - стікер
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for adhesive labels and stickers.
```

### `catalog/seeds/catalog_seed_v0_1.yaml`

- SHA256: `25654e306bacaee4c5350b83f9343a000075c1a242e8f02b7984ed6c3c019da7`
- Bytes: `9924`

```yaml
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: "0.1"
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: >
    Draft canonical seed for projection use by dependent ForPrint modules.
    This is not a final production contract.

materials:
  - id: paper_300g_matte
    name_uk: Папір 300 г матовий
    name_en: 300 gsm matte paper
    aliases:
      - папір 300 мат
      - 300gsm matte
      - матовий папір 300 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: paper_350g_gloss
    name_uk: Папір 350 г глянцевий
    name_en: 350 gsm gloss paper
    aliases:
      - папір 350 глянц
      - 350gsm gloss
      - мелований 350 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: paper_130g_matte
    name_uk: Папір 130 г матовий
    name_en: 130 gsm matte paper
    aliases:
      - папір 130 мат
      - 130gsm matte
      - матовий папір 130 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: banner_440g
    name_uk: Банер 440 г
    name_en: 440 gsm banner material
    aliases:
      - банер 440
      - 440gsm banner
      - банерна тканина 440 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: pvc_3mm
    name_uk: ПВХ 3 мм
    name_en: 3 mm PVC sheet
    aliases:
      - пвх 3мм
      - pvc 3mm
      - пластик пвх 3 мм
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: self_adhesive_vinyl
    name_uk: Самоклеюча вінілова плівка
    name_en: Self-adhesive vinyl
    aliases:
      - самоклейка вініл
      - self adhesive vinyl
      - вінілова плівка з клеєм
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

product_families:
  - id: business_card
    name_uk: Візитка
    name_en: Business card
    aliases:
      - візитка
      - business card
      - карточка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for small-format contact cards.

  - id: flyer
    name_uk: Флаєр
    name_en: Flyer
    aliases:
      - флаєр
      - flyer
      - рекламна листівка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for simple promotional leaflets.

  - id: leaflet
    name_uk: Буклет
    name_en: Leaflet
    aliases:
      - буклет
      - leaflet
      - складна листівка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for folded informational products.

  - id: poster
    name_uk: Плакат
    name_en: Poster
    aliases:
      - плакат
      - poster
      - афіша
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for posters and display prints.

  - id: banner
    name_uk: Банер
    name_en: Banner
    aliases:
      - банер
      - banner
      - банерна продукція
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for large-format banners.

  - id: sticker
    name_uk: Наліпка
    name_en: Sticker
    aliases:
      - наліпка
      - sticker
      - стікер
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for adhesive labels and stickers.

operations:
  - id: digital_print
    name_uk: Цифровий друк
    name_en: Digital print
    aliases:
      - цифровий друк
      - digital print
      - друк цифровий
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: large_format_print
    name_uk: Широкоформатний друк
    name_en: Large-format print
    aliases:
      - широкоформатний друк
      - large format print
      - друк на банері
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: cutting
    name_uk: Різання
    name_en: Cutting
    aliases:
      - різання
      - cutting
      - порізка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: lamination
    name_uk: Ламінування
    name_en: Lamination
    aliases:
      - ламінування
      - lamination
      - покриття плівкою
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: rounding
    name_uk: Заокруглення кутів
    name_en: Corner rounding
    aliases:
      - заокруглення кутів
      - corner rounding
      - округлення кутів
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: folding
    name_uk: Фальцювання
    name_en: Folding
    aliases:
      - фальцювання
      - folding operation
      - згинання продукції
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: scoring
    name_uk: Бігування
    name_en: Scoring
    aliases:
      - бігування
      - scoring
      - лінія згину
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

print_modes:
  - id: color_4_0
    name_uk: 4+0
    name_en: Full color one side
    aliases:
      - 4+0
      - односторонній повноколір
      - full color one side
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

  - id: color_4_4
    name_uk: 4+4
    name_en: Full color both sides
    aliases:
      - 4+4
      - двосторонній повноколір
      - full color both sides
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

  - id: color_1_0
    name_uk: 1+0
    name_en: One color one side
    aliases:
      - 1+0
      - односторонній один колір
      - one color one side
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

  - id: color_1_1
    name_uk: 1+1
    name_en: One color both sides
    aliases:
      - 1+1
      - двосторонній один колір
      - one color both sides
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

finishing_options:
  - id: none
    name_uk: Без постобробки
    name_en: No finishing
    aliases:
      - без постобробки
      - no finishing
      - без додаткової обробки
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: matte_lamination
    name_uk: Матова ламінація
    name_en: Matte lamination
    aliases:
      - матова ламінація
      - matte lamination
      - матове ламінування
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: gloss_lamination
    name_uk: Глянцева ламінація
    name_en: Gloss lamination
    aliases:
      - глянцева ламінація
      - gloss lamination
      - глянцеве ламінування
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: corner_rounding
    name_uk: Заокруглення кутів як опція
    name_en: Corner rounding finish
    aliases:
      - заокруглені кути
      - corner rounding finish
      - круглі кути
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: finishing_folding
    name_uk: Фальцювання як опція
    name_en: Folding finish
    aliases:
      - фальцювання як опція
      - folding finish
      - згин як постобробка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.
```

### `coordination/blueprint_awareness/document_review_ledger.yaml`

- SHA256: `85b0c4f1a4302dfbb2df357e2d20b89d57ebca810fb631866863a2eefe3354fc`
- Bytes: `4574`

```yaml
schema_version: module_document_awareness_ledger_v0_1
module: forprint_library
reviewed_documents:
- document_id: global_policy.readme
  path: coordination/global_policy/README.md
  content_hash: sha256:fb331a112cc3f6c5fe4e731b2d78bdc6a108f2e399d5837c492cf0732f235c18
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T12:17:30+00:00'
  module_commit: 03aaba7
  notes: Critical global policy baseline acknowledged before Library reference contract
    v0.2 work.
- document_id: global_policy.current_execution_focus
  path: coordination/global_policy/current_execution_focus.md
  content_hash: sha256:0cd73a28e0af34d896c1e8353988faa72da6733316ffeb0eba6608f5658bfb19
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T12:17:30+00:00'
  module_commit: 03aaba7
  notes: Critical global policy baseline acknowledged before Library reference contract
    v0.2 work.
- document_id: global_policy.ecosystem_module_map
  path: coordination/global_policy/ecosystem_module_map.md
  content_hash: sha256:622a5d9e0a378f42a14d1ac217ae359aa5b93b21b22cbc7a35fa237bb0b412c9
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T12:17:30+00:00'
  module_commit: 03aaba7
  notes: Critical global policy baseline acknowledged before Library reference contract
    v0.2 work.
- document_id: global_policy.forprint_project_doctrine
  path: coordination/global_policy/forprint_project_doctrine.md
  content_hash: sha256:c1b74e2fb9528477e6d50f7200b5b97a9df0bf05b941321b3a72aa9b585ab2a3
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T12:17:30+00:00'
  module_commit: 03aaba7
  notes: Critical global policy baseline acknowledged before Library reference contract
    v0.2 work.
- document_id: global_policy.forprint_strategic_control_plane_policy
  path: coordination/global_policy/forprint_strategic_control_plane_policy.md
  content_hash: sha256:a8529c57f059ea57b25cbb1fa833ea5bdd8725ecf1bbd6fcd2ba9a4acc615376
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T12:17:30+00:00'
  module_commit: 03aaba7
  notes: Critical global policy baseline acknowledged before Library reference contract
    v0.2 work.
- document_id: module_policy.forprint_library.module_policy
  path: coordination/module_policy/forprint_library/module_policy.md
  content_hash: sha256:aeb5b2ba25a09025f102ded77d5e096f8e991955320e4ff4853ef20f33ad7024
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T12:17:30+00:00'
  module_commit: 03aaba7
  notes: Library module policy baseline acknowledged before Library reference contract
    v0.2 work.
- document_id: outgoing_prompts.forprint_library.approved.2026_05_22_align_library_with_blueprint
  path: coordination/outgoing_prompts/forprint_library/approved/2026-05-22-align-library-with-blueprint.md
  content_hash: sha256:e6532245a564e9544bd244429294d0a9b909101ed5f6c3fdf704c0a98501bbf5
  module_review_status: applied
  reviewed_at: '2026-07-01T12:21:54+00:00'
  module_commit: b401557
  notes: Historical Library alignment prompt applied in previous checkpoints.
- document_id: outgoing_prompts.forprint_library.approved.2026_06_23_library_make_first_semantic_reference_readiness_v0_1
  path: coordination/outgoing_prompts/forprint_library/approved/2026-06-23__library__make_first_semantic_reference_readiness_v0_1.md
  content_hash: sha256:623f96540b9a7b909bb30002cdaf7a53cef8dfb8358ad82fcdb1ed783e93582d
  module_review_status: applied
  reviewed_at: '2026-07-01T12:21:54+00:00'
  module_commit: b401557
  notes: Make-first semantic reference readiness prompt already completed and accepted.
- document_id: outgoing_prompts.forprint_library.approved.2026_06_29_library_reference_contract_foundation_v0_2
  path: coordination/outgoing_prompts/forprint_library/approved/2026-06-29__library__reference_contract_foundation_v0_2.md
  content_hash: sha256:5e12b9d5e937c942f5d448e0773335cb385c9d91ef48ac31c964f596f161cc44
  module_review_status: applied
  reviewed_at: '2026-07-01T13:05:25+00:00'
  module_commit: '3428289'
  notes: 'Reference Contract Foundation v0.2 artifacts verified: docs, examples, schema,
    validator, tests, check-report and module validation.'
- document_id: outgoing_prompts.forprint_library.index
  path: coordination/outgoing_prompts/forprint_library/index.yaml
  content_hash: sha256:45ad4f594aabea6592a93940f69238348b42daf73746901980ea8e43de63af58
  module_review_status: acknowledged
  reviewed_at: '2026-07-01T14:48:46+00:00'
  module_commit: d2e1834
  notes: Library prompt queue index refreshed after Blueprint accepted Reference Contract
    Foundation v0.2.
```

### `coordination/prompts/active/2026-06-23__library__make_first_semantic_reference_readiness_v0_1.md`

- SHA256: `623f96540b9a7b909bb30002cdaf7a53cef8dfb8358ad82fcdb1ed783e93582d`
- Bytes: `6228`

```markdown
# Prompt: Library Make-First Semantic Reference Readiness v0.1

## Target module

`forprint_library`

## Working directory

`/srv/software_development/forprint-project/forprint_library`

## Blueprint directory

`/srv/software_development/forprint-project/forprint_system_blueprint`

## Purpose

Align ForPrint Library with the Blueprint Make Command Standard v0.2 and prepare a small semantic/reference readiness layer for downstream modules.

The goal is not to build the full production catalog.

The goal is to make Library easier to start, verify, and use as the canonical semantic/catalog authority for early Calculator, Operational Registry, Telegram Bot, and later CRM workflows.

## Strategic role reminder

ForPrint Library owns canonical semantic/catalog authority for:

```text
product/service naming
material naming
operation naming
aliases
technical card references
template references
contract definitions
semantic IDs
catalog meaning
```

Library must remain the semantic/catalog authority.

Library must not become:

```text
operational order registry
client database
payment/accounting truth
warehouse stock truth
CRM workflow engine
Telegram runtime adapter
Calculator pricing engine
production runtime controller
```

## Blueprint baseline

Use the current ForPrint System Blueprint.

Relevant Blueprint files:

```text
coordination/module_policy/forprint_library/module_policy.md
coordination/standards/make_command_standard.md
coordination/templates/module_makefile_standard.template.mk
coordination/outgoing_prompts/forprint_library/index.yaml
```

## Make-first workflow requirement

This prompt must follow the Blueprint Make Command Standard v0.2.

Do not rely on long raw command sequences as the normal workflow.

Before implementing the main semantic readiness scope, add or align the module Makefile with the standard high-level workflow targets if they are missing:

```text
blueprint-prompts-list
blueprint-prompts-check
blueprint-prompts-sync
blueprint-prompts
prompt-read
blueprint-sync
module-start
module-sync
module-validate
module-finish
report-clean
completion-packet-check
```

The exact implementation may remain module-specific, but the external command names must be standardized.

Required start command:

```bash
make module-start
```

Required validation command:

```bash
make module-validate
```

If completion packet automation is not yet implemented in Library, do not fake it. Either add a minimal safe implementation or clearly defer it and report the gap.

## Required starting verification

Run the standardized start workflow:

```bash
make module-start
```

Expected behavior:

* Blueprint repository is pulled.
* Blueprint paths are checked.
* Blueprint directives sync is executed or clearly deferred.
* Blueprint instruction intake is listed, checked and synchronized.
* Blueprint standards are listed, checked and synchronized.
* Blueprint outgoing prompts are listed, checked and synchronized.
* Module coordination metadata is checked.
* Current module status is shown.
* The active prompt is readable through `make prompt-read`.

If any required target is missing, implement or safely defer it according to the Blueprint Make Command Standard v0.2 before continuing.

## Main scope

After make-first alignment, implement a small semantic/reference readiness checkpoint.

This checkpoint should make Library more useful to other modules without expanding into a full catalog system.

Required direction:

```text
minimal semantic reference inventory;
stable sample canonical IDs;
alias/readiness examples;
downstream handoff notes for Calculator and Operational Registry;
clear boundaries for what Library owns and does not own;
check-report visibility for semantic readiness.
```

Suggested files may include existing or new Library-local equivalents of:

```text
docs/semantic_reference_readiness.md
docs/downstream_reference_contract_notes.md
examples/semantic_reference_preview.yaml
```

Use the module's existing structure where possible. Do not create duplicate concepts if better files already exist.

## Semantic readiness expectations

The checkpoint should show, at minimum:

```text
how a downstream module can refer to a canonical product/service/material/operation id;
how aliases are represented or planned;
how ambiguous naming should be reported;
how Library avoids owning pricing, stock, order state or accounting truth;
how local fixtures remain non-production and versioned.
```

## Required boundaries

Do not implement:

```text
production catalog database;
live API;
CRM integration;
Telegram integration;
Operational Registry write;
Calculator pricing logic;
warehouse stock logic;
accounting or payment logic;
1C sync/write;
automatic posting;
production runtime service.
```

Allowed:

```text
local docs;
local YAML/JSON examples;
local preview script if useful;
tests for semantic/reference examples;
check-report row showing readiness;
Makefile standard alignment.
```

## Required check-report visibility

If Library has a check-report runner, add or align rows for:

```text
Make-first workflow alignment
Semantic reference readiness
Blueprint prompt visibility
Blueprint standards visibility
```

If check-report is simpler at this stage, ensure the report clearly states whether each item is implemented, deferred, or warning-level.

## Required final validation

Use the standardized validation workflow:

```bash
make module-validate
```

If completion packet automation is available or added, also run:

```bash
make module-finish PACKET=coordination/completion_packets/examples/library_semantic_reference_readiness_v0_1.yaml
```

Expected behavior:

* check-report passes;
* check passes;
* governance-check passes;
* report-clean leaves the working tree reviewable;
* status-report shows the updated phase or readiness state;
* no generated runtime reports remain dirty unless intentionally tracked as source-of-truth.

## Final response required

Return:

```text
changed files
created or updated Makefile targets
semantic/reference readiness files
validation results
whether completion packet automation exists or is deferred
git status
commit recommendation
```

Do not commit until checks are green and the operator approves.
```

### `coordination/prompts/active/2026-06-29__library__reference_contract_foundation_v0_2.md`

- SHA256: `5e12b9d5e937c942f5d448e0773335cb385c9d91ef48ac31c964f596f161cc44`
- Bytes: `6410`

```markdown
# Prompt: Library Reference Contract Foundation v0.2

## Target module

`forprint_library`

## Working directory

`/srv/software_development/forprint-project/forprint_library`

## Blueprint directory

`/srv/software_development/forprint-project/forprint_system_blueprint`

## Current baseline

The latest known Library checkpoint is:

```text
781bb30 Refresh Library Blueprint standards snapshot
```

Previous Library semantic readiness work is already completed:

```text
935e51b Record Library semantic readiness completion
28fe2d0 Align Library make-first semantic readiness workflow
```

The module already has Make-first workflow targets and semantic/reference readiness checks.

## Purpose

Implement a small **Library Reference Contract Foundation v0.2** checkpoint.

The goal is to make Library references clearer and safer for downstream modules such as:

```text
calculator_engine
forprint_operational_registry
forprint_integration_gateway
telegram_bot
future forprint_crm
```

This is not a full production catalog implementation.

The goal is to define how other modules should refer to Library-owned semantic/catalog entities without copying Library ownership or inventing local canonical IDs.

## Required start workflow

Start with the standardized Make-first command:

```bash
make module-start
```

Then inspect the current state:

```bash
git status --short
git log -5 --oneline
find docs examples app tests coordination -maxdepth 3 -type f | sort | sed -n '1,260p'
```

Before adding files, review the current folder layout and respect the Blueprint Folder Architecture Policy.

Relevant Blueprint standard:

```text
coordination/standards/governance/folder_architecture_policy.md
```

Do not add new unrelated files into overcrowded flat directories. Prefer one thematic nesting level when useful.

## Main scope

Add or improve a small reference contract layer that documents and validates how downstream modules should store and exchange references to Library-owned entities.

The checkpoint should cover at minimum:

```text
canonical Library reference id format
reference type / entity type
display label
optional alias input
reference resolution status
source module
schema/version marker
deprecation handling
ambiguous/manual-review handling
unknown/unresolved references
example downstream payloads
```

The contract should make clear that downstream modules may store references to Library entities, but must not become the owner of Library semantic/catalog truth.

## Suggested files

Use existing structure where possible. Do not duplicate concepts if suitable files already exist.

Possible new or updated files:

```text
docs/reference_contract_foundation.md
docs/downstream_reference_contract_notes.md
examples/reference_contract/library_reference_examples.yaml
schemas/reference_contract/library_reference.schema.yaml
tests/content/test_library_reference_contract.py
```

If the repository already has better existing directories, use them instead.

Keep the folder structure shallow and thematic. Do not create deep nesting unless clearly justified.

## Expected contract examples

Include examples for at least:

```text
product_service
material
operation
unit
template
technical_card
```

Each example should show a safe downstream reference pattern.

Example concept, adapt to existing project conventions:

```yaml
library_reference:
  schema_version: library_reference_v0_2
  reference_type: product_service
  reference_id: product_service.business_card.standard
  display_label: Business card / standard
  resolution_status: library_reference_confirmed
  source_module: calculator_engine
  alias_input: "візитки стандарт"
```

Also include examples for:

```text
library_reference_pending
ambiguous_manual_review_required
deprecated_reference
unknown
```

## Boundary rules

Library owns:

```text
semantic/catalog IDs
product/service meaning
material meaning
operation meaning
template references
technical card references
aliases
deprecation rules
reference resolution semantics
```

Library must not own:

```text
order state
client database
pricing logic
warehouse stock truth
payment/accounting truth
CRM workflow state
Telegram runtime behavior
Integration Gateway delivery ledger
production runtime state
```

Do not implement:

```text
production catalog database
live API
CRM integration
Telegram integration
Operational Registry write
Calculator pricing logic
warehouse stock logic
accounting/payment logic
1C sync/write
automatic posting
production runtime service
```

Allowed:

```text
local docs
local YAML/JSON examples
schema files
tests for examples/schema
check-report visibility
small preview helper only if genuinely useful
```

## Check-report requirement

If possible, add or align one check-report row:

```text
Library reference contract foundation
```

Expected result:

```text
Reference contract docs, schemas and examples validate
```

The check should be OK only if the relevant docs/examples/schema exist and validate.

## Tests

Add focused tests only. Prefer thematic location according to Folder Architecture Policy.

Suggested test path:

```text
tests/content/test_library_reference_contract.py
```

Tests should verify:

```text
example file exists
required reference examples exist
schema/version field exists
reference_id/type/status fields exist
forbidden ownership language is not introduced
expected statuses are represented
```

Use the project's existing validation style where possible.

## Required validation

Run:

```bash
make lint
make test
make check-report
make governance-check
make module-validate
git diff --check
git status --short
```

If `make module-validate` regenerates reports or Blueprint standards snapshots, include only intentional tracked updates.

Do not commit until checks are green and the operator approves.

## Final response required

Return:

```text
changed files
created/updated docs
created/updated examples
created/updated schemas
created/updated tests
check-report rows added or changed
validation results
known deferred items
git status
commit recommendation
```

## Important

This checkpoint should remain small and safe.

Do not start full catalog expansion.

Do not create a production database.

Do not implement external integrations.

Do not change other modules.

Do not perform broad structural refactors unless needed for this checkpoint and explicitly justified.
```

### `coordination/prompts/active/current_blueprint_prompt.md`

- SHA256: `4a1e689270407aea87418b450cab99ad366868dcd042e61c38c12cd5978352ab`
- Bytes: `7214`

```markdown
# ForPrint Library Calculator Input Contract v0.1

## Coordination metadata

```yaml
prompt_id: forprint_library_calculator_input_contract_v0_1
module: forprint_library
status: ready
priority: critical
issued_by: forprint_system_blueprint
issued_date: 2026-07-17
previous_front: configurable_product_workbench_business_card_skeleton_v0_1
target_branch: feature/library-calculator-input-contract-v01
scope_class: library_read_contract
pricing_formula_scope_allowed: false
integration_write_scope_allowed: false
```

## 1. Purpose

Create a stable, deterministic, versioned, read-only Library contract that converts a validated configurable product selection into Calculator-ready reference input.

The first covered product is:

```text
product.business_card
```

This front unblocks the Library → Calculator critical path. It does not implement prices, production formulas, order creation, Telegram behavior, Logistics behavior, or external writes.

## 2. Preconditions

Start only after the previous business-card skeleton front is fully accepted and merged, including:

```text
docs/operations/business_card_skeleton_runbook.md
docs/operations/business_card_skeleton_recovery.md
```

Record:

- Library `main` commit;
- Blueprint `main` commit;
- active prompt ID;
- clean working tree;
- previous completion report path;
- previous recovery evidence.

## 3. Ownership boundary

Library owns:

- product identity;
- configurable parameter definitions;
- validation and normalization rules;
- reference identifiers;
- deterministic product-configuration projection;
- schema/version metadata.

Calculator owns:

- price formulas;
- pricing policy;
- numerical calculations;
- costs and margins;
- quote totals.

The Library contract must not contain monetary values, pricing coefficients, hidden formulas, vendor prices, production costs, discounts, taxes, or delivery prices.

## 4. Required public contract

Provide a typed, versioned contract equivalent in meaning to:

```python
CalculatorInputEnvelope(
    schema_version: str,
    product_id: str,
    configuration_id: str,
    normalized_parameters: Mapping[str, object],
    reference_ids: CalculatorReferenceIds,
    validation_snapshot: ValidationSnapshot,
)
```

Exact Python names may follow existing Library conventions, but semantics must remain stable and documented.

Required business-card projection:

```text
product_id
size
sides
material_ref
print_mode_ref
quantity
finishing_refs
artwork_source when supplied
```

Requirements:

- deterministic field ordering in serialized artifacts;
- stable normalization;
- no locale-dependent values;
- no database-object leakage;
- no mutable internal-model leakage;
- no implicit defaults hidden from Calculator;
- explicit schema version;
- explicit validation result;
- explicit error taxonomy.

## 5. Error taxonomy

At minimum distinguish:

```text
unknown_product
invalid_configuration
missing_required_parameter
invalid_reference
unsupported_projection_version
internal_contract_error
```

Errors must be typed or structurally stable and safe for Calculator consumption.

Do not expose stack traces or internal persistence details as public contract data.

## 6. API behavior

Provide a read-only entry point equivalent in meaning to:

```python
build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope
```

Rules:

- the same valid input produces semantically identical output;
- input mappings are not mutated;
- finishing references are normalized deterministically;
- quantity validation remains owned by Library;
- references remain identifiers, not expanded pricing records;
- unsupported products fail explicitly;
- no network calls;
- no writes;
- no Calculator import dependency inside Library.

## 7. Serialization fixtures

Add canonical fixtures for:

- minimal valid business card;
- business card with finishing;
- business card with artwork source;
- invalid missing material;
- invalid print-mode reference;
- invalid quantity.

Machine-readable fixture output must have a documented stable path.

## 8. Compatibility

Preserve:

- existing `product.business_card` behavior;
- current configurable-product workbench API;
- current validation behavior unless a documented defect is found;
- all existing public imports;
- current tests and fixtures;
- module policy and reporting contracts.

Any unavoidable public change requires:

- compatibility adapter;
- migration note;
- contract test;
- Blueprint review before merge.

## 9. Documentation and recovery gate

Create or update:

```text
docs/architecture/library_calculator_input_contract.md
docs/operations/library_calculator_input_contract_runbook.md
docs/operations/library_calculator_input_contract_recovery.md
coordination/reports/completion/forprint_library_calculator_input_contract_v0_1_completion.md
```

Documentation must explain:

- ownership boundary;
- schema versioning;
- normalization;
- deterministic serialization;
- error taxonomy;
- Calculator consumption example;
- verification commands;
- rollback;
- recovery from incompatible schema or fixture regressions.

## 10. Required tests

Add focused tests for:

1. valid minimal business-card projection;
2. valid full business-card projection;
3. deterministic output for semantically equal input;
4. input mapping is not mutated;
5. finishing references normalize deterministically;
6. optional artwork-source behavior;
7. missing required parameter;
8. invalid material reference;
9. invalid print-mode reference;
10. invalid quantity;
11. unknown product;
12. unsupported schema version;
13. stable serialized fixture;
14. no monetary fields in contract output;
15. no network or write side effects;
16. backward compatibility with existing business-card tests.

Preserve the complete existing Library test suite.

## 11. Forbidden scope

Do not implement:

- price formulas;
- quote totals;
- cost, margin, discount, tax, or currency calculations;
- Calculator internals;
- canonical-order creation;
- Telegram Bot changes;
- Logistics changes;
- CRM, Gateway, 1C, payment, stock, or production writes;
- production deployment.

Do not merge to `main` before Blueprint acceptance.

## 12. Required validation

Run and report exact exit codes and counts:

```bash
make lint
make format-check
make check
make governance-check
make module-validate
make check-report
make check-report-full
git diff --check
git status -sb
```

Also run focused Calculator-input contract tests separately.

Human-facing reports must be colored by default. Use `NO_COLOR=1` only for machine-readable evidence.

## 13. Completion response

Return:

- repository;
- branch;
- base commit;
- final commit;
- Blueprint commit consumed;
- changed files grouped by area;
- public contract summary;
- schema version;
- fixture paths;
- focused test counts;
- full-suite count;
- governance/report results;
- docs/runbook/recovery paths;
- compatibility confirmation;
- forbidden-scope confirmation;
- blockers and deferred work;
- clean `git status -sb`;
- readiness for Blueprint review.

Final line:

```text
RESULT: READY_FOR_BLUEPRINT_REVIEW | BLOCKED | INCOMPLETE
```
```

### `coordination/prompts/index.yaml`

- SHA256: `c4e1d697446581ed7018e7f6e2ea27674526c9c04f3bbfb1b06c95f2debc6d15`
- Bytes: `91`

```yaml
module_id: forprint_library
index_type: received_prompts
updated_at: "2026-06-05"
items: []
```

### `coordination/reports/completion/2026-06-29__forprint_library__report__reference-contract-foundation-v0-2.md`

- SHA256: `5be21bcfbc5320badce7bd15489e2ada24d4033e75fcbe87abd5f35c5a720576`
- Bytes: `3581`

```markdown
# ForPrint Library Reference Contract Foundation v0.2

## Completion Report

Report ID: `2026-06-29__forprint_library__report__reference-contract-foundation-v0-2`

Module: `forprint_library`

Status: `completed_pending_blueprint_review`

Date: `2026-06-29`

## Blueprint prompt

Prompt ID: `reference_contract_foundation_v0_2`

Prompt path:

```text
/srv/software_development/forprint-project/forprint_system_blueprint/coordination/outgoing_prompts/forprint_library/approved/2026-06-29__library__reference_contract_foundation_v0_2.md
```

## Implementation commit

```text
78bd7e1 Add Library reference contract foundation
```

Push status: `pushed to origin/main`

## Changed files

```text
docs/architecture/reference_contract_foundation.md
examples/reference_contract/library_reference_examples.yaml
schemas/reference_contract/library_reference.schema.yaml
scripts/reference_contract/validate_library_reference_contract.py
tests/content/test_library_reference_contract.py
scripts/run_library_checks.py
reports/library_check_report.json
reports/library_check_report.md
```

## Created or updated docs

```text
docs/architecture/reference_contract_foundation.md
```

## Created or updated examples

```text
examples/reference_contract/library_reference_examples.yaml
```

## Created or updated schemas

```text
schemas/reference_contract/library_reference.schema.yaml
```

## Created or updated tests

```text
tests/content/test_library_reference_contract.py
```

## Reference contract scope

The checkpoint defines a small Library reference contract layer.

It covers:

```text
canonical Library reference id format
reference type / entity type
display label
optional alias input
reference resolution status
source module
schema/version marker
deprecation handling
ambiguous/manual-review handling
unknown/unresolved references
example downstream payloads
```

Reference examples cover:

```text
product_service
material
operation
unit
template
technical_card
```

Resolution statuses represented:

```text
library_reference_confirmed
library_reference_pending
ambiguous_manual_review_required
deprecated_reference
unknown
```

## Check-report visibility

The check report now includes:

```text
Library reference contract foundation
```

Expected result:

```text
Reference contract docs, schemas and examples validate
```

Status: `OK`.

## Validation results

```text
reference contract validator: OK
make lint: OK
make test: 94 passed
make check-report: OK
make governance-check: OK
make module-validate: OK
git diff --check: OK
```

## Manual Blueprint mode note

Makefile active prompt was intentionally not changed.

The project is temporarily using manual chat-based Blueprint prompt
intake and reporting while the work policy is being adjusted.

## Deferred items

```text
production catalog database
live API
CRM integration
Telegram integration
Operational Registry write
Calculator pricing logic
warehouse stock logic
accounting/payment logic
1C sync/write
automatic posting
production runtime service
formal completion packet automation
```

## Blueprint review request

Blueprint should review Library reference contract foundation v0.2.

Requested decisions:

1. Confirm the Library reference payload shape for downstream use.
2. Decide Operational Registry projection expectations.
3. Decide Calculator Engine reference input expectations.
4. Decide Integration Gateway and Telegram reference handoff guidance.
5. Decide whether v0.3 should follow after downstream feedback.

## Recommended next step

Wait for Blueprint review and downstream alignment guidance.
```

### `coordination/reports/completion/2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3.md`

- SHA256: `1baee0bc5830ef808d1db04918a184c4b1d93a79cf25474b71c8c94bd217bde2`
- Bytes: `4274`

```markdown
# ForPrint Library Completion Report

## Subject

Library Reference Consumption Pilot v0.3

## Module

`forprint_library`

## Prompt ID

`library_reference_consumption_pilot_v0_3`

## Status

`completed_pending_blueprint_review`

## Date

`2026-07-08`

## Blueprint prompt path

Read-only reference:

```text
/srv/software_development/forprint-project/forprint_system_blueprint/coordination/outgoing_prompts/forprint_library/approved/2026-07-08__library__reference_consumption_pilot_v0_3.md
Implementation commit
7e000cb Add Library reference consumption pilot
Purpose

This checkpoint adds a small, controlled, local and read-only reference
consumption pilot inside ForPrint Library.

The pilot demonstrates how downstream ForPrint modules may consume
Library-owned reference contract identifiers without making Library responsible
for downstream runtime behavior.

Completed scope

The implementation added:

examples/reference_consumption/library_reference_consumption_examples.yaml
schemas/reference_consumption/library_reference_consumption.schema.yaml
scripts/reference_consumption/validate_reference_consumption_pilot.py
docs/architecture/reference_consumption_pilot.md
tests/coordination/test_reference_consumption_pilot.py
scripts/run_library_checks.py
reports/library_check_report.json
reports/library_check_report.md
Consumer examples

The pilot includes valid local examples for:

calculator_engine consuming a Library product/service reference as pricing context
telegram_bot consuming a Library template reference as a channel-local hint
forprint_operational_registry consuming a Library material reference as foreign-domain metadata

The pilot also includes invalid examples for:

unknown Library reference id
consumer semantic redefinition
consumer runtime ownership/write fields
Reference IDs used

The pilot consumes controlled reference contract example IDs from:

examples/reference_contract/library_reference_examples.yaml

Examples include:

product_service.business_card.standard
template.business_card.90x50
material.paper.mondi_color_copy_300gsm

These are controlled reference contract examples, not production catalog records.

Validation behavior

The validator confirms that:

referenced Library IDs exist in the existing reference contract examples
valid consumer payloads pass
invalid consumer payloads fail clearly
consumer payloads do not redefine Library-owned semantics
consumer payloads do not introduce downstream runtime ownership into Library
human-readable preview output renders
Check-report visibility

The Library check report now includes:

Library reference consumption pilot

Expected result:

Reference consumption examples, schema and validator work

Status:

OK
Validation performed

The implementation was validated with:

reference consumption validator: OK
reference consumption preview: OK
focused tests: 7 passed
make lint: OK
make test: 115 passed
make check-report: OK
make check: OK
make governance-check: OK
make module-validate: OK
git diff --check: OK
Repository ownership boundary

All files were created or updated inside the Library repository only.

Library did not write into:

/srv/software_development/forprint-project/forprint_system_blueprint/...

Blueprint-side incoming report registration, review metadata, prompt queue
acceptance and next-prompt issuance remain Blueprint-owned actions.

Explicit non-goals preserved
No Configurable Product Workbench
No Business Card Skeleton
No product modeling UI
No production catalog database
No live API
No 1C import
No 1C synchronization
No Calculator integration
No Telegram Bot integration
No Operational Registry write
No production write
No price calculation
No material write-off logic
No Blueprint repository writes

Completion packet automation is not used for this checkpoint.

The module-side completion report, reports index and current status files are
updated by a local Library closure exporter.

This does not perform Blueprint-side intake, review or acceptance.

Readiness statement

Library is ready for Blueprint review of:

library_reference_consumption_pilot_v0_3

The next step belongs to Blueprint: review this module-side completion output,
record Blueprint-side acceptance or return-for-fix metadata, and decide the next
approved prompt.
```

### `coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`

- SHA256: `8ce090e65bee5106a99de46a0ffef5cf78b65dd6037faf098452dac6f8376958`
- Bytes: `5021`

```markdown
# ForPrint Library completion report

## Prompt

- Prompt ID: `library_configurable_product_workbench_business_card_skeleton_v0_1`
- Prompt title: Library Configurable Product Workbench v0.1 — Business Card Skeleton
- Blueprint prompt path: `coordination/outgoing_prompts/forprint_library/approved/2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1.md`
- Product ID: `product.business_card`
- Status: `completed_pending_blueprint_review`

## Module commits

- Implementation commit: `b8eb062` — Add Library business card product skeleton.
- Initial completion/closure commit: `7a7cb85` — Record Library business card skeleton completion.
- Cleanup closure commit before this reporting cleanup: `ad99e0a` — Clean business card closure exporter whitespace.
- Latest module commit before this cleanup pass: `ad99e0a`.
- Final reporting cleanup commit before Blueprint acceptance verification: `1694215` — Finalize Library business card completion metadata.

The final reporting cleanup commit before this verification pass is `1694215`. If this metadata-only patch creates another cleanup commit, that new commit is reported in chat after push rather than embedded inside its own tracked content.

## Summary

Library Configurable Product Workbench v0.1 — Business Card Skeleton is
completed and ready for Blueprint review.

The Library repository now contains the first controlled configurable product
reference for business cards / візитки: `product.business_card`.

The product card is intentionally scoped as a Library reference object. It
describes stable names, aliases, constructor parameters, references to existing
Library catalog IDs, consumer notes, validation and preview support.

## Product card artifacts

- `catalog/configurable_products/business_card.yaml`
- `schemas/configurable_product.schema.yaml`
- `examples/product_cards/business_card_product_card.yaml`
- `docs/architecture/configurable_product_workbench.md`
- `docs/architecture/business_card_skeleton.md`
- `scripts/product_workbench/validate_business_card_product.py`
- `scripts/product_workbench/preview_business_card_product.py`
- `tests/content/test_business_card_product_card.py`

## Reporting and closure artifacts

- `coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`
- `coordination/reports/index.yaml`
- `coordination/status/current_status.yaml`
- `coordination/status/current_status.md`
- `coordination/status/next_questions_for_blueprint.md`
- `scripts/coordination/export_business_card_skeleton_closure.py`
- `tests/coordination/test_business_card_skeleton_closure.py`

## Constructor parameters

- `size`
- `sides`
- `material_ref`
- `print_mode_ref`
- `quantity`
- `finishing_refs`
- `artwork_source`

## Consumer notes

Telegram Bot may use `product.business_card` and aliases as route hints only.

Calculator Engine may later use constructor parameters as pricing input context,
but no formula is implemented in Library.

Operational Registry may store `product.business_card` as foreign-domain metadata, but
Library does not create operational records.

## Checks passed

- Business card product skeleton: OK
- Business card product preview: OK
- Business card validator: OK
- Business card preview: OK
- Focused business card tests: 8 passed
- Full pytest suite: 137 passed
- Ruff lint: OK
- `make check-report`: OK
- `make check`: OK
- `make governance-check`: OK
- `make module-validate`: OK
- `git diff --check`: OK

## Known warnings

Blueprint module directives index is missing/deferred for `forprint_library`.

Document awareness still reports unseen Blueprint documents. This is advisory
and outside this checkpoint's implementation scope.

## Boundary confirmation

- No full product catalog.
- No product modeling UI.
- No production catalog database.
- No live API.
- No 1C import.
- No 1C synchronization.
- No Calculator integration.
- No Telegram Bot integration.
- No Operational Registry write.
- No CRM write.
- No Website write.
- No price calculation.
- No final price formula.
- No material write-off logic.
- No warehouse stock truth.
- No production task creation.
- No real client or order data.
- No production runtime.
- No Blueprint repository writes.

## Completion packet automation

Generic completion packet automation was not available or was deferred for this module step.

A Library-side exporter generated the original required module-side coordination files inside the Library repository.

The final reporting cleanup adjusted completion metadata formatting only and did not write into the Blueprint repository.

## Blueprint repository write confirmation

No files were written directly into the Blueprint repository.

All completion metadata in this cleanup pass is stored inside the Library
repository.


## Governance closeout documentation

- `docs/operations/business_card_skeleton_runbook.md`
- `docs/operations/business_card_skeleton_recovery.md`

## Open questions

No open questions.
```

### `coordination/reports/completion/forprint_library_calculator_input_contract_v0_1_completion.md`

- SHA256: `8b2ef36caf5227fbc6f3c76d4f4e285ca864ed2bcd2c5e7ffc1cf10590d68cf4`
- Bytes: `7485`

```markdown
# ForPrint Library Calculator Input Contract v0.1 Completion Report

## Prompt

- Prompt ID: `forprint_library_calculator_input_contract_v0_1`
- Prompt title: ForPrint Library Calculator Input Contract v0.1
- Module: `forprint_library`
- Repository: `/srv/software_development/forprint-project/forprint_library`
- Branch: `feature/library-calculator-input-contract-v01`
- Status: `completed_pending_blueprint_review`
- Scope class: `library_read_contract`
- Product covered first: `product.business_card`

## Commits

- Base Library commit: `01f78ea` (`01f78ea0687f8a9c9bee99d3f1042cda0fce2d55`)
- Final Library implementation commit: `0b8cbce` (`0b8cbce6b4c4dc0d37f9d9fcb4b58d20929dd4a7`)
- Blueprint commit consumed during validation: `3f18787` (`3f1878763c052afca9cdee28b5dfe45c6bb60f5f`)
- Blueprint branch observed during final validation: `main`

## Summary

Library now provides a stable, deterministic, versioned, read-only Calculator
input contract for `product.business_card`.

The contract converts a validated configurable product selection into a
Calculator-ready reference input envelope. It preserves Library ownership of
product identity, configurable parameter definitions, validation,
normalization, reference identifiers and schema metadata.

Calculator remains the owner of price formulas, pricing policy, numerical
calculation, costs, margins and quote totals.

## Public contract

Public package:

- `app/forprint_library/calculator_input/__init__.py`
- `app/forprint_library/calculator_input/contract.py`

Public entry point:

```python
build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope
```

Public envelope semantics:

```python
CalculatorInputEnvelope(
    schema_version: str,
    product_id: str,
    configuration_id: str,
    normalized_parameters: Mapping[str, object],
    reference_ids: CalculatorReferenceIds,
    validation_snapshot: ValidationSnapshot,
)
```

Schema version:

```text
calculator_input_envelope_v0_1
```

## Business-card projection

The `product.business_card` projection includes:

- `product_id`
- `size`
- `sides`
- `material_ref`
- `print_mode_ref`
- `quantity`
- `finishing_refs`
- `artwork_source` when supplied

## Error taxonomy

Stable public error types:

- `unknown_product`
- `invalid_configuration`
- `missing_required_parameter`
- `invalid_reference`
- `unsupported_projection_version`
- `internal_contract_error`

Errors are typed, structurally stable and safe for Calculator consumption.

## Determinism and safety

Confirmed behavior:

- deterministic field ordering in serialized artifacts;
- stable normalization;
- deterministic `finishing_refs` sorting by catalog and id;
- duplicate finishing references collapse deterministically;
- no locale-dependent values;
- no database-object leakage;
- no mutable internal-model leakage;
- no implicit defaults hidden from Calculator;
- explicit schema version;
- explicit validation snapshot;
- no network calls;
- no writes;
- no Calculator import dependency inside Library.

## Schema and fixtures

Schema:

- `schemas/calculator_input/calculator_input_envelope.schema.yaml`

Canonical machine-readable fixtures:

- `examples/calculator_input_contract/minimal_valid_business_card.yaml`
- `examples/calculator_input_contract/business_card_with_finishing.yaml`
- `examples/calculator_input_contract/business_card_with_artwork_source.yaml`
- `examples/calculator_input_contract/invalid_missing_material.yaml`
- `examples/calculator_input_contract/invalid_print_mode_reference.yaml`
- `examples/calculator_input_contract/invalid_quantity.yaml`

Validator:

- `scripts/calculator_input/validate_calculator_input_contract.py`

Tests:

- `tests/content/test_calculator_input_contract.py`
- `tests/content/test_business_card_product_card.py`

## Documentation and recovery

Architecture document:

- `docs/architecture/library_calculator_input_contract.md`

Operations runbook:

- `docs/operations/library_calculator_input_contract_runbook.md`

Recovery guide:

- `docs/operations/library_calculator_input_contract_recovery.md`

Completion report:

- `coordination/reports/completion/forprint_library_calculator_input_contract_v0_1_completion.md`

## Validation evidence

Focused validation:

```text
PYTHONPATH=app .venv_forprint_library/bin/python -m pytest \
  tests/content/test_calculator_input_contract.py \
  tests/content/test_business_card_product_card.py

Result: 25 passed
```

Fixture validator:

```text
PYTHONPATH=app .venv_forprint_library/bin/python \
  scripts/calculator_input/validate_calculator_input_contract.py

Result: OK: Library Calculator input contract validates
```

Required validation:

```text
make lint
Result: LINT_EXIT: 0

make format-check
Result: FORMAT_CHECK_EXIT: 0

make check
Result: CHECK_EXIT: 0
Full suite: 160 passed

make governance-check
Result: GOVERNANCE_CHECK_EXIT: 0

make module-validate
Result: MODULE_VALIDATE_EXIT: 0

make check-report
Result: CHECK_REPORT_EXIT: 0

make check-report-full
Result: CHECK_REPORT_FULL_EXIT: 0

git diff --check
Result: DIFF_CHECK_FINAL_EXIT: 0
```

## Changed files grouped by area

### Contract API

- `app/forprint_library/calculator_input/__init__.py`
- `app/forprint_library/calculator_input/contract.py`

### Schema and fixtures

- `schemas/calculator_input/calculator_input_envelope.schema.yaml`
- `examples/calculator_input_contract/minimal_valid_business_card.yaml`
- `examples/calculator_input_contract/business_card_with_finishing.yaml`
- `examples/calculator_input_contract/business_card_with_artwork_source.yaml`
- `examples/calculator_input_contract/invalid_missing_material.yaml`
- `examples/calculator_input_contract/invalid_print_mode_reference.yaml`
- `examples/calculator_input_contract/invalid_quantity.yaml`

### Validation and tests

- `scripts/calculator_input/validate_calculator_input_contract.py`
- `tests/content/test_calculator_input_contract.py`

### Documentation and recovery

- `docs/architecture/library_calculator_input_contract.md`
- `docs/operations/library_calculator_input_contract_runbook.md`
- `docs/operations/library_calculator_input_contract_recovery.md`

## Compatibility confirmation

Preserved:

- existing `product.business_card` behavior;
- current configurable-product workbench API;
- current validation behavior;
- current public imports outside the new `calculator_input` package;
- existing business-card tests and fixtures;
- module policy and reporting contracts.

## Forbidden-scope confirmation

Not implemented:

- price formulas;
- quote totals;
- cost, margin, discount, tax or currency calculations;
- Calculator internals;
- canonical-order creation;
- Telegram Bot changes;
- Logistics changes;
- CRM changes;
- Gateway changes;
- 1C changes;
- payment writes;
- stock writes;
- production writes;
- production deployment;
- Blueprint repository writes.

## Known warnings and deferred work

Blueprint module directives index remains missing/deferred for `forprint_library`.
This is an existing governance warning and not a blocker for this Library
contract completion.

Blueprint repository refactor is ongoing separately. This completion report
does not restore or modify Blueprint WIP.

Blueprint acceptance and merge to `main` remain deferred until Blueprint review.

## Final status

Ready for Blueprint review after this module-side completion report is committed
and pushed.

RESULT: READY_FOR_BLUEPRINT_REVIEW
```

### `coordination/reports/index.yaml`

- SHA256: `599f84cf2459181a8da8deeb8d159c817a76bb524b5793172a9e315fc976d393`
- Bytes: `7151`

```yaml
module_id: forprint_library
index_type: coordination_reports
updated_at: '2026-07-08'
completion_reports:
- id: 2026-06-06__forprint_library__report__catalog-seed-v0-1-and-coordination-bootstrap
  path: coordination/reports/completion/2026-06-06__forprint_library__report__catalog-seed-v0-1-and-coordination-bootstrap.md
  status: completed
  checkpoint: checkpoint_d
  summary: Canonical Catalog Seed v0.1 and coordination bootstrap completion report.
- id: 2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1
  path: coordination/reports/completion/2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1.md
  status: completed
  phase: shared_operational_dictionary_v0_1
  summary: Shared Operational Dictionary v0.1 completion report.
- id: 2026-06-25__forprint_library__report__make-first-semantic-reference-readiness-v0-1
  module_id: forprint_library
  type: completion_report
  status: completed_pending_blueprint_review
  path: coordination/reports/completion/2026-06-25__forprint_library__report__make-first-semantic-reference-readiness-v0-1.md
  related_prompt_id: make_first_semantic_reference_readiness_v0_1
  blueprint_commit: 2d49d63
  implementation_commit: 28fe2d0
  created_at: '2026-06-25'
- id: 2026-06-29__forprint_library__report__reference-contract-foundation-v0-2
  module_id: forprint_library
  type: completion_report
  status: accepted_by_blueprint
  path: coordination/reports/completion/2026-06-29__forprint_library__report__reference-contract-foundation-v0-2.md
  related_prompt_id: reference_contract_foundation_v0_2
  implementation_commit: 78bd7e1
  closure_commit: 6343f65
  blueprint_acceptance_commit: 059d7c1
  created_at: '2026-06-29'
- id: 2026-07-03__forprint_library__report__coordination-foundation-alignment-v0-1
  module_id: forprint_library
  type: completion_report
  status: completed_pending_blueprint_review
  path: coordination/reports/completion/2026-07-03__forprint_library__report__coordination-foundation-alignment-v0-1.md
  related_prompt_id: library_coordination_foundation_alignment_v0_1
  implementation_commit: 02e2cad
  closure_commit: 8031d3e
  created_at: '2026-07-03'
- id: 2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3
  module_id: forprint_library
  type: completion_report
  status: completed_pending_blueprint_review
  path: coordination/reports/completion/2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3.md
  related_prompt_id: library_reference_consumption_pilot_v0_3
  implementation_commit: 7e000cb
  created_at: '2026-07-08'
commit_reports:
- id: checkpoint_a
  commit: e2f9302
  message: Bootstrap Library coordination and check report standard
  status: pushed
- id: checkpoint_b
  commit: bb7a317
  message: Add Library canonical catalog seed v0.1
  status: pushed
- id: checkpoint_c
  commit: 967d74a
  message: Document Library catalog boundaries and dependent usage
  status: pushed
- id: shared_dictionary_checkpoint_a
  commit: 18900ee
  message: Add shared operational dictionary files
  status: pushed
- id: shared_dictionary_checkpoint_b
  commit: 2fc7694
  message: Add shared dictionary resolver and preview
  status: pushed
- id: shared_dictionary_checkpoint_c
  commit: pending
  message: Finalize shared operational dictionary checkpoint
  status: pending_final_commit
- id: forprint_library_make_first_semantic_readiness_commit_28fe2d0
  module_id: forprint_library
  type: commit_record
  status: pushed
  commit: 28fe2d0
  message: Align Library make-first semantic readiness workflow
  related_prompt_id: make_first_semantic_reference_readiness_v0_1
  created_at: '2026-06-25'
- id: forprint_library_reference_contract_foundation_commit_78bd7e1
  module_id: forprint_library
  type: commit_record
  status: pushed
  commit: 78bd7e1
  message: Add Library reference contract foundation
  related_prompt_id: reference_contract_foundation_v0_2
  created_at: '2026-06-29'
- id: forprint_library_reference_contract_foundation_completion_commit_6343f65
  module_id: forprint_library
  type: commit_record
  status: pushed
  commit: 6343f65
  message: Record Library reference contract completion
  related_prompt_id: reference_contract_foundation_v0_2
  completion_report: coordination/reports/completion/2026-06-29__forprint_library__report__reference-contract-foundation-v0-2.md
  created_at: '2026-06-29'
- id: forprint_library_coordination_foundation_alignment_commit_02e2cad
  module_id: forprint_library
  type: commit_record
  status: pushed
  commit: 02e2cad
  message: Add Library coordination foundation alignment
  related_prompt_id: library_coordination_foundation_alignment_v0_1
  created_at: '2026-07-03'
- id: forprint_library_coordination_foundation_alignment_completion_commit_8031d3e
  module_id: forprint_library
  type: commit_record
  status: pushed
  commit: 8031d3e
  message: Record Library coordination foundation alignment completion
  related_prompt_id: library_coordination_foundation_alignment_v0_1
  completion_report: coordination/reports/completion/2026-07-03__forprint_library__report__coordination-foundation-alignment-v0-1.md
  created_at: '2026-07-03'
- id: 2026-07-07__forprint_library__commit-report__coordination-foundation-alignment-v0-1
  module_id: forprint_library
  type: commit_report
  status: pushed
  path: coordination/reports/commits/2026-07-07__forprint_library__commit-report__coordination-foundation-alignment-v0-1.md
  related_prompt_id: library_coordination_foundation_alignment_v0_1
  implementation_commit: 02e2cad
  closure_commit: 8031d3e
  created_at: '2026-07-07'
- id: forprint_library_reference_consumption_pilot_commit_7e000cb
  module_id: forprint_library
  type: commit_record
  status: pushed
  commit: 7e000cb
  message: Add Library reference consumption pilot
  related_prompt_id: library_reference_consumption_pilot_v0_3
  completion_report: coordination/reports/completion/2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3.md
  created_at: '2026-07-08'
schema_version: module_reports_index_v0_1
reports:
- id: 2026-07-11__forprint_library__report__business-card-skeleton-v0-1
  type: completion_report
  prompt_id: library_configurable_product_workbench_business_card_skeleton_v0_1
  title: Library Configurable Product Workbench v0.1 — Business Card Skeleton
  status: completed_pending_blueprint_review
  product_id: product.business_card
  path: coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md
  report_file: coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md
  implementation_commit: b8eb062
  completion_commits:
  - 7a7cb85
  - ad99e0a
  - '1694215'
  final_cleanup_commit: reported_after_push
  blueprint_prompt_path: coordination/outgoing_prompts/forprint_library/approved/2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1.md
  blueprint_repository_written: false
  checks_passed:
  - make governance-check
  - make check
  - make check-report
  - make module-validate
  - git diff --check
  created_at: '2026-07-11'
  updated_at: '2026-07-13'
```

### `coordination/standards/blueprint_standards_available_snapshot.txt`

- SHA256: `7ef37f3a7ced6efd379176078a0dc0533ecfcaa79828d5c301f22977c348891f`
- Bytes: `4992`

```text
module_id: forprint_library
snapshot_type: blueprint_standards_available_snapshot
blueprint_root: /srv/software_development/forprint-project/forprint_system_blueprint
standards_files:
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/configuration_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/coordination_metadata_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/current_status_extension_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/directive_index_schema.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/governance/coordination_document_awareness_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/governance/folder_architecture_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/governance/index.yaml
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/governance/prompt_queue_navigation_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/governance/README.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/governance/standards_directory_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/index.yaml
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/make_command_standard.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/architecture_topology_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/data_ownership_and_storage_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/gateway_responsibility_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/index.yaml
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/module_global_context_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/module_interaction_reliability_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/modular_topology_and_resilience/README.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_alignment_policy.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_assistant_start_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_coordination_records_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_governance_make_targets.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_governance_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_make_target_contract.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_outgoing_prompt_pull_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_pre_commit_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_prompt_completion_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/module_standards_awareness_protocol.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/project_structure_standard.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/README.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/repository_structure_baseline.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/testing_and_check_report_standard.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/third_party_reuse/index.yaml
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/third_party_reuse/README.md
  - /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards/third_party_reuse/third_party_reuse_policy.md
```

### `coordination/status/current_status.md`

- SHA256: `f5e4ae8e88aa5983f02cbba017bba96d941258022253881fd57f98bda5d422b7`
- Bytes: `2722`

```markdown
# ForPrint Library Current Status

## Status

`completed_pending_blueprint_review`

Previous rolling status alias: `business_card_skeleton_v0_1_ready_pending_blueprint_review`.

## Current phase

`business_card_skeleton_v0_1`

## Completed prompt

- Prompt ID: `library_configurable_product_workbench_business_card_skeleton_v0_1`
- Product ID: `product.business_card`
- Implementation commit: `b8eb062`
- Completion commits before this cleanup:
  - `7a7cb85`
  - `ad99e0a`
- Final cleanup commit before Blueprint acceptance verification: `1694215`

The exact final cleanup commit hash must be reported after `git push`.

## Completion report

`coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`

## Summary

Library Configurable Product Workbench v0.1 — Business Card Skeleton is
completed and ready for Blueprint review.

The Library repository contains `product.business_card` as the first controlled
configurable product reference for business cards / візитки.

## Checks passed

- Business card validator: OK
- Business card preview: OK
- Focused business card tests: 8 passed
- Full pytest suite: 137 passed
- Ruff lint: OK
- `make check-report`: OK
- `make check`: OK
- `make governance-check`: OK
- `make module-validate`: OK
- `git diff --check`: OK

## Blueprint repository writes

No Blueprint repository writes.

No files were written directly into the Blueprint repository.

## Boundaries preserved

- No full product catalog.
- No product modeling UI.
- No production catalog database.
- No live API.
- No 1C import.
- No 1C synchronization.
- No Calculator integration.
- No Telegram Bot integration.
- No Operational Registry write.
- No CRM write.
- No Website write.
- No price calculation.
- No final price formula.
- No material write-off logic.
- No warehouse stock truth.
- No production task creation.
- No real client or order data.
- No production runtime.

## Previous completed checkpoints

### make_first_semantic_reference_readiness_v0_1

Accepted by Blueprint before the business card skeleton checkpoint.

### reference_contract_foundation_v0_2

Accepted by Blueprint before the business card skeleton checkpoint.

### coordination_foundation_alignment_v0_1

- Makefile was not rewritten.
- No real secrets or credentials were committed.
- Coordination foundation alignment remains recorded as a historical checkpoint.

### reference_consumption_pilot_v0_3

- Reference consumption pilot remains recorded as a historical checkpoint.
- Previous rolling status: `reference_consumption_pilot_v0_3_ready_pending_blueprint_review`.

## Next step

Blueprint review of `library_configurable_product_workbench_business_card_skeleton_v0_1`.
```

### `coordination/status/current_status.yaml`

- SHA256: `261bd7797a1d1f39b0349bf65a7d889f59c59083e1fcd5d0b63379ba59821695`
- Bytes: `11034`

```yaml
module_id: forprint_library
status: completed_pending_blueprint_review
stage: coordination_foundation_alignment_v0_1_completion
updated_at: '2026-07-13'
owner_module: forprint_library
current_focus:
- Business Card Skeleton completed and ready for Blueprint review.
- product.business_card is available as a controlled Library reference object.
- Implementation and closure metadata are recorded in Library repository.
- No Blueprint repository writes were performed.
boundary_confirmation:
  owns:
  - canonical catalog semantics
  - stable catalog IDs
  - aliases
  - contract definitions
  does_not_own:
  - clients
  - orders
  - payments
  - warehouse stock truth
  - production runtime
  - 1C synchronization
  - CRM workflow
  - Telegram runtime
  - Calculator logic
catalog_seed_v0_1:
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  projection_use_allowed_for:
  - calculator_engine
  - telegram_bot
  - forprint_operational_registry
  - forprint_accounting_registry_service
  - forprint_prepress_hub
checkpoint_a:
  coordination_structure: done
  makefile_standard: done
  check_report: done
  commit: e2f9302
checkpoint_b:
  catalog_seed: done
  schemas: done
  component_catalogs: done
  validation_tests: done
  check_report_catalog_validation: done
  commit: bb7a317
checkpoint_c:
  docs_policy_pack: done
  architecture_tests: done
  commit: 967d74a
checkpoint_d:
  final_report_and_status: done
  reports_index: in_progress
  final_check: pending
  commit: pending
next_recommended_step:
  status: wait_for_blueprint_review
  recommended_action: Ask Blueprint to review Library coordination foundation alignment
    v0.1 and confirm readiness for the next prompt.
  candidate_next_prompt: Library Configurable Product Workbench v0.1 — Business Card
    Skeleton
current_phase: business_card_skeleton_v0_1
last_completed_step: library_business_card_skeleton_ready
shared_operational_dictionary_v0_1:
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
  dictionary_groups_count: 18
  dictionary_files: done
  schemas: done
  loader_validation: done
  resolver: done
  terminal_preview: done
  examples: done
  architecture_docs: done
  check_report_extension: done
  coordination_report: done
shared_operational_dictionary_checkpoints:
  checkpoint_a:
    name: dictionary_files_and_schemas
    status: done
    commit: 18900ee
  checkpoint_b:
    name: resolver_examples_and_preview
    status: done
    commit: 2fc7694
  checkpoint_c:
    name: docs_check_report_and_coordination
    status: in_progress_until_final_commit
    commit: pending
module_name: ForPrint Library
module_status: active
priority: p0
last_report_id: 2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1
last_commit: 5c7c230
branch: main
checks:
  lint: ok
  tests: ok_76_passed
  check_report: ok
  dictionary_preview: ok
  coordination_check: pending_blueprint_recheck
boundary:
  no_foreign_ownership: true
  no_production_api: true
  no_live_write: true
  no_real_integrations: true
validation:
  make_check: ok
  make_check_report: ok
  dictionary_preview: ok
  coordination_metadata: pending_blueprint_recheck
boundaries:
  operational_orders_added: false
  real_clients_added: false
  real_payments_added: false
  real_material_stock_added: false
  real_product_catalog_added: false
  real_1c_sync_added: false
  calculator_formulas_added: false
  telegram_runtime_added: false
  crm_dashboard_added: false
  warehouse_stock_truth_added: false
recommended_next_step:
- Pass shared operational dictionary v0.1 to Blueprint for review.
- 'Recommended next candidate: Operational Registry mapping from local draft statuses/types
  to Library canonical dictionary IDs.'
make_first_semantic_reference_readiness_v0_1:
  prompt_id: make_first_semantic_reference_readiness_v0_1
  blueprint_prompt_path: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/outgoing_prompts/forprint_library/approved/2026-06-23__library__make_first_semantic_reference_readiness_v0_1.md
  blueprint_commit: 2d49d63
  implementation_commit: 28fe2d0
  completion_report_id: 2026-06-25__forprint_library__report__make-first-semantic-reference-readiness-v0-1
  completion_report_path: coordination/reports/completion/2026-06-25__forprint_library__report__make-first-semantic-reference-readiness-v0-1.md
  status: completed_pending_blueprint_review
  makefile_alignment: done
  make_first_targets: done
  module_start: passing
  module_validate: passing
  prompt_read: passing
  report_clean: passing_without_git_or_venv_scan
  semantic_reference_examples: done
  semantic_reference_docs: done
  downstream_handoff_notes: done
  check_report_visibility: done
  tests: 83_passed
  completion_packet_automation: deferred_safe_not_faked
  production_catalog_database: not_implemented
  live_api: not_implemented
  runtime_integrations: not_implemented
reference_contract_foundation_v0_2:
  prompt_id: reference_contract_foundation_v0_2
  blueprint_prompt_path: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/outgoing_prompts/forprint_library/approved/2026-06-29__library__reference_contract_foundation_v0_2.md
  implementation_commit: 78bd7e1
  implementation_commit_message: Add Library reference contract foundation
  completion_report_id: 2026-06-29__forprint_library__report__reference-contract-foundation-v0-2
  completion_report_path: coordination/reports/completion/2026-06-29__forprint_library__report__reference-contract-foundation-v0-2.md
  status: accepted_by_blueprint
  docs: done
  examples: done
  schemas: done
  validator: done
  tests: 94_passed
  check_report_visibility: done
  makefile_changes: not_changed_manual_blueprint_mode
  completion_packet_automation: deferred_safe_not_faked
  production_catalog_database: not_implemented
  live_api: not_implemented
  runtime_integrations: not_implemented
coordination_foundation_alignment_v0_1:
  prompt_id: library_coordination_foundation_alignment_v0_1
  blueprint_prompt_path: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/outgoing_prompts/forprint_library/approved/2026-07-03__library__coordination_foundation_alignment_v0_1.md
  implementation_commit: 02e2cad
  implementation_commit_message: Add Library coordination foundation alignment
  completion_report_id: 2026-07-03__forprint_library__report__coordination-foundation-alignment-v0-1
  completion_report_path: coordination/reports/completion/2026-07-03__forprint_library__report__coordination-foundation-alignment-v0-1.md
  status: completed_pending_blueprint_review
  makefile_rewrite: not_needed
  operator_workflow: confirmed
  prompt_queue_navigation: confirmed
  document_awareness: confirmed
  context_bundle_no_write: confirmed
  configuration_policy: documented_deferred_until_needed
  secrets_policy: not_applicable_no_secrets_added
  project_tree_alignment: documented
  check_report_visibility: done
  tests: 104_passed
  workbench_started: false
  product_modeling_started: false
  production_runtime_changes: false
reference_consumption_pilot_v0_3:
  status: completed_pending_blueprint_review
  prompt_id: library_reference_consumption_pilot_v0_3
  implementation_commit: 7e000cb
  completion_report: coordination/reports/completion/2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3.md
  blueprint_prompt_path: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/outgoing_prompts/forprint_library/approved/2026-07-08__library__reference_consumption_pilot_v0_3.md
  added_artifacts:
  - examples/reference_consumption/library_reference_consumption_examples.yaml
  - schemas/reference_consumption/library_reference_consumption.schema.yaml
  - scripts/reference_consumption/validate_reference_consumption_pilot.py
  - docs/architecture/reference_consumption_pilot.md
  - tests/coordination/test_reference_consumption_pilot.py
  check_report_visibility: Library reference consumption pilot
  validation:
    focused_tests: 7 passed
    full_tests: 115 passed
    check_report: OK
    make_check: OK
    governance_check: OK
    module_validate: OK
    git_diff_check: OK
  boundaries:
    configurable_product_workbench_started: false
    business_card_skeleton_started: false
    product_modeling_ui_added: false
    production_catalog_database_added: false
    live_api_added: false
    one_c_import_added: false
    calculator_integration_added: false
    telegram_integration_added: false
    operational_registry_write_added: false
    production_write_added: false
    price_calculation_added: false
    material_write_off_added: false
    blueprint_repository_written: false
  next_recommended_step: Blueprint review of module-side completion report.
configurable_product_workbench_business_card_skeleton_v0_1:
  status: completed_pending_blueprint_review
  prompt_id: library_configurable_product_workbench_business_card_skeleton_v0_1
  title: Library Configurable Product Workbench v0.1 — Business Card Skeleton
  product_id: product.business_card
  implementation_commit: b8eb062
  completion_commits:
  - 7a7cb85
  - ad99e0a
  - '1694215'
  final_cleanup_commit: reported_after_push
  completion_report: coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md
  blueprint_prompt_path: coordination/outgoing_prompts/forprint_library/approved/2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1.md
  checks_passed:
    business_card_validator: OK
    business_card_preview: OK
    focused_business_card_tests: 8 passed
    full_tests: 137 passed
    ruff_lint: OK
    check_report: OK
    make_check: OK
    governance_check: OK
    module_validate: OK
    git_diff_check: OK
  blueprint_repository_written: false
  boundaries:
    full_product_catalog_added: false
    product_modeling_ui_added: false
    production_catalog_database_added: false
    live_api_added: false
    one_c_import_added: false
    one_c_synchronization_added: false
    calculator_integration_added: false
    telegram_bot_integration_added: false
    operational_registry_write_added: false
    crm_write_added: false
    website_write_added: false
    price_calculation_added: false
    final_price_formula_added: false
    material_write_off_added: false
    warehouse_stock_truth_added: false
    production_task_creation_added: false
    real_client_order_data_added: false
    production_runtime_added: false
    blueprint_repository_written: false
  notes:
  - Final cleanup commit hash is reported after push because a Git commit cannot contain
    its own final hash.
  legacy_status_aliases:
  - business_card_skeleton_v0_1_ready_pending_blueprint_review
```

### `coordination/status/next_questions_for_blueprint.md`

- SHA256: `b0cf6706707fdd910d1a9631b5b2bec6084130e6776cbbd14d99affe747f048b`
- Bytes: `782`

```markdown
# Next questions for Blueprint

## Current checkpoint

`library_configurable_product_workbench_business_card_skeleton_v0_1`

## Status

`completed_pending_blueprint_review`

## Product ID

`product.business_card`

## Open questions

No open questions.

## Review request

Please review the Library-side completion report:

`coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`

The module is waiting for Blueprint acceptance or requested fixes.

## Blueprint repository writes

No files were written directly into the Blueprint repository.

## Latest cleanup commit before Blueprint acceptance verification

`1694215` — Finalize Library business card completion metadata.

## Boundary confirmation

No Blueprint repository writes.
```

### `dictionaries/shared_operational_dictionary_v0_1.yaml`

- SHA256: `3610bb44537903fa66fdd7be02deacabcd6b073e69d2a44c80a8a8c075056d26`
- Bytes: `63700`

```yaml
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
dictionary_groups:
  source_system:
  - id: forprint_operational_registry
    label_uk: Forprint Operational Registry
    label_en: Forprint Operational Registry
    description: Canonical shared operational dictionary value 'forprint_operational_registry'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - operational_registry
    - opr
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_library
    label_uk: Forprint Library
    label_en: Forprint Library
    description: Canonical shared operational dictionary value 'forprint_library'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - library
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: calculator_engine
    label_uk: Calculator Engine
    label_en: Calculator Engine
    description: Canonical shared operational dictionary value 'calculator_engine'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - calculator
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: accounting_registry_service
    label_uk: Accounting Registry Service
    label_en: Accounting Registry Service
    description: Canonical shared operational dictionary value 'accounting_registry_service'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - accounting_registry
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: telegram_bot
    label_uk: Telegram Bot
    label_en: Telegram Bot
    description: Canonical shared operational dictionary value 'telegram_bot' for
      dictionary group 'source_system'.
    status: active
    aliases:
    - telegram
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_crm
    label_uk: Forprint Crm
    label_en: Forprint Crm
    description: Canonical shared operational dictionary value 'forprint_crm' for
      dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_integration_gateway
    label_uk: Forprint Integration Gateway
    label_en: Forprint Integration Gateway
    description: Canonical shared operational dictionary value 'forprint_integration_gateway'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_prepress_hub
    label_uk: Forprint Prepress Hub
    label_en: Forprint Prepress Hub
    description: Canonical shared operational dictionary value 'forprint_prepress_hub'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: warehouse_service
    label_uk: Warehouse Service
    label_en: Warehouse Service
    description: Canonical shared operational dictionary value 'warehouse_service'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: logistics_service
    label_uk: Logistics Service
    label_en: Logistics Service
    description: Canonical shared operational dictionary value 'logistics_service'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: website
    label_uk: Website
    label_en: Website
    description: Canonical shared operational dictionary value 'website' for dictionary
      group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: mobile_app
    label_uk: Mobile App
    label_en: Mobile App
    description: Canonical shared operational dictionary value 'mobile_app' for dictionary
      group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: one_c_bas
    label_uk: 1C/BAS
    label_en: One C Bas
    description: Canonical shared operational dictionary value 'one_c_bas' for dictionary
      group 'source_system'.
    status: active
    aliases:
    - 1c
    - bas
    - 1c_bas
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: sanitized_demo
    label_uk: Sanitized Demo
    label_en: Sanitized Demo
    description: Canonical shared operational dictionary value 'sanitized_demo' for
      dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_entry
    label_uk: Manual Entry
    label_en: Manual Entry
    description: Canonical shared operational dictionary value 'manual_entry' for
      dictionary group 'source_system'.
    status: active
    aliases:
    - manual
    - ручне введення
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'source_system'.
    status: active
    aliases: &id001
    - невідомо
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  entity_type:
  - id: client_account
    label_uk: Client Account
    label_en: Client Account
    description: Canonical shared operational dictionary value 'client_account' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_group
    label_uk: Client Group
    label_en: Client Group
    description: Canonical shared operational dictionary value 'client_group' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contact_person
    label_uk: Contact Person
    label_en: Contact Person
    description: Canonical shared operational dictionary value 'contact_person' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contact_method
    label_uk: Contact Method
    label_en: Contact Method
    description: Canonical shared operational dictionary value 'contact_method' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_address
    label_uk: Client Address
    label_en: Client Address
    description: Canonical shared operational dictionary value 'client_address' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: legal_entity_profile
    label_uk: Legal Entity Profile
    label_en: Legal Entity Profile
    description: Canonical shared operational dictionary value 'legal_entity_profile'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: external_reference
    label_uk: External Reference
    label_en: External Reference
    description: Canonical shared operational dictionary value 'external_reference'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: order
    label_uk: Order
    label_en: Order
    description: Canonical shared operational dictionary value 'order' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: order_line
    label_uk: Order Line
    label_en: Order Line
    description: Canonical shared operational dictionary value 'order_line' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: calculator_output_package
    label_uk: Calculator Output Package
    label_en: Calculator Output Package
    description: Canonical shared operational dictionary value 'calculator_output_package'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: product_service_reference
    label_uk: Product Service Reference
    label_en: Product Service Reference
    description: Canonical shared operational dictionary value 'product_service_reference'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: material_requirement
    label_uk: Material Requirement
    label_en: Material Requirement
    description: Canonical shared operational dictionary value 'material_requirement'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: payment_projection
    label_uk: Payment Projection
    label_en: Payment Projection
    description: Canonical shared operational dictionary value 'payment_projection'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: workflow_template
    label_uk: Workflow Template
    label_en: Workflow Template
    description: Canonical shared operational dictionary value 'workflow_template'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: workflow_stage
    label_uk: Workflow Stage
    label_en: Workflow Stage
    description: Canonical shared operational dictionary value 'workflow_stage' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: deadline_control
    label_uk: Deadline Control
    label_en: Deadline Control
    description: Canonical shared operational dictionary value 'deadline_control'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contractor_reference
    label_uk: Contractor Reference
    label_en: Contractor Reference
    description: Canonical shared operational dictionary value 'contractor_reference'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: alert_rule
    label_uk: Alert Rule
    label_en: Alert Rule
    description: Canonical shared operational dictionary value 'alert_rule' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: alert_event
    label_uk: Alert Event
    label_en: Alert Event
    description: Canonical shared operational dictionary value 'alert_event' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: report_definition
    label_uk: Report Definition
    label_en: Report Definition
    description: Canonical shared operational dictionary value 'report_definition'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: report_projection
    label_uk: Report Projection
    label_en: Report Projection
    description: Canonical shared operational dictionary value 'report_projection'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: operational_event
    label_uk: Operational Event
    label_en: Operational Event
    description: Canonical shared operational dictionary value 'operational_event'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'entity_type'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  order_status:
  - id: draft
    label_uk: Чернетка
    label_en: Draft
    description: Canonical shared operational dictionary value 'draft' for dictionary
      group 'order_status'.
    status: active
    aliases: &id002
    - чернетка
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: needs_review
    label_uk: Потребує перевірки
    label_en: Needs Review
    description: Canonical shared operational dictionary value 'needs_review' for
      dictionary group 'order_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: confirmed
    label_uk: Підтверджено
    label_en: Confirmed
    description: Canonical shared operational dictionary value 'confirmed' for dictionary
      group 'order_status'.
    status: active
    aliases: &id008
    - підтверджено
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'order_status'.
    status: active
    aliases: &id003
    - у роботі
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'order_status'.
    status: active
    aliases: &id004
    - завершено
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'order_status'.
    status: active
    aliases: &id005
    - скасовано
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'order_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'order_status'.
    status: active
    aliases: &id006
    - manual_review
    - ручна перевірка
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: archived
    label_uk: Архівовано
    label_en: Archived
    description: Canonical shared operational dictionary value 'archived' for dictionary
      group 'order_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'order_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  order_line_status:
  - id: draft
    label_uk: Чернетка
    label_en: Draft
    description: Canonical shared operational dictionary value 'draft' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id002
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: pending_reference_resolution
    label_uk: Pending Reference Resolution
    label_en: Pending Reference Resolution
    description: Canonical shared operational dictionary value 'pending_reference_resolution'
      for dictionary group 'order_line_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ready
    label_uk: Готово
    label_en: Ready
    description: Canonical shared operational dictionary value 'ready' for dictionary
      group 'order_line_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id003
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'order_line_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  payment_status:
  - id: not_invoiced
    label_uk: Not Invoiced
    label_en: Not Invoiced
    description: Canonical shared operational dictionary value 'not_invoiced' for
      dictionary group 'payment_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: invoice_reference_pending
    label_uk: Invoice Reference Pending
    label_en: Invoice Reference Pending
    description: Canonical shared operational dictionary value 'invoice_reference_pending'
      for dictionary group 'payment_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unpaid
    label_uk: Не оплачено
    label_en: Unpaid
    description: Canonical shared operational dictionary value 'unpaid' for dictionary
      group 'payment_status'.
    status: active
    aliases:
    - не оплачено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: partially_paid
    label_uk: Частково оплачено
    label_en: Partially Paid
    description: Canonical shared operational dictionary value 'partially_paid' for
      dictionary group 'payment_status'.
    status: active
    aliases:
    - частково оплачено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: paid_reference_confirmed
    label_uk: Підтверджено оплату
    label_en: Paid Reference Confirmed
    description: Canonical shared operational dictionary value 'paid_reference_confirmed'
      for dictionary group 'payment_status'.
    status: active
    aliases:
    - paid
    - оплачено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: overdue
    label_uk: Прострочено
    label_en: Overdue
    description: Canonical shared operational dictionary value 'overdue' for dictionary
      group 'payment_status'.
    status: active
    aliases:
    - прострочено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'payment_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'payment_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  production_status:
  - id: not_started
    label_uk: Не розпочато
    label_en: Not Started
    description: Canonical shared operational dictionary value 'not_started' for dictionary
      group 'production_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ready
    label_uk: Готово
    label_en: Ready
    description: Canonical shared operational dictionary value 'ready' for dictionary
      group 'production_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'production_status'.
    status: active
    aliases: *id003
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: waiting_external_contractor
    label_uk: Очікування зовнішнього підрядника
    label_en: Waiting External Contractor
    description: Canonical shared operational dictionary value 'waiting_external_contractor'
      for dictionary group 'production_status'.
    status: active
    aliases: &id007
    - external_contractor_wait
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'production_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'production_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'production_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'production_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  workflow_status:
  - id: not_started
    label_uk: Не розпочато
    label_en: Not Started
    description: Canonical shared operational dictionary value 'not_started' for dictionary
      group 'workflow_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: active
    label_uk: Активний
    label_en: Active
    description: Canonical shared operational dictionary value 'active' for dictionary
      group 'workflow_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'workflow_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'workflow_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'workflow_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'workflow_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'workflow_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  workflow_stage_status:
  - id: not_started
    label_uk: Не розпочато
    label_en: Not Started
    description: Canonical shared operational dictionary value 'not_started' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ready
    label_uk: Готово
    label_en: Ready
    description: Canonical shared operational dictionary value 'ready' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id003
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: waiting_external_contractor
    label_uk: Очікування зовнішнього підрядника
    label_en: Waiting External Contractor
    description: Canonical shared operational dictionary value 'waiting_external_contractor'
      for dictionary group 'workflow_stage_status'.
    status: active
    aliases: *id007
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: late
    label_uk: Прострочено
    label_en: Late
    description: Canonical shared operational dictionary value 'late' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases:
    - прострочений етап
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'workflow_stage_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  material_requirement_status:
  - id: planned
    label_uk: Заплановано
    label_en: Planned
    description: Canonical shared operational dictionary value 'planned' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: library_reference_pending
    label_uk: Library Reference Pending
    label_en: Library Reference Pending
    description: Canonical shared operational dictionary value 'library_reference_pending'
      for dictionary group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: warehouse_reference_pending
    label_uk: Warehouse Reference Pending
    label_en: Warehouse Reference Pending
    description: Canonical shared operational dictionary value 'warehouse_reference_pending'
      for dictionary group 'material_requirement_status'.
    status: active
    aliases:
    - warehouse_pending
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: reserved_reference_pending
    label_uk: Reserved Reference Pending
    label_en: Reserved Reference Pending
    description: Canonical shared operational dictionary value 'reserved_reference_pending'
      for dictionary group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: confirmed
    label_uk: Підтверджено
    label_en: Confirmed
    description: Canonical shared operational dictionary value 'confirmed' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: *id008
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: fulfilled
    label_uk: Виконано
    label_en: Fulfilled
    description: Canonical shared operational dictionary value 'fulfilled' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  reference_resolution_status:
  - id: draft_display_only
    label_uk: Draft Display Only
    label_en: Draft Display Only
    description: Canonical shared operational dictionary value 'draft_display_only'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: reference_pending
    label_uk: Reference Pending
    label_en: Reference Pending
    description: Canonical shared operational dictionary value 'reference_pending'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: reference_confirmed
    label_uk: Reference Confirmed
    label_en: Reference Confirmed
    description: Canonical shared operational dictionary value 'reference_confirmed'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ambiguous_manual_review_required
    label_uk: Ambiguous Manual Review Required
    label_en: Ambiguous Manual Review Required
    description: Canonical shared operational dictionary value 'ambiguous_manual_review_required'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: deprecated_reference
    label_uk: Deprecated Reference
    label_en: Deprecated Reference
    description: Canonical shared operational dictionary value 'deprecated_reference'
      for dictionary group 'reference_resolution_status'.
    status: deprecated
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'reference_resolution_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  product_service_reference_status:
  - id: draft_display_only
    label_uk: Draft Display Only
    label_en: Draft Display Only
    description: Canonical shared operational dictionary value 'draft_display_only'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: library_reference_pending
    label_uk: Library Reference Pending
    label_en: Library Reference Pending
    description: Canonical shared operational dictionary value 'library_reference_pending'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: library_reference_confirmed
    label_uk: Library Reference Confirmed
    label_en: Library Reference Confirmed
    description: Canonical shared operational dictionary value 'library_reference_confirmed'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ambiguous_manual_review_required
    label_uk: Ambiguous Manual Review Required
    label_en: Ambiguous Manual Review Required
    description: Canonical shared operational dictionary value 'ambiguous_manual_review_required'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: deprecated_reference
    label_uk: Deprecated Reference
    label_en: Deprecated Reference
    description: Canonical shared operational dictionary value 'deprecated_reference'
      for dictionary group 'product_service_reference_status'.
    status: deprecated
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'product_service_reference_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  contractor_reference_status:
  - id: display_only
    label_uk: Display Only
    label_en: Display Only
    description: Canonical shared operational dictionary value 'display_only' for
      dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_account_reference_pending
    label_uk: Client Account Reference Pending
    label_en: Client Account Reference Pending
    description: Canonical shared operational dictionary value 'client_account_reference_pending'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_account_reference_confirmed
    label_uk: Client Account Reference Confirmed
    label_en: Client Account Reference Confirmed
    description: Canonical shared operational dictionary value 'client_account_reference_confirmed'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: external_reference_pending
    label_uk: External Reference Pending
    label_en: External Reference Pending
    description: Canonical shared operational dictionary value 'external_reference_pending'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'contractor_reference_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  deadline_type:
  - id: order_due
    label_uk: Order Due
    label_en: Order Due
    description: Canonical shared operational dictionary value 'order_due' for dictionary
      group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: stage_due
    label_uk: Stage Due
    label_en: Stage Due
    description: Canonical shared operational dictionary value 'stage_due' for dictionary
      group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: payment_due
    label_uk: Payment Due
    label_en: Payment Due
    description: Canonical shared operational dictionary value 'payment_due' for dictionary
      group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: material_required_by
    label_uk: Material Required By
    label_en: Material Required By
    description: Canonical shared operational dictionary value 'material_required_by'
      for dictionary group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_due
    label_uk: Manual Review Due
    label_en: Manual Review Due
    description: Canonical shared operational dictionary value 'manual_review_due'
      for dictionary group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'deadline_type'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  alert_rule_type:
  - id: workflow_stage_late
    label_uk: Workflow Stage Late
    label_en: Workflow Stage Late
    description: Canonical shared operational dictionary value 'workflow_stage_late'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: order_deadline_near
    label_uk: Order Deadline Near
    label_en: Order Deadline Near
    description: Canonical shared operational dictionary value 'order_deadline_near'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: payment_overdue
    label_uk: Payment Overdue
    label_en: Payment Overdue
    description: Canonical shared operational dictionary value 'payment_overdue' for
      dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: material_requirement_unresolved
    label_uk: Material Requirement Unresolved
    label_en: Material Requirement Unresolved
    description: Canonical shared operational dictionary value 'material_requirement_unresolved'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_stale
    label_uk: Manual Review Stale
    label_en: Manual Review Stale
    description: Canonical shared operational dictionary value 'manual_review_stale'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contractor_stage_blocked
    label_uk: Contractor Stage Blocked
    label_en: Contractor Stage Blocked
    description: Canonical shared operational dictionary value 'contractor_stage_blocked'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'alert_rule_type'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  alert_severity:
  - id: info
    label_uk: Інформаційно
    label_en: Info
    description: Canonical shared operational dictionary value 'info' for dictionary
      group 'alert_severity'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: warning
    label_uk: Попередження
    label_en: Warning
    description: Canonical shared operational dictionary value 'warning' for dictionary
      group 'alert_severity'.
    status: active
    aliases:
    - warn
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: high
    label_uk: Високий
    label_en: High
    description: Canonical shared operational dictionary value 'high' for dictionary
      group 'alert_severity'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: critical
    label_uk: Критичний
    label_en: Critical
    description: Canonical shared operational dictionary value 'critical' for dictionary
      group 'alert_severity'.
    status: active
    aliases:
    - crit
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'alert_severity'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  alert_event_status:
  - id: open
    label_uk: Відкрито
    label_en: Open
    description: Canonical shared operational dictionary value 'open' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: acknowledged
    label_uk: Підтверджено оператором
    label_en: Acknowledged
    description: Canonical shared operational dictionary value 'acknowledged' for
      dictionary group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: resolved
    label_uk: Вирішено
    label_en: Resolved
    description: Canonical shared operational dictionary value 'resolved' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ignored
    label_uk: Проігноровано
    label_en: Ignored
    description: Canonical shared operational dictionary value 'ignored' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: failed_to_notify
    label_uk: Failed To Notify
    label_en: Failed To Notify
    description: Canonical shared operational dictionary value 'failed_to_notify'
      for dictionary group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  notification_status:
  - id: not_sent
    label_uk: Не надіслано
    label_en: Not Sent
    description: Canonical shared operational dictionary value 'not_sent' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: queued
    label_uk: У черзі
    label_en: Queued
    description: Canonical shared operational dictionary value 'queued' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: sent
    label_uk: Надіслано
    label_en: Sent
    description: Canonical shared operational dictionary value 'sent' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: failed
    label_uk: Помилка
    label_en: Failed
    description: Canonical shared operational dictionary value 'failed' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: disabled
    label_uk: Вимкнено
    label_en: Disabled
    description: Canonical shared operational dictionary value 'disabled' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'notification_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  unit:
  - id: pcs
    label_uk: Штуки
    label_en: Pcs
    description: Canonical shared operational dictionary value 'pcs' for dictionary
      group 'unit'.
    status: active
    aliases:
    - piece
    - pieces
    - шт
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: set
    label_uk: Комплект
    label_en: Set
    description: Canonical shared operational dictionary value 'set' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: m
    label_uk: Метри
    label_en: M
    description: Canonical shared operational dictionary value 'm' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: m2
    label_uk: Квадратні метри
    label_en: M2
    description: Canonical shared operational dictionary value 'm2' for dictionary
      group 'unit'.
    status: active
    aliases:
    - sqm
    - square_meter
    - м2
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: kg
    label_uk: Кілограми
    label_en: Kg
    description: Canonical shared operational dictionary value 'kg' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: g
    label_uk: Грами
    label_en: G
    description: Canonical shared operational dictionary value 'g' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: l
    label_uk: Літри
    label_en: L
    description: Canonical shared operational dictionary value 'l' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ml
    label_uk: Мілілітри
    label_en: Ml
    description: Canonical shared operational dictionary value 'ml' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: hour
    label_uk: Година
    label_en: Hour
    description: Canonical shared operational dictionary value 'hour' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: minute
    label_uk: Хвилина
    label_en: Minute
    description: Canonical shared operational dictionary value 'minute' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: service
    label_uk: Послуга
    label_en: Service
    description: Canonical shared operational dictionary value 'service' for dictionary
      group 'unit'.
    status: active
    aliases:
    - послуга
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'unit'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
```

### `docs/architecture/README.md`

- SHA256: `00f426b9e45d999fee3a1564e123ea3251b76d9d7bc9accc54f397cee2ceb706`
- Bytes: `715`

```markdown
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
```

### `docs/architecture/alias_policy.md`

- SHA256: `af0ef87976844483623d1af974129dd3e9e6db5ba1bded4ab768e649e69ece0b`
- Bytes: `1219`

```markdown
# Alias Policy

## Status

Draft policy for ForPrint Library aliases.

## Core rule

Aliases are lookup helpers, not canonical truth.

The canonical truth is the stable Library ID.

## Allowed alias examples

A product family may have aliases such as:

```yaml
id: business_card
aliases:
  - візитка
  - business card
  - карточка

A material may have aliases such as:

id: paper_350g_gloss
aliases:
  - папір 350 глянц
  - 350gsm gloss
  - мелований 350 г
Conflict rule

Alias conflicts must not silently resolve to a random entity.

If one alias can point to more than one item, Library validation or future
approval workflow must report it as ambiguous.

Unknown aliases

Unknown aliases should be reported as unresolved.

They should not automatically create new canonical catalog entries.

Future approval workflow

A future approval workflow may allow responsible users to:

approve new aliases;
reject invalid aliases;
merge duplicate aliases;
deprecate old aliases;
route ambiguous aliases for manual review.
Dependent module behavior

Dependent modules may use aliases for search and display, but they should store
the resolved canonical ID after successful resolution.


---
```

### `docs/architecture/canonical_id_policy.md`

- SHA256: `4e4f3807ca1ae08aed9554ebdb89418990e75255955ec8fa2d14b1d678ceac80`
- Bytes: `1456`

```markdown
# Canonical ID Policy

## Status

Draft policy for ForPrint Library canonical IDs.

## Core rule

Canonical IDs are stable internal truth.

Human-readable names may change, but canonical IDs should remain stable unless a
formal migration is created.

## Names are not truth

Names such as:

- `Візитка`;
- `Business card`;
- `карточка`;

may all point to one canonical ID:

```yaml
product_family_id: business_card

Dependent modules must reference canonical IDs, not uncontrolled free text.

Alias relationship

Aliases help users and modules find the correct canonical ID, but aliases are
not canonical truth.

Aliases may be added, deprecated or reviewed without changing the canonical ID.

Dependent module rule

Dependent modules should store and exchange Library IDs where possible.

Examples:

material_id: paper_350g_gloss
product_family_id: business_card
operation_id: digital_print
print_mode_id: color_4_4
finishing_option_id: matte_lamination
Ambiguous input

If a name or alias can point to more than one entity, the system must not
silently choose a random ID.

Ambiguous input should be reported as unresolved or routed to a future approval
workflow.

Current seed limitation

Canonical Catalog Seed v0.1 is:

catalog_status: draft_canonical_seed
schema_status: unstable_v0_1
usage: allowed_for_projection_use
contract_status: not_final_contract

It is safe for projection use, but it is not a final production contract.


---
```

### `docs/architecture/catalog_seed_policy.md`

- SHA256: `1331b4a43fe9cfd50ccb80f9594e7701cae60c72e589f4de2b8c1e475f8ad769`
- Bytes: `1270`

```markdown
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
```

### `docs/architecture/dictionary_consumption_policy.md`

- SHA256: `790a352c98ab614865bd24fa27966fc720090cac814a3e410f00cdd6d811730c`
- Bytes: `1103`

```markdown
# Dictionary Consumption Policy

Status

Draft policy for consuming Library dictionaries.

General rule

Dependent modules may consume Library dictionaries as projection input and validation references.

They should reference canonical IDs and display labels, 
not invent new internal IDs for shared operational concepts.

Operational Registry

Operational Registry should later reference these canonical values for statuses, 
entity types, source systems, alerts, deadlines and reference resolution states.

Calculator Engine

Calculator Engine should use these values when producing structured output packages, 
especially for source_system, entity_type, 
reference_resolution_status and product_service_reference_status.

Accounting Registry

Accounting Registry may map accounting statuses carefully, 
but it must not become the source of operational truth.

Telegram Bot and CRM

Telegram Bot and CRM should display labels and route ambiguous or 
unknown values for review instead of inventing canonical IDs.

Deprecated values

Deprecated dictionary values remain readable for historical records.
```

### `docs/architecture/dictionary_versioning_policy.md`

- SHA256: `6219b3484fca51b031dec00a3472ce07f71850cf189d4cc97a2cc20857e30b55`
- Bytes: `771`

```markdown
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
```

### `docs/architecture/library_boundaries.md`

- SHA256: `d8d40ec4624584b375514bceedc5d9a2ac0b514c3319429a60908d19be35dd2d`
- Bytes: `1481`

```markdown
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
```

### `docs/architecture/library_calculator_input_contract.md`

- SHA256: `bb89a0f089a3253ddb1fa912b4aa0fd08d8ce748314bf46e5cb7839ce7431a59`
- Bytes: `2892`

```markdown
# Library Calculator Input Contract v0.1

## Purpose

This document defines the ForPrint Library read-only Calculator input contract
for `product.business_card`.

The contract converts a validated configurable product selection into a
deterministic, schema-versioned envelope that Calculator can consume as
reference input.

## Ownership boundary

Library owns:

- product identity;
- configurable parameter definitions;
- validation and normalization rules;
- Library reference identifiers;
- deterministic product-configuration projection;
- schema/version metadata.

Calculator owns:

- price formulas;
- pricing policy;
- numerical calculations;
- costs and margins;
- quote totals.

The Library contract must not contain prices, totals, margins, costs, taxes,
discounts, currency fields, vendor prices or hidden formulas.

## Schema versioning

Current envelope schema:

`calculator_input_envelope_v0_1`

Unsupported schema versions fail with the stable error type:

`unsupported_projection_version`

## Public entry point

```python
build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope
```

The entry point is read-only. It does not mutate input mappings, perform writes,
make network calls, import Calculator code or create runtime records.

## Business-card projection

For `product.business_card`, the projection includes:

- `product_id`;
- `size`;
- `sides`;
- `material_ref`;
- `print_mode_ref`;
- `quantity`;
- `finishing_refs`;
- `artwork_source` when supplied.

## Deterministic serialization

Serialized envelope field order is stable:

1. `schema_version`
2. `product_id`
3. `configuration_id`
4. `normalized_parameters`
5. `reference_ids`
6. `validation_snapshot`

`finishing_refs` are normalized by catalog and id. Duplicate finishing
references are collapsed.

## Error taxonomy

Stable public error types:

- `unknown_product`
- `invalid_configuration`
- `missing_required_parameter`
- `invalid_reference`
- `unsupported_projection_version`
- `internal_contract_error`

Errors are safe for Calculator consumption and do not expose stack traces or
persistence internals.

## Fixture paths

Machine-readable fixtures live in:

`examples/calculator_input_contract/`

Schema lives in:

`schemas/calculator_input/calculator_input_envelope.schema.yaml`

## Calculator consumption example

Calculator may consume the envelope as reference input context. Calculator must
still own all price formulas, pricing policy, totals, cost and margin logic.

## Forbidden scope

This contract does not implement:

- price formulas;
- quote totals;
- cost, margin, discount, tax or currency calculations;
- Calculator internals;
- canonical-order creation;
- Telegram behavior;
- Logistics behavior;
- CRM, Gateway, 1C, payment, stock or production writes;
- production deployment.
```

### `docs/architecture/reference_consumption_pilot.md`

- SHA256: `db89be548a69a25f9afd7415f8a6c7a796d3c7023ec98f97570e866c8647c181`
- Bytes: `4290`

```markdown
# Library Reference Consumption Pilot v0.3

## Purpose

This document describes a small, local and read-only reference consumption pilot
for ForPrint Library.

The pilot demonstrates how downstream ForPrint modules may consume
Library-owned reference IDs without making Library responsible for downstream
runtime behavior.

This is not a production integration.

This does not start Configurable Product Workbench.

## Active prompt

```text
library_reference_consumption_pilot_v0_3
```
Source contract

The pilot consumes the existing Library Reference Contract Foundation v0.2
example references from:

examples/reference_contract/library_reference_examples.yaml

These references are controlled contract examples. They are not a final
production catalog database.

Library-owned reference IDs

Library-owned reference IDs represent stable semantic references owned by
ForPrint Library.

Examples used by the pilot:

product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
template.business_card.90x50

Library owns the semantic meaning of these reference identifiers.

Library may define and validate reference semantics.

## consumer-owned runtime fields

Consumer-owned runtime fields belong to downstream modules.

Examples:

calculator_engine requested quantity
telegram_bot channel hint
forprint_operational_registry local task reference

These fields may travel next to Library references in consumer payloads, but
they do not become Library-owned fields.

Foreign module references

A consumer payload may include foreign module references.

Examples:

calculator_engine.demo.pricing_context_001
telegram_bot.demo.message_001
forprint_operational_registry.demo.material_ref_001

These foreign module references are owned by the downstream module that created
them.

Library stores no runtime state for these examples.

Boundary rule

Consumer payloads must not redefine Library-owned semantics.

Consumer payloads must not include fields that try to rename, override or mutate
Library references.

Forbidden examples include:

canonical_name_override
semantic_definition_override
library_alias_write
library_reference_write

Consumer payloads must also avoid runtime ownership fields that would imply
Library is performing downstream work.

Forbidden examples include:

final_price
price_formula
stock_mutation
material_write_off
order_creation
client_creation
payment_posting
production_runtime_write
telegram_runtime_behavior
calculator_runtime_integration
operational_registry_write
one_c_sync
one_c_import
What the pilot does

The pilot provides:

local consumer fixture examples
schema documentation
validation that referenced Library IDs exist in the reference contract examples
validation that consumer payloads do not redefine Library-owned semantics
validation that consumer payloads do not place downstream runtime ownership in Library
human-readable preview output
tests for valid and invalid payloads
What the pilot does not do

The pilot does not implement Calculator formulas.

The pilot does not implement Telegram runtime behavior.

The pilot does not implement Operational Registry storage.

The pilot does not implement Accounting Registry behavior.

The pilot does not implement Prepress Hub behavior.

The pilot does not import 1C data.

The pilot does not synchronize with 1C.

The pilot does not create clients.

The pilot does not create orders.

The pilot does not mutate stock.

The pilot does not calculate final price.

The pilot does not expose a live API.

The pilot does not start production runtime.

The pilot does not start Configurable Product Workbench.

Example preview

A valid consumer payload may be rendered as:

Consumer: calculator_engine
Uses Library reference: product_service::product_service.business_card.standard
Boundary: no semantic redefinition, no downstream runtime write

This means Calculator Engine may use the Library reference as a stable semantic
identifier, but Library does not calculate price and does not own Calculator
runtime behavior.

Readiness

This pilot proves that Library reference contracts can be consumed locally by
example downstream payloads while preserving module boundaries.

It prepares the ground for future module integration contracts, but does not
perform real integration.
```

### `docs/architecture/reference_contract_foundation.md`

- SHA256: `2ff2544795deebf35d5b5247c1196fbbc6419818fc45e9b01cf64dc9ce77f190`
- Bytes: `5775`

```markdown
# Library Reference Contract Foundation v0.2

## Purpose

This document defines the local ForPrint Library reference contract foundation.

The goal is to make Library-owned semantic/catalog references safe for downstream
modules without turning downstream modules into owners of Library truth.

This checkpoint is intentionally small.

It is not a production catalog implementation.

## Scope

The reference contract describes how downstream modules may store and exchange
references to Library-owned entities.

The contract covers:

```text
canonical Library reference id format
reference type / entity type
display label
optional alias input
reference resolution status
source module
schema/version marker
deprecation handling
ambiguous/manual-review handling
unknown/unresolved references
example downstream payloads
Library ownership

Library owns:

semantic/catalog IDs
product/service meaning
material meaning
operation meaning
unit meaning
template references
technical card references
aliases
deprecation rules
reference resolution semantics
Downstream ownership boundaries

Downstream modules may store Library references.

Downstream modules must not become owners of Library semantic/catalog truth.

Library must not own:

order state
client database
pricing logic
warehouse stock truth
payment/accounting truth
CRM workflow state
Telegram runtime behavior
Integration Gateway delivery ledger
production runtime state
Canonical reference id format

A canonical Library reference id should be stable, lowercase, namespaced and
dot-separated.

Recommended pattern:

<reference_type>.<domain>.<stable_name>[.<variant_or_version>]

Examples:

product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
operation.print.digital_color
unit.piece
template.business_card.90x50
technical_card.business_card.standard_v1

Reference ids are owned by Library.

Downstream modules should not invent new canonical Library ids locally.

If a downstream module receives user input that does not resolve to a known
Library id, it should store the user input as alias_input and mark the
reference with a non-confirmed resolution status.

Required payload shape

A downstream payload should carry a library_reference object.

Minimal fields:

library_reference:
  schema_version: library_reference_v0_2
  reference_type: product_service
  reference_id: product_service.business_card.standard
  display_label: Business card / standard
  resolution_status: library_reference_confirmed
  source_module: calculator_engine
  alias_input: "візитки стандарт"
Reference types

The v0.2 foundation covers these reference types:

product_service
material
operation
unit
template
technical_card
Resolution statuses

The v0.2 foundation uses these statuses:

library_reference_confirmed
library_reference_pending
ambiguous_manual_review_required
deprecated_reference
unknown
library_reference_confirmed

The reference is known and safe to use as a Library-owned canonical reference.

library_reference_pending

The reference has a plausible alias or provisional input, but Library has not
confirmed it yet.

ambiguous_manual_review_required

The input may match more than one Library-owned entity or needs human review.

deprecated_reference

The reference points to an older Library-owned id that should be migrated or
replaced when safe.

unknown

The input cannot currently be resolved to a known Library-owned entity.

Alias input

alias_input is optional.

It should preserve the original user-facing or downstream-provided wording.

Examples:

візитки стандарт
папір 300
кольоровий друк

Alias input is not a canonical id.

Alias input should not be used as a substitute for a confirmed Library reference.

Deprecation handling

Deprecated references should keep the original reference_id.

They may also provide a replacement candidate:

deprecation:
  is_deprecated: true
  replaced_by: product_service.business_card.standard
  message: Use the current standard business card reference.

Deprecation does not mean the downstream module owns migration truth.

It only means the Library reference contract can communicate the migration
direction.

Manual review handling

Ambiguous references should include a manual review marker:

manual_review:
  required: true
  reason: Multiple Library references may match the alias input.

Manual review should happen before treating the reference as confirmed.

Unknown references

Unknown references should preserve source context and alias input when available.

They should not silently become new Library ids.

A downstream module may keep the unresolved payload for intake, support or
operator review.

Safe downstream pattern

Downstream modules should store:

schema_version
reference_type
reference_id when known
display_label
resolution_status
source_module
alias_input when available
deprecation metadata when relevant
manual_review metadata when relevant

Downstream modules should not store copied Library catalog definitions as their
own source of truth.

Current checkpoint limitations

This checkpoint does not implement:

production catalog database
live API
CRM integration
Telegram integration
Operational Registry write
Calculator pricing logic
warehouse stock logic
accounting/payment logic
1C sync/write
automatic posting
production runtime service

Allowed in this checkpoint:

local docs
local YAML examples
schema files
tests for examples/schema
check-report visibility
small local validation helper
Related local files
examples/reference_contract/library_reference_examples.yaml
schemas/reference_contract/library_reference.schema.yaml
scripts/reference_contract/validate_library_reference_contract.py
tests/content/test_library_reference_contract.py

---
```

### `docs/architecture/semantic_reference_readiness.md`

- SHA256: `7a90b6878b87963788e3d56329313c9f8d1c7eb909a82e8f01e420bbe3958c7b`
- Bytes: `2091`

```markdown
# Semantic Reference Readiness v0.1

## Status

Draft readiness checkpoint for `forprint_library`.

## Purpose

This document defines a minimal semantic/reference readiness layer for early downstream module usage.

The goal is not to build the full production catalog database.

The goal is to show how downstream modules can safely refer to canonical Library IDs for product/service, material, operation and template meanings.

## Canonical reference examples

Current local examples are stored in:

```text
examples/semantic_reference_preview.yaml

The example file includes canonical IDs such as:

product_service.business_card.standard
material.paper.mondi_color_copy_300gsm
operation.print.digital_color
template.business_card.90x50

These IDs are stable sample references for early integration discussions.

They are not a final production catalog.

Alias readiness

Aliases are allowed as lookup helpers.

Aliases must not become canonical IDs.

If an alias maps clearly to one reference, the expected resolution status is:

confirmed_with_alias

If an alias is unknown, the expected resolution status is:

unresolved_manual_review_required

If an alias could match more than one canonical reference, the expected resolution status is:

ambiguous_manual_review_required
Boundary

Library owns semantic/catalog meaning.

Library does not own:

pricing formulas
warehouse stock truth
operational order state
client database
payment or accounting truth
production runtime state
Telegram runtime
CRM workflow
1C synchronization or posting
Downstream usage

Calculator Engine may reference canonical IDs for pricing input context, but pricing logic remains in Calculator.

Operational Registry may store canonical reference IDs as projections, but operational truth remains in Operational Registry.

Telegram Bot and CRM may display labels and route unresolved values for review, but they must not invent canonical semantic IDs.

Readiness conclusion

This checkpoint makes Library ready for early semantic/reference handoff.

It does not make Library a production catalog database.


---
```

### `docs/architecture/shared_operational_dictionary_policy.md`

- SHA256: `ebec7c0a6034fa87dea85931c77826d21f7bcb235529f8a7563552dc4ba8dd01`
- Bytes: `1190`

```markdown
# Shared Operational Dictionary Policy

## Status

Draft policy for Shared Operational Dictionary v0.1.

## Purpose

Library owns canonical shared operational dictionary definitions.
ForPrint Library owns canonical shared operational 
dictionary definitions for the ForPrint ecosystem.

These dictionaries define stable operational IDs, labels, descriptions, 
aliases, statuses and versioning rules for concepts reused by 
Operational Registry, Calculator Engine, 
Accounting Registry, Telegram Bot, CRM, Gateway, Prepress Hub, 
Warehouse, Logistics, Website and future Mobile App.

## Core rule

Library defines canonical dictionary values.

Other modules may consume these values, reference them, display 
their labels and create temporary local projections, 
but they must not become independent permanent dictionary authorities.

## Boundary

This dictionary layer does not create real operational orders, real clients, real payments, 
real material stock, real warehouse records, Calculator formulas, 
Telegram runtime, CRM dashboard or 1C synchronization.

Operational Registry owns operational facts and records.

Library owns canonical operational language and semantic references.
```

### `docs/architecture/status_dictionary_policy.md`

- SHA256: `0d82c7d987eb19b8cf696e2a850d30b45cae3792cd12bda765fda544dbb43c38`
- Bytes: `1037`

```markdown
# Status Dictionary Policy

## Status

Draft policy for shared status dictionaries.

## Purpose

Shared status dictionaries prevent modules from inventing 
conflicting values for the same operational state.

Examples include order_status, order_line_status, payment_status, 
production_status, workflow_status, workflow_stage_status, 
material_requirement_status, alert_event_status and notification_status.

## Stable IDs

Status IDs are stable machine values.

Labels may change, but IDs should remain stable unless a migration or deprecation rule is created.

## Consumption

Operational Registry should later reference these canonical values for operational records.

Calculator Engine should use these values when producing output packages.

Telegram Bot and CRM should display labels and must not invent internal status IDs.

Accounting Registry may map accounting statuses carefully 
without becoming the source of operational truth.

## Deprecated values

Deprecated values remain readable for historical records and migrations.
```

### `docs/decisions/ADR-0001-forprint-library-boundary.md`

- SHA256: `17a2d6e85189b3e2c417744ed54b21110d71c4108a4465f08ed2f5fbd9ab38d1`
- Bytes: `561`

```markdown
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
```

### `docs/decisions/ADR-0002-historical-compatibility.md`

- SHA256: `2db94f249420c4855554de1a9275886ec8637818f1c471ee9638048fe5140354`
- Bytes: `539`

```markdown
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
```

### `docs/operations/business_card_skeleton_recovery.md`

- SHA256: `d4bdf1f72c67d3e8a2e9853dc95e0f1c121f9de897b118a46b0fb599de57fd53`
- Bytes: `3382`

```markdown
# Business Card Skeleton Recovery

## Purpose

This document describes how to recover the accepted Library governance state
for the Business Card Skeleton checkpoint without changing the product model.

- Prompt ID: `library_configurable_product_workbench_business_card_skeleton_v0_1`
- Blueprint prompt ID: `2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1`
- Product ID: `product.business_card`
- Blueprint-accepted commit: `a87d62c`

## Known commit chain

Implementation and governance commits known for this checkpoint:

- `b8eb062` — Add Library business card product skeleton
- `7a7cb85` — Record Library business card skeleton completion
- `ad99e0a` — Clean business card closure exporter whitespace
- `1694215` — Finalize Library business card completion metadata
- `a87d62c` — Finalize Library business card Blueprint acceptance metadata

## Recovery principles

Recovery is limited to Library repository state and documentation metadata.

Do not recover by creating new product schema fields, runtime behavior,
Calculator formulas, 1C integrations, stock logic, production tasks or order
writes.

Do not write directly into the Blueprint repository from this Library-side
recovery process.

## Basic recovery inspection

From repository root:

`/srv/software_development/forprint-project/forprint_library`

Check branch and status:

`git status -sb`

Check recent commits:

`git log -5 --oneline`

Check that the canonical product card exists:

`test -f catalog/configurable_products/business_card.yaml`

Check that the completion report exists:

`test -f coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`

Check that no root-level duplicate completion report is tracked:

`git ls-files | grep '^2026-07-11__forprint_library__report__business-card-skeleton-v0-1\.md$' || true`

If that command prints nothing, no tracked root duplicate exists.

## Verification after recovery

Run focused tests:

`PYTHONPATH=app .venv_forprint_library/bin/python -m pytest tests/coordination/test_business_card_skeleton_closure.py tests/coordination/test_reference_consumption_pilot_closure.py tests/coordination/test_coordination_foundation_alignment_closure.py tests/content/test_business_card_product_card.py tests/contract/test_completion_report.py`

Run full checks:

`make check`

Run check report:

`make check-report`

Run whitespace check:

`git diff --check`

Restore generated report noise if it is timing-only:

`git restore reports/library_check_report.json reports/library_check_report.md`

## Expected healthy state

A healthy recovered state has:

- branch on `main`;
- clean `git status -sb`;
- focused tests passing;
- full tests passing;
- `make check-report` passing;
- `git diff --check` passing;
- completion report present under `coordination/reports/completion/`;
- no tracked root duplicate completion report;
- no Blueprint repository writes;
- no changes to `product.business_card` model during recovery.

## Escalation

Escalate to Blueprint only if:

- the accepted commit chain cannot be found;
- the canonical product card is missing;
- completion metadata contradicts the accepted implementation;
- focused tests fail after generated report noise is restored;
- recovery would require product model, runtime, Calculator, stock, 1C or
  production scope changes.
```

### `docs/operations/business_card_skeleton_runbook.md`

- SHA256: `c05da4141aac7d9caf6c40361f6fb631f742a329c9efd589bede122b50127e41`
- Bytes: `3919`

```markdown
# Business Card Skeleton Runbook

## Purpose

This runbook documents the governance operation procedure for the accepted
ForPrint Library configurable product reference:

- Prompt ID: `library_configurable_product_workbench_business_card_skeleton_v0_1`
- Blueprint prompt ID: `2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1`
- Product ID: `product.business_card`
- Blueprint-accepted commit: `a87d62c`

This runbook is governance documentation only. It does not authorize product
model changes, Calculator integration, runtime integration, production writes,
1C writes, stock writes or order writes.

## Scope

Use this runbook when checking, reviewing or preparing the Library-side
business card skeleton for Blueprint governance acceptance.

The accepted implementation provides a Library reference object for business
cards / візитки. It is not a production runtime component and it is not a
pricing engine.

## Canonical artifacts

Product and schema artifacts:

- `catalog/configurable_products/business_card.yaml`
- `schemas/configurable_product.schema.yaml`
- `examples/product_cards/business_card_product_card.yaml`

Documentation artifacts:

- `docs/architecture/configurable_product_workbench.md`
- `docs/architecture/business_card_skeleton.md`
- `docs/operations/business_card_skeleton_runbook.md`
- `docs/operations/business_card_skeleton_recovery.md`

Validation and preview artifacts:

- `scripts/product_workbench/validate_business_card_product.py`
- `scripts/product_workbench/preview_business_card_product.py`
- `tests/content/test_business_card_product_card.py`

Completion metadata artifacts:

- `coordination/reports/completion/2026-07-11__forprint_library__report__business-card-skeleton-v0-1.md`
- `coordination/reports/index.yaml`
- `coordination/status/current_status.yaml`
- `coordination/status/current_status.md`
- `coordination/status/next_questions_for_blueprint.md`

## Standard verification commands

Run from the repository root:

`/srv/software_development/forprint-project/forprint_library`

Focused tests:

`PYTHONPATH=app .venv_forprint_library/bin/python -m pytest tests/coordination/test_business_card_skeleton_closure.py tests/coordination/test_reference_consumption_pilot_closure.py tests/coordination/test_coordination_foundation_alignment_closure.py tests/content/test_business_card_product_card.py tests/contract/test_completion_report.py`

Full check:

`make check`

Check report:

`make check-report`

Whitespace check:

`git diff --check`

## Generated report noise

`make check-report` may regenerate timing-only report files:

- `reports/library_check_report.json`
- `reports/library_check_report.md`

If those files contain only generated/timing changes, restore them before commit:

`git restore reports/library_check_report.json reports/library_check_report.md`

## Acceptance checklist

Before handing back to Blueprint, confirm:

- focused tests pass;
- `make check` passes;
- `make check-report` passes;
- `git diff --check` passes;
- no root-level duplicate completion report exists;
- generated report noise is not committed unless intentionally required;
- `git status -sb` is clean after commit/push;
- Blueprint repository was not written from the Library-side task;
- `product.business_card` model was not changed during governance closeout.

## Boundary reminders

This checkpoint must not add:

- product schema expansion;
- Calculator integration;
- price formulas;
- stock truth;
- material write-off logic;
- 1C import or synchronization;
- order writes;
- CRM writes;
- Website writes;
- production runtime;
- production task creation;
- real client or order data.

## Calculator dependency note

Calculator may later consume `product.business_card` and its constructor parameters as
reference input context.

This runbook does not define Calculator formulas, pricing ownership or
Calculator runtime integration.
```

### `docs/operations/library_calculator_input_contract_recovery.md`

- SHA256: `82e4112b6195fdf622dd42f8d62553e2255023ebc4402368e4d600d6ee551c9f`
- Bytes: `1827`

```markdown
# Library Calculator Input Contract Recovery

## Purpose

Recovery guidance for the Library Calculator input contract v0.1.

## Recovery principle

Recover by restoring Library reference contract files and fixtures only. Do not
add prices, Calculator internals, external writes, stock truth, 1C sync,
production runtime, order writes or new product-model scope.

## Recovery checks

From repository root:

```bash
git status -sb
git log -8 --oneline
test -f app/forprint_library/calculator_input/contract.py
test -f schemas/calculator_input/calculator_input_envelope.schema.yaml
test -d examples/calculator_input_contract
```

Run focused validation:

```bash
PYTHONPATH=app .venv_forprint_library/bin/python -m pytest   tests/content/test_calculator_input_contract.py   tests/content/test_business_card_product_card.py

PYTHONPATH=app .venv_forprint_library/bin/python   scripts/calculator_input/validate_calculator_input_contract.py
```

Run full validation before returning to Blueprint:

```bash
make lint
make format-check
make check
make governance-check
make module-validate
make check-report
make check-report-full
git diff --check
git status -sb
```

## Incompatible schema or fixture regression

If a fixture no longer matches deterministic output:

1. do not edit Calculator behavior;
2. inspect `app/forprint_library/calculator_input/contract.py`;
3. compare the fixture to current `build_calculator_input(...).to_dict()`;
4. restore deterministic ordering and stable schema version;
5. rerun focused and full validation.

## Escalation

Escalate to Blueprint if recovery requires:

- changing `product.business_card`;
- adding Calculator formulas;
- introducing a Calculator package dependency;
- changing public error taxonomy;
- writing to external systems;
- changing order, stock, 1C, production or CRM scope.
```

### `docs/operations/library_calculator_input_contract_runbook.md`

- SHA256: `95973032ebe86ff69faab529404a4c0bcd807720d249412a8dff88c831d183ab`
- Bytes: `1896`

```markdown
# Library Calculator Input Contract Runbook

## Purpose

Runbook for verifying the read-only Library Calculator input contract v0.1.

## Scope

This runbook applies only to:

`forprint_library_calculator_input_contract_v0_1`

It covers `product.business_card` projection into Calculator-ready reference
input. It does not authorize pricing, Calculator runtime integration, stock,
1C, order, CRM, Telegram, Logistics, Gateway or production writes.

## Key artifacts

- `app/forprint_library/calculator_input/contract.py`
- `schemas/calculator_input/calculator_input_envelope.schema.yaml`
- `examples/calculator_input_contract/`
- `scripts/calculator_input/validate_calculator_input_contract.py`
- `tests/content/test_calculator_input_contract.py`
- `docs/architecture/library_calculator_input_contract.md`

## Focused verification

```bash
PYTHONPATH=app .venv_forprint_library/bin/python -m pytest   tests/content/test_calculator_input_contract.py   tests/content/test_business_card_product_card.py

PYTHONPATH=app .venv_forprint_library/bin/python   scripts/calculator_input/validate_calculator_input_contract.py
```

## Full validation

```bash
make lint
make format-check
make check
make governance-check
make module-validate
make check-report
make check-report-full
git diff --check
git status -sb
```

## Generated report noise

`make check-report` and `make check-report-full` may update:

- `reports/library_check_report.json`
- `reports/library_check_report.md`

If those contain only generated timing/status noise, restore before commit:

```bash
git restore reports/library_check_report.json reports/library_check_report.md
```

## Expected healthy state

- focused tests pass;
- full Library test suite passes;
- fixture validator passes;
- `git diff --check` passes;
- no product model changes are required;
- no Calculator dependency is imported;
- no external writes are performed.
```

### `examples/calculator_input_contract/business_card_with_artwork_source.yaml`

- SHA256: `0cd3b15949f4020ed31e2680abd430f01ce3a9905776188b9136074f5ac5cb36`
- Bytes: `1651`

```yaml
schema_version: calculator_input_fixture_v0_1
case_id: business_card_with_artwork_source
description: Valid business card projection with optional artwork source.
product_id: product.business_card
input_configuration:
  size: size_90x50_mm
  sides: one_sided
  material_ref:
    catalog: materials
    id: paper_300g_matte
  print_mode_ref:
    catalog: print_modes
    id: color_4_0
  quantity: 250
  artwork_source: customer_needs_prepress_check
expected_output:
  schema_version: calculator_input_envelope_v0_1
  product_id: product.business_card
  configuration_id: calc_input_28601317bb609ed2
  normalized_parameters:
    size: size_90x50_mm
    sides: one_sided
    material_ref:
      catalog: materials
      id: paper_300g_matte
    print_mode_ref:
      catalog: print_modes
      id: color_4_0
    quantity: 250
    finishing_refs: []
    artwork_source: customer_needs_prepress_check
  reference_ids:
    product_id: product.business_card
    size_id: size_90x50_mm
    sides_id: one_sided
    material_ref:
      catalog: materials
      id: paper_300g_matte
    print_mode_ref:
      catalog: print_modes
      id: color_4_0
    finishing_refs: []
  validation_snapshot:
    schema_version: calculator_input_validation_snapshot_v0_1
    valid: true
    errors: []
    warnings: []
    required_parameters:
    - size
    - sides
    - material_ref
    - print_mode_ref
    - quantity
    normalization_notes:
    - Output field order is stable.
    - finishing_refs are sorted by catalog and id.
    - Optional artwork_source is included only when supplied.
    - No monetary, pricing, stock, production or runtime fields are projected.
```

### `examples/calculator_input_contract/business_card_with_finishing.yaml`

- SHA256: `ef1506d91eb039b959f3f9942da1fe95fd549b9dd1cf667ee682242855a1b923`
- Bytes: `1914`

```yaml
schema_version: calculator_input_fixture_v0_1
case_id: business_card_with_finishing
description: Valid business card projection with deterministic finishing refs.
product_id: product.business_card
input_configuration:
  size: size_85x55_mm
  sides: two_sided
  material_ref:
    catalog: materials
    id: paper_350g_gloss
  print_mode_ref:
    catalog: print_modes
    id: color_4_4
  quantity: 500
  finishing_refs:
  - catalog: finishing_options
    id: matte_lamination
  - catalog: finishing_options
    id: corner_rounding
expected_output:
  schema_version: calculator_input_envelope_v0_1
  product_id: product.business_card
  configuration_id: calc_input_7eb5af3a5f80d3b5
  normalized_parameters:
    size: size_85x55_mm
    sides: two_sided
    material_ref:
      catalog: materials
      id: paper_350g_gloss
    print_mode_ref:
      catalog: print_modes
      id: color_4_4
    quantity: 500
    finishing_refs:
    - catalog: finishing_options
      id: corner_rounding
    - catalog: finishing_options
      id: matte_lamination
  reference_ids:
    product_id: product.business_card
    size_id: size_85x55_mm
    sides_id: two_sided
    material_ref:
      catalog: materials
      id: paper_350g_gloss
    print_mode_ref:
      catalog: print_modes
      id: color_4_4
    finishing_refs:
    - catalog: finishing_options
      id: corner_rounding
    - catalog: finishing_options
      id: matte_lamination
  validation_snapshot:
    schema_version: calculator_input_validation_snapshot_v0_1
    valid: true
    errors: []
    warnings: []
    required_parameters:
    - size
    - sides
    - material_ref
    - print_mode_ref
    - quantity
    normalization_notes:
    - Output field order is stable.
    - finishing_refs are sorted by catalog and id.
    - Optional artwork_source is included only when supplied.
    - No monetary, pricing, stock, production or runtime fields are projected.
```

### `examples/calculator_input_contract/invalid_missing_material.yaml`

- SHA256: `230e96f0b82ba81f3a8afe79d5b5f9c55460527aae1ded5f07897e37fdbfffaa`
- Bytes: `567`

```yaml
schema_version: calculator_input_error_fixture_v0_1
case_id: invalid_missing_material
description: Invalid business card projection without material_ref.
product_id: product.business_card
input_configuration:
  size: size_90x50_mm
  sides: one_sided
  print_mode_ref:
    catalog: print_modes
    id: color_4_0
  quantity: 100
expected_error:
  schema_version: calculator_input_error_v0_1
  error_type: missing_required_parameter
  message: Missing required Calculator input parameter.
  field_path: material_ref
  details:
    missing_parameters:
    - material_ref
```

### `examples/calculator_input_contract/invalid_print_mode_reference.yaml`

- SHA256: `2d9dd38ecab4f1281b917f787d5215b93303bcbe6a8db570270e1a3cfee3d6fb`
- Bytes: `705`

```yaml
schema_version: calculator_input_error_fixture_v0_1
case_id: invalid_print_mode_reference
description: Invalid business card projection with unknown print mode reference.
product_id: product.business_card
input_configuration:
  size: size_90x50_mm
  sides: one_sided
  material_ref:
    catalog: materials
    id: paper_300g_matte
  print_mode_ref:
    catalog: print_modes
    id: unknown_print_mode
  quantity: 100
expected_error:
  schema_version: calculator_input_error_v0_1
  error_type: invalid_reference
  message: Reference parameter id is not allowed for this product.
  field_path: print_mode_ref
  details:
    reference_id: unknown_print_mode
    allowed_refs:
    - color_4_0
    - color_4_4
```

### `examples/calculator_input_contract/invalid_quantity.yaml`

- SHA256: `4dcfd185cb7591e9d175e3e4955fe77055006fc6955c03f956b3a737d30a90d3`
- Bytes: `595`

```yaml
schema_version: calculator_input_error_fixture_v0_1
case_id: invalid_quantity
description: Invalid business card projection with zero quantity.
product_id: product.business_card
input_configuration:
  size: size_90x50_mm
  sides: one_sided
  material_ref:
    catalog: materials
    id: paper_300g_matte
  print_mode_ref:
    catalog: print_modes
    id: color_4_0
  quantity: 0
expected_error:
  schema_version: calculator_input_error_v0_1
  error_type: invalid_configuration
  message: Quantity must be greater than or equal to 1.
  field_path: quantity
  details:
    minimum: 1
    value: 0
```

### `examples/calculator_input_contract/minimal_valid_business_card.yaml`

- SHA256: `2a72eb680edcbe9284f5106ee64ab7cf6da6266599083edd64d42b22dcd86d3b`
- Bytes: `1543`

```yaml
schema_version: calculator_input_fixture_v0_1
case_id: minimal_valid_business_card
description: Minimal valid business card Calculator input projection.
product_id: product.business_card
input_configuration:
  size: size_90x50_mm
  sides: one_sided
  material_ref:
    catalog: materials
    id: paper_300g_matte
  print_mode_ref:
    catalog: print_modes
    id: color_4_0
  quantity: 100
expected_output:
  schema_version: calculator_input_envelope_v0_1
  product_id: product.business_card
  configuration_id: calc_input_9e21b73a7e5c28db
  normalized_parameters:
    size: size_90x50_mm
    sides: one_sided
    material_ref:
      catalog: materials
      id: paper_300g_matte
    print_mode_ref:
      catalog: print_modes
      id: color_4_0
    quantity: 100
    finishing_refs: []
  reference_ids:
    product_id: product.business_card
    size_id: size_90x50_mm
    sides_id: one_sided
    material_ref:
      catalog: materials
      id: paper_300g_matte
    print_mode_ref:
      catalog: print_modes
      id: color_4_0
    finishing_refs: []
  validation_snapshot:
    schema_version: calculator_input_validation_snapshot_v0_1
    valid: true
    errors: []
    warnings: []
    required_parameters:
    - size
    - sides
    - material_ref
    - print_mode_ref
    - quantity
    normalization_notes:
    - Output field order is stable.
    - finishing_refs are sorted by catalog and id.
    - Optional artwork_source is included only when supplied.
    - No monetary, pricing, stock, production or runtime fields are projected.
```

### `examples/catalog_seed_v0_1.example.yaml`

- SHA256: `3b28e14cf85af6a9ba1815e0041fd7de917d6d26fbfd9105bb9fa9dd8bc66746`
- Bytes: `1954`

```yaml
metadata:
  id: canonical_catalog_seed_v0_1_example
  name: Canonical Catalog Seed v0.1 Example
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: Example projection-safe catalog seed structure.
materials:
- id: paper_300g_matte
  name_uk: Папір 300 г матовий
  name_en: 300 gsm matte paper
  aliases:
  - папір 300 мат
  - 300gsm matte
  - матовий папір 300 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
product_families:
- id: business_card
  name_uk: Візитка
  name_en: Business card
  aliases:
  - візитка
  - business card
  - карточка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for small-format contact cards.
operations:
- id: digital_print
  name_uk: Цифровий друк
  name_en: Digital print
  aliases:
  - цифровий друк
  - digital print
  - друк цифровий
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
print_modes:
- id: color_4_0
  name_uk: 4+0
  name_en: Full color one side
  aliases:
  - 4+0
  - односторонній повноколір
  - full color one side
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
finishing_options:
- id: none
  name_uk: Без постобробки
  name_en: No finishing
  aliases:
  - без постобробки
  - no finishing
  - без додаткової обробки
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
```

### `examples/reference_consumption/library_reference_consumption_examples.yaml`

- SHA256: `f35d68cb5389737d48c893ca2d8c76f6e8e631c7edbff791fe0109730b606089`
- Bytes: `6319`

```yaml
schema_version: library_reference_consumption_examples_v0_3
pilot_id: library_reference_consumption_pilot_v0_3
owner_module: forprint_library
description: >
  Local, read-only examples showing how downstream ForPrint modules may consume
  Library reference contract identifiers without redefining Library-owned
  semantics or adding downstream runtime ownership to Library.

reference_contract_source:
  schema_version: library_reference_v0_2
  path: examples/reference_contract/library_reference_examples.yaml
  note: >
    These examples consume the controlled Library reference contract examples.
    They are not production catalog records and do not start Configurable Product
    Workbench.

valid_consumer_payloads:
  - id: calculator_pricing_context_reference
    description: Calculator Engine keeps a Library product reference as pricing context input.
    consumer_module: calculator_engine
    consumer_payload_id: calculator_context_demo_001
    library_owned_reference:
      schema_version: library_reference_v0_2
      reference_type: product_service
      reference_id: product_service.business_card.standard
      display_label: Business card / standard
      resolution_status: library_reference_confirmed
    consumer_owned_fields:
      pricing_context_note: Example pricing context only; no price calculation is performed.
      requested_quantity: 500
      requested_size_hint: 90x50
    foreign_module_references:
      calculator_context_reference: calculator_engine.demo.pricing_context_001
    boundary_assertions:
      example_only: true
      no_library_semantic_redefinition: true
      no_downstream_runtime_write: true
      no_price_calculation: true

  - id: telegram_channel_hint_reference
    description: Telegram Bot keeps a Library template reference as a channel-local hint.
    consumer_module: telegram_bot
    consumer_payload_id: telegram_hint_demo_001
    library_owned_reference:
      schema_version: library_reference_v0_2
      reference_type: template
      reference_id: template.business_card.90x50
      display_label: Business card template 90x50
      resolution_status: library_reference_confirmed
    consumer_owned_fields:
      channel_hint: User mentioned a 90x50 business card layout.
      message_locale: uk-UA
    foreign_module_references:
      telegram_message_reference: telegram_bot.demo.message_001
    boundary_assertions:
      example_only: true
      no_library_semantic_redefinition: true
      no_downstream_runtime_write: true
      no_telegram_runtime_behavior: true

  - id: operational_registry_foreign_reference
    description: Operational Registry stores a Library material reference as foreign-domain metadata.
    consumer_module: forprint_operational_registry
    consumer_payload_id: operational_reference_demo_001
    library_owned_reference:
      schema_version: library_reference_v0_2
      reference_type: material
      reference_id: material.paper.mondi_color_copy_300gsm
      display_label: Mondi Color Copy 300 gsm
      resolution_status: library_reference_confirmed
    consumer_owned_fields:
      operational_note: Example foreign-domain metadata only.
      local_task_reference: operational_registry.demo.task_001
    foreign_module_references:
      operational_registry_reference: forprint_operational_registry.demo.material_ref_001
    boundary_assertions:
      example_only: true
      no_library_semantic_redefinition: true
      no_downstream_runtime_write: true
      no_stock_mutation: true

invalid_consumer_payloads:
  - id: invalid_unknown_library_reference_id
    expected_error_contains: unknown Library reference id
    description: Consumer payload points to a reference ID that is not present in the Library reference contract examples.
    consumer_module: calculator_engine
    consumer_payload_id: invalid_calculator_context_demo_001
    library_owned_reference:
      schema_version: library_reference_v0_2
      reference_type: product_service
      reference_id: product_service.unknown.not_registered
      display_label: Unknown product/service
      resolution_status: library_reference_confirmed
    consumer_owned_fields:
      pricing_context_note: Invalid example.
    foreign_module_references:
      calculator_context_reference: calculator_engine.demo.invalid_context_001
    boundary_assertions:
      example_only: true
      no_library_semantic_redefinition: true
      no_downstream_runtime_write: true

  - id: invalid_consumer_redefines_library_semantics
    expected_error_contains: forbidden field
    description: Consumer tries to redefine Library-owned meaning.
    consumer_module: telegram_bot
    consumer_payload_id: invalid_telegram_hint_demo_001
    library_owned_reference:
      schema_version: library_reference_v0_2
      reference_type: template
      reference_id: template.business_card.90x50
      display_label: Business card template 90x50
      resolution_status: library_reference_confirmed
    consumer_owned_fields:
      channel_hint: Invalid example.
      canonical_name_override: Consumer tries to rename a Library-owned semantic reference.
    foreign_module_references:
      telegram_message_reference: telegram_bot.demo.invalid_message_001
    boundary_assertions:
      example_only: true
      no_library_semantic_redefinition: false
      no_downstream_runtime_write: true

  - id: invalid_consumer_runtime_ownership
    expected_error_contains: forbidden field
    description: Consumer payload tries to place runtime write responsibility into the Library reference consumption payload.
    consumer_module: forprint_operational_registry
    consumer_payload_id: invalid_operational_reference_demo_001
    library_owned_reference:
      schema_version: library_reference_v0_2
      reference_type: material
      reference_id: material.paper.mondi_color_copy_300gsm
      display_label: Mondi Color Copy 300 gsm
      resolution_status: library_reference_confirmed
    consumer_owned_fields:
      operational_note: Invalid example.
      stock_mutation: reserve 100 sheets
    foreign_module_references:
      operational_registry_reference: forprint_operational_registry.demo.invalid_material_ref_001
    boundary_assertions:
      example_only: true
      no_library_semantic_redefinition: true
      no_downstream_runtime_write: false
```

### `examples/reference_contract/library_reference_examples.yaml`

- SHA256: `5b8d17be4e4869d646f48848f6b94f15cb033f8150df24efec6ca74e9cf5d8d2`
- Bytes: `7487`

```yaml
schema_version: library_reference_examples_v0_2
contract_id: library_reference_contract_foundation_v0_2
owner_module: forprint_library
description: >
  Local non-production examples for safe downstream references to
  Library-owned semantic/catalog entities.

library_reference_contract:
  schema_version: library_reference_v0_2
  allowed_reference_types:
    - product_service
    - material
    - operation
    - unit
    - template
    - technical_card
  allowed_resolution_statuses:
    - library_reference_confirmed
    - library_reference_pending
    - ambiguous_manual_review_required
    - deprecated_reference
    - unknown
  allowed_source_modules:
    - calculator_engine
    - forprint_operational_registry
    - forprint_integration_gateway
    - telegram_bot
    - future_forprint_crm
    - forprint_library

examples:
  - id: product_service_confirmed
    description: Confirmed product/service reference from Calculator input.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: product_service
        reference_id: product_service.business_card.standard
        display_label: Business card / standard
        resolution_status: library_reference_confirmed
        source_module: calculator_engine
        alias_input: "візитки стандарт"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: material_confirmed
    description: Confirmed material reference for operational projection.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: material
        reference_id: material.paper.mondi_color_copy_300gsm
        display_label: Mondi Color Copy 300 gsm
        resolution_status: library_reference_confirmed
        source_module: forprint_operational_registry
        alias_input: "папір 300"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: operation_confirmed
    description: Confirmed operation reference from Integration Gateway intake.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: operation
        reference_id: operation.print.digital_color
        display_label: Digital color print
        resolution_status: library_reference_confirmed
        source_module: forprint_integration_gateway
        alias_input: "кольоровий друк"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: unit_confirmed
    description: Confirmed unit reference.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: unit
        reference_id: unit.piece
        display_label: Piece
        resolution_status: library_reference_confirmed
        source_module: calculator_engine
        alias_input: "шт"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: template_confirmed
    description: Confirmed template reference.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: template
        reference_id: template.business_card.90x50
        display_label: Business card template 90x50
        resolution_status: library_reference_confirmed
        source_module: telegram_bot
        alias_input: "візитка 90 на 50"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: technical_card_confirmed
    description: Confirmed technical card reference.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: technical_card
        reference_id: technical_card.business_card.standard_v1
        display_label: Business card standard technical card v1
        resolution_status: library_reference_confirmed
        source_module: future_forprint_crm
        alias_input: "стандартна техкарта візитки"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: product_service_pending
    description: Pending product/service reference from unconfirmed alias.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: product_service
        reference_id: product_service.flyer.pending
        display_label: Flyer / pending Library confirmation
        resolution_status: library_reference_pending
        source_module: telegram_bot
        alias_input: "флаєри прості"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: false
          reason:

  - id: ambiguous_material_manual_review
    description: Ambiguous material reference that must be reviewed manually.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: material
        reference_id: material.paper.ambiguous
        display_label: Paper / ambiguous
        resolution_status: ambiguous_manual_review_required
        source_module: forprint_integration_gateway
        alias_input: "крейда 300"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: true
          reason: >
            Alias may refer to multiple coated paper references and requires
            Library/operator review.

  - id: deprecated_template_reference
    description: Deprecated template reference with replacement direction.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: template
        reference_id: template.business_card.old_90x50
        display_label: Business card old 90x50 template
        resolution_status: deprecated_reference
        source_module: forprint_operational_registry
        alias_input: "старий шаблон візитки"
        deprecation:
          is_deprecated: true
          replaced_by: template.business_card.90x50
          message: Use the current 90x50 business card template reference.
        manual_review:
          required: false
          reason:

  - id: unknown_operation_reference
    description: Unknown operation reference that must not become a local id.
    downstream_payload:
      library_reference:
        schema_version: library_reference_v0_2
        reference_type: operation
        reference_id:
        display_label: Unknown operation
        resolution_status: unknown
        source_module: telegram_bot
        alias_input: "зробити красиво"
        deprecation:
          is_deprecated: false
          replaced_by:
          message:
        manual_review:
          required: true
          reason: >
            Input cannot be resolved to a known Library operation reference.
```

### `examples/semantic_reference_preview.yaml`

- SHA256: `dbd51fa3eda8fb28c8e3f4b81b5441968443c339e6f631c1480534549d9edb14`
- Bytes: `4187`

```yaml
metadata:
  id: semantic_reference_preview_v0_1
  version: "0.1"
  owner_module: forprint_library
  status: draft_semantic_reference_readiness_v0_1
  usage: local_demo_and_downstream_handoff_only
  contract_status: not_final_contract
  production_catalog_status: not_production_catalog_database

canonical_references:
  - id: product_service.business_card.standard
    reference_type: product_service
    label_uk: Візитка стандартна
    label_en: Standard business card
    aliases:
      - візитка
      - визитка
      - business card
    readiness_status: ready_for_reference_example
    downstream_usage:
      calculator_engine: may_reference_id_for_pricing_input_context
      forprint_operational_registry: may_store_reference_id_without_owning_catalog_meaning
    forbidden_usage:
      - pricing_formula
      - warehouse_stock_truth
      - operational_order_state

  - id: material.paper.mondi_color_copy_300gsm
    reference_type: material
    label_uk: Папір Mondi Color Copy 300 г/м²
    label_en: Mondi Color Copy 300gsm paper
    aliases:
      - mondi 300
      - color copy 300
      - папір 300
    readiness_status: ready_for_reference_example
    downstream_usage:
      calculator_engine: may_reference_material_id_for_estimation_context
      forprint_operational_registry: may_store_material_reference_projection
    forbidden_usage:
      - warehouse_quantity
      - purchase_accounting_truth
      - supplier_invoice_truth

  - id: operation.print.digital_color
    reference_type: operation
    label_uk: Цифровий кольоровий друк
    label_en: Digital color print
    aliases:
      - кольоровий друк
      - digital color
      - цифра колір
    readiness_status: ready_for_reference_example
    downstream_usage:
      calculator_engine: may_reference_operation_id_for_rule_selection_context
      forprint_operational_registry: may_store_operation_reference_projection
    forbidden_usage:
      - machine_runtime_truth
      - operator_assignment
      - production_execution_status

  - id: template.business_card.90x50
    reference_type: template
    label_uk: Шаблон візитки 90x50 мм
    label_en: Business card template 90x50 mm
    aliases:
      - 90x50
      - business card 90x50
      - візитка 90х50
    readiness_status: ready_for_reference_example
    downstream_usage:
      calculator_engine: may_reference_template_id_for_size_context
      forprint_operational_registry: may_store_template_reference_projection
    forbidden_usage:
      - final_layout_file_truth
      - prepress_runtime_state
      - production_approval_status

alias_resolution_examples:
  - input: візитка
    expected_reference_id: product_service.business_card.standard
    expected_resolution_status: confirmed_with_alias

  - input: mondi 300
    expected_reference_id: material.paper.mondi_color_copy_300gsm
    expected_resolution_status: confirmed_with_alias

  - input: unknown material name
    expected_reference_id: null
    expected_resolution_status: unresolved_manual_review_required

ambiguous_naming_examples:
  - input: банер
    candidates:
      - product_service.banner.indoor
      - product_service.banner.outdoor
    expected_resolution_status: ambiguous_manual_review_required
    note: Library should report ambiguity instead of inventing a canonical ID.

downstream_handoff_notes:
  calculator_engine:
    allowed:
      - reference canonical product_service/material/operation/template IDs
      - use aliases only for input normalization
      - keep pricing formulas outside Library
    forbidden:
      - treat Library examples as final production pricing catalog
      - write Calculator pricing logic into Library

  forprint_operational_registry:
    allowed:
      - store canonical reference IDs as projections
      - record unresolved or ambiguous references for review
      - keep operational records separate from Library definitions
    forbidden:
      - make Library the order database
      - store operational lifecycle truth in Library
      - write warehouse stock or payment truth into Library
```

### `pyproject.toml`

- SHA256: `b495cd39f3cb7f711dc15c2cb2d0c5a7e1d97c77ae6c7b81ef8a00166faff36c`
- Bytes: `857`

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "forprint-library"
version = "0.1.0"
description = "Canonical catalog, semantic naming, alias and contract-definition authority for the ForPrint ecosystem."
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.7.0",
    "jsonschema>=4.22.0",
    "PyYAML>=6.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.2.0",
    "ruff>=0.5.0",
    "mypy>=1.10.0",
]

[tool.setuptools.packages.find]
where = ["app"]

[tool.pytest.ini_options]
pythonpath = ["app"]
testpaths = ["tests"]
addopts = "-q"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.11"
strict = true
mypy_path = "app"
```

### `schemas/calculator_input/calculator_input_envelope.schema.yaml`

- SHA256: `26146654e9a3317d1792c51ef1cd32d8e1b4d41de160e421b3c1a3b1074e64c8`
- Bytes: `1079`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Library Calculator Input Envelope
type: object
required:
  - schema_version
  - product_id
  - configuration_id
  - normalized_parameters
  - reference_ids
  - validation_snapshot
properties:
  schema_version:
    const: calculator_input_envelope_v0_1
  product_id:
    const: product.business_card
  configuration_id:
    type: string
    pattern: ^calc_input_[a-f0-9]{16}$
  normalized_parameters:
    type: object
    required:
      - size
      - sides
      - material_ref
      - print_mode_ref
      - quantity
      - finishing_refs
    additionalProperties: true
  reference_ids:
    type: object
    required:
      - product_id
      - size_id
      - sides_id
      - material_ref
      - print_mode_ref
      - finishing_refs
    additionalProperties: true
  validation_snapshot:
    type: object
    required:
      - schema_version
      - valid
      - errors
      - warnings
      - required_parameters
      - normalization_notes
    additionalProperties: true
additionalProperties: false
```

### `schemas/catalog_seed.schema.yaml`

- SHA256: `7369da57d72df233a1432ba86ba68c72a40ca1a89e0f4b6fb7e5f766a7a0acdb`
- Bytes: `2119`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Catalog Seed
type: object
required:
- metadata
- materials
- product_families
- operations
- print_modes
- finishing_options
properties:
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  materials:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  product_families:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  operations:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  print_modes:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  finishing_options:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
additionalProperties: false
$defs:
  catalog_item:
    type: object
    required:
    - id
    - name_uk
    - name_en
    - aliases
    - status
    - version
    - owner_module
    - schema_status
    - notes
    properties:
      id:
        type: string
        pattern: ^[a-z0-9_]+$
      name_uk:
        type: string
        minLength: 1
      name_en:
        type: string
        minLength: 1
      aliases:
        type: array
        minItems: 1
        items:
          type: string
          minLength: 1
      status:
        enum:
        - draft
        - active
        - deprecated
        - experimental
      version:
        type: string
      owner_module:
        const: forprint_library
      schema_status:
        const: unstable_v0_1
      notes:
        type: string
    additionalProperties: true
```

### `schemas/configurable_product.schema.yaml`

- SHA256: `ba6c6941e13f047a6d7b198b0c8164a366ad180c615b1b7e0540014229b41ddc`
- Bytes: `1758`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Configurable Product Card
type: object
required:
  - schema_version
  - product_id
  - kind
  - status
  - version
  - owner_module
  - names
  - aliases
  - constructor_parameters
  - consumer_usage_notes
  - boundary_notes
properties:
  schema_version:
    const: configurable_product_card_v0_1
  product_id:
    type: string
    pattern: ^product\.[a-z0-9_]+$
  kind:
    const: configurable_product
  status:
    enum:
      - draft_reference
      - active_reference
      - deprecated_reference
  version:
    type: string
  owner_module:
    const: forprint_library
  names:
    type: object
    required:
      - uk
      - en
    properties:
      uk:
        type: string
        minLength: 1
      en:
        type: string
        minLength: 1
    additionalProperties: true
  aliases:
    type: array
    minItems: 1
    items:
      type: string
      minLength: 1
  compatibility_aliases:
    type: array
    items:
      type: string
      minLength: 1
  product_family_ref:
    type: object
    required:
      - catalog
      - id
    properties:
      catalog:
        const: product_families
      id:
        type: string
    additionalProperties: true
  constructor_parameters:
    type: array
    minItems: 1
    items:
      type: object
      required:
        - key
        - type
        - required
      properties:
        key:
          type: string
          pattern: ^[a-z0-9_]+$
        type:
          type: string
        required:
          type: boolean
      additionalProperties: true
  consumer_usage_notes:
    type: object
    additionalProperties: true
  boundary_notes:
    type: object
    additionalProperties: true
additionalProperties: true
```

### `schemas/dictionary_entry.schema.yaml`

- SHA256: `ce8d1fa752b0e29b55dc053012f1ddd6c6b64219d55be02147b8985b345cee16`
- Bytes: `741`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Dictionary Entry
type: object
required:
- id
- label_uk
- label_en
- description
- status
- aliases
- owner_module
- dictionary_group
- version
- notes
properties:
  id:
    type: string
    pattern: ^[a-z0-9_]+$
  label_uk:
    type: string
    minLength: 1
  label_en:
    type: string
    minLength: 1
  description:
    type: string
    minLength: 1
  status:
    enum:
    - active
    - draft
    - deprecated
  aliases:
    type: array
    items:
      type: string
      minLength: 1
  owner_module:
    const: forprint_library
  dictionary_group:
    type: string
    minLength: 1
  version:
    const: '0.1'
  notes:
    type: string
additionalProperties: true
```

### `schemas/finishing_option.schema.yaml`

- SHA256: `ad22428258457bd45347fe97ce8b0a7665ed5c5798619c81558f948012a00505`
- Bytes: `1761`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Finishing Option Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: finishing_options
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

### `schemas/material.schema.yaml`

- SHA256: `f363b1a32fe60f275282427068444576a024a6dc519265e44f8a1ca74526486e`
- Bytes: `1745`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Material Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: materials
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

### `schemas/operation.schema.yaml`

- SHA256: `b6b7f80b7fbfb016d6599502b1bc39aa2311b6bb701ced1f3194bbe53b9c288d`
- Bytes: `1747`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Operation Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: operations
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

### `schemas/print_mode.schema.yaml`

- SHA256: `a73dad6ae5d41b5b8be7275a2cd39792ce9192addfdfb65ceebf6cc153844e0f`
- Bytes: `1749`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Print Mode Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: print_modes
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

### `schemas/product_family.schema.yaml`

- SHA256: `6544b3cc1c7fc267a477544fa39847236e63454a1698aad659f7b687b57bbaab`
- Bytes: `1758`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Product Family Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: product_families
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

### `schemas/reference_consumption/library_reference_consumption.schema.yaml`

- SHA256: `eb6dde5077a4712f77a992245afdee46159074398ede7fe3bba4001ef71d90f8`
- Bytes: `2206`

```yaml
$id: forprint_library.reference_consumption.library_reference_consumption_v0_3
title: ForPrint Library Reference Consumption Pilot v0.3
type: object
description: >
  Local schema for example downstream consumer payloads that consume
  Library-owned reference contract identifiers without redefining Library
  semantics or adding runtime ownership to Library.
required:
  - schema_version
  - pilot_id
  - owner_module
  - reference_contract_source
  - valid_consumer_payloads
  - invalid_consumer_payloads
properties:
  schema_version:
    type: string
    const: library_reference_consumption_examples_v0_3
  pilot_id:
    type: string
    const: library_reference_consumption_pilot_v0_3
  owner_module:
    type: string
    const: forprint_library
  description:
    type: string
  reference_contract_source:
    type: object
    required:
      - schema_version
      - path
    properties:
      schema_version:
        type: string
        const: library_reference_v0_2
      path:
        type: string
      note:
        type: string
  valid_consumer_payloads:
    type: array
  invalid_consumer_payloads:
    type: array
additionalProperties: false

consumer_payload_shape:
  required:
    - id
    - description
    - consumer_module
    - consumer_payload_id
    - library_owned_reference
    - consumer_owned_fields
    - foreign_module_references
    - boundary_assertions
  library_owned_reference_required:
    - schema_version
    - reference_type
    - reference_id
    - display_label
    - resolution_status
  allowed_consumer_modules:
    - calculator_engine
    - telegram_bot
    - forprint_operational_registry
    - forprint_accounting_registry_service
    - forprint_prepress_hub
    - forprint_integration_gateway
  forbidden_consumer_fields:
    - canonical_name_override
    - semantic_definition_override
    - library_alias_write
    - library_reference_write
    - final_price
    - price_formula
    - stock_mutation
    - material_write_off
    - order_creation
    - client_creation
    - payment_posting
    - production_runtime_write
    - telegram_runtime_behavior
    - calculator_runtime_integration
    - operational_registry_write
    - one_c_sync
    - one_c_import
```

### `schemas/reference_contract/library_reference.schema.yaml`

- SHA256: `06124b7a5d378a4068a5c7d0b41cb9dcd24c249c50a313bf5b8c46906f2165a9`
- Bytes: `1856`

```yaml
$id: forprint_library.reference_contract.library_reference_v0_2
title: ForPrint Library Reference Contract v0.2
type: object
description: >
  JSON-schema-like local schema for downstream references to Library-owned
  semantic/catalog entities.
required:
  - schema_version
  - reference_type
  - reference_id
  - display_label
  - resolution_status
  - source_module
properties:
  schema_version:
    type: string
    const: library_reference_v0_2
  reference_type:
    type: string
    enum:
      - product_service
      - material
      - operation
      - unit
      - template
      - technical_card
  reference_id:
    type:
      - string
      - "null"
    description: >
      Canonical Library reference id when known. Unknown references may keep
      this field null and preserve alias_input for review.
  display_label:
    type: string
  resolution_status:
    type: string
    enum:
      - library_reference_confirmed
      - library_reference_pending
      - ambiguous_manual_review_required
      - deprecated_reference
      - unknown
  source_module:
    type: string
    enum:
      - calculator_engine
      - forprint_operational_registry
      - forprint_integration_gateway
      - telegram_bot
      - future_forprint_crm
      - forprint_library
  alias_input:
    type:
      - string
      - "null"
  deprecation:
    type: object
    required:
      - is_deprecated
      - replaced_by
      - message
    properties:
      is_deprecated:
        type: boolean
      replaced_by:
        type:
          - string
          - "null"
      message:
        type:
          - string
          - "null"
  manual_review:
    type: object
    required:
      - required
      - reason
    properties:
      required:
        type: boolean
      reason:
        type:
          - string
          - "null"
additionalProperties: false
```

### `schemas/shared_operational_dictionary.schema.yaml`

- SHA256: `385e35f4b33d6e41ad6452ccc23e3d7db8ca9b9afa805614b571b049d354d02b`
- Bytes: `4238`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Shared Operational Dictionary
type: object
required:
- metadata
- dictionary_groups
properties:
  metadata:
    type: object
    required:
    - id
    - version
    - dictionary_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        const: '0.1'
      dictionary_status:
        const: draft_shared_operational_dictionary_v0_1
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      unit_dictionary_status:
        const: not_final_inventory_unit_system
    additionalProperties: true
  dictionary_groups:
    type: object
    required:
    - source_system
    - entity_type
    - order_status
    - order_line_status
    - payment_status
    - production_status
    - workflow_status
    - workflow_stage_status
    - material_requirement_status
    - reference_resolution_status
    - product_service_reference_status
    - contractor_reference_status
    - deadline_type
    - alert_rule_type
    - alert_severity
    - alert_event_status
    - notification_status
    - unit
    properties:
      source_system:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      entity_type:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      order_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      order_line_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      payment_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      production_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      workflow_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      workflow_stage_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      material_requirement_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      reference_resolution_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      product_service_reference_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      contractor_reference_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      deadline_type:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      alert_rule_type:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      alert_severity:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      alert_event_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      notification_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      unit:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
    additionalProperties: false
additionalProperties: false
$defs:
  dictionary_entry:
    $schema: https://json-schema.org/draft/2020-12/schema
    title: ForPrint Dictionary Entry
    type: object
    required:
    - id
    - label_uk
    - label_en
    - description
    - status
    - aliases
    - owner_module
    - dictionary_group
    - version
    - notes
    properties:
      id:
        type: string
        pattern: ^[a-z0-9_]+$
      label_uk:
        type: string
        minLength: 1
      label_en:
        type: string
        minLength: 1
      description:
        type: string
        minLength: 1
      status:
        enum:
        - active
        - draft
        - deprecated
      aliases:
        type: array
        items:
          type: string
          minLength: 1
      owner_module:
        const: forprint_library
      dictionary_group:
        type: string
        minLength: 1
      version:
        const: '0.1'
      notes:
        type: string
    additionalProperties: true
```

### `scripts/calculator_input/validate_calculator_input_contract.py`

- SHA256: `2443f2342b9552f871b0ebb64ae51e9f04b1e82686d16493a922334ef335c8b0`
- Bytes: `4441`

```python
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app"))

from forprint_library.calculator_input import (  # noqa: E402
    CalculatorInputContractError,
    CalculatorInputErrorType,
    build_calculator_input,
)

FIXTURE_DIR = ROOT / "examples" / "calculator_input_contract"
SCHEMA_PATH = ROOT / "schemas" / "calculator_input" / "calculator_input_envelope.schema.yaml"

VALID_FIXTURES = {
    "minimal_valid_business_card": "minimal_valid_business_card.yaml",
    "business_card_with_finishing": "business_card_with_finishing.yaml",
    "business_card_with_artwork_source": "business_card_with_artwork_source.yaml",
}

INVALID_FIXTURES = {
    "invalid_missing_material": (
        "invalid_missing_material.yaml",
        CalculatorInputErrorType.MISSING_REQUIRED_PARAMETER,
    ),
    "invalid_print_mode_reference": (
        "invalid_print_mode_reference.yaml",
        CalculatorInputErrorType.INVALID_REFERENCE,
    ),
    "invalid_quantity": (
        "invalid_quantity.yaml",
        CalculatorInputErrorType.INVALID_CONFIGURATION,
    ),
}

FORBIDDEN_KEYS = {
    "amount",
    "calculator_formula",
    "coefficient",
    "cost",
    "currency",
    "discount",
    "final_price",
    "formula",
    "margin",
    "price",
    "price_formula",
    "quote_total",
    "subtotal",
    "tax",
    "total",
    "vendor_price",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be mapping: {path.relative_to(ROOT)}")
    return data


def iter_keys(value: object) -> list[str]:
    if isinstance(value, dict):
        keys = list(value)
        for nested in value.values():
            keys.extend(iter_keys(nested))
        return [str(key) for key in keys]

    if isinstance(value, list):
        keys: list[str] = []
        for item in value:
            keys.extend(iter_keys(item))
        return keys

    return []


def assert_no_forbidden_keys(data: dict[str, Any]) -> None:
    found = sorted(FORBIDDEN_KEYS.intersection(iter_keys(data)))
    if found:
        raise AssertionError(f"Forbidden monetary/pricing keys found: {found}")


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)
    assert schema["title"] == "ForPrint Library Calculator Input Envelope"
    assert schema["properties"]["schema_version"]["const"] == "calculator_input_envelope_v0_1"
    assert schema["properties"]["product_id"]["const"] == "product.business_card"


def validate_valid_fixture(case_id: str, filename: str) -> None:
    fixture = load_yaml(FIXTURE_DIR / filename)
    assert fixture["schema_version"] == "calculator_input_fixture_v0_1"
    assert fixture["case_id"] == case_id
    assert fixture["product_id"] == "product.business_card"

    output = build_calculator_input(
        "product.business_card",
        fixture["input_configuration"],
    ).to_dict()

    assert output == fixture["expected_output"]
    assert_no_forbidden_keys(output)


def validate_invalid_fixture(
    case_id: str,
    filename: str,
    error_type: CalculatorInputErrorType,
) -> None:
    fixture = load_yaml(FIXTURE_DIR / filename)
    assert fixture["schema_version"] == "calculator_input_error_fixture_v0_1"
    assert fixture["case_id"] == case_id
    assert fixture["product_id"] == "product.business_card"

    try:
        build_calculator_input("product.business_card", fixture["input_configuration"])
    except CalculatorInputContractError as exc:
        error = exc.to_public_error()
    else:
        raise AssertionError(f"{case_id}: expected CalculatorInputContractError")

    assert error["error_type"] == error_type.value
    assert error == fixture["expected_error"]
    assert_no_forbidden_keys(error)


def main() -> int:
    validate_schema_file()

    for case_id, filename in VALID_FIXTURES.items():
        validate_valid_fixture(case_id, filename)

    for case_id, (filename, error_type) in INVALID_FIXTURES.items():
        validate_invalid_fixture(case_id, filename, error_type)

    print("OK: Library Calculator input contract validates")
    print(f"Fixtures: {FIXTURE_DIR.relative_to(ROOT)}")
    print(f"Schema: {SCHEMA_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `scripts/export_catalog_schema_artifacts.py`

- SHA256: `4375b2bf7dd82e1d386bac858c3d21f5f28526bbad3193dd883b9f54cb23c0d5`
- Bytes: `6534`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"
SEED_PATH = ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"

COMPONENT_SCHEMAS: dict[str, tuple[str, str]] = {
    "material.schema.yaml": ("ForPrint Material Catalog", "materials"),
    "product_family.schema.yaml": ("ForPrint Product Family Catalog", "product_families"),
    "operation.schema.yaml": ("ForPrint Operation Catalog", "operations"),
    "print_mode.schema.yaml": ("ForPrint Print Mode Catalog", "print_modes"),
    "finishing_option.schema.yaml": (
        "ForPrint Finishing Option Catalog",
        "finishing_options",
    ),
}


def catalog_item_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "id",
            "name_uk",
            "name_en",
            "aliases",
            "status",
            "version",
            "owner_module",
            "schema_status",
            "notes",
        ],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
            "name_uk": {"type": "string", "minLength": 1},
            "name_en": {"type": "string", "minLength": 1},
            "aliases": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "status": {
                "enum": [
                    "draft",
                    "active",
                    "deprecated",
                    "experimental",
                ]
            },
            "version": {"type": "string"},
            "owner_module": {"const": "forprint_library"},
            "schema_status": {"const": "unstable_v0_1"},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }


def metadata_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "id",
            "version",
            "catalog_status",
            "schema_status",
            "usage",
            "contract_status",
            "owner_module",
        ],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "version": {"type": "string"},
            "catalog_status": {"const": "draft_canonical_seed"},
            "schema_status": {"const": "unstable_v0_1"},
            "usage": {"const": "allowed_for_projection_use"},
            "contract_status": {"const": "not_final_contract"},
            "owner_module": {"const": "forprint_library"},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }


def catalog_seed_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ForPrint Catalog Seed",
        "type": "object",
        "required": [
            "metadata",
            "materials",
            "product_families",
            "operations",
            "print_modes",
            "finishing_options",
        ],
        "properties": {
            "metadata": metadata_schema(),
            "materials": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "product_families": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "operations": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "print_modes": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "finishing_options": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
        },
        "additionalProperties": False,
        "$defs": {"catalog_item": catalog_item_schema()},
    }


def component_catalog_schema(title: str, catalog_type: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "required": [
            "catalog_type",
            "metadata",
            "items",
        ],
        "properties": {
            "catalog_type": {"const": catalog_type},
            "metadata": metadata_schema(),
            "items": {
                "type": "array",
                "minItems": 1,
                "items": catalog_item_schema(),
            },
        },
        "additionalProperties": False,
    }


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"OK: wrote {path.relative_to(ROOT)}")


def read_seed() -> dict[str, Any]:
    data = yaml.safe_load(SEED_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Catalog seed must be a YAML mapping.")
    return data


def export_schemas() -> None:
    write_yaml(
        SCHEMAS_DIR / "catalog_seed.schema.yaml",
        catalog_seed_schema(),
    )

    for filename, schema_config in COMPONENT_SCHEMAS.items():
        title, catalog_type = schema_config
        write_yaml(
            SCHEMAS_DIR / filename,
            component_catalog_schema(title, catalog_type),
        )


def export_example_seed() -> None:
    seed = read_seed()
    example = {
        "metadata": {
            **seed["metadata"],
            "id": "canonical_catalog_seed_v0_1_example",
            "name": "Canonical Catalog Seed v0.1 Example",
            "notes": "Example projection-safe catalog seed structure.",
        },
        "materials": [seed["materials"][0]],
        "product_families": [seed["product_families"][0]],
        "operations": [seed["operations"][0]],
        "print_modes": [seed["print_modes"][0]],
        "finishing_options": [seed["finishing_options"][0]],
    }

    write_yaml(
        EXAMPLES_DIR / "catalog_seed_v0_1.example.yaml",
        example,
    )


def main() -> int:
    export_schemas()
    export_example_seed()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `scripts/export_component_catalogs.py`

- SHA256: `c718d6af6d580148138e42c354ee2143bf7c3b8eeb9de3b452dc109880408b65`
- Bytes: `1402`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"

SECTIONS: dict[str, str] = {
    "materials": "materials.yaml",
    "product_families": "product_families.yaml",
    "operations": "operations.yaml",
    "print_modes": "print_modes.yaml",
    "finishing_options": "finishing_options.yaml",
}


def read_seed() -> dict[str, Any]:
    data = yaml.safe_load(SEED_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Catalog seed must be a YAML mapping.")
    return data


def main() -> int:
    seed = read_seed()
    metadata = seed["metadata"]

    for section, filename in SECTIONS.items():
        items = seed.get(section)
        if not isinstance(items, list):
            raise ValueError(f"Seed section must be a list: {section}")

        payload = {
            "catalog_type": section,
            "metadata": metadata,
            "items": items,
        }

        target_path = ROOT / "catalog" / filename
        target_path.write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(f"OK: wrote {target_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `scripts/export_dictionary_policy_docs.py`

- SHA256: `53a87594cc61cf44667c22a5fe0795c1ef3bd70d9a4aa4f980b2e1fbdd8bd93f`
- Bytes: `6885`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs" / "architecture"

DOCS: dict[str, str] = {
    "shared_operational_dictionary_policy.md": """# Shared Operational Dictionary Policy

## Status

Draft policy for Shared Operational Dictionary v0.1.

## Purpose

Library owns canonical shared operational dictionary definitions.
ForPrint Library owns canonical shared operational 
dictionary definitions for the ForPrint ecosystem.

These dictionaries define stable operational IDs, labels, descriptions, 
aliases, statuses and versioning rules for concepts reused by 
Operational Registry, Calculator Engine, 
Accounting Registry, Telegram Bot, CRM, Gateway, Prepress Hub, 
Warehouse, Logistics, Website and future Mobile App.

## Core rule

Library defines canonical dictionary values.

Other modules may consume these values, reference them, display 
their labels and create temporary local projections, 
but they must not become independent permanent dictionary authorities.

## Boundary

This dictionary layer does not create real operational orders, real clients, real payments, 
real material stock, real warehouse records, Calculator formulas, 
Telegram runtime, CRM dashboard or 1C synchronization.

Operational Registry owns operational facts and records.

Library owns canonical operational language and semantic references.
""",
    "status_dictionary_policy.md": """# Status Dictionary Policy

## Status

Draft policy for shared status dictionaries.

## Purpose

Shared status dictionaries prevent modules from inventing 
conflicting values for the same operational state.

Examples include order_status, order_line_status, payment_status, 
production_status, workflow_status, workflow_stage_status, 
material_requirement_status, alert_event_status and notification_status.

## Stable IDs

Status IDs are stable machine values.

Labels may change, but IDs should remain stable unless a migration or deprecation rule is created.

## Consumption

Operational Registry should later reference these canonical values for operational records.

Calculator Engine should use these values when producing output packages.

Telegram Bot and CRM should display labels and must not invent internal status IDs.

Accounting Registry may map accounting statuses carefully 
without becoming the source of operational truth.

## Deprecated values

Deprecated values remain readable for historical records and migrations.
""",
    "source_system_dictionary_policy.md": """# Source System Dictionary Policy

## Status

Draft policy for the source_system dictionary.

## Purpose

source_system defines canonical IDs for systems, 
modules and external sources that produce or reference data in the ForPrint ecosystem.

Examples include forprint_operational_registry, forprint_library, calculator_engine, 
accounting_registry_service, telegram_bot, forprint_crm, 
forprint_integration_gateway, one_c_bas, manual_entry and unknown.

## Rule

Modules should store canonical source_system IDs when recording provenance, 
imports, projections or references.

Aliases may help import and display, but canonical IDs remain the stable internal truth.
""",
    "entity_type_dictionary_policy.md": """# Entity Type Dictionary Policy

## Status

Draft policy for the entity_type dictionary.

## Purpose

entity_type defines canonical IDs for shared business and operational concepts.

Examples include client_account, client_group, order, order_line, 
product_service_reference, material_requirement, payment_projection, 
workflow_stage, deadline_control, contractor_reference, alert_event and report_projection.

## Rule

Modules should reference canonical entity_type IDs in logs, alerts, reports, projections, 
integration messages and resolution records.

Entity type IDs do not mean Library owns the records. 
Operational records remain owned by their responsible modules.
""",
    "unit_dictionary_policy.md": """# Unit Dictionary Policy

## Status

Draft policy for the shared unit dictionary.

## Scope

The current unit dictionary is intentionally small and draft.

It includes values such as pcs, set, m, m2, kg, g, l, ml, hour, minute, service and unknown.

## Important limitation

This is marked as:

```yaml
dictionary_status: draft_shared_operational_dictionary_v0_1
unit_dictionary_status: not_final_inventory_unit_system

It is not a final inventory, warehouse or accounting unit system.

Future Warehouse, Accounting Registry and Library work may refine units, 
conversions and inventory-specific rules.
""",
"dictionary_consumption_policy.md": """# Dictionary Consumption Policy

Status

Draft policy for consuming Library dictionaries.

General rule

Dependent modules may consume Library dictionaries as projection input and validation references.

They should reference canonical IDs and display labels, 
not invent new internal IDs for shared operational concepts.

Operational Registry

Operational Registry should later reference these canonical values for statuses, 
entity types, source systems, alerts, deadlines and reference resolution states.

Calculator Engine

Calculator Engine should use these values when producing structured output packages, 
especially for source_system, entity_type, 
reference_resolution_status and product_service_reference_status.

Accounting Registry

Accounting Registry may map accounting statuses carefully, 
but it must not become the source of operational truth.

Telegram Bot and CRM

Telegram Bot and CRM should display labels and route ambiguous or 
unknown values for review instead of inventing canonical IDs.

Deprecated values

Deprecated dictionary values remain readable for historical records.
""",
"dictionary_versioning_policy.md": """# Dictionary Versioning Policy

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
""",
}

def main() -> int:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, content in DOCS.items():
        path = DOCS_DIR / filename
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        print(f"OK: wrote {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `scripts/export_shared_operational_dictionaries.py`

- SHA256: `1452c1e03b008d503db3bcf3aae322b8e546e93cfb455e73c91e315a31cf0f6e`
- Bytes: `14278`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DICTIONARIES_DIR = ROOT / "dictionaries"
SCHEMAS_DIR = ROOT / "schemas"

OWNER_MODULE = "forprint_library"
VERSION = "0.1"

DICTIONARY_VALUES: dict[str, list[str]] = {
    "source_system": [
        "forprint_operational_registry",
        "forprint_library",
        "calculator_engine",
        "accounting_registry_service",
        "telegram_bot",
        "forprint_crm",
        "forprint_integration_gateway",
        "forprint_prepress_hub",
        "warehouse_service",
        "logistics_service",
        "website",
        "mobile_app",
        "one_c_bas",
        "sanitized_demo",
        "manual_entry",
        "unknown",
    ],
    "entity_type": [
        "client_account",
        "client_group",
        "contact_person",
        "contact_method",
        "client_address",
        "legal_entity_profile",
        "external_reference",
        "order",
        "order_line",
        "calculator_output_package",
        "product_service_reference",
        "material_requirement",
        "payment_projection",
        "workflow_template",
        "workflow_stage",
        "deadline_control",
        "contractor_reference",
        "alert_rule",
        "alert_event",
        "report_definition",
        "report_projection",
        "operational_event",
        "unknown",
    ],
    "order_status": [
        "draft",
        "needs_review",
        "confirmed",
        "in_progress",
        "completed",
        "cancelled",
        "blocked",
        "manual_review_required",
        "archived",
        "unknown",
    ],
    "order_line_status": [
        "draft",
        "pending_reference_resolution",
        "ready",
        "in_progress",
        "completed",
        "cancelled",
        "manual_review_required",
        "unknown",
    ],
    "payment_status": [
        "not_invoiced",
        "invoice_reference_pending",
        "unpaid",
        "partially_paid",
        "paid_reference_confirmed",
        "overdue",
        "cancelled",
        "unknown",
    ],
    "production_status": [
        "not_started",
        "ready",
        "in_progress",
        "waiting_external_contractor",
        "blocked",
        "completed",
        "cancelled",
        "unknown",
    ],
    "workflow_status": [
        "not_started",
        "active",
        "blocked",
        "completed",
        "cancelled",
        "manual_review_required",
        "unknown",
    ],
    "workflow_stage_status": [
        "not_started",
        "ready",
        "in_progress",
        "blocked",
        "waiting_external_contractor",
        "completed",
        "cancelled",
        "late",
        "manual_review_required",
        "unknown",
    ],
    "material_requirement_status": [
        "planned",
        "library_reference_pending",
        "warehouse_reference_pending",
        "reserved_reference_pending",
        "confirmed",
        "fulfilled",
        "cancelled",
        "unknown",
    ],
    "reference_resolution_status": [
        "draft_display_only",
        "reference_pending",
        "reference_confirmed",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
    ],
    "product_service_reference_status": [
        "draft_display_only",
        "library_reference_pending",
        "library_reference_confirmed",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
    ],
    "contractor_reference_status": [
        "display_only",
        "client_account_reference_pending",
        "client_account_reference_confirmed",
        "external_reference_pending",
        "manual_review_required",
        "unknown",
    ],
    "deadline_type": [
        "order_due",
        "stage_due",
        "payment_due",
        "material_required_by",
        "manual_review_due",
        "unknown",
    ],
    "alert_rule_type": [
        "workflow_stage_late",
        "order_deadline_near",
        "payment_overdue",
        "material_requirement_unresolved",
        "manual_review_stale",
        "contractor_stage_blocked",
        "unknown",
    ],
    "alert_severity": [
        "info",
        "warning",
        "high",
        "critical",
        "unknown",
    ],
    "alert_event_status": [
        "open",
        "acknowledged",
        "resolved",
        "ignored",
        "failed_to_notify",
        "unknown",
    ],
    "notification_status": [
        "not_sent",
        "queued",
        "sent",
        "failed",
        "disabled",
        "unknown",
    ],
    "unit": [
        "pcs",
        "set",
        "m",
        "m2",
        "kg",
        "g",
        "l",
        "ml",
        "hour",
        "minute",
        "service",
        "unknown",
    ],
}

UK_LABEL_OVERRIDES: dict[str, str] = {
    "draft": "Чернетка",
    "needs_review": "Потребує перевірки",
    "confirmed": "Підтверджено",
    "in_progress": "У роботі",
    "completed": "Завершено",
    "cancelled": "Скасовано",
    "blocked": "Заблоковано",
    "manual_review_required": "Потрібна ручна перевірка",
    "archived": "Архівовано",
    "unknown": "Невідомо",
    "ready": "Готово",
    "active": "Активний",
    "late": "Прострочено",
    "not_started": "Не розпочато",
    "waiting_external_contractor": "Очікування зовнішнього підрядника",
    "unpaid": "Не оплачено",
    "partially_paid": "Частково оплачено",
    "paid_reference_confirmed": "Підтверджено оплату",
    "overdue": "Прострочено",
    "planned": "Заплановано",
    "fulfilled": "Виконано",
    "open": "Відкрито",
    "acknowledged": "Підтверджено оператором",
    "resolved": "Вирішено",
    "ignored": "Проігноровано",
    "failed": "Помилка",
    "disabled": "Вимкнено",
    "queued": "У черзі",
    "sent": "Надіслано",
    "not_sent": "Не надіслано",
    "info": "Інформаційно",
    "warning": "Попередження",
    "high": "Високий",
    "critical": "Критичний",
    "pcs": "Штуки",
    "set": "Комплект",
    "m": "Метри",
    "m2": "Квадратні метри",
    "kg": "Кілограми",
    "g": "Грами",
    "l": "Літри",
    "ml": "Мілілітри",
    "hour": "Година",
    "minute": "Хвилина",
    "service": "Послуга",
    "one_c_bas": "1C/BAS",
}

ALIASES: dict[str, list[str]] = {
    "forprint_operational_registry": ["operational_registry", "opr"],
    "forprint_library": ["library"],
    "calculator_engine": ["calculator"],
    "accounting_registry_service": ["accounting_registry"],
    "telegram_bot": ["telegram"],
    "one_c_bas": ["1c", "bas", "1c_bas"],
    "manual_entry": ["manual", "ручне введення"],
    "draft": ["чернетка"],
    "confirmed": ["підтверджено"],
    "in_progress": ["у роботі"],
    "completed": ["завершено"],
    "cancelled": ["скасовано"],
    "manual_review_required": ["manual_review", "ручна перевірка"],
    "unpaid": ["не оплачено"],
    "partially_paid": ["частково оплачено"],
    "overdue": ["прострочено"],
    "paid_reference_confirmed": ["paid", "оплачено"],
    "waiting_external_contractor": ["external_contractor_wait"],
    "late": ["прострочений етап"],
    "warehouse_reference_pending": ["warehouse_pending"],
    "warning": ["warn"],
    "critical": ["crit"],
    "pcs": ["piece", "pieces", "шт"],
    "m2": ["sqm", "square_meter", "м2"],
    "service": ["послуга"],
    "unknown": ["невідомо"],
}

DEPRECATED_VALUES: set[tuple[str, str]] = {
    ("reference_resolution_status", "deprecated_reference"),
    ("product_service_reference_status", "deprecated_reference"),
}

METADATA: dict[str, str] = {
    "id": "shared_operational_dictionary_v0_1",
    "name": "Shared Operational Dictionary v0.1",
    "version": VERSION,
    "dictionary_status": "draft_shared_operational_dictionary_v0_1",
    "schema_status": "unstable_v0_1",
    "usage": "allowed_for_projection_use",
    "contract_status": "not_final_contract",
    "owner_module": OWNER_MODULE,
    "unit_dictionary_status": "not_final_inventory_unit_system",
}


def title_from_id(value: str) -> str:
    return value.replace("_", " ").title()


def label_uk(value: str) -> str:
    return UK_LABEL_OVERRIDES.get(value, title_from_id(value))


def build_entry(group_name: str, value: str) -> dict[str, Any]:
    status = "deprecated" if (group_name, value) in DEPRECATED_VALUES else "active"

    return {
        "id": value,
        "label_uk": label_uk(value),
        "label_en": title_from_id(value),
        "description": (
            f"Canonical shared operational dictionary value '{value}' "
            f"for dictionary group '{group_name}'."
        ),
        "status": status,
        "aliases": ALIASES.get(value, []),
        "owner_module": OWNER_MODULE,
        "dictionary_group": group_name,
        "version": VERSION,
        "notes": "Draft shared operational dictionary entry.",
    }


def dictionary_entry_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ForPrint Dictionary Entry",
        "type": "object",
        "required": [
            "id",
            "label_uk",
            "label_en",
            "description",
            "status",
            "aliases",
            "owner_module",
            "dictionary_group",
            "version",
            "notes",
        ],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
            "label_uk": {"type": "string", "minLength": 1},
            "label_en": {"type": "string", "minLength": 1},
            "description": {"type": "string", "minLength": 1},
            "status": {"enum": ["active", "draft", "deprecated"]},
            "aliases": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "owner_module": {"const": OWNER_MODULE},
            "dictionary_group": {"type": "string", "minLength": 1},
            "version": {"const": VERSION},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }


def shared_dictionary_schema() -> dict[str, Any]:
    group_properties = {
        group_name: {
            "type": "array",
            "items": {"$ref": "#/$defs/dictionary_entry"},
        }
        for group_name in DICTIONARY_VALUES
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ForPrint Shared Operational Dictionary",
        "type": "object",
        "required": ["metadata", "dictionary_groups"],
        "properties": {
            "metadata": {
                "type": "object",
                "required": [
                    "id",
                    "version",
                    "dictionary_status",
                    "schema_status",
                    "usage",
                    "contract_status",
                    "owner_module",
                ],
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "version": {"const": VERSION},
                    "dictionary_status": {
                        "const": "draft_shared_operational_dictionary_v0_1"
                    },
                    "schema_status": {"const": "unstable_v0_1"},
                    "usage": {"const": "allowed_for_projection_use"},
                    "contract_status": {"const": "not_final_contract"},
                    "owner_module": {"const": OWNER_MODULE},
                    "unit_dictionary_status": {
                        "const": "not_final_inventory_unit_system"
                    },
                },
                "additionalProperties": True,
            },
            "dictionary_groups": {
                "type": "object",
                "required": list(DICTIONARY_VALUES),
                "properties": group_properties,
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
        "$defs": {"dictionary_entry": dictionary_entry_schema()},
    }


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"OK: wrote {path.relative_to(ROOT)}")


def export_shared_dictionary() -> dict[str, Any]:
    dictionary_groups = {
        group_name: [build_entry(group_name, value) for value in values]
        for group_name, values in DICTIONARY_VALUES.items()
    }

    shared_dictionary = {
        "metadata": METADATA,
        "dictionary_groups": dictionary_groups,
    }

    write_yaml(
        DICTIONARIES_DIR / "shared_operational_dictionary_v0_1.yaml",
        shared_dictionary,
    )

    return shared_dictionary


def export_group_dictionaries(shared_dictionary: dict[str, Any]) -> None:
    for group_name, entries in shared_dictionary["dictionary_groups"].items():
        payload = {
            "dictionary_group": group_name,
            "metadata": METADATA,
            "entries": entries,
        }
        write_yaml(DICTIONARIES_DIR / f"{group_name}.yaml", payload)


def export_schemas() -> None:
    write_yaml(SCHEMAS_DIR / "dictionary_entry.schema.yaml", dictionary_entry_schema())
    write_yaml(
        SCHEMAS_DIR / "shared_operational_dictionary.schema.yaml",
        shared_dictionary_schema(),
    )


def main() -> int:
    shared_dictionary = export_shared_dictionary()
    export_group_dictionaries(shared_dictionary)
    export_schemas()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

---

# C. Blueprint authority context

### `forprint_system_blueprint/coordination/module_policy/forprint_library/module_policy.md`

- SHA256: `60010ad1b6ae83a18ee0828139708a4523d01c67a424143b7c427b70c3c5414c`
- Bytes: `1848`

```markdown
# Module Policy — ForPrint Library

## Module ID

```text
forprint_library
```

## Priority

```text
p1
```

## Development status

```text
active_development
```

## Strategic role

Canonical semantic, catalog, naming, alias and contract-definition authority for products, services, materials, operations and templates.

## Main goals

- `Own canonical product/service/material/operation IDs.`
- `Maintain aliases and naming rules.`
- `Provide semantic resolution for module ambiguity.`
- `Keep contract definitions and catalog semantics versioned.`
- `Publish the versioned shared ForPrint UI design-system package and reusable component catalog.`
- `Expose searchable semantic and reusable-capability references before modules create competing implementations.`

## Owns

- `product_catalog_semantics`
- `service_catalog_semantics`
- `material_catalog_semantics`
- `operation_catalog_semantics`
- `aliases`
- `templates`
- `technical_cards`
- `contract_definitions`
- `ui_design_system_publication`
- `shared_ui_component_catalog`
- `ui_component_version_and_adoption_metadata`

## Must not own

- `operational_orders`
- `client_database`
- `accounting_truth`
- `production_runtime`
- `crm_workflow`
- `domain_business_rules_outside_library_semantics`

## Next focus

- `Canonical Product/Service ID and Alias Governance.`
- `Define ambiguity routing and approval lifecycle.`
- `Prepare contract registry direction.`
- `Publish the first versioned shared UI component/catalog surface.`
- `Strengthen reusable semantic/capability discoverability without absorbing domain ownership.`

## Adoption rule

This module policy is strategic guidance. It does not automatically authorize large refactors or broad rewrites. The module should compare this policy with its current implementation and report alignment, conflicts or questions to Blueprint.
```

### `forprint_system_blueprint/coordination/human_intent/modules/forprint_library.yaml`

- SHA256: `920d0f2d76b0d4af1667aef8514fc9c790c875ff8e6bfb8c045686be60eaf248`
- Bytes: `7366`

```yaml
schema_version: forprint_module_human_intent_ledger_v0_1
module_id: forprint_library
display_name: ForPrint Library
authority: planning_context_not_release_authority
status: active_planning_context
append_only: true
intents:
  - status: RECOVERED
    text: Library володіє stable canonical IDs і versioned schemas для products/materials/services/operations.
    context: Price/accounting/operational state від цього відділений.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-001
  - status: RECOVERED
    text: Aliases, supplier part numbers, alternate names, normalization rules і provenance/confidence мають бути
      частиною semantic layer.
    context: Це дозволяє безпечно мапити зовнішні джерела.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-002
  - status: RECOVERED
    text: External catalog ingestion повинен зберігати source/provider/fetched-at/key/hash/raw snapshot refs і давати
      human review для ambiguous merge.
    context: Не переписувати canonical truth без підтвердження.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-003
  - status: AGREED
    text: Library є canonical owner calibration profiles для фізичних вимірювань Operations Assistant, включно з
      параметрами товщини/ваги/толерансів.
    context: Сам Assistant лише використовує профіль.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-004
  - status: RECOVERED
    text: Library -> Calculator reference input має бути deterministic, typed, versioned і read-only.
    context: Pricing formulas залишаються в Calculator.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-005
  - status: AGREED
    text: Library повинна зберігати SOP/instruction/media knowledge для contextual work guidance.
    context: Operations Assistant показує потрібну інструкцію з контексту.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-006
  - status: RECOVERED
    text: Canonical ForPrint Design System owner закріплений за Library; Website та інші UI мають мігрувати до нього
      без page-local систем.
    context: Це вже було окремо додано в Blueprint.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-007
  - status: AGREED
    text: Reference photos/product media можуть індексуватися Semantic Retrieval, але Library лишається owner canonical
      assets/metadata.
    context: Пошуковий індекс — projection.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-008
  - intent_id: HI-FP-LIBRARY-009
    status: AGREED
    text: Library owns canonical aliases, common misspellings, short production tokens, naming profiles and profile-specific
      defaults for materials/operations/device capabilities.
    context: Calculator consumes these definitions instead of maintaining a private vocabulary.
    roadmap: LIB-FILE-01
  - intent_id: HI-FP-LIBRARY-010
    status: AGREED
    text: A short human filename may omit common information only when the active naming profile defines the default
      unambiguously.
    context: 'Example: Ricoh lamMat represents the agreed default thin matte roll lamination.'
    roadmap: LIB-FILE-02
  - intent_id: HI-FP-LIBRARY-011
    status: AGREED
    text: The same short token may have different meaning across equipment/production profiles, so structured profile/capability
      context must remain explicit.
    context: Do not globally interpret a token without its naming/production profile.
    roadmap: LIB-FILE-03
  - intent_id: HI-FP-LIBRARY-012
    status: AGREED
    text: Library semantic changes that affect inter-module payloads must flow through a versioned Contract Registry/adoption
      process rather than being changed locally in one consumer.
    context: Avoid modules drifting onto different meanings of the same field/token.
    roadmap: LIB-FILE-04
  - intent_id: HI-FP-LIBRARY-013
    status: AGREED
    text: Library should eventually provide standardized visual/SOP instructions for Job Ticket and Operations Assistant
      steps, with manager-provided notes/images as fallback when no standard exists.
    context: Human guidance is a Library knowledge responsibility; execution truth remains OCR.
    roadmap: LIB-FILE-05
  - intent_id: HI-FP-LIBRARY-014
    status: AGREED
    text: Library is publication owner for shared ForPrint UI tokens, themes, reusable components, component catalog,
      versions and adoption metadata.
    context: Blueprint governs; consumers compose; Inspector validates.
    roadmap: LIB-UI-01
  - intent_id: HI-FP-LIBRARY-015
    status: AGREED
    text: Shared indexes should help modules discover reusable technical primitives and semantic definitions before
      creating competing implementations.
    context: Domain business rules still belong to domain owners.
    roadmap: LIB-INDEX-01
  - intent_id: HI-LIBRARY-U131-20260906-001
    status: AGREED
    text: ForPrint Library is the shared semantic and contract reference authority; modules should consult its existing
      canonical/recommended semantics before creating significant competing shared implementations.
    context: This extends the Library role already present in module policy; it does not move domain business ownership
      into Library.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-U131-20260906-002
    status: AGREED
    text: A first registered semantic ID may remain stable while maturity, recommended implementation names, aliases
      and contract versions evolve.
    context: Registration does not automatically mean CANONICAL.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-U131-20260906-003
    status: AGREED
    text: Semantic registration should prioritize module-public, cross-module, external-boundary, high-criticality
      and widely reused surfaces rather than every local helper.
    context: Interaction scope and criticality are independent signals for standardization review.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-U131-20260906-004
    status: AGREED
    text: Library should batch unresolved semantic registration/enrichment proposals and publish versioned semantic
      changes; Blueprint remains responsible for rollout timing and adoption mode across affected modules.
    context: Adoption may be informational, new-code-only, migrate-on-touch, roadmap-required or migration-required.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-ARCH-20260919-001
    status: RECOVERED
    text: Historical/reference asset indexing should use stable asset and revision semantics with provenance; an index/search
      result is a projection and must not become canonical asset, order or production truth.
    context: Recovered from the 2026-09-19 historical asset indexing discussion.
    roadmap: ''
    source_refs:
    - coordination/internal_work/blueprint/evening_reviews/2026-09-19/forprint_evening_architecture_handoff_20260919_v0_1/00_README.md
    - coordination/internal_work/blueprint/evening_reviews/2026-09-19/forprint_evening_architecture_handoff_20260919_v0_1/10_portfolio_reconciliation_20260921_v0_1.yaml
```

### `forprint_system_blueprint/coordination/global_policy/forprint_project_doctrine.md`

- SHA256: `204ffe57264b7a188bff86a09088766a788c67adc02695e38ccce46086c6be58`
- Bytes: `9182`

```markdown
# ForPrint Project Doctrine

## Status

Active global policy

## Core idea

ForPrint is an operational platform for advertising and informational products.

The system must support:

```text
customer intake;
calculation;
structured order formalization;
internal operational registry;
accounting and 1C synchronization;
prepress preparation;
production support;
reporting and analytics;
multi-channel customer communication.
```

ForPrint is not only a print shop tool.

It should be built as an extensible operational platform for advertising/informational products and related services.

Main strategic goal

The goal is to build a coordinated ecosystem where modules work through clear boundaries and shared contracts.

The system must reduce manual duplicate work, especially:

manual order re-entry;
manual 1C data entry;
manual customer history search;
manual repeated report building;
manual cross-module status tracking.
Current governance

Current governance is:

owner / mentor
+
architectural assistant
+
ForPrint System Blueprint

ForPrint Control Plane is planned but deferred.

Control Plane must not be actively implemented until core modules are alive and interconnected.

Core module roles
ForPrint System Blueprint

Owns architecture, module boundaries, execution queue, coordination standards and global project alignment.

Operations Control Registry

Canonical owner of ForPrint operational control state and operational write boundaries.

It coordinates order state, obligations, reservations/shortages, incidents, deadlines and cross-module execution context.
Persistent business data uses centrally managed persistence; the module does not own the physical storage topology for every domain.

Compatibility note: the current technical identifier `forprint_operations_control_registry`, existing repository path/name,
contract IDs and released prompt IDs/paths remain legacy compatibility identifiers until a separately approved technical migration.
The canonical display/working identity is **Operations Control Registry**.

Library

Canonical semantic/catalog authority.

It owns canonical product/service/material/operation IDs, names, aliases, catalog definitions and semantic registry.

Calculator Engine

Primary formalization point for new order/calculation requests.

It produces structured machine-readable calculation and order draft packages.

Accounting Registry

Accounting and 1C synchronization boundary.

It owns 1C import/export, mapping, staging, reconciliation and accounting workflow adapters.

Telegram Bot / Website / Mobile App

Customer channel adapters.

They must not become business truth owners.

Integration Gateway

Future runtime validation, routing, idempotency and correlation layer.

Gateway remains limited until real runtime handoff is needed.

CRM

Future human dashboard, reporting and workflow coordination layer.

CRM must not become the physical database owner.

Core development principles
1. One ecosystem, many modules

Modules must move in one coordinated direction.

A module should not optimize itself in a way that breaks the overall ecosystem.

2. Stable IDs over names

Names can change.

Stable IDs must be used for canonical references:

ClientAccount ID;
product_id;
service_id;
material_id;
operation_id;
order_id;
request_id;
quote_id.
3. Phone is lookup, not truth

Phone number is a strong lookup/contact key.

Canonical customer identity is ClientAccount ID.

4. Calculator-first order formalization

New orders should primarily pass through Calculator Engine.

Manual and legacy paths are fallback only.

5. Operations Control Registry owns operational state, not storage topology

ForPrint persistent business data belongs in centrally managed persistence with explicit domain write boundaries.

Operations Control Registry owns the operational model, operational state transitions and authorized writes for its domain.
It must not become a hidden private database for every module or a substitute for Library, CRM, Accounting, Warehouse or Identity ownership.

6. Library controls semantics

Modules must not invent permanent product/service/material names independently.

Ambiguity must go to Library.

7. 1C-aware, not 1C-dependent

ForPrint DB must be 1C-aware and sync-friendly.

1C remains important, but it is not the global ForPrint source of truth.

8. Configuration over hardcoding

No important paths, thresholds, repository locations or timing rules should be hardcoded in business logic.

Use config files.

9. Reports and checkups are part of development

Each module must publish coordination status, reports and open questions.

10. Manual override must be visible

Manager/manual adjustments are allowed where needed, but they must be logged and later analyzed.

11. Development-first governance

ForPrint is a young, actively evolving system. Existing policy, protocol,
document or workflow is not authoritative merely because it is older.

When an existing rule blocks a materially better current design, first decide
whether that rule still has an active consumer, migration value or explicit
governance reason. If it does not, evolve the authority deliberately: update
the current document when the concern is continuous, or create the next clear
revision and mark the previous authority deprecated/superseded when semantics
materially change.

Backward compatibility is not a project goal by itself. Architecture must not
be distorted solely to preserve obsolete assumptions.

12. Durable project memory and forward control

Significant completed implementation, architecture and governance decisions
must be recoverable from repository evidence. Chat history is not canonical
project memory.

Roadmaps define intended project movement. Prompt sequencing defines executable
coordination steps. Current work must stay reconciled with both so modules move
at a balanced pace and dependent work is not advanced prematurely.

Current strategic direction

Near-term project direction:

1. Stabilize Blueprint coordination.
2. Apply module coordination standard.
3. Use Calculator as first active module in the full coordination loop.
4. Move Calculator toward CalculationOutputPackage / Quote / OrderDraft.
5. Expand Operations Control Registry operational-control model and centralized-persistence boundaries later.
6. Strengthen Library canonical catalog/semantic authority.
7. Keep Accounting Registry ready, but wait for sanitized 1C samples before deeper v0.6.

---

<!-- forprint-execution-workspace-compatibility-v0-1 -->
## Execution compatibility over global cleanliness

ForPrint development is expected to remain active while coordination work is queued and executed. Global repository cleanliness is therefore not a project goal by itself.

Execution must be judged from explicit authority, immutable contracts, required-input compatibility, and execution ownership. Unrelated Blueprint worktree changes do not invalidate a prompt. Material changes to required inputs do.

Shared module execution lanes remain attributable before CLAIM. Future parallelism in one module must use isolated execution workspaces rather than multiple agents writing into one dirty checkout.

No workflow may destroy, auto-stash, absorb, or silently reinterpret unrelated operator work merely to satisfy a historical "clean tree" assumption.

<!-- portfolio-operated-development-doctrine-v0-1:start -->
## Portfolio-operated development and roadmap continuity

ForPrint module development is governed as a portfolio, not as isolated repositories.

Blueprint must continuously maintain enough durable knowledge to recover:

- why a module exists;
- what it can/should do;
- what the current target finish is;
- what roadmap outcomes remain;
- what dependencies exist and when they become blocking;
- what evidence justifies progress.

Roadmaps remain living control artifacts until final project delivery.
A roadmap item whose design intent cannot be reconstructed is a governance defect.

Module executors consume Blueprint standards as read-only authority. They may request clarification or propose a
change, but they do not silently fork project-wide governance inside their own repositories.

Portfolio optimization balances time, budget, dependency criticality, business/project value, risk and executor
quality rather than maximizing one module's local velocity.
<!-- portfolio-operated-development-doctrine-v0-1:end -->

<!-- theory-knowledge-automation-principle-v0-1:start -->
## Maximum useful automation and manual-work reduction

ForPrint should systematically reduce avoidable manual work across business and development
operations.

Automation is valuable when it improves speed, consistency, recoverability or operator effort
without sacrificing correctness, auditability, safety, semantic ownership or meaningful human
control.

Every module should treat reduction of repetitive manual work as a standing design objective where
economically and operationally justified.

This principle does not authorize uncontrolled autonomy, security/destructive actions, automatic
business/module ACCEPT, or cross-repository mutation.
<!-- theory-knowledge-automation-principle-v0-1:end -->
```

### `forprint_system_blueprint/coordination/global_policy/ecosystem_module_map.md`

- SHA256: `a90c3d6ac4ab0af17af9c1ea83e1ebb595eb9333fcfcdd9f162c49aec85ab51c`
- Bytes: `3324`

```markdown
# ForPrint Ecosystem Module Map

## Status

Active global policy

## Purpose

This document gives all module assistants a shared high-level view of the ForPrint ecosystem.

It is not a full technical design.

It defines module roles and prevents modules from taking ownership of responsibilities that belong elsewhere.

## Core modules

| Module | Strategic role | Must not become |
|---|---|---|
| forprint_strategic_control_plane | Future strategic governance, priority control, ecosystem status aggregation and decision-support layer | Active runtime orchestrator before core modules are alive |
| forprint_system_blueprint | Architecture, boundaries, execution queue, coordination standards | Runtime service |
| forprint_operations_control_registry | Operations Control Registry: operational state/write-boundary authority (legacy technical ID retained) | Calculator, CRM, Library, Accounting, Warehouse, Logistics |
| forprint_library | Canonical semantic/catalog authority | Operational DB |
| calculator_engine | Calculation and order formalization engine | Order registry, CRM, accounting, warehouse |
| forprint_accounting_registry_service | Accounting/1C synchronization boundary | Operations Control Registry, CRM, Library |
| forprint_integration_gateway | Runtime transport/validation/routing layer | Business brain |
| forprint_contract_registry | Canonical inter-module interface contract catalog, ownership, version and compatibility authority | Runtime gateway, business-semantic owner or workflow orchestrator |
| telegram_bot | Customer channel adapter | Business truth owner |
| website | Customer channel adapter | Business truth owner |
| mobile_app | Future customer channel | Active module before Calculator maturity |
| forprint_crm | Human dashboard/workflow coordination | Physical DB owner |
| forprint_prepress_hub | Prepress/file preparation lifecycle | Calculator, accounting, order registry |
| warehouse_service | Future stock/material operations | Catalog semantic authority |
| logistics_service | Future delivery/logistics operations | CRM or order registry |
| cloud_backup_manager | Infrastructure backup utility | Business module |

## Primary future flow

```text
Customer / manager request
↓
Customer channel or internal UI
↓
CustomerRequest
↓
Calculator Engine
↓
CalculationOutputPackage / Quote / OrderDraft
↓
Operations Control Registry records operational state through the centrally managed persistence boundary
↓
Accounting Registry prepares accounting/1C sync
↓
Prepress / production / warehouse / logistics receive references and tasks
```
## Current first practical focus

The first practical module coordination loop is being tested with:

calculator_engine

The goal is to validate:

Blueprint instructions
↓
module self-check
↓
module coordination files
↓
Blueprint collector
↓
snapshot report

After the Calculator loop is stable, the same pattern can be applied to other modules.


---

## Strategic Control Plane

ForPrint Strategic Control Plane is planned as a future high-priority governance module.

Current status:

```text
planned_high_priority_deferred_until_core_modules_alive
```

It must not be actively implemented yet.

Current governance remains with the owner / mentor, architectural assistant and ForPrint System Blueprint.


---
```

### `forprint_system_blueprint/coordination/global_policy/current_execution_focus.md`

- SHA256: `909c49f4bc961a1bfb27676240cffc92bcd8c26049ae14a3caa767864fae5ac3`
- Bytes: `23851`

```markdown
# Current ForPrint Execution Focus

## Status

Active global policy

## Current priority model

## P0

### 1. System Blueprint coordination foundation

Keep System Blueprint as the current governance and coordination center.

Control Plane is planned but deferred.

### 2. Calculator Engine

Calculator Engine is the first module used to validate the full coordination loop.

Calculator remains a P0 module.

Current direction:

```text
CalculationOutputPackage;
Quote / CommercialOffer;
OrderDraft / OrderCreationDraft;
price_breakdown;
material_consumption_estimate;
production_method_plan;
accounting line drafts;
prepress requirements;
manual/custom operation drafts.
```
3. Module coordination loop

Each active module must eventually maintain:

coordination/status/current_status.yaml;
coordination/prompts/index.yaml;
coordination/reports/index.yaml;
completion reports;
questions for Blueprint.
P1
Operations Control Registry

Compatibility: current machine/repository identifier remains `forprint_operations_control_registry`
until a separately approved external-repository migration.

Next planned direction:

Core ForPrint Data Model Expansion

Expected future focus:

ClientAccount;
ClientGroup;
ContactPerson;
ContactMethod;
ChannelIdentity;
Relationship;
CustomerRequest lifecycle;
Order lifecycle;
1C-aware references;
logistics addresses;
manual decision records.
Library

Next planned direction:

Canonical Product/Service ID and Alias Governance

Expected future focus:

canonical IDs;
aliases;
semantic definition requests;
draft/review/approved lifecycle;
module ambiguity routing.
Telegram Bot

Next planned direction:

Channel-agnostic customer request and Calculator handoff

Telegram must remain a channel adapter.

Selective / waiting
Accounting Registry

Current status:

sandbox_1c_import_export_ready

Next deeper v0.6 requires real sanitized 1C export samples.

Do not proceed to live 1C write or production sync.

Hold / planned
Integration Gateway

Hold until real runtime handoff is needed.

Control Plane

Planned high priority, deferred until core modules are alive.

Legacy file parser

Low-priority fallback.

Future core workflow should come from Calculator-generated packages.


---

<!-- forprint-execution-workspace-compatibility-v0-1 -->
## v0.4.1 execution-workspace interpretation

Current B1 work uses the following interpretation:

- Blueprint global cleanliness is not a readiness condition by itself.
- Readiness is determined from release authority, prompt/contract binding, declared required inputs, compatibility classification, and preflight evidence.
- Unrelated Blueprint development may coexist with queued or active module work.
- The current shared module execution lane remains clean/attributable before CLAIM; a busy lane keeps later work queued.
- Stable execution identity after CLAIM prevents `HEAD` chasing.
- Future same-module parallel execution requires isolated execution workspaces; it is not authorized by simply relaxing the module dirty-worktree blocker.
- Tool-specific clean-worktree requirements may remain temporarily where a mutation tool has not yet implemented exact dirty-scope preservation; such a tooling constraint is not an ecosystem compatibility rule.

This clarification changes no B1 acceptance state and authorizes no autonomous execution by itself.

<!-- b1-logistics-reference-validation-current-focus-v0-1 -->
## v0.4.1 current B1 checkpoint — 2026-08-24

B1 implementation and Logistics reference validation are complete.

Current durable exit marker:

`B1_LOGISTICS_REFERENCE_VALIDATION_PASS`

The next legally eligible transition is explicit `B1-ACCEPT` review / seal /
publication.

This checkpoint does not ACCEPT or close B1, does not activate B2, does not
release a business prompt, and does not authorize autonomous execution.

<!-- b1-explicit-acceptance-current-focus-v0-1 -->
## v0.4.1 B1 acceptance checkpoint — 2026-08-24

Operator decision: `ACCEPT B1`.

B1 has passed implementation, Logistics reference validation and final
acceptance-readiness review.

This transaction creates the local B1 acceptance/seal. It does not activate B2.
After separate publication of the exact seal commit, the next transition is
`B2-ACTIVATE`.

<!-- b2-explicit-activation-current-focus-v0-1 -->
## v0.4.1 B2 current slice — 2026-08-24

Operator decision: `ACTIVATE B2`.

Current slice:

`blueprint_v0_4_1_coordination_data_classification_and_persistence_boundary_v0_1`

Current functional package: `B2-IMPLEMENT-ACCEPT`.

B2 is a persistence-boundary/design hardening slice only. Live SQLite runtime,
daemon/systemd execution and autonomous coordination remain disabled.

## B2 explicit acceptance checkpoint

Operator decision: `ACCEPT B2`.

B2 implementation commit:

`b0bf657677e1cde9e624fe81c85adf0dcba44d79`

Acceptance transaction state:

- B2 implementation: committed and published;
- B2 semantic review: PASS;
- B2 operator decision: ACCEPT;
- B2 local acceptance seal: recorded by this transaction;
- publication of this acceptance seal: separate explicit transaction;
- Q1 remains inactive until B2 acceptance seal is published;
- live SQLite runtime: disabled;
- daemon/systemd: disabled;
- autonomous execution: disabled;
- automatic ACCEPT: disabled.

Next after publication: `Q1 — Clarification question lifecycle`.

## Q1 explicit activation checkpoint

Operator direction: proceed to the Q-track.

Current v0.4.1 slice:

`blueprint_v0_4_1_clarification_question_lifecycle_v0_1`

Activation basis:

- B2 exit marker `B2_ACCEPTED_PUBLISHED_CLOSED` is satisfied and published at
  `c0b74c261b11f4c0e59d49fdd7bfc12d5be54788`;
- Q1 dependency on `B2-IMPLEMENT-ACCEPT` is satisfied;
- Q1 is the first legally eligible planned package;
- Q2-Q8 remain planned and inactive;
- WIP target remains one current functional package.

Q1 scope:

- first-class clarification question threads;
- lifecycle `OPEN -> ROUTED -> ANSWERED -> CONFIRMED -> RESOLVED`;
- alternative terminals `ESCALATED`, `CANCELLED`, `EXPIRED`;
- prompt may remain `in_progress` with `waiting_on_clarification`;
- minimum question identity and evidence correlation;
- a question alone never implies RETURN or HOLD.

This activation does not implement Q2 five-round escalation, Q3-Q8 semantics,
live SQLite runtime, daemon/systemd, autonomous execution, automatic ACCEPT,
automatic next activation, Telegram transport or cross-repository writes.

Current functional package: `Q1`.

Next completion gate: `Q1_ACCEPTED_PUBLISHED_CLOSED`.

## Q1 explicit acceptance checkpoint

Operator decision: `ACCEPT Q1`.

Q1 implementation commit:

`f0536f384c5524043e3a7a4cf4f6a8587e2eae6d`

Acceptance readiness was revalidated in this transaction before any write:

- exact Q1 implementation parent/subject/scope: PASS;
- exact Q1 contract/validator/test hashes: PASS;
- implementation published to the live remote: PASS;
- Q1 semantic validator: PASS;
- focused Q1 tests: PASS;
- standards index validation: PASS;
- canonical `make check`: PASS;
- Q2 remains inactive;
- live SQLite runtime / daemon / systemd / autonomy remain disabled.

Acceptance transaction state:

- Q1 operator decision: ACCEPT;
- Q1 local acceptance seal: recorded by this transaction;
- publication of this acceptance seal: separate explicit transaction;
- Q2 remains inactive until Q1 acceptance seal is published and Q2 is separately activated.

Next after publication: `Q2 — Bounded five-round clarification and escalation`.

## Q2 explicit activation checkpoint

Operator decision: `ACTIVATE Q2`.

Q1 exit marker `Q1_ACCEPTED_PUBLISHED_CLOSED` is satisfied and published at:

`516ee17fc5b678112dc28732166a3bd16691d8a0`

Current v0.4.1 slice:

`blueprint_v0_4_1_bounded_clarification_and_escalation_v0_1`

Current functional package: `Q2`.

Q2 scope is semantic hardening for bounded clarification:

- default `maximum_unresolved_round_trips_per_question_thread: 5`;
- the limit is per unresolved question thread, not per whole prompt;
- after round five, further autonomous dialogue for that thread stops;
- the thread becomes `ESCALATED`;
- a blocking prompt becomes visibly waiting/blocked, without silently becoming
  RETURN or HOLD;
- escalation evidence must preserve the original question, all rounds,
  evidence, unresolved fact, impact, safe options and recommended next action.

This activation defines the Q2 contract only. It does not enable a live
autonomous dialogue worker, SQLite runtime, daemon/systemd, Telegram transport,
automatic ACCEPT, automatic next activation, business prompt release, or
cross-repository writes.

Q3-Q8 remain planned and inactive.

Next completion gate: `Q2_ACCEPTED_PUBLISHED_CLOSED`.

<!-- phase-boundary-progression-gate-current-focus-v0-1 -->
## Phase-boundary progression gate — current authority

<!-- phase-boundary-progression-gate-policy-v0-1 -->
## Phase-boundary progression gate policy — 2026-08-24

The operator changed the progress-confirmation rule.

Manual progress confirmation is now required at **major phase boundaries**, not
between every small Blueprint-owned package inside the same approved phase.

For the current Q phase, Q1-Q8 are one phase. After a Q package satisfies its
declared deterministic acceptance/semantic gates, publication and activation of
the next eligible Q package do not require a new `ACCEPT Qn` or
`ACTIVATE Qn+1` confirmation.

This does not authorize automatic ACCEPT/RETURN/HOLD of module or business
prompts. It does not waive WIP=1, dependency checks, semantic review,
publication verification, or exception authority. RETURN/HOLD, waiver, scope
change, dependency override, security/credential, destructive/production and
other exceptional authority decisions remain manual.

Current non-autonomous execution remains explicit and user-run; no background
push is authorized.

The next required manual **progress** gate after the Q phase is the Q -> H10
phase transition.

<!-- portfolio-automation-foundation-current-focus-v0-1:start -->
## 2026-08-25 portfolio/automation foundation checkpoint

The published Q2 slice remains current:

`blueprint_v0_4_1_bounded_clarification_and_escalation_v0_1`

Development progression is intentionally paused for portfolio-foundation planning.
This checkpoint does not implement Q2, activate Q3, release a business prompt or enable broad module automation.

New cross-cutting planning foundation:

- module concept/roadmap traceability;
- end-to-end gray-zone review;
- portfolio dependency/prioritization;
- weighted progress/baseline measurement;
- module readiness/blocking classification;
- mandatory frontend design-system governance;
- bounded module-executor automation standards;
- provisional concepts/roadmaps for Operations Assistant, System Administration and Marketing Orchestrator.

Existing non-Blueprint module roadmaps remain useful evidence, but they are not sufficient post-Q automated
portfolio-selection authority until rebuilt under the new common roadmap model.

Resume target remains:

`Q2_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- portfolio-automation-foundation-current-focus-v0-1:end -->

<!-- q2-deterministic-closeout-q3-activation-v0-1:start -->
## Q2 deterministic closeout / Q3 activation — 2026-08-25

The temporary portfolio-foundation pause is finished for the Q-track.

Q2 implementation commit:

`ba5c83eab07a44cd65b72680d099f3a18d26f9b6`

Q2 result:

`Q2_ACCEPTED_PUBLISHED_CLOSED`

Acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_execution_blocker_taxonomy_v0_1`

Current functional package:

`Q3`

Q3 scope is blocker taxonomy and prompt blocking semantics. It must keep
`clarification_required`, `execution_blocked`, `unable_to_execute`, `RETURN` and `HOLD`
semantically distinct. `unable_to_execute` is module evidence for governance review, not an
automatic Blueprint RETURN.

Q4-Q8 remain planned/inactive.

Live SQLite runtime, daemon/systemd, Telegram transport, autonomous worker execution,
automatic module/business ACCEPT, automatic RETURN/HOLD, business prompt release and
cross-repository writes remain disabled.

Next:

`Q3_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- q2-deterministic-closeout-q3-activation-v0-1:end -->

<!-- q3-deterministic-closeout-q4-activation-v0-1:start -->
## Q3 deterministic closeout / Q4 activation — 2026-08-25

Q3 implementation commit:

`7993f873f2f8aba31b9ee2c52fd6f2d3799391be`

Q3 result:

`Q3_ACCEPTED_PUBLISHED_CLOSED`

Acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_immutable_prompt_adjustment_and_decision_v0_1`

Current functional package:

`Q4`

Q4 scope is immutable prompt adjustment / operator decision / correlation semantics.
Released prompts remain immutable; any governed adjustment must be represented by a separate,
traceable decision/adjustment artifact rather than silently editing released prompt history.

Q5-Q8 remain planned/inactive.

Live SQLite runtime, daemon/systemd, Telegram transport, autonomous worker execution,
automatic module/business ACCEPT, automatic RETURN/HOLD, business prompt release and
cross-repository writes remain disabled.

Next:

`Q4_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- q3-deterministic-closeout-q4-activation-v0-1:end -->

<!-- q4-deterministic-closeout-q5-activation-v0-1:start -->
## Q4 deterministic closeout / Q5 activation — 2026-08-25

Q4 implementation commit:

`711d22224e84fe280ab6ce8f0516a853436f207d`

Q4 result:

`Q4_ACCEPTED_PUBLISHED_CLOSED`

Acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_common_coordination_event_envelope_v0_1`

Current functional package:

`Q5`

Q5 scope is the common coordination event envelope contract. It must define one immutable event
shape before any daemon/runtime is built, while keeping event observations separate from projected
state and preserving correlation/causation/idempotency semantics.

Q6-Q8 remain planned/inactive.

Live SQLite runtime, daemon/systemd, Telegram transport, autonomous worker execution,
automatic module/business ACCEPT, automatic RETURN/HOLD, automatic follow-up prompt release,
business prompt release and cross-repository writes remain disabled.

Next:

`Q5_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- q4-deterministic-closeout-q5-activation-v0-1:end -->

<!-- q5-deterministic-closeout-q6-activation-v0-1:start -->
## Q5 deterministic closeout / Q6 activation — 2026-08-25

Q5 implementation commit:

`2309437b6a5e14b54f0a6de1c08e33f2bc5c553c`

Q5 result:

`Q5_ACCEPTED_PUBLISHED_CLOSED`

Acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_operator_attention_semantics_v0_1`

Current functional package:

`Q6`

Q6 scope is operator-attention semantics and causes. The hardening plan currently names attention
reasons including clarification escalation, access required, execution blocked, unable to execute,
no dispatchable work, operator execution/acceptance required, manual review, stale coordination,
dependency blocked and repeated verification failure.

Attention state must remain independent from transport. Q6 does not enable Telegram delivery,
daemon/systemd or live SQLite merely by defining semantic attention state.

Q7-Q8 remain planned/inactive.

Automatic module/business ACCEPT, automatic RETURN/HOLD, automatic next-prompt release,
business prompt release and cross-repository writes remain disabled.

Next:

`Q6_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- q5-deterministic-closeout-q6-activation-v0-1:end -->

<!-- q6-deterministic-closeout-q7-activation-v0-1:start -->
## Q6 deterministic closeout / Q7 activation — 2026-08-25

Q6 implementation commit:

`7845ab850b334460a9120d827d2397f799339fc0`

Q6 result:

`Q6_ACCEPTED_PUBLISHED_CLOSED`

Acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_cross_module_question_routing_contract_v0_1`

Current functional package:

`Q7`

Q7 scope is the cross-module question-routing contract. Current v0.4.1 authority requires
contract/evidence semantics only, not persistent runtime. Allowed directional identities are
module -> Blueprint/operator, module -> module, and Blueprint -> module.

Q7 must preserve no cross-repository writes, evidence-backed answers, strategic ambiguity
escalation, direct operator routing for secrets/access where appropriate, and the existing
five-round per-thread clarification limit.

Q8 remains planned/inactive.

Live SQLite, daemon/systemd, Telegram transport, autonomous workers, automatic module/business
ACCEPT, automatic RETURN/HOLD, automatic next-prompt release and business prompt release remain
disabled.

Next:

`Q7_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- q6-deterministic-closeout-q7-activation-v0-1:end -->

<!-- q7-deterministic-closeout-q8-activation-v0-1:start -->
## Q7 deterministic closeout / Q8 activation — 2026-08-25

Q7 implementation commit:

`501d53352cdf5f4ea755de335aefc6b077c6ff02`

Q7 result:

`Q7_ACCEPTED_PUBLISHED_CLOSED`

Acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_logistics_clarification_reference_validation_v0_1`

Current functional package:

`Q8`

Q8 scope is Logistics clarification reference validation. It must prove the combined Q1-Q7
semantics against the accepted Logistics reference: recoverable clarification without RETURN,
representable module/operator routing identities, deterministic five-round escalation, explicit
blocker reason, immutable released prompt, separate scope-adjustment evidence, completion
deviations, visible attention state, no automatic module/business ACCEPT, no cross-repository
Blueprint write, and no unbounded/cross-phase automatic release.

H10 remains planned/inactive.

Q8 -> H10 is a major phase boundary and requires explicit manual progress confirmation after Q8
is accepted/published/closed. This Q7->Q8 transaction does not provide that approval.

Live SQLite, daemon/systemd, Telegram transport, autonomous workers, automatic module/business
ACCEPT, automatic RETURN/HOLD, automatic next-prompt release and business prompt release remain
disabled.

Next:

`Q8_IMPLEMENTATION_SCOPE_AND_ACCEPTANCE_CRITERIA_REVIEW`
<!-- q7-deterministic-closeout-q8-activation-v0-1:end -->

<!-- q8-closeout-h10-manual-phase-boundary-activation-v0-1:start -->
## Q8 closeout / H10 manual phase-boundary activation — 2026-08-25

Operator explicitly approved:

`Підтверджую перехід Q → H10.`

Q8 implementation:

`a028f94ce20b273b459e6b7ecb853540d93f3657`

Q8 result:

`Q8_ACCEPTED_PUBLISHED_CLOSED`

Q8 acceptance basis:

`deterministic_phase_gate`

Current v0.4.1 slice:

`blueprint_v0_4_1_ecosystem_rollout_balance_and_dependency_adoption_v0_1`

Current functional package:

`H10`

H10 objective remains the existing canonical objective: roll current coordination mechanics across
eligible modules. Activation is not rollout implementation.

Before substantive H10 rollout, perform the H10 entry/scope review using the existing entry
refinement: H9 accepted, B1-B2 complete, Q1-Q8 complete, current release reconciled, Logistics
reference still passing, and no new legacy dependency.

H11 remains planned/inactive and requires explicit manual `H10 -> H11` phase-boundary approval.

Live SQLite, daemon/systemd, Telegram, autonomous workers, automatic module/business ACCEPT,
automatic RETURN/HOLD, automatic business prompt release and cross-repository writes remain disabled.

Next:

`H10_ENTRY_AND_ECOSYSTEM_ROLLOUT_SCOPE_REVIEW`
<!-- q8-closeout-h10-manual-phase-boundary-activation-v0-1:end -->

<!-- logistics-only-automation-pilot-scope-v0-1:start -->
## Logistics-only automation pilot scope — 2026-08-25

Current H10 execution strategy is now explicit:

`pilot_first_fail_closed`

Sole module connected to the new automation validation flow:

`logistics_service`

All other modules:

`not_connected_until_logistics_stability_gate`

Before expansion:

- run at least `2` real automatic prompts on Logistics;
- obtain passing required checks and no unresolved blocking regression;
- perform positive operator stability review;
- record a separate reviewed expansion decision.

Library and Telegram are not connected to the new functionality during this pilot.
Website remains paused/excluded.

This is a scope clarification for H10 execution strategy, not H10 closeout and not H11 activation.

Durable decision:

`coordination/internal_work/blueprint/governance/2026-08-25__blueprint__logistics_only_automation_pilot_scope_decision_v0_1.yaml`

Immediate priority after publishing this clarification:

1. build two temporary knowledge archives;
2. preserve them outside repo history;
3. resume H-series work only if operator time remains.
<!-- logistics-only-automation-pilot-scope-v0-1:end -->

<!-- post-v0-4-1-knowledge-foundation-plan-v0-1:start -->
## Post-v0.4.1 owner-directed Knowledge Foundation plan — 2026-08-26

Current release authority remains `coordination/releases/current.yaml`.

At this checkpoint the live v0.4.1 phase is H10. This planning note does not alter H10/H11, activate
a package, release a business prompt or enable broad autonomy.

Owner direction: after the full v0.4.1 hardening program closes, the next major Blueprint foundation
is the Knowledge Foundation / project self-knowledge program before unrelated broad autonomous
expansion.

Planning references:
- `coordination/roadmaps/details/forprint_system_blueprint/knowledge_foundation_program_v0_1.md`
- `coordination/repository_knowledge/repository_knowledge_and_direction_snapshot_protocol_v0_3.md`
- `coordination/standards/knowledge/index.yaml`
<!-- post-v0-4-1-knowledge-foundation-plan-v0-1:end -->

<!-- blueprint-internal-zero-stage-before-logistics-external-pilot-2026-09-15:start -->
## Current pilot sequencing reconciliation — 2026-09-15

The previous Logistics-first policy is preserved as an **external/module pilot** policy, not as a prohibition on an earlier Blueprint-internal control-plane trial.

Current sequence:

1. finish the minimum governed worker stack: Procedure Graphs / Run Manifests, Handoff Compiler v2 and Dispatcher integration;
2. run exactly one bounded local Blueprint worker in manual/shadow zero-stage mode;
3. use real bounded Blueprint maintenance work to validate isolation, profile/budget/context selection, retries/recovery, validation and result handling;
4. close critical defects found by that internal trial;
5. use `logistics_service` as the first external/module pilot;
6. keep broad multi-module rollout blocked until external pilot evidence and later readiness/autonomy gates are satisfied.

The small local Dispatcher Telegram bot is a separate Dispatcher operator surface, not the full `telegram_bot` module. Unless a minimal subset proves to be a launch blocker, it belongs to early Blueprint-worker training backlog rather than pre-worker manual implementation.
<!-- blueprint-internal-zero-stage-before-logistics-external-pilot-2026-09-15:end -->

<!-- strategic-transition-vector-2026-09-16:start -->
## 2026-09-16 autonomous-worker transition
Read `coordination/global_policy/strategic_transition_vector_v0_1.md` and
`coordination/global_policy/governed_change_and_acceptance_policy_direction_v0_1.md`.

Until the first internal worker is usable, keep code work on the minimum CF-08 → CF-09 → CF-10 path except true blockers.
After launch, delegate bounded routine Blueprint self-hardening to the internal worker and move global/chat focus toward module audits, target functionality, complete roadmaps, dependencies and portfolio waves.
Early retry is observation-first. Mutation provenance reporting should evolve toward adapter/tool evidence ↔ observed diff reconciliation. Wave boundaries remain human-accepted.
<!-- strategic-transition-vector-2026-09-16:end -->
```

### `forprint_system_blueprint/coordination/global_policy/deterministic_worker_promotion_policy_v0_1.md`

- SHA256: `ecb2f4ebca65016d7c346fddd905dff016d51c325fb42586afc00bca303da2ac`
- Bytes: `3183`

```markdown
# Deterministic Worker Promotion Policy v0.1

Status: `CANONICAL_PLANNING_POLICY`
Owner: `forprint_system_blueprint`
Execution authority: `false`

## Purpose

ForPrint should use AI workers where they add real capability, while continuously moving stable,
repetitive and economically formalizable work into deterministic business logic, scripts,
contracts, templates or bounded reusable services.

This promotes and extends the earlier Managed Assistant Autonomy self-optimization direction
into a system-wide architecture rule.

## Preferred execution order

1. deterministic business/domain logic;
2. deterministic reusable tool/template/service;
3. AI worker;
4. human escalation where required.

AI remains appropriate for genuinely generative, ambiguous, interpretive or otherwise
uneconomic-to-formalize tasks.

## Permanent loop

`OBSERVE → PATTERN → CANDIDATE → ROI/RISK → OWNER/CONTRACT CHECK → IMPLEMENT IN DEV → VERIFY → ADOPT/ROLLBACK → OBSERVE AGAIN`

There is no terminal DONE state.

## Evidence

Where technically feasible, worker-enabled capabilities should expose enough diagnostic evidence
to distinguish deterministic success, partial deterministic handling followed by worker,
deterministic failure/insufficiency followed by worker, direct worker delegation, final failure
and human escalation.

Useful evidence may include request/capability class, deterministic handler path, worker-escalation
reason, AI/tool calls, retries, latency, cost/resource evidence, result/rework outcome and recurrence.

This evidence is diagnostic and must not become a second business source of truth.

## Promotion rule

A repeated AI pattern becomes a deterministic-promotion candidate when semantics are stable,
owner/contract evidence supports the behavior, deterministic handling is cheaper/safer/faster/more
reliable, module boundaries remain intact and an equivalent reusable capability does not already exist.

Frequency alone never authorizes implementation.

## Responsibility split

- Production Runtime Inspector / canonical runtime telemetry: factual runtime evidence where available.
- Project Inspector: architecture/conformance evidence, duplicate/equivalent capability candidates.
- Verification Lab: adversarial/regression verification.
- Blueprint + human governance: initial promotion decision, owner selection and gates.
- Each module owner: approved domain-local implementation.

Project Inspector does not own runtime truth or canonical business semantics.

## Adoption rule

This policy applies to every capability that invokes or materially depends on an AI/LLM/generative worker.
Module roadmaps should reference this global policy during their next controlled enrichment rather than
creating parallel local policies.

## Source lineage

- `coordination/internal_work/blueprint/evening_packages/2026-09-03__u92/governance/07_managed_assistant_autonomy_context_cost_policy_v0_1.md`
- `coordination/internal_work/blueprint/evening_packages/2026-09-03__u92/governance/09_verification_adversarial_testing_policy_v0_1.md`
- `coordination/internal_work/blueprint/evening_packages/2026-09-25__deterministic_promotion_verification_prepress_v0_1/`
```

### `forprint_system_blueprint/coordination/global_policy/deterministic_worker_promotion_policy_v0_1.yaml`

- SHA256: `3c8f952ff229504945d550bbeafe695a25dc2f4bfb734d2a4a996b64eae269d1`
- Bytes: `1259`

```yaml
schema_version: forprint_deterministic_worker_promotion_policy_v0_1
status: CANONICAL_PLANNING_POLICY
owner: forprint_system_blueprint
execution_authority: false
applies_when:
  - module_or_capability_invokes_ai_worker
  - module_or_capability_materially_depends_on_llm_or_generative_worker
execution_preference:
  - deterministic_business_logic
  - deterministic_reusable_tool_template_or_service
  - ai_worker
  - human_escalation_when_required
loop:
  - OBSERVE
  - PATTERN
  - CANDIDATE
  - ROI_RISK
  - OWNER_CONTRACT_CHECK
  - IMPLEMENT_IN_DEV
  - VERIFY
  - ADOPT_OR_ROLLBACK
  - OBSERVE_AGAIN
terminal_done_state: false
roles:
  production_runtime_inspector_or_canonical_runtime_telemetry: factual_runtime_evidence
  forprint_project_inspector: architecture_and_conformance_evidence
  verification_lab: adversarial_and_regression_verification
  forprint_system_blueprint_and_human_governance: candidate_decision_owner_selection_and_gates
  each_module_owner: approved_domain_local_implementation
guardrails:
  - frequency_does_not_authorize_implementation
  - ai_does_not_invent_canonical_business_truth
  - preserve_module_ownership_boundaries
  - reuse_existing_deterministic_capability_before_new_implementation
  - telemetry_is_not_business_truth
```

### `03_blueprint_authority/subsets/portfolio_full_horizon_target_states_v0_1__forprint_library.yaml`

- SHA256: `d3b050beda76ecd4bcc9f4fe1b6e557a455afadd91c7195059b6dc396d28685d`
- Bytes: `2725`

```yaml
source_container_key: modules
subset:
  forprint_library:
    strategic_priority: P0
    role: Canonical semantic/catalog/reference and shared UI publication authority
    target_state:
      agreed_or_recovered:
      - Canonical products/materials/services/operations/aliases/profiles; shared UI package publication.
      - Historical/reference asset semantics use stable asset and revision references; Library may own canonical reference-media
        metadata where applicable, while customer/order/production truth remains with its domain owners.
      - Historical Asset Index entries are projections over authoritative sources; an index/search result never becomes canonical
        asset, order or production truth.
      synthetic_or_proposed:
      - Fast capability/semantic discovery and mature version/adoption lifecycle.
    full_horizon_steps:
    - Reconcile current Library catalog, alias, template, naming-profile and UI publication evidence.
    - Confirm Library ownership of product/material/service/operation semantics and shared UI publication, excluding business
      workflows.
    - Complete capability/self-inventory for canonical IDs, aliases, misspellings, production tokens, templates and technical
      cards.
    - Define versioned naming/profile/default semantics consumed by Calculator, Prepress and operations surfaces.
    - Define material/product/service canonical identifiers and stable lookup contracts for Warehouse and other consumers.
    - 'Define UI design-system package lifecycle: lookup, proposal, prototype, Inspector review, operator approval, publish
      and adoption.'
    - Add version/adoption metadata and compatibility rules without creating live global CSS or uncontrolled defaults.
    - Plan fast capability/semantic discovery while keeping retrieval candidate-only and domain-owner truth authoritative.
    - Define deprecation/migration paths for legacy aliases/profiles and evidence requirements for consumer adoption.
    - Hold broader implementation until Contract Registry and consumer readiness are reconciled in the portfolio.
    - Define stable historical/reference asset metadata semantics including asset ID, source module, entity links, revision
      references, media type and provenance.
    - Define the boundary between Library-owned canonical reference media and customer/order/production assets owned by operational
      domains.
    dependencies_or_inputs:
    - forprint_contract_registry
    human_control_surfaces:
    - DEVELOPER_AUDIT
    - ADMIN_FACING
    inventory_state: OWNER_DIRECTION_CLEAR
    implementation_eligible_now: false
    portfolio_gate: HOLD_UNTIL_PORTFOLIO_READINESS_BASELINE_COMPLETE
    module_value_test: KEEP
```

### `03_blueprint_authority/subsets/portfolio_module_roadmap_approval_matrix_v0_1__forprint_library.yaml`

- SHA256: `1929d992815865b4f0d5caf588521dc4c37094cc8f17e8205b2bb78475eb8e81`
- Bytes: `5420`

```yaml
source_container_key: modules
subset:
  forprint_library:
    identity_state: CANONICAL
    strategic_priority: P0
    role: Canonical semantic/catalog/reference and shared UI publication authority
    module_value_test: KEEP
    inventory_state: OWNER_DIRECTION_CLEAR
    dependencies_or_inputs: &id001
    - forprint_contract_registry
    owns:
    - product_catalog_semantics
    - service_catalog_semantics
    - material_catalog_semantics
    - operation_catalog_semantics
    - aliases
    - templates
    - technical_cards
    - contract_definitions
    - ui_design_system_publication
    - shared_ui_component_catalog
    - ui_component_version_and_adoption_metadata
    must_not_own:
    - operational_orders
    - client_database
    - accounting_truth
    - production_runtime
    - crm_workflow
    - domain_business_rules_outside_library_semantics
    target_state:
      agreed_or_recovered:
      - Canonical products/materials/services/operations/aliases/profiles; shared UI package publication.
      synthetic_or_proposed:
      - Fast capability/semantic discovery and mature version/adoption lifecycle.
    roadmap_status: PLANNING_ONLY_NOT_DISTRIBUTED
    steps:
    - sequence: 1
      step_id: FORPRINT_LIBRARY-H01
      title: Reconcile current Library catalog, alias, template, naming-profile and UI publication evidence.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: current_evidence_reconciliation
      execution_authority: false
      dependency_gate: []
    - sequence: 2
      step_id: FORPRINT_LIBRARY-H02
      title: Confirm Library ownership of product/material/service/operation semantics and shared UI publication, excluding
        business workflows.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: ownership_and_role_boundary
      execution_authority: false
      dependency_gate: []
    - sequence: 3
      step_id: FORPRINT_LIBRARY-H03
      title: Complete capability/self-inventory for canonical IDs, aliases, misspellings, production tokens, templates and
        technical cards.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: self_inventory_requirement
      execution_authority: false
      dependency_gate: []
    - sequence: 4
      step_id: FORPRINT_LIBRARY-H04
      title: Define versioned naming/profile/default semantics consumed by Calculator, Prepress and operations surfaces.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: dependency_and_contract_planning
      execution_authority: false
      dependency_gate: *id001
    - sequence: 5
      step_id: FORPRINT_LIBRARY-H05
      title: Define material/product/service canonical identifiers and stable lookup contracts for Warehouse and other consumers.
      approval_state: AGREED_OR_RECOVERED_TARGET
      source_basis: agreed_or_recovered_target_state
      execution_authority: false
      dependency_gate: []
    - sequence: 6
      step_id: FORPRINT_LIBRARY-H06
      title: 'Define UI design-system package lifecycle: lookup, proposal, prototype, Inspector review, operator approval,
        publish and adoption.'
      approval_state: AGREED_OR_RECOVERED_TARGET
      source_basis: agreed_or_recovered_target_state
      execution_authority: false
      dependency_gate: []
    - sequence: 7
      step_id: FORPRINT_LIBRARY-H07
      title: Add version/adoption metadata and compatibility rules without creating live global CSS or uncontrolled defaults.
      approval_state: AGREED_OR_RECOVERED_TARGET
      source_basis: agreed_or_recovered_target_state
      execution_authority: false
      dependency_gate: []
    - sequence: 8
      step_id: FORPRINT_LIBRARY-H08
      title: Plan fast capability/semantic discovery while keeping retrieval candidate-only and domain-owner truth authoritative.
      approval_state: PROPOSED_TARGET_REFINEMENT
      source_basis: proposed_mature_target
      execution_authority: false
      dependency_gate: []
    - sequence: 9
      step_id: FORPRINT_LIBRARY-H09
      title: Define deprecation/migration paths for legacy aliases/profiles and evidence requirements for consumer adoption.
      approval_state: PROPOSED_TARGET_REFINEMENT
      source_basis: proposed_mature_target
      execution_authority: false
      dependency_gate: []
    - sequence: 10
      step_id: FORPRINT_LIBRARY-H10
      title: Hold broader implementation until Contract Registry and consumer readiness are reconciled in the portfolio.
      approval_state: HOLD_FOR_FINAL_PORTFOLIO_APPROVAL
      source_basis: operator_distribution_gate
      execution_authority: false
      dependency_gate: *id001
    - sequence: 11
      step_id: FORPRINT_LIBRARY-H11
      title: Define stable historical/reference asset metadata semantics including asset ID, source module, entity links,
        revision references, media type and provenance.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: operator_confirmed_evening_architecture_20260919
      execution_authority: false
      dependency_gate: []
    - sequence: 12
      step_id: FORPRINT_LIBRARY-H12
      title: Define the boundary between Library-owned canonical reference media and customer/order/production assets owned
        by operational domains.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: operator_confirmed_evening_architecture_20260919
      execution_authority: false
      dependency_gate: []
```

---

# D. Git provenance

### `provenance/blueprint_branch.txt`

- SHA256: `dc22cda94c902fb29b26ae0eade2f4d474197999304fccaf304b9f8396af2066`
- Bytes: `45`

```text
audit/blueprint-inventory-refresh-2026-07-29
```

### `provenance/blueprint_head.txt`

- SHA256: `a584437da10108559d7ccea5131503370a2c3466a12031dc23b49f96100fd966`
- Bytes: `41`

```text
b6ab9b65a2c27b70a574468caa8e3de4c3b454c5
```

### `provenance/blueprint_status.txt`

- SHA256: `bfcbc1286a622321639dbfc32cc16805979f01c1395d0d0aa27519b2e8aad5d8`
- Bytes: `6608`

```text
 M AGENTS.md
 M README.md
 M coordination/bootstrap/START_HERE.md
 M coordination/global_policy/current_execution_focus.md
 M coordination/internal_work/blueprint/worker_tasks/index.yaml
 M coordination/standards/automation/index.yaml
 M indexes/README.md
 M indexes/authorities.yaml
 M indexes/contracts.yaml
 M indexes/dependencies.json
 M indexes/derivations.yaml
 M indexes/document_catalog.yaml
 M indexes/documents.yaml
 M indexes/files.json
 M indexes/governance.yaml
 M indexes/incoming_requests.yaml
 M indexes/index.yaml
 M indexes/knowledge_summary.yaml
 M indexes/legacy.yaml
 M indexes/modules.yaml
 M indexes/prompts.yaml
 M indexes/references.json
 M indexes/review_candidates.yaml
 M indexes/roadmaps.yaml
 M indexes/source_coverage.yaml
 M machine/contracts.yaml
 M machine/data_flows.yaml
 M machine/data_objects.yaml
 M machine/domains.yaml
 M machine/future_channel_readiness.yaml
 M machine/impact_rules.yaml
 M machine/module_identity_registry.yaml
 M machine/module_manifest_schema.yaml
 M machine/module_status_report_schema.yaml
 M machine/modules.yaml
 M machine/ownership.yaml
 M machine/system_control_flows.yaml
 M machine/system_layers.yaml
?? coordination/bootstrap/ACTIVE_RECONCILIATION_QUESTIONS.yaml
?? coordination/bootstrap/assistant_context_system_specs_v0_1.yaml
?? coordination/bootstrap/index_v0_1.yaml
?? coordination/bootstrap/parallel_workstream_current_snapshot_v0_1.yaml
?? coordination/continuity/events/000066__evt-u180j-plan-20260921t102727249527__4dd85ce6ef7f.yaml
?? coordination/continuity/events/000067__evt-u180j-activate-20260921t102955259861__ad000c7b9af2.yaml
?? coordination/continuity/execution_attempts/cf10-u180j-a003__1c8b6804277a.yaml
?? coordination/continuity/execution_attempts/cf10-u180j-a003__571944de6a4e.yaml
?? coordination/continuity/execution_attempts/cf10-u180j-a004__bc64bdd79056.yaml
?? coordination/continuity/execution_attempts/cf10-u180j-a004__be56313f5c2f.yaml
?? coordination/continuity/projections/BLOCKERS.yaml
?? coordination/continuity/projections/CURRENT_WORKFRONT.yaml
?? coordination/continuity/projections/DECISIONS.yaml
?? coordination/continuity/projections/NEXT_HORIZON.yaml
?? coordination/continuity/projections/RECENT_ACTIVITY.yaml
?? coordination/continuity/projections/SOURCE_STATE.yaml
?? coordination/continuity/projections/UNRECONCILED_CURRENT_DELTA.yaml
?? coordination/continuity/projections/WORKER_PORTFOLIO.yaml
?? coordination/internal_work/blueprint/worker_tasks/cf10_local_dispatcher_telegram_operator_surface_v0_1.yaml
?? coordination/internal_work/blueprint/worker_tasks/cf10_zero_stage_dispatch_boundary_regression_v0_1.yaml
?? coordination/roadmap_execution/projections/ROADMAP_EXECUTION_STATUS.yaml
?? coordination/roadmap_execution/projections/ROADMAP_RECONCILIATION_STATUS.yaml
?? coordination/roadmaps/details/forprint_system_blueprint/control_foundation_near_horizon_program_v0_1.yaml
?? coordination/standards/automation/control_plane/bootstrap_task_context_mode_v0_1.yaml
?? coordination/standards/automation/control_plane/bootstrap_worker_runtime_profile_v0_1.yaml
?? coordination/standards/automation/control_plane/module_bootstrap_execution_policy_v0_1.yaml
?? coordination/standards/automation/control_plane/module_bootstrap_prompt_requirements_v0_1.yaml
?? coordination/standards/automation/worker_candidate_promotion_contract_v0_1.yaml
?? coordination/standards/automation/worker_runtime_adapter_registry_contract_v0_1.yaml
?? coordination/standards/automation/worker_runtime_benchmark_contract_v0_1.yaml
?? coordination/standards/automation/worker_task_envelope_contract_v0_1.yaml
?? coordination/work_fronts/cf10_internal_dispatch_exception_real_workspace_v0_1.yaml
?? coordination/work_fronts/cf10_internal_task_context_adapter_v0_1.yaml
?? coordination/work_fronts/cf10_isolated_workspace_dispatch_preflight_v0_1.yaml
?? coordination/work_fronts/cf10_local_dispatcher_telegram_operator_surface_v0_1.yaml
?? coordination/work_fronts/cf10_multi_provider_runtime_registry_v0_1.yaml
?? coordination/work_fronts/cf10_runtime_standards_index_convergence_v0_1.yaml
?? coordination/work_fronts/cf10_worker_runtime_foundation_v0_1.yaml
?? coordination/work_fronts/cf10_zero_stage_dispatch_boundary_regression_v0_1.yaml
?? indexes/execution_dependency_graph.yaml
?? indexes/generator_inventory.yaml
?? scripts/coordination/build_worker_invocation.py
?? scripts/coordination/control_plane/context/__init__.py
?? scripts/coordination/control_plane/context/bootstrap_task_context.py
?? scripts/coordination/control_plane/context/runtime.py
?? scripts/coordination/control_plane/context/task_context_adapter.py
?? scripts/coordination/control_plane/tasking/__init__.py
?? scripts/coordination/control_plane/tasking/envelope.py
?? scripts/coordination/control_plane/tasking/runtime.py
?? scripts/coordination/control_plane/tasking/sources/__init__.py
?? scripts/coordination/control_plane/tasking/sources/external_prompt_queue.py
?? scripts/coordination/control_plane/tasking/sources/manual_internal.py
?? scripts/coordination/roadmap_execution_reconciliation.py
?? scripts/validation/control_plane/context/validate_bootstrap_task_context_mode_v0_1.py
?? scripts/validation/control_plane/context/validate_logistics_bootstrap_prompt_v0_2_candidate.py
?? scripts/validation/control_plane/context/validate_module_bootstrap_prompt_requirements_v0_1.py
?? scripts/validation/control_plane/worker_runtime/validate_bootstrap_worker_runtime_profile_v0_1.py
?? scripts/validation/validate_cf10_internal_dispatch_exception_real_workspace_v0_1.py
?? scripts/validation/validate_cf10_internal_task_context_adapter_v0_1.py
?? scripts/validation/validate_cf10_multi_provider_runtime_registry_v0_1.py
?? scripts/validation/validate_console_worker_adapter_v0_1.py
?? scripts/validation/validate_roadmap_execution_reconciliation_v0_1.py
?? scripts/validation/validate_worker_runtime_foundation_v0_1.py
?? tests/coordination/control_plane/context/test_bootstrap_task_context_mode_v0_1.py
?? tests/coordination/control_plane/context/test_cf10_internal_task_context_adapter_v0_1.py
?? tests/coordination/control_plane/context/test_module_bootstrap_prompt_requirements_v0_1.py
?? tests/coordination/control_plane/tasking/test_worker_task_envelope_v0_1.py
?? tests/coordination/control_plane/test_cf09_dispatcher_assistant_ack_gate_v0_1.py
?? tests/coordination/test_console_worker_adapter_v0_1.py
?? tests/validation/test_cf10_multi_provider_runtime_registry_contract_v0_1.py
?? tests/validation/test_roadmap_execution_dependency_registration_v0_1.py
?? tests/validation/test_roadmap_execution_reconciliation_v0_1.py
```

### `provenance/library_branch.txt`

- SHA256: `e0e361f0c897b5e211bcc3c632477ffd4133456a668212f7bd42dc4f0ccdfab5`
- Bytes: `46`

```text
feature/library-calculator-input-contract-v01
```

### `provenance/library_head.txt`

- SHA256: `b34b89944b4d96e23fa8d15cf0c3533cd1bd744ae4c6cd87c4543d6f0644086f`
- Bytes: `41`

```text
bba52bf6001f256a5c13ea7dbe175336b431754c
```

### `provenance/library_log_40.txt`

- SHA256: `c84d7f303970c56cd4ae3c499278b099f67a22f3fff30619250c826b8cd4db9a`
- Bytes: `2368`

```text
bba52bf (HEAD -> feature/library-calculator-input-contract-v01, origin/feature/library-calculator-input-contract-v01) fix: validate Library completion packet schema
89c4ec6 Record Calculator input completion packet
d094851 Record Library Calculator input contract completion
0b8cbce Add Library Calculator input contract
2a55286 fix: add Library validation compatibility targets
6a60816 chore: ignore local tmp helper
829df96 fix: align Library Blueprint prompt consumer with queue resolver
01f78ea (origin/main, main) Add Library business card governance closeout docs
a87d62c Finalize Library business card Blueprint acceptance metadata
1694215 Finalize Library business card completion metadata
ad99e0a Clean business card closure exporter whitespace
7a7cb85 Record Library business card skeleton completion
b8eb062 Add Library business card product skeleton
15e1c8c Record Library reference consumption pilot completion
7e000cb Add Library reference consumption pilot
d5ae83d Add Library coordination alignment commit report
8031d3e Record Library coordination foundation alignment completion
02e2cad Add Library coordination foundation alignment
27144f0 Resolve Library active prompt from prompt queue
052cd5b Align Library prompt navigation defaults
c048840 Record Blueprint acceptance in Library status
eb4b95d Refresh Library awareness after Blueprint acceptance
d2e1834 Verify Library reference contract foundation v0.2
3428289 Record Library reference contract prompt pull
007ec2f Mark Library prompt queue baseline
b401557 Acknowledge Library critical Blueprint baseline
03aaba7 Apply Library baseline document awareness review
3f69d57 Expose document ledger updater in Library Makefile
893ff2b Clean Library document awareness ledger placeholder
8cd7c23 Add Library document awareness ledger
66bd544 Refresh Library check report after Makefile alignment
dac2c2c Align Makefile with Blueprint prompt and awareness tooling
6343f65 Record Library reference contract completion
78bd7e1 Add Library reference contract foundation
781bb30 Refresh Library Blueprint standards snapshot
935e51b Record Library semantic readiness completion
28fe2d0 Align Library make-first semantic readiness workflow
4811e33 Add Library governance check target
0006127 Update Library check reports after metadata normalization
b8221fd Normalize Library coordination status metadata
```

### `provenance/library_status.txt`

- SHA256: `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`
- Bytes: `1`

```text

```

### `provenance/library_upstream.txt`

- SHA256: `b34b89944b4d96e23fa8d15cf0c3533cd1bd744ae4c6cd87c4543d6f0644086f`
- Bytes: `41`

```text
bba52bf6001f256a5c13ea7dbe175336b431754c
```
