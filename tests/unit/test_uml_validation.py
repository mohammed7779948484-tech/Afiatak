from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, SourceRef, ViewSpec
from qa.uml import validate_uml

REF = (SourceRef("synthetic-test-reference"),)


def _model(elements, relations):
    return SemanticModel(
        "synthetic.invalid", "1", tuple(elements), tuple(relations), test_data=True
    )


def _view(diagram_type, elements, relations):
    return ViewSpec(
        "invalid",
        "TEST DATA",
        diagram_type,
        "model.yaml",
        tuple(elements),
        tuple(relations),
        diagram_type,
    )


def test_interaction_order_must_be_positive_integer() -> None:
    elements = [
        SemanticElement("component.a", "A", "component", "Test", source_refs=REF),
        SemanticElement("component.b", "B", "component", "Test", source_refs=REF),
    ]
    relation = SemanticRelation(
        "relation.invalid.message",
        "message",
        "component.a",
        "component.b",
        source_refs=REF,
        metadata={"sequence": "first"},
    )
    diagnostics = validate_uml(
        _model(elements, [relation]),
        _view("sequence", [item.id for item in elements], [relation.id]),
    )
    assert "invalid-message-order" in {item.code for item in diagnostics}


def test_state_rejects_unreachable_state() -> None:
    elements = [
        SemanticElement("state.initial", "Initial", "initial", "Test", source_refs=REF),
        SemanticElement("state.orphan", "Orphan", "state", "Test", source_refs=REF),
    ]
    diagnostics = validate_uml(
        _model(elements, []),
        _view("state", [item.id for item in elements], []),
    )
    assert "unreachable-state" in {item.code for item in diagnostics}


def test_component_connector_requires_opposite_interfaces() -> None:
    elements = [
        SemanticElement("component.a", "A", "provided_interface", "Test", source_refs=REF),
        SemanticElement("component.b", "B", "provided_interface", "Test", source_refs=REF),
    ]
    relation = SemanticRelation(
        "relation.invalid.connector",
        "connector",
        "component.a",
        "component.b",
        source_refs=REF,
    )
    diagnostics = validate_uml(
        _model(elements, [relation]),
        _view("component", [item.id for item in elements], [relation.id]),
    )
    assert "invalid-interface-connector" in {item.code for item in diagnostics}
