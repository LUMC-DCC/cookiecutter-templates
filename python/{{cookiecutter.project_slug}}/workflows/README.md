# Workflows

This directory contains workflow material for {{ (cookiecutter.project_name or cookiecutter.project_slug) }}.

## Current workflow

The current Python workflow accepts text input, processes it through the
project service layer, and returns a structured result.

```python
from {{ cookiecutter.project_slug }}.workflows.pipeline import run_workflow

result = run_workflow("example input")
print(result.output_text)
```

## Contents

| Path | Contents |
| ---- | -------- |
| `definitions/` | Engine-specific workflow definitions for this project. |
| `examples/example_input.txt` | Minimal example input for smoke tests and demonstrations. |
| `src/{{ cookiecutter.project_slug }}/workflows/` | Importable Python workflow code. |
