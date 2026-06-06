# Dependent Module Usage Policy

## Status

Draft policy for modules that consume ForPrint Library catalog data.

## Purpose

This document explains how dependent ForPrint modules may consume Library
canonical catalog seed data.

ForPrint Library is the canonical semantic, catalog, naming, alias and
contract-definition authority. Dependent modules may consume Library data, but
must not become independent permanent catalog owners.

## Calculator Engine

Calculator Engine may consume Library catalog seed as projection input.

It may use Library IDs for product families, materials, operations, print modes
and finishing options.

Calculator Engine must not become the canonical catalog owner.

## Telegram Bot

Telegram Bot may display product choices derived from Library or Calculator
projections.

Telegram Bot must not create independent permanent product catalogs.

## Operational Registry

Operational Registry stores operational records and may store references to
Library IDs.

Example:

```yaml
product_family_id: business_card
material_id: paper_350g_gloss
operation_id: digital_print
print_mode_id: color_4_4
finishing_option_id: matte_lamination

Operational Registry must not redefine Library catalog truth.

Accounting Registry

Accounting Registry may map Library IDs to 1C nomenclature references.

It owns accounting synchronization workflows, not Library semantic truth.

Prepress Hub

Prepress Hub may use Library operation, template and technical-card references.

It must not become the canonical naming source for products, materials or
operations.

CRM

CRM may present Library-derived choices to users and managers.

CRM may coordinate human review, but it must not become the physical owner of
Library catalog data.

Website and future Mobile App

Website and future Mobile App should consume channel-agnostic projections
through approved contracts or Gateway/Calculator flows.

They should not maintain separate permanent catalog definitions.

Current limitation

Canonical Catalog Seed v0.1 is projection-safe but not final:

catalog_status: draft_canonical_seed
schema_status: unstable_v0_1
usage: allowed_for_projection_use
contract_status: not_final_contract
owner_module: forprint_library