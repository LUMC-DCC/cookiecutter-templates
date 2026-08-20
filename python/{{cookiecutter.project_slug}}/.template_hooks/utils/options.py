"""Interpret rendered Cookiecutter option values."""


def is_yes(ctx, value):
    """Check if a context value is a yes equivalent.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    value : str
        Context key to inspect.

    Returns
    -------
    bool
        Whether the value is truthy for template options.
    """
    return ctx.get(value, "").strip().lower() in (
        "yes", "y", "true", "1", "on", "enabled", "include"
    )


def is_no(ctx, value):
    """Check if a context value is a no equivalent.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    value : str
        Context key to inspect.

    Returns
    -------
    bool
        Whether the value is falsey for template options.
    """
    return ctx.get(value, "").strip().lower() in (
        "no", "n", "false", "0", "none", ""
    )
