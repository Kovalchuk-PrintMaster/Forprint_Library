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
