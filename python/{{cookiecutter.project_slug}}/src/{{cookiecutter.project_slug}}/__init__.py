"""Public Python package for {{ cookiecutter.project_name }}.

The package exports the small public API that other Python code can import.
Implementation details live in named modules and subpackages such as
``services``.
"""

from {{ cookiecutter.project_slug }}.services.processing import (
    ProcessingResult,
    process_text,
)

__version__ = "{{ cookiecutter.version }}"

# Keep the public import surface explicit so downstream users can see which
# names are intended to be stable.
__all__ = [
    "ProcessingResult",
    "__version__",
    "process_text",
]
