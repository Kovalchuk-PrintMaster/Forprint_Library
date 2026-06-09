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
