"""Build an integrator-facing JSON Schema from the context contract.

The maintained contract remains ``_contracts/template_context.json``. This
script renders a strict JSON Schema that services can use to validate
Cookiecutter ``extra_context`` payloads before calling a template.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTRACT_PATH = ROOT / "_contracts" / "template_context.json"
DEFAULT_OUTPUT_PATH = ROOT / "_contracts" / "template_context.schema.json"


def with_common_metadata(field: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """Add description and default metadata to one field schema.

    Parameters
    ----------
    field : dict
        Field definition from the context contract.
    schema : dict
        JSON Schema fragment for the field.

    Returns
    -------
    dict
        JSON Schema fragment with shared metadata.
    """
    schema = copy.deepcopy(schema)
    if field.get("description"):
        schema["description"] = field["description"]
    if "default" in field:
        schema["default"] = field["default"]
    return schema


def entries_schema(field: dict[str, Any], item_schema: dict[str, Any]) -> dict[str, Any]:
    """Build the ``{"entries": [...]}`` wrapper schema.

    Parameters
    ----------
    field : dict
        Field definition from the context contract.
    item_schema : dict
        JSON Schema fragment for one entry.

    Returns
    -------
    dict
        JSON Schema fragment for a Cookiecutter array wrapper.
    """
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["entries"],
        "properties": {
            "entries": {
                "type": "array",
                "items": copy.deepcopy(item_schema),
            },
        },
        "default": {"entries": field.get("default", [])},
    }
    return with_common_metadata(field, schema)


def field_schema(field: dict[str, Any]) -> dict[str, Any]:
    """Build a JSON Schema fragment for one contract field.

    Parameters
    ----------
    field : dict
        Field definition from the context contract.

    Returns
    -------
    dict
        JSON Schema fragment.
    """
    if "schema" in field:
        return with_common_metadata(field, field["schema"])

    field_type = field["type"]
    if field_type == "choice":
        return with_common_metadata(
            field,
            {
                "type": "string",
                "enum": field["choices"],
            },
        )

    if field_type == "string":
        return with_common_metadata(field, {"type": "string"})

    if field_type == "string_array":
        item_schema = field.get("item_schema", {"type": "string"})
        return entries_schema(field, item_schema)

    if field_type == "object_array":
        entry_schema_name = field["entry_schema"]
        return entries_schema(field, {"$ref": f"#/$defs/{entry_schema_name}"})

    raise ValueError(f"Unsupported context field type: {field_type}")


def template_schema_conditions(contract: dict[str, Any]) -> list[dict[str, Any]]:
    """Build language-conditional field constraints.

    Parameters
    ----------
    contract : dict
        Parsed context contract.

    Returns
    -------
    list[dict]
        JSON Schema ``if``/``then`` conditions grouped by template language.
    """
    template_properties: dict[str, dict[str, Any]] = {}
    for field in contract["fields"]:
        for template, fragment in field.get("template_schemas", {}).items():
            template_properties.setdefault(template, {})[field["name"]] = copy.deepcopy(
                fragment
            )

    return [
        {
            "if": {
                "properties": {"language": {"const": template}},
                "required": ["language"],
            },
            "then": {"properties": properties},
        }
        for template, properties in sorted(template_properties.items())
    ]


def build_schema(contract: dict[str, Any]) -> dict[str, Any]:
    """Build a JSON Schema from a template context contract.

    Parameters
    ----------
    contract : dict
        Parsed context contract.

    Returns
    -------
    dict
        JSON Schema document.
    """
    required = [
        field["name"]
        for field in contract["fields"]
        if field.get("required")
    ]
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://lumc-dcc.github.io/cookiecutter-templates/template_context.schema.json",
        "title": "LUMC cookiecutter template context",
        "description": contract["description"],
        "type": "object",
        "additionalProperties": False,
        "properties": {
            field["name"]: field_schema(field)
            for field in contract["fields"]
        },
        "$defs": copy.deepcopy(contract.get("entry_schemas", {})),
    }
    if required:
        schema["required"] = required
    conditions = template_schema_conditions(contract)
    if conditions:
        schema["allOf"] = conditions
    return schema


def load_contract(path: Path) -> dict[str, Any]:
    """Load a context contract.

    Parameters
    ----------
    path : pathlib.Path
        Contract JSON path.

    Returns
    -------
    dict
        Parsed contract.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def write_schema(schema: dict[str, Any], path: Path) -> None:
    """Write a generated JSON Schema document.

    Parameters
    ----------
    schema : dict
        JSON Schema document.
    path : pathlib.Path
        Destination path.
    """
    path.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    """Run the command-line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    write_schema(build_schema(load_contract(args.contract)), args.output)


if __name__ == "__main__":
    main()
