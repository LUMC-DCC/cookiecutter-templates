# Upstream repository suggestions

Reviewed against the pinned releases:

- `rsm-schema` at `5bdcbcbc4383d352a1385065265f970e9fd361ea`
- `rs-files-templates` at `cb90caa88ca839f4828dada5945e70ab54730564`

## rs-files-templates

1. Normalize constrained license values inside each metadata model. In
   particular, `ZenodoModel` should omit custom license text from Zenodo's SPDX
   license field, and `CitationModel` should populate its license from the RSM
   licensing object when the value is a valid SPDX expression.
2. Give SPDX consumers a public configuration interface for an alternative
   endpoint and a resolution result that distinguishes SPDX identifiers from
   custom terms. This would remove the need for callers to modify a module
   constant and repeat a network lookup.
3. Tighten Jinja whitespace handling in the package renderer and templates so
   conditional sections do not introduce leading or repeated blank lines.
4. Extend `ContributingModel` with optional capability rows for vulnerability
   scanning and license compatibility, plus local pre-commit and license checks
   when a consumer provides those commands. The current model covers metadata,
   manager, quality, test, documentation, and distribution stages but cannot
   describe every generated verification path.
5. Consider reusable models for GitHub issue forms and the pull-request
   template. They should move upstream only if their inputs and prose can remain
   language-neutral and repository-host-neutral.
6. Publish a machine-readable inventory of supported file models, or expose it
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

Contribution workflow, branching, and pull-request policy should remain
generator policy unless they become portable research-software metadata used by
multiple consumers.
