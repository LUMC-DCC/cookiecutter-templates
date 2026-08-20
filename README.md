# LUMC research software templates

Service-agnostic Cookiecutter templates for creating maintainable, FAIR
research software repositories. The Python template is the current reference
implementation; shared contracts and assets support additional language
templates without coupling generation to a particular upstream service.

## Documentation

- [Use a generated project](https://lumc-dcc.github.io/cookiecutter-templates/users/)
- [Integrate a generation service](https://lumc-dcc.github.io/cookiecutter-templates/integrators/)
- [Develop the templates](https://lumc-dcc.github.io/cookiecutter-templates/developers/)
- [Understand the architecture](https://lumc-dcc.github.io/cookiecutter-templates/architecture/)

## Development

```bash
poetry install --with docs,dev
poetry run pre-commit install
poetry run pre-commit run --all-files
poetry run pytest
poetry run python _scripts/check_generated_docs.py
poetry run mkdocs build --strict
```
