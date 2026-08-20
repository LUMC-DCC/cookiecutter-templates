"""Resolve testing options for the selected language template."""

from utils.context import (
    entries,
    normalize_choice,
    template_default,
    template_supported_choices,
)
from utils.options import is_no


def resolve_test_framework(ctx):
    """Resolve a compatible testing framework.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.

    Returns
    -------
    tuple[str, str]
        Requested and effective testing framework labels.
    """
    defaults = [
        normalize_choice(framework)
        for framework in (template_default(ctx, "test_frameworks") or [])
        if normalize_choice(framework)
    ]
    supported = set(template_supported_choices(ctx, "test_frameworks"))
    requested = [
        normalize_choice(framework)
        for framework in entries(ctx, "test_frameworks")
        if normalize_choice(framework)
    ]
    default = defaults[0] if defaults else "pytest"

    for framework in requested:
        if framework in supported:
            return framework, framework

    requested_label = ", ".join(requested)
    return requested_label, default


def select_test_framework(ctx, cwd):
    """Warn when requested test frameworks are not compatible.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    cwd : pathlib.Path
        Generated project root.
    """
    del cwd
    if is_no(ctx, "include_tests"):
        return

    requested, effective = resolve_test_framework(ctx)
    if requested and requested != effective:
        print(
            "[warning] Test framework "
            f"{requested!r} is not supported for {ctx['language']!r}; "
            f"using the language default {effective!r}."
        )
