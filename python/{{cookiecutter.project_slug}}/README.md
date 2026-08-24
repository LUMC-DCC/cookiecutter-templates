# {{ (cookiecutter.project_name or cookiecutter.project_slug) }}

{{ cookiecutter.project_short_description }}

{% if cookiecutter.urls.homepage and cookiecutter.urls.homepage != cookiecutter.urls.repository %}
Homepage: {{ cookiecutter.urls.homepage }}
{% endif %}
{% if cookiecutter.urls.documentation and cookiecutter.urls.documentation != cookiecutter.urls.repository and cookiecutter.urls.documentation != cookiecutter.urls.homepage %}
Documentation: {{ cookiecutter.urls.documentation }}
{% endif %}
{% set effective_formatter_tool = cookiecutter.quality_tools.formatter if cookiecutter.quality_tools.formatter in cookiecutter._template_supported_choices.quality_tools.formatter else "" %}
{% set effective_linter_tool = cookiecutter.quality_tools.linter if cookiecutter.quality_tools.linter in cookiecutter._template_supported_choices.quality_tools.linter else "" %}
{% set effective_type_checker = cookiecutter.quality_tools.type_checker if cookiecutter.quality_tools.type_checker in cookiecutter._template_supported_choices.quality_tools.type_checker else "" %}
{% set has_quality_checks = effective_formatter_tool or effective_linter_tool or effective_type_checker %}
{% set has_tests = cookiecutter.test_types.entries | length > 0 %}
{% set has_local_checks = "CHANGELOG.md" in cookiecutter.community_files.entries or has_quality_checks or has_tests %}

## Installation

Set up the project and its generated development tools from the repository root:

```bash
@@PROJECT_SETUP_ALL@@
```

## Usage

Run the package entry point inside the managed environment:

```bash
@@PROJECT_RUN@@python -m {{ cookiecutter.project_slug }}
```

{% if has_local_checks or cookiecutter.include_metadata %}
## Development

{% if has_local_checks %}
Run the checks that are configured for this project before opening a pull request:

```bash
{% if "CHANGELOG.md" in cookiecutter.community_files.entries %}
@@PROJECT_RUN@@python tools/check_changelog.py
{% endif %}
{% if effective_linter_tool == "ruff" %}
@@PROJECT_RUN@@ruff check .
{% endif %}
{% if effective_formatter_tool == "ruff" %}
@@PROJECT_RUN@@ruff format --check .
{% endif %}
{% if effective_type_checker == "mypy" %}
@@PROJECT_RUN@@mypy src
{% endif %}
{% if has_quality_checks %}
@@PROJECT_RUN@@pre-commit run --all-files
{% endif %}
{% if has_tests %}
@@PROJECT_RUN@@python -m pytest
{% endif %}
```
{% endif %}

{% if cookiecutter.include_metadata %}
Continuous integration also validates the project metadata.
{% endif %}
{% endif %}
