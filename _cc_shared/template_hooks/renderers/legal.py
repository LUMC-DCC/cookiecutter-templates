"""Build generated legal and licensing text."""


def build_license_label(license_value):
    """Build a human-readable license label.

    Parameters
    ----------
    license_value : str
        SPDX license identifier, custom license text, or an empty string.

    Returns
    -------
    str
        Markdown label for the selected license.
    """
    value = license_value.strip()
    if "\n" in value or " " in value:
        return "the custom terms in `LICENSE.txt`"

    return f"`{value}`"


def build_legal_lines(license_value, compatibility_notes):
    """Build generated legal and licensing lines.

    Parameters
    ----------
    license_value : str
        SPDX license identifier, custom license text, or an empty string.
    compatibility_notes : str
        Public notes about license compatibility.

    Returns
    -------
    list[str]
        Human-readable legal and licensing paragraphs.
    """
    lines = []
    if license_value.strip():
        label = build_license_label(license_value)
        lines.append(
            f"This project is licensed under {label}. "
            "See `LICENSE.txt` for the full license text."
        )
    if compatibility_notes:
        lines.append(compatibility_notes)

    return lines


def build_legal_section(license_value, compatibility_notes):
    """Build the generated legal and licensing section.

    Parameters
    ----------
    license_value : str
        SPDX license identifier, custom license text, or an empty string.
    compatibility_notes : str
        Public notes about license compatibility.

    Returns
    -------
    str
        Markdown section, or an empty string.
    """
    lines = build_legal_lines(license_value, compatibility_notes)
    if not lines:
        return ""

    return "## Legal and Licensing\n\n" + "\n\n".join(lines)


def build_legal_page_content(license_value, compatibility_notes):
    """Build content for the generated legal documentation page.

    Parameters
    ----------
    license_value : str
        SPDX license identifier, custom license text, or an empty string.
    compatibility_notes : str
        Public notes about license compatibility.

    Returns
    -------
    str
        Markdown content to append to a legal documentation page.
    """
    lines = build_legal_lines(license_value, compatibility_notes)
    if not lines:
        lines = ["No project license has been selected yet."]

    return "\n\n" + "\n\n".join(lines) + "\n"
