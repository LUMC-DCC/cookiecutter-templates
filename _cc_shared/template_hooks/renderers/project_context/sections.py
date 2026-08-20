"""Compose generated public project-context sections."""

from renderers.project_context.basic import (
    build_audience_section,
    build_funding_section,
    build_purpose_categories_section,
    build_purpose_section,
    build_related_software_section,
)
from renderers.project_context.interoperability import (
    build_external_dependencies_section,
    build_external_services_section,
    build_interfaces_section,
    build_operating_systems_section,
    build_programming_languages_section,
    build_software_functions_section,
)
from utils.context import entries


def build_project_context_sections(
    ctx,
    include_funding,
    include_interoperability=True,
):
    """Build public project context sections.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    include_funding : bool
        Whether to include funding acknowledgements.
    include_interoperability : bool, default=True
        Whether to include interoperability summaries.

    Returns
    -------
    str
        Combined Markdown sections.
    """
    sections = [
        build_purpose_section(ctx.get("purpose", "")),
        build_purpose_categories_section(entries(ctx, "purpose_categories")),
        build_audience_section(entries(ctx, "audiences")),
        build_related_software_section(entries(ctx, "related_software")),
    ]
    if include_interoperability:
        sections.extend(
            [
                build_programming_languages_section(
                    entries(ctx, "programming_languages")
                ),
                build_software_functions_section(entries(ctx, "software_functions")),
                build_interfaces_section(entries(ctx, "interfaces")),
                build_operating_systems_section(entries(ctx, "operating_systems")),
                build_external_dependencies_section(
                    entries(ctx, "external_dependencies")
                ),
                build_external_services_section(entries(ctx, "external_services")),
            ]
        )
    if include_funding:
        sections.append(build_funding_section(entries(ctx, "funding")))

    sections = [section for section in sections if section]
    if not sections:
        return ""

    return "\n\n" + "\n\n".join(sections) + "\n"
