# Entity Type Dictionary Policy

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
