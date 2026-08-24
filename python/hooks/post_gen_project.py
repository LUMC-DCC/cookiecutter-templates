"""Finalize generated project files after Cookiecutter rendering.

The entry point keeps orchestration small and delegates domain-specific cleanup
to helper modules in the temporary ``.template_hooks`` directory.
"""

import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(os.getcwd()) / ".template_hooks"))

from context import load_context
from post_generation.community_files import select_community_files
from post_generation.containerization import select_container_recipes
from post_generation.documentation import select_documentation_builder
from post_generation.license_integration import update_license_integrations
from post_generation.optional_files import (
    remove_optional_paths,
    remove_template_only_paths,
)
from post_generation.project_management import configure_project_manager
from post_generation.public_files import update_public_context
from post_generation.quality import select_quality_tools
from post_generation.repository_files import render_repository_files
from post_generation.testing import select_test_framework
from post_generation.validation import validate_context


def cleanup():
    """Run all post-generation actions."""
    ctx = load_context()
    cwd = Path(os.getcwd())

    validate_context(ctx)
    select_documentation_builder(ctx, cwd)
    select_container_recipes(ctx, cwd)
    select_community_files(ctx, cwd)
    spdx_id = render_repository_files(ctx, cwd)
    update_license_integrations(cwd, spdx_id)
    update_public_context(ctx, cwd)
    configure_project_manager(ctx, cwd)
    select_quality_tools(ctx, cwd)
    select_test_framework(ctx, cwd)
    remove_optional_paths(ctx, cwd)
    remove_template_only_paths(cwd)


if __name__ == "__main__":
    cleanup()
