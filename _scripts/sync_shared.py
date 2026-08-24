"""Synchronize shared Cookiecutter assets into each language template.

Shared files live in ``_cc_shared`` and are copied into every template that has
a ``{{cookiecutter.project_slug}}`` project directory. Cookiecutter context
files are generated per template so language-specific defaults can differ.
"""

import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

from build_cookiecutter_context import build_context, load_policies, write_context

ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = ROOT / "_config" / "template_policies.json"
SHARED_CONTEXT_PATH = ROOT / "_cc_shared" / "cookiecutter.json"

TEMPLATE_DIRS = sorted(
    (
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and not path.name.startswith((".", "_"))
        and (path / "{{cookiecutter.project_slug}}").exists()
    ),
    key=lambda path: path.name,
)

RELATIVE_SYNC_MAP = {
    "hooks": "hooks",
    "template_hooks": "{{cookiecutter.project_slug}}/.template_hooks",
    "cookiecutter.json": "cookiecutter.json",
    ".github/ISSUE_TEMPLATE": "{{cookiecutter.project_slug}}/.github/ISSUE_TEMPLATE",
    ".github/dependabot.yml": "{{cookiecutter.project_slug}}/.github/dependabot.yml",
    ".github/pull_request_template.md": (
        "{{cookiecutter.project_slug}}/.github/pull_request_template.md"
    ),
    ".github/workflows/changelog.yml": (
        "{{cookiecutter.project_slug}}/.github/workflows/changelog.yml"
    ),
    ".github/workflows/metadata.yml": (
        "{{cookiecutter.project_slug}}/.github/workflows/metadata.yml"
    ),
    "tools/check_changelog.py": (
        "{{cookiecutter.project_slug}}/tools/check_changelog.py"
    ),
    "CONTRIBUTING.md": "{{cookiecutter.project_slug}}/CONTRIBUTING.md",
}

IGNORED_SYNC_NAMES = {
    ".DS_Store",
    "__pycache__",
}

IGNORED_SYNC_SUFFIXES = {
    ".pyc",
}

# Collect modified paths
MODIFIED_PATHS = []


def should_ignore(path: Path):
    """Check whether a source path should be excluded from sync.

    Parameters
    ----------
    path : pathlib.Path
        Source path candidate.

    Returns
    -------
    bool
        Whether the path should be ignored.
    """
    return path.name in IGNORED_SYNC_NAMES or path.suffix in IGNORED_SYNC_SUFFIXES


def sync_cookiecutter_context(policies, template_name: str, dst: Path):
    """Write one template-specific Cookiecutter context file.

    Parameters
    ----------
    policies : dict
        Parsed language-specific template policies.
    template_name : str
        Template name used to resolve template-specific defaults.
    dst : pathlib.Path
        Destination ``cookiecutter.json`` path.

    Returns
    -------
    bool
        Whether the context file changed.
    """
    if write_context(
        build_context(policies=policies, template=template_name),
        dst,
    ):
        MODIFIED_PATHS.append(dst)
        print(f"[sync] Generated Cookiecutter context for {template_name} → {dst}")
        return True
    return False


def remove_path(path: Path):
    """Remove a file or directory, retrying transient filesystem failures.

    Parameters
    ----------
    path : pathlib.Path
        Path to remove.
    """
    for attempt in range(3):
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
            return
        except FileNotFoundError:
            return
        except OSError:
            if attempt == 2:
                raise
            time.sleep(0.1)


def copy_file_if_changed(src: Path, dst: Path):
    """Copy a file only when destination content differs.

    Parameters
    ----------
    src : pathlib.Path
        Source file.
    dst : pathlib.Path
        Destination file.

    Returns
    -------
    bool
        Whether the destination file changed.
    """
    if dst.exists() and dst.is_file() and dst.read_bytes() == src.read_bytes():
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def sync_dir(src: Path, dst: Path):
    """Mirror one directory while preserving the destination root.

    Parameters
    ----------
    src : pathlib.Path
        Source directory.
    dst : pathlib.Path
        Destination directory.

    Returns
    -------
    bool
        Whether the destination directory changed.
    """
    changed = not dst.exists() or not dst.is_dir()

    if dst.exists() and not dst.is_dir():
        remove_path(dst)

    dst.mkdir(parents=True, exist_ok=True)

    src_entries = {entry.name for entry in src.iterdir() if not should_ignore(entry)}
    for dst_entry in dst.iterdir():
        if dst_entry.name not in src_entries:
            remove_path(dst_entry)
            changed = True

    for src_entry in src.iterdir():
        if should_ignore(src_entry):
            continue
        changed = sync_path(src_entry, dst / src_entry.name) or changed

    return changed


def sync_path(src: Path, dst: Path):
    """Synchronize one file or directory.

    Parameters
    ----------
    src : pathlib.Path
        Source path.
    dst : pathlib.Path
        Destination path.

    Returns
    -------
    bool
        Whether the destination path changed.
    """
    if should_ignore(src):
        return False

    if src.is_file():
        if dst.exists() and dst.is_dir():
            remove_path(dst)
        if copy_file_if_changed(src, dst):
            MODIFIED_PATHS.append(dst)
            print(f"[sync] Synced {src} → {dst}")
            return True
        return False
    elif src.is_dir():
        if sync_dir(src, dst):
            MODIFIED_PATHS.append(dst)
            print(f"[sync] Synced {src} → {dst}")
            return True
        return False
    else:
        print(f"[warning] Unknown source type: {src}")
        return False


def main():
    """Run synchronization for every discovered language template."""
    MODIFIED_PATHS.clear()
    policies = load_policies(POLICY_PATH)
    if write_context(build_context(policies=policies), SHARED_CONTEXT_PATH):
        MODIFIED_PATHS.append(SHARED_CONTEXT_PATH)

    seen = set()
    for template_dir in TEMPLATE_DIRS:
        for rel_src, rel_dst in RELATIVE_SYNC_MAP.items():
            src = ROOT / "_cc_shared" / rel_src
            dst = template_dir / rel_dst
            key = (str(src), str(dst))

            if key in seen:
                continue
            seen.add(key)

            if rel_src == "cookiecutter.json":
                sync_cookiecutter_context(policies, template_dir.name, dst)
            else:
                sync_path(src, dst)

    for path in MODIFIED_PATHS:
        print(f"[modified]{path}")


if __name__ == "__main__":
    main()
