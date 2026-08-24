"""Runtime entry point for ``python -m {{ cookiecutter.project_slug }}``.

This module provides a tiny package-level command for quick smoke tests. Keep
larger runtime interfaces in dedicated modules.
"""

from {{ cookiecutter.project_slug }}.services.processing import process_text


def main(text: str = "{{ (cookiecutter.project_name or cookiecutter.project_slug) }}") -> None:
    """Run the package entry point.

    Parameters
    ----------
    text : str, default="{{ (cookiecutter.project_name or cookiecutter.project_slug) }}"
        Text to process.
    """
    # Delegate to the service layer so the entry point stays small and
    # testable.
    result = process_text(text)
    print(result.output_text)


if __name__ == "__main__":
    main()
