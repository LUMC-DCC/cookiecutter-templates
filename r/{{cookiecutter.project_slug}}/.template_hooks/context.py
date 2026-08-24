"""Load rendered Cookiecutter context for post-generation hooks."""

import json


def load_context():
    """Load rendered Cookiecutter values used by cleanup hooks.

    Returns
    -------
    dict
        Rendered context values.
    """
    return json.loads({{cookiecutter | tojson | tojson}})
