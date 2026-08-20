"""FastAPI web application for {{ cookiecutter.project_name }}.

The web adapter serves human-facing pages. Keep page routing and rendering here,
and keep reusable data processing in services.
"""

from fastapi import FastAPI

from {{ cookiecutter.project_slug }}.adapters.web.routes import index


def create_web_app() -> FastAPI:
    """Create and configure the web application.

    Returns
    -------
    fastapi.FastAPI
        Configured web application.
    """
    # Metadata appears in the generated OpenAPI page and browser tooling.
    web = FastAPI(
        title="{{ cookiecutter.project_name }}",
        version="{{ cookiecutter.version }}",
        description="{{ cookiecutter.project_short_description }}",
    )

    # Web routes are registered explicitly so the application surface is easy
    # to inspect as the project grows.
    web.include_router(index.router)

    return web


# ASGI servers can import this object directly.
app = create_web_app()
