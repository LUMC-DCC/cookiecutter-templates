"""FastAPI portal application for {{ cookiecutter.project_name }}.

The portal adapter exposes browsable project records and summaries. It is kept
separate from the generic web app so portal-specific models, routes, and data
access can evolve without crowding simpler page routes.
"""

from fastapi import FastAPI

from {{ cookiecutter.project_slug }}.adapters.portal.routes import index, records


def create_portal_app() -> FastAPI:
    """Create and configure the portal application.

    Returns
    -------
    fastapi.FastAPI
        Configured portal application.
    """
    # Portal metadata is intentionally explicit because portals are often
    # indexed, linked, or embedded by external research infrastructure.
    portal = FastAPI(
        title="{{ cookiecutter.project_name }} portal",
        version="{{ cookiecutter.version }}",
        description="{{ cookiecutter.project_short_description }}",
    )

    # Register portal route modules here. Add new route modules when new portal
    # record types or views are introduced.
    portal.include_router(index.router)
    portal.include_router(records.router)

    return portal


# ASGI servers can import this object directly.
app = create_portal_app()
