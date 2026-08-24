# For service integrators

This section is for teams building services that generate repositories from
these templates.

Services should provide a service-agnostic Cookiecutter context matching
`_contracts/template_context.json`. Service-specific conversion belongs outside
this repository. For example, an SMP or DSW adapter should translate its own data
model into the template context before calling Cookiecutter.

The workflow for an integration service is:

```text
service data
→ template context
→ validate with _contracts/template_context.schema.json
→ pass as Cookiecutter extra_context
```

`_contracts/template_context.json` is the readable contract. The JSON Schema is
generated from it so services can validate payloads with standard tooling.

## Integration shape

Callers should:

1. Select the template directory from `language`.
2. Pass known context fields through `extra_context`.
3. Avoid sending private or internal-only details.
4. Treat `_contracts/template_context.json` as the stable interface.
5. Use `_contracts/field_usage.json` to understand which generated artifacts are
   affected by each field.
6. Validate payloads against `_contracts/template_context.schema.json` before
   calling Cookiecutter.

The templates may accept rich nested values such as `authors.entries`,
`funding.entries`, and `interfaces.entries`.

Integrator payloads must explicitly provide `language`, `project_name`,
`project_slug`, and `project_short_description`. These identify the generated
project and should not silently inherit demonstration defaults. Other fields
are optional and use the defaults declared in the contract.

`project_slug` follows the selected language's package-name rules:

| Language | Accepted shape |
| --- | --- |
| `python` | Lowercase Python identifier using letters, digits, and underscores; it must start with a letter and cannot be a Python keyword. |
| `r` | At least two ASCII letters, digits, or dots; it must start with a letter and cannot end with a dot. |

These rules are available as language-conditional constraints in the generated
JSON Schema and are checked again by the generation hook.

Repeatable metadata values use this shape:

```json
{
  "authors": {
    "entries": [
      {
        "name": "Ada Lovelace",
        "email": "ada@example.org",
        "orcid": "0000-0000-0000-0000"
      }
    ]
  }
}
```

Person entries may provide a display `name` or structured `given_names` and
`family_names`; structured names require both parts, and services do not need
to duplicate both forms. `affiliation` is an organization object with a required
`name` and optional ROR `identifier`, `url`, `email`, and `address`. A person's
`roles` is one controlled array; there is no separate singular role field.

The generated JSON Schema controls the allowed keys for each entry type and
rejects unknown fields. For example, `authors.entries` accepts person fields,
while `funding.entries` accepts funding fields. This lets integrators catch
mapping mistakes in their own service before rendering a repository.

Independent on/off options are scalar `yes`/`no` values. Controlled
multi-selects use an `entries` array, including `community_files`.

Services may also provide tooling choices when they know them, such as
`documentation_builder`. If a service does not provide a tooling choice, the
selected language template uses its default from `_contracts/template_context.json`.

`interfaces.entries` uses controlled bio.tools tool types. `type` selects the
generated scaffold, while optional `specification` and SMP-controlled `status`
(`Stable`, `Experimental`, or `Internal`) are rendered as public documentation;
status does not suppress the requested scaffold.

`software_functions.entries` is the canonical interoperability structure for
operations, inputs, outputs, and commands. Input and output format records may
carry an EDAM term and URI plus `version_constraint`, `schema_constraints`, and
`sample_url`. Sample URLs also become linked CodeMeta supporting-data nodes.

`operating_systems.entries` maps the SMP fields to `name`, `specification`, and
`status`. Status accepts `Officially supported` or `Expected to work`;
officially supported platforms define the generated test matrix.

`external_dependencies.entries` describes important external requirements beyond
the normal language package manifest. Use it for software, standards, ontologies,
or platform tools that users or operators may need to provide or account for.
Each entry needs a `name` and may include `version_constraint`, `url`,
`license`, and `purpose`.

`external_services.entries` describes external services, partners, or roles
needed by the project. Each entry needs a `name` and may include `provider`,
`service_types`, `quantity`, and `cost_coverage`.

`test_types.entries` uses the SMP testing checklist labels, such as
`Smoke tests`, `Unit tests`, and `Integration tests`. `test_frameworks.entries`
uses controlled framework names; the Python template currently supports
`pytest`. An empty test-type list omits tests and their CI workflow.

Quality tools use one controlled selector per responsibility: `formatter_tool`,
`linter_tool`, and `type_checker`. The Python template currently supports
`ruff` for formatting and linting and `mypy` for optional type checking. Use
`none` to omit a responsibility. When at least one quality check is selected,
the Python template includes pre-commit as the local runner and `quality.yml`
as the CI runner.

CI inclusion is derived from the requested repository capabilities. Tests,
documentation, quality checks, changelog validation, license checking,
containers, and distribution each include their own workflow only when their
corresponding context is present.

`project_manager` is one controlled primary manager, not a free-form list.
Python accepts `uv`, `poetry`, `pdm`, `hatch`, `pixi`, or `pip` and defaults to
`uv`. R currently accepts `renv` or `rix`. A service should normalize the SMP
management-tools answer to the value supported by the selected template.
Generated Python projects use the selection consistently in local commands and
CI but do not ship a generated lockfile.

`containerization.entries` selects generated container recipes using `Docker`,
`OCI / Podman`, `Apptainer / Singularity`, or `Other`; optional `details`
preserves public context. Pixi is an environment and project manager; Nix is a
whole-environment manager but is not implemented by the current templates.
Lockfiles are outputs of the selected project manager rather than container
types. Python generates executable recipes for the three supported types.

`distribution_channels.entries` is a controlled, repeatable list of package
registries, container registries, archives, source distribution, installers,
and hosted-service delivery. Python automates package builds for PyPI, GitHub
Releases, and conda-forge selections, publishes PyPI and GitHub Releases on
matching tags, and publishes OCI images for GitHub Container Registry and
Docker Hub when an OCI recipe is present. Other selected channels are included
in generated release guidance for project-specific setup.

Use `Zenodo` as a distribution channel when releases will be archived there.
The generated `.zenodo.json` is derived from existing public project metadata;
`registries` remains for software catalogue records such as bio.tools or the
Research Software Directory.

README badges are derived rather than separately controlled. Repository,
documentation, distribution-channel, persistent-identifier, interface, and CI
fields determine which badges have enough information to render. External
self-assessment badges should be added only after the project has an assessment
URL or project identifier from the issuing service.

`versioning_scheme` is one controlled choice: `SemVer`, `CalVer`, or `Custom`.
Use `versioning_scheme_details` for an exact CalVer pattern such as `YYYY.MM` or
to preserve a custom policy from the source service. `version` remains the
actual release value. `release_frequency` records the expected cadence; it does
not schedule releases by itself.

`license_compatibility_check` is a binary `yes`/`no` value. Set it to `yes`
when the source data says dependency license compatibility is checked.

## Documentation and citation

Documentation is controlled by `documentation_types`. Supported canonical values
are `user`, `deployment`, and `developer`. Developer documentation includes the
technical reference for public APIs, commands, configuration, formats, and
extension points.
Passing an empty `documentation_types.entries` list omits the documentation
scaffold.

`documentation_builder` selects the build tooling for the selected
documentation pages. If a requested builder is not supported by the selected
language template, the language default is used.

`include_citation_cff` controls whether `CITATION.cff` is generated. When it is
disabled, generated metadata checks compare the remaining metadata files.

## Resources, sustainability, and risk

`problem_statement` and `value_proposition` preserve the corresponding public
SMP motivation answers in the generated project overview.

`resource_requirements` is public prose describing typical and worst-case
memory, storage, compute, GPU, wall-clock, or scaling needs.

`maintenance_level` is one controlled public commitment: `Active/routine
maintenance`, `Security maintenance only`, or `Best-effort maintenance / no
timeline commitment`. Leave it empty when no commitment is declared.
`continuity_plan` contains the public handover plan. `retirement_criteria` is a
controlled `entries` list using the choices declared in the context schema.

Use `security_measures.entries` for the controlled SMP measures and
`additional_security_measures` for public measures outside that list.
Use `regulatory_requirements.entries` for public selections from the SMP
compliance checklist and `additional_regulatory_requirements` for public
requirements outside it.
`security_contact`, `public_risk_notes`, `sensitive_data_statement`, and
`dmp_reference` must contain only information suitable for a public
repository.

## License

Use `license` for an SPDX identifier or custom license text. Leave it empty to
omit `LICENSE.txt`. Recognized SPDX identifiers are used for the generated
license file and machine-readable metadata. Unrecognized values are written to
`LICENSE.txt` as custom license text. Generation stops when the SPDX service is
unavailable or returns an invalid record, preventing an identifier from being
silently mistaken for custom license text.

## Community files

Community files use one controlled filename array. All standard files are
selected by default; pass an empty array to generate none:

```json
{
  "community_files": {
    "entries": ["CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md"]
  }
}
```

The standard community files default to included and can be disabled explicitly.
Content comes from broader context fields, such as `support_routes`, `governance_notes`,
`code_of_conduct_contact`, `security_contact`, `security_measures`,
`additional_security_measures`, `maintenance_level`, `public_risk_notes`,
`continuity_plan`, and release fields.

For SMP or DSW adapters, useful mappings include:

- contributing guidelines expectation to `CONTRIBUTING.md`
- code of conduct expectation to `CODE_OF_CONDUCT.md`
- release or changelog expectation to `CHANGELOG.md`
- governance text to `GOVERNANCE.md` and `governance_notes`
- security and access-control expectation to `SECURITY.md`,
  `security_contact`, and `security_measures`
- bug-reporting or feature-request expectation to `SUPPORT.md` and
  `support_routes`; each route contains a `system` and optional public `url`

Selecting `CONTRIBUTING.md` also includes a pull request template. When
`SUPPORT.md` is selected, the generated project includes structured GitHub issue
forms. These GitHub templates use public context only.

The shared community files use broadly recognized conventions where possible:

- `CODE_OF_CONDUCT.md` points to Contributor Covenant 2.0.
- `CHANGELOG.md` follows Keep a Changelog and can be combined with
  Conventional Commits or similar tooling for release automation.
- `SECURITY.md` and `SUPPORT.md` follow GitHub community-health file behavior,
  while their content remains useful outside GitHub.
