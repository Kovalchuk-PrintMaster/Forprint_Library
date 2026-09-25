
Business Card Skeleton
Product
product.business_card
Human names
uk: Візитки
en: Business cards
Why business cards first

Business cards are a small, familiar рекламно-інформаційний продукт with clear
options: size, sides, material, print mode, quantity and finishing.

This makes the product useful as a first configurable product skeleton without
forcing Library to implement pricing, orders, production, stock or runtime
integrations.

Constructor parameters
size
sides
material_ref
print_mode_ref
quantity
finishing_refs
artwork_source

quantity is input context only. It is not a price and does not trigger a
formula inside Library.

Library-owned references

The card uses existing Library draft catalog references:

product_families.business_card
materials.paper_300g_matte
materials.paper_350g_gloss
print_modes.color_4_0
print_modes.color_4_4
finishing_options.none
finishing_options.matte_lamination
finishing_options.gloss_lamination
finishing_options.corner_rounding
Consumer notes

Telegram Bot may use product.business_card and aliases as route hints only.

Calculator Engine may later use constructor parameters as pricing input context,
but no formula is implemented here.

Operational Registry may store product.business_card as foreign-domain
metadata, but Library does not create operational records.

Boundary

This is not a 1C import, not production runtime, not order creation, not stock
truth and not material write-off logic.
