"""Build Cookiecutter contexts from the public contract.

The contract is the maintained source of truth. This script renders
Cookiecutter-compatible JSON files, optionally applying template-specific
defaults for fields whose preferred default differs by language.
"""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTRACT_PATH = ROOT / "_contracts" / "template_context.json"
DEFAULT_OUTPUT_PATH = ROOT / "_cc_shared" / "cookiecutter.json"


def resolve_default(field, template=None):
    """Resolve the default value for one field.

    Parameters
    ----------
    field : dict
        Field definition from the context contract.
    template : str, optional
        Template name, such as ``python`` or ``r``.

    Returns
    -------
    object
        Template-specific default when available, otherwise the field default.
    """
    if template:
        template_defaults = field.get("template_defaults", {})
        if template in template_defaults:
            return template_defaults[template]

    return field.get("default")


def resolve_supported_choices(field, template=None):
    """Resolve supported choices for one template.

    Parameters
    ----------
    field : dict
        Field definition from the context contract.
    template : str, optional
        Template name used to resolve language-specific supported choices.

    Returns
    -------
    list
        Template-specific supported choices when available, otherwise global choices.
    """
    if template:
        template_supported_choices = field.get("template_supported_choices", {})
        if template in template_supported_choices:
            return list(template_supported_choices[template])

    if "choices" in field:
        return list(field["choices"])

    return list(field.get("item_schema", {}).get("enum", []))


def order_choices(field, template=None):
    """Return Cookiecutter choices with the default first.

    Parameters
    ----------
    field : dict
        Choice field definition from the context contract.
    template : str, optional
        Template name used to resolve language-specific defaults.

    Returns
    -------
    list
        Ordered choice values.
    """
    choices = list(field["choices"])
    default = resolve_default(field, template)

    if default is None:
        return choices
    if default not in choices:
        raise ValueError(
            f"Default {default!r} is not a valid choice for {field['name']!r}"
        )

    return [default, *[choice for choice in choices if choice != default]]


def build_template_metadata(contract, template=None):
    """Build private metadata consumed by post-generation hooks.

    Parameters
    ----------
    contract : dict
        Parsed contract document.
    template : str, optional
        Template name used to resolve language-specific metadata.

    Returns
    -------
    dict
        Private Cookiecutter metadata.
    """
    metadata = {
        "_template_defaults": {},
        "_template_schemas": {},
        "_template_supported_choices": {},
    }

    if not template:
        return metadata

    for field in contract["fields"]:
        name = field["name"]

        if "template_defaults" in field:
            metadata["_template_defaults"][name] = resolve_default(field, template)

        if template in field.get("template_schemas", {}):
            metadata["_template_schemas"][name] = field["template_schemas"][template]

        if "template_supported_choices" in field:
            metadata["_template_supported_choices"][name] = resolve_supported_choices(
                field,
                template,
            )

    return metadata


def build_context(contract, template=None):
    """Render Cookiecutter defaults from a template context contract.

    Parameters
    ----------
    contract : dict
        Parsed contract document from ``_contracts/template_context.json``.
    template : str, optional
        Template name used to apply language-specific defaults.

    Returns
    -------
    dict
        Cookiecutter context, including ``__prompts__`` when prompts exist.
    """
    context = {}
    prompts = {}

    for field in contract["fields"]:
        name = field["name"]
        field_type = field["type"]

        if field_type == "choice":
            context[name] = order_choices(field, template)
        elif field_type == "string":
            context[name] = resolve_default(field, template) or ""
        elif field_type in {"object_array", "string_array"}:
            context[name] = {"entries": resolve_default(field, template) or []}
        else:
            raise ValueError(f"Unsupported context field type: {field_type}")

        if field.get("prompt"):
            prompts[name] = field["prompt"]

    if prompts:
        context["__prompts__"] = prompts

    # Apply whitespace control consistently across every text template.
    context["_jinja2_env_vars"] = {
        "lstrip_blocks": True,
        "trim_blocks": True,
    }
    context.update(build_template_metadata(contract, template))

    return context


def load_contract(path):
    """Load a context contract from disk.

    Parameters
    ----------
    path : pathlib.Path
        JSON contract path.

    Returns
    -------
    dict
        Parsed contract data.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def write_context(context, path):
    """Write a generated Cookiecutter context file.

    Parameters
    ----------
    context : dict
        Cookiecutter context data.
    path : pathlib.Path
        Destination JSON path.

    Returns
    -------
    bool
        Whether the file content changed.
    """
    content = json.dumps(context, indent=2, ensure_ascii=False) + "\n"

    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False

    path.write_text(content, encoding="utf-8")
    return True


def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--template")
    args = parser.parse_args()

    write_context(
        build_context(load_contract(args.contract), template=args.template),
        args.output,
    )


if __name__ == "__main__":
    main()
