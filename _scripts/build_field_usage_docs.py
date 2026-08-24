"""Build the field usage reference page from the usage map.

The generated Markdown page keeps human-facing documentation in sync with the
curated implementation map in ``_contracts/field_usage.json``.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USAGE_PATH = ROOT / "_contracts" / "field_usage.json"
DEFAULT_OUTPUT_PATH = ROOT / "_docs" / "contract" / "field-usage.md"


def markdown_escape(value):
    """Escape table-sensitive Markdown characters.

    Parameters
    ----------
    value : object
        Value to render in a Markdown table cell.

    Returns
    -------
    str
        Escaped single-line Markdown text.
    """
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_table(usage):
    """Render the field usage map as a Markdown table.

    Parameters
    ----------
    usage : dict
        Parsed field usage map.

    Returns
    -------
    str
        Markdown document content.
    """
    templates = list(usage["templates"])
    status_headers = [f"{template.title()} Status" for template in templates]
    lines = [
        "# Field Usage",
        "",
        "This table is generated from `_contracts/field_usage.json`.",
        "Update the usage map first, then regenerate this page.",
        "",
        "| Field | " + " | ".join(status_headers) + " | Targets | Notes |",
        "| --- | " + " | ".join("---" for _ in status_headers) + " | --- | --- |",
    ]

    for field in usage["fields"]:
        targets = ", ".join(f"`{target}`" for target in field["targets"])
        statuses = [
            f"`{markdown_escape(field['statuses'][template])}`"
            for template in templates
        ]
        lines.append(
            "| {name} | {statuses} | {targets} | {notes} |".format(
                name=f"`{markdown_escape(field['name'])}`",
                statuses=" | ".join(statuses),
                targets=markdown_escape(targets),
                notes=markdown_escape(field["notes"]),
            )
        )

    lines.append("")
    return "\n".join(lines)


def load_usage(path):
    """Load a field usage map from disk.

    Parameters
    ----------
    path : pathlib.Path
        JSON usage map path.

    Returns
    -------
    dict
        Parsed usage map.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def write_docs(content, path):
    """Write generated documentation content.

    Parameters
    ----------
    content : str
        Markdown content to write.
    path : pathlib.Path
        Destination documentation path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--usage", type=Path, default=DEFAULT_USAGE_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    write_docs(build_table(load_usage(args.usage)), args.output)


if __name__ == "__main__":
    main()
