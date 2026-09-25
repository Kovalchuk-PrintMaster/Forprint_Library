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
