"""Smoke tests for the generated Python package."""

from {{ cookiecutter.project_slug }} import __version__, process_text
from {{ cookiecutter.project_slug }}.main import main


def test_package_has_version():
    """Ensure the package exposes the generated version."""
    assert __version__ == "{{ (cookiecutter.versioning.version or "0.1.0") }}"


def test_main_is_callable():
    """Ensure the runtime entry point can be imported."""
    assert callable(main)


def test_library_api_processes_text():
    """Ensure reusable service logic is available from the package API."""
    result = process_text("example")

    assert result.input_text == "example"
    assert result.output_text == "EXAMPLE"
