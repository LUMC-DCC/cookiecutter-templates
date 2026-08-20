{% macro person_label(person) -%}
{%- if person.name is defined and person.name -%}
{{ person.name }}
{%- else -%}
{%- set given_names = person.given_names if person.given_names is defined else "" -%}
{%- set family_names = person.family_names if person.family_names is defined else "" -%}
{{ (given_names ~ " " ~ family_names) | trim or "Project member" }}
{%- endif -%}
{%- endmacro -%}
# Governance

{% if cookiecutter.governance_notes -%}
{{ cookiecutter.governance_notes }}

{% endif -%}
## Roles

{% if cookiecutter.maintainers.entries -%}
Maintainers are responsible for day-to-day project decisions, review, releases,
and support:

{% for maintainer in cookiecutter.maintainers.entries -%}
- {{ person_label(maintainer) }}{% if maintainer.email is defined and maintainer.email %} <{{ maintainer.email }}>{% endif %}{% if maintainer.affiliation is defined and maintainer.affiliation %}, {{ maintainer.affiliation }}{% endif %}
{% endfor %}

{% else -%}
Maintainers are responsible for day-to-day project decisions, review, releases,
and support.

{% endif -%}
{% if cookiecutter.principal_investigators.entries -%}
Principal investigators provide scientific or institutional oversight:

{% for principal_investigator in cookiecutter.principal_investigators.entries -%}
- {{ person_label(principal_investigator) }}{% if principal_investigator.email is defined and principal_investigator.email %} <{{ principal_investigator.email }}>{% endif %}{% if principal_investigator.affiliation is defined and principal_investigator.affiliation %}, {{ principal_investigator.affiliation }}{% endif %}
{% endfor %}

{% endif -%}
## Decision making

Routine decisions are made by maintainer consensus. Larger changes, releases,
governance changes, and changes that affect users should be discussed in a pull
request or issue before implementation.

When consensus is not possible, maintainers should document the disagreement,
choose the lowest-risk option for users, and escalate to project leadership or
institutional support when needed.

## Release responsibility

Maintainers decide when a release is ready, confirm that checks pass, update the
changelog, and publish release metadata.

{% if cookiecutter.continuity_plan -%}
## Continuity

{{ cookiecutter.continuity_plan }}

{% endif -%}
{% if cookiecutter.retirement_criteria.entries -%}
## Retirement

The project may be retired when one or more of these conditions apply:

{% for criterion in cookiecutter.retirement_criteria.entries -%}
- {{ criterion }}
{% endfor %}
{% endif -%}
