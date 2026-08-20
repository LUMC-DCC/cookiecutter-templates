# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

{% if cookiecutter.homepage_url and cookiecutter.homepage_url != cookiecutter.repository_url -%}
Homepage: {{ cookiecutter.homepage_url }}
{% endif -%}
{% if cookiecutter.documentation_url and cookiecutter.documentation_url != cookiecutter.repository_url and cookiecutter.documentation_url != cookiecutter.homepage_url -%}
Documentation: {{ cookiecutter.documentation_url }}
{% endif %}
{% set effective_formatter_tool = cookiecutter.formatter_tool if cookiecutter.formatter_tool in cookiecutter._template_supported_choices.formatter_tool else cookiecutter._template_defaults.formatter_tool -%}
{% set effective_linter_tool = cookiecutter.linter_tool if cookiecutter.linter_tool in cookiecutter._template_supported_choices.linter_tool else cookiecutter._template_defaults.linter_tool -%}
{% set effective_type_checker = cookiecutter.type_checker if cookiecutter.type_checker in cookiecutter._template_supported_choices.type_checker else cookiecutter._template_defaults.type_checker -%}
{% set has_quality_checks = effective_formatter_tool != "none" or effective_linter_tool != "none" or effective_type_checker != "none" -%}

## Installation

```bash
@@PROJECT_SETUP_ALL@@
```

## Usage

```bash
@@PROJECT_RUN@@python -m {{ cookiecutter.project_slug }}
```

## Development

```bash
{% if cookiecutter.include_citation_cff == "yes" -%}
@@METADATA_VALIDATE@@
{% endif -%}
{% if cookiecutter.include_changelog == "yes" -%}
@@PROJECT_RUN@@python tools/check_changelog.py
{% endif -%}
{% if effective_linter_tool == "ruff" -%}
@@PROJECT_RUN@@ruff check .
{% endif -%}
{% if effective_formatter_tool == "ruff" -%}
@@PROJECT_RUN@@ruff format --check .
{% endif -%}
{% if effective_type_checker == "mypy" -%}
@@PROJECT_RUN@@mypy src
{% endif -%}
{% if has_quality_checks -%}
@@PROJECT_RUN@@pre-commit run --all-files
{% endif -%}
{% if cookiecutter.include_tests == "yes" -%}
@@PROJECT_RUN@@python -m pytest
{% endif -%}
```
