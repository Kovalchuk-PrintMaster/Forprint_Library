# ForPrint Library Check Report

Generated at: `2026-06-05T18:21:47`

| Check | Expected result | Status | Time | Details |
|---|---|---:|---:|---|
| Ruff lint | No lint errors | OK | 0.04s | All checks passed! |
| Pytest | All tests pass | OK | 0.31s | .....                                                                    [100%]<br>5 passed in 0.03s |
| Catalog seed validation | Seed exists or is deferred to Checkpoint B | WARN | 0.00s | Deferred to Checkpoint B. |
| Required architecture docs | Docs exist or are deferred to Checkpoint C | WARN | 0.00s | Deferred to Checkpoint C: ['docs/architecture/canonical_id_policy.md', 'docs/architecture/alias_policy.md', 'docs/architecture/dependent_module_usage.md'] |
| Blueprint source config | blueprint_source.yaml is valid | OK | 0.00s | coordination/blueprint_source.yaml |
| Prompts index | coordination/prompts/index.yaml is valid | OK | 0.00s | coordination/prompts/index.yaml |
| Reports index | coordination/reports/index.yaml is valid | OK | 0.00s | coordination/reports/index.yaml |
| Coordination status YAML | current_status.yaml exists | OK | 0.00s | coordination/status/current_status.yaml |
| Coordination status MD | current_status.md exists | OK | 0.00s | coordination/status/current_status.md |
| Next questions | next_questions_for_blueprint.md exists | OK | 0.00s | coordination/status/next_questions_for_blueprint.md |
| Module manifest boundary | Manifest exists and forbids operational ownership | OK | 0.01s | Boundary exclusions are present. |
| Makefile standard targets | Required targets exist | OK | 0.00s | All required targets found. |
| Blueprint policy check | Blueprint paths readable; module directives may be deferred | OK | 0.05s | OK: Blueprint root: /srv/software_development/forprint-project/forprint_system_blueprint<br>OK: Global policy: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/global_policy<br>OK: Standards: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/standards<br>OK: Module policy: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/module_policy/forprint_library/module_policy.md<br>OK: Global directives index: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/directives/global/index.yaml<br>WARN: Module directives index missing/deferred: /srv/software_development/forprint-project/forprint_system_blueprint/coordination/directives/modules/forprint_library/index.yaml |
