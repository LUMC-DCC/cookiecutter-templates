"""Executable module for ``python -m {{ cookiecutter.project_slug }}``.

Python runs this file when the package is executed as a module. The real entry
logic lives in ``main.py`` so it can also be imported and tested directly.
"""

from {{ cookiecutter.project_slug }}.main import main


if __name__ == "__main__":
    main()
