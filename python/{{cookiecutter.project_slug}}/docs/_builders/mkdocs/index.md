# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Contents

- [Project overview](overview.md)
{% if "user" in cookiecutter.documentation_types.entries %}
- [Usage](usage.md)
{% endif -%}
{% if "deployment" in cookiecutter.documentation_types.entries %}
- [Deployment notes](deployment.md)
{% endif -%}
{% if "developer" in cookiecutter.documentation_types.entries %}
- [Developer guide](developer.md)
{% endif -%}
{% if "api" in cookiecutter.documentation_types.entries %}
- [API reference](api.md)
{% endif -%}
{% if "tutorial" in cookiecutter.documentation_types.entries %}
- [Tutorials](tutorials/index.md)
{% endif -%}
{% if "reference" in cookiecutter.documentation_types.entries %}
- [Reference](reference/index.md)
{% endif -%}
- [Build and view the documentation](documentation.md)
- [Legal and licensing](legal.md)
