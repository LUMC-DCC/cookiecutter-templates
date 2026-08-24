# Contract overview

The template contract defines the service-agnostic context accepted by this
repository. It is intentionally broader than the files currently rendered by the
templates so that different services can provide rich public research software
metadata without coupling this repository to one upstream system.

## Source files

- `_contracts/template_context.json` is the only hand-maintained public context
  contract. It defines accepted fields, defaults, choices, categories,
  public/private expectations, and repeatable-entry schemas.
- `_contracts/template_context.schema.json` is generated from the context
  contract and can be used by services to validate incoming context payloads.
- `_contracts/field_usage.json` maps every field to generated artifacts and
  implementation status.
- `_cc_shared/cookiecutter.json` is generated from the context contract and then
  synced into language templates.

The dependency flow is:

```text
_contracts/template_context.json
├── _contracts/template_context.schema.json
└── _cc_shared/cookiecutter.json
    ├── python/cookiecutter.json
    └── r/cookiecutter.json
```

Edit `template_context.json` when the public context changes. Do not edit the
schema or Cookiecutter context files directly; regenerate them instead.

Usage-map targets should be short but self-explanatory. Prefer target names that
describe the role of the artifact or behavior, such as `README title`,
`package description`, `docs overview page`, or `generated smoke test imports`.
Avoid broad file-only labels when they do not explain how a field is used.

Some fields can define `template_defaults` when a sensible default differs by
language. For example, `documentation_builder` may default to `sphinx` for
Python and `pkgdown` for R while still exposing one service-agnostic field to
integrators.

Repeatable fields use an `entries` wrapper because Cookiecutter transports
nested values more reliably as objects than as bare lists. The allowed shape of
each entry is still controlled: `object_array` fields point to named
`entry_schemas`, `string_array` fields define an `item_schema`, and the generated
JSON Schema rejects unknown top-level and nested properties.

Root `required` fields are values an integration service must deliberately
supply: `language`, `project_name`, `project_slug`, and
`project_short_description`. Defaults still support direct Cookiecutter use.
Other fields may be omitted and use controlled defaults or empty values.

Symmetric multi-select controls use controlled `entries` arrays. For example,
`community_files.entries` contains only supported root filenames. Scalar
`yes`/`no` fields are reserved for independent binary policies such as
`include_citation_cff`.

`language` selects the template directory that Cookiecutter renders.
`programming_languages` describes the generated project implementation and can
contain multiple entries with version constraints and roles.

## Status meanings

- `external`: used by callers or Cookiecutter routing rather than rendered.
- `control`: controls whether generated files or directories are included.
- `implemented`: currently rendered into generated project artifacts.
- `partial`: rendered somewhere, but more relevant artifacts are planned.
- `planned`: represented in the contract and intentionally reserved for future work.

Statuses are tracked per template, because a field can be implemented in Python
while still planned for R, for example.

Statuses are human-curated. The automated audit checks whether a template
references a field that is missing from the contract or still marked `planned`,
but it does not decide whether all intended targets have been completed.

## Generated artifacts

After editing the contract or usage map, regenerate derived files before
committing:

```bash
poetry run python _scripts/build_context_schema.py
poetry run python _scripts/build_cookiecutter_context.py
poetry run python _scripts/sync_shared.py
poetry run python _scripts/build_field_usage_docs.py
```

CI reruns these commands and fails if they produce uncommitted changes.
