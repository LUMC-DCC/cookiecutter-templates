"""Integration tests for generated interface adapters."""

{% set interface_types = namespace(values=[]) %}
{% for interface in cookiecutter.interfaces.entries %}
{% if interface.type is defined and interface.type %}
{% set _ = interface_types.values.append(interface.type) %}
{% endif %}
{% endfor %}
{% set has_cli = "Command-line tool" in interface_types.values %}
{% set has_api = "Web API" in interface_types.values or "SPARQL endpoint" in interface_types.values %}
{% set has_soap = "Web service" in interface_types.values %}
{% set has_script = "Script" in interface_types.values %}
{% if has_script %}
import importlib.util
from pathlib import Path

{% endif %}
{% if has_soap %}
from wsgiref.util import setup_testing_defaults

{% endif %}
{% if has_api or has_cli or has_soap %}
import pytest

{% endif %}
from {{ cookiecutter.project_slug }}.services.processing import process_text


def test_service_integration_path_processes_text():
    """Ensure the reusable service path behaves consistently."""
    assert process_text("abc").output_text == "ABC"


{% if has_cli %}
def test_cli_command_reuses_service_layer():
    """Ensure CLI command logic delegates to the service layer."""
    pytest.importorskip("typer")

    from {{ cookiecutter.project_slug }}.adapters.cli.commands.process import (
        run as run_cli_process,
    )

    assert run_cli_process("abc") == "ABC"


{% endif %}
{% if has_api %}
def test_api_application_registers_routes():
    """Ensure the generated API application registers expected routes."""
    pytest.importorskip("fastapi")

    from {{ cookiecutter.project_slug }}.adapters.api.app import create_app

    app = create_app()
    paths = set(app.openapi()["paths"])

    assert "/health" in paths
{% if "Web API" in interface_types.values %}
    assert "/process" in paths
{% endif %}
{% if "SPARQL endpoint" in interface_types.values %}
    assert "/sparql" in paths
{% endif %}


{% endif %}
{% if has_soap %}
def test_soap_application_publishes_wsdl():
    """Ensure the SOAP service exposes a usable WSDL contract."""
    pytest.importorskip("spyne")
    pytest.importorskip("a2wsgi")

    from {{ cookiecutter.project_slug }}.adapters.soap.app import app, wsgi_app

    assert callable(app)

    environ = {}
    setup_testing_defaults(environ)
    environ.update(
        {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/",
            "QUERY_STRING": "wsdl",
        }
    )
    response = {}

    def start_response(status, headers, exc_info=None):
        """Capture the WSGI status and headers for assertions."""
        response["status"] = status
        response["headers"] = headers

    body = b"".join(wsgi_app(environ, start_response))

    assert response["status"] == "200 OK"
    assert b"<wsdl:definitions" in body
    assert b'operation name="process"' in body


{% endif %}
{% if has_script %}
def test_example_script_can_run_without_cli_process():
    """Ensure the generated script delegates to package code."""
    script_path = Path(__file__).parents[1] / "scripts" / "run_example.py"
    spec = importlib.util.spec_from_file_location("run_example", script_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.process_text("abc").output_text == "ABC"
{% endif %}
