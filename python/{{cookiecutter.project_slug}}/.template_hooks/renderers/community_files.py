"""Select explicitly requested community files."""

from utils.options import is_yes


COMMUNITY_FILE_FIELDS = {
    "include_changelog": "CHANGELOG.md",
    "include_code_of_conduct": "CODE_OF_CONDUCT.md",
    "include_contributing": "CONTRIBUTING.md",
    "include_governance": "GOVERNANCE.md",
    "include_security": "SECURITY.md",
    "include_support": "SUPPORT.md",
}


def selected_community_files(ctx):
    """Return selected community files in stable order.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.

    Returns
    -------
    set[str]
        Repository paths selected by explicit context fields.
    """
    return {
        rel_path
        for field_name, rel_path in COMMUNITY_FILE_FIELDS.items()
        if is_yes(ctx, field_name)
    }


def all_community_files():
    """Return all supported community file paths.

    Returns
    -------
    set[str]
        Repository paths controlled by explicit community-file fields.
    """
    return set(COMMUNITY_FILE_FIELDS.values())
