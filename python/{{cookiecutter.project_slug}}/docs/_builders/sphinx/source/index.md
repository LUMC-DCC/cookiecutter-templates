# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

```{toctree}
:maxdepth: 2
:caption: Contents

overview
{% if "user" in cookiecutter.documentation_types.entries %}
usage
{% endif %}
{% if "deployment" in cookiecutter.documentation_types.entries %}
deployment
{% endif %}
{% if "developer" in cookiecutter.documentation_types.entries %}
developer
reference
{% endif %}
documentation
legal
```
