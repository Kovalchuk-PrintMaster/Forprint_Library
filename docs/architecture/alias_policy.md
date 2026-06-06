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