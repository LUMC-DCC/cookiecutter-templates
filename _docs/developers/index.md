# For template developers

This section is for people maintaining and extending this template repository.

Development should be contract-first and test-driven. When adding or changing a
field, update the central contract and usage map before changing individual
template files.

## Context workflow

`_contracts/template_context.json` is the source of truth for the public context.
It generates two derived files:

- `_contracts/template_context.schema.json` for service-side validation
- `_cc_shared/cookiecutter.json` for Cookiecutter defaults and prompts

The shared Cookiecutter context is then synced into each language template as
`<template>/cookiecutter.json`. Edit the contract, regenerate the derived files,
and let tests verify that they stayed in sync.

## Way of working

1. Choose one coherent field group, such as people, licensing, or quality tooling.
2. Update `_contracts/template_context.json` if the public interface changes.
3. Update `_contracts/field_usage.json` to describe where the field should land.
4. Apply the field to generated artifacts.
5. Extend generation tests with representative context values.
6. Run the full verification suite.

Prefer small slices.

When updating `_contracts/field_usage.json`, prefer target names that describe
the artifact role. For example, use `docs overview page` or `citation abstract`
instead of only naming the file that happens to contain the value. Concrete file
paths should still be asserted in language-specific generation tests.

Repeatable context fields should be constrained in the contract. Use
`entry_schemas` for repeatable object fields and `item_schema` for repeatable
string fields so service integrators can validate payloads with
`_contracts/template_context.schema.json`.

When a default should differ between language templates, add `template_defaults`
to the field in `_contracts/template_context.json`. The sync script applies
those defaults when generating each template's `cookiecutter.json`.

When a field has language-specific validation, add `template_schemas` to its
contract entry. Schema generation emits conditional rules for integrators, and
the same fragments are copied into each template for hook-time validation.

When a field appears in machine-readable metadata, map its fullest public form
into `codemeta.json` and the supported subset into ecosystem metadata. The
official `rs-metadata` validator owns profile and cross-file comparison rules;
do not duplicate those rules in template code. The repository-wide strategy is
described in [Metadata](../users/metadata.md).

Keep builder-neutral generated documentation in the template's `docs/_shared/`
directory. Builder folders should contain only files that genuinely differ.
Prefer renderer functions for context-driven prose and derive build
configuration from generated metadata where the documentation tool supports it.

Post-generation code should read repeatable fields with the shared context
accessors and resolve controlled selectors with the shared choice resolver. The
rendered context is loaded in full, so adding a contract field does not require a
second declaration in the hook loader.

## Contract curation

The status values in `_contracts/field_usage.json` are curated by maintainers.
They are not inferred automatically, because a field can be rendered somewhere
while still missing other important artifacts.

Use these rules when changing a field status:

- Keep `planned` when a field exists in the contract but is not used by that
  template yet.
- Use `control` when the field decides whether files or directories are kept.
- Use `partial` when the field is rendered, but more intended targets remain.
- Use `implemented` only when the intended targets for that template are covered
  by tests.

Generated files must be refreshed after contract or usage-map edits:

```bash
poetry run python _scripts/build_context_schema.py
poetry run python _scripts/sync_shared.py
poetry run python _scripts/build_field_usage_docs.py
```

## Verification

Run the same checks locally that CI runs:

```bash
poetry run pre-commit run --all-files
poetry run python _scripts/audit_field_usage_status.py
poetry run python _scripts/audit_action_pins.py
poetry run pytest
poetry run python _scripts/check_generated_docs.py
poetry run mkdocs build --strict
git diff --exit-code
git diff --check
```

The audit script guards against stale status declarations by scanning each
template for `cookiecutter.<field>` references. It verifies that referenced
fields exist in the contract and are not still marked as `planned`.

External GitHub Actions must use full commit SHAs with their release tag in an
inline comment. Dependabot keeps those references and repository dependencies
current; the action-pin audit enforces immutability locally and in CI.
