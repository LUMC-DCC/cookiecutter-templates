# Architecture

This repository maintains Cookiecutter templates for research software projects.
The Python template is the reference implementation while the shared layer and
tests are kept language-agnostic enough to support R and mixed-language
templates later.

## Repository layout

- `_contracts/` defines the service-agnostic template context. Any upstream
  service may produce this context, but service-specific conversion does not
  belong in this repository.
- `_cc_shared/` contains assets and hooks that should be identical across
  templates.
- `_scripts/` contains maintenance scripts for this template repository.
- `python/` contains the Python Cookiecutter template.
- `r/` contains the early R Cookiecutter template.
- `tests/` validates generated projects rather than only validating this
  repository.

Shared post-generation helpers in `_cc_shared/template_hooks/` follow the hook
pipeline structure:

- `context.py` loads rendered Cookiecutter values.
- `post_generation/` contains the actions run after Cookiecutter has rendered
  files, such as selecting documentation pages, generating the license file,
  selecting metadata files, updating public files, and removing disabled paths.
- `renderers/` builds Markdown fragments from context values. Larger renderer
  areas, such as `project_context/`, are split into focused modules by concern.
- `utils/` contains low-level helpers for paths, Markdown edits, and option
  parsing.

The context loader serializes the complete rendered Cookiecutter context.
Shared accessors read structured entries, template defaults, and supported
choices without maintaining a second field list inside the hook code.
Language-specific field constraints are also generated from the contract: the
JSON Schema exposes them to services, while hook metadata enforces them during
generation.

The top-level Cookiecutter `post_gen_project.py` should remain
orchestration-only.

The Python documentation scaffold keeps builder-neutral Markdown once under
`docs/_shared/`. Builder folders contain only navigation, configuration, and
builder-specific usage. Post-generation assembly copies the shared pages into
the selected MkDocs, Sphinx, or unbuilt documentation layout.

## Development workflow

The first quality gate is generation: every supported option set should produce
a coherent project with no unresolved Cookiecutter variables, no local machine
artifacts, and the expected optional files.

The Python template is tested through a small option matrix. Generated projects
must be importable, include valid packaging metadata, and pass their own smoke
tests when tests are enabled.

Machine-readable metadata is generated into both ecosystem-specific files and
cross-language standards. CodeMeta is the canonical metadata record, and the
official `rs-metadata` action validates the LUMC profile and semantic agreement
with each supported ecosystem file it discovers.

## Context contract

The context contract is intentionally broader than the files currently rendered
by the templates. It covers public information from the research software
management plan and the best-practice guidance:

- identity, descriptions, keywords, and initial version
- authors, maintainers, principal investigators, affiliations, roles, and ORCID
- funding, related software, audiences, purpose, purpose categories, and scope
- repository, homepage, documentation, registries, persistent identifiers, and
  publications
- SPDX identifiers, custom license text, and public license-compatibility notes
- documentation types, community files, GitHub templates, issue tracking, and
  governance notes
- programming languages, formats, functions, operations, interfaces, platforms,
  dependencies, and services
- tests, linting, type checking, derived CI, and project-management tools
- versioning scheme, releases, packaging, and distribution
- containerization, resource requirements, maintenance, retirement, and public
  risk statements

Sensitive or internal-only details should be reduced to public statements before
they reach this repository.

`_contracts/template_context.json` is the maintained source of truth. It is used
to generate the service-facing JSON Schema and the Cookiecutter context files:

```text
template_context.json
├── template_context.schema.json
└── cookiecutter.json files
```

Each context field also has an implementation entry in
`_contracts/field_usage.json`. Use that file as the working checklist when
applying fields to generated artifacts. A field should only move from `planned`
to `partial` or `implemented` when tests prove that a generated project renders
the intended artifact correctly.

Recommended implementation rhythm:

1. Pick one field group from `_contracts/field_usage.json`.
2. Add or update the generated artifacts that should consume those fields.
3. Extend the generation fixture with representative values.
4. Assert the rendered files contain the expected public metadata.
5. Update the field usage status and notes.

## Continuous integration

Repository CI mirrors the local maintenance workflow:

- regenerate the context JSON Schema, shared Cookiecutter context, synchronized
  template copies, and generated field-usage documentation
- fail if regenerated files differ from the committed state
- run the field-usage status audit
- generate Python template projects and run their tests
- render Python projects and build both MkDocs and Sphinx documentation with
  warnings treated as errors
- reject mutable third-party GitHub Action references
- build the MkDocs documentation with strict validation

The docs publishing workflow only deploys documentation from `main`; the CI
workflow is the quality gate for pull requests and pushes.

Third-party actions are pinned to full commit SHAs. Inline release-tag comments
allow Dependabot to update those immutable references. Generated repositories
also include weekly Action updates; Python repositories include Python
dependency updates.
