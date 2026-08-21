# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

This documentation does not assume a build tool yet.

## Contents

- [Project overview](overview.md)
{% if "user" in cookiecutter.documentation_types.entries %}
- [Usage](usage.md)
{% endif %}
{% if "deployment" in cookiecutter.documentation_types.entries %}
- [Deployment notes](deployment.md)
{% endif %}
{% if "developer" in cookiecutter.documentation_types.entries %}
- [Developer guide](developer.md)
- [Technical reference](reference.md)
{% endif %}
- [Access and publish the documentation](documentation.md)
- [Legal and licensing](legal.md)
