# Configurable Product Workbench

## Purpose

The Configurable Product Workbench is a Library-side pattern for describing
configurable рекламно-інформаційні продукти as stable reference objects.

This checkpoint introduces the pattern with one product only:
`product.business_card`.

## What Library owns

Library owns stable product semantics:

```text
product_id
human-readable names
aliases
compatibility aliases
constructor parameter definitions
references to Library catalog IDs
boundary and consumer usage notes
What consumers own

Downstream modules may own selected runtime values and context:

Telegram route context
Calculator pricing input context
Operational Registry foreign-domain metadata
channel-specific hints
runtime selections made outside Library

Consumer-owned values do not become Library-owned runtime state.

What this is not

This workbench skeleton is not:

a full product catalog
a product modeling UI
a production database
a live API
a 1C import
a 1C synchronization workflow
a Calculator integration
a Telegram Bot integration
an Operational Registry write path
a CRM write path
a Website write path
a price calculation engine
a material write-off engine
a warehouse stock truth source
a production runtime
Pattern for future products

Future products should copy the same structure:

one stable product_id
clear names and aliases
minimal constructor parameters
references to existing Library catalog IDs
consumer usage notes
explicit non-goals
validator coverage
human-readable preview

Do not expand this into a broad product database without a separate Blueprint
prompt.
