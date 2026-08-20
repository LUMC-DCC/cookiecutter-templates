"""Workflow entry point for {{ cookiecutter.project_name }}.

The pipeline module coordinates workflow steps in order. It should stay thin:
call step functions, pass configuration, and return a structured result. Put
reusable domain logic in ``services`` so workflow orchestration remains focused
on ordering and data flow.
"""

from {{ cookiecutter.project_slug }}.workflows.config import WorkflowConfig
from {{ cookiecutter.project_slug }}.workflows.steps import (
    WorkflowInput,
    WorkflowResult,
    process_step,
)


def run_workflow(
    text: str = "{{ cookiecutter.project_name }}",
    config: WorkflowConfig | None = None,
) -> WorkflowResult:
    """Run the default text-processing workflow.

    Parameters
    ----------
    text : str, default="{{ cookiecutter.project_name }}"
        Text value passed into the first workflow step.
    config : WorkflowConfig | None, optional
        Runtime workflow configuration. When ``None``, default settings are
        created for this run.

    Returns
    -------
    WorkflowResult
        Structured workflow result.
    """
    # Create defaults inside the function so future mutable settings do not
    # become shared across workflow runs.
    selected_config = WorkflowConfig() if config is None else config

    # The pipeline converts raw inputs into a typed payload before handing them
    # to a step. That keeps the step signature stable as the workflow grows.
    result = process_step(WorkflowInput(text=text, config=selected_config))
    return WorkflowResult(
        input_text=result.input_text,
        output_text=result.output_text,
    )
