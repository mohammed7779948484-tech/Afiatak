from pathlib import Path

from engine.core.io import load_model
from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, SourceRef
from qa.semantic import validate_model

FIXTURES = Path(__file__).parents[1] / "fixtures"


def test_missing_source_reference_is_rejected() -> None:
    model = load_model(FIXTURES / "invalid" / "missing-source.yaml")
    assert "missing-source-ref" in {item.code for item in validate_model(model)}


def test_dangling_relation_is_rejected() -> None:
    model = load_model(FIXTURES / "invalid" / "dangling-relation.yaml")
    assert "dangling-relation" in {item.code for item in validate_model(model)}


def test_production_relation_requires_product_source() -> None:
    source = SourceRef(source="lecturer-uml-rules", page=6)
    model = SemanticModel(
        model_id="production.test",
        version="1",
        elements=(
            SemanticElement("actor.test", "Actor", "actor", "Test", source_refs=(source,)),
            SemanticElement("uc.test", "Use", "use_case", "Test", source_refs=(source,)),
        ),
        relations=(
            SemanticRelation(
                "relation.test.association",
                "association",
                "actor.test",
                "uc.test",
                source_refs=(source,),
            ),
        ),
    )
    assert "relation-needs-product-source" in {item.code for item in validate_model(model)}
