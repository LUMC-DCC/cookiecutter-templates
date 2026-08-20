# Support

{% if cookiecutter.documentation_url or cookiecutter.support_routes.entries -%}
## Routes

| Need | Route |
| --- | --- |
{% if cookiecutter.documentation_url -%}
| Documentation | {{ cookiecutter.documentation_url }} |
{% endif -%}
{% for route in cookiecutter.support_routes.entries -%}
| {{ route.purpose if route.purpose is defined and route.purpose else route.name if route.name is defined and route.name else route.type if route.type is defined and route.type else "Support" }} | {{ route.url if route.url is defined and route.url else route.contact if route.contact is defined and route.contact else route.name if route.name is defined and route.name else "Contact the maintainers" }} |
{% endfor %}

{% else -%}
Contact the project maintainers for support.

{% endif -%}
Use the issue templates for bug reports and feature requests when they are
available.

## What to include

When asking for help, include:

- version or commit
- operating system and environment details
- command, input, or workflow that failed
- expected behavior
- observed behavior and full error message

{% if cookiecutter.maintenance_level -%}
## Maintenance level

{{ cookiecutter.maintenance_level }}

{% endif -%}
Support is limited to the public maintenance commitment for this project.
