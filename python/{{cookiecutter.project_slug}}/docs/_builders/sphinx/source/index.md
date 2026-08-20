# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

```{toctree}
:maxdepth: 2
:caption: Contents

overview
{% if "user" in cookiecutter.documentation_types.entries %}
usage
{% endif -%}
{% if "deployment" in cookiecutter.documentation_types.entries %}
deployment
{% endif -%}
{% if "developer" in cookiecutter.documentation_types.entries %}
developer
{% endif -%}
{% if "api" in cookiecutter.documentation_types.entries %}
api
{% endif -%}
{% if "tutorial" in cookiecutter.documentation_types.entries %}
tutorials/index
{% endif -%}
{% if "reference" in cookiecutter.documentation_types.entries %}
reference/index
{% endif -%}
documentation
legal
```
