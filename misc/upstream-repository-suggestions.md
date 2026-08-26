# Upstream repository suggestions

Reviewed against the pinned releases:

- `rsm-schema` at `5727be9bb76deaf43dff4bbc168bda4b217c63ab`
- `rs-files-templates` at `2486fd3a4d4c2bc67f5809cea6fdc02218561897`

## rs-files-templates

1. Normalize constrained license values inside each metadata model. In
   particular, `ZenodoModel` should omit custom license text from Zenodo's SPDX
   license field, and `CitationModel` should populate its license from the RSM
   licensing object when the value is a valid SPDX expression.
2. Give SPDX consumers a public configuration interface for an alternative
   endpoint and a resolution result that distinguishes SPDX identifiers from
   custom terms. This would remove the need for callers to modify a module
   constant and repeat a network lookup.
3. Extend `ContributingModel` with optional capability rows for vulnerability
   scanning and license compatibility, plus local pre-commit and license checks
   when a consumer provides those commands. The current model covers metadata,
   manager, quality, test, documentation, and distribution stages but cannot
   describe every generated verification path.
4. Publish a machine-readable inventory of supported file models, or expose it
   from the package API. Consumers could then check complete integration
   without discovering private package resources.

See [rs-files-templates template primers](rs-files-templates-template-primers.md)
for concrete models and acceptance criteria for additional reusable files.

## rsm-schema

1. Add an optional controlled `example_artifacts.entries` multi-select for
   generated, user-facing examples. Initial values could be `Jupyter notebook`,
   `Example script`, `API request collection`, and `Workflow example`. The
   default should be empty. This lets integrators request notebooks independently
   of interface type and avoids treating every library or script as a notebook
   project.
2. Consider a portable runtime-configuration model only when integrations need
   to describe public configuration keys. It should distinguish public settings
   from secrets and must never carry secret values. The current
   `external_services` records describe resources and providers, so they should
   not be repurposed as runtime endpoints.
3. Update the top-level `software_functions` description to name `operations`,
   `topics`, `inputs`, and `outputs`. Its referenced definition is current, but
   the prompt-facing description still lists the old singular property names
   and a removed `summary` property.

Contribution workflow, branching, and pull-request policy should remain
generator policy unless they become portable research-software metadata used by
multiple consumers.
