# Generated projects

Generated repositories are starting points. They include files that can be used
immediately and files that the project team should review, complete, and adapt.

## Review order

After generation, review the project in this order:

1. Read `README.md`.
2. Check `CITATION.cff`, if citation metadata was included.
3. Check `codemeta.json`.
4. Review the selected license.
5. Open `docs/`, if documentation types were selected.
6. Run the commands shown in the generated project.

## Common files

`README.md` is the quick front door for the project. It should stay short and
help people understand what the project is and where to go next. Prefer project
background and scope in `docs/overview.md`. When software functions are
provided, the README includes collapsible `biotools-function` metadata blocks
for tool registries and other downstream services.

`CITATION.cff` contains machine-readable citation metadata when citation
metadata is included.

`codemeta.json` contains cross-language FAIR software metadata for catalogues,
registries, archival systems, and institutional tooling.

Programming language entries appear in project documentation and in
`codemeta.json`. Software function records describe operations, inputs, outputs,
formats, and command examples in project documentation when provided.
Interface entries describe how users access the software and appear in generated
overview, usage, developer, and technical reference documentation when those
pages exist. Interface status describes maturity or intended visibility; it
does not change the architecture selected by the interface type.
Operating-system entries appear as platform support in the README and generated
documentation, and supported platforms are included in `codemeta.json` when
provided.
External dependency entries appear in generated documentation and are included
in `codemeta.json` as software requirements when provided.
External service entries appear in generated overview and deployment
documentation when provided.
Templates may also use controlled interface entries to include minimal working
code for common access routes, such as command-line tools, web APIs, scripts,
web applications, plug-ins, workflows, ontologies, portals, and library entry
points.

Generated code is deliberately organized so reusable logic sits behind thin
interface layers. Treat package `__init__.py` files as import boundaries rather
than places for application logic.

`LICENSE.txt` is included when a license value was provided. Recognized SPDX
identifiers are written from SPDX metadata. Unrecognized license values are
written as custom license text.

`docs/` contains project documentation when one or more documentation types are
selected. Longer motivation, scope, funding acknowledgements, and context should
live in the documentation overview rather than making the README heavy.

`tests/` contains the generated test suite when one or more test types are
selected. The selected types control which starter test files are kept.

`.github/workflows/` contains purpose-specific GitHub Actions configuration.
Each workflow is included only when its corresponding generated capability is
present. Some workflows are shared across templates, and some are
language-specific.

Python workflows read the supported Python version from `pyproject.toml`, so CI
and package metadata stay aligned when the runtime constraint changes.

| Workflow | Purpose |
| --- | --- |
| `metadata.yml` | Checks deterministic metadata overlaps. |
| `changelog.yml` | Checks changelog structure when changelog support is included. |
| `license-compatibility.yml` | Checks dependency license compatibility when enabled. |
| `quality.yml` | Runs selected linting, formatting, and type-checking commands. |
| `docs.yml` | Builds documentation when a buildable docs scaffold is included. |
| `tests.yml` | Runs generated tests when tests are included. |
| `containers.yml` | Builds selected container recipes and publishes configured OCI registries on release tags. |
| `distribution.yml` | Builds Python distributions and publishes configured package or release channels on release tags. |

Python workflows share `.github/actions/setup-python-project/action.yml`, which
installs the selected project manager and prepares one consistent environment
for tests, documentation, quality, licensing, and distribution jobs.

`tools/` contains project-maintenance commands, such as changelog and release
checks. These are not importable package modules or analysis scripts.

Generated documentation includes a release page with the versioning scheme,
expected cadence, distribution destinations, channel setup, and release steps.
Container usage is documented in deployment notes when deployment documentation
is selected.

When relevant public context is supplied, generated documentation also contains
small pages for resource requirements, sustainability, and security and data.
If documentation is omitted, these sections are placed in `README.md` so the
information remains discoverable without duplicating it when docs are present.

MkDocs reads project identity, description, and repository links from
`codemeta.json`. Sphinx reads project identity, organization, and repository
links from CodeMeta and the version from installed package metadata. The
documentation workflow builds these configurations in CI, while the metadata
workflow uses `rs-metadata` to validate the LUMC profile and compare CodeMeta
with detected package, citation, and container metadata.

See [Metadata](metadata.md) for how package metadata, CodeMeta, CFF, README
content, and documentation are expected to relate to each other.

## Community files

Community files are optional generated files for collaboration, support,
release notes, governance, and security reporting.

| File | Main context fields |
| --- | --- |
| `CONTRIBUTING.md` | `test_types`, `documentation_types`, quality selectors |
| `CODE_OF_CONDUCT.md` | `code_of_conduct_contact`, `maintainers` |
| `GOVERNANCE.md` | `maintainers`, `principal_investigators`, `governance_notes`, `continuity_plan`, `retirement_criteria` |
| `SECURITY.md` | `security_contact`, security and regulatory fields, `sensitive_data_statement`, `public_risk_notes`, `dmp_reference` |
| `SUPPORT.md` | `documentation_url`, `support_routes`, `maintenance_level` |
| `CHANGELOG.md` | `version`, `repository_url`, `versioning_scheme`, `versioning_scheme_details`, `release_frequency`, `distribution_channels` |

Review these files before sharing the repository publicly, especially private
contact routes for community and security reports.

When `CONTRIBUTING.md` is included, generated projects also include a GitHub
pull request template in `.github/pull_request_template.md`.

When `SUPPORT.md` is included, generated projects also include structured
GitHub issue forms for bug reports and feature requests in
`.github/ISSUE_TEMPLATE/`.

When `CHANGELOG.md` is included, generated projects also include
`tools/check_changelog.py`. Generated CI calls this check from a shared
`changelog.yml` workflow.

## Generated guidance

Each generated project includes its own commands for installation, usage,
testing, and documentation builds.

Python projects use the selected `project_manager` consistently in those
commands and in language-specific CI. Lockfiles are created by the manager when
the project is first set up; they are not manufactured during template
generation.

## Editable content

Generated text is intentionally conservative. Project teams should update
README sections, documentation pages, citation metadata, examples, and tests as
the project becomes more specific.
