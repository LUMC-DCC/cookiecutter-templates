"""Unit tests for reusable processing behavior."""

from {{ cookiecutter.project_slug }}.services.processing import make_upper, process_text


def test_process_text_returns_structured_result():
    """Ensure service processing preserves input and returns output."""
    result = process_text("abc")

    assert result.input_text == "abc"
    assert result.output_text == "ABC"


def test_make_upper_reuses_processing_service():
    """Ensure convenience helper follows service behavior."""
    assert make_upper("research") == "RESEARCH"
