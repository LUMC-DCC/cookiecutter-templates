"""Typer command-line application for {{ (cookiecutter.project_name or cookiecutter.project_slug) }}.

The CLI adapter translates command-line input into calls to reusable project
services. Command modules stay small so they are easy to test separately from
terminal formatting.
"""

import typer

from {{ cookiecutter.project_slug }}.adapters.cli.commands import process

# The Typer app is the command registry. Add new commands by importing their
# modules and registering them below.
app = typer.Typer(help="{{ cookiecutter.project_short_description }}")
app.command(name="process")(process.command)


def main() -> None:
    """Run the command-line application."""
    app()
