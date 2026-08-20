"""Remove disabled optional scaffolds and template-only paths."""

from post_generation.documentation import (
    has_documentation,
    resolve_documentation_builder,
)
from post_generation.quality import has_pre_commit, has_quality_checks
from utils.context import entries
from utils.containerization import has_container_recipe, has_container_type
from utils.interfaces import (
    has_api_interface,
    has_cli_interface,
    has_desktop_interface,
    has_http_interface,
    has_ontology_interface,
    has_plugin_interface,
    has_portal_interface,
    has_processing_api_interface,
    has_script_interface,
    has_soap_interface,
    has_sparql_interface,
    has_suite_interface,
    has_web_interface,
    has_workflow_interface,
)
from utils.options import is_no
from utils.paths import remove_path
from utils.release import has_python_distribution


def lacks_test_type(ctx, test_type):
    """Return whether a generated project should omit one test type.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    test_type : str
        Canonical SMP test type label.

    Returns
    -------
    bool
        Whether the test type is not selected or tests are disabled.
    """
    return is_no(ctx, "include_tests") or test_type not in entries(ctx, "test_types")


def needs_python_project_setup(ctx):
    """Return whether any generated workflow needs the Python setup action.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.

    Returns
    -------
    bool
        Whether a selected workflow installs the generated Python project.
    """
    if ctx.get("language") != "python":
        return False

    _, documentation_builder = resolve_documentation_builder(ctx)
    builds_documentation = (
        has_documentation(ctx)
        and documentation_builder in {"mkdocs", "sphinx"}
    )
    checks_licenses = (
        not is_no(ctx, "license_compatibility_check")
        and bool(ctx.get("license", "").strip())
    )
    return any(
        (
            not is_no(ctx, "include_tests"),
            has_quality_checks(ctx),
            builds_documentation,
            checks_licenses,
            has_python_distribution(
                entries(ctx, "distribution_channels")
            ),
        )
    )


OPTIONAL_PATHS = [
    {
        "path": "docs",
        "should_remove": lambda ctx: not has_documentation(ctx),
    },
    {
        "path": "mkdocs.yml",
        "should_remove": lambda ctx: not has_documentation(ctx),
    },
    {
        "path": ".github/workflows/docs.yml",
        "should_remove": lambda ctx: not has_documentation(ctx),
    },
    {
        "path": "tests",
        "should_remove": lambda ctx: is_no(ctx, "include_tests"),
    },
    {
        "path": ".github/workflows/tests.yml",
        "should_remove": lambda ctx: is_no(ctx, "include_tests"),
    },
    {
        "path": "tests/test_smoke.py",
        "should_remove": lambda ctx: lacks_test_type(ctx, "Smoke tests"),
    },
    {
        "path": "tests/test_doctest.py",
        "should_remove": lambda ctx: lacks_test_type(ctx, "Doctests"),
    },
    {
        "path": "tests/test_unit.py",
        "should_remove": lambda ctx: lacks_test_type(ctx, "Unit tests"),
    },
    {
        "path": "tests/test_integration.py",
        "should_remove": lambda ctx: lacks_test_type(ctx, "Integration tests"),
    },
    {
        "path": "tests/test_system.py",
        "should_remove": lambda ctx: lacks_test_type(
            ctx,
            "System / end-to-end tests",
        ),
    },
    {
        "path": "tests/test_regression.py",
        "should_remove": lambda ctx: lacks_test_type(ctx, "Regression tests"),
    },
    {
        "path": "tests/test_property.py",
        "should_remove": lambda ctx: lacks_test_type(
            ctx,
            "Property-based / fuzz",
        ),
    },
    {
        "path": "tools/check_changelog.py",
        "should_remove": lambda ctx: is_no(ctx, "include_changelog"),
    },
    {
        "path": ".github/workflows/changelog.yml",
        "should_remove": lambda ctx: is_no(ctx, "include_changelog"),
    },
    {
        "path": ".github/workflows/license-compatibility.yml",
        "should_remove": lambda ctx: (
            is_no(ctx, "license_compatibility_check")
            or not ctx.get("license", "").strip()
        ),
    },
    {
        "path": ".github/workflows/quality.yml",
        "should_remove": lambda ctx: not has_quality_checks(ctx),
    },
    {
        "path": ".github/actions/setup-python-project",
        "should_remove": lambda ctx: not needs_python_project_setup(ctx),
    },
    {
        "path": ".github/workflows/containers.yml",
        "should_remove": lambda ctx: not has_container_recipe(
            entries(ctx, "containerization")
        ),
    },
    {
        "path": ".github/workflows/distribution.yml",
        "should_remove": lambda ctx: not has_python_distribution(
            entries(ctx, "distribution_channels")
        ),
    },
    {
        "path": ".pre-commit-config.yaml",
        "should_remove": lambda ctx: not has_pre_commit(ctx),
    },
    {
        "path": ".github/ISSUE_TEMPLATE",
        "should_remove": lambda ctx: is_no(ctx, "include_support"),
    },
    {
        "path": ".github/pull_request_template.md",
        "should_remove": lambda ctx: is_no(ctx, "include_contributing"),
    },
    {
        "path": "LICENSE.txt",
        "should_remove": lambda ctx: not ctx.get("license", "").strip(),
    },
    {
        "path": "Dockerfile",
        "should_remove": lambda ctx: not has_container_type(
            entries(ctx, "containerization"),
            "docker",
        ),
    },
    {
        "path": "Containerfile",
        "should_remove": lambda ctx: not has_container_type(
            entries(ctx, "containerization"),
            "oci",
        ),
    },
    {
        "path": ".dockerignore",
        "should_remove": lambda ctx: not (
            has_container_type(entries(ctx, "containerization"), "docker")
            or has_container_type(entries(ctx, "containerization"), "oci")
        ),
    },
    {
        "path": "Apptainer.def",
        "should_remove": lambda ctx: not has_container_type(
            entries(ctx, "containerization"),
            "apptainer",
        ),
    },
    {
        "path": "tools/check_release.py",
        "should_remove": lambda ctx: not has_python_distribution(
            entries(ctx, "distribution_channels")
        ),
    },
    {
        "path": "src/{project_slug}/adapters/api",
        "should_remove": lambda ctx: not has_api_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/api/routes/processing.py",
        "should_remove": lambda ctx: not has_processing_api_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/api/schemas.py",
        "should_remove": lambda ctx: not has_processing_api_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/api/routes/sparql.py",
        "should_remove": lambda ctx: not has_sparql_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/soap",
        "should_remove": lambda ctx: not has_soap_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/server.py",
        "should_remove": lambda ctx: not has_http_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/cli",
        "should_remove": lambda ctx: not has_cli_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/desktop",
        "should_remove": lambda ctx: not has_desktop_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/plugin",
        "should_remove": lambda ctx: not has_plugin_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/portal",
        "should_remove": lambda ctx: not has_portal_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/suite",
        "should_remove": lambda ctx: not has_suite_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters/web",
        "should_remove": lambda ctx: not has_web_interface(ctx),
    },
    {
        "path": "src/{project_slug}/adapters",
        "should_remove": lambda ctx: (
            not has_api_interface(ctx)
            and not has_soap_interface(ctx)
            and not has_cli_interface(ctx)
            and not has_desktop_interface(ctx)
            and not has_plugin_interface(ctx)
            and not has_portal_interface(ctx)
            and not has_suite_interface(ctx)
            and not has_web_interface(ctx)
        ),
    },
    {
        "path": "src/{project_slug}/ontology",
        "should_remove": lambda ctx: (
            not has_ontology_interface(ctx)
            and not has_sparql_interface(ctx)
        ),
    },
    {
        "path": "src/{project_slug}/workflows",
        "should_remove": lambda ctx: not has_workflow_interface(ctx),
    },
    {
        "path": "workflows",
        "should_remove": lambda ctx: not has_workflow_interface(ctx),
    },
    {
        "path": "scripts",
        "should_remove": lambda ctx: not has_script_interface(ctx),
    },
]

ALWAYS_REMOVE_PATHS = [
    ".template_hooks",
]

EMPTY_DIRECTORY_CANDIDATES = [
    "tools",
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    ".github",
]


def remove_optional_paths(ctx, cwd):
    """Remove optional generated paths disabled by context values.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    cwd : pathlib.Path
        Generated project root.
    """
    for entry in OPTIONAL_PATHS:
        if entry["should_remove"](ctx):
            rendered_path = entry["path"].format(**ctx)
            target = cwd / rendered_path
            remove_path(target)

    for rel_path in EMPTY_DIRECTORY_CANDIDATES:
        target = cwd / rel_path
        if target.exists() and target.is_dir() and not any(target.iterdir()):
            remove_path(target)


def remove_template_only_paths(cwd):
    """Remove paths that are only needed while rendering the template.

    Parameters
    ----------
    cwd : pathlib.Path
        Generated project root.
    """
    for rel_path in ALWAYS_REMOVE_PATHS:
        target = cwd / rel_path
        remove_path(target)
