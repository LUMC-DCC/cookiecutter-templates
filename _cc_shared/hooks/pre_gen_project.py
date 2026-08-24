"""Check generator dependencies before Cookiecutter writes a project."""


def check_generator_dependencies():
    """Raise a concise error when required generator packages are unavailable.

    Raises
    ------
    RuntimeError
        If the RSM contract or reusable file package cannot be imported.
    """
    try:
        import rs_files_templates  # noqa: F401
        import rsm_schema  # noqa: F401
    except ImportError as error:
        raise RuntimeError(
            "Template generation requires the rsm-schema and "
            "rs-files-templates packages in the Cookiecutter environment."
        ) from error


if __name__ == "__main__":
    check_generator_dependencies()
