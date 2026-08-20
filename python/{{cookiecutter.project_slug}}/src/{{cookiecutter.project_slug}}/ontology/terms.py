"""Ontology term models for {{ cookiecutter.project_name }}.

Terms are kept as simple Python objects so they can be tested and reviewed
before they are serialized as RDF. Larger projects can extend this module with
synonyms, mappings, examples, or provenance fields.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OntologyTerm:
    """Ontology term definition.

    Parameters
    ----------
    identifier : str
        Local term identifier.
    label : str
        Human-readable term label.
    description : str
        Term description.
    """

    identifier: str
    label: str
    description: str


def default_terms() -> list[OntologyTerm]:
    """Return the starter ontology terms for this project.

    Returns
    -------
    list[OntologyTerm]
        Starter term definitions.
    """
    # The generated term gives the ontology document a concrete example and
    # makes the serializer/test path usable immediately.
    return [
        OntologyTerm(
            identifier="example",
            label="{{ cookiecutter.project_name }} example",
            description="{{ cookiecutter.project_short_description }}",
        )
    ]
