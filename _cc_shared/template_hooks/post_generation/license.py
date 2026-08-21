"""Create generated license files and license metadata."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from utils.paths import remove_path


DEFAULT_SPDX_LICENSE_API_BASE = "https://spdx.org/licenses"


class SPDXLicenseFetchError(Exception):
    """Raised when SPDX license metadata cannot be fetched or used."""


class SPDXLicenseNotFoundError(SPDXLicenseFetchError):
    """Raised when SPDX has no record for a requested identifier."""


def license_json_url(spdx_id, base_url=None):
    """Build the SPDX per-license JSON URL.

    Parameters
    ----------
    spdx_id : str
        SPDX license identifier.
    base_url : str, optional
        Base URL for SPDX license JSON records.

    Returns
    -------
    str
        Per-license SPDX JSON URL.
    """
    base = (base_url or DEFAULT_SPDX_LICENSE_API_BASE).rstrip("/")
    return f"{base}/{quote(spdx_id, safe='.-+')}.json"


def fetch_spdx_license(spdx_id, base_url=None):
    """Fetch one SPDX license JSON record.

    Parameters
    ----------
    spdx_id : str
        SPDX license identifier.
    base_url : str, optional
        Base URL for SPDX license JSON records.

    Returns
    -------
    dict
        SPDX license JSON payload.

    Raises
    ------
    SPDXLicenseNotFoundError
        If SPDX has no record for ``spdx_id``.
    SPDXLicenseFetchError
        If the SPDX service fails or returns an invalid record.
    """
    url = license_json_url(spdx_id, base_url)
    try:
        with urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code == 404:
            raise SPDXLicenseNotFoundError(
                f"SPDX has no license record for {spdx_id!r}"
            ) from error
        msg = f"Could not fetch SPDX license JSON from {url}"
        raise SPDXLicenseFetchError(msg) from error
    except URLError as error:
        if isinstance(error.reason, FileNotFoundError):
            raise SPDXLicenseNotFoundError(
                f"SPDX has no license record for {spdx_id!r}"
            ) from error
        msg = f"Could not fetch SPDX license JSON from {url}"
        raise SPDXLicenseFetchError(msg) from error
    except (OSError, TimeoutError, json.JSONDecodeError) as error:
        msg = f"Could not fetch SPDX license JSON from {url}"
        raise SPDXLicenseFetchError(msg) from error

    license_id = payload.get("licenseId")
    if license_id != spdx_id:
        raise SPDXLicenseFetchError(
            f"SPDX license JSON from {url} returned licenseId {license_id!r}"
        )
    if not payload.get("licenseText"):
        raise SPDXLicenseFetchError(
            f"SPDX license JSON from {url} does not include licenseText"
        )

    return payload


def render_license_text(record):
    """Render SPDX license text for ``LICENSE.txt``.

    Parameters
    ----------
    record : dict
        SPDX license JSON payload.

    Returns
    -------
    str
        License file content.
    """
    text = record["licenseText"].strip()
    return f"{text}\n"


def render_custom_license_text(license_value):
    """Render custom license text for ``LICENSE.txt``.

    Parameters
    ----------
    license_value : str
        Non-SPDX license value from the rendered context.

    Returns
    -------
    str
        Custom license file content.
    """
    text = license_value.strip()
    return f"{text}\n"


def update_pyproject_license(cwd, spdx_id):
    """Insert or remove Python package license metadata.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    spdx_id : str or None
        Recognized SPDX identifier, or ``None`` to omit package license metadata.
    """
    path = cwd / "pyproject.toml"
    if not path.exists():
        return

    lines = []
    in_project = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("["):
            in_project = line == "[project]"
        if in_project and line.startswith("license = "):
            continue
        lines.append(line)

    if spdx_id:
        for index, line in enumerate(lines):
            if line.startswith("requires-python = "):
                lines.insert(index + 1, f"license = {json.dumps(spdx_id)}")
                break

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_pyproject_array_block(lines, assignment):
    """Remove a generated TOML array assignment block.

    Parameters
    ----------
    lines : list[str]
        TOML lines.
    assignment : str
        Assignment prefix to remove, such as ``"license = ["``.

    Returns
    -------
    list[str]
        TOML lines with the generated block removed.
    """
    updated = []
    index = 0
    while index < len(lines):
        if lines[index].startswith(assignment):
            index += 1
            while index < len(lines) and lines[index] != "]":
                index += 1
            if index < len(lines):
                index += 1
            continue

        updated.append(lines[index])
        index += 1

    return updated


def remove_pyproject_section(lines, section_name):
    """Remove a generated TOML section.

    Parameters
    ----------
    lines : list[str]
        TOML lines.
    section_name : str
        Section header to remove, such as ``"[tool.licensecheck]"``.

    Returns
    -------
    list[str]
        TOML lines with the generated section removed.
    """
    updated = []
    index = 0
    while index < len(lines):
        if lines[index] == section_name:
            index += 1
            while index < len(lines) and not lines[index].startswith("["):
                index += 1
            continue

        updated.append(lines[index])
        index += 1

    return updated


def remove_pyproject_licensecheck(cwd):
    """Remove Python license compatibility checker configuration.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    """
    path = cwd / "pyproject.toml"
    if not path.exists():
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    lines = remove_pyproject_array_block(lines, "license = [")
    lines = remove_pyproject_section(lines, "[tool.licensecheck]")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def remove_license_compatibility_workflow(cwd):
    """Remove generated dependency license compatibility checks.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    """
    remove_path(cwd / ".github" / "workflows" / "license-compatibility.yml")
    remove_pyproject_licensecheck(cwd)


def update_codemeta_license(cwd, license_value, spdx_id=None):
    """Insert or remove CodeMeta license metadata.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    license_value : str or None
        License text supplied to the template, or ``None`` to retain the
        generated mandatory-field placeholder.
    spdx_id : str or None, optional
        Recognized SPDX identifier.
    """
    path = cwd / "codemeta.json"
    if not path.exists():
        return

    data = json.loads(path.read_text(encoding="utf-8"))
    if spdx_id:
        data["license"] = f"https://spdx.org/licenses/{spdx_id}"
    elif license_value:
        data["license"] = {
            "@type": "CreativeWork",
            "name": "Custom license",
            "text": license_value,
        }
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def update_citation_license(cwd, spdx_id):
    """Insert or remove CFF license metadata.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    spdx_id : str or None
        Recognized SPDX identifier, or ``None`` to omit CFF license metadata.
    """
    path = cwd / "CITATION.cff"
    if not path.exists():
        return

    lines = [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.startswith("license: ")
    ]
    if spdx_id:
        for index, line in enumerate(lines):
            if line.startswith("abstract: "):
                lines.insert(index + 1, f"license: {json.dumps(spdx_id)}")
                break

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_container_license(cwd, spdx_id):
    """Insert an OCI-compatible SPDX license label into container recipes.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    spdx_id : str or None
        Recognized SPDX identifier, or ``None`` to omit the label.
    """
    for file_name in ("Containerfile", "Dockerfile"):
        path = cwd / file_name
        if not path.exists():
            continue
        lines = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if not line.startswith("LABEL org.opencontainers.image.licenses=")
        ]
        if spdx_id:
            runtime_index = lines.index("FROM python:3.12-slim AS runtime")
            lines.insert(
                runtime_index + 1,
                "LABEL org.opencontainers.image.licenses=" + json.dumps(spdx_id),
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    apptainer_path = cwd / "Apptainer.def"
    if not apptainer_path.exists():
        return
    lines = [
        line
        for line in apptainer_path.read_text(encoding="utf-8").splitlines()
        if not line.strip().startswith("org.opencontainers.image.licenses ")
    ]
    if spdx_id:
        labels_index = lines.index("%labels")
        lines.insert(
            labels_index + 1,
            f"    org.opencontainers.image.licenses {spdx_id}",
        )
    apptainer_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_license_metadata(cwd, license_value, spdx_id=None):
    """Update machine-readable license metadata.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    license_value : str or None
        License text supplied to the template, or ``None`` when absent.
    spdx_id : str or None, optional
        Recognized SPDX identifier.
    """
    update_pyproject_license(cwd, spdx_id)
    update_codemeta_license(cwd, license_value, spdx_id)
    update_citation_license(cwd, spdx_id)
    update_container_license(cwd, spdx_id)
    if not spdx_id:
        remove_license_compatibility_workflow(cwd)


def update_license_file(ctx, cwd):
    """Create or remove the generated project license file.

    Empty license values remove ``LICENSE.txt``. Recognized SPDX identifiers
    write canonical SPDX text and machine-readable license metadata.
    Unrecognized values are written as custom license text.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    cwd : pathlib.Path
        Generated project root.
    """
    license_path = cwd / "LICENSE.txt"
    license_value = ctx.get("license", "").strip()
    if not license_value:
        remove_path(license_path)
        update_license_metadata(cwd, None)
        return

    base_url = os.environ.get("SPDX_LICENSE_API_BASE", DEFAULT_SPDX_LICENSE_API_BASE)
    try:
        record = fetch_spdx_license(license_value, base_url)
    except SPDXLicenseNotFoundError as error:
        print(f"[warning] {error}")
        license_path.write_text(
            render_custom_license_text(license_value),
            encoding="utf-8",
        )
        update_license_metadata(cwd, license_value)
        return

    license_path.write_text(render_license_text(record), encoding="utf-8")
    update_license_metadata(cwd, license_value, record["licenseId"])
