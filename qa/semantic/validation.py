from __future__ import annotations

from engine.core.ids import validate_id
from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


def validate_model(model: SemanticModel) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    ids: set[str] = set()
    registered_sources = {
        item["name"] for item in load_yaml(ROOT / "registry" / "sources.yaml")["sources"]
    }

    def check_refs(subject, refs, kind):
        if not refs:
            diagnostics.append(
                Diagnostic("Q2", "missing-source-ref", f"{kind} has no provenance", subject=subject)
            )
            return
        for ref in refs:
            synthetic = model.test_data and ref.source.startswith("synthetic-")
            if ref.source not in registered_sources and not synthetic:
                diagnostics.append(
                    Diagnostic(
                        "Q2", "unknown-source-ref", "Source is not registered", subject=subject
                    )
                )
            if ref.line_start and ref.line_end and ref.line_end < ref.line_start:
                diagnostics.append(
                    Diagnostic(
                        "Q2",
                        "invalid-source-range",
                        "line_end precedes line_start",
                        subject=subject,
                    )
                )

    for element in model.elements:
        if not validate_id(element.id):
            diagnostics.append(
                Diagnostic("Q1", "invalid-id", "ID violates namespace policy", subject=element.id)
            )
        if element.id in ids:
            diagnostics.append(
                Diagnostic("Q1", "duplicate-id", "Duplicate semantic ID", subject=element.id)
            )
        ids.add(element.id)
        check_refs(element.id, element.source_refs, "Element")
    for relation in model.relations:
        if not validate_id(relation.id):
            diagnostics.append(
                Diagnostic("Q1", "invalid-id", "ID violates namespace policy", subject=relation.id)
            )
        if relation.id in ids:
            diagnostics.append(
                Diagnostic("Q1", "duplicate-id", "Duplicate semantic ID", subject=relation.id)
            )
        ids.add(relation.id)
        if relation.source not in model.by_id or relation.target not in model.by_id:
            diagnostics.append(
                Diagnostic(
                    "Q3", "dangling-relation", "Relation endpoint is undefined", subject=relation.id
                )
            )
        check_refs(relation.id, relation.source_refs, "Relation")
        if (
            not model.test_data
            and relation.source_refs
            and not any(
                ref.source == "aafiatak-product-specification" for ref in relation.source_refs
            )
        ):
            diagnostics.append(
                Diagnostic(
                    "Q2",
                    "relation-needs-product-source",
                    "Production relations require product-spec provenance",
                    subject=relation.id,
                )
            )
        if (
            relation.type in {"include", "extend", "generalization", "aggregation", "composition"}
            and not relation.rationale
        ):
            diagnostics.append(
                Diagnostic(
                    "Q2",
                    "missing-rationale",
                    "Derived UML relation requires rationale",
                    subject=relation.id,
                )
            )
    return diagnostics


def validate_view(model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    ids = set(model.by_id)
    relation_ids = {relation.id for relation in model.relations}
    for item in view.include:
        if item not in ids:
            diagnostics.append(
                Diagnostic(
                    "Q1",
                    "undefined-view-element",
                    "View references an undefined element",
                    subject=item,
                )
            )
    for item in view.relations:
        if item not in relation_ids:
            diagnostics.append(
                Diagnostic(
                    "Q1",
                    "undefined-view-relation",
                    "View references an undefined relation",
                    subject=item,
                )
            )
    return diagnostics
