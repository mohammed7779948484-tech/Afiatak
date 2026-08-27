from pathlib import Path

from jsonschema import validate

from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, SourceRef, ViewSpec
from qa.uml import validate_uml


REF = (SourceRef("synthetic-test-reference"),)


def _component_model(elements, relations):
    return SemanticModel("synthetic.component", "1", tuple(elements), tuple(relations), test_data=True)


def _component_view(elements, relations):
    return ViewSpec(
        "synthetic-component",
        "Synthetic Component",
        "component",
        "model.yaml",
        tuple(elements),
        tuple(relations),
        "lecturer-component",
    )


def test_view_schema_accepts_component_diagram_type() -> None:
    schema = load_yaml(ROOT / "engine" / "schemas" / "view.schema.json")
    validate(
        {
            "id": "synthetic-component",
            "title": "Synthetic Component",
            "diagramType": "component",
            "model": "model.yaml",
            "include": ["component.synthetic.backend"],
        },
        schema,
    )


def test_component_required_interface_must_declare_component_owner() -> None:
    backend = SemanticElement(
        "component.synthetic.backend", "Backend", "component", "Test", source_refs=REF
    )
    persistence = SemanticElement(
        "component.synthetic.persistence", "Persistence", "provided_interface", "Test", source_refs=REF
    )
    required = SemanticElement(
        "component.synthetic.persistence-required", "Persistence", "required_interface", "Test", source_refs=REF
    )
    connector = SemanticRelation(
        "relation.synthetic.persistence-connector",
        "connector",
        persistence.id,
        required.id,
        source_refs=REF,
    )
    diagnostics = validate_uml(
        _component_model([backend, persistence, required], [connector]),
        _component_view([backend.id, persistence.id, required.id], [connector.id]),
    )
    assert "required-interface-owner" in {item.code for item in diagnostics}


def test_component_required_interface_owner_must_be_a_visible_component() -> None:
    backend = SemanticElement(
        "component.synthetic.backend", "Backend", "component", "Test", source_refs=REF
    )
    persistence = SemanticElement(
        "component.synthetic.persistence", "Persistence", "provided_interface", "Test", source_refs=REF
    )
    required = SemanticElement(
        "component.synthetic.persistence-required",
        "Persistence",
        "required_interface",
        "Test",
        source_refs=REF,
        metadata={"ownerComponent": "component.synthetic.missing"},
    )
    connector = SemanticRelation(
        "relation.synthetic.persistence-connector",
        "connector",
        persistence.id,
        required.id,
        source_refs=REF,
    )
    diagnostics = validate_uml(
        _component_model([backend, persistence, required], [connector]),
        _component_view([backend.id, persistence.id, required.id], [connector.id]),
    )
    assert "required-interface-owner" in {item.code for item in diagnostics}
