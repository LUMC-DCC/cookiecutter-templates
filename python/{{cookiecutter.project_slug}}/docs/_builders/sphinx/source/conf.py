"""Configure Sphinx from package and CodeMeta metadata."""

import json
import sys
from datetime import date
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODEMETA = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))

# Allow autodoc to import the package from an editable source checkout.
sys.path.insert(0, str(ROOT / "src"))

project = CODEMETA["name"]
author = CODEMETA.get("provider", {}).get("name", "")
copyright = f"{date.today().year}, {author}"
try:
    release = metadata.version("{{ cookiecutter.project_slug | replace('_', '-') }}")
except metadata.PackageNotFoundError:
    # Source checkouts can build docs before the package is installed.
    release = CODEMETA["version"]

extensions = [
    # Import docstrings from Python modules.
    "sphinx.ext.autodoc",
    # Render NumPy- and Google-style docstrings.
    "sphinx.ext.napoleon",
    # Link documented objects back to highlighted source code.
    "sphinx.ext.viewcode",
    # Allow Sphinx pages to be written in Markdown with MyST directives.
    "myst_parser",
]

exclude_patterns = []

html_theme = "sphinx_book_theme"
html_title = project
html_theme_options = {
    # Show nested headings in the right-hand page table of contents.
    "show_toc_level": 2,
    # Keep the starter theme quiet and focused.
    "use_download_button": False,
    "use_fullscreen_button": False,
}
repository_url = CODEMETA.get("codeRepository", "")
if repository_url and "REPLACE_WITH" not in repository_url:
    # Add a repository button when a public repository URL is available.
    html_theme_options["repository_url"] = repository_url
    html_theme_options["use_repository_button"] = True
