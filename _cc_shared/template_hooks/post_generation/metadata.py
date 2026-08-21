"""Select generated metadata files and validation workflows."""

from utils.options import is_no
from utils.paths import remove_path


def compact_citation_file(cwd):
    """Remove blank-only lines from rendered CFF metadata.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    """
    path = cwd / "CITATION.cff"
    if not path.exists():
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    compacted = [line for line in lines if line.strip()]
    path.write_text("\n".join(compacted) + "\n", encoding="utf-8")


def select_metadata_files(ctx, cwd):
    """Finalize citation metadata or remove it when CFF is disabled.

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
        compact_citation_file(cwd)
        return

    remove_path(cwd / "CITATION.cff")
    remove_path(cwd / ".github" / "workflows" / "metadata.yml")
