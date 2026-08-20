"""Populate MkDocs configuration from generated project metadata."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEMETA_PATH = ROOT / "codemeta.json"


def load_codemeta():
    """Load public project metadata.

    Returns
    -------
    dict
        Parsed CodeMeta document.
    """
    return json.loads(CODEMETA_PATH.read_text(encoding="utf-8"))


def on_config(config):
    """Apply CodeMeta values to MkDocs configuration.

    Parameters
    ----------
    config : mkdocs.config.defaults.MkDocsConfig
        Mutable MkDocs configuration.

    Returns
    -------
    mkdocs.config.defaults.MkDocsConfig
        Updated configuration.
    """
    codemeta = load_codemeta()
    config["site_name"] = codemeta["name"]
    config["site_description"] = codemeta.get("description", "")

    repository_url = codemeta.get("codeRepository", "")
    if repository_url:
        config["repo_url"] = repository_url
        config["repo_name"] = repository_url.rstrip("/").rsplit("/", 1)[-1]

    return config
