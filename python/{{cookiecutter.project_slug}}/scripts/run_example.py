"""Standalone example script for {{ (cookiecutter.project_name or cookiecutter.project_slug) }}.

Scripts are useful for small one-off commands, tutorials, or demonstrations.
Keep reusable behavior in package modules and let scripts act as thin wrappers.
"""

import argparse

from {{ cookiecutter.project_slug }}.services.processing import process_text


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser for the script.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser.
    """
    parser = argparse.ArgumentParser(
        description="Run the {{ (cookiecutter.project_name or cookiecutter.project_slug) }} example script.",
    )
    # The optional positional argument keeps the script usable with no input
    # while still allowing callers to pass a custom text value.
    parser.add_argument(
        "text",
        nargs="?",
        default="{{ (cookiecutter.project_name or cookiecutter.project_slug) }}",
        help="Text to process.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the example script.

    Parameters
    ----------
    argv : list[str] | None, optional
        Command-line arguments without the script name.
    """
    args = build_parser().parse_args(argv)
    # Scripts should call package code rather than duplicating project logic.
    result = process_text(args.text)
    print(result.output_text)


if __name__ == "__main__":
    main()
