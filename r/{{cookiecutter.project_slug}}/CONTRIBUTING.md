# Contributing

Thank you for improving this project.

## Workflow

| Step | Rule |
| --- | --- |
| Branching | Create a short-lived branch from the target branch. |
| Scope | Keep each branch focused on one bug, feature, or documentation change. |
| Rebase | Rebase on the target branch before opening the pull request, before requesting review after long work, and before merge when the target branch changed. |
| Pull request | Open a pull request for every change to the target branch. |
| Review | Wait for maintainer review and passing CI before merge. |
| Merge style | Keep history linear; avoid merge commits from the target branch into the feature branch. |

Before starting a larger change, open an issue or discussion so maintainers can
confirm scope and avoid duplicated work.

{% set effective_documentation_builder = cookiecutter.documentation_builder if cookiecutter.documentation_builder in cookiecutter._template_supported_choices.documentation_builder else cookiecutter._template_defaults.documentation_builder %}
{% set should_build_docs = cookiecutter.documentation_types.entries and effective_documentation_builder in ["mkdocs", "sphinx"] %}
{% set effective_formatter_tool = cookiecutter.formatter_tool if cookiecutter.formatter_tool in cookiecutter._template_supported_choices.formatter_tool else cookiecutter._template_defaults.formatter_tool %}
{% set effective_linter_tool = cookiecutter.linter_tool if cookiecutter.linter_tool in cookiecutter._template_supported_choices.linter_tool else cookiecutter._template_defaults.linter_tool %}
{% set effective_type_checker = cookiecutter.type_checker if cookiecutter.type_checker in cookiecutter._template_supported_choices.type_checker else cookiecutter._template_defaults.type_checker %}
{% set has_quality_checks = effective_formatter_tool != "none" or effective_linter_tool != "none" or effective_type_checker != "none" %}
{% set release_channels = namespace(values=[]) %}
{% for channel in cookiecutter.distribution_channels.entries %}
{% set _ = release_channels.values.append(channel | lower) %}
{% endfor %}
{% set has_distribution = "pypi" in release_channels.values or "github release" in release_channels.values or "github releases" in release_channels.values or "conda-forge" in release_channels.values %}

Use the pull request template when opening a pull request.

## Development setup

{% if cookiecutter.language == "python" %}
This project uses `@@PROJECT_MANAGER@@` for its development environment.

```bash
@@PROJECT_SETUP_ALL@@
```

Add a Python dependency with:

```bash
@@PROJECT_ADD@@
```

@@PROJECT_LOCK_GUIDANCE@@
{% elif cookiecutter.language == "r" %}
Install the package dependencies with the package-management workflow used by
this project.
{% else %}
Install the project dependencies with the package-management workflow used by
this project.
{% endif %}

## Local checks

{% if cookiecutter.language == "python" %}
| Check | Command |
| --- | --- |
{% if "CHANGELOG.md" in cookiecutter.community_files.entries %}
| Changelog format | `@@PROJECT_RUN@@python tools/check_changelog.py` |
{% endif %}
{% if has_distribution %}
| Release metadata | `@@PROJECT_RUN@@python tools/check_release.py` |
{% endif %}
{% if effective_linter_tool == "ruff" %}
| Lint | `@@PROJECT_RUN@@ruff check .` |
{% endif %}
{% if effective_formatter_tool == "ruff" %}
| Format | `@@PROJECT_RUN@@ruff format --check .` |
{% endif %}
{% if effective_type_checker == "mypy" %}
| Type checking | `@@PROJECT_RUN@@mypy src` |
{% endif %}
{% if has_quality_checks %}
| Pre-commit hooks | `@@PROJECT_RUN@@pre-commit run --all-files` |
{% endif %}
{% if cookiecutter.test_types.entries %}
| Tests | `@@PROJECT_RUN@@python -m pytest` |
{% else %}
| Import check | `@@PROJECT_RUN@@python -c "import {{ cookiecutter.project_slug }}"` |
{% endif %}
{% if should_build_docs and effective_documentation_builder == "mkdocs" %}
| Documentation | `@@PROJECT_RUN@@mkdocs build --strict` |
{% elif should_build_docs and effective_documentation_builder == "sphinx" %}
| Documentation | `@@PROJECT_RUN@@sphinx-build -W -b html docs/source docs/build/html` |
{% endif %}
{% else %}
Run the test, metadata, and documentation checks configured for this project.
{% endif %}

## Continuous integration

CI runs on every push and pull request.

{% if cookiecutter.language == "python" %}
| Stage | Runs when | What it does |
| --- | --- | --- |
{% if cookiecutter.include_citation_cff == "yes" %}
| Metadata | Citation metadata is included | Runs `rs-metadata validate`. |
{% endif %}
{% if "CHANGELOG.md" in cookiecutter.community_files.entries %}
| Changelog | Changelog is included | Runs `python tools/check_changelog.py`. |
{% endif %}
{% if cookiecutter.license_compatibility_check == "yes" %}
| License compatibility | License compatibility checking is enabled | Runs `licensecheck`. |
{% endif %}
{% if has_quality_checks %}
| Quality | Quality checks are included | Runs selected linting and type-checking commands. |
{% endif %}
{% if has_distribution %}
| Distribution | Distribution channels are declared | Validates release metadata and builds Python distributions; tagged releases publish configured channels. |
{% endif %}
{% if cookiecutter.test_types.entries %}
| Tests | Tests are included | Sets up the selected project environment and runs `python -m pytest`. |
{% endif %}
{% if should_build_docs and effective_documentation_builder == "mkdocs" %}
| Documentation | MkDocs documentation is included | Sets up the selected project environment and runs `mkdocs build --strict`. |
{% elif should_build_docs and effective_documentation_builder == "sphinx" %}
| Documentation | Sphinx documentation is included | Sets up the selected project environment and runs `sphinx-build -W -b html docs/source docs/build/html`. |
{% endif %}
{% endif %}

The pull request should be up to date with the target branch and all CI stages
should pass before merge.

## Commit messages

Use Conventional Commits for every commit that may be merged, and for the squash
commit title when the pull request is squashed.

| Prefix | Use for |
| --- | --- |
| `fix:` | bug fixes |
| `feat:` | user-facing features |
| `docs:` | documentation-only changes |
| `test:` | tests |
| `refactor:` | code changes without user-facing behavior changes |
| `build:` | build system, packaging, or dependency workflow changes |
| `ci:` | continuous integration changes |
| `chore:` | maintenance tasks that do not affect users |

Use an optional scope when useful, for example `fix(parser): handle empty input`.
Use `!` or `BREAKING CHANGE:` when a supported interface breaks.

## Pull request checklist

- [ ] The branch is rebased on the target branch.
- [ ] The pull request title follows Conventional Commits.
- [ ] The change is focused and linked to an issue or decision record when relevant.
- [ ] Metadata is updated when project name, authors, version, license, URLs, citation, or registry information changed.
- [ ] Documentation is updated when installation, usage, API, CLI, configuration, or behavior changed.
- [ ] Tests are added or updated for behavior changes.
- [ ] Local checks listed above pass.
- [ ] CI passes on the latest commit.
- [ ] `CHANGELOG.md` has a user-facing entry when the change affects users.
- [ ] No secrets, private data, or non-public security details are included.

## Release flow

Maintainers release from the target branch after CI passes. A release change
should update:

- `CHANGELOG.md`
- version metadata
- citation, archive, or registry metadata when relevant
- release notes for the publication channel used by the project
