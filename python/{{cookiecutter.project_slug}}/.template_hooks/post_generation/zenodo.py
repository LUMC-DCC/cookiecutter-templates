"""Generate Zenodo GitHub-release metadata from public project context."""

import json
import re

from utils.context import entries


def uses_zenodo(ctx):
    """Return whether Zenodo is a selected distribution channel.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.

    Returns
    -------
    bool
        Whether the project plans to archive releases in Zenodo.
    """
    return any(
        " ".join(str(channel).strip().lower().split()) == "zenodo"
        for channel in entries(ctx, "distribution_channels")
    )


def person_identity(person):
    """Build a stable best-effort identity for deduplication.

    Parameters
    ----------
    person : dict
        Public person record.

    Returns
    -------
    str
        Normalized ORCID, email, or name identity.
    """
    for field in ("orcid", "email"):
        value = str(person.get(field, "")).strip().lower()
        if value:
            return f"{field}:{value.removeprefix('https://orcid.org/')}"
    name = str(person.get("name", "")).strip() or " ".join(
        part
        for part in (
            str(person.get("given_names", "")).strip(),
            str(person.get("family_names", "")).strip(),
        )
        if part
    )
    return f"name:{name.lower()}"


def zenodo_person(person, contributor_type=""):
    """Map one contract person to legacy Zenodo deposit metadata.

    Parameters
    ----------
    person : dict
        Public person record.
    contributor_type : str, optional
        Zenodo contributor role.

    Returns
    -------
    dict
        Zenodo creator or contributor record.
    """
    given_names = str(person.get("given_names", "")).strip()
    family_names = str(person.get("family_names", "")).strip()
    if family_names:
        name = f"{family_names}, {given_names}" if given_names else family_names
    else:
        name = str(person.get("name", "")).strip() or "Project member"

    record = {"name": name}
    affiliation = person.get("affiliation", {})
    if isinstance(affiliation, dict) and affiliation.get("name"):
        record["affiliation"] = affiliation["name"]
    orcid = str(person.get("orcid", "")).strip()
    if orcid:
        record["orcid"] = orcid.removeprefix("https://orcid.org/")
    if contributor_type:
        record["type"] = contributor_type
    return record


def zenodo_contributors(ctx, creator_identities):
    """Build non-author maintainer and project-leader records.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    creator_identities : set[str]
        Identities already represented as creators.

    Returns
    -------
    list[dict]
        Deduplicated Zenodo contributor records.
    """
    contributors = []
    seen = set(creator_identities)
    groups = (
        (entries(ctx, "maintainers"), "ContactPerson"),
        (entries(ctx, "principal_investigators"), "ProjectLeader"),
    )
    for people, contributor_type in groups:
        for person in people:
            identity = person_identity(person)
            if identity in seen:
                continue
            contributors.append(zenodo_person(person, contributor_type))
            seen.add(identity)
    return contributors


def zenodo_related_identifiers(ctx):
    """Map publication identifiers to Zenodo relationships.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.

    Returns
    -------
    list[dict]
        Zenodo related-identifier records.
    """
    related = []
    seen = set()
    for publication in entries(ctx, "publications"):
        doi = str(publication.get("doi", "")).strip()
        url = str(publication.get("url", "")).strip()
        identifier = doi or url
        if not identifier or identifier in seen:
            continue
        record = {
            "identifier": identifier,
            "relation": "isDocumentedBy",
        }
        if doi:
            record["scheme"] = "doi"
            record["resource_type"] = "publication-article"
        else:
            record["scheme"] = "url"
        related.append(record)
        seen.add(identifier)
    return related


def zenodo_grants(ctx):
    """Map recognized Zenodo grant identifiers to grant records.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.

    Returns
    -------
    list[dict]
        Deduplicated Zenodo grant identifiers. Free-form local award numbers
        are omitted because Zenodo resolves grant identifiers against its
        controlled grant catalogue.
    """
    grant_ids = []
    for funding in entries(ctx, "funding"):
        grant_id = str(
            funding.get("award_number") or funding.get("project_code") or ""
        ).strip()
        is_zenodo_id = bool(re.fullmatch(r"\d+|10\.13039/[^\s:]+::\S+", grant_id))
        if is_zenodo_id and grant_id not in grant_ids:
            grant_ids.append(grant_id)
    return [{"id": grant_id} for grant_id in grant_ids]


def build_zenodo_metadata(ctx, spdx_id=None):
    """Build legacy Zenodo GitHub integration metadata.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    spdx_id : str or None, optional
        SPDX identifier confirmed while generating the license file.

    Returns
    -------
    dict
        JSON-serializable Zenodo metadata.
    """
    authors = entries(ctx, "authors")
    creators = [zenodo_person(author) for author in authors]
    if not creators:
        creators = [{"name": ctx.get("organization_name") or "Project team"}]
    creator_identities = {person_identity(author) for author in authors}

    metadata = {
        "title": ctx.get("project_name", "Research software project"),
        "description": (
            ctx.get("project_long_description")
            or ctx.get("project_short_description")
            or "Research software project."
        ),
        "creators": creators,
        "version": ctx.get("version", "0.1.0"),
        "upload_type": "software",
        "access_right": "open",
    }
    optional_values = {
        "contributors": zenodo_contributors(ctx, creator_identities),
        "keywords": entries(ctx, "keywords"),
        "grants": zenodo_grants(ctx),
        "related_identifiers": zenodo_related_identifiers(ctx),
    }
    for field, value in optional_values.items():
        if value:
            metadata[field] = value
    if spdx_id:
        metadata["license"] = spdx_id
    return metadata


def select_zenodo_metadata(ctx, cwd, spdx_id=None):
    """Write Zenodo metadata when the distribution channel is selected.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    cwd : pathlib.Path
        Generated project root.
    spdx_id : str or None, optional
        SPDX identifier confirmed while generating the license file.
    """
    if not uses_zenodo(ctx):
        return

    path = cwd / ".zenodo.json"
    path.write_text(
        json.dumps(
            build_zenodo_metadata(ctx, spdx_id),
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
