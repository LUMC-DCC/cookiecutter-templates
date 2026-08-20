"""Select generated metadata files and validation workflows."""

from utils.options import is_no
from utils.paths import remove_path


def select_metadata_files(ctx, cwd):
    """Remove citation metadata and its validator when CFF is disabled.

    The LUMC metadata profile requires both ``codemeta.json`` and
    ``CITATION.cff``. Projects that omit CFF keep CodeMeta but do not receive a
    CI workflow that could never pass the profile.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    cwd : pathlib.Path
        Generated project root.
    """
    if not is_no(ctx, "include_citation_cff"):
        return

    remove_path(cwd / "CITATION.cff")
    remove_path(cwd / ".github" / "workflows" / "metadata.yml")
