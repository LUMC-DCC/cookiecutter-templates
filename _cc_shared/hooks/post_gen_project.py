import os
import shutil
import json


def is_yes(ctx, value):
    """Check if the value is a 'yes' equivalent."""
    return ctx.get(value, "").strip().lower() in (
        "yes", "y", "true", "1", "on", "enabled", "include"
    )

def is_no(ctx, value):
    """Check if the value is a 'no' equivalent."""
    return ctx.get(value, "").strip().lower() in (
        "no", "n", "false", "0", "none", ""
    )


OPTIONAL_PATHS = [
    {
        "path": "docs",
        "should_remove": lambda ctx: is_no(ctx, "include_docs")
    },
    {
        "path": "tests",
        "should_remove": lambda ctx: is_no(ctx, "include_tests")
    },
    {
        "path": "github",
        "should_remove": lambda ctx: is_no(ctx, "using_ci")
    },
    {
        "path": "LICENSE.txt",
        "should_remove": lambda ctx: is_no(ctx, "license")
    },
    {
        "path": "src/{project_slug}/adapters/api",
        "should_remove": lambda ctx: is_no(ctx, "api")
    },
    {
        "path": "src/{project_slug}/adapters/cli",
        "should_remove": lambda ctx: is_no(ctx, "cli")
    },
    {
        "path": "src/{project_slug}/adapters",
        "should_remove": lambda ctx: is_no(ctx, "api") and is_no(ctx, "cli")
    },
    {
        "path": "src/{project_slug}/services",
        "should_remove": lambda ctx: is_no(ctx, "api") and is_no(ctx, "cli")
    },
]

def load_context():
    return {
        "include_docs": "{{ cookiecutter.include_docs }}",
        "include_tests": "{{ cookiecutter.include_tests }}",
        "using_ci": "{{ cookiecutter.using_ci }}",
        "license": "{{ cookiecutter.license }}",
        "project_slug": "{{ cookiecutter.project_slug }}",
        "api": "{{ cookiecutter.using_api }}",
        "cli": "{{ cookiecutter.using_cli }}",
    }

ALWAYS_REMOVE_PATHS = [
    "licenses",
]

def remove_path(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        print(f"[INFO] Removed {path}")
    else:
        print(f"[SKIP] {path} does not exist")


def cleanup():
    ctx = load_context()
    cwd = os.getcwd()

    for entry in OPTIONAL_PATHS:
        if entry["should_remove"](ctx):
            rendered_path = entry["path"].format(**ctx)
            target = os.path.join(cwd, rendered_path)
            print(f"[INFO] Removing {rendered_path}")
            remove_path(target)

    for rel_path in ALWAYS_REMOVE_PATHS:
        target = os.path.join(cwd, rel_path)
        print(f"[INFO] Removing always-remove path: {rel_path}")
        remove_path(target)


if __name__ == '__main__':
    cleanup()