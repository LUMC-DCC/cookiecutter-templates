"""Tests for the service-agnostic template context contract.

These tests keep the central contract, generated Cookiecutter context, field
usage map, and generated contract documentation aligned.
"""

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "_contracts" / "template_context.json"
FIELD_USAGE_PATH = ROOT / "_contracts" / "field_usage.json"
COOKIECUTTER_CONTEXT_PATH = ROOT / "_cc_shared" / "cookiecutter.json"
GENERATOR_PATH = ROOT / "_scripts" / "build_cookiecutter_context.py"
CONTEXT_SCHEMA_GENERATOR_PATH = ROOT / "_scripts" / "build_context_schema.py"
CONTEXT_SCHEMA_PATH = ROOT / "_contracts" / "template_context.schema.json"
FIELD_DOC_GENERATOR_PATH = ROOT / "_scripts" / "build_field_usage_docs.py"
FIELD_USAGE_AUDIT_PATH = ROOT / "_scripts" / "audit_field_usage_status.py"
FIELD_USAGE_DOC_PATH = ROOT / "_docs" / "contract" / "field-usage.md"
VALIDATION_PATH = (
    ROOT
    / "_cc_shared"
    / "template_hooks"
    / "post_generation"
    / "validation.py"
)


def load_generator():
    """Load the Cookiecutter context builder module.

    Returns
    -------
    module
        Imported ``build_cookiecutter_context`` module.
    """
    spec = importlib.util.spec_from_file_location(
        "build_cookiecutter_context",
        GENERATOR_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_field_doc_generator():
    """Load the field usage documentation builder module.

    Returns
    -------
    module
        Imported ``build_field_usage_docs`` module.
    """
    spec = importlib.util.spec_from_file_location(
        "build_field_usage_docs",
        FIELD_DOC_GENERATOR_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_context_schema_generator():
    """Load the template context schema builder module.

    Returns
    -------
    module
        Imported ``build_context_schema`` module.
    """
    spec = importlib.util.spec_from_file_location(
        "build_context_schema",
        CONTEXT_SCHEMA_GENERATOR_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_field_usage_audit():
    """Load the field usage status audit module.

    Returns
    -------
    module
        Imported ``audit_field_usage_status`` module.
    """
    spec = importlib.util.spec_from_file_location(
        "audit_field_usage_status",
        FIELD_USAGE_AUDIT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_context_validator():
    """Load the template-specific context validator module.

    Returns
    -------
    module
        Imported post-generation validation module.
    """
    spec = importlib.util.spec_from_file_location(
        "template_context_validation",
        VALIDATION_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_contract():
    """Load the template context contract.

    Returns
    -------
    dict
        Parsed contract data.
    """
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def load_field_usage():
    """Load the field usage map.

    Returns
    -------
    dict
        Parsed usage map.
    """
    return json.loads(FIELD_USAGE_PATH.read_text(encoding="utf-8"))


def test_context_contract_has_unique_fields():
    """Ensure every public context field has one canonical definition."""
    contract = load_contract()
    field_names = [field["name"] for field in contract["fields"]]

    assert len(field_names) == len(set(field_names))


def test_cookiecutter_context_is_generated_from_contract():
    """Ensure the shared Cookiecutter context is derived from the contract."""
    contract = load_contract()
    expected = load_generator().build_context(contract)
    actual = json.loads(COOKIECUTTER_CONTEXT_PATH.read_text(encoding="utf-8"))

    assert actual == expected


def test_context_schema_is_generated_from_contract():
    """Ensure the integrator-facing schema is derived from the contract."""
    contract = load_contract()
    expected = load_context_schema_generator().build_schema(contract)
    actual = json.loads(CONTEXT_SCHEMA_PATH.read_text(encoding="utf-8"))

    assert actual == expected


def test_template_cookiecutter_contexts_use_template_defaults():
    """Ensure language templates get their own Cookiecutter defaults."""
    contract = load_contract()
    generator = load_generator()

    for template in load_field_usage()["templates"]:
        path = ROOT / template / "cookiecutter.json"
        expected = generator.build_context(contract, template=template)
        actual = json.loads(path.read_text(encoding="utf-8"))

        assert actual == expected

    python_context = generator.build_context(contract, template="python")
    r_context = generator.build_context(contract, template="r")

    assert python_context["language"][0] == "python"
    assert r_context["language"][0] == "r"
    assert python_context["project_slug"] == "my_awesome_project"
    assert r_context["project_slug"] == "my.awesome.project"
    assert python_context["documentation_builder"][0] == "sphinx"
    assert r_context["documentation_builder"][0] == "pkgdown"
    assert "pkgdown" in python_context["documentation_builder"]
    assert "sphinx" in r_context["documentation_builder"]
    assert python_context["_template_defaults"]["documentation_builder"] == "sphinx"
    assert r_context["_template_defaults"]["documentation_builder"] == "pkgdown"
    assert python_context["_template_supported_choices"]["documentation_builder"] == [
        "none",
        "mkdocs",
        "sphinx",
    ]
    assert r_context["_template_supported_choices"]["documentation_builder"] == [
        "none",
        "pkgdown",
    ]
    assert python_context["test_frameworks"]["entries"] == ["pytest"]
    assert r_context["test_frameworks"]["entries"] == ["testthat"]
    assert python_context["_template_supported_choices"]["test_frameworks"] == [
        "pytest"
    ]
    assert r_context["_template_supported_choices"]["test_frameworks"] == [
        "testthat"
    ]
    assert python_context["formatter_tool"][0] == "ruff"
    assert python_context["linter_tool"][0] == "ruff"
    assert python_context["type_checker"][0] == "none"
    assert python_context["project_manager"][0] == "uv"
    assert r_context["formatter_tool"][0] == "none"
    assert r_context["linter_tool"][0] == "none"
    assert r_context["type_checker"][0] == "none"
    assert r_context["project_manager"][0] == "renv"
    assert python_context["_template_supported_choices"]["formatter_tool"] == [
        "none",
        "ruff",
    ]
    assert python_context["_template_supported_choices"]["linter_tool"] == [
        "none",
        "ruff",
    ]
    assert python_context["_template_supported_choices"]["type_checker"] == [
        "none",
        "mypy",
    ]
    assert python_context["_template_supported_choices"]["project_manager"] == [
        "uv",
        "poetry",
        "pdm",
        "hatch",
        "pixi",
        "pip",
    ]
    assert r_context["_template_supported_choices"]["project_manager"] == [
        "renv",
        "rix",
    ]


def test_project_slug_rules_are_language_specific_and_enforced():
    """Ensure schema clients and hooks share language-specific slug rules."""
    contract = load_contract()
    generator = load_generator()
    schema = load_context_schema_generator().build_schema(contract)
    conditions = {
        condition["if"]["properties"]["language"]["const"]: condition["then"][
            "properties"
        ]["project_slug"]
        for condition in schema["allOf"]
    }

    python_context = generator.build_context(contract, template="python")
    r_context = generator.build_context(contract, template="r")
    assert python_context["_template_schemas"]["project_slug"] == conditions["python"]
    assert r_context["_template_schemas"]["project_slug"] == conditions["r"]

    validator = load_context_validator()
    validator.validate_context(python_context | {"project_slug": "valid_package"})
    validator.validate_context(r_context | {"project_slug": "Valid.Package"})

    with pytest.raises(ValueError, match="Invalid 'project_slug'.*python"):
        validator.validate_context(python_context | {"project_slug": "invalid-name"})
    with pytest.raises(ValueError, match="Invalid 'project_slug'.*r"):
        validator.validate_context(r_context | {"project_slug": "invalid_name"})


def test_template_supported_choices_and_defaults_are_valid():
    """Ensure template-specific supported choices and defaults are valid."""
    contract = load_contract()
    templates = load_field_usage()["templates"]

    for field in contract["fields"]:
        global_choices = set(
            field.get("choices", field.get("item_schema", {}).get("enum", []))
        )

        for template, choices in field.get("template_supported_choices", {}).items():
            assert template in templates
            assert set(choices).issubset(global_choices)

        for template, default in field.get("template_defaults", {}).items():
            assert template in templates
            choices = set(
                field.get("template_supported_choices", {}).get(
                    template,
                    field.get("choices", field.get("item_schema", {}).get("enum", [])),
                )
            )
            if choices:
                defaults = default if isinstance(default, list) else [default]
                assert set(defaults).issubset(choices)
            elif "default" in field:
                assert isinstance(default, type(field["default"]))


def test_generated_context_writes_only_when_content_changes(tmp_path):
    """Ensure context generation can run idempotently in hooks."""
    path = tmp_path / "cookiecutter.json"
    context = {"project_name": "Demo"}

    assert load_generator().write_context(context, path) is True
    assert load_generator().write_context(context, path) is False


def test_feature_flags_reference_known_fields():
    """Ensure optional feature flags refer to declared contract fields."""
    contract = load_contract()
    field_names = {field["name"] for field in contract["fields"]}

    for feature in contract["features"]:
        assert feature["flag"] in field_names
        assert feature["template_paths"]


def test_contract_covers_public_research_software_dimensions():
    """Ensure the contract spans the expected public policy dimensions."""
    contract = load_contract()
    categories = {field["category"] for field in contract["fields"]}

    assert {
        "identity",
        "people",
        "funding",
        "motivation",
        "accessibility",
        "licensing",
        "documentation",
        "interoperability",
        "quality",
        "release",
        "reproducibility",
        "sustainability",
        "risk",
        "governance",
    }.issubset(categories)


def test_repeatable_people_fields_are_supported():
    """Ensure people fields render as repeatable context objects."""
    contract = load_contract()
    fields = {field["name"]: field for field in contract["fields"]}
    context = load_generator().build_context(contract)

    for name in ["authors", "maintainers", "principal_investigators"]:
        assert fields[name]["type"] == "object_array"
        assert context[name] == {"entries": []}


def test_person_entries_accept_name_or_structured_parts():
    """Ensure person records do not require duplicate name representations."""
    person_schema = load_contract()["entry_schemas"]["person"]

    assert "required" not in person_schema
    assert {"required": ["name"]} in person_schema["anyOf"]
    assert {"required": ["given_names", "family_names"]} in person_schema["anyOf"]
    assert "role" not in person_schema["properties"]
    assert person_schema["properties"]["affiliation"] == {
        "$ref": "#/$defs/organization"
    }


def test_community_file_fields_are_binary_switches():
    """Ensure community-file options render as binary include switches."""
    contract = load_contract()
    fields = {field["name"]: field for field in contract["fields"]}
    context = load_generator().build_context(contract)
    schema = json.loads(CONTEXT_SCHEMA_PATH.read_text(encoding="utf-8"))

    for name in [
        "include_contributing",
        "include_code_of_conduct",
        "include_governance",
        "include_security",
        "include_support",
        "include_changelog",
    ]:
        assert fields[name]["type"] == "choice"
        assert fields[name]["choices"] == ["yes", "no"]
        assert context[name] == ["yes", "no"]
        assert schema["properties"][name]["type"] == "string"
        assert schema["properties"][name]["enum"] == ["yes", "no"]
        assert "entries" not in schema["properties"][name].get("properties", {})


def test_containerization_types_are_controlled():
    """Ensure integrators receive canonical environment specification types."""
    contract = load_contract()
    container_schema = contract["entry_schemas"]["containerization"]

    assert container_schema["required"] == ["type"]
    assert container_schema["properties"]["type"]["enum"] == [
        "Docker",
        "OCI / Podman",
        "Apptainer / Singularity",
        "Other",
    ]


def test_release_selectors_are_controlled():
    """Ensure release policy and destinations use canonical choices."""
    fields = {field["name"]: field for field in load_contract()["fields"]}

    assert fields["versioning_scheme"]["type"] == "choice"
    assert fields["versioning_scheme"]["choices"] == [
        "SemVer",
        "CalVer",
        "Custom",
    ]
    assert fields["versioning_scheme"]["default"] == "SemVer"
    assert fields["distribution_channels"]["type"] == "string_array"
    assert fields["distribution_channels"]["item_schema"]["enum"] == [
        "PyPI",
        "conda-forge",
        "CRAN",
        "Bioconductor",
        "npm",
        "crates.io",
        "Docker Hub",
        "GitHub Container Registry",
        "Quay",
        "Apptainer Library",
        "BioContainers",
        "GitHub Releases",
        "Zenodo",
        "Institutional archive",
        "Source repository",
        "Self-hosted installer",
        "Hosted service",
        "Other",
    ]


def test_citation_file_field_is_default_on():
    """Ensure CFF citation metadata is controlled by an explicit switch."""
    contract = load_contract()
    fields = {field["name"]: field for field in contract["fields"]}
    context = load_generator().build_context(contract)

    assert fields["include_citation_cff"]["type"] == "choice"
    assert fields["include_citation_cff"]["choices"] == ["yes", "no"]
    assert fields["include_citation_cff"]["default"] == "yes"
    assert context["include_citation_cff"] == ["yes", "no"]


def test_documentation_types_control_documentation_scaffold():
    """Ensure documentation is represented through selected content types."""
    contract = load_contract()
    fields = {field["name"]: field for field in contract["fields"]}

    assert fields["documentation_types"]["type"] == "string_array"


def test_interface_types_are_controlled():
    """Ensure public interface types are controlled for integrators."""
    contract = load_contract()
    interface_schema = contract["entry_schemas"]["interface"]

    assert interface_schema["required"] == ["type"]
    assert interface_schema["properties"]["type"]["enum"] == [
        "Bioinformatics portal",
        "Command-line tool",
        "Database portal",
        "Desktop application",
        "Library",
        "Ontology",
        "Plug-in",
        "Script",
        "SPARQL endpoint",
        "Suite",
        "Web application",
        "Web API",
        "Web service",
        "Workbench",
        "Workflow",
    ]


def test_operating_system_statuses_match_the_smp():
    """Ensure operating-system support labels match the SMP choices."""
    operating_system_schema = load_contract()["entry_schemas"]["operating_system"]

    assert operating_system_schema["required"] == ["name"]
    assert operating_system_schema["properties"]["status"]["enum"] == [
        "Officially supported",
        "Expected to work",
    ]


def test_external_dependencies_require_named_entries():
    """Ensure external dependencies have stable public labels."""
    external_dependency_schema = load_contract()["entry_schemas"]["external_dependency"]

    assert external_dependency_schema["required"] == ["name"]
    assert set(external_dependency_schema["properties"]) == {
        "name",
        "version_constraint",
        "url",
        "license",
        "purpose",
    }


def test_external_services_match_smp_planning_fields():
    """Ensure external service entries follow the SMP item shape."""
    external_service_schema = load_contract()["entry_schemas"]["external_service"]

    assert external_service_schema["required"] == ["name"]
    assert set(external_service_schema["properties"]) == {
        "name",
        "provider",
        "service_types",
        "quantity",
        "cost_coverage",
    }
    assert external_service_schema["properties"]["service_types"]["items"]["enum"] == [
        "Institutional support (DCC, IT, library)",
        "Hosted compute / storage",
        "CI / CD minutes",
        "SaaS subscription",
        "Legal / contractual",
        "External review or audit",
        "Domain expertise",
        "Other",
    ]
    assert external_service_schema["properties"]["cost_coverage"]["items"]["enum"] == [
        "Project budget",
        "Departmental overhead",
        "External grant",
        "Free tier",
        "In-kind / unfunded",
    ]


def test_repeatable_contract_fields_have_controlled_entry_shapes():
    """Ensure ``entries`` fields declare controlled item schemas."""
    contract = load_contract()
    entry_schema_names = set(contract["entry_schemas"])

    for field in contract["fields"]:
        if field["type"] == "object_array":
            assert field["entry_schema"] in entry_schema_names
        if field["type"] == "string_array":
            assert field["item_schema"]["type"] == "string"

    for schema in contract["entry_schemas"].values():
        assert schema["type"] == "object"
        assert schema["additionalProperties"] is False
        assert schema["properties"]


def test_integrator_schema_controls_entries_wrapper():
    """Ensure the JSON Schema keeps nested context values constrained."""
    schema = json.loads(CONTEXT_SCHEMA_PATH.read_text(encoding="utf-8"))
    author_schema = schema["properties"]["authors"]
    documentation_types_schema = schema["properties"]["documentation_types"]

    assert schema["additionalProperties"] is False
    assert "language" in schema["required"]
    assert author_schema["additionalProperties"] is False
    assert author_schema["required"] == ["entries"]
    assert author_schema["properties"]["entries"]["items"] == {"$ref": "#/$defs/person"}
    assert schema["$defs"]["person"]["additionalProperties"] is False
    assert "unexpected_field" not in schema["$defs"]["person"]["properties"]
    assert documentation_types_schema["properties"]["entries"]["items"]["enum"] == [
        "user",
        "deployment",
        "developer",
    ]


def test_every_contract_field_has_usage_mapping():
    """Ensure every contract field is represented in the usage checklist."""
    contract = load_contract()
    usage = load_field_usage()

    contract_fields = {field["name"] for field in contract["fields"]}
    mapped_fields = [field["name"] for field in usage["fields"]]

    assert len(mapped_fields) == len(set(mapped_fields))
    assert set(mapped_fields) == contract_fields


def test_field_usage_entries_are_actionable():
    """Ensure usage entries have valid per-template statuses and guidance."""
    usage = load_field_usage()
    allowed_statuses = set(usage["statuses"])
    templates = set(usage["templates"])

    for field in usage["fields"]:
        assert set(field["statuses"]) == templates
        for status in field["statuses"].values():
            assert status in allowed_statuses
        assert field["targets"]
        assert field["notes"]


def test_field_usage_documentation_targets_are_template_agnostic():
    """Ensure usage targets avoid documentation-engine-specific paths."""
    usage = load_field_usage()

    documentation_paths = []
    for field in usage["fields"]:
        documentation_paths.extend(
            target
            for target in field["targets"]
            if target.startswith("docs/")
        )

    assert documentation_paths == []


def test_field_usage_docs_are_generated_from_usage_map():
    """Ensure generated field usage docs match the maintained usage map."""
    usage = load_field_usage()
    expected = load_field_doc_generator().build_table(usage)
    actual = FIELD_USAGE_DOC_PATH.read_text(encoding="utf-8")

    assert actual == expected


def test_field_usage_statuses_match_template_references():
    """Ensure referenced fields are not still marked as only planned."""
    errors = load_field_usage_audit().audit_usage(
        load_contract(),
        load_field_usage(),
        ROOT,
    )

    assert errors == []
