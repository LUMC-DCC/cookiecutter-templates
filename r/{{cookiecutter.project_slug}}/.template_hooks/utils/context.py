"""Read structured values from the rendered Cookiecutter context."""


def entries(ctx, field_name):
    """Return entries from one structured repeatable context field.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    field_name : str
        Public contract field containing an ``entries`` list.

    Returns
    -------
    list
        Rendered entries, or an empty list for a missing or invalid field.
    """
    field = ctx.get(field_name, {})
    if not isinstance(field, dict):
        return []
    values = field.get("entries", [])
    return values if isinstance(values, list) else []


def normalize_choice(value):
    """Normalize one selector value for comparison.

    Parameters
    ----------
    value : object
        Raw selector value.

    Returns
    -------
    str
        Lowercase selector value without surrounding whitespace.
    """
    return str(value or "").strip().lower()


def template_default(ctx, field_name):
    """Return one template-specific default value.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    field_name : str
        Public contract field name.

    Returns
    -------
    object
        Configured template default, or ``None`` when absent.
    """
    defaults = ctx.get("_template_defaults", {})
    if not isinstance(defaults, dict):
        return None
    return defaults.get(field_name)


def template_supported_choices(ctx, field_name):
    """Return normalized choices supported by one template.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    field_name : str
        Public contract field name.

    Returns
    -------
    list[str]
        Supported choices in configured order.
    """
    supported = ctx.get("_template_supported_choices", {})
    if not isinstance(supported, dict):
        return []
    choices = supported.get(field_name, [])
    if not isinstance(choices, list):
        return []
    return [
        normalized
        for choice in choices
        if (normalized := normalize_choice(choice))
    ]


def resolve_choice(ctx, field_name, fallback="none"):
    """Resolve one selector against template-specific capabilities.

    Parameters
    ----------
    ctx : dict
        Rendered Cookiecutter context.
    field_name : str
        Public selector field name.
    fallback : str, default="none"
        Value used when neither the request nor template default is supported.

    Returns
    -------
    tuple[str, str]
        Requested and effective normalized selector values.
    """
    requested = normalize_choice(ctx.get(field_name))
    default = normalize_choice(template_default(ctx, field_name))
    supported = set(template_supported_choices(ctx, field_name))

    if requested in supported:
        return requested, requested
    if default in supported:
        return requested, default
    return requested, normalize_choice(fallback)
