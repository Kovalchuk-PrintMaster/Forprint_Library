# Source System Dictionary Policy

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
