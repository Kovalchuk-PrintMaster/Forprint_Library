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
