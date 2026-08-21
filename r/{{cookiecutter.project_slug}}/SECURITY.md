# Security

## Supported versions

| Version | Supported |
| --- | --- |
| Current release | Yes |
| Older releases | Best effort |

## Reporting a vulnerability

Do not report sensitive security issues in public issue trackers, discussions,
pull requests, or public forks.

{% if cookiecutter.security_contact %}
Report suspected vulnerabilities privately to: {{ cookiecutter.security_contact }}
{% elif cookiecutter.maintainers.entries %}
Report suspected vulnerabilities privately to the project maintainers listed in
the project metadata.
{% else %}
Report suspected vulnerabilities privately to the project maintainers.
{% endif %}

Include:

- affected version, branch, or commit
- operating system and relevant environment details
- steps to reproduce
- observed impact
- proof of concept or logs when safe to share privately

## Handling reports

Maintainers acknowledge reports, investigate privately, coordinate fixes, and
publish public details only after disclosure is appropriate.

{% if cookiecutter.security_measures.entries %}
## Security measures

{% for measure in cookiecutter.security_measures.entries %}
- {{ measure }}
{% endfor %}

{% endif %}
{% if cookiecutter.additional_security_measures %}
## Additional security measures

{{ cookiecutter.additional_security_measures }}

{% endif %}
{% if cookiecutter.sensitive_data_statement %}
## Sensitive data

{{ cookiecutter.sensitive_data_statement }}

{% endif %}
{% if cookiecutter.public_risk_notes %}
## Public risk notes

{{ cookiecutter.public_risk_notes }}

{% endif %}
{% if cookiecutter.dmp_reference %}
## Data management reference

{{ cookiecutter.dmp_reference }}
{% endif %}
